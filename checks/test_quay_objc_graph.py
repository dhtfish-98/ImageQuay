"""Objective-C graph boundaries and independent compiler/tool observations."""
import hashlib
import io
from pathlib import Path
import re
import struct
import subprocess
import sys
from types import SimpleNamespace as NS
import pytest
import imagequay
from imagequay.container_io import quay_MachOFile
from imagequay.failure_types import quay_MalformedMachOException as Malformed
from imagequay.formatting import quay_ignore
from imagequay.objc_model import (quay_ObjCImage,quay_Class,quay_Category,quay_Protocol,
    quay_Method,quay_MethodList,quay_Property,quay_Ivar,quay_TypeProcessor,
    quay_objc2_meth_list,quay_objc2_class,quay_objc2_class_ro,quay_objc2_prot,
    quay_objc2_ivar,quay_objc2_prot_list)
from imagequay_support.record_engine import quay_Struct

ROOT=Path(__file__).parent


def fixture(ptr_size=8,byte_order='little',base=None):
    base=(0x100000000 if ptr_size==8 else 0x1000) if base is None else base
    raw=bytearray(4096)
    prefix='<' if byte_order=='little' else '>'
    raw[:32]=struct.pack(prefix+'8I',0xfeedfacf,0x01000007,3,2,0,0,0,0)
    owner=quay_MachOFile(io.BytesIO(raw));view=owner.slices[0]
    image=NS(slice=view,ptr_size=ptr_size,base_name='Owned',symbols={},import_table={},chained_fixups=None)
    image.segments={'__DATA':NS(vm_address=base,file_address=0,file_size=len(raw),sections={})}
    def patch(offset,data):view.patch(offset,data)
    def uint(offset,value,width=None):patch(offset,value.to_bytes(width or ptr_size,byte_order))
    def text(offset,value):patch(offset,value.encode()+b'\0')
    def record(offset,kind,values):
        encoded=quay_Struct.create_with_values(kind,values,byte_order,ptr_size=ptr_size)
        patch(offset,encoded.raw)
        return encoded
    objc=quay_ObjCImage(image)
    return NS(objc=objc,image=image,base=base,patch=patch,uint=uint,text=text,record=record)


def class_record(f,*,superclass=0,isa=0,methods=0,protocols=0,ivars=0,properties=0):
    f.text(64,'OwnedClass')
    f.record(128,quay_objc2_class,[isa,superclass,0,0,(f.base+256)|3])
    f.record(256,quay_objc2_class_ro,[0,0,0,0,0,f.base+64,methods,protocols,ivars,0,properties])
    f.uint(1024,f.base+128)
    f.objc=quay_ObjCImage(f.image)
    return f.base+128


@pytest.mark.parametrize('ptr_size,byte_order',[(8,'little'),(4,'little'),(8,'big'),(4,'big')])
def test_class_records_preserve_pointer_width_and_byte_order(ptr_size,byte_order):
    f=fixture(ptr_size,byte_order)
    location=class_record(f)
    result=quay_Class.from_image(f.objc,f.base+1024)
    assert result.name=='OwnedClass' and result.loc==location
    assert result.raw_bytes()==f.image.slice.read_bytearray(128,5*ptr_size)
    assert f.objc.class_map[location] is result and f.objc.class_map[f.base+1024] is result
    assert quay_objc2_prot_list.size(ptr_size=ptr_size)==ptr_size


@pytest.mark.parametrize('ptr_size',[4,8])
def test_objc_protocol_root_reads_virtual_coordinates_and_pointer_sized_counts(ptr_size):
    f=fixture(ptr_size)
    f.text(64,'Base')
    f.record(128,quay_objc2_prot,[0,f.base+64,0,0,0,0,0,0,8*ptr_size+8,0])
    f.uint(1024,f.base+128)
    f.image.segments['__DATA'].sections={'__objc_protolist':NS(name='__objc_protolist',vm_address=f.base+1024,size=ptr_size)}
    result=quay_ObjCImage.from_image(f.image)
    assert result.complete and not result.errors and result.protolist[0].name=='Base'
    location=class_record(f,protocols=f.base+768)
    f.uint(768,1);f.uint(768+ptr_size,f.base+128)
    # Rebuild the class/protocol at distinct offsets: both are in one confined graph.
    f.record(1536,quay_objc2_prot,[0,f.base+80,0,0,0,0,0,0,8*ptr_size+8,0])
    f.text(80,'Adopted');f.uint(768+ptr_size,f.base+1536)
    f.objc=quay_ObjCImage(f.image)
    assert quay_Class.from_image(f.objc,location,class_ptr_is_direct=True).protocols[0].name=='Adopted'


