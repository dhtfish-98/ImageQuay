"""Independent input, write, container, signature, trie and VM contract probes."""
from contextlib import contextmanager
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
from types import SimpleNamespace

import pytest
import imagequay
from imagequay.container_io import (
    quay_BackingFile as BackingFile, quay_MachOFile as MachOFile,
    quay_MachOImageHeader as ImageHeader, quay_Slice as Slice,
)
from imagequay.failure_types import quay_MalformedMachOException as Malformed, quay_VMAddressingError as VMError
from imagequay.file_ops import safe_open, metadata_leaf, set_overwrite, _allow_overwrite
from imagequay.metadata_reader import quay_ExportTrie as ExportTrie
from imagequay.parsed_image import quay_VM as VM, quay_MisalignedVM as MisalignedVM
from imagequay.signing_reader import quay_CodesignInfo as CodesignInfo
from imagequay.update_reader import read_release, ENDPOINT, MAX_RESPONSE_BYTES, RELEASE_ROOT
from imagequay_layout.binary_records import quay_Struct as Struct, quay_rpath_command as Rpath, quay_unk_command as Unknown, quay_linkedit_data_command as Linkedit, quay_mach_header as Header32, quay_mach_header_64 as Header64

ROOT = Path(__file__).parent


def thin(payload=b'', commands=(), order='<', bits=64):
    raw = b''.join(commands)
    values = [0xfeedfacf if bits == 64 else 0xfeedface, 0x01000007 if bits == 64 else 7, 3, 2, len(commands), len(raw), 0]
    if bits == 64:
        values.append(0)
    return struct.pack(order + 'I' * len(values), *values) + raw + payload


def image_view(data):
    owner = MachOFile(BytesIO(data))
    return SimpleNamespace(slice=owner.slices[0], read_bytearray=owner.slices[0].read_bytearray,
                           read_struct=owner.slices[0].read_struct, read_fixed_len_str=owner.slices[0].read_fixed_len_str)


@pytest.mark.parametrize('address,count', [(-1,1),(0,-1),(5,0),(0,5),(4,1),(True,1),(0,False),(1<<64,1),(1,1<<64)])
def test_exact_byte_ranges(address, count):
    backing = BackingFile(BytesIO(b'abcd'), use_mmaped_io=True)
    with pytest.raises(Malformed):
        backing.read_bytes(address, count)


@pytest.mark.parametrize('address,data', [(-1,b'a'),(4,b'a'),(2,b'abc'),(1<<64,b'a')])
def test_patch_checks_entire_range_before_change(address, data):
    backing = BackingFile(BytesIO(b'abcd'))
    with pytest.raises(Malformed):
        backing.write(address, data)
    assert backing.read_bytes(0,4) == b'abcd'


@pytest.mark.parametrize('order', ['<','>'])
@pytest.mark.parametrize('bits', [32,64])
def test_header_byte_order_and_roundtrip(order, bits):
    unknown = struct.pack(order+'II', 0x7777, 8)
    data = thin(commands=[unknown],order=order,bits=bits)
    owner = MachOFile(BytesIO(data))
    view = ImageHeader.from_image(owner.slices[0])
    assert view.dyld_header.cpu_type == (0x01000007 if bits == 64 else 7)
    assert view.raw_bytes() == data
    assert view.load_commands[0].cmd == 0x7777
    assert bytes(view.insert_load_command(Struct.create_with_values(Unknown,[0x6666,8], owner.slices[0].byte_order)).remove_load_command(1).raw) == data


@pytest.mark.parametrize('length', list(range(32)))
def test_truncated_thin_header(length):
    with pytest.raises(Malformed):
        owner = MachOFile(BytesIO(thin()[:length]))
        ImageHeader.from_image(owner.slices[0])


@pytest.mark.parametrize('count,size,command', [
    (1,0,b''),(2,8,struct.pack('<II',0x7777,8)),(1,8,struct.pack('<II',0x7777,0)),
    (1,8,struct.pack('<II',0x7777,4)),(1,8,struct.pack('<II',0x7777,16)),
    (1,16,struct.pack('<II',0x7777,8)+b'\0'*8),(1,12,struct.pack('<II',0x7777,12)+b'\0'*4),
])
def test_load_command_region_contract(count, size, command):
    raw = bytearray(thin(payload=command))
    struct.pack_into('<II', raw, 16, count, size)
    owner = MachOFile(BytesIO(raw))
    with pytest.raises(Malformed):
        ImageHeader.from_image(owner.slices[0])


