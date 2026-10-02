# Derived API from ktool/lib0cyn; Copyright (c) 0cyn 2022, MIT in LICENSE.
# Packing, layout validation and instance state rewritten for ImageQuay.
"""Finite record layouts with exact decoding and symmetric field encoding.

Schemas describe bytes; they do not hold decoded state. Each instance owns its
bitfields. Nested records inherit byte order and pointer width. Invalid schemas,
short data and values outside a field raise exceptions without terminating the
calling process. Compatibility spellings remain at the public name boundary.
"""
import enum as quay_enum
import inspect as quay_inspect
import re as quay_re
from typing import List as quay_List
from types import MappingProxyType
import imagequay_boundary as _name_boundary

quay_ansi_escape = quay_re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
quay_type_mask, quay_size_mask = 0xFFFF0000, 0xFFFF
quay_type_uint, quay_type_sint, quay_type_str, quay_type_bytes = 0, 0x10000, 0x20000, 0x30000
quay_uint8_t, quay_uint16_t, quay_uint32_t, quay_uint64_t = 1, 2, 4, 8
quay_int8_t, quay_int16_t, quay_int32_t, quay_int64_t = [quay_type_sint | n for n in (1, 2, 4, 8)]
quay_char_t = [quay_type_str | n for n in range(65)]
quay_bytes_t = [quay_type_bytes | n for n in range(65)]
MAX_RECORD_BYTES = 1 << 20
MAX_RECORD_FIELDS = 4096
MAX_RECORD_DEPTH = 64


def quay_strip_ansi(msg):
    return quay_ansi_escape.sub('', msg)


def _order(byte_order):
    if byte_order not in ('little', 'big'):
        raise ValueError('byte_order must be little or big')
    return byte_order


def _pointer_size(ptr_size):
    if type(ptr_size) is not int or ptr_size not in (4, 8):
        raise ValueError('pointer width must be 4 or 8 bytes')
    return ptr_size


def _width(size):
    if type(size) is not int or not 0 <= size <= MAX_RECORD_BYTES:
        raise ValueError('record width exceeds the 1 MiB budget')
    return size


@_name_boundary.class_contract('uintptr_t', {})
class quay_uintptr_t:
    """Pointer-width unsigned field marker."""


@_name_boundary.class_contract('pad_for_64_bit_only', {'size': 'quay_size'})
class quay_pad_for_64_bit_only:
    def __init__(self, size=4):
        self.size = _width(size)


@_name_boundary.class_contract('Bitfield', {n: 'quay_' + n for n in
    ('fields', 'size', 'size_bits', 'decoded_fields', 'decode_bitfield')})
class quay_Bitfield:
    def __init__(self, fields: dict):
        if not isinstance(fields, dict) or not fields or len(fields) > MAX_RECORD_FIELDS:
            raise ValueError('bitfield needs a finite nonempty field dictionary')
        for name, bits in fields.items():
            if not isinstance(name, str) or not name or type(bits) is not int or bits <= 0:
                raise ValueError('bitfield names and widths are invalid')
        total = sum(fields.values())
        if total % 8 or total > 4096:
            raise ValueError('bitfield width must be byte aligned and at most 4096 bits')
        self.fields = MappingProxyType(dict(fields))
        self.size_bits, self.size = total, total // 8
        self.decoded_fields = {}

    def quay_decode_bitfield(self, value, byte_order='little'):
        raw = bytes(value)
        if len(raw) != self.size:
            raise ValueError('bitfield byte count does not match its layout')
        word, position = int.from_bytes(raw, _order(byte_order)), 0
        decoded = {}
        for name, bits in self.fields.items():
            decoded[name] = (word >> position) & ((1 << bits) - 1)
            position += bits
        self.decoded_fields = decoded
        for name, number in decoded.items():
            _name_boundary.write_attribute(self, name, number)
        return dict(decoded)


