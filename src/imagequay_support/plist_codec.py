# Derived public API from ktool's modified CPython plistlib; retained notices in
# LICENSE and licenses/CPython-plistlib-LICENSE.txt. New finite decoder architecture.
"""Bounded XML and binary property lists, including legacy Data/hex integers.

The decoder owns its XML state and validates binary object regions and reference
DAGs before constructing values. It never resolves XML entities or external DTDs.
Writers use the maintained Python standard library after graph validation. Public
path helpers use ImageQuay's private, atomic output policy and protected input.
"""
import base64
import datetime
import io
import os
import plistlib
import re
import struct
from xml.parsers import expat
import imagequay_boundary as _name_boundary

MAX_PLIST_BYTES = 16 << 20
MAX_PLIST_OBJECTS = 100_000
MAX_PLIST_DEPTH = 128
quay_PlistFormat = plistlib.PlistFormat
FMT_XML, FMT_BINARY = plistlib.FMT_XML, plistlib.FMT_BINARY
quay_UID = plistlib.UID


@_name_boundary.class_contract('InvalidFileException', {})
class quay_InvalidFileException(ValueError):
    """Malformed property list or exhausted decoding budget."""


@_name_boundary.class_contract('Data', {n: 'quay_'+n for n in ('data', 'fromBase64', 'asBase64')})
class quay_Data:
    def __init__(self, data):
        if not isinstance(data, bytes):
            raise TypeError('data must be as bytes')
        if len(data) > MAX_PLIST_BYTES:
            raise ValueError('Data exceeds the 16 MiB byte budget')
        self.data = data

    @classmethod
    def quay_fromBase64(cls, data):
        if isinstance(data, str):
            data = data.encode('ascii')
        return cls(base64.b64decode(b''.join(data.split()), validate=True))

    def quay_asBase64(self, maxlinelength=76):
        if type(maxlinelength) is not int or maxlinelength < 4 or maxlinelength > MAX_PLIST_BYTES:
            raise ValueError('base64 line width must be between 4 and 16 MiB')
        width = maxlinelength // 4 * 3
        return b''.join(base64.b64encode(self.data[start:start+width])+b'\n'
                        for start in range(0, len(self.data), width))

    def __eq__(self, other):
        if isinstance(other, quay_Data):
            return self.data == other.data
        if isinstance(other, bytes):
            return self.data == other
        return NotImplemented

    def __repr__(self):
        return f'Data({self.data!r})'


def _bounded_read(fp):
    result = bytearray()
    while True:
        chunk = fp.read(min(1 << 16, MAX_PLIST_BYTES+1-len(result)))
        if not isinstance(chunk, (bytes, bytearray)):
            raise TypeError('plist input must be a binary stream')
        if not chunk:
            return bytes(result)
        result.extend(chunk)
        if len(result) > MAX_PLIST_BYTES:
            raise quay_InvalidFileException('plist exceeds the 16 MiB input budget')


