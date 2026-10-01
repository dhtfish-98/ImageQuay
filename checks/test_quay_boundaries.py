"""Record identity, public data labels and errors around binary parsing."""
import pytest as quay_pytest
from imagequay_support.record_engine import quay_Struct
from imagequay_layout.binary_records import quay_linkedit_data_command
from imagequay_layout.header_codes import quay_LOAD_COMMAND


def test_quay_record_wire_keys_and_private_fields():
    quay_record=quay_Struct.create_with_values(quay_linkedit_data_command,[0x1d,16,0x1234,0x5678],'little')
    assert quay_record.cmd==quay_record.quay_cmd==0x1d
    assert quay_record.serialize()['type']=='linkedit_data_command'
    assert tuple(quay_record.serialize())==('type','cmd','cmdsize','dataoff','datasize')
    assert 'quay_cmd' in vars(quay_record)
    assert 'cmd' not in vars(quay_record)


@quay_pytest.mark.parametrize('quay_order',['little','big'])
def test_quay_record_byte_order_roundtrip(quay_order):
    quay_record=quay_Struct.create_with_values(quay_linkedit_data_command,[0x1d,16,0x1234,0x5678],quay_order)
    quay_restored=quay_Struct.create_with_bytes(quay_linkedit_data_command,quay_record.raw,quay_order)
    assert quay_restored==quay_record
    assert quay_restored.serialize()==quay_record.serialize()


def test_quay_enum_error_keeps_display_label():
    with quay_pytest.raises(ValueError,match='is not a valid LOAD_COMMAND'):
        quay_LOAD_COMMAND(0xffffffff)
