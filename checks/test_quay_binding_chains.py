"""Declared-region and dyld semantics tests; never execute input Mach-O data."""
import hashlib
import io
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
from types import SimpleNamespace as NS
import pytest
import imagequay
from imagequay.binding_reader import quay_BindingTable as BindingTable
from imagequay.chained_reader import quay_ChainedFixups as ChainedFixups
from imagequay.container_io import quay_MachOFile as MachOFile
from imagequay.failure_types import quay_MalformedMachOException as Malformed
from imagequay.metadata_reader import quay_SymbolTable as SymbolTable
from imagequay_layout.pointer_records import quay_dyld_chained_import_addend64, quay_ChainedFixupPointer32, quay_dyld_chained_start_offsets

ROOT = Path(__file__).parent


def minimal(data, pointer_size=8, base=0x100000000):
    raw = bytearray(data)
    raw[:32] = struct.pack('<8I', 0xfeedfacf, 0x01000007, 3, 2, 0, 0, 0, 0)
    view = MachOFile(io.BytesIO(raw)).slices[0]
    segment = NS(name='__DATA', vm_address=base, file_address=0, size=4096, file_size=4096)
    return NS(slice=view, ptr_size=pointer_size, segments={'__DATA': segment}, vm=NS(vm_base_addr=base),
        linked_images=[NS(install_name='libexample')], read_uint=view.read_uint, read_bytearray=view.read_bytearray,
        macho_header=NS(is64=pointer_size == 8))


def binding(opcodes, pointers=None, base=0x100000000):
    data = bytearray(8192)
    data[4096:4096+len(opcodes)] = opcodes
    for offset, word in (pointers or {}).items():
        data[offset:offset+8] = struct.pack('<Q', word)
    return minimal(data, base=base), 4096, len(opcodes)


def test_binding_done_does_not_create_an_extra_action_and_preserves_64_bit_address():
    # library #1, symbol, type pointer, segment0+128, two binds, DONE.
    opcodes = b'\x11\x40_symbol\0\x51\x70\x80\x01\x90\x90\0'
    image, start, size = binding(opcodes, base=0x10000000000)
    table = BindingTable(image, start, size)
    assert [(s.fullname, s.address) for s in table.symbol_table] == [('_symbol', image.vm.vm_base_addr+128), ('_symbol', image.vm.vm_base_addr+136)]
    assert len(table.import_stack) == len(table.actions) == 2
    assert BindingTable(image, start+size-1, 1).symbol_table == []


@pytest.mark.parametrize('special,ordinal', [(0x30, 0), (0x3f, -1), (0x3e, -2), (0x3d, -3)])
def test_binding_special_ordinals_are_signed_and_not_python_negative_indices(special, ordinal):
    image, start, size = binding(bytes([special])+b'\x40foo\0\x51\x70\x80\x01\x90\0')
    symbol = BindingTable(image, start, size).symbol_table[0]
    assert symbol.ordinal == str(ordinal) and symbol.binding_ordinal == ordinal


@pytest.mark.parametrize('tail,offsets', [
    (b'\xa0\x10\x90', [128, 152]),
    (b'\xb2\x90', [128, 152]),
    (b'\xc0\x02\x08', [128, 144]),
])
def test_binding_all_normal_advance_opcodes(tail, offsets):
    opcodes = b'\x11\x40foo\0\x51\x70\x80\x01'+tail+b'\0'
    image, start, size = binding(opcodes)
    assert [entry.seg_offset for entry in BindingTable(image, start, size).import_stack] == offsets


def test_binding_sleb_and_utf8_cursor_are_kept_exact():
    opcodes = b'\x11\x40'+ '鱼'.encode()+b'\0\x51\x60\x7f\x70\x80\x01\x90\0'
    image, start, size = binding(opcodes)
    symbol = BindingTable(image, start, size).symbol_table[0]
    assert symbol.fullname == '鱼' and symbol.addend == -1