class _XMLDecoder:
    TAGS = {'plist', 'dict', 'array', 'key', 'string', 'data', 'date', 'integer', 'real', 'true', 'false'}

    def __init__(self, builtin, dict_type):
        self.builtin, self.dict_type = builtin, dict_type
        self.stack, self.root, self.count, self.seen_root = [], None, 0, False

    def begin(self, tag, attrs):
        self.count += 1
        if self.count > MAX_PLIST_OBJECTS or len(self.stack) > MAX_PLIST_DEPTH:
            raise quay_InvalidFileException('XML plist exceeds its object or depth budget')
        if tag not in self.TAGS or (attrs and (tag != 'plist' or attrs != {'version': '1.0'})):
            raise quay_InvalidFileException('unknown plist element or attributes')
        if not self.stack:
            if tag != 'plist' or self.seen_root:
                raise quay_InvalidFileException('XML plist requires one plist root')
            self.seen_root = True
        elif tag == 'plist' or self.stack[-1]['tag'] not in ('plist', 'dict', 'array'):
            raise quay_InvalidFileException('invalid nested plist element')
        if tag == 'key' and (not self.stack or self.stack[-1]['tag'] != 'dict'):
            raise quay_InvalidFileException('key occurs outside a dictionary')
        frame = {'tag': tag, 'text': [], 'values': [], 'key': None, 'keys': set()}
        if tag == 'dict':
            frame['dict'] = self.dict_type()
        self.stack.append(frame)

    def text(self, text):
        if self.stack:
            self.stack[-1]['text'].append(text)
        elif text.strip():
            raise quay_InvalidFileException('text occurs outside the plist root')

    def end(self, tag):
        frame = self.stack.pop()
        if frame['tag'] != tag:
            raise quay_InvalidFileException('unbalanced plist elements')
        text = ''.join(frame['text'])
        if tag in ('plist', 'dict', 'array'):
            if text.strip():
                raise quay_InvalidFileException('text occurs inside a plist container')
            if frame['key'] is not None:
                raise quay_InvalidFileException('dictionary key has no value')
            if tag == 'plist':
                if len(frame['values']) != 1:
                    raise quay_InvalidFileException('plist root must contain exactly one value')
                self.root = frame['values'][0]
                return
            value = frame['dict'] if tag == 'dict' else frame['values']
        elif tag in ('key', 'string'):
            value = text
        elif tag == 'integer':
            integer = text.strip()
            if integer and not re.fullmatch(r'[+-]?(?:0[xX][0-9a-fA-F]+|[0-9]+)', integer):
                raise quay_InvalidFileException('invalid plist integer')
            # Empty values and hexadecimal integers are retained ktool extensions.
            if len(integer) > 64:
                raise quay_InvalidFileException('plist integer text exceeds the 64-character budget')
            value = int(integer, 16 if 'x' in integer.lower() else 10) if integer else 0
            if not -(1 << 63) <= value < 1 << 64:
                raise quay_InvalidFileException('plist integer exceeds 64-bit storage')
        elif tag == 'real':
            value = float(text)
        elif tag == 'data':
            value = base64.b64decode(''.join(text.split()).encode('ascii'), validate=True)
            if not self.builtin:
                value = quay_Data(value)
        elif tag == 'date':
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', text):
                raise quay_InvalidFileException('invalid plist date')
            value = datetime.datetime.strptime(text, '%Y-%m-%dT%H:%M:%SZ')
        else:
            if text.strip():
                raise quay_InvalidFileException('boolean plist value contains text')
            value = tag == 'true'
        parent = self.stack[-1]
        if parent['tag'] == 'dict':
            if tag == 'key':
                if parent['key'] is not None or value in parent['keys']:
                    raise quay_InvalidFileException('duplicate key or missing dictionary value')
                parent['key'] = value
                parent['keys'].add(value)
            else:
                if parent['key'] is None:
                    raise quay_InvalidFileException('dictionary value has no key')
                parent['dict'][parent['key']] = value
                parent['key'] = None
        else:
            parent['values'].append(value)

    def decode(self, raw):
        parser = expat.ParserCreate()
        parser.buffer_text = True
        parser.StartElementHandler, parser.EndElementHandler = self.begin, self.end
        parser.CharacterDataHandler = self.text
        def refuse(*args):
            raise quay_InvalidFileException('XML entity declarations and references are unsupported')
        parser.EntityDeclHandler = refuse
        parser.ExternalEntityRefHandler = refuse
        parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
        parser.Parse(raw, True)
        if not self.seen_root or self.stack:
            raise quay_InvalidFileException('XML plist has no complete root')
        return self.root


