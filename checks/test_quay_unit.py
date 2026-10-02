# Derived from tests/unit.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | tests
#  unit.py
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
import unittest as quay_unittest
import json as quay_json
import random as quay_random
import imagequay as quay_imagequay
from imagequay_layout.pointer_records import quay_ChainedPointerArm64E as quay_ChainedPointerArm64E
from imagequay.container_io import *
from imagequay.formatting import *
from imagequay.parsed_image import *
from imagequay_support.diagnostics import quay_log as quay_log, quay_LogLevel as quay_LogLevel
quay_scriptdir = _name_boundary.attributes(quay_os)['path'].dirname(_name_boundary.attributes(quay_os)['path'].realpath(__file__))
_name_boundary.attributes(_name_boundary.attributes(quay_sys)['path'])['insert'](0, _name_boundary.attributes(quay_os)['path'].abspath(f'{quay_scriptdir}/../src'))
_name_boundary.attributes(quay_log)['LOG_LEVEL'] = quay_LogLevel.WARN
quay_error_buffer = ''

@_name_boundary.callable_contract({'old': 'quay_old_4375c45', 'new': 'quay_new_6c90e5a'}, 'diff_byte_array_set_assertion')
def quay_diff_byte_array_set_assertion(quay_old_4375c45: bytearray, quay_new_6c90e5a: bytearray):
    if quay_old_4375c45 != quay_new_6c90e5a:
        quay_diff_a7f9004 = '        Old       New\n'
        for quay_index_db9dba1 in range(0, len(quay_old_4375c45), 4):
            quay_old_bytes_65e95ce = quay_old_4375c45[quay_index_db9dba1:quay_index_db9dba1 + 4]
            quay_new_bytes_310bb06 = quay_new_6c90e5a[quay_index_db9dba1:quay_index_db9dba1 + 4]
            quay_set_is_diff_086c356 = False
            for quay_sub_index_94921d3, quay_byte_c907d4e in enumerate(quay_old_bytes_65e95ce):
                try:
                    if quay_byte_c907d4e != quay_new_bytes_310bb06[quay_sub_index_94921d3]:
                        quay_set_is_diff_086c356 = True
                except IndexError:
                    quay_set_is_diff_086c356 = True
            if quay_set_is_diff_086c356:
                quay_diff_a7f9004 += hex(quay_index_db9dba1).ljust(8)
                quay_diff_a7f9004 += _name_boundary.attributes(quay_old_bytes_65e95ce)['hex']() + '  '
                quay_diff_a7f9004 += _name_boundary.attributes(quay_new_bytes_310bb06)['hex']() + '  '
                quay_diff_a7f9004 += '\n'
        print(quay_diff_a7f9004)
        raise AssertionError

@_name_boundary.callable_contract({'msg': 'quay_msg_e611b90'}, 'error_remap')
def quay_error_remap(quay_msg_e611b90):
    global quay_error_buffer
    quay_error_buffer += quay_msg_e611b90 + '\n'

@_name_boundary.callable_contract({}, 'enable_error_capture')
def quay_enable_error_capture():
    _name_boundary.attributes(quay_log)['LOG_ERR'] = quay_error_remap
    global quay_error_buffer
    quay_error_buffer = ''

@_name_boundary.callable_contract({'msg': 'quay_msg_75f6c77'}, 'assert_error_printed')
def quay_assert_error_printed(quay_msg_75f6c77):
    assert quay_msg_75f6c77 in quay_error_buffer, "Error buffer didn't have '{}', has '{}'".format(quay_msg_75f6c77, quay_error_buffer)

@_name_boundary.callable_contract({}, 'disable_error_capture')
def quay_disable_error_capture():
    _name_boundary.attributes(quay_log)['LOG_ERR'] = quay_print_err

@_name_boundary.class_contract('ScratchFile', {'copy': 'quay_copy', 'get': 'quay_get', 'read': 'quay_read', 'write': 'quay_write', 'reset': 'quay_reset', 'scratch': 'quay_scratch', 'backup': 'quay_backup', 'fp': 'quay_fp'})
class quay_ScratchFile:

    @_name_boundary.callable_contract({'self': 'quay_self_de47d24', 'fp': 'quay_fp_ff14f55'}, '__init__')
    def __init__(quay_self_de47d24, quay_fp_ff14f55):
        _name_boundary.attributes(quay_self_de47d24)['scratch'] = quay_BytesIO()
        _name_boundary.attributes(quay_self_de47d24)['backup'] = quay_BytesIO()
        _name_boundary.attributes(quay_self_de47d24)['fp'] = quay_fp_ff14f55
        quay_data_aed5feb = _name_boundary.attributes(quay_fp_ff14f55)['read']()
        if _name_boundary.has_attribute(_name_boundary.attributes(quay_self_de47d24)['fp'], 'close'):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_de47d24)['fp'])['close']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_de47d24)['backup'])['write'](quay_data_aed5feb)
        _name_boundary.attributes(quay_self_de47d24)['backup'].seek(0)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_de47d24)['scratch'])['write'](quay_data_aed5feb)
        _name_boundary.attributes(quay_self_de47d24)['scratch'].seek(0)

    @_name_boundary.callable_contract({'self': 'quay_self_639c739'}, 'copy')
    def quay_copy(quay_self_639c739):
        quay_fp_01ec69d = _name_boundary.attributes(quay_self_639c739)['get']()
        quay_new_38f23ab = quay_ScratchFile(quay_fp_01ec69d)
        _name_boundary.attributes(quay_new_38f23ab)['scratch'] = quay_BytesIO()
        _name_boundary.attributes(_name_boundary.attributes(quay_new_38f23ab)['scratch'])['write'](_name_boundary.attributes(_name_boundary.attributes(quay_self_639c739)['scratch'])['read']())
        _name_boundary.attributes(quay_self_639c739)['scratch'].seek(0)
        return quay_new_38f23ab

    @_name_boundary.callable_contract({'self': 'quay_self_e2eecab'}, 'get')
    def quay_get(quay_self_e2eecab):
        quay_copy_85586a9 = quay_BytesIO()
        _name_boundary.attributes(quay_copy_85586a9)['write'](_name_boundary.attributes(_name_boundary.attributes(quay_self_e2eecab)['scratch'])['read'](_name_boundary.attributes(quay_self_e2eecab)['scratch'].getbuffer().nbytes))
        quay_copy_85586a9.seek(0)
        return quay_copy_85586a9

    @_name_boundary.callable_contract({'self': 'quay_self_89e1b2c', 'location': 'quay_location_7dffe69', 'count': 'quay_count_ea730db'}, 'read')
    def quay_read(quay_self_89e1b2c, quay_location_7dffe69, quay_count_ea730db):
        _name_boundary.attributes(quay_self_89e1b2c)['scratch'].seek(quay_location_7dffe69)
        quay_data_ef722c4 = _name_boundary.attributes(_name_boundary.attributes(quay_self_89e1b2c)['scratch'])['read'](quay_count_ea730db)
        _name_boundary.attributes(quay_self_89e1b2c)['scratch'].seek(0)
        return quay_data_ef722c4

    @_name_boundary.callable_contract({'self': 'quay_self_07f35d6', 'location': 'quay_location_6890ff7', 'data': 'quay_data_85ec66b'}, 'write')
    def quay_write(quay_self_07f35d6, quay_location_6890ff7, quay_data_85ec66b):
        if isinstance(quay_data_85ec66b, int):
            quay_data_85ec66b = quay_data_85ec66b.to_bytes(4, 'big')
        _name_boundary.attributes(quay_self_07f35d6)['scratch'].seek(quay_location_6890ff7)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_07f35d6)['scratch'])['write'](quay_data_85ec66b)
        _name_boundary.attributes(quay_self_07f35d6)['scratch'].seek(0)

    @_name_boundary.callable_contract({'self': 'quay_self_4bd970f'}, 'reset')
    def quay_reset(quay_self_4bd970f):
        _name_boundary.attributes(quay_self_4bd970f)['scratch'] = quay_BytesIO()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_4bd970f)['scratch'])['write'](_name_boundary.attributes(_name_boundary.attributes(quay_self_4bd970f)['backup'])['read']())
        _name_boundary.attributes(quay_self_4bd970f)['backup'].seek(0)
        _name_boundary.attributes(quay_self_4bd970f)['scratch'].seek(0)