@pytest.mark.parametrize('ptr_size',[4,8])
def test_chained_pointer_views_relocate_without_mutating_source(ptr_size):
    f=fixture(ptr_size);location=class_record(f)
    f.uint(1024,0xdeadbeef)
    f.uint(128+4*ptr_size,0xbaadf00d)
    f.objc=quay_ObjCImage(f.image)
    raw=f.image.slice.full_bytes_for_slice()
    f.image.chained_fixups=NS(rebases={f.base+1024:location,f.base+128+4*ptr_size:f.base+256},unresolved_rebases={})
    result=quay_Class.from_image(f.objc,f.base+1024)
    assert result.name=='OwnedClass'
    assert f.image.slice.full_bytes_for_slice()==raw
    f.image.chained_fixups.unresolved_rebases[f.base+128+4*ptr_size]={'cache':0}
    with pytest.raises(Malformed,match='cache base'):
        quay_Class.from_image(quay_ObjCImage(f.image),location,class_ptr_is_direct=True)


@pytest.mark.parametrize('direct',[False,True])
def test_relative_method_fields_are_signed_and_based_at_their_own_addresses(direct):
    f=fixture()
    f.text(64,'apply:');f.text(80,'v24@0:8i16');f.uint(96,f.base+64)
    flags=0x80000000|(0x40000000 if direct else 0)|12|3
    f.patch(256,struct.pack('<IIiii',flags,1,(64 if direct else 96)-264,80-268,128-272))
    f.objc=quay_ObjCImage(f.image)
    result=quay_MethodList(f.objc,f.objc.read_struct(f.base+256,quay_objc2_meth_list),f.base+256,False,'Owned')
    assert [(m.sel,m.imp,m.signature) for m in result.methods]==[('apply:',f.base+128,'-(void)apply:(int)arg0 ')]
    assert result.methods[0].raw_bytes()==struct.pack('<iii',(64 if direct else 96)-264,80-268,128-272)


def test_zero_relative_imp_is_the_storage_address_not_null():
    f=fixture();f.text(64,'apply');f.text(80,'v16@0:8')
    f.objc=quay_ObjCImage(f.image)
    result=quay_Method.from_image(f.objc,64-256,80-260,0,False,f.base+256,True,True)
    assert result.imp==f.base+264


@pytest.mark.parametrize('stride,count',[(20,1),(0,0),(24,0xffffffff),(24,1024)])
def test_method_list_rejects_format_count_and_full_span_before_walk(stride,count):
    f=fixture();f.patch(256,struct.pack('<II',stride,count));f.objc=quay_ObjCImage(f.image)
    with pytest.raises(Malformed):
        quay_MethodList(f.objc,f.objc.read_struct(f.base+256,quay_objc2_meth_list),f.base+256,False,'Owned')


@pytest.mark.parametrize('encoding,selector',[('v16@0:8i16','apply'),('v16@0:8','apply:'),('v24@0:8i16','apply:extra:')])
def test_selector_arity_cannot_silently_drop_encoded_arguments(encoding,selector):
    with pytest.raises(ValueError,match='argument count'):
        quay_Method.from_values(selector,encoding)


@pytest.mark.parametrize('attributes',['N','Ti,Ti','Ti,G','Ti,S','Ti,,N','T{A=i','Ti,Nbad','Tii'])
def test_property_attribute_structures_and_duplicate_types_are_explicit(attributes):
    with pytest.raises(ValueError):quay_Property.from_values('owned',attributes)


def test_property_accessors_objects_protocols_dynamic_and_unknown_metadata():
    value=quay_Property.from_values('title','T@"NSString",C,N,GreadTitle,SwriteTitle:,V_title,D,Zextension')
    assert value.type=='NSString *' and value.getter=='readTitle' and value.setter=='writeTitle:'
    assert value.attr.is_dynamic and value.unknown_attributes==('Zextension',)
    assert str(value)=='@property (copy, nonatomic, getter=readTitle, setter=writeTitle:) NSString * title'
    assert quay_Property.from_values('value','T@,N').type=='id'
    assert quay_Property.from_values('value','T@"<Owned>",R').type=='id<Owned>'
    assert quay_Property.from_values('value','Ti').setter=='setValue:'
    assert quay_Property.from_values('value','Ti,R').setter==''
    processor=quay_TypeProcessor()
    assert processor.process('@"NSString"')[0].declaration('title')=='NSString *title'
    assert processor.process('@"<Owned>"')[0].declaration('object')=='id<Owned> object'
    assert processor.process('jd')[0].declaration('value')=='_Complex double value'
    assert processor.process('A^i')[0].declaration('value')=='_Atomic(int *) value'