def test_threaded_binding_apply_reads_ordinal_and_signed_pointer_addend():
    opcodes = b'\xd0\x01\x11\x51\x40foo\0\x60\x7e\x90\x70\x80\x02\xd1\0'
    # thread chain first bind with -1 pointer addend, next auth bind with no addend.
    first = (1 << 62) | (1 << 51) | (0x7ffff << 32)
    second = (1 << 63) | (1 << 62)
    image, start, size = binding(opcodes, {256: first, 264: second})
    symbols = BindingTable(image, start, size).symbol_table
    assert [(symbol.address, symbol.addend) for symbol in symbols] == [(image.vm.vm_base_addr+256, -3), (image.vm.vm_base_addr+264, -2)]


@pytest.mark.parametrize('opcodes', [
    b'\xe0', b'\xd2', b'\xd1', b'\x54', b'\x3c\x40foo\0\x70\0\x90',
    b'\x12\x40foo\0\x70\0\x90', b'\x11\x70\0\x90', b'\x71\0',
    b'\x11\x40foo\0\x70\xff\x1f\x90',
    b'\xd0\x01\xd1', b'\xd0\x01\x11\x40foo\0\x90\x90',
])
def test_invalid_binding_states_fail_explicitly(opcodes):
    image, start, size = binding(opcodes)
    with pytest.raises(Malformed):
        BindingTable(image, start, size)


def chained(pointer_format=6, import_format=1, words=None, *, starts=(256,), main_start=None, addend=0):
    data = bytearray(8192)
    entry = struct.pack('<HHQIH', 4096, pointer_format, 0, 0, 1)
    # one primary page start, optionally followed by the overflow list.
    if main_start is None:
        body = entry+struct.pack('<H', starts[0])
    else:
        body = entry+struct.pack('<H', main_start)+b''.join(struct.pack('<H', start) for start in starts)
    segment = struct.pack('<I', len(body)+4)+body
    starts_region = struct.pack('<II', 1, 8)+segment
    imports_offset = 28+len(starts_region)
    if import_format == 1:
        imported = struct.pack('<I', 1)
    elif import_format == 2:
        imported = struct.pack('<Ii', 1, addend)
    else:
        imported = struct.pack('<QQ', 1, addend)
    header = struct.pack('<7I', 0, 28, imports_offset, imports_offset+len(imported), 1, import_format, 0)
    payload = header+starts_region+imported+b'_symbol\0'
    data[4096:4096+len(payload)] = payload
    width = 4 if pointer_format in (3, 4, 5) else 8
    for offset, word in (words or {256: (1 << 63)}).items():
        data[offset:offset+width] = word.to_bytes(width, 'little')
    image = minimal(data, pointer_size=4 if width == 4 else 8, base=0x1000 if width == 4 else 0x100000000)
    return image, NS(dataoff=4096, datasize=len(payload))


def test_chain_absolute_locations_offset_rebases_and_stable_raw():
    image, command = chained(words={256: 0x200 | (2 << 51), 264: 1 << 63})
    result = ChainedFixups.from_image(image, command)
    assert result.rebases == {image.vm.vm_base_addr+256: image.vm.vm_base_addr+0x200, image.vm.vm_base_addr+264: 0}
    assert result.symbols[0].address == image.vm.vm_base_addr+264
    original = result.raw_bytes()
    image.slice.patch(command.dataoff, b'\xff')
    assert result.raw_bytes() == original


@pytest.mark.parametrize('import_format,addend', [(1, 0), (2, -17), (3, (1 << 63)+4)])
def test_all_chain_import_widths_and_addends(import_format, addend):
    image, command = chained(import_format=import_format, addend=addend)
    result = ChainedFixups.from_image(image, command)
    assert result.symbols[0].addend == addend
    assert quay_dyld_chained_import_addend64.size() == 16
    assert quay_ChainedFixupPointer32.size() == 4
    assert quay_dyld_chained_start_offsets.size() == 12


@pytest.mark.parametrize('pointer_format,word,expected', [
    (1, 0x1234, 0x1234), (2, 0x1234, 0x1234), (3, 0x1234, 0x1234),
    (5, 0x1234, 0x1234), (6, 0x1234, 0x100001234),
    (7, 0x1234, 0x100001234), (9, 0x1234, 0x100001234), (10, 0x1234, 0x1234),
    (12, 0x1234, 0x100001234), (14, 0x123, 0x100000123),
])
def test_chain_pointer_formats_have_correct_normal_targets(pointer_format, word, expected):
    image, command = chained(pointer_format, words={256: word})
    assert ChainedFixups.from_image(image, command).rebases[image.vm.vm_base_addr+256] == expected


