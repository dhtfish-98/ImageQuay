"""Finite language metadata contracts and compiler-owned static oracles."""
import io
import re
import struct
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace as NS
import pytest
import imagequay
from imagequay.container_io import quay_MachOFile
from imagequay.objc_encoding import (quay_TypeProcessor, quay_Type,
    quay_Struct_Representation, quay_EncodedType)
from imagequay.objc_model import quay_TypeProcessor as PublicProcessor
from imagequay.metadata_graph import MetadataGraph
from imagequay.swift_model import (quay_SwiftImage, quay_SwiftType,
    quay_SwiftStruct, quay_SwiftClass, quay_SwiftEnum, quay__FieldDescriptor,
    quay_Field)
from imagequay_swift.name_decoder import quay_demangle
from imagequay_swift.metadata_records import quay_ClassDescriptor, quay_FieldDescriptor
from imagequay_support.record_engine import quay_Struct
from imagequay.failure_types import quay_MalformedMachOException as Malformed

ROOT = Path(__file__).parent


@pytest.mark.parametrize('encoding,displays', [
    ('i', ['int']), ('^^i', ['**int']), ('r^i', ['*int']),
    ('v24@0:8i16', ['void', 'id', 'SEL', 'int']),
    ('@"NSObject<P>"i', ['NSObject<P>', 'int']),
    ('@?', ['id']), ('[3i]', ['int [3]']), ('D', ['long double']),
    ('jd', ['_Complex double']), ('ji', ['_Complex int']), ('Ai', ['_Atomic(int)']),
])
def test_type_encodings_preserve_complete_types_and_offsets(encoding, displays):
    processor = PublicProcessor()
    assert isinstance(processor, quay_TypeProcessor)
    values = processor.process(encoding)
    assert [str(value) for value in values] == displays
    if encoding == 'v24@0:8i16':
        assert [value.offset for value in values] == [24, 0, 8, 16]
    if encoding == 'r^i':
        assert values[0].qualifiers == ('r',)
        assert values[0].declaration('count') == 'const int *count'


def test_nested_aggregate_fields_have_names_pointers_arrays_and_union_kind():
    processor = PublicProcessor()
    value = processor.process('{Outer="next"^{Outer}"values"[2i]"choice"(Choice=iq)}')[0]
    aggregate = value.value
    assert aggregate.field_names == ['next', 'values', 'choice']
    assert aggregate.fields[0].pointer_count == 1
    assert aggregate.fields[1].declaration('values') == 'int values[2]'
    assert aggregate.fields[2].value.kind == 'union'
    rendered = str(aggregate)
    assert 'struct Outer *next;' in rendered
    assert 'int values[2];' in rendered
    assert 'union Choice choice;' in rendered
    assert processor.structs['Outer'].fields
    assert quay_Struct_Representation(processor, '{Opaque}').field_names == []


def test_type_cache_and_registry_do_not_share_mutable_returned_views():
    processor = PublicProcessor()
    first = processor.process('{Pair="left"i"right"q}')
    first[0].value.fields[0].value = 'modified'
    first[0].value.field_names[0] = 'changed'
    first.pop()
    again = processor.process('{Pair="left"i"right"q}')
    assert again[0].value.fields[0].value == 'int'
    assert processor.structs['Pair'].field_names == ['left', 'right']
    assert isinstance(processor.type_cache['{Pair="left"i"right"q}'], list)


@pytest.mark.parametrize('encoding', ['', '^', '[3', '[3i}', '{A=', '{A=i)',
    '{=i}', '@"unterminated', '[4294967296i]', 'i4294967296', 'z',
    '^'*65+'i', '{A='*66+'i'+'}'*66, 'i'*4097, 'i'*16385,
    '{A="bad\nname"i}', 'v+'])
def test_malformed_type_encodings_fail_explicitly(encoding):
    with pytest.raises(ValueError):
        PublicProcessor().process(encoding)


def test_exact_single_type_and_legacy_tokens():
    processor = PublicProcessor()
    assert PublicProcessor.tokenize('^^i@"NSObject"') == ['^', '^', 'i', '"NSObject"']
    assert quay_Type(processor, 'i', 2).pointer_count == 2
    with pytest.raises(ValueError):
        quay_Type(processor, 'ii')
    assert processor.process('b3')[0].declaration('flags') == 'unsigned int flags : 3'
    with pytest.raises(TypeError):
        processor.process(None)