@_name_boundary.class_contract('sunion_test', {'_FIELDNAMES': 'quay__FIELDNAMES', '_SIZES': 'quay__SIZES', 'SIZE': 'quay_SIZE', 'field': 'quay_field'})
class quay_sunion_test(quay_Struct):
    quay__FIELDNAMES = ['field']
    quay__SIZES = [quay_ChainedPointerArm64E]
    quay_SIZE = quay_uint64_t

    @_name_boundary.callable_contract({'self': 'quay_self_e1220da', 'byte_order': 'quay_byte_order_ce30482'}, '__init__')
    def __init__(quay_self_e1220da, quay_byte_order_ce30482='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_e1220da)['_FIELDNAMES'], sizes=_name_boundary.attributes(quay_self_e1220da)['_SIZES'], byte_order=quay_byte_order_ce30482)

@_name_boundary.class_contract('StructTestCase', {'test_equality_check': 'quay_test_equality_check', 'test_union': 'quay_test_union'})
class quay_StructTestCase(quay_unittest.TestCase):

    @_name_boundary.callable_contract({'self': 'quay_self_9be658c'}, 'test_equality_check')
    def quay_test_equality_check(quay_self_9be658c):
        quay_s1_c0c4db6 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_linkedit_data_command, [52 | quay_LC_REQ_DYLD, 16, 49152, 208], 'little')
        quay_s2_40a81d0 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_linkedit_data_command, [52 | quay_LC_REQ_DYLD, 16, 49152, 208], 'little')
        quay_s3_cc0470a = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_linkedit_data_command, [52 | quay_LC_REQ_DYLD, 16, 49152, 224], 'little')
        assert quay_s1_c0c4db6 == quay_s2_40a81d0
        assert quay_s1_c0c4db6 != quay_s3_cc0470a

    @_name_boundary.callable_contract({'self': 'quay_self_0d4b033'}, 'test_union')
    def quay_test_union(quay_self_0d4b033):
        quay_tval_e3f45b5 = 6533314739538231299
        quay_tval_e3f45b5 = int('{:08b}'.format(quay_tval_e3f45b5)[::-1], 2)
        quay_tval_raw_f99c197 = quay_tval_e3f45b5.to_bytes(8, 'little')
        quay_stc_9859b04 = _name_boundary.attributes(quay_Struct)['create_with_bytes'](quay_sunion_test, quay_tval_raw_f99c197)
        assert _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_stc_9859b04)['field'])['dyld_chained_ptr_arm64e_auth_rebase'])['target'] == int('{:08b}'.format(1521155876)[::-1], 2)

@_name_boundary.class_contract('BackingFileTestCase', {'test_with_mmaped_and_actual_file_pointer': 'quay_test_with_mmaped_and_actual_file_pointer'})
class quay_BackingFileTestCase(quay_unittest.TestCase):

    @_name_boundary.callable_contract({'self': 'quay_self_e645777'}, 'test_with_mmaped_and_actual_file_pointer')
    def quay_test_with_mmaped_and_actual_file_pointer(quay_self_e645777):
        quay_fp_b23f7a7 = open(quay_scriptdir + '/bins/testbin1', 'rb')
        quay_bf_cc927d8 = quay_BackingFile(quay_fp_b23f7a7, use_mmaped_io=True)
        quay_self_e645777.assertNotEqual(_name_boundary.attributes(quay_bf_cc927d8)['size'], 0)
        _name_boundary.attributes(quay_bf_cc927d8)['write'](0, b'\xde\xad\xbe\xef')
        quay_self_e645777.assertEqual(_name_boundary.attributes(quay_bf_cc927d8)['read_bytes'](0, 4), b'\xde\xad\xbe\xef')
        _name_boundary.attributes(quay_fp_b23f7a7)['close']()