def test_header_edits_preserve_unknown_tail_and_unicode():
    command = struct.pack('<II',0x7777,16)+b'abcdEFGH'
    owner = MachOFile(BytesIO(thin(commands=[command])))
    header = ImageHeader.from_image(owner.slices[0])
    rpath = Struct.create_with_values(Rpath,[0x8000001c,0,12])
    changed = header.insert_load_command(rpath,suffix='目录')
    assert changed.raw[32:48] == command
    assert header.raw == thin(commands=[command])
    assert bytes(changed.remove_load_command(1).raw) == bytes(header.raw)
    with pytest.raises(IndexError):
        header.remove_load_command(9)
    with pytest.raises(ValueError):
        header.insert_load_command(rpath,suffix='bad\0name')


@pytest.mark.parametrize('kind', ['negative','outside','overlap','table','misaligned','cpu','count'])
def test_fat_range_contract(kind):
    raw = bytearray(0x1000+32)
    struct.pack_into('>II',raw,0,0xcafebabe,1)
    struct.pack_into('>IIIII',raw,8,0x01000007,3,0x1000,32,12)
    raw[0x1000:] = thin()
    if kind=='negative':struct.pack_into('>I',raw,16,0xffffffff)
    if kind=='outside':struct.pack_into('>I',raw,20,33)
    if kind=='table':struct.pack_into('>I',raw,16,8)
    if kind=='misaligned':struct.pack_into('>I',raw,24,30)
    if kind=='cpu':struct.pack_into('>I',raw,8,0x0100000c)
    if kind=='count':struct.pack_into('>I',raw,4,0xffffffff)
    if kind=='overlap':
        struct.pack_into('>I',raw,4,2)
        raw[28:48] = raw[8:28]
    with pytest.raises(Malformed):MachOFile(BytesIO(raw))


def test_cstring_limit_unicode_and_patch_cache():
    owner=MachOFile(BytesIO(thin('é\0old\0'.encode())))
    view=owner.slices[0]
    assert view.read_cstr(32,limit=3)=='é'
    with pytest.raises(Malformed):view.read_cstr(32,limit=2)
    assert view.read_cstr(35)=='old'
    view.file.write(35,b'new')
    assert view.read_cstr(35)=='new'


@pytest.mark.parametrize('raw', [b'\x80'*10,b'\xff'*9+b'\x02',b'\x80'])
def test_uleb_cannot_leave_input_or_overflow(raw):
    owner=MachOFile(BytesIO(thin(raw)))
    with pytest.raises(Malformed):owner.slices[0].read_uleb128(32)


@pytest.mark.parametrize('raw,value', [(b'\x00',0),(b'\x7f',127),(b'\x80\x01',128),(b'\xff'*9+b'\x01',(1<<64)-1)])
def test_uleb_known_unsigned_values(raw,value):
    owner=MachOFile(BytesIO(thin(raw)))
    assert owner.slices[0].read_uleb128(32)==(value,32+len(raw))


def test_signature_roundtrip_and_entitlement():
    payload=b'<plist><dict/></plist>'
    blob=struct.pack('>II',0xfade7171,8+len(payload))+payload
    raw=struct.pack('>III',0xfade0cc0,20+len(blob),1)+struct.pack('>II',5,20)+blob
    image=image_view(thin(raw))
    command=Struct.create_with_values(Linkedit,[0x1d,16,32,len(raw)])
    result=CodesignInfo.from_image(image,command)
    assert result.entitlements==payload.decode()
    assert result.raw_bytes()==raw


@pytest.mark.parametrize('mutation', ['count','length','index','bloblength','magic','duplicate','overlap'])
def test_signature_slots_stay_in_superblob(mutation):
    blob=struct.pack('>II',0xfade7171,12)+b'test'
    raw=bytearray(struct.pack('>III',0xfade0cc0,28+len(blob),2)+struct.pack('>IIII',5,28,7,28)+blob)
    if mutation=='count':struct.pack_into('>I',raw,8,0xffffffff)
    if mutation=='length':struct.pack_into('>I',raw,4,len(raw)+1)
    if mutation=='index':struct.pack_into('>I',raw,16,12)
    if mutation=='bloblength':struct.pack_into('>I',raw,32,len(raw))
    if mutation=='magic':struct.pack_into('>I',raw,28,0)
    if mutation=='duplicate':struct.pack_into('>I',raw,20,5)
    image=image_view(thin(raw));command=Struct.create_with_values(Linkedit,[0x1d,16,32,len(raw)])
    with pytest.raises(Malformed):CodesignInfo.from_image(image,command)