def _schema(record_class):
    fields = _name_boundary.read_attribute(record_class, 'FIELDS', None)
    if fields is None:
        fields = _name_boundary.read_attribute(record_class, '_FIELDS', None)
    if fields is not None:
        if not hasattr(fields, 'items'):
            raise TypeError('record schema must be an ordered mapping')
        pairs = list(fields.items())
    else:
        names = _name_boundary.read_attribute(record_class, '_FIELDNAMES', None)
        sizes = _name_boundary.read_attribute(record_class, '_SIZES', None)
        if names is None or sizes is None:
            return None
        if len(names) != len(sizes):
            raise ValueError('record field names and widths differ in length')
        pairs = list(zip(names, sizes))
    _field_names(pairs)
    return pairs


def _field_names(pairs):
    if len(pairs) > MAX_RECORD_FIELDS:
        raise ValueError('record field count exceeds the 4096-field budget')
    names = [name for name, _ in pairs]
    if any(not isinstance(name, str) or not name for name in names) or len(set(names)) != len(names):
        raise ValueError('record fields require unique nonempty names')


def _layout(pairs, ptr_size, ancestry=()):
    _field_names(pairs)
    if len(ancestry) > MAX_RECORD_DEPTH:
        raise ValueError('record nesting exceeds the 64-level budget')
    result, offset = [], 0
    for name, spec in pairs:
        if type(spec) is int:
            kind, width = spec & quay_type_mask, spec & quay_size_mask
            if spec < 0 or kind not in (quay_type_uint, quay_type_sint, quay_type_str, quay_type_bytes):
                raise ValueError('unknown scalar record field type')
        elif isinstance(spec, quay_Bitfield):
            kind, width = 'bits', spec.size
        elif isinstance(spec, quay_pad_for_64_bit_only):
            kind, width = 'padding', spec.size if _pointer_size(ptr_size) == 8 else 0
        elif isinstance(spec, type) and issubclass(spec, quay_uintptr_t):
            kind, width = 'pointer', _pointer_size(ptr_size)
        elif isinstance(spec, type) and issubclass(spec, quay_StructUnion):
            kind, width = 'union', _width(_name_boundary.read_attribute(spec, 'SIZE'))
            if spec in ancestry:
                raise ValueError('recursive union record layout')
        elif isinstance(spec, type) and issubclass(spec, quay_Struct):
            if spec in ancestry:
                raise ValueError('recursive record layout')
            nested = _schema(spec)
            kind = 'record'
            width = (sum(item[2] for item in _layout(nested, ptr_size, ancestry + (spec,)))
                     if nested is not None else _width(_name_boundary.read_attribute(spec, 'SIZE')))
        else:
            raise TypeError('unsupported record field descriptor')
        _width(offset + width)
        result.append((name, spec, width, offset, kind))
        offset += width
    return tuple(result)


@_name_boundary.class_contract('StructUnion', {n: 'quay_' + n for n in
    ('size', 'types', 'load_from_bytes', 'raw')})
class quay_StructUnion:
    """Read-only alternative views of the same finite byte region.

    Union views can be smaller than their storage. The original bytes are kept
    for lossless writes; editing a view does not silently choose a union member.
    """
    def __init__(self, size: int, types: quay_List[object]):
        self.size, self.types = _width(size), tuple(types)
        if not self.types or len(self.types) > MAX_RECORD_FIELDS:
            raise ValueError('union must have a finite nonempty member list')
        self._raw = None

    def quay_load_from_bytes(self, data, byte_order='little', ptr_size=8, _depth=0):
        if _depth > MAX_RECORD_DEPTH:
            raise ValueError('union nesting exceeds the 64-level budget')
        raw = bytes(data)
        if len(raw) < self.size:
            raise ValueError('union input is shorter than its layout')
        raw = raw[:self.size]
        _order(byte_order)
        _pointer_size(ptr_size)
        members = {}
        for member in self.types:
            if not isinstance(member, type):
                raise TypeError('union member must be a record or union type')
            if issubclass(member, quay_Struct):
                width = member.size(ptr_size=ptr_size)
                if width > self.size:
                    raise ValueError('union member is wider than its storage')
                decoded = quay_Struct.create_with_bytes(member, raw[:width], byte_order, ptr_size, _depth=_depth+1)
            elif issubclass(member, quay_StructUnion):
                decoded = member()
                if decoded.size > self.size:
                    raise ValueError('nested union is wider than its storage')
                decoded.load_from_bytes(raw, byte_order, ptr_size, _depth=_depth+1)
            else:
                raise TypeError('union member must be a record or union type')
            members[_name_boundary.type_label(member)] = decoded
        self._raw = raw
        for name, decoded in members.items():
            _name_boundary.write_attribute(self, name, decoded)
        return self

    @property
    def quay_raw(self):
        if self._raw is None:
            raise ValueError('union has not been decoded')
        return bytearray(self._raw)

    def __int__(self):
        return int.from_bytes(self.raw, 'little')