@_name_boundary.class_contract('SliceTestCase', {'test_patch': 'quay_test_patch', 'test_find': 'quay_test_find', 'test_get_bytes': 'quay_test_get_bytes', 'test_get_str': 'quay_test_get_str', 'test_get_cstr': 'quay_test_get_cstr', 'test_decode_uleb128': 'quay_test_decode_uleb128', 'thin': 'quay_thin', 'fat': 'quay_fat'})
class quay_SliceTestCase(quay_unittest.TestCase):

    @_name_boundary.callable_contract({'self': 'quay_self_db281c8', 'args': 'quay_args_95870ef', 'kwargs': 'quay_kwargs_6e40578'}, '__init__')
    def __init__(quay_self_db281c8, *quay_args_95870ef, **quay_kwargs_6e40578):
        super().__init__(*quay_args_95870ef, **quay_kwargs_6e40578)
        _name_boundary.attributes(quay_self_db281c8)['thin'] = quay_ScratchFile(open(quay_scriptdir + '/bins/testbin1', 'rb'))
        _name_boundary.attributes(quay_self_db281c8)['fat'] = quay_ScratchFile(open(quay_scriptdir + '/bins/testbin1.fat', 'rb'))

    @_name_boundary.callable_contract({'self': 'quay_self_a48d06d'}, 'test_patch')
    def quay_test_patch(quay_self_a48d06d):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_a48d06d)['thin'])['reset']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_a48d06d)['fat'])['reset']()
        quay_macho_5aa4270 = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_a48d06d)['thin'])['get']())
        quay_macho_slice_2e13bd4 = _name_boundary.attributes(quay_macho_5aa4270)['slices'][0]
        _name_boundary.attributes(quay_macho_slice_2e13bd4)['patch'](0, b'\xde\xad\xbe\xef')
        _name_boundary.attributes(_name_boundary.attributes(quay_self_a48d06d)['thin'])['write'](0, 3735928559)
        quay_self_a48d06d.assertEqual(_name_boundary.attributes(quay_macho_slice_2e13bd4)['full_bytes_for_slice'](), _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_a48d06d)['thin'])['get']())['read']())
        _name_boundary.attributes(_name_boundary.attributes(quay_self_a48d06d)['thin'])['reset']()
        quay_self_a48d06d.assertNotEqual(_name_boundary.attributes(quay_macho_slice_2e13bd4)['full_bytes_for_slice'](), _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_a48d06d)['thin'])['get']())['read']())
        quay_macho_5aa4270 = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_a48d06d)['fat'])['get']())
        quay_macho_slice_2e13bd4 = _name_boundary.attributes(quay_macho_5aa4270)['slices'][1]
        _name_boundary.attributes(quay_macho_slice_2e13bd4)['patch'](0, b'\xde\xad\xbe\xef')
        _name_boundary.attributes(_name_boundary.attributes(quay_self_a48d06d)['fat'])['write'](_name_boundary.attributes(quay_macho_slice_2e13bd4)['offset'], 3735928559)
        quay_self_a48d06d.assertEqual(_name_boundary.attributes(quay_macho_slice_2e13bd4)['full_bytes_for_slice'](), bytes(bytearray(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_a48d06d)['fat'])['get']())['read']())[_name_boundary.attributes(quay_macho_slice_2e13bd4)['offset']:_name_boundary.attributes(quay_macho_slice_2e13bd4)['offset'] + _name_boundary.attributes(quay_macho_slice_2e13bd4)['size']]))

    @_name_boundary.callable_contract({'self': 'quay_self_dcd478c'}, 'test_find')
    def quay_test_find(quay_self_dcd478c):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_dcd478c)['thin'])['reset']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_dcd478c)['fat'])['reset']()
        quay_macho_57cf453 = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_dcd478c)['thin'])['get']())
        quay_macho_slice_5f043c3 = _name_boundary.attributes(quay_macho_57cf453)['slices'][0]
        quay_size_87e46e3 = _name_boundary.attributes(quay_macho_slice_5f043c3)['size']
        quay_loadsize_ac97e00 = _name_boundary.attributes(quay_macho_slice_5f043c3)['read_uint'](20, 4) + 32
        quay_random_location_696200e = quay_random.randint(quay_loadsize_ac97e00, quay_size_87e46e3)
        quay_needle_1821279 = b'\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef'
        _name_boundary.attributes(_name_boundary.attributes(quay_self_dcd478c)['thin'])['write'](quay_random_location_696200e, quay_needle_1821279)
        quay_macho_57cf453 = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_dcd478c)['thin'])['get']())
        quay_macho_slice_5f043c3 = _name_boundary.attributes(quay_macho_57cf453)['slices'][0]
        quay_location_2fba14b = _name_boundary.attributes(quay_macho_slice_5f043c3)['find'](quay_needle_1821279)
        quay_self_dcd478c.assertEqual(quay_location_2fba14b, quay_random_location_696200e)
        quay_macho_57cf453 = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_dcd478c)['fat'])['get']())
        quay_macho_slice_5f043c3 = _name_boundary.attributes(quay_macho_57cf453)['slices'][1]
        quay_slice_base_d30f2ae = _name_boundary.attributes(quay_macho_slice_5f043c3)['offset']
        quay_size_87e46e3 = _name_boundary.attributes(quay_macho_slice_5f043c3)['size']
        quay_loadsize_ac97e00 = _name_boundary.attributes(quay_macho_slice_5f043c3)['read_uint'](20, 4) + 32
        quay_random_location_696200e = quay_random.randint(quay_loadsize_ac97e00, quay_size_87e46e3)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_dcd478c)['fat'])['write'](quay_slice_base_d30f2ae + quay_random_location_696200e, quay_needle_1821279)
        quay_macho_57cf453 = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_dcd478c)['fat'])['get']())
        quay_macho_slice_5f043c3 = _name_boundary.attributes(quay_macho_57cf453)['slices'][1]
        quay_location_2fba14b = _name_boundary.attributes(quay_macho_slice_5f043c3)['find'](quay_needle_1821279)
        quay_self_dcd478c.assertEqual(quay_location_2fba14b, quay_random_location_696200e)

    @_name_boundary.callable_contract({'self': 'quay_self_0666f60'}, 'test_get_bytes')
    def quay_test_get_bytes(quay_self_0666f60):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0666f60)['thin'])['reset']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0666f60)['fat'])['reset']()
        quay_macho_87206ea = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_0666f60)['thin'])['get']())
        quay_macho_slice_d2469f5 = _name_boundary.attributes(quay_macho_87206ea)['slices'][0]
        quay_size_12b5e76 = _name_boundary.attributes(quay_macho_slice_d2469f5)['size']
        quay_loadsize_202a646 = _name_boundary.attributes(quay_macho_slice_d2469f5)['read_uint'](20, 4) + 32
        quay_random_location_af76b26 = quay_random.randint(quay_loadsize_202a646, quay_size_12b5e76)
        quay_write_b24ca7b = b'\xde\xad\xbe\xef'
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0666f60)['thin'])['write'](quay_random_location_af76b26, quay_write_b24ca7b)
        quay_macho_87206ea = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_0666f60)['thin'])['get']())
        quay_macho_slice_d2469f5 = _name_boundary.attributes(quay_macho_87206ea)['slices'][0]
        quay_readout_112796e = _name_boundary.attributes(quay_macho_slice_d2469f5)['read_bytearray'](quay_random_location_af76b26, 4)
        quay_self_0666f60.assertEqual(quay_write_b24ca7b, quay_readout_112796e)

    @_name_boundary.callable_contract({'self': 'quay_self_a848ae8'}, 'test_get_str')
    def quay_test_get_str(quay_self_a848ae8):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_a848ae8)['thin'])['reset']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_a848ae8)['fat'])['reset']()
        quay_macho_0a6cfd2 = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_a848ae8)['thin'])['get']())
        quay_macho_slice_9cb8d41 = _name_boundary.attributes(quay_macho_0a6cfd2)['slices'][0]
        quay_size_e014f7c = _name_boundary.attributes(quay_macho_slice_9cb8d41)['size']
        quay_loadsize_c443348 = _name_boundary.attributes(quay_macho_slice_9cb8d41)['read_uint'](20, 4) + 32
        quay_random_location_168cee9 = quay_random.randint(quay_loadsize_c443348, quay_size_e014f7c)
        quay_write_07515b1 = b'Decode a printable string.'
        _name_boundary.attributes(_name_boundary.attributes(quay_self_a848ae8)['thin'])['write'](quay_random_location_168cee9, quay_write_07515b1)
        quay_macho_0a6cfd2 = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_a848ae8)['thin'])['get']())
        quay_macho_slice_9cb8d41 = _name_boundary.attributes(quay_macho_0a6cfd2)['slices'][0]
        quay_readout_008afab = _name_boundary.attributes(quay_macho_slice_9cb8d41)['read_fixed_len_str'](quay_random_location_168cee9, len(quay_write_07515b1))
        quay_self_a848ae8.assertEqual(quay_write_07515b1.decode('utf-8'), quay_readout_008afab)

    @_name_boundary.callable_contract({'self': 'quay_self_0cf6bb8'}, 'test_get_cstr')
    def quay_test_get_cstr(quay_self_0cf6bb8):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0cf6bb8)['thin'])['reset']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0cf6bb8)['fat'])['reset']()
        quay_macho_d4059ea = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_0cf6bb8)['thin'])['get']())
        quay_macho_slice_1811458 = _name_boundary.attributes(quay_macho_d4059ea)['slices'][0]
        quay_size_af7a908 = _name_boundary.attributes(quay_macho_slice_1811458)['size']
        quay_loadsize_70aa07c = _name_boundary.attributes(quay_macho_slice_1811458)['read_uint'](20, 4) + 32
        quay_random_location_c9f1023 = quay_random.randint(quay_loadsize_70aa07c, quay_size_af7a908)
        quay_write_5c38a0b = b'Decode a printable string.\x00'
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0cf6bb8)['thin'])['write'](quay_random_location_c9f1023, quay_write_5c38a0b)
        quay_macho_d4059ea = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_0cf6bb8)['thin'])['get']())
        quay_macho_slice_1811458 = _name_boundary.attributes(quay_macho_d4059ea)['slices'][0]
        quay_readout_a73724c = _name_boundary.attributes(quay_macho_slice_1811458)['read_cstr'](quay_random_location_c9f1023)
        quay_self_0cf6bb8.assertEqual(quay_write_5c38a0b[:-1].decode('utf-8'), quay_readout_a73724c)

    @_name_boundary.callable_contract({'self': 'quay_self_0e3f7ad'}, 'test_decode_uleb128')
    def quay_test_decode_uleb128(quay_self_0e3f7ad):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0e3f7ad)['thin'])['reset']()
        quay_value_5ddb1d6 = 624485
        quay_encoded_7d8e5e2 = b'\xe5\x8e&'
        quay_macho_2c8dc26 = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_0e3f7ad)['thin'])['get']())
        quay_macho_slice_ed07f61 = _name_boundary.attributes(quay_macho_2c8dc26)['slices'][0]
        quay_size_fd9007a = _name_boundary.attributes(quay_macho_slice_ed07f61)['size']
        quay_loadsize_c784b05 = _name_boundary.attributes(quay_macho_slice_ed07f61)['read_uint'](20, 4) + 32
        quay_random_location_c6267bb = quay_random.randint(quay_loadsize_c784b05, quay_size_fd9007a)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0e3f7ad)['thin'])['write'](quay_random_location_c6267bb, quay_encoded_7d8e5e2)
        quay_macho_2c8dc26 = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_0e3f7ad)['thin'])['get']())
        quay_macho_slice_ed07f61 = _name_boundary.attributes(quay_macho_2c8dc26)['slices'][0]
        quay_decoded_value_5a37a82, quay___7ae3ee7 = _name_boundary.attributes(quay_macho_slice_ed07f61)['read_uleb128'](quay_random_location_c6267bb)
        quay_self_0e3f7ad.assertEqual(quay_value_5ddb1d6, quay_decoded_value_5a37a82)

