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