@pytest.mark.parametrize('ptr_size',[4,8])
def test_ivar_offset_dereferences_the_four_byte_abi_cell(ptr_size):
    f=fixture(ptr_size);f.text(64,'owned');f.text(80,'i');f.uint(96,20,4)
    f.record(256,quay_objc2_ivar,[f.base+96,f.base+64,f.base+80,2,4]);f.objc=quay_ObjCImage(f.image)
    result=quay_Ivar.from_image(f.objc,f.objc.read_struct(f.base+256,quay_objc2_ivar))
    assert result.offset==20 and result.offset_location==f.base+96
    assert result.serialize()['type_is_id'] is False


def test_class_cycle_partial_diagnostics_and_strict_error_contract(monkeypatch):
    f=fixture();location=class_record(f,superclass=f.base+128)
    partial=quay_Class.from_image(f.objc,location,class_ptr_is_direct=True)
    assert partial.name=='OwnedClass' and not f.objc.complete
    assert any('inheritance cycle' in message for message in partial.load_errors)
    monkeypatch.setattr(quay_ignore,'OBJC_ERRORS',False)
    with pytest.raises(Malformed,match='inheritance cycle'):
        quay_Class.from_image(quay_ObjCImage(f.image),location,class_ptr_is_direct=True)


def test_protocol_cycle_preserves_visible_local_errors():
    f=fixture();f.text(64,'Owned');f.uint(768,1);f.uint(776,f.base+128)
    f.record(128,quay_objc2_prot,[0,f.base+64,f.base+768,0,0,0,0,0,72,0]);f.objc=quay_ObjCImage(f.image)
    result=quay_Protocol.from_image(f.objc,f.objc.read_struct(f.base+128,quay_objc2_prot),f.base+128)
    assert result.name=='Owned' and not f.objc.complete
    assert any('inheritance cycle' in message for message in result.load_errors)


@pytest.mark.parametrize('declared_size',[0,71,4097])
def test_protocol_declared_size_stays_inside_header_and_segment(declared_size):
    f=fixture();f.text(64,'Owned');f.record(128,quay_objc2_prot,[0,f.base+64,0,0,0,0,0,0,declared_size,0]);f.objc=quay_ObjCImage(f.image)
    with pytest.raises(Malformed):quay_Protocol.from_image(f.objc,f.objc.read_struct(f.base+128,quay_objc2_prot),f.base+128)


def test_objc_root_rejects_partial_pointer_and_reports_each_invalid_item():
    f=fixture();section=NS(name='__objc_classlist',vm_address=f.base+1024,size=7)
    f.image.segments['__DATA'].sections={'__objc_classlist':section}
    with pytest.raises(Malformed,match='partial pointer'):quay_ObjCImage.from_image(f.image)
    section.size=16;f.uint(1024,f.base+4090);f.uint(1032,f.base+4095)
    result=quay_ObjCImage.from_image(f.image)
    assert not result.complete and not result.classlist and len(result.errors)==2
    assert result.serialize()['metadata-status']['complete'] is False
    assert result.serialize()['metadata-status']['errors']==result.errors


def apple_method_observations(output):
    return {(int(address,16),prefix,owner,selector) for address,prefix,owner,selector in
        re.findall(r'0x([0-9A-Fa-f]+)\s+([+-])\[([^ ]+) ([^\]]+)\]',output)}


def apple_arm64_32_empty_objc_output(output,path):
    lines=[line.strip() for line in output.splitlines()]
    header=[str(path)+' [arm64_32]:','-objc:']
    return lines==header or lines==header+['@interface (null) : (null)','@end']


def test_arm64_32_apple_empty_objc_output_shapes_are_exact():
    path=Path('/local/testbin1.fat')
    header=f'{path} [arm64_32]:\n    -objc:\n'
    assert apple_arm64_32_empty_objc_output(header,path)
    assert apple_arm64_32_empty_objc_output(header+'    @interface (null) : (null)\n    @end\n',path)
    assert not apple_arm64_32_empty_objc_output(header+'    @interface Other : NSObject\n    @end\n',path)
    assert not apple_arm64_32_empty_objc_output(header+'    @interface (null) : (null)\n    - (void)unexpected;\n    @end\n',path)