@_name_boundary.class_contract('ImageHeaderTestCase', {'test_constructable': 'quay_test_constructable', 'test_bad_load_command': 'quay_test_bad_load_command', 'test_readint': 'quay_test_readint', 'test_insert_cmd': 'quay_test_insert_cmd', 'test_remove_cmd': 'quay_test_remove_cmd', 'test_replace_load_command': 'quay_test_replace_load_command', 'thin': 'quay_thin', 'thin_lib': 'quay_thin_lib'})
class quay_ImageHeaderTestCase(quay_unittest.TestCase):

    @_name_boundary.callable_contract({'self': 'quay_self_749eb47', 'args': 'quay_args_ae9aa3b', 'kwargs': 'quay_kwargs_9d2688a'}, '__init__')
    def __init__(quay_self_749eb47, *quay_args_ae9aa3b, **quay_kwargs_9d2688a):
        super().__init__(*quay_args_ae9aa3b, **quay_kwargs_9d2688a)
        _name_boundary.attributes(quay_self_749eb47)['thin'] = quay_ScratchFile(open(quay_scriptdir + '/bins/testbin1', 'rb'))
        _name_boundary.attributes(quay_self_749eb47)['thin_lib'] = quay_ScratchFile(open(quay_scriptdir + '/bins/testlib1.dylib', 'rb'))

    @_name_boundary.callable_contract({'self': 'quay_self_8e21cd9'}, 'test_constructable')
    def quay_test_constructable(quay_self_8e21cd9):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_8e21cd9)['thin'])['reset']()
        quay_image_59df87d = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_8e21cd9)['thin'])['get']())
        quay_image_header_df22477 = _name_boundary.attributes(quay_image_59df87d)['macho_header']
        quay_old_image_header_raw_bb28cc5 = _name_boundary.attributes(_name_boundary.attributes(quay_image_59df87d)['macho_header'])['raw_bytes']()
        quay_flags_7889bf1 = _name_boundary.attributes(quay_image_header_df22477)['flags']
        quay_filetype_384b497 = _name_boundary.attributes(quay_image_header_df22477)['filetype']
        quay_cpu_type_78c5f3e = _name_boundary.attributes(_name_boundary.attributes(quay_image_59df87d)['slice'])['type']
        quay_cpu_subtype_a4525a2 = _name_boundary.attributes(_name_boundary.attributes(quay_image_59df87d)['slice'])['subtype']
        quay_load_command_items_d345fb9 = []
        for quay_command_81580ed in _name_boundary.attributes(_name_boundary.attributes(quay_image_59df87d)['macho_header'])['load_commands']:
            if isinstance(quay_command_81580ed, quay_segment_command) or isinstance(quay_command_81580ed, quay_segment_command_64):
                quay_load_command_items_d345fb9.append(quay_Segment(quay_image_59df87d, quay_command_81580ed))
            elif isinstance(quay_command_81580ed, quay_dylib_command):
                quay_suffix_12621c0 = _name_boundary.attributes(quay_image_59df87d)['read_cstr'](_name_boundary.attributes(quay_command_81580ed)['off'] + _name_boundary.attributes(quay_command_81580ed.__class__)['size']())
                quay_encoded_489d718 = quay_suffix_12621c0.encode('utf-8') + b'\x00'
                while (len(quay_encoded_489d718) + _name_boundary.attributes(quay_command_81580ed.__class__)['size']()) % 8 != 0:
                    quay_encoded_489d718 += b'\x00'
                quay_load_command_items_d345fb9.append(quay_command_81580ed)
                quay_load_command_items_d345fb9.append(quay_encoded_489d718)
            elif quay_command_81580ed.__class__ in [quay_dylinker_command, quay_build_version_command]:
                quay_load_command_items_d345fb9.append(quay_command_81580ed)
                quay_actual_size_a01ce16 = _name_boundary.attributes(quay_command_81580ed)['cmdsize']
                quay_dat_59c0a0c = _name_boundary.attributes(quay_image_59df87d)['read_bytearray'](_name_boundary.attributes(quay_command_81580ed)['off'] + _name_boundary.attributes(quay_command_81580ed)['size'](), quay_actual_size_a01ce16 - _name_boundary.attributes(quay_command_81580ed)['size']())
                quay_load_command_items_d345fb9.append(quay_dat_59c0a0c)
            else:
                quay_load_command_items_d345fb9.append(quay_command_81580ed)
        quay_new_image_header_42c6f26 = _name_boundary.attributes(quay_MachOImageHeader)['from_values'](_name_boundary.attributes(_name_boundary.attributes(quay_image_59df87d)['macho_header'])['is64'], quay_cpu_type_78c5f3e, quay_cpu_subtype_a4525a2, quay_filetype_384b497, quay_flags_7889bf1, quay_load_command_items_d345fb9)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_8e21cd9)['thin'])['write'](0, _name_boundary.attributes(quay_new_image_header_42c6f26)['raw_bytes']())
        quay_new_image_header_raw_406cd08 = _name_boundary.attributes(quay_new_image_header_42c6f26)['raw_bytes']()
        quay_diff_byte_array_set_assertion(bytearray(quay_old_image_header_raw_bb28cc5), bytearray(quay_new_image_header_raw_406cd08))
        _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_8e21cd9)['thin'])['get']())

    @_name_boundary.callable_contract({'self': 'quay_self_0c19e22'}, 'test_bad_load_command')
    def quay_test_bad_load_command(quay_self_0c19e22):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0c19e22)['thin'])['reset']()
        quay_image_3c5be98 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_0c19e22)['thin'])['get']())
        quay_image_header_dfb529b = _name_boundary.attributes(quay_image_3c5be98)['macho_header']
        quay_flags_32e5f28 = _name_boundary.attributes(quay_image_header_dfb529b)['flags']
        quay_filetype_338e9c1 = _name_boundary.attributes(quay_image_header_dfb529b)['filetype']
        quay_cpu_type_f129a05 = _name_boundary.attributes(_name_boundary.attributes(quay_image_3c5be98)['slice'])['type']
        quay_cpu_subtype_af4e31c = _name_boundary.attributes(_name_boundary.attributes(quay_image_3c5be98)['slice'])['subtype']
        quay_load_command_items_d7d7268 = []
        for quay_command_6e686d5 in _name_boundary.attributes(_name_boundary.attributes(quay_image_3c5be98)['macho_header'])['load_commands']:
            if isinstance(quay_command_6e686d5, quay_segment_command) or isinstance(quay_command_6e686d5, quay_segment_command_64):
                quay_load_command_items_d7d7268.append(quay_Segment(quay_image_3c5be98, quay_command_6e686d5))
            elif isinstance(quay_command_6e686d5, quay_dylib_command):
                quay_suffix_9cdeb25 = _name_boundary.attributes(quay_image_3c5be98)['read_cstr'](_name_boundary.attributes(quay_command_6e686d5)['off'] + _name_boundary.attributes(quay_command_6e686d5.__class__)['size']())
                quay_encoded_5a50c31 = quay_suffix_9cdeb25.encode('utf-8') + b'\x00'
                while (len(quay_encoded_5a50c31) + _name_boundary.attributes(quay_command_6e686d5.__class__)['size']()) % 8 != 0:
                    quay_encoded_5a50c31 += b'\x00'
                quay_load_command_items_d7d7268.append(quay_command_6e686d5)
                quay_load_command_items_d7d7268.append(quay_encoded_5a50c31)
            elif quay_command_6e686d5.__class__ == quay_symtab_command:
                _name_boundary.attributes(quay_command_6e686d5)['cmd'] = 153
                quay_load_command_items_d7d7268.append(quay_command_6e686d5)
            elif quay_command_6e686d5.__class__ in [quay_dylinker_command, quay_build_version_command]:
                quay_load_command_items_d7d7268.append(quay_command_6e686d5)
                quay_actual_size_ef5ef4d = _name_boundary.attributes(quay_command_6e686d5)['cmdsize']
                quay_dat_ee5bdb4 = _name_boundary.attributes(quay_image_3c5be98)['read_bytearray'](_name_boundary.attributes(quay_command_6e686d5)['off'] + _name_boundary.attributes(quay_command_6e686d5)['size'](), quay_actual_size_ef5ef4d - _name_boundary.attributes(quay_command_6e686d5)['size']())
                quay_load_command_items_d7d7268.append(quay_dat_ee5bdb4)
            else:
                quay_load_command_items_d7d7268.append(quay_command_6e686d5)
        quay_new_image_header_eccaf7c = _name_boundary.attributes(quay_MachOImageHeader)['from_values'](_name_boundary.attributes(_name_boundary.attributes(quay_image_3c5be98)['macho_header'])['is64'], quay_cpu_type_f129a05, quay_cpu_subtype_af4e31c, quay_filetype_338e9c1, quay_flags_32e5f28, quay_load_command_items_d7d7268)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0c19e22)['thin'])['write'](0, _name_boundary.attributes(quay_new_image_header_eccaf7c)['raw_bytes']())
        quay_enable_error_capture()
        _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_0c19e22)['thin'])['get']())
        quay_disable_error_capture()
        quay_assert_error_printed('Bad Load Command ')
        quay_assert_error_printed('0x99 -')

    @_name_boundary.callable_contract({'self': 'quay_self_8b97dd7'}, 'test_readint')
    def quay_test_readint(quay_self_8b97dd7):
        quay_inp_0d21aaa = 4294967212
        quay_output_30f59d0 = -84
        assert quay_uint_to_int(quay_inp_0d21aaa, 32) == quay_output_30f59d0

    @_name_boundary.callable_contract({'self': 'quay_self_6cc5bc3'}, 'test_insert_cmd')
    def quay_test_insert_cmd(quay_self_6cc5bc3):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_6cc5bc3)['thin'])['reset']()
        quay_image_ecbf92e = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_6cc5bc3)['thin'])['get']())
        quay_image_header_1a2a8b3 = _name_boundary.attributes(quay_image_ecbf92e)['macho_header']
        quay_dylib_item_ed0aadf = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_dylib, [24, 2, 65536, 65536])
        quay_dylib_cmd_b4a3751 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_dylib_command, [_name_boundary.attributes(quay_LOAD_COMMAND.LOAD_DYLIB)['value'], 0, _name_boundary.attributes(quay_dylib_item_ed0aadf)['raw']])
        quay_new_header_41dfea4 = _name_boundary.attributes(_name_boundary.attributes(quay_image_ecbf92e)['macho_header'])['insert_load_command'](quay_dylib_cmd_b4a3751, -1, suffix='/unit/test')
        assert len(_name_boundary.attributes(quay_image_header_1a2a8b3)['load_commands']) + 1 == len(_name_boundary.attributes(quay_new_header_41dfea4)['load_commands'])
        assert b'/unit/test' in _name_boundary.attributes(quay_new_header_41dfea4)['raw']
        assert _name_boundary.attributes(quay_image_header_1a2a8b3)['raw'] != _name_boundary.attributes(quay_new_header_41dfea4)['raw']
        _name_boundary.attributes(_name_boundary.attributes(quay_self_6cc5bc3)['thin'])['write'](0, _name_boundary.attributes(quay_new_header_41dfea4)['raw'])
        quay_new_image_f11c354 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_6cc5bc3)['thin'])['get']())
        assert _name_boundary.attributes(_name_boundary.attributes(quay_new_image_f11c354)['linked_images'][-1])['install_name'] == '/unit/test'

    @_name_boundary.callable_contract({'self': 'quay_self_6ff7536'}, 'test_remove_cmd')
    def quay_test_remove_cmd(quay_self_6ff7536):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_6ff7536)['thin'])['reset']()
        quay_image_7124a6c = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_6ff7536)['thin'])['get']())
        quay_image_header_3de4067 = _name_boundary.attributes(quay_image_7124a6c)['macho_header']
        quay_new_header_a80f317 = _name_boundary.attributes(_name_boundary.attributes(quay_image_7124a6c)['macho_header'])['remove_load_command'](5)
        assert len(_name_boundary.attributes(quay_image_header_3de4067)['load_commands']) - 1 == len(_name_boundary.attributes(quay_new_header_a80f317)['load_commands'])
        _name_boundary.attributes(_name_boundary.attributes(quay_self_6ff7536)['thin'])['write'](0, _name_boundary.attributes(quay_new_header_a80f317)['raw_bytes']())
        _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_6ff7536)['thin'])['get']())

    @_name_boundary.callable_contract({'self': 'quay_self_598e015'}, 'test_replace_load_command')
    def quay_test_replace_load_command(quay_self_598e015):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_598e015)['thin_lib'])['reset']()
        quay_image_5b725c6 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_598e015)['thin_lib'])['get']())
        quay_image_header_d7a72b3 = _name_boundary.attributes(quay_image_5b725c6)['macho_header']
        quay_old_commands_4ee1783 = [*_name_boundary.attributes(quay_image_header_d7a72b3)['load_commands']]
        quay_dylib_item_0c342d4 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_dylib, [24, 1, 0, 0])
        quay_dylib_cmd_24e9802 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_dylib_command, [_name_boundary.attributes(quay_LOAD_COMMAND.ID_DYLIB)['value'], 0, quay_dylib_item_0c342d4])
        quay_new_header_5ba7077 = _name_boundary.attributes(_name_boundary.attributes(quay_image_5b725c6)['macho_header'])['replace_load_command'](quay_dylib_cmd_24e9802, 4, suffix='/unit/test/iname')
        _name_boundary.attributes(_name_boundary.attributes(quay_self_598e015)['thin_lib'])['write'](0, _name_boundary.attributes(quay_new_header_5ba7077)['raw'])
        quay_new_image_2a3302a = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_598e015)['thin_lib'])['get']())
        assert _name_boundary.attributes(quay_new_image_2a3302a)['install_name'] == '/unit/test/iname'
        for quay_i_04ff6da, quay_cmd_008b798 in enumerate(_name_boundary.attributes(quay_new_header_5ba7077)['load_commands']):
            if not quay_cmd_008b798 == quay_old_commands_4ee1783[quay_i_04ff6da]:
                _name_boundary.attributes(quay_log)['error'](f'{str(quay_cmd_008b798)} != {str(quay_old_commands_4ee1783[quay_i_04ff6da])}')
                raise AssertionError