@pytest.mark.parametrize('pointer_format', [4, 8, 11, 13])
def test_external_cache_targets_remain_explicit_until_base_is_supplied(pointer_format):
    image, command = chained(pointer_format, words={256: 0x1234})
    result = ChainedFixups.from_image(image, command)
    address = image.vm.vm_base_addr+256
    assert address not in result.rebases
    assert result.unresolved_rebases[address]['target_offset'] == 0x1234
    resolved = ChainedFixups.from_image(image, command, cache_bases={0: 0x200000000})
    assert resolved.rebases[address] == 0x200001234


def test_multiple_chain_starts_have_bounded_overflow_and_no_duplicate_locations():
    image, command = chained(words={256: 1 << 63, 264: 0x300}, main_start=0x8001, starts=(256, 0x8108))
    assert len(ChainedFixups.from_image(image, command).rebase_details) == 2
    image, command = chained(words={256: 1 << 63}, main_start=0x8001, starts=(256, 0x8100))
    with pytest.raises(Malformed, match='more than one chain'):
        ChainedFixups.from_image(image, command)


@pytest.mark.parametrize('field,value', [(0, 1), (1, 0xffffffff), (2, 0xffffffff), (3, 0xffffffff), (4, 0xffffffff), (5, 99), (6, 1)])
def test_chain_header_offsets_counts_versions_and_formats(field, value):
    image, command = chained()
    image.slice.patch(command.dataoff+field*4, struct.pack('<I', value))
    with pytest.raises(Malformed):
        ChainedFixups.from_image(image, command)


def test_chain_page_overrun_ordinal_overrun_and_segment_identity():
    image, command = chained(words={4088: 1 << 51}, starts=(4088,))
    with pytest.raises(Malformed, match='page'):
        ChainedFixups.from_image(image, command)
    image, command = chained(words={256: (1 << 63) | 1})
    with pytest.raises(Malformed, match='ordinal'):
        ChainedFixups.from_image(image, command)
    image, command = chained()
    image.slice.patch(command.dataoff+36+8, struct.pack('<Q', 99))
    with pytest.raises(Malformed, match='segment offset'):
        ChainedFixups.from_image(image, command)


def test_symbol_table_cannot_take_a_string_or_record_from_neighbor_bytes():
    data = bytearray(8192)
    data[256:272] = struct.pack('<IBBHQ', 1, 1, 0, 0, 0x1234)
    data[512:520] = b'\0name\0xx'
    image = minimal(data)
    image.read_struct = image.slice.read_struct
    cmd = NS(symoff=256, nsyms=1, stroff=512, strsize=2)
    with pytest.raises(Malformed, match='terminated'):
        SymbolTable(image, cmd)
    cmd.strsize = 6
    assert SymbolTable(image, cmd).table[0].fullname == 'name'
    cmd.nsyms = 1 << 63
    with pytest.raises(Malformed):
        SymbolTable(image, cmd)