def swift_image(kind=17, *, ptr_size=8, base=0x100000000):
    raw = bytearray(4096)
    raw[:32] = struct.pack('<8I', 0xfeedfacf, 0x01000007, 3, 2, 0, 0, 0, 0)
    def put(offset, form, *values):struct.pack_into('<'+form, raw, offset, *values)
    # Module descriptor, then a type, then its field records. All names and
    # manglings precede the references to exercise negative signed rel32s.
    raw[64:69], raw[72:78] = b'Mod\0\0', b'Thing\0'
    raw[80:86], raw[88:91], raw[96:99] = b'value\0', b'Si\0', b'\x01\0\0'
    put(128, 'Iii', 0, 0, 64-(128+8))
    if kind == 16:
        put(256, 'IiiiiIIIIII', kind, 128-(256+4), 72-(256+8), 0,
            512-(256+16), 0, 0, 0, 0, 1, 0)
    elif kind in (17, 18):
        put(256, 'IiiiiII', kind, 128-(256+4), 72-(256+8), 0, 512-(256+16), 1, 0)
    else:
        put(256, 'Iii', kind, 0, 72-(256+8))
    put(512, 'iiHHI', 0, 0, {16:1,17:0,18:2}.get(kind,0), 12, 1)
    put(528, 'Iii', 2, 88-(528+4), 80-(528+8))
    put(768, 'i', 256-768)
    owner = quay_MachOFile(io.BytesIO(raw))
    view = owner.slices[0]
    section = NS(name='__swift5_types',vm_address=base+768,size=4)
    segment = NS(vm_address=base, file_address=0, file_size=len(raw), sections={'__swift5_types':section})
    image = NS(slice=view, ptr_size=ptr_size, segments={'__TEXT':segment})
    return NS(image=image, classlist=[]), lambda offset, data:view.patch(offset, data)


@pytest.mark.parametrize('kind,record_class', [(16,quay_SwiftClass),(17,quay_SwiftStruct),(18,quay_SwiftEnum)])
def test_swift_negative_relative_pointer_dispatch_names_fields_and_snapshot(kind, record_class):
    objc, _ = swift_image(kind)
    image = quay_SwiftImage.from_image(objc)
    item = image.types[0]
    assert isinstance(item, record_class)
    assert item.name == 'Thing' and item.context_path == ('Mod','Thing')
    assert [(field.name,field.type_name,field.flags) for field in item.fields] == [('value','Si',2)]
    assert item.field_desc.raw_bytes() == bytes(objc.image.slice.read_bytearray(512,28))
    assert len(item.raw_bytes()) == (44 if kind == 16 else 28)
    assert image.raw_bytes() == struct.pack('<i',256-768)


def test_swift_type_reference_indirection_is_confined_and_has_explicit_kind():
    objc, patch = swift_image()
    patch(900, struct.pack('<Q',0x100000000+256))
    patch(768, struct.pack('<i',(900-768)|1))
    assert quay_SwiftImage.from_image(objc).types[0].name == 'Thing'
    patch(768, struct.pack('<i',(900-768)|2))
    with pytest.raises(Malformed,match='reference kind'):
        quay_SwiftImage.from_image(objc)


@pytest.mark.parametrize('offset,raw', [(512+10,struct.pack('<H',8)),
    (512+12,struct.pack('<I',0xffffffff)), (256+8,struct.pack('<i',0)),
    (256,struct.pack('<I',17|(1<<8))), (128+4,struct.pack('<i',128-(128+4)))])
def test_swift_descriptor_lengths_counts_required_names_versions_and_cycles(offset, raw):
    objc, patch = swift_image()
    patch(offset,raw)
    with pytest.raises(Malformed):
        quay_SwiftImage.from_image(objc)


def test_swift_empty_sections_unknown_dispatch_and_unsigned_field_header():
    objc, _ = swift_image(4)
    result = quay_SwiftImage.from_image(objc)
    assert result.types == [None] and not result.complete
    assert result.unsupported_types[0]['kind'] == 4
    objc.image.segments['__TEXT'].sections = {}
    assert quay_SwiftImage.from_image(objc).types == []
    record = quay_Struct.create_with_bytes(quay_FieldDescriptor,struct.pack('<iiHHI',0,0,0,65535,0xffffffff))
    assert record.FieldRecordSize == 65535 and record.NumFields == 0xffffffff
    assert quay_ClassDescriptor.size() == 44


def test_swift_null_field_descriptor_is_a_real_empty_type():
    objc, patch = swift_image()
    patch(256+16,struct.pack('<i',0))
    item = quay_SwiftImage.from_image(objc).types[0]
    assert item.field_desc is None and item.fields == []


def test_swift_symbolic_names_keep_embedded_null_bytes_without_following_them():
    objc, patch = swift_image()
    mangling = b'\x01\0\0\0\0Sg\0'
    patch(88,mangling)
    field = quay_SwiftImage.from_image(objc).types[0].fields[0]
    assert field.type_name_bytes == mangling[:-1]
    assert field.type_name == '<symbolic:0x01:00000000>Sg' and field.symbolic_type


