# Derived from src/ktool/codesign.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  codesign.py
#
#
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2022.
#
import imagequay_boundary as _name_boundary
from typing import List as quay_List
from imagequay_layout.record_contract import quay_Constructable as quay_Constructable
from imagequay_layout.binary_records import quay_linkedit_data_command as quay_linkedit_data_command
from imagequay_layout.signing_records import *
from imagequay_support.diagnostics import quay_log as quay_log

@_name_boundary.callable_contract({'value': 'quay_value_6bf628e'}, 'swap_32')
def quay_swap_32(quay_value_6bf628e: int):
    quay_value_6bf628e = quay_value_6bf628e >> 8 & 16711935 | quay_value_6bf628e << 8 & 4278255360
    quay_value_6bf628e = quay_value_6bf628e >> 16 & 65535 | quay_value_6bf628e << 16 & 4294901760
    return quay_value_6bf628e

@_name_boundary.class_contract('CodesignInfo', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'superblob': 'quay_superblob', 'slots': 'quay_slots', 'entitlements': 'quay_entitlements', 'req_dat': 'quay_req_dat'})
class quay_CodesignInfo(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_1686436', 'image': 'quay_image_2ace247', 'codesign_cmd': 'quay_codesign_cmd_7657e88'}, 'from_image')
    def quay_from_image(quay_cls_1686436, quay_image_2ace247, quay_codesign_cmd_7657e88: quay_linkedit_data_command):
        quay_superblob_35e13a8: quay_SuperBlob = _name_boundary.attributes(quay_image_2ace247)['read_struct'](_name_boundary.attributes(quay_codesign_cmd_7657e88)['dataoff'], quay_SuperBlob)
        quay_slots_8609295: quay_List[quay_BlobIndex] = []
        quay_off_d666714 = _name_boundary.attributes(quay_codesign_cmd_7657e88)['dataoff'] + _name_boundary.attributes(quay_SuperBlob)['size']()
        quay_req_dat_f6cde79 = None
        quay_entitlements_ff8ff4f = ''
        quay_requirements_c4f3988 = ''
        for quay_i_13a2767 in range(quay_swap_32(_name_boundary.attributes(quay_superblob_35e13a8)['count'])):
            quay_blob_index_54735a8 = _name_boundary.attributes(quay_image_2ace247)['read_struct'](quay_off_d666714, quay_BlobIndex)
            _name_boundary.attributes(quay_blob_index_54735a8)['type'] = quay_swap_32(_name_boundary.attributes(quay_blob_index_54735a8)['type'])
            _name_boundary.attributes(quay_blob_index_54735a8)['offset'] = quay_swap_32(_name_boundary.attributes(quay_blob_index_54735a8)['offset'])
            quay_slots_8609295.append(quay_blob_index_54735a8)
            quay_off_d666714 += _name_boundary.attributes(quay_BlobIndex)['size']()
        for quay_blob_7c3fdb0 in quay_slots_8609295:
            if _name_boundary.attributes(quay_blob_7c3fdb0)['type'] == quay_CSSLOT_ENTITLEMENTS:
                quay_start_e1f16f4 = _name_boundary.attributes(quay_superblob_35e13a8)['off'] + _name_boundary.attributes(quay_blob_7c3fdb0)['offset']
                quay_ent_blob_04d2a23 = _name_boundary.attributes(quay_image_2ace247)['read_struct'](quay_start_e1f16f4, quay_Blob)
                _name_boundary.attributes(quay_ent_blob_04d2a23)['magic'] = quay_swap_32(_name_boundary.attributes(quay_ent_blob_04d2a23)['magic'])
                _name_boundary.attributes(quay_ent_blob_04d2a23)['length'] = quay_swap_32(_name_boundary.attributes(quay_ent_blob_04d2a23)['length'])
                quay_ent_size_2428d69 = _name_boundary.attributes(quay_ent_blob_04d2a23)['length']
                quay_entitlements_ff8ff4f = _name_boundary.attributes(quay_image_2ace247)['read_fixed_len_str'](quay_start_e1f16f4 + _name_boundary.attributes(quay_Blob)['size'](), quay_ent_size_2428d69 - _name_boundary.attributes(quay_Blob)['size']())
            elif _name_boundary.attributes(quay_blob_7c3fdb0)['type'] == quay_CSSLOT_REQUIREMENTS:
                quay_start_e1f16f4 = _name_boundary.attributes(quay_superblob_35e13a8)['off'] + _name_boundary.attributes(quay_blob_7c3fdb0)['offset']
                quay_req_blob_65c7ea9 = _name_boundary.attributes(quay_image_2ace247)['read_struct'](quay_start_e1f16f4, quay_Blob)
                _name_boundary.attributes(quay_req_blob_65c7ea9)['magic'] = quay_swap_32(_name_boundary.attributes(quay_req_blob_65c7ea9)['magic'])
                _name_boundary.attributes(quay_req_blob_65c7ea9)['length'] = quay_swap_32(_name_boundary.attributes(quay_req_blob_65c7ea9)['length'])
                quay_req_dat_f6cde79 = _name_boundary.attributes(quay_image_2ace247)['read_bytearray'](quay_start_e1f16f4 + _name_boundary.attributes(quay_Blob)['size'](), _name_boundary.attributes(quay_req_blob_65c7ea9)['length'] - _name_boundary.attributes(quay_Blob)['size']())
        return quay_cls_1686436(quay_superblob_35e13a8, quay_slots_8609295, entitlements=quay_entitlements_ff8ff4f, req_dat=quay_req_dat_f6cde79)

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_462ece3', 'args': 'quay_args_dcb4e70', 'kwargs': 'quay_kwargs_882350c'}, 'from_values')
    def quay_from_values(quay_cls_462ece3, *quay_args_dcb4e70, **quay_kwargs_882350c):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_3822b11'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_3822b11):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_7d49d2d', 'superblob': 'quay_superblob_f667335', 'slots': 'quay_slots_b72f4de', 'entitlements': 'quay_entitlements_13e200f', 'req_dat': 'quay_req_dat_2f7eec3'}, '__init__')
    def __init__(quay_self_7d49d2d, quay_superblob_f667335, quay_slots_b72f4de, quay_entitlements_13e200f=None, quay_req_dat_2f7eec3=None):
        _name_boundary.attributes(quay_self_7d49d2d)['superblob'] = quay_superblob_f667335
        _name_boundary.attributes(quay_self_7d49d2d)['slots'] = quay_slots_b72f4de
        _name_boundary.attributes(quay_self_7d49d2d)['entitlements'] = quay_entitlements_13e200f
        _name_boundary.attributes(quay_self_7d49d2d)['req_dat'] = quay_req_dat_2f7eec3
_name_boundary.module_contract(globals(), {'swap_32': 'quay_swap_32', 'Constructable': 'quay_Constructable', 'linkedit_data_command': 'quay_linkedit_data_command', 'CodesignInfo': 'quay_CodesignInfo', 'log': 'quay_log', 'List': 'quay_List'})