@pytest.mark.skipif(sys.platform!='darwin',reason='Apple dyld_info supplies a static metadata oracle')
@pytest.mark.parametrize('filename',['testbin1','testbin1.signed','testlib1.dylib','testbin1.fat'])
def test_all_six_legacy_slices_objc_methods_match_apple_tool_and_preserve_inputs(filename):
    path=ROOT/'bins'/filename;before=hashlib.sha256(path.read_bytes()).hexdigest()
    with path.open('rb') as stream:owner=quay_MachOFile(stream)
    total=0
    for view in owner.slices:
        image=imagequay.load_image(view);raw=view.full_bytes_for_slice();objc=imagequay.load_objc_metadata(image)
        arch=view.type.name.lower()
        if arch=='arm6432':arch='arm64_32'
        tool=subprocess.check_output(['/usr/bin/xcrun','dyld_info','-arch',arch,'-objc',str(path)],text=True)
        expected=apple_method_observations(tool)
        if arch=='arm64_32' and not expected:
            assert before=='21c25d914d271b1d6e001ae8e34a40e6283bf937ee951d21fa7a8ba094deb988'
            # The tool can render a null class placeholder without method data.
            # Accept only the two observed shapes, then require independent labels and IMPs.
            assert apple_arm64_32_empty_objc_output(tool,path)
            nm=subprocess.check_output(['/usr/bin/xcrun','nm','-arch',arch,'-n',str(path)],text=True)
            otool=subprocess.check_output(['/usr/bin/xcrun','otool','-arch',arch,'-ov',str(path)],text=True)
            expected={(int(address,16),prefix,owner,selector) for address,prefix,owner,selector in
                re.findall(r'^([0-9a-fA-F]+) \w ([+-])\[([^ ]+) ([^\]]+)\]$',nm,re.M)}
            decoded={(int(address,16),prefix,owner,selector) for address,prefix,owner,selector in
                re.findall(r'imp\s+0x[0-9a-fA-F]+ \(0x([0-9a-fA-F]+)\) ([+-])\[([^ ]+) ([^\]]+)\]',otool)}
            assert expected==decoded and len(decoded)==5
        actual={(method.imp,'+' if method.meta else '-',item.name,method.sel)
            for item in objc.classlist for method in item.methods}
        assert actual==expected and len(actual)==5
        assert objc.complete and not objc.errors
        assert len(objc.classlist)==1 and objc.classlist[0].superclass=='NSObject'
        assert view.full_bytes_for_slice()==raw
        total+=1
    assert total==(3 if filename.endswith('.fat') else 1)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==before


@pytest.mark.skipif(sys.platform!='darwin',reason='Clang and Apple dyld_info supply owned ObjC metadata')
def test_owned_compiled_objc_graph_matches_apple_protocol_category_and_method_oracle(tmp_path):
    path=tmp_path/'oracle.dylib'
    subprocess.run(['/usr/bin/xcrun','clang','-dynamiclib','-fobjc-arc','-framework','Foundation',
        '-target','arm64-apple-macos13','-o',str(path),str(ROOT/'sources/objc_metadata_vectors.m')],check=True,capture_output=True)
    before=path.read_bytes()
    with path.open('rb') as stream:image=imagequay.load_image(stream)
    objc=imagequay.load_objc_metadata(image)
    assert objc.complete and not objc.errors
    klass=objc.classlist[0];category=objc.catlist[0]
    assert (klass.name,klass.superclass)==('QuayRoot','NSObject')
    assert (category.name,category.classname)==('QuayExternal','NSObject')
    actual={(m.imp,'+' if m.meta else '-',c.name,m.sel) for c in objc.classlist for m in c.methods}
    # dyld_info's category header carries the category name; its method lines
    # identify only the owning class. Verify both rather than inventing a label.
    actual.update((m.imp,'+' if m.meta else '-',c.classname,m.sel) for c in objc.catlist for m in c.methods)
    tool=subprocess.check_output(['/usr/bin/xcrun','dyld_info','-objc',str(path)],text=True)
    assert actual==apple_method_observations(tool)
    assert '@interface NSObject(QuayExternal) : NSObject' in tool or '@interface NSObject(QuayExternal)' in tool
    assert len(actual)==12
    assert {p.name for p in klass.properties}=={'counter','title','tag','shared','doubled'}
    protocols={p.name:p for p in objc.protolist}
    assert {p.name for p in protocols['QuayChild'].protocols}=={'QuayBase'}
    assert {p.name for p in protocols['QuayChild'].class_properties}=={'shared'}
    assert {m.sel for m in protocols['QuayBase'].methods}=={'updateValue:','tag'}
    assert [(m.sel,m.meta) for m in protocols['QuayBase'].opt_methods]==[('make',True)]
    assert [(p.name,p.type) for p in category.properties]==[('quayMarker','int')]
    assert {ivar.name:ivar.offset for ivar in klass.ivars}=={'_counter':8,'_title':16}
    assert path.read_bytes()==before and image.slice.full_bytes_for_slice()==before