@_name_boundary.class_contract('MachOLoaderTestCase', {'test_thin_type': 'quay_test_thin_type', 'test_fat_type': 'quay_test_fat_type', 'test_bad_magic': 'quay_test_bad_magic', 'test_bad_fat_offset': 'quay_test_bad_fat_offset', 'test_slice_count': 'quay_test_slice_count', 'thin': 'quay_thin', 'fat': 'quay_fat'})
class quay_MachOLoaderTestCase(quay_unittest.TestCase):

    @_name_boundary.callable_contract({'self': 'quay_self_fa7278b', 'args': 'quay_args_1556a05', 'kwargs': 'quay_kwargs_1e5f523'}, '__init__')
    def __init__(quay_self_fa7278b, *quay_args_1556a05, **quay_kwargs_1e5f523):
        super().__init__(*quay_args_1556a05, **quay_kwargs_1e5f523)
        _name_boundary.attributes(quay_self_fa7278b)['thin'] = quay_ScratchFile(open(quay_scriptdir + '/bins/testbin1', 'rb'))
        _name_boundary.attributes(quay_self_fa7278b)['fat'] = quay_ScratchFile(open(quay_scriptdir + '/bins/testbin1.fat', 'rb'))

    @_name_boundary.callable_contract({'self': 'quay_self_5d44968'}, 'test_thin_type')
    def quay_test_thin_type(quay_self_5d44968):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_5d44968)['thin'])['reset']()
        quay_macho_9e5bf10 = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_5d44968)['thin'])['get']())
        assert _name_boundary.attributes(quay_macho_9e5bf10)['type'] == quay_MachOFileType.THIN

    @_name_boundary.callable_contract({'self': 'quay_self_e1a6742'}, 'test_fat_type')
    def quay_test_fat_type(quay_self_e1a6742):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_e1a6742)['fat'])['reset']()
        quay_macho_2411964 = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_e1a6742)['fat'])['get']())
        assert _name_boundary.attributes(quay_macho_2411964)['type'] == quay_MachOFileType.FAT

    @_name_boundary.callable_contract({'self': 'quay_self_0e1f64d'}, 'test_bad_magic')
    def quay_test_bad_magic(quay_self_0e1f64d):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0e1f64d)['thin'])['reset']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0e1f64d)['thin'])['write'](0, 3735928559)
        quay_enable_error_capture()
        with quay_self_0e1f64d.assertRaises(quay_UnsupportedFiletypeException) as quay_context_bda9477:
            quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_0e1f64d)['thin'])['get']())
        quay_disable_error_capture()

    @_name_boundary.callable_contract({'self': 'quay_self_0c0b29b'}, 'test_bad_fat_offset')
    def quay_test_bad_fat_offset(quay_self_0c0b29b):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0c0b29b)['fat'])['reset']()
        quay_macho_3f1be9a = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_0c0b29b)['fat'])['get']())
        quay_header_f4b949a: quay_fat_header = _name_boundary.attributes(quay_macho_3f1be9a)['_load_struct'](0, quay_fat_header, 'big')
        for quay_off_f6d6098 in range(1, _name_boundary.attributes(quay_header_f4b949a)['nfat_archs']):
            quay_offset_9d60d74 = _name_boundary.attributes(quay_fat_header)['size']() + quay_off_f6d6098 * _name_boundary.attributes(quay_fat_arch)['size']()
            quay_arch_struct_054a4d4: quay_fat_arch = _name_boundary.attributes(quay_macho_3f1be9a)['_load_struct'](quay_offset_9d60d74, quay_fat_arch, 'big')
            _name_boundary.attributes(quay_arch_struct_054a4d4)['offset'] = 3735928559
            _name_boundary.attributes(_name_boundary.attributes(quay_self_0c0b29b)['fat'])['write'](_name_boundary.attributes(quay_arch_struct_054a4d4)['off'], _name_boundary.attributes(quay_arch_struct_054a4d4)['raw'])
        quay_enable_error_capture()
        with quay_self_0c0b29b.assertRaises(quay_MalformedMachOException):
            quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_0c0b29b)['fat'])['get']())
        quay_disable_error_capture()

    @_name_boundary.callable_contract({'self': 'quay_self_1d26664'}, 'test_slice_count')
    def quay_test_slice_count(quay_self_1d26664):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_1d26664)['fat'])['reset']()
        quay_macho_985ea4e = quay_imagequay.load_macho_file(_name_boundary.attributes(_name_boundary.attributes(quay_self_1d26664)['fat'])['get']())
        quay_header_b5fd887: quay_fat_header = _name_boundary.attributes(quay_macho_985ea4e)['_load_struct'](0, quay_fat_header, 'big')
        quay_slice_count_9cd2ef5 = _name_boundary.attributes(quay_header_b5fd887)['nfat_archs']
        quay_self_1d26664.assertEqual(quay_slice_count_9cd2ef5, len(_name_boundary.attributes(quay_macho_985ea4e)['slices']))

