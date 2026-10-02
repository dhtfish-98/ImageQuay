"""Record and plist contracts independently checked against struct/plistlib."""
from collections import OrderedDict
import datetime
import io
from pathlib import Path
import plistlib
import random
import struct
import pytest

from imagequay_support import record_engine as records
from imagequay_support import plist_codec as codec
from imagequay_layout import pointer_records


class Signed(records.Struct):
    FIELDS = {'value': records.int32_t}


class Nested(records.Struct):
    FIELDS = {'before': records.uint16_t, 'child': Signed, 'after': records.uint16_t}


class Variable(records.Struct):
    FIELDS = {'pointer': records.uintptr_t, 'padding': records.pad_for_64_bit_only(4), 'last': records.uint16_t}


@pytest.mark.parametrize('order,prefix', [('little', '<'), ('big', '>')])
@pytest.mark.parametrize('number', [-2147483648, -1, 0, 1, 2147483647])
def test_signed_pack_and_nested_order(order, prefix, number):
    packed = struct.pack(prefix+'HiH', 0x1234, number, 0x5678)
    value = records.Struct.create_with_bytes(Nested, packed, order)
    assert value.child.value == number
    assert value.child.byte_order == order
    assert value.raw == packed
    value.child.value = -number if number != -2147483648 else 0
    assert value.raw == struct.pack(prefix+'HiH', 0x1234, value.child.value, 0x5678)
    single = records.Struct.create_with_values(Signed, [number], order)
    assert single.raw == struct.pack(prefix+'i', number)


@pytest.mark.parametrize('count', range(8))
def test_short_records_do_not_synthesize_missing_fields(count):
    with pytest.raises(ValueError, match='needs 8 bytes'):
        records.Struct.create_with_bytes(Nested, b'\0'*count)


def test_variable_layout_is_not_shared_or_cached_across_widths():
    assert Variable.size(4) == 6
    assert Variable.size(8) == 14
    assert Variable.size(4) == 6
    with pytest.raises(ValueError, match='pointer width'):
        Variable.size()
    small = records.Struct.create_with_bytes(Variable, struct.pack('>IH', 0xaabbccdd, 7), 'big', 4)
    large = records.Struct.create_with_bytes(Variable, struct.pack('>QIH', 0xaabbccdd00112233, 0x99, 9), 'big', 8)
    assert small.raw == struct.pack('>IH', 0xaabbccdd, 7)
    assert large.raw == struct.pack('>QIH', 0xaabbccdd00112233, 0x99, 9)
    assert small._field_offsets == {'pointer': 0, 'padding': 4, 'last': 4}
    assert large._field_offsets == {'pointer': 0, 'padding': 8, 'last': 12}


@pytest.mark.parametrize('ptr_size', [0, 1, 16, None, True])
def test_bad_pointer_width_is_an_exception_not_process_exit(ptr_size):
    with pytest.raises(ValueError):
        records.Struct.create_with_bytes(Variable, b'\0'*32, ptr_size=ptr_size)


def test_fixed_bytes_and_text_are_validated_before_record_publication():
    class Text(records.Struct):
        FIELDS = {'name': records.char_t[4], 'data': records.bytes_t[2]}
    item = records.Struct.create_with_values(Text, ['鱼', b'12'])
    assert item.raw == '鱼'.encode()+b'\0'+b'12'
    assert records.Struct.create_with_bytes(Text, item.raw).name == '鱼'
    for values in (['太长', b'12'], ['ok', b'1'], ['ok'], ['ok', b'12', 7]):
        with pytest.raises(ValueError):
            records.Struct.create_with_values(Text, values)
    with pytest.raises(OverflowError):
        records.Struct.create_with_values(Signed, [1 << 31])


def test_schema_validation_and_recursive_type_detection(monkeypatch):
    class Recursive(records.Struct):
        FIELDS = {}
    Recursive.FIELDS['self'] = Recursive
    with pytest.raises(ValueError, match='recursive'):
        Recursive.size()
    class Invalid(records.Struct):
        FIELDS = {'bad': object()}
    with pytest.raises(TypeError):
        Invalid.size()
    class TooWide(records.Struct):
        FIELDS = {'first': records.uint64_t, 'last': records.uint64_t}
    monkeypatch.setattr(records, 'MAX_RECORD_BYTES', 8)
    with pytest.raises(ValueError, match='budget'):
        TooWide.size()


BIT_LAYOUTS = {
    'dyld_chained_ptr_arm64e_rebase': [('target', 43), ('high8', 8), ('next', 11), ('bind', 1), ('auth', 1)],
    'dyld_chained_ptr_arm64e_bind': [('ordinal', 16), ('zero', 16), ('addend', 19), ('next', 11), ('bind', 1), ('auth', 1)],
    'dyld_chained_ptr_64_rebase': [('target', 36), ('high8', 8), ('reserved', 7), ('next', 12), ('bind', 1)],
}


