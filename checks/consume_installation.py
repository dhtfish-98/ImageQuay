"""Run using python -I after wheel installation; never add the source tree."""
from pathlib import Path as ConsumerPath
import importlib as consumer_importlib
import io as consumer_io
import struct as consumer_struct
consumer_project='ImageQuay'
consumer_package='imagequay'
consumer_module=consumer_importlib.import_module(consumer_package)
consumer_location=ConsumerPath(consumer_module.__file__).resolve()
assert 'site-packages' in consumer_location.parts,consumer_location
if consumer_project=='ImageQuay':
    from imagequay_layout.binary_records import quay_linkedit_data_command
    from imagequay_support.record_engine import quay_Struct
    consumer_record=quay_Struct.create_with_values(quay_linkedit_data_command,[0x1d,16,0x1234,0x5678],'little')
    assert consumer_record.quay_cmd==consumer_record.cmd==0x1d
    assert consumer_record.serialize()['type']=='linkedit_data_command'
    assert consumer_record.raw==consumer_struct.pack('<IIII',0x1d,16,0x1234,0x5678)
    from imagequay_support.plist_codec import quay_dumps,quay_loads,FMT_BINARY
    assert quay_loads(quay_dumps({'value':True},fmt=FMT_BINARY))=={'value':True}
elif consumer_project=='TraceMeadow':
    from tracemeadow.event_records import meadow_from_kd_buf
    from tracemeadow.code_index import meadow_default_trace_codes
    consumer_record=meadow_from_kd_buf(b'\xff'*64)
    assert consumer_record.eventid==0xfffffffc and consumer_record.func_qualifier==3
    assert repr(consumer_record).startswith('Kevent(')
    assert meadow_default_trace_codes()
else:
    from policymosaic.regex_bytecode import mosaic_parse
    from policymosaic.filter_catalog import mosaic_Filters
    from policymosaic.string_bytecode import mosaic_SandboxString
    consumer_nodes=[]
    mosaic_parse(b'\x02.',0,consumer_nodes)
    assert consumer_nodes==[{'pos':-6,'type':'character','value':'[.]'}]
    assert mosaic_Filters.mosaic_filters
    assert mosaic_SandboxString().mosaic_parse_byte_string(b'\x40a\x0a',[])==['a']
print(consumer_project+' installed consumer PASS')
if consumer_project=='ImageQuay':
    import importlib.metadata
    import tempfile
    import stat
    from imagequay.container_io import quay_MachOFile,quay_MachOImageHeader
    from imagequay.metadata_reader import quay_ExportTrie
    from imagequay.failure_types import quay_MalformedMachOException
    from imagequay.file_ops import safe_open
    from types import SimpleNamespace
    assert importlib.metadata.version('imagequay')=='1.0.9'
    header=consumer_struct.pack('<8I',0xfeedfacf,0x01000007,3,2,0,0,0,0)
    owner=quay_MachOFile(consumer_io.BytesIO(header+b'\x04\x00\xc0\x90\x01\x00'))
    view=owner.slices[0]
    parsed=quay_MachOImageHeader.from_image(view)
    assert parsed.is64 and parsed.dyld_header.loadcnt==0
    minimal=SimpleNamespace(slice=view,read_bytearray=view.read_bytearray)
    assert quay_ExportTrie.from_image(minimal,32,6).symbols[0].address==18496
    try:view.read_bytearray(-1,1)
    except quay_MalformedMachOException:pass
    else:raise AssertionError('installed range checking is absent')
    with tempfile.TemporaryDirectory(prefix='imagequay-consumer-') as folder:
        destination=ConsumerPath(folder)/'private-output'
        with safe_open(destination,'wb') as stream:stream.write(b'owned')
        assert destination.read_bytes()==b'owned'
        assert stat.S_IMODE(destination.stat().st_mode)==0o600
        try:safe_open(destination,'wb')
        except FileExistsError:pass
        else:raise AssertionError('installed output protection is absent')
    print('ImageQuay 1.0.9 installed snapshot/export/private-output PASS')

    class InstalledSigned(quay_Struct):
        FIELDS={'signed':0x10004}
    class InstalledNested(quay_Struct):
        FIELDS={'prefix':2,'inner':InstalledSigned}
    consumer_nested=quay_Struct.create_with_bytes(InstalledNested,consumer_struct.pack('>Hi',0x1234,-9),'big')
    assert consumer_nested.inner.signed==-9 and consumer_nested.raw==consumer_struct.pack('>Hi',0x1234,-9)
    from imagequay_support.plist_codec import quay_InvalidFileException
    try:quay_loads(b'<!DOCTYPE plist [<!ENTITY x "expanded">]><plist><string>&x;</string></plist>')
    except quay_InvalidFileException:pass
    else:raise AssertionError('installed plist entity policy is absent')
    consumer_cycle=[];consumer_cycle.append(consumer_cycle)
    try:quay_dumps(consumer_cycle)
    except ValueError:pass
    else:raise AssertionError('installed plist cycle policy is absent')
    from imagequay_layout.pointer_records import quay_dyld_chained_ptr_64_rebase
    consumer_bits=quay_Struct.create_with_bytes(quay_dyld_chained_ptr_64_rebase,(0x123456789).to_bytes(8,'little'))
    assert consumer_bits.target==0x123456789 and consumer_bits.raw==(0x123456789).to_bytes(8,'little')
    print('ImageQuay 1.0.9 installed signed/nested/bitfield/plist policy PASS')

if consumer_project=='ImageQuay':
    from imagequay.objc_model import quay_TypeProcessor,quay_Property
    from imagequay.swift_model import quay_SwiftStruct,quay__FieldDescriptor,quay_Field
    consumer_processor=quay_TypeProcessor()
    assert consumer_processor.process('{Pair="items"[3i]}')[0].value.fields[0].declaration('items')=='int items[3]'
    assert consumer_processor.process('jd')[0].declaration('value')=='_Complex double value'
    assert quay_Property.from_values('title','T@"NSString",C,N').type=='NSString *'
    consumer_field=quay_Field(2,'Si','value')
    assert quay_SwiftStruct.from_values('Owned',quay__FieldDescriptor.from_values([consumer_field])).fields==[consumer_field]
    consumer_fixture=ConsumerPath(__file__).resolve().parents[1]/'Build'/'fixtures'/'testbin1.fat'
    with consumer_fixture.open('rb') as consumer_stream:consumer_owner=quay_MachOFile(consumer_stream)
    consumer_count=0
    for consumer_view in consumer_owner.slices:
        consumer_source=consumer_view.full_bytes_for_slice()
        consumer_image=consumer_module.load_image(consumer_view)
        consumer_objc=consumer_module.load_objc_metadata(consumer_image)
        assert consumer_objc.complete and not consumer_objc.errors
        assert len(consumer_objc.classlist)==1 and len(consumer_objc.classlist[0].methods)==5
        assert consumer_view.full_bytes_for_slice()==consumer_source
        consumer_count+=1
    assert consumer_count==3
    print('ImageQuay 1.0.9 installed language grammar/Swift models/three immutable ObjC slices PASS')