@_name_boundary.class_contract('SegmentLCTestCase', {'test_constructable': 'quay_test_constructable', 'thin': 'quay_thin'})
class quay_SegmentLCTestCase(quay_unittest.TestCase):

    @_name_boundary.callable_contract({'self': 'quay_self_3b60b93', 'args': 'quay_args_62434d5', 'kwargs': 'quay_kwargs_1379227'}, '__init__')
    def __init__(quay_self_3b60b93, *quay_args_62434d5, **quay_kwargs_1379227):
        super().__init__(*quay_args_62434d5, **quay_kwargs_1379227)
        _name_boundary.attributes(quay_self_3b60b93)['thin'] = quay_ScratchFile(open(quay_scriptdir + '/bins/testbin1', 'rb'))

    @_name_boundary.callable_contract({'self': 'quay_self_91d3e2d'}, 'test_constructable')
    def quay_test_constructable(quay_self_91d3e2d):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_91d3e2d)['thin'])['reset']()
        quay_image_05f6b94 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_91d3e2d)['thin'])['get']())
        quay_image_header_00ab593 = _name_boundary.attributes(quay_image_05f6b94)['macho_header']
        quay_old_command_57334f6: quay_segment_command_64 = _name_boundary.attributes(quay_image_header_00ab593)['load_commands'][1]
        quay_old_dat_f15d202 = _name_boundary.attributes(quay_image_05f6b94)['read_bytearray'](_name_boundary.attributes(quay_old_command_57334f6)['off'], _name_boundary.attributes(quay_old_command_57334f6)['cmdsize'])
        quay_text_26cd81b = _name_boundary.attributes(quay_image_05f6b94)['segments']['__TEXT']
        quay_cmd_9a135ef: quay_segment_command = _name_boundary.attributes(quay_text_26cd81b)['cmd']
        quay_text_sections_ad0f862 = []
        for quay_s_2cb9c8f in _name_boundary.attributes(quay_text_26cd81b)['sections'].values():
            quay_text_sections_ad0f862.append(quay_s_2cb9c8f)
        quay_lc_c0c6400 = _name_boundary.attributes(quay_SegmentLoadCommand)['from_values'](_name_boundary.attributes(quay_image_header_00ab593)['is64'], '__TEXT', _name_boundary.attributes(quay_text_26cd81b)['vm_address'], _name_boundary.attributes(quay_text_26cd81b)['size'], _name_boundary.attributes(quay_text_26cd81b)['file_address'], _name_boundary.attributes(quay_text_26cd81b)['file_size'], _name_boundary.attributes(quay_cmd_9a135ef)['maxprot'], _name_boundary.attributes(quay_cmd_9a135ef)['initprot'], _name_boundary.attributes(quay_cmd_9a135ef)['flags'], quay_text_sections_ad0f862)
        quay_new_dat_9b8a125 = _name_boundary.attributes(quay_lc_c0c6400)['raw_bytes']()
        quay_diff_byte_array_set_assertion(bytearray(quay_old_dat_f15d202), bytearray(quay_new_dat_9b8a125))

@_name_boundary.class_contract('VMTestCase', {'test_good_16k_page_vm_map': 'quay_test_good_16k_page_vm_map', 'test_fallback_vm': 'quay_test_fallback_vm', 'test_bad_16k_page_vm_map': 'quay_test_bad_16k_page_vm_map'})
class quay_VMTestCase(quay_unittest.TestCase):

    @_name_boundary.callable_contract({'self': 'quay_self_c8240c4'}, 'test_good_16k_page_vm_map')
    def quay_test_good_16k_page_vm_map(quay_self_c8240c4):
        quay_vm_702637f = quay_VM(16384)
        quay_vm_base_d70f9bb = quay_random.randint(100, 200) * 16384
        quay_file_base_b266930 = quay_random.randint(1, 100) * 16384
        quay_diff_a959f19 = quay_vm_base_d70f9bb - quay_file_base_b266930
        quay_size_b63b4ae = 16384 * 2
        quay_k_seg_start_d000fa2 = 18446744073709486080
        _name_boundary.attributes(quay_vm_702637f)['map_pages'](16384 * 300, quay_k_seg_start_d000fa2, 16384)
        _name_boundary.attributes(quay_vm_702637f)['map_pages'](quay_file_base_b266930, quay_vm_base_d70f9bb, quay_size_b63b4ae)
        for quay_address_ff10455 in range(quay_vm_base_d70f9bb, quay_vm_base_d70f9bb + quay_size_b63b4ae, 4):
            quay_correct_address_f829d44 = quay_address_ff10455 - quay_diff_a959f19
            quay_translated_address_01da8f5 = _name_boundary.attributes(quay_vm_702637f)['translate'](quay_address_ff10455)
            quay_self_c8240c4.assertEqual(quay_correct_address_f829d44, quay_translated_address_01da8f5)
            quay_self_c8240c4.assertEqual(_name_boundary.attributes(quay_vm_702637f)['de_translate'](quay_translated_address_01da8f5), quay_address_ff10455)
        _name_boundary.attributes(quay_vm_702637f)['detag_64'] = True
        quay_translated_address_01da8f5 = _name_boundary.attributes(quay_vm_702637f)['translate'](quay_vm_base_d70f9bb + 320232761589760)
        quay_self_c8240c4.assertEqual(quay_translated_address_01da8f5, quay_vm_base_d70f9bb - quay_diff_a959f19)
        _name_boundary.attributes(quay_vm_702637f)['detag_64'] = False
        _name_boundary.attributes(quay_vm_702637f)['detag_kern_64'] = True
        quay_tagged_k64_addr_f4fcec4 = 1311954866448302088
        quay_self_c8240c4.assertEqual(_name_boundary.attributes(quay_vm_702637f)['translate'](quay_tagged_k64_addr_f4fcec4), 16384 * 300 + 8)
        _name_boundary.attributes(quay_vm_702637f)['detag_kern_64'] = False
        quay_self_c8240c4.assertFalse(_name_boundary.attributes(quay_vm_702637f)['vm_check'](-4000))
        quay_self_c8240c4.assertTrue(_name_boundary.attributes(quay_vm_702637f)['vm_check'](quay_vm_base_d70f9bb))
        with quay_self_c8240c4.assertRaises(quay_VMAddressingError):
            _name_boundary.attributes(quay_vm_702637f)['de_translate'](-4)

    @_name_boundary.callable_contract({'self': 'quay_self_933583d'}, 'test_fallback_vm')
    def quay_test_fallback_vm(quay_self_933583d):
        quay_vm_443b8d2: quay_VM = quay_VM(16384)
        quay_vm_base_09e9497 = quay_random.randint(100, 200) * 16384
        quay_file_base_e93f308 = quay_random.randint(1, 100) * 16384
        quay_diff_736e6df = quay_vm_base_09e9497 - quay_file_base_e93f308
        quay_size_7af3c90 = 16384 * 2
        _name_boundary.attributes(quay_vm_443b8d2)['map_pages'](quay_file_base_e93f308, quay_vm_base_09e9497, quay_size_7af3c90)
        quay_k_seg_start_21724b4 = 18446744073709486080
        _name_boundary.attributes(quay_vm_443b8d2)['map_pages'](16384 * 300, quay_k_seg_start_21724b4, 16384)
        quay_vm_443b8d2: quay_MisalignedVM = _name_boundary.attributes(quay_vm_443b8d2)['fallback']
        for quay_address_c5e629f in range(quay_vm_base_09e9497, quay_vm_base_09e9497 + quay_size_7af3c90, 4):
            quay_correct_address_c272327 = quay_address_c5e629f - quay_diff_736e6df
            quay_translated_address_b142f26 = _name_boundary.attributes(quay_vm_443b8d2)['translate'](quay_address_c5e629f)
            quay_self_933583d.assertEqual(quay_correct_address_c272327, quay_translated_address_b142f26)
            quay_self_933583d.assertEqual(_name_boundary.attributes(quay_vm_443b8d2)['de_translate'](quay_translated_address_b142f26), quay_address_c5e629f)
        _name_boundary.attributes(quay_vm_443b8d2)['detag_64'] = True
        quay_translated_address_b142f26 = _name_boundary.attributes(quay_vm_443b8d2)['translate'](quay_vm_base_09e9497 + 320232761589760)
        quay_self_933583d.assertEqual(quay_translated_address_b142f26, quay_vm_base_09e9497 - quay_diff_736e6df)
        _name_boundary.attributes(quay_vm_443b8d2)['detag_64'] = False
        _name_boundary.attributes(quay_vm_443b8d2)['detag_kern_64'] = True
        quay_tagged_k64_addr_6ea299a = 1311954866448302088
        quay_self_933583d.assertEqual(_name_boundary.attributes(quay_vm_443b8d2)['translate'](quay_tagged_k64_addr_6ea299a), 16384 * 300 + 8)
        _name_boundary.attributes(quay_vm_443b8d2)['detag_kern_64'] = False
        quay_self_933583d.assertFalse(_name_boundary.attributes(quay_vm_443b8d2)['vm_check'](-4000))
        quay_self_933583d.assertTrue(_name_boundary.attributes(quay_vm_443b8d2)['vm_check'](quay_vm_base_09e9497))

    @_name_boundary.callable_contract({'self': 'quay_self_9ff8bc1'}, 'test_bad_16k_page_vm_map')
    def quay_test_bad_16k_page_vm_map(quay_self_9ff8bc1):
        quay_vm_0d0c332 = quay_VM(16384)
        quay_vm_base_15b806d = quay_random.randint(100, 200) * 16384
        quay_file_base_6b3109c = quay_random.randint(1, 100) * 16384
        quay_vm_base_15b806d -= 1
        with quay_self_9ff8bc1.assertRaises(quay_MachOAlignmentError) as quay_context_5241858:
            _name_boundary.attributes(quay_vm_0d0c332)['map_pages'](quay_vm_base_15b806d, quay_file_base_6b3109c, 16384)
        quay_vm_base_15b806d += 1
        quay_file_base_6b3109c -= 1
        with quay_self_9ff8bc1.assertRaises(quay_MachOAlignmentError) as quay_context_5241858:
            _name_boundary.attributes(quay_vm_0d0c332)['map_pages'](quay_vm_base_15b806d, quay_file_base_6b3109c, 16384)
        quay_file_base_6b3109c += 1
        with quay_self_9ff8bc1.assertRaises(quay_MachOAlignmentError) as quay_context_5241858:
            _name_boundary.attributes(quay_vm_0d0c332)['map_pages'](quay_vm_base_15b806d, quay_file_base_6b3109c, 14745)