@pytest.mark.parametrize('raw', [b'\0\1A\0\1', b'\x03\0\x80',b'\0\1A',b'\0\1A\0\x7f',b'\0\1A\0\0'])
def test_export_cycles_ranges_and_strings(raw):
    image=image_view(thin(raw))
    with pytest.raises(Malformed):ExportTrie.from_image(image,32,len(raw))


@pytest.mark.parametrize('address', [0,127,128,0x4840,1<<40])
def test_export_terminal_integer_uses_all_bits(address):
    value=address;encoded=bytearray()
    while True:
        byte=value&127;value>>=7;encoded.append(byte|(128 if value else 0))
        if not value:break
    terminal=b'\0'+encoded
    raw=bytes([len(terminal)])+terminal+b'\0'
    image=image_view(thin(raw))
    result=ExportTrie.from_image(image,32,len(raw))
    assert result.symbols[0].address==address
    assert result.nodes[0].flags==0


def test_export_reexport_and_resolver_metadata():
    for terminal,flags,extra in [(b'\x08\x02other\0',8,('reexport_ordinal',2)),(b'\x10\x7f\x80\x01',16,('resolver_offset',128))]:
        raw=bytes([len(terminal)])+terminal+b'\0'
        result=ExportTrie.from_image(image_view(thin(raw)),32,len(raw))
        assert result.nodes[0].flags==flags
        assert getattr(result.symbols[0],extra[0])==extra[1]


@pytest.mark.parametrize('vm_type',[VM,MisalignedVM])
def test_vm_half_open_ranges_and_zero_fill(vm_type):
    vm=vm_type(4096) if vm_type is VM else vm_type()
    segment=SimpleNamespace(name='__DATA',vm_address=0x2000,file_address=0x100,size=0x1000,file_size=0x10)
    vm.add_segment(segment)
    assert vm.translate(0x200f)==0x10f
    with pytest.raises(VMError):vm.translate(0x2010)
    with pytest.raises(VMError):vm.de_translate(0x110)


def test_huge_virtual_map_does_not_allocate_page_per_address():
    vm=VM(4096)
    vm.map_pages(0,0x1000,1<<48)
    assert len(vm.segs)==1 and not vm.page_table
    assert vm.translate((1<<48)+0x0fff)==(1<<48)-1


def test_record_cache_keeps_type_byteorder_and_generation():
    with (ROOT.parent/'Build/fixtures/testbin1').open('rb') as stream:image=imagequay.load_image(stream)
    a=image.read_struct(0,Header32)
    b=image.read_struct(0,Header64)
    assert type(a) is not type(b)
    assert len(a.raw)==28 and len(b.raw)==32
    previous=a.cpu_subtype
    image.slice.patch(8,struct.pack('<I',8))
    assert image.read_struct(0,Header32).cpu_subtype==8
    assert a.cpu_subtype==previous


@pytest.mark.parametrize('name',['','..','../escape','a/b','a\\b','bad\0name','bad\nname','x'*241])
def test_binary_metadata_cannot_choose_output_directories(name):
    with pytest.raises(ValueError):metadata_leaf(name)


def test_atomic_outputs_no_clobber_and_private_modes(tmp_path):
    path=tmp_path/'output'
    with safe_open(path,'wb') as stream:
        stream.write(b'first');assert not path.exists()
    assert path.read_bytes()==b'first' and path.stat().st_mode&0o777==0o600
    with pytest.raises(FileExistsError):safe_open(path,'wb')
    token=set_overwrite(True)
    try:
        with safe_open(path,'wb') as stream:stream.write(b'second')
        link=tmp_path/'link';link.symlink_to(path)
        with pytest.raises(OSError):safe_open(link,'wb')
        assert path.read_bytes()==b'second'
    finally:_allow_overwrite.reset(token)
    assert not list(tmp_path.glob('.imagequay-*'))


def test_failed_output_never_publishes_partial_bytes(tmp_path):
    path=tmp_path/'new'
    with pytest.raises(RuntimeError):
        with safe_open(path,'wb') as stream:
            stream.write(b'partial');raise RuntimeError('stop')
    assert not path.exists() and not list(tmp_path.glob('.imagequay-*'))