@pytest.mark.parametrize('name,layout', BIT_LAYOUTS.items())
def test_bitfield_roundtrip_masks_and_instance_isolation(name, layout):
    record_type = getattr(pointer_records, name)
    rng = random.Random(112211)
    vectors = [0, 1, 1 << 63, (1 << 64)-1]+[rng.getrandbits(64) for _ in range(128)]
    before = [dict(spec.decoded_fields) for spec in record_type._FIELDS.values() if isinstance(spec, records.Bitfield)]
    instances = []
    for word in vectors:
        raw = struct.pack('<Q', word)
        instance = records.Struct.create_with_bytes(record_type, raw)
        position = 0
        decoded = {}
        for field, bits in layout:
            expected = (word >> position) & ((1 << bits)-1)
            assert getattr(instance, field) == expected
            decoded[field] = expected
            position += bits
        assert instance.raw == raw
        assert list(instance.serialize().values())[1] == decoded
        assert name in str(instance)
        instances.append(instance)
    # Later decoding must not alter earlier data or class-level descriptors.
    assert instances[0].raw == bytes(8)
    assert before == [dict(spec.decoded_fields) for spec in record_type._FIELDS.values() if isinstance(spec, records.Bitfield)]
    assert instances[0]._field_sizes[next(iter(record_type._FIELDS))] is not instances[-1]._field_sizes[next(iter(record_type._FIELDS))]


def test_bitfield_value_writer_and_reject_out_of_width():
    class Bits(records.Struct):
        FIELDS = {'flags': records.Bitfield({'lo': 3, 'hi': 5})}
    value = records.Struct.create_with_values(Bits, [{'lo': 5, 'hi': 20}])
    assert value.raw == bytes([5 | 20 << 3])
    value.lo = 8
    with pytest.raises(ValueError, match='does not fit'):
        value.raw
    with pytest.raises(ValueError):
        records.Struct.create_with_values(Bits, [{'lo': 1}])


def test_union_views_are_exact_and_keep_their_storage():
    raw = struct.pack('<Q', 0xfedcba9876543210)
    union = pointer_records.ChainedPointerArm64E().load_from_bytes(raw)
    assert union.raw == raw and int(union) == 0xfedcba9876543210
    assert union.dyld_chained_ptr_arm64e_rebase.raw == raw
    with pytest.raises(ValueError):
        pointer_records.ChainedPointerArm64E().load_from_bytes(raw[:-1])


@pytest.mark.parametrize('fmt', [codec.FMT_XML, codec.FMT_BINARY])
@pytest.mark.parametrize('value', [
    {'中文': [True, False, 'fish', b'\0\xff', -7, (1 << 64)-1, 1.5]},
    [datetime.datetime(2024, 1, 2, 3, 4, 5), {}, []],
    {'': 0, 'nest': {'empty': '', 'data': b'abc'}},
])
def test_plist_writers_are_stdlib_identical_and_decoders_interoperate(fmt, value):
    encoded = codec.dumps(value, fmt=fmt)
    assert encoded == plistlib.dumps(value, fmt=fmt)
    assert codec.loads(encoded) == value
    assert plistlib.loads(encoded) == value
    assert codec.load(io.BytesIO(encoded), dict_type=OrderedDict) == value


def test_binary_uid_shared_references_and_data_compatibility():
    shared = {'uid': plistlib.UID(0x11223344), 'data': b'abc'}
    data = codec.dumps([shared, shared], fmt=codec.FMT_BINARY)
    decoded = codec.loads(data)
    assert decoded == [shared, shared] and decoded[0] is decoded[1]
    wrapped = codec.loads(data, use_builtin_types=False)
    assert isinstance(wrapped[0]['data'], codec.Data)
    assert wrapped[0]['data'].data == b'abc'
    assert codec.dumps(wrapped, fmt=codec.FMT_BINARY) == data


def test_legacy_data_hex_empty_integer_and_path_helpers(tmp_path):
    xml = b'<plist><array><integer/><integer>0xFa</integer><data>AAE=</data></array></plist>'
    assert codec.loads(xml) == [0, 250, b'\0\1']
    legacy = codec.readPlistFromBytes(xml)
    assert isinstance(legacy[2], codec.Data)
    assert legacy[2].asBase64(8) == b'AAE=\n'
    assert codec.Data.fromBase64(b'AAE=') == b'\0\1'
    destination = tmp_path/'example.plist'
    codec.writePlist({'data': codec.Data(b'abc')}, destination)
    assert codec.readPlist(destination)['data'] == codec.Data(b'abc')
    with pytest.raises(FileExistsError):
        codec.writePlist({}, destination)
    with pytest.raises(ValueError):
        legacy[2].asBase64(0)