@_name_boundary.class_contract('ImageTestCase', {'test_serialization': 'quay_test_serialization', 'test_vm_realignment': 'quay_test_vm_realignment', 'test_rw_prims': 'quay_test_rw_prims', 'thin': 'quay_thin'})
class quay_ImageTestCase(quay_unittest.TestCase):

    @_name_boundary.callable_contract({'self': 'quay_self_ee03bf8', 'args': 'quay_args_331fa2b', 'kwargs': 'quay_kwargs_9a0472c'}, '__init__')
    def __init__(quay_self_ee03bf8, *quay_args_331fa2b, **quay_kwargs_9a0472c):
        super().__init__(*quay_args_331fa2b, **quay_kwargs_9a0472c)
        _name_boundary.attributes(quay_self_ee03bf8)['thin'] = quay_ScratchFile(open(quay_scriptdir + '/bins/testbin1', 'rb'))

    @_name_boundary.callable_contract({'self': 'quay_self_b78b4af'}, 'test_serialization')
    def quay_test_serialization(quay_self_b78b4af):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_b78b4af)['thin'])['reset']()
        quay_img_13849e3 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_b78b4af)['thin'])['get']())
        _name_boundary.attributes(quay_img_13849e3)['rpath'] = 'asdf'
        _name_boundary.attributes(quay_img_13849e3)['install_name'] = 'asdf'
        quay_img_dict_a1ef244 = _name_boundary.attributes(quay_img_13849e3)['serialize']()
        quay_out_7453ef0 = quay_json.dumps(quay_img_dict_a1ef244)
        assert quay_out_7453ef0
        quay_re_in_0c54fde = quay_json.loads(quay_out_7453ef0)
        assert quay_re_in_0c54fde

    @_name_boundary.callable_contract({'self': 'quay_self_2dc2cc2'}, 'test_vm_realignment')
    def quay_test_vm_realignment(quay_self_2dc2cc2):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['reset']()
        quay_image_8990831 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['get']())
        quay_macho_header_f39646f: quay_mach_header_64 = _name_boundary.attributes(_name_boundary.attributes(quay_image_8990831)['macho_header'])['dyld_header']
        _name_boundary.attributes(quay_macho_header_f39646f)['cpu_type'] = _name_boundary.attributes(quay_CPUType.ARM64)['value']
        _name_boundary.attributes(quay_macho_header_f39646f)['cpu_subtype'] = _name_boundary.attributes(quay_CPUSubTypeARM64.ARM64E)['value']
        quay_raw_9590d8b = _name_boundary.attributes(quay_macho_header_f39646f)['raw']
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['write'](0, quay_raw_9590d8b)
        quay_image_8990831 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['get']())
        quay_self_2dc2cc2.assertTrue(_name_boundary.attributes(_name_boundary.attributes(quay_image_8990831)['vm'])['detag_64'])
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['reset']()
        quay_image_8990831 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['get']())
        quay_dat_6b2e7e2 = _name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['read'](128, 8)
        quay_dat_6b2e7e2 = int.from_bytes(quay_dat_6b2e7e2, 'little')
        quay_dat_6b2e7e2 += 4096
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['write'](128, quay_dat_6b2e7e2.to_bytes(8, 'little'))
        quay_dat_6b2e7e2 = _name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['read'](136, 8)
        quay_dat_6b2e7e2 = int.from_bytes(quay_dat_6b2e7e2, 'little')
        quay_dat_6b2e7e2 -= 4096
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['write'](136, quay_dat_6b2e7e2.to_bytes(8, 'little'))
        with quay_self_2dc2cc2.assertRaises(quay_VMAddressingError):
            quay_image_8990831 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['get']())
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['reset']()
        quay_image_8990831 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['get']())
        quay_dat_6b2e7e2 = _name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['read'](128, 8)
        quay_dat_6b2e7e2 = int.from_bytes(quay_dat_6b2e7e2, 'little')
        quay_dat_6b2e7e2 += 4100
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['write'](128, quay_dat_6b2e7e2.to_bytes(8, 'little'))
        quay_dat_6b2e7e2 = _name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['read'](136, 8)
        quay_dat_6b2e7e2 = int.from_bytes(quay_dat_6b2e7e2, 'little')
        quay_dat_6b2e7e2 -= 4100
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['write'](136, quay_dat_6b2e7e2.to_bytes(8, 'little'))
        with quay_self_2dc2cc2.assertRaises(quay_VMAddressingError):
            quay_image_8990831 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_2dc2cc2)['thin'])['get']())

    @_name_boundary.callable_contract({'self': 'quay_self_23ab95e'}, 'test_rw_prims')
    def quay_test_rw_prims(quay_self_23ab95e):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_23ab95e)['thin'])['reset']()
        quay_str_and_cstr_test_string_bddd0d0 = 'AAAA AAAA'
        quay_str_size_5f55526 = len(quay_str_and_cstr_test_string_bddd0d0)
        quay_str_test_location_67d2775 = 4096
        quay_cstr_test_location_aed3df5 = 8192
        _name_boundary.attributes(_name_boundary.attributes(quay_self_23ab95e)['thin'])['write'](quay_str_test_location_67d2775, quay_str_and_cstr_test_string_bddd0d0.encode('utf-8'))
        _name_boundary.attributes(_name_boundary.attributes(quay_self_23ab95e)['thin'])['write'](quay_cstr_test_location_aed3df5, quay_str_and_cstr_test_string_bddd0d0.encode('utf-8') + b'\x00')
        quay_image_5f4e635 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_23ab95e)['thin'])['get']())
        quay_macho_slice_fc2f04a = _name_boundary.attributes(quay_image_5f4e635)['slice']
        quay_vm_base_73a0e38 = _name_boundary.attributes(_name_boundary.attributes(quay_image_5f4e635)['vm'])['de_translate'](0)
        quay_self_23ab95e.assertTrue(_name_boundary.attributes(quay_image_5f4e635)['vm_check'](quay_vm_base_73a0e38))
        quay_self_23ab95e.assertEqual(_name_boundary.attributes(_name_boundary.attributes(quay_image_5f4e635)['vm'])['translate'](quay_vm_base_73a0e38), 0)
        quay_self_23ab95e.assertEqual(_name_boundary.attributes(quay_macho_slice_fc2f04a)['read_uint'](0, 4), _name_boundary.attributes(quay_image_5f4e635)['read_uint'](0, 4))
        quay_self_23ab95e.assertEqual(_name_boundary.attributes(quay_macho_slice_fc2f04a)['read_uint'](0, 4), _name_boundary.attributes(quay_image_5f4e635)['read_uint'](quay_vm_base_73a0e38, 4, vm=True))
        quay_self_23ab95e.assertEqual(_name_boundary.attributes(quay_macho_slice_fc2f04a)['read_bytearray'](0, 4), _name_boundary.attributes(quay_image_5f4e635)['read_bytearray'](0, 4))
        quay_self_23ab95e.assertEqual(_name_boundary.attributes(quay_macho_slice_fc2f04a)['read_bytearray'](0, 4), _name_boundary.attributes(quay_image_5f4e635)['read_bytearray'](quay_vm_base_73a0e38, 4, vm=True))
        quay_self_23ab95e.assertEqual(_name_boundary.attributes(quay_macho_slice_fc2f04a)['read_struct'](0, quay_mach_header_64, 'little'), _name_boundary.attributes(quay_image_5f4e635)['read_struct'](0, quay_mach_header_64, endian='little', vm=False, force_reload=True))
        quay_self_23ab95e.assertEqual(_name_boundary.attributes(quay_macho_slice_fc2f04a)['read_struct'](0, quay_mach_header_64, 'little'), _name_boundary.attributes(quay_image_5f4e635)['read_struct'](quay_vm_base_73a0e38, quay_mach_header_64, vm=True, endian='little', force_reload=True))
        quay_self_23ab95e.assertEqual(quay_str_and_cstr_test_string_bddd0d0, _name_boundary.attributes(quay_image_5f4e635)['read_fixed_len_str'](quay_str_test_location_67d2775, quay_str_size_5f55526))
        quay_self_23ab95e.assertEqual(quay_str_and_cstr_test_string_bddd0d0, _name_boundary.attributes(quay_image_5f4e635)['read_fixed_len_str'](_name_boundary.attributes(_name_boundary.attributes(quay_image_5f4e635)['vm'])['de_translate'](quay_str_test_location_67d2775), quay_str_size_5f55526, vm=True))
        quay_self_23ab95e.assertEqual(quay_str_and_cstr_test_string_bddd0d0, _name_boundary.attributes(quay_image_5f4e635)['read_cstr'](quay_cstr_test_location_aed3df5))
        quay_self_23ab95e.assertEqual(quay_str_and_cstr_test_string_bddd0d0, _name_boundary.attributes(quay_image_5f4e635)['read_cstr'](_name_boundary.attributes(_name_boundary.attributes(quay_image_5f4e635)['vm'])['de_translate'](quay_cstr_test_location_aed3df5), vm=True))