def test_vm_graph_read_range_string_and_snapshot_boundaries():
    objc, patch = swift_image()
    graph = MetadataGraph(objc.image)
    with pytest.raises(Malformed,match='segment'):
        graph.bytes(0x100000000+4095,2)
    with pytest.raises(Malformed,match='pointer width'):
        graph.bytes((1<<64)-1,2)
    patch(64,b'X')
    with pytest.raises(Malformed,match='changed'):
        graph.string(0x100000000+64)
    graph = MetadataGraph(objc.image)
    graph.remaining = 0
    with pytest.raises(Malformed,match='work budget'):
        graph.bytes(0x100000000,1)


def test_pointer_width_four_and_partial_type_section():
    objc, _ = swift_image(ptr_size=4,base=0x1000)
    assert quay_SwiftImage.from_image(objc).types[0].name == 'Thing'
    objc.image.segments['__TEXT'].sections['__swift5_types'].size = 3
    with pytest.raises(Malformed,match='partial'):
        quay_SwiftImage.from_image(objc)


@pytest.mark.parametrize('name,expected', [('_TtC3Mod5Thing',('Mod','Thing')),
    ('$s3Mod5ThingC',('Mod','Thing')), ('$s3Mod5ThingV',('Mod','Thing')),
    ('_TtC3Mod99Thing',('','')), ('OrdinaryName',('','')),
    ('$s3Mod5ThingCextra',('',''))])
def test_simple_nominal_name_lengths_and_scope(name, expected):
    assert quay_demangle(name) == expected


def test_swift_from_values_is_useful_but_does_not_pretend_to_encode_metadata():
    field = quay_Field(2,'Si','value')
    descriptor = quay__FieldDescriptor.from_values([field])
    value = quay_SwiftStruct.from_values('Value',descriptor)
    assert quay_SwiftImage.from_values([value]).types[0].fields == [field]
    with pytest.raises(ValueError,match='snapshot'):
        value.raw_bytes()


@pytest.mark.skipif(sys.platform!='darwin',reason='Clang supplies independent @encode vectors')
def test_owned_clang_encodings_match_the_full_parser(tmp_path):
    target=tmp_path/'encodings.ll'
    subprocess.run(['/usr/bin/xcrun','clang','-S','-emit-llvm','-x','objective-c',
        '-target','arm64-apple-macos13','-o',str(target),str(ROOT/'sources/objc_encoding_vectors.m')],check=True,capture_output=True)
    output=target.read_text()
    encodings=[]
    for encoded in re.findall(r'constant \[\d+ x i8\] c"([^"\n]*)"',output):
        assert encoded.endswith('\\00')
        encodings.append(encoded[:-3])
    assert encodings == ['i','^^i','r^i','[3i]','[2[3i]]','{Pair=id}','(Choice=iq)','{Bits=b3b5}','@',':','jd','Ai']
    processor=PublicProcessor()
    for encoded in encodings:
        assert len(processor.process(encoded)) == 1
    assert processor.process('{Bits=b3b5}')[0].value.fields[1].bit_width == 5


@pytest.mark.skipif(sys.platform!='darwin',reason='Swift compiler and nm supply independent static descriptors')
def test_owned_compiled_swift_descriptors_match_nm_and_demangler(tmp_path):
    target=tmp_path/'oracle.dylib'
    subprocess.run(['/usr/bin/xcrun','swiftc','-emit-library','-parse-as-library',
        '-module-name','QuayOracle','-module-cache-path',str(tmp_path/'module-cache'),
        '-o',str(target),str(ROOT/'sources/swift_metadata_vectors.swift')],check=True,capture_output=True)
    with target.open('rb') as stream:
        image=imagequay.load_image(stream)
    swift=quay_SwiftImage.from_image(NS(image=image,classlist=[]))
    actual={item.name:item for item in swift.types}
    expected_fields={'QuayValue':['number','label'],'QuayChoice':['value','empty'],
                     'QuayReference':['count','value']}
    assert {name:[field.name for field in item.fields] for name,item in actual.items()} == expected_fields
    nm=subprocess.check_output(['/usr/bin/xcrun','nm','-g','-n',str(target)],text=True)
    descriptors=[]
    for line in nm.splitlines():
        match=re.match(r'([0-9a-fA-F]+) \w (\S+Mn)$',line)
        if match:descriptors.append((int(match[1],16),match[2]))
    demangled=subprocess.run(['/usr/bin/xcrun','swift-demangle','--compact'],
        input='\n'.join(name for _,name in descriptors)+'\n',text=True,check=True,capture_output=True).stdout.splitlines()
    assert len(descriptors) == len(demangled) == 3
    for (address,_),name in zip(descriptors,demangled):
        assert name.startswith('nominal type descriptor for QuayOracle.')
        nominal=name.rsplit('.',1)[1]
        assert actual[nominal].location == address
        assert actual[nominal].context_path == ('QuayOracle',nominal)
    assert actual['QuayChoice'].fields[0].symbolic_type
    assert actual['QuayValue'].fields[0].type_name_bytes == b'Si'