class _BinaryDecoder:
    def __init__(self, raw, builtin, dict_type):
        self.raw, self.builtin, self.dict_type = raw, builtin, dict_type

    def decode(self):
        data = self.raw
        if len(data) < 40 or data[:8] != b'bplist00':
            raise quay_InvalidFileException('invalid binary plist header or trailer')
        _, offset_width, ref_width, count, root, table = struct.unpack('>6sBBQQQ', data[-32:])
        if offset_width not in (1, 2, 4, 8) or ref_width not in (1, 2, 4, 8):
            raise quay_InvalidFileException('invalid binary plist offset or reference width')
        if not 1 <= count <= MAX_PLIST_OBJECTS or root >= count or not 8 <= table <= len(data)-32:
            raise quay_InvalidFileException('invalid binary plist object count or table')
        if count*offset_width != len(data)-32-table:
            raise quay_InvalidFileException('binary plist offset table length is inconsistent')
        offsets = [int.from_bytes(data[table+i*offset_width:table+(i+1)*offset_width], 'big') for i in range(count)]
        if len(set(offsets)) != count or any(not 8 <= offset < table for offset in offsets):
            raise quay_InvalidFileException('binary plist object offsets overlap or leave the object area')
        ends = dict(zip(sorted(offsets), sorted(offsets)[1:]+[table]))
        nodes, total_refs = [], 0
        for offset in offsets:
            boundary = ends[offset]
            def take(position, width):
                if width < 0 or position < offset or width > boundary-position:
                    raise quay_InvalidFileException('binary plist object extends beyond its region')
                return data[position:position+width]
            marker = take(offset, 1)[0]
            kind, small, position = marker >> 4, marker & 15, offset+1
            size = small
            if kind in (4, 5, 6, 10, 13) and small == 15:
                integer_marker = take(position, 1)[0]
                if integer_marker >> 4 != 1 or integer_marker & 15 > 3:
                    raise quay_InvalidFileException('invalid binary plist extended length')
                width = 1 << (integer_marker & 15)
                size = int.from_bytes(take(position+1, width), 'big')
                position += 1+width
            refs = ()
            if kind in (10, 13):
                if size > MAX_PLIST_OBJECTS:
                    raise quay_InvalidFileException('binary plist container exceeds its reference budget')
                ref_count = size * (2 if kind == 13 else 1)
                total_refs += ref_count
                if total_refs > MAX_PLIST_OBJECTS:
                    raise quay_InvalidFileException('binary plist exceeds the 100000-reference budget')
                payload = take(position, ref_count*ref_width)
                refs = tuple(int.from_bytes(payload[i*ref_width:(i+1)*ref_width], 'big') for i in range(ref_count))
                if any(reference >= count for reference in refs):
                    raise quay_InvalidFileException('binary plist reference leaves its object table')
                value = None
            elif kind == 0 and small in (0, 8, 9):
                value = {0: None, 8: False, 9: True}[small]
            elif kind == 1 and small <= 4:
                payload = take(position, 1 << small)
                value = int.from_bytes(payload, 'big', signed=small >= 3)
                if not -(1 << 63) <= value < 1 << 64:
                    raise quay_InvalidFileException('binary plist integer exceeds 64-bit storage')
            elif kind == 2 and small in (2, 3):
                value = struct.unpack('>f' if small == 2 else '>d', take(position, 1 << small))[0]
            elif marker == 0x33:
                seconds = struct.unpack('>d', take(position, 8))[0]
                value = datetime.datetime(2001, 1, 1)+datetime.timedelta(seconds=seconds)
            elif kind in (4, 5, 6):
                payload = take(position, size*(2 if kind == 6 else 1))
                if kind == 4:
                    value = payload if self.builtin else quay_Data(payload)
                else:
                    value = payload.decode('ascii' if kind == 5 else 'utf-16be')
            elif kind == 8 and small < 8:
                value = quay_UID(int.from_bytes(take(position, small+1), 'big'))
            else:
                raise quay_InvalidFileException('unsupported binary plist object marker')
            nodes.append((kind, value, refs, size))
        # DFS postorder constructs each reachable node once and rejects cycles.
        states, values, depths = {}, {}, {}
        pending = [(root, False)]
        while pending:
            index, finished = pending.pop()
            kind, scalar, refs, size = nodes[index]
            if finished:
                depth = 1+max((depths[r] for r in refs), default=0)
                if depth > MAX_PLIST_DEPTH:
                    raise quay_InvalidFileException('binary plist exceeds the 128-level depth budget')
                if kind == 10:
                    value = [values[r] for r in refs]
                elif kind == 13:
                    value = self.dict_type()
                    keys = [values[r] for r in refs[:size]]
                    if any(not isinstance(key, str) for key in keys) or len(set(keys)) != len(keys):
                        raise quay_InvalidFileException('binary plist dictionary keys are invalid or duplicate')
                    for key, reference in zip(keys, refs[size:]):
                        value[key] = values[reference]
                else:
                    value = scalar
                values[index], depths[index], states[index] = value, depth, 2
            elif states.get(index) == 1:
                raise quay_InvalidFileException('binary plist contains a reference cycle')
            elif states.get(index) != 2:
                states[index] = 1
                pending.append((index, True))
                pending.extend((reference, False) for reference in reversed(refs))
        return values[root]


def quay_loads(value, *, fmt=None, use_builtin_types=True, dict_type=dict):
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError('plist input must contain bytes')
    if len(value) > MAX_PLIST_BYTES:
        raise quay_InvalidFileException('plist exceeds the 16 MiB input budget')
    raw = bytes(value)
    if fmt is None:
        fmt = FMT_BINARY if raw.startswith(b'bplist00') else FMT_XML
    if fmt not in (FMT_BINARY, FMT_XML):
        raise ValueError(f'Unsupported format: {fmt!r}')
    decoder = _BinaryDecoder(raw, use_builtin_types, dict_type) if fmt == FMT_BINARY else _XMLDecoder(use_builtin_types, dict_type)
    try:
        return decoder.decode() if fmt == FMT_BINARY else decoder.decode(raw)
    except quay_InvalidFileException:
        raise
    except (ValueError, TypeError, OverflowError, IndexError, expat.ExpatError) as error:
        raise quay_InvalidFileException(f'invalid plist: {error}') from error