@_name_boundary.class_contract('CodesignTestClass', {'test_codesigning': 'quay_test_codesigning', 'signed': 'quay_signed'})
class quay_CodesignTestClass(quay_unittest.TestCase):

    @_name_boundary.callable_contract({'self': 'quay_self_d72d757', 'args': 'quay_args_0b7d697', 'kwargs': 'quay_kwargs_ac849fe'}, '__init__')
    def __init__(quay_self_d72d757, *quay_args_0b7d697, **quay_kwargs_ac849fe):
        super().__init__(*quay_args_0b7d697, **quay_kwargs_ac849fe)
        _name_boundary.attributes(quay_self_d72d757)['signed'] = quay_ScratchFile(open(quay_scriptdir + '/bins/testbin1.signed', 'rb'))

    @_name_boundary.callable_contract({'self': 'quay_self_50ddd7d'}, 'test_codesigning')
    def quay_test_codesigning(quay_self_50ddd7d):
        quay_im_876ce71 = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_50ddd7d)['signed'])['get']())
        assert len(_name_boundary.attributes(_name_boundary.attributes(quay_im_876ce71)['codesign_info'])['entitlements']) != 0

@_name_boundary.class_contract('DyldTestCase', {'test_install_name': 'quay_test_install_name', 'test_linked_images': 'quay_test_linked_images', 'thin': 'quay_thin', 'thin_lib': 'quay_thin_lib'})
class quay_DyldTestCase(quay_unittest.TestCase):
    """
    This operates primarily on the "Image" class, but Image doesn't handle loading its values in, Dyld does
    we will test the cyclomatically complex portions of the Image class elsewhere.
    """

    @_name_boundary.callable_contract({'self': 'quay_self_8f8f4db', 'args': 'quay_args_4813e9e', 'kwargs': 'quay_kwargs_15a47a1'}, '__init__')
    def __init__(quay_self_8f8f4db, *quay_args_4813e9e, **quay_kwargs_15a47a1):
        super().__init__(*quay_args_4813e9e, **quay_kwargs_15a47a1)
        _name_boundary.attributes(quay_self_8f8f4db)['thin'] = quay_ScratchFile(open(quay_scriptdir + '/bins/testbin1', 'rb'))
        _name_boundary.attributes(quay_self_8f8f4db)['thin_lib'] = quay_ScratchFile(open(quay_scriptdir + '/bins/testlib1.dylib', 'rb'))

    @_name_boundary.callable_contract({'self': 'quay_self_111cafe'}, 'test_install_name')
    def quay_test_install_name(quay_self_111cafe):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_111cafe)['thin_lib'])['reset']()
        quay_image_0585c0f = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_111cafe)['thin_lib'])['get']())
        quay_self_111cafe.assertEqual('bins/testlib1.dylib', _name_boundary.attributes(quay_image_0585c0f)['install_name'])

    @_name_boundary.callable_contract({'self': 'quay_self_3e84cbe'}, 'test_linked_images')
    def quay_test_linked_images(quay_self_3e84cbe):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_3e84cbe)['thin_lib'])['reset']()
        quay_image_39395bc = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(_name_boundary.attributes(quay_self_3e84cbe)['thin_lib'])['get']())
        quay_self_3e84cbe.assertEqual(len(_name_boundary.attributes(quay_image_39395bc)['linked_images']), 3)
        quay_self_3e84cbe.assertEqual(_name_boundary.attributes(_name_boundary.attributes(quay_image_39395bc)['linked_images'][0])['install_name'], '/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation')
        quay_self_3e84cbe.assertEqual(_name_boundary.attributes(_name_boundary.attributes(quay_image_39395bc)['linked_images'][1])['install_name'], '/usr/lib/libSystem.B.dylib')
        quay_self_3e84cbe.assertEqual(_name_boundary.attributes(_name_boundary.attributes(quay_image_39395bc)['linked_images'][2])['install_name'], '/usr/lib/libobjc.A.dylib')
if __name__ == '__main__':
    _name_boundary.attributes(quay_ignore)['OBJC_ERRORS'] = False
_name_boundary.module_contract(globals(), {'enable_error_capture': 'quay_enable_error_capture', 'ChainedPointerArm64E': 'quay_ChainedPointerArm64E', 'SliceTestCase': 'quay_SliceTestCase', 'error_buffer': 'quay_error_buffer', 'unittest': 'quay_unittest', 'sunion_test': 'quay_sunion_test', 'CodesignTestClass': 'quay_CodesignTestClass', 'ImageTestCase': 'quay_ImageTestCase', 'scriptdir': 'quay_scriptdir', 'ktool': 'quay_imagequay', 'MachOLoaderTestCase': 'quay_MachOLoaderTestCase', 'disable_error_capture': 'quay_disable_error_capture', 'random': 'quay_random', 'BackingFileTestCase': 'quay_BackingFileTestCase', 'SegmentLCTestCase': 'quay_SegmentLCTestCase', 'StructTestCase': 'quay_StructTestCase', 'LogLevel': 'quay_LogLevel', 'ImageHeaderTestCase': 'quay_ImageHeaderTestCase', 'diff_byte_array_set_assertion': 'quay_diff_byte_array_set_assertion', 'DyldTestCase': 'quay_DyldTestCase', 'VMTestCase': 'quay_VMTestCase', 'ScratchFile': 'quay_ScratchFile', 'json': 'quay_json', 'assert_error_printed': 'quay_assert_error_printed', 'error_remap': 'quay_error_remap', 'log': 'quay_log'})