@pytest.mark.skipif(sys.platform != 'darwin', reason='Apple dyld_info supplies an independent Mach-O oracle')
@pytest.mark.parametrize('filename', ['testbin1', 'testbin1.fat', 'testbin1.signed', 'testlib1.dylib'])
def test_all_fixture_chained_bind_and_rebase_locations_match_apple_dyld_info(filename):
    path = ROOT/'bins'/filename
    expected = json.loads((ROOT/'export_nm_expected.json').read_text())[filename]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected['sha256']
    with path.open('rb') as stream:
        owner = imagequay.load_macho_file(stream)
        for view in owner.slices:
            image = imagequay.load_image(view)
            arch = {'ARM6432': 'arm64_32'}.get(view.type.name, view.type.name.lower())
            output = subprocess.check_output(['/usr/bin/xcrun', 'dyld_info', '-arch', arch, '-fixups', '-function_starts', '-opcodes', str(path)], text=True)
            function_starts = [int(value,16) for value in re.findall(r'(?m)^\s*(0x[0-9a-fA-F]+)\s', output.split('    -function_starts:', 1)[1])]
            assert image.function_starts == function_starts
            binds, rebases = {}, {}
            for line in output.splitlines():
                match = re.search(r'\s(0x[0-9a-fA-F]+)\s+(?:auth-)?(bind|lazy-bind|rebase)\s+(\S+)', line)
                if not match:
                    continue
                address, kind, target = match.groups()
                if kind.endswith('bind'): binds[int(address, 16)] = target.rsplit('/', 1)[-1]
                else: rebases[int(address, 16)] = int(target, 16)
            actual = {symbol.address: symbol.fullname for symbol in image.imports}
            if arch == 'arm64_32':
                # Apple BindOpcodes.cpp forEachBindLocation increments a target
                # ordinal after its callback. In current dyld_info builds repeated
                # targets can therefore print the next symbol. Keep every site
                # checked, and verify names against Apple's printed opcode operands
                # plus this exact SHA-bound fixture vector; never accept arbitrary
                # tool or library differences.
                vector = json.loads((ROOT/'arm64_32_binding_expected.json').read_text())
                assert vector['sha256'] == expected['sha256']
                regular = output.split('        bind opcodes:\n', 1)[1].split('        lazy bind opcodes:', 1)[0]
                trace = re.findall(r'^\s+0x[0-9a-fA-F]+ (BIND_OPCODE_\w+\([^\n]*\))$', regular, re.M)
                assert trace == vector['regular_bind_opcodes']
                assert actual == {int(address): name for address, name in vector['binds'].items()}
                assert set(actual) == set(binds)
                assert binds[65536] == '_objc_copyStruct'  # lazy target is unique
            else:
                assert actual == binds, output
            if image.chained_fixups:
                assert {address: target for address, target in image.chained_fixups.rebases.items() if address not in binds} == rebases


def test_weak_implicit_ordinal_and_strong_definition_metadata():
    image, start, size = binding(b'\x40foo\0\x51\x70\x80\x01\x90\0')
    result = BindingTable(image, start, size, kind='weak')
    assert result.symbol_table[0].binding_ordinal == -3
    image, start, size = binding(b'\x48strong\0\0')
    result = BindingTable(image, start, size, kind='weak')
    assert result.strong_definitions == ['strong'] and result.actions == []


def test_lazy_done_retains_state_and_regular_done_does_not_restart():
    opcodes = b'\x11\x40foo\0\x70\x80\x01\x90\0\x40bar\0\x90\0'
    image, start, size = binding(opcodes)
    result = BindingTable(image, start, size, kind='lazy')
    assert [(record.name, record.seg_offset) for record in result.import_stack] == [('foo', 128), ('bar', 136)]
    with pytest.raises(Malformed):
        BindingTable(image, start, size)


@pytest.mark.parametrize('opcodes', [
    b'\x51\x40foo\0\x70\0\x90',  # no ordinal
    b'\x11\x51\x40foo\0\x90',  # no selected segment
    b'\x11\x40foo\0\x70\0\x90',  # no normal binding type
    b'\x11\x51\x40\xff\0\x70\0\x90',  # invalid UTF-8
])
def test_binding_missing_state_is_not_filled_with_default_facts(opcodes):
    image, start, size = binding(opcodes)
    with pytest.raises(Malformed):
        BindingTable(image, start, size)


def test_backward_uleb_cursor_and_end_of_segment_text_binding():
    backwards = b'\xf0'+b'\xff'*8+b'\x01'  # uint64 -16
    opcodes = b'\x11\x51\x40foo\0\x70\x80\x01\x90\x80'+backwards+b'\x90\0'
    image, start, size = binding(opcodes)
    assert [record.seg_offset for record in BindingTable(image, start, size).import_stack] == [128, 120]
    opcodes = b'\x11\x52\x40foo\0\x70\xfc\x1f\x90\0'
    image, start, size = binding(opcodes)
    result = BindingTable(image, start, size)
    assert result.import_stack[0].seg_offset == 4092 and result.import_stack[0].type == 2