def quay_load(fp, *, fmt=None, use_builtin_types=True, dict_type=dict):
    return quay_loads(_bounded_read(fp), fmt=fmt, use_builtin_types=use_builtin_types, dict_type=dict_type)


def _writer_value(value, skipkeys):
    active, cache = set(), {}
    count, payload = 0, 0
    def visit(item, depth):
        nonlocal count, payload
        count += 1
        if count > MAX_PLIST_OBJECTS or depth > MAX_PLIST_DEPTH:
            raise ValueError('plist output exceeds its object or depth budget')
        if isinstance(item, quay_Data):
            item = item.data
        if isinstance(item, (str, bytes, bytearray)):
            payload += len(item.encode('utf-8')) if isinstance(item, str) else len(item)
            if payload > MAX_PLIST_BYTES:
                raise ValueError('plist output exceeds its 16 MiB scalar budget')
        if not isinstance(item, (dict, list, tuple)):
            return item
        identity = id(item)
        if identity in active:
            raise ValueError('plist output contains a reference cycle')
        if identity in cache:
            return cache[identity]
        active.add(identity)
        if isinstance(item, dict):
            result = {}
            for key, child in item.items():
                if not isinstance(key, str):
                    if skipkeys:
                        continue
                    raise TypeError('plist dictionary keys must be strings')
                visit(key, depth+1)
                result[key] = visit(child, depth+1)
        else:
            result = [visit(child, depth+1) for child in item]
        active.remove(identity)
        cache[identity] = result
        return result
    return visit(value, 1)


class _BoundedOutput(io.BytesIO):
    def write(self, data):
        if self.tell()+len(data) > MAX_PLIST_BYTES:
            raise ValueError('plist output exceeds the 16 MiB byte budget')
        return super().write(data)


def quay_dumps(value, *, fmt=FMT_XML, skipkeys=False, sort_keys=True):
    if fmt not in (FMT_BINARY, FMT_XML):
        raise ValueError(f'Unsupported format: {fmt!r}')
    stream = _BoundedOutput()
    plistlib.dump(_writer_value(value, skipkeys), stream, fmt=fmt, skipkeys=False, sort_keys=sort_keys)
    return stream.getvalue()


def _write_all(data, fp):
    written = 0
    while written < len(data):
        count = fp.write(data[written:])
        if type(count) is not int or not 0 < count <= len(data)-written:
            raise OSError('plist output stream did not accept its bytes')
        written += count


def quay_dump(value, fp, *, fmt=FMT_XML, sort_keys=True, skipkeys=False):
    _write_all(quay_dumps(value, fmt=fmt, sort_keys=sort_keys, skipkeys=skipkeys), fp)


def quay_readPlist(pathOrFile):
    if isinstance(pathOrFile, (str, bytes, os.PathLike)):
        from imagequay.file_ops import safe_open
        with safe_open(os.fsdecode(pathOrFile), 'rb') as stream:
            return quay_load(stream, use_builtin_types=False)
    return quay_load(pathOrFile, use_builtin_types=False)


def quay_writePlist(value, pathOrFile):
    # Prepare and validate before opening an output stage.
    data = quay_dumps(value)
    if isinstance(pathOrFile, (str, bytes, os.PathLike)):
        from imagequay.file_ops import safe_open
        with safe_open(os.fsdecode(pathOrFile), 'wb') as stream:
            stream.write(data)
    else:
        _write_all(data, pathOrFile)


def quay_readPlistFromBytes(data):
    return quay_loads(data, use_builtin_types=False)


def quay_writePlistToBytes(value):
    return quay_dumps(value)


__all__ = ['readPlist', 'writePlist', 'readPlistFromBytes', 'writePlistToBytes', 'Data',
    'InvalidFileException', 'FMT_XML', 'FMT_BINARY', 'load', 'dump', 'loads', 'dumps', 'UID']
_name_boundary.module_contract(globals(), {name: 'quay_'+name for name in
    ('readPlist', 'writePlist', 'readPlistFromBytes', 'writePlistToBytes', 'Data',
     'InvalidFileException', 'PlistFormat', 'load', 'dump', 'loads', 'dumps', 'UID')})