def test_output_concurrent_creation_wins_without_truncation(tmp_path):
    path=tmp_path/'new'
    with pytest.raises(FileExistsError):
        with safe_open(path,'wb') as stream:
            stream.write(b'staged');path.write_bytes(b'other-owner')
    assert path.read_bytes()==b'other-owner'
    assert not list(tmp_path.glob('.imagequay-*'))


def test_safe_input_rejects_symlink_fifo_and_preserves_bytes(tmp_path):
    path=tmp_path/'input';original=thin();path.write_bytes(original)
    link=tmp_path/'link';link.symlink_to(path)
    with pytest.raises(OSError):safe_open(link)
    if hasattr(os,'mkfifo'):
        fifo=tmp_path/'fifo';os.mkfifo(fifo)
        with pytest.raises(OSError):safe_open(fifo)
    with safe_open(path) as stream:owner=MachOFile(stream,use_mmaped_io=True)
    owner.slices[0].patch(0,b'xxxx')
    assert path.read_bytes()==original


@pytest.mark.parametrize('document', [
    {}, {'tag_name':'v2.0','html_url':'https://unrelated.example/'},
    {'tag_name':'not-a-version','html_url':RELEASE_ROOT+'not-a-version'},
    {'tag_name':'v1.0','html_url':RELEASE_ROOT+'v1.0'},
])
def test_explicit_update_reader_ignores_invalid_or_old_metadata(document):
    def opener(request,timeout):
        assert request.full_url==ENDPOINT and timeout==3
        return BytesIO(json.dumps(document).encode())
    assert read_release('1.0.2',opener)==None


def test_explicit_update_reader_response_limit():
    assert read_release('1.0.2',lambda *args,**kwargs:BytesIO(b'a'*(MAX_RESPONSE_BYTES+1))) is None
    expected=RELEASE_ROOT+'v2.0.0'
    assert read_release('1.0.2',lambda *args,**kwargs:BytesIO(json.dumps({'tag_name':'v2.0.0','html_url':expected}).encode()))==expected


def test_default_cli_never_calls_update_network(monkeypatch):
    from imagequay import console
    monkeypatch.setattr(console,'read_release',lambda *args:pytest.fail('implicit network query'))
    monkeypatch.setattr(sys,'argv',['imagequay','-V'])
    with pytest.raises(SystemExit) as exit:console.quay_main()
    assert exit.value.code is None


@pytest.mark.skipif(sys.platform!='darwin',reason='Apple nm is used as an independent Mach-O oracle')
@pytest.mark.parametrize('name',['testbin1','testbin1.fat','testbin1.signed','testlib1.dylib'])
def test_current_export_addresses_match_apple_nm(name):
    expected=json.loads((ROOT/'export_nm_expected.json').read_text())[name]
    path=ROOT.parent/'Build'/'fixtures'/name
    assert hashlib.sha256(path.read_bytes()).hexdigest()==expected['sha256']
    with path.open('rb') as stream:image=imagequay.load_image(stream)
    architecture=image.slice.type.name.lower()
    result=subprocess.run(['/usr/bin/xcrun','nm','-arch',architecture,'-gU',str(path)],capture_output=True,text=True,check=True,timeout=10)
    values={line.split()[-1]:int(line.split()[0],16) for line in result.stdout.splitlines() if len(line.split())==3}
    for item in image.exports:
        assert item.fullname in values,item.fullname
        assert item.address==values[item.fullname]-image.vm.vm_base_addr
    assert {item.fullname:item.address for item in image.exports}==expected['exports']


def test_header_growth_is_confined_to_declared_padding():
    from imagequay.toolkit_api import patch_image_header
    with (ROOT.parent/'Build/fixtures/testbin1').open('rb') as stream:image=imagequay.load_image(stream)
    rpath=Struct.create_with_values(Rpath,[0x8000001c,0,12])
    before=image.slice.full_bytes_for_slice()
    changed=image.macho_header.insert_load_command(rpath,suffix='@loader_path/owned')
    reloaded=patch_image_header(image,changed)
    assert reloaded.rpath=='@loader_path/owned'
    earliest=min(section.file_address for segment in image.segments.values() for section in segment.sections.values() if section.size and section.file_address>=len(image.macho_header.raw))
    assert image.slice.full_bytes_for_slice()[earliest:]==before[earliest:]
    impossible=reloaded.macho_header.insert_load_command(rpath,suffix='x'*earliest)
    current=image.slice.full_bytes_for_slice()
    with pytest.raises(Malformed):patch_image_header(reloaded,impossible)
    assert image.slice.full_bytes_for_slice()==current