def quay__bytes_to_hex(data):
    return data.hex()


def quay__uint_to_int(uint, bits):
    if type(bits) is not int or bits <= 0 or bits > MAX_RECORD_BYTES * 8:
        raise ValueError('signed integer width is invalid')
    if type(uint) is not int or not 0 <= uint < 1 << bits:
        raise ValueError('unsigned input does not fit the signed field')
    return uint - (1 << bits) if uint & (1 << (bits - 1)) else uint


_STRUCT_NAMES = ('StructFieldColorType', 't', 't_base', 't_token', 't_name', 'size',
    'create_with_bytes', 'create_with_values', 'type_name', 'description', 'raw',
    '_default_field_render', 'render_color', 'render_indented', 'serialize',
    'initialized', 'super', '_fields', 'byte_order', '_field_sizes', '_field_offsets',
    '_field_composers', 'off', 'add_field_composer', 'pre_init', 'post_init')


@_name_boundary.class_contract('Struct', {n: 'quay_' + n for n in _STRUCT_NAMES})
class quay_Struct:
    class quay_StructFieldColorType(quay_enum.IntEnum):
        BASETYPE_ITEM, TOKEN_ITEM, NAME_ITEM = 0, 1, 2

    @staticmethod
    def quay_t(ty, text):
        colors = {0: 141, 1: 189, 2: 60}
        return f'\x1b[38;5;{colors[ty]}m{text}\x1b[0m'

    @staticmethod
    def quay_t_base(text):
        return quay_Struct.t(0, text)

    @staticmethod
    def quay_t_token(text):
        return quay_Struct.t(1, text)

    @staticmethod
    def quay_t_name(text):
        return quay_Struct.t(2, text)

    @classmethod
    def quay_size(cls, ptr_size=None):
        pairs = _schema(cls)
        if pairs is None:
            return _width(_name_boundary.read_attribute(cls, 'SIZE'))
        return sum(entry[2] for entry in _layout(pairs, ptr_size, (cls,)))

    def __init__(self, fields=None, sizes=None, byte_order='little'):
        pairs = _schema(type(self))
        if pairs is None:
            if fields is None or sizes is None:
                raise TypeError('Struct requires a record schema')
            fields, sizes = list(fields), list(sizes)
            if len(fields) != len(sizes):
                raise ValueError('record field names and widths differ in length')
            pairs = list(zip(fields, sizes))
        _field_names(pairs)
        # Clone bit descriptors. Definitions are never mutated by a decode.
        pairs = [(name, quay_Bitfield(dict(spec.fields)) if isinstance(spec, quay_Bitfield) else spec)
                 for name, spec in pairs]
        self.initialized, self.super, self.byte_order = False, super(), _order(byte_order)
        self._fields = [name for name, _ in pairs]
        self._field_sizes, self._field_offsets, self._field_composers = dict(pairs), {}, {}
        self._ptr_size, self.off = 8, 0

    @staticmethod
    def quay_create_with_bytes(struct_class, raw, byte_order='little', ptr_size=8, *, _depth=0):
        _order(byte_order)
        _pointer_size(ptr_size)
        if _depth > MAX_RECORD_DEPTH:
            raise ValueError('record nesting exceeds the 64-level budget')
        if not isinstance(struct_class, type) or not issubclass(struct_class, quay_Struct):
            raise TypeError('record class must derive from Struct')
        if not isinstance(raw, (bytes, bytearray, memoryview)):
            raise TypeError('record input must contain bytes')
        instance = struct_class(byte_order=byte_order)
        plan = _layout(list(instance._field_sizes.items()), ptr_size, (struct_class,))
        required = sum(item[2] for item in plan)
        if len(raw) < required:
            raise ValueError(f'record input needs {required} bytes, received {len(raw)}')
        data = bytes(raw[:required])
        instance._ptr_size = ptr_size
        for name, spec, width, offset, kind in plan:
            piece = data[offset:offset+width]
            instance._field_offsets[name] = offset
            if kind == 'bits':
                decoded = spec.decode_bitfield(piece, byte_order)
                for field, value in decoded.items():
                    _name_boundary.write_attribute(instance, field, value)
                continue
            if kind == quay_type_str:
                value = piece.decode('utf-8').replace('\0', '')
            elif kind == quay_type_bytes:
                value = piece
            elif kind == 'record':
                value = quay_Struct.create_with_bytes(spec, piece, byte_order, ptr_size, _depth=_depth+1)
            elif kind == 'union':
                value = spec().load_from_bytes(piece, byte_order, ptr_size, _depth=_depth+1)
            else:
                value = int.from_bytes(piece, byte_order, signed=kind == quay_type_sint)
            _name_boundary.write_attribute(instance, name, value)
        instance.pre_init()
        instance.initialized = True
        instance.post_init()
        return instance

    @staticmethod
    def quay_create_with_values(struct_class, values, byte_order='little', ptr_size=8):
        _order(byte_order)
        _pointer_size(ptr_size)
        instance = struct_class(byte_order=byte_order)
        values = list(values)
        if len(values) != len(instance._fields):
            raise ValueError('record value count does not match its fields')
        instance._ptr_size = ptr_size
        for name, value in zip(instance._fields, values):
            spec = instance._field_sizes[name]
            if isinstance(spec, quay_Bitfield):
                if not isinstance(value, dict) or set(value) != set(spec.fields):
                    raise ValueError('bitfield values must name every declared subfield')
                for field, number in value.items():
                    _name_boundary.write_attribute(instance, field, number)
            else:
                _name_boundary.write_attribute(instance, name, value)
        instance.pre_init()
        # Validate the whole record before exposing an initialized result.
        instance.raw
        instance.initialized = True
        instance.post_init()
        return instance

    @property
    def quay_type_name(self):
        return _name_boundary.type_label(type(self))

    @property
    def quay_description(self):
        return ''

    @property
    def quay_raw(self):
        plan = _layout(list(self._field_sizes.items()), self._ptr_size, (type(self),))
        chunks = []
        for name, spec, width, offset, kind in plan:
            if kind == 'bits':
                word, position = 0, 0
                for field, bits in spec.fields.items():
                    value = _name_boundary.read_attribute(self, field)
                    if not isinstance(value, int) or not 0 <= value < (1 << bits):
                        raise ValueError(f'bitfield {field} does not fit its declared width')
                    word |= value << position
                    position += bits
                piece = word.to_bytes(width, self.byte_order)
            else:
                value = _name_boundary.read_attribute(self, name)
                if kind in ('record', 'union'):
                    if isinstance(value, (bytes, bytearray, memoryview)):
                        piece = bytes(value)
                    elif isinstance(value, spec):
                        piece = bytes(value.raw)
                    else:
                        raise TypeError(f'field {name} has the wrong record type')
                elif kind == quay_type_str:
                    if not isinstance(value, str):
                        raise TypeError(f'field {name} must be text')
                    piece = value.encode('utf-8')
                    if len(piece) > width:
                        raise ValueError(f'field {name} text exceeds its byte width')
                    piece = piece.ljust(width, b'\0')
                elif kind == quay_type_bytes:
                    if not isinstance(value, (bytes, bytearray, memoryview)):
                        raise TypeError(f'field {name} must contain bytes')
                    piece = bytes(value)
                elif isinstance(value, (bytes, bytearray, memoryview)):
                    # The public builder also accepts an already encoded field.
                    # Preserve that capability, checking the full byte width.
                    piece = bytes(value)
                else:
                    if not isinstance(value, int):
                        raise TypeError(f'field {name} must be an integer or exact-width bytes')
                    piece = value.to_bytes(width, self.byte_order, signed=kind == quay_type_sint)
            if len(piece) != width:
                raise ValueError(f'field {name} byte count does not match its layout')
            chunks.append(piece)
        return bytearray(b''.join(chunks))

    def __eq__(self, other):
        if not isinstance(other, quay_Struct) or type(self) is not type(other):
            return False
        try:
            return self.serialize() == other.serialize()
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return str(self)

    def __str__(self):
        return quay_strip_ansi(self.render_color())

    @staticmethod
    def quay__default_field_render(struct, field, indent_size=2, newline_breaks=False):
        spec = struct._field_sizes[field]
        if isinstance(spec, quay_Bitfield):
            pairs = [f'{name}={_name_boundary.read_attribute(struct, name)}' for name in spec.fields]
            return ('\n' + ''.join(' '*(indent_size+2)+p+'\n' for p in pairs)
                    if newline_breaks else ''.join(p+', ' for p in pairs))
        value = _name_boundary.read_attribute(struct, field, spec)
        if isinstance(value, str):
            return struct.t_base(f'"{value}"')
        if isinstance(value, (bytes, bytearray)):
            return struct.t_base(value)
        if isinstance(value, int):
            return struct.t_base(hex(value))
        if isinstance(value, quay_Struct):
            return ('\n' + ' '*(indent_size+2) + value.render_indented(indent_size+2)
                    if newline_breaks else value.render_color())
        return str(value)

    def _render_field(self, field, indent, breaks):
        composer = self._field_composers.get(field, self._default_field_render)
        args = quay_inspect.signature(composer).parameters
        kwargs = {}
        if 'indent_size' in args:
            kwargs['indent_size'] = indent
        if 'newline_breaks' in args:
            kwargs['newline_breaks'] = breaks
        return composer(self, field, **kwargs)

    def quay_render_color(self):
        text = f"{self.t_name(self.type_name)} {self.t_token('{')} "
        for index, field in enumerate(self._fields):
            comma = self.t_token(',') if index+1 != len(self._fields) else ''
            text += f'{self.t_token(field)}{self.t_token("=")}{self._render_field(field, 0, False)}{comma} '
        return text + self.t_token('}')

    def quay_render_indented(self, indent_size=2):
        if type(indent_size) is not int or not 0 <= indent_size <= 4096:
            raise ValueError('render indentation exceeds its budget')
        text = self.t_name(self.type_name) + '\n'
        for field in self._fields:
            text += ' '*indent_size + field + self.t_token('=') + self._render_field(field, indent_size, True) + '\n'
        return text

    def quay_serialize(self):
        result = {'type': self.type_name}
        for field in self._fields:
            spec = self._field_sizes[field]
            if isinstance(spec, quay_Bitfield):
                result[field] = {name: _name_boundary.read_attribute(self, name) for name in spec.fields}
                continue
            value = _name_boundary.read_attribute(self, field)
            if isinstance(value, quay_Struct):
                value = value.serialize()
            elif isinstance(value, (bytes, bytearray, quay_StructUnion)):
                value = (value.raw if isinstance(value, quay_StructUnion) else value).hex()
            elif not isinstance(value, (str, int)):
                value = None
            result[field] = value
        return result

    def quay_add_field_composer(self, field, func):
        if field not in self._fields or not callable(func):
            raise ValueError('field composer requires a known field and callable')
        self._field_composers[field] = func

    def quay_pre_init(self):
        pass

    def quay_post_init(self):
        pass


_name_boundary.module_contract(globals(), {name: 'quay_'+name for name in
    ('int16_t', 'StructUnion', 'int64_t', 'pad_for_64_bit_only', 'ansi_escape',
     'type_sint', 'size_mask', 'type_str', '_bytes_to_hex', 'int8_t', 'int32_t',
     'char_t', 'uint16_t', 'uint64_t', 'uint8_t', 'uint32_t', 'Struct', 'type_mask',
     '_uint_to_int', 'type_bytes', 'inspect', 'List', 'bytes_t', 'strip_ansi',
     'uintptr_t', 'type_uint', 're', 'Bitfield', 'enum')})