@pytest.mark.parametrize('xml', [
    b'<plist/>', b'<plist><integer>1</integer><integer>2</integer></plist>',
    b'<plist><dict><key>x</key></dict></plist>',
    b'<plist><dict><string>x</string></dict></plist>',
    b'<plist><dict><key>x</key><true/><key>x</key><false/></dict></plist>',
    b'<plist><array><key>x</key></array></plist>',
    b'<plist><unknown/></plist>', b'<plist><string><array/></string></plist>',
    b'<plist><true>text</true></plist>', b'<plist><data>!invalid!</data></plist>',
    b'<plist><integer>18446744073709551616</integer></plist>',
    b'<!DOCTYPE plist [<!ENTITY x "expanded">]><plist><string>&x;</string></plist>',
    b'<!DOCTYPE plist [<!ENTITY x SYSTEM "file:///etc/passwd">]><plist><string>&x;</string></plist>',
])
def test_invalid_xml_and_entity_payloads_are_rejected(xml):
    with pytest.raises(codec.InvalidFileException):
        codec.loads(xml)


def binary(objects, root=0, refs=1):
    body = b'bplist00'
    offsets = []
    for obj in objects:
        offsets.append(len(body))
        body += obj
    table = len(body)
    width = 1 if table < 256 else 2
    return body+b''.join(offset.to_bytes(width, 'big') for offset in offsets)+struct.pack('>6sBBQQQ', bytes(6), width, refs, len(objects), root, table)


@pytest.mark.parametrize('data', [
    b'bplist00', binary([b'\xa1\x00']),  # self reference
    binary([b'\xa1\x01', b'\xa1\x00']),  # two node cycle
    binary([b'\xa1\x03']),  # out of table reference
    binary([b'\x4f\x13'+struct.pack('>Q', 1 << 50)]),  # oversized data
    binary([b'\x4f\xff']),  # non integer extended length
    binary([b'\x5f\x10\x08abc']),  # overlapping/truncated object
    binary([b'\xd1\x00\x00']),  # dictionary key is not text (also cycles)
    binary([b'\xa0'], root=1),
    binary([b'\xff']),
])
def test_binary_graph_and_object_bounds(data):
    with pytest.raises(codec.InvalidFileException):
        codec.loads(data)


def test_binary_duplicate_keys_and_offset_regions():
    data = binary([b'\xd2\x01\x01\x02\x03', b'\x51x', b'\x08', b'\x09'])
    with pytest.raises(codec.InvalidFileException, match='duplicate'):
        codec.loads(data)
    data = bytearray(binary([b'\x08', b'\x09']))
    # Point the second offset at the first offset.
    data[-33] = data[-34]
    with pytest.raises(codec.InvalidFileException, match='offsets'):
        codec.loads(data)


def test_input_output_graph_budgets_and_cycle_fail_before_stream_write(monkeypatch):
    monkeypatch.setattr(codec, 'MAX_PLIST_BYTES', 128)
    with pytest.raises(codec.InvalidFileException):
        codec.load(io.BytesIO(b'x'*129))
    with pytest.raises(ValueError):
        codec.dumps('x'*129)
    with pytest.raises(ValueError):
        codec.dumps('x'*50)  # XML framing alone exceeds the total byte budget.
    monkeypatch.setattr(codec, 'MAX_PLIST_BYTES', 16 << 20)
    monkeypatch.setattr(codec, 'MAX_PLIST_DEPTH', 3)
    with pytest.raises(codec.InvalidFileException, match='depth'):
        codec.loads(b'<plist><array><array><array><array/></array></array></array></plist>')
    with pytest.raises(codec.InvalidFileException, match='depth'):
        codec.loads(binary([b'\xa1\x01', b'\xa1\x02', b'\xa1\x03', b'\xa0']))
    cycle = []
    cycle.append(cycle)
    stream = io.BytesIO(b'original')
    with pytest.raises(ValueError, match='cycle'):
        codec.dump(cycle, stream)
    assert stream.getvalue() == b'original'


def test_dump_checks_partial_writes_and_never_writes_unvalidated_data():
    class Partial:
        def __init__(self): self.data = bytearray()
        def write(self, payload):
            self.data += payload[:7]
            return min(7, len(payload))
    stream = Partial()
    codec.dump({'hello': 'world'}, stream)
    assert codec.loads(stream.data) == {'hello': 'world'}
    class Broken:
        def write(self, payload): return None
    with pytest.raises(OSError):
        codec.dump({}, Broken())


@pytest.mark.parametrize('raw', [b'\xca\xfe\xba\xbe', bytearray(b'\xca\xfe\xba\xbe')])
def test_scalar_values_builder_preserves_exact_width_encoded_bytes(raw):
    from imagequay_layout.binary_records import fat_header
    value=records.Struct.create_with_values(fat_header,[raw,2],'big')
    assert value.raw==raw+struct.pack('>I',2)
    with pytest.raises(ValueError,match='byte count'):
        records.Struct.create_with_values(fat_header,[raw[:-1],2],'big')
    class Boolean(records.Struct):
        FIELDS={'flag':records.uint8_t}
    assert records.Struct.create_with_values(Boolean,[True]).raw==b'\x01'