def test_verification_restores_ignore_state_when_input_is_bad():
    from imagequay.toolkit_api import quay_macho_verify
    from imagequay.formatting import quay_ignore
    previous=quay_ignore.MALFORMED
    quay_ignore.MALFORMED=True
    try:
        with pytest.raises(Malformed):quay_macho_verify(BytesIO(thin()[:12]))
        assert quay_ignore.MALFORMED is True
    finally:quay_ignore.MALFORMED=previous


@pytest.mark.parametrize('raw,declared',[(b'\x40name\0\0',2),(b'\x20\x80\0',2),(b'\x70\x80\0',2)])
def test_bindings_cannot_read_past_their_declared_region(raw,declared):
    from imagequay.metadata_reader import quay_BindingTable as BindingTable
    image=image_view(thin(raw))
    image.ptr_size=8
    with pytest.raises(Malformed):BindingTable(image,32,declared)


def test_binding_repeat_count_has_a_finite_allocation_budget():
    from imagequay.metadata_reader import quay_BindingTable as BindingTable
    # DO_BIND_ULEB_TIMES_SKIPPING_ULEB with unsigned 64-bit maximum count.
    raw=b'\xc0'+b'\xff'*9+b'\x01'+b'\0\0'
    image=image_view(thin(raw));image.ptr_size=8
    with pytest.raises(Malformed,match='work budget'):BindingTable(image,32,len(raw))


def test_export_shared_terminal_is_valid_but_active_path_cycle_is_not():
    shared=b'\0\2A\0\x08B\0\x08'+b'\x02\0\x01\0'
    result=ExportTrie.from_image(image_view(thin(shared)),32,len(shared))
    assert {(item.fullname,item.address) for item in result.symbols}=={('A',1),('B',1)}
    cyclic=b'\0\2A\0\x08B\0\x08'+b'\0\1C\0\x08'
    with pytest.raises(Malformed,match='cycle'):ExportTrie.from_image(image_view(thin(cyclic)),32,len(cyclic))


def test_export_deep_path_has_an_explicit_limit():
    def uleb(value):
        data=bytearray()
        while True:
            byte=value&127;value>>=7;data.append(byte|(128 if value else 0))
            if not value:return bytes(data)
    payload=bytearray()
    for _ in range(4097):
        cursor=len(payload);target=cursor+5
        while target != cursor+4+len(uleb(target)):target=cursor+4+len(uleb(target))
        payload.extend(b'\0\1a\0'+uleb(target))
    payload.extend(b'\0\0')
    with pytest.raises(Malformed,match='depth budget'):ExportTrie.from_image(image_view(thin(payload)),32,len(payload))


@pytest.mark.parametrize('failure',['fchmod','fdopen','text_wrapper'])
def test_output_initialization_failure_closes_descriptor_and_removes_stage(tmp_path,monkeypatch,failure):
    from imagequay import file_ops
    import gc
    created=[]
    actual_create=file_ops.tempfile.mkstemp
    def create(*args,**kwargs):
        descriptor,path=actual_create(*args,**kwargs)
        created.append((descriptor,Path(path)))
        return descriptor,path
    def fail(*args,**kwargs):
        raise OSError('injected initialization failure')
    monkeypatch.setattr(file_ops.tempfile,'mkstemp',create)
    if failure=='fchmod':monkeypatch.setattr(file_ops.os,'fchmod',fail)
    elif failure=='fdopen':monkeypatch.setattr(file_ops.os,'fdopen',fail)
    else:monkeypatch.setattr(file_ops.io,'TextIOWrapper',fail)
    with pytest.raises(OSError,match='injected initialization failure'):
        safe_open(tmp_path/'new','w' if failure=='text_wrapper' else 'wb')
    gc.collect()
    assert len(created)==1
    descriptor,path=created[0]
    with pytest.raises(OSError):os.fstat(descriptor)
    assert not path.exists()
    assert not (tmp_path/'new').exists()
    assert not list(tmp_path.glob('.imagequay-*'))
