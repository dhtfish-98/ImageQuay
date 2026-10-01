# Derived from src/ktool/objc.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  objc.py
#
#  This file contains utilities for parsing objective C classes within a MachO binary
#  I dont like it. The structure is bad and it needs gutted and reassembled.
#
#  Basically, ktool was originally this horrible hacked together single python script called 'kdump' that
#  did the bare minimum to try and dump objc metadata and spit out headers, bc we wanted a class dump that worked on
#  non-apple platforms
#
#  I at some point realized "oh this could be like, insanely useful as a portable mach-o introspection lib",
#  and having to write and use it on a Windows on Arm laptop (when NOTHING worked and all I had was a half-functional
#  python w/ no pip) solidified that. That constraint may inform other decisions made in this library.
#
#  A *lot* of code in specifically this file is a holdover from that crappy original script. It was written before I
#  had any professional development experience and it shows. Eventually I will gut and rewrite it, but if you need
#  therapeutic code to go view after digging through this, the new swift stuff is not bad.
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary
from collections import namedtuple as quay_namedtuple
from enum import Enum as quay_Enum
from typing import List as quay_List, Dict as quay_Dict, Optional as quay_Optional
from imagequay_layout.record_contract import quay_Constructable as quay_Constructable
from imagequay.metadata_reader import quay_Image as quay_Image
from imagequay.failure_types import quay_VMAddressingError as quay_VMAddressingError
from imagequay.objc_records import *
from imagequay.formatting import quay_ignore as quay_ignore, quay_usi32_to_si32 as quay_usi32_to_si32, quay_opts as quay_opts, quay_Queue as quay_Queue, quay_QueueItem as quay_QueueItem
from imagequay_support.diagnostics import quay_log as quay_log
quay_type_encodings = {'c': 'char', 'i': 'int', 's': 'short', 'l': 'long', 'q': 'NSInteger', 'C': 'unsigned char', 'I': 'unsigned int', 'S': 'unsigned short', 'L': 'unsigned long', 'A': 'uint8_t', 'Q': 'NSUInteger', 'f': 'float', 'd': 'CGFloat', 'b': 'BOOL', '@': 'id', 'B': 'BOOL', 'v': 'void', '*': 'char *', '#': 'Class', ':': 'SEL', '?': 'unk', 'T': 'unk'}
quay_RELATIVE_METHODS_SELECTORS_ARE_DIRECT_FLAG = 1073741824
quay_RELATIVE_METHOD_FLAG = 2147483648
quay_METHOD_LIST_FLAGS_MASK = 4294901760

@_name_boundary.class_contract('ObjCImage', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'serialize': 'quay_serialize', 'vm_check': 'quay_vm_check', 'read_uint': 'quay_read_uint', 'read_ptr': 'quay_read_ptr', 'read_struct': 'quay_read_struct', 'read_fixed_len_str': 'quay_read_fixed_len_str', 'read_cstr': 'quay_read_cstr', 'image': 'quay_image', 'tp': 'quay_tp', 'classlist': 'quay_classlist', 'catlist': 'quay_catlist', 'protolist': 'quay_protolist', 'class_map': 'quay_class_map', 'cat_map': 'quay_cat_map', 'prot_map': 'quay_prot_map', 'name': 'quay_name'})
class quay_ObjCImage(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_23576bb', 'image': 'quay_image_1beae75'}, 'from_image')
    def quay_from_image(quay_cls_23576bb, quay_image_1beae75: quay_Image):
        quay_objc_image_2efbb2a = quay_ObjCImage(quay_image_1beae75)
        quay_cat_prot_queue_7f42c5d = quay_Queue()
        quay_class_queue_5b00357 = quay_Queue()
        _name_boundary.attributes(quay_cat_prot_queue_7f42c5d)['multithread'] = False
        _name_boundary.attributes(quay_class_queue_5b00357)['multithread'] = False
        quay_sect_128c3fe = None
        for quay_seg_cfc70cc in _name_boundary.attributes(quay_image_1beae75)['segments']:
            for quay_sec_6189292 in _name_boundary.attributes(_name_boundary.attributes(quay_image_1beae75)['segments'][quay_seg_cfc70cc])['sections']:
                if quay_sec_6189292 == '__objc_catlist':
                    quay_sect_128c3fe = _name_boundary.attributes(_name_boundary.attributes(quay_image_1beae75)['segments'][quay_seg_cfc70cc])['sections'][quay_sec_6189292]
        if quay_sect_128c3fe is not None:
            quay_count_babeefa = _name_boundary.attributes(quay_sect_128c3fe)['size'] // _name_boundary.attributes(quay_image_1beae75)['ptr_size']
            for quay_offset_ac01ea7 in range(0, quay_count_babeefa):
                try:
                    quay_item_0b5b2ed = quay_QueueItem()
                    _name_boundary.attributes(quay_item_0b5b2ed)['func'] = _name_boundary.attributes(quay_Category)['from_image']
                    _name_boundary.attributes(quay_item_0b5b2ed)['args'] = [quay_objc_image_2efbb2a, _name_boundary.attributes(quay_sect_128c3fe)['vm_address'] + quay_offset_ac01ea7 * _name_boundary.attributes(quay_image_1beae75)['ptr_size']]
                    _name_boundary.attributes(quay_cat_prot_queue_7f42c5d)['items'].append(quay_item_0b5b2ed)
                except Exception as quay_ex_0e511a1:
                    if not _name_boundary.attributes(quay_ignore)['OBJC_ERRORS']:
                        raise quay_ex_0e511a1
                    _name_boundary.attributes(quay_log)['error'](f'Failed to load a category! Ex: {str(quay_ex_0e511a1)}')
        quay_sect_128c3fe = None
        for quay_seg_cfc70cc in _name_boundary.attributes(quay_image_1beae75)['segments']:
            for quay_sec_6189292 in _name_boundary.attributes(_name_boundary.attributes(quay_image_1beae75)['segments'][quay_seg_cfc70cc])['sections']:
                if quay_sec_6189292 == '__objc_classlist':
                    quay_sect_128c3fe = _name_boundary.attributes(_name_boundary.attributes(quay_image_1beae75)['segments'][quay_seg_cfc70cc])['sections'][quay_sec_6189292]
        if quay_sect_128c3fe is not None:
            quay_cnt_7b7b1b0 = _name_boundary.attributes(quay_sect_128c3fe)['size'] // _name_boundary.attributes(quay_image_1beae75)['ptr_size']
            for quay_i_bc2442b in range(0, quay_cnt_7b7b1b0):
                try:
                    quay_item_0b5b2ed = quay_QueueItem()
                    _name_boundary.attributes(quay_item_0b5b2ed)['func'] = _name_boundary.attributes(quay_Class)['from_image']
                    _name_boundary.attributes(quay_item_0b5b2ed)['args'] = [quay_objc_image_2efbb2a, _name_boundary.attributes(quay_sect_128c3fe)['vm_address'] + quay_i_bc2442b * _name_boundary.attributes(quay_image_1beae75)['ptr_size']]
                    _name_boundary.attributes(quay_class_queue_5b00357)['items'].append(quay_item_0b5b2ed)
                except Exception as quay_ex_0e511a1:
                    if not _name_boundary.attributes(quay_ignore)['OBJC_ERRORS']:
                        raise quay_ex_0e511a1
                    _name_boundary.attributes(quay_log)['error'](f'Failed to load a class! Ex: {str(quay_ex_0e511a1)}')
        quay_sect_128c3fe = None
        for quay_seg_cfc70cc in _name_boundary.attributes(quay_image_1beae75)['segments']:
            for quay_sec_6189292 in _name_boundary.attributes(_name_boundary.attributes(quay_image_1beae75)['segments'][quay_seg_cfc70cc])['sections']:
                if quay_sec_6189292 == '__objc_protolist':
                    quay_sect_128c3fe = _name_boundary.attributes(_name_boundary.attributes(quay_image_1beae75)['segments'][quay_seg_cfc70cc])['sections'][quay_sec_6189292]
        if quay_sect_128c3fe is not None:
            quay_cnt_7b7b1b0 = _name_boundary.attributes(quay_sect_128c3fe)['size'] // _name_boundary.attributes(quay_image_1beae75)['ptr_size']
            for quay_i_bc2442b in range(0, quay_cnt_7b7b1b0):
                quay_ptr_f417a7c = _name_boundary.attributes(quay_sect_128c3fe)['vm_address'] + quay_i_bc2442b * _name_boundary.attributes(quay_image_1beae75)['ptr_size']
                if _name_boundary.attributes(quay_objc_image_2efbb2a)['vm_check'](quay_ptr_f417a7c):
                    quay_loc_258c5d2 = _name_boundary.attributes(quay_image_1beae75)['read_ptr'](quay_ptr_f417a7c)
                    try:
                        quay_proto_d3cd33b = _name_boundary.attributes(quay_image_1beae75)['read_struct'](quay_loc_258c5d2, quay_objc2_prot, vm=True)
                        quay_item_0b5b2ed = quay_QueueItem()
                        _name_boundary.attributes(quay_item_0b5b2ed)['func'] = _name_boundary.attributes(quay_Protocol)['from_image']
                        _name_boundary.attributes(quay_item_0b5b2ed)['args'] = [quay_objc_image_2efbb2a, quay_proto_d3cd33b, quay_loc_258c5d2]
                        _name_boundary.attributes(quay_cat_prot_queue_7f42c5d)['items'].append(quay_item_0b5b2ed)
                    except Exception as quay_ex_0e511a1:
                        if not _name_boundary.attributes(quay_ignore)['OBJC_ERRORS']:
                            raise quay_ex_0e511a1
                        _name_boundary.attributes(quay_log)['error']('Failed to load a protocol with ' + str(quay_ex_0e511a1))
        _name_boundary.attributes(quay_cat_prot_queue_7f42c5d)['go']()
        for quay_val_ed7f70d in _name_boundary.attributes(quay_cat_prot_queue_7f42c5d)['returns']:
            if quay_val_ed7f70d:
                if isinstance(quay_val_ed7f70d, quay_Protocol):
                    _name_boundary.attributes(quay_objc_image_2efbb2a)['protolist'].append(quay_val_ed7f70d)
                    _name_boundary.attributes(quay_objc_image_2efbb2a)['prot_map'][_name_boundary.attributes(quay_val_ed7f70d)['loc']] = quay_val_ed7f70d
                else:
                    _name_boundary.attributes(quay_objc_image_2efbb2a)['catlist'].append(quay_val_ed7f70d)
                    _name_boundary.attributes(quay_objc_image_2efbb2a)['cat_map'][_name_boundary.attributes(quay_val_ed7f70d)['loc']] = quay_val_ed7f70d
        _name_boundary.attributes(quay_class_queue_5b00357)['go']()
        for quay_val_ed7f70d in _name_boundary.attributes(quay_class_queue_5b00357)['returns']:
            if quay_val_ed7f70d:
                _name_boundary.attributes(quay_objc_image_2efbb2a)['classlist'].append(quay_val_ed7f70d)
                _name_boundary.attributes(quay_objc_image_2efbb2a)['class_map'][_name_boundary.attributes(quay_val_ed7f70d)['loc']] = quay_val_ed7f70d
        return quay_objc_image_2efbb2a

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_cf08d2e', 'image': 'quay_image_c8b2f51', 'name': 'quay_name_278600c', 'classlist': 'quay_classlist_5240a27', 'catlist': 'quay_catlist_823e540', 'protolist': 'quay_protolist_1c90f24', 'type_processor': 'quay_type_processor_edd990f'}, 'from_values')
    def quay_from_values(quay_cls_cf08d2e, quay_image_c8b2f51, quay_name_278600c, quay_classlist_5240a27, quay_catlist_823e540, quay_protolist_1c90f24, quay_type_processor_edd990f=None):
        quay_objc_image_e94cde8 = quay_cls_cf08d2e(quay_image_c8b2f51, quay_type_processor_edd990f)
        _name_boundary.attributes(quay_objc_image_e94cde8)['name'] = quay_name_278600c
        _name_boundary.attributes(quay_objc_image_e94cde8)['classlist'] = quay_classlist_5240a27
        _name_boundary.attributes(quay_objc_image_e94cde8)['catlist'] = quay_catlist_823e540
        _name_boundary.attributes(quay_objc_image_e94cde8)['protolist'] = quay_protolist_1c90f24
        return quay_objc_image_e94cde8

    @_name_boundary.callable_contract({'self': 'quay_self_56ec062'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_56ec062):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_b0dd3a5', 'image': 'quay_image_11e8200', 'type_processor': 'quay_type_processor_69bf291'}, '__init__')
    def __init__(quay_self_b0dd3a5, quay_image_11e8200, quay_type_processor_69bf291=None):
        if quay_type_processor_69bf291 is None:
            quay_type_processor_69bf291 = quay_TypeProcessor()
        _name_boundary.attributes(quay_self_b0dd3a5)['image'] = quay_image_11e8200
        if quay_image_11e8200:
            _name_boundary.attributes(quay_self_b0dd3a5)['name'] = _name_boundary.attributes(quay_image_11e8200)['base_name']
        else:
            _name_boundary.attributes(quay_self_b0dd3a5)['name'] = ''
        _name_boundary.attributes(quay_self_b0dd3a5)['tp'] = quay_type_processor_69bf291
        _name_boundary.attributes(quay_self_b0dd3a5)['classlist'] = []
        _name_boundary.attributes(quay_self_b0dd3a5)['catlist'] = []
        _name_boundary.attributes(quay_self_b0dd3a5)['protolist'] = []
        _name_boundary.attributes(quay_self_b0dd3a5)['class_map']: quay_Dict[int, 'Class'] = {}
        _name_boundary.attributes(quay_self_b0dd3a5)['cat_map']: quay_Dict[int, 'Category'] = {}
        _name_boundary.attributes(quay_self_b0dd3a5)['prot_map']: quay_Dict[int, 'Protocol'] = {}

    @_name_boundary.callable_contract({'self': 'quay_self_d815cc5'}, 'serialize')
    def quay_serialize(quay_self_d815cc5):
        return {'classes': [_name_boundary.attributes(quay_cls_0bf0035)['serialize']() for quay_cls_0bf0035 in _name_boundary.attributes(quay_self_d815cc5)['classlist']], 'categories': [_name_boundary.attributes(quay_cat_1444e34)['serialize']() for quay_cat_1444e34 in _name_boundary.attributes(quay_self_d815cc5)['catlist']], 'protocols': [_name_boundary.attributes(quay_prot_4512f82)['serialize']() for quay_prot_4512f82 in _name_boundary.attributes(quay_self_d815cc5)['protolist']]}

    @_name_boundary.callable_contract({'self': 'quay_self_03264f0', 'address': 'quay_address_353feae'}, 'vm_check')
    def quay_vm_check(quay_self_03264f0, quay_address_353feae):
        return _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_03264f0)['image'])['vm'])['vm_check'](quay_address_353feae)

    @_name_boundary.callable_contract({'self': 'quay_self_7ac7aed', 'offset': 'quay_offset_1bd3d29', 'length': 'quay_length_a440906', 'vm': 'quay_vm_0541c7a'}, 'read_uint')
    def quay_read_uint(quay_self_7ac7aed, quay_offset_1bd3d29: int, quay_length_a440906: int, quay_vm_0541c7a=False):
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_7ac7aed)['image'])['read_uint'](quay_offset_1bd3d29, quay_length_a440906, quay_vm_0541c7a)

    @_name_boundary.callable_contract({'self': 'quay_self_417dad0', 'offset': 'quay_offset_78e77f1', 'vm': 'quay_vm_424dc2b'}, 'read_ptr')
    def quay_read_ptr(quay_self_417dad0, quay_offset_78e77f1: int, quay_vm_424dc2b=False):
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_417dad0)['image'])['read_ptr'](quay_offset_78e77f1, quay_vm_424dc2b)

    @_name_boundary.callable_contract({'self': 'quay_self_685c019', 'addr': 'quay_addr_87c0a88', 'struct_type': 'quay_struct_type_784f431', 'vm': 'quay_vm_868f8fa', 'endian': 'quay_endian_8bca5ef'}, 'read_struct')
    def quay_read_struct(quay_self_685c019, quay_addr_87c0a88: int, quay_struct_type_784f431, quay_vm_868f8fa=True, quay_endian_8bca5ef='little'):
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_685c019)['image'])['read_struct'](quay_addr_87c0a88, quay_struct_type_784f431, quay_vm_868f8fa, quay_endian_8bca5ef)

    @_name_boundary.callable_contract({'self': 'quay_self_b9a5c86', 'addr': 'quay_addr_dde9b22', 'count': 'quay_count_e5f5b25', 'vm': 'quay_vm_5401011'}, 'read_fixed_len_str')
    def quay_read_fixed_len_str(quay_self_b9a5c86, quay_addr_dde9b22: int, quay_count_e5f5b25: int, quay_vm_5401011=True):
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_b9a5c86)['image'])['read_fixed_len_str'](quay_addr_dde9b22, quay_count_e5f5b25, quay_vm_5401011)

    @_name_boundary.callable_contract({'self': 'quay_self_13d9fcf', 'addr': 'quay_addr_3c8bc2c', 'limit': 'quay_limit_f42e7b1', 'vm': 'quay_vm_464c8b7'}, 'read_cstr')
    def quay_read_cstr(quay_self_13d9fcf, quay_addr_3c8bc2c: int, quay_limit_f42e7b1: int=0, quay_vm_464c8b7=True):
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_13d9fcf)['image'])['read_cstr'](quay_addr_3c8bc2c, quay_limit_f42e7b1, quay_vm_464c8b7)

@_name_boundary.class_contract('Struct_Representation', {'name': 'quay_name', 'field_names': 'quay_field_names', 'fields': 'quay_fields'})
class quay_Struct_Representation:

    @_name_boundary.callable_contract({'self': 'quay_self_7f9c260', 'processor': 'quay_processor_0bbe641', 'type_str': 'quay_type_str_f2ac25c'}, '__init__')
    def __init__(quay_self_7f9c260, quay_processor_0bbe641: 'TypeProcessor', quay_type_str_f2ac25c: str):
        _name_boundary.attributes(quay_self_7f9c260)['name']: str = quay_type_str_f2ac25c[1:-1].split('=')[0]
        if '=' not in quay_type_str_f2ac25c:
            _name_boundary.attributes(quay_self_7f9c260)['fields'] = []
            return
        _name_boundary.attributes(quay_self_7f9c260)['field_names'] = []
        quay_process_string_3373fe3 = quay_type_str_f2ac25c[1:-1].split('=', 1)[1]
        if quay_process_string_3373fe3.startswith('"'):
            quay_output_string_63a6ebf = ''
            quay_in_field_566424a = False
            quay_in_substruct_depth_fdf7921 = 0
            quay_field_573b8c6 = ''
            for quay_character_92a2366 in quay_process_string_3373fe3:
                if quay_character_92a2366 == '{':
                    quay_in_substruct_depth_fdf7921 += 1
                    quay_output_string_63a6ebf += quay_character_92a2366
                    continue
                elif quay_character_92a2366 == '}':
                    quay_in_substruct_depth_fdf7921 -= 1
                    quay_output_string_63a6ebf += quay_character_92a2366
                    continue
                if quay_in_substruct_depth_fdf7921 == 0:
                    if quay_character_92a2366 == '"':
                        if quay_in_field_566424a:
                            _name_boundary.attributes(quay_self_7f9c260)['field_names'].append(quay_field_573b8c6)
                            quay_in_field_566424a = False
                            quay_field_573b8c6 = ''
                        else:
                            quay_in_field_566424a = True
                    elif quay_in_field_566424a:
                        quay_field_573b8c6 += quay_character_92a2366
                    else:
                        quay_output_string_63a6ebf += quay_character_92a2366
                else:
                    quay_output_string_63a6ebf += quay_character_92a2366
            quay_process_string_3373fe3 = quay_output_string_63a6ebf
        _name_boundary.attributes(quay_self_7f9c260)['fields'] = _name_boundary.attributes(quay_processor_0bbe641)['process'](quay_process_string_3373fe3)

    @_name_boundary.callable_contract({'self': 'quay_self_94517c0'}, '__str__')
    def __str__(quay_self_94517c0):
        quay_ret_0a73752 = 'typedef struct ' + _name_boundary.attributes(quay_self_94517c0)['name'] + ' {\n'
        if not _name_boundary.attributes(quay_self_94517c0)['fields']:
            quay_ret_0a73752 += '} // Error Processing Struct Fields'
            return quay_ret_0a73752
        for quay_i_4f5f2ba, quay_field_aaacac0 in enumerate(_name_boundary.attributes(quay_self_94517c0)['fields']):
            quay_field_name_d64292b = f'field{str(quay_i_4f5f2ba)}'
            if len(_name_boundary.attributes(quay_self_94517c0)['field_names']) > 0:
                try:
                    quay_field_name_d64292b = _name_boundary.attributes(quay_self_94517c0)['field_names'][quay_i_4f5f2ba]
                except IndexError:
                    _name_boundary.attributes(quay_log)['debug'](f"Missing a field in struct {_name_boundary.attributes(quay_self_94517c0)['name']}")
            if isinstance(_name_boundary.attributes(quay_field_aaacac0)['value'], quay_Struct_Representation):
                quay_field_aaacac0 = _name_boundary.attributes(_name_boundary.attributes(quay_field_aaacac0)['value'])['name']
            else:
                quay_field_aaacac0 = _name_boundary.attributes(quay_field_aaacac0)['value']
            quay_ret_0a73752 += '    ' + quay_field_aaacac0 + ' ' + quay_field_name_d64292b + ';\n'
        quay_ret_0a73752 += '} ' + _name_boundary.attributes(quay_self_94517c0)['name'] + ';'
        if len(_name_boundary.attributes(quay_self_94517c0)['fields']) == 0:
            quay_ret_0a73752 += ' // Error Processing Struct Fields'
        return quay_ret_0a73752

@_name_boundary.class_contract('EncodingType', {})
class quay_EncodingType(quay_Enum):
    METHOD = 0
    PROPERTY = 1
    IVAR = 2

@_name_boundary.class_contract('EncodedType', {})
class quay_EncodedType(quay_Enum):
    STRUCT = 0
    NAMED = 1
    ID = 2
    NORMAL = 3

@_name_boundary.class_contract('Type', {'child': 'quay_child', 'pointer_count': 'quay_pointer_count', 'type': 'quay_type', 'value': 'quay_value'})
class quay_Type:

    @_name_boundary.callable_contract({'self': 'quay_self_94a25a0', 'processor': 'quay_processor_839cd1c', 'type_string': 'quay_type_string_1f80116', 'pc': 'quay_pc_cb4f0ff'}, '__init__')
    def __init__(quay_self_94a25a0, quay_processor_839cd1c, quay_type_string_1f80116, quay_pc_cb4f0ff=0):
        quay_start_9681eac = quay_type_string_1f80116[0]
        _name_boundary.attributes(quay_self_94a25a0)['child'] = None
        _name_boundary.attributes(quay_self_94a25a0)['pointer_count'] = quay_pc_cb4f0ff
        if quay_start_9681eac in quay_type_encodings.keys():
            _name_boundary.attributes(quay_self_94a25a0)['type'] = quay_EncodedType.NORMAL
            _name_boundary.attributes(quay_self_94a25a0)['value'] = quay_type_encodings[quay_start_9681eac]
            return
        elif quay_start_9681eac == '"':
            _name_boundary.attributes(quay_self_94a25a0)['type'] = quay_EncodedType.NAMED
            _name_boundary.attributes(quay_self_94a25a0)['value'] = quay_type_string_1f80116[1:-1]
            return
        elif quay_start_9681eac == '{':
            _name_boundary.attributes(quay_self_94a25a0)['type'] = quay_EncodedType.STRUCT
            _name_boundary.attributes(quay_self_94a25a0)['value'] = quay_Struct_Representation(quay_processor_839cd1c, quay_type_string_1f80116)
            return
        raise ValueError(f'Struct with type {quay_start_9681eac} not found')

    @_name_boundary.callable_contract({'self': 'quay_self_fc27cff'}, '__str__')
    def __str__(quay_self_fc27cff):
        quay_pref_e94bfec = ''
        for quay_i_a4e76e5 in range(0, _name_boundary.attributes(quay_self_fc27cff)['pointer_count']):
            quay_pref_e94bfec += '*'
        return quay_pref_e94bfec + str(_name_boundary.attributes(quay_self_fc27cff)['value'])

@_name_boundary.class_contract('TypeProcessor', {'save_struct': 'quay_save_struct', 'process': 'quay_process', 'tokenize': 'quay_tokenize', 'structs': 'quay_structs', 'type_cache': 'quay_type_cache'})
class quay_TypeProcessor:

    @_name_boundary.callable_contract({'self': 'quay_self_7e005ff'}, '__init__')
    def __init__(quay_self_7e005ff):
        _name_boundary.attributes(quay_self_7e005ff)['structs'] = {}
        _name_boundary.attributes(quay_self_7e005ff)['type_cache'] = {}

    @_name_boundary.callable_contract({'self': 'quay_self_5e1d904', 'struct_to_save': 'quay_struct_to_save_ac06f3d'}, 'save_struct')
    def quay_save_struct(quay_self_5e1d904, quay_struct_to_save_ac06f3d: quay_Struct_Representation):
        if _name_boundary.attributes(quay_struct_to_save_ac06f3d)['name'] not in _name_boundary.attributes(quay_self_5e1d904)['structs'].keys():
            _name_boundary.attributes(quay_self_5e1d904)['structs'][_name_boundary.attributes(quay_struct_to_save_ac06f3d)['name']] = quay_struct_to_save_ac06f3d
        else:
            if len(_name_boundary.attributes(_name_boundary.attributes(quay_self_5e1d904)['structs'][_name_boundary.attributes(quay_struct_to_save_ac06f3d)['name']])['fields']) == 0:
                _name_boundary.attributes(quay_self_5e1d904)['structs'][_name_boundary.attributes(quay_struct_to_save_ac06f3d)['name']] = quay_struct_to_save_ac06f3d
            if len(_name_boundary.attributes(quay_struct_to_save_ac06f3d)['field_names']) > 0 and len(_name_boundary.attributes(_name_boundary.attributes(quay_self_5e1d904)['structs'][_name_boundary.attributes(quay_struct_to_save_ac06f3d)['name']])['field_names']) == 0:
                _name_boundary.attributes(quay_self_5e1d904)['structs'][_name_boundary.attributes(quay_struct_to_save_ac06f3d)['name']] = quay_struct_to_save_ac06f3d

    @_name_boundary.callable_contract({'self': 'quay_self_c6906b1', 'type_to_process': 'quay_type_to_process_4504f37'}, 'process')
    def quay_process(quay_self_c6906b1, quay_type_to_process_4504f37: str):
        if quay_type_to_process_4504f37 in _name_boundary.attributes(quay_self_c6906b1)['type_cache']:
            return _name_boundary.attributes(quay_self_c6906b1)['type_cache'][quay_type_to_process_4504f37]
        try:
            quay_tokens_84f1772 = _name_boundary.attributes(quay_self_c6906b1)['tokenize'](quay_type_to_process_4504f37)
            quay_types_3b0f1d7 = []
            quay_pc_1c52186 = 0
            for quay_i_f6dd7dc, quay_token_f97f11b in enumerate(quay_tokens_84f1772):
                if quay_token_f97f11b == '^':
                    quay_pc_1c52186 += 1
                else:
                    quay_typee_70ac242 = quay_Type(quay_self_c6906b1, quay_token_f97f11b, quay_pc_1c52186)
                    quay_types_3b0f1d7.append(quay_typee_70ac242)
                    if _name_boundary.attributes(quay_typee_70ac242)['type'] == quay_EncodedType.STRUCT:
                        _name_boundary.attributes(quay_self_c6906b1)['save_struct'](_name_boundary.attributes(quay_typee_70ac242)['value'])
                    quay_pc_1c52186 = 0
            _name_boundary.attributes(quay_self_c6906b1)['type_cache'][quay_type_to_process_4504f37] = quay_types_3b0f1d7
            return quay_types_3b0f1d7
        except Exception:
            pass

    @staticmethod
    @_name_boundary.callable_contract({'type_to_tokenize': 'quay_type_to_tokenize_e6c408d'}, 'tokenize')
    def quay_tokenize(quay_type_to_tokenize_e6c408d: str):
        quay_tokens_3b6f730 = []
        quay_parsing_brackets_f365836 = False
        quay_bracket_count_0dd9ee0 = 0
        quay_buffer_c24ffc4 = ''
        for quay_c_a83b4bd in quay_type_to_tokenize_e6c408d:
            if quay_parsing_brackets_f365836:
                quay_buffer_c24ffc4 += quay_c_a83b4bd
                if quay_c_a83b4bd == '{':
                    quay_bracket_count_0dd9ee0 += 1
                elif quay_c_a83b4bd == '}':
                    quay_bracket_count_0dd9ee0 -= 1
                    if quay_bracket_count_0dd9ee0 == 0:
                        quay_tokens_3b6f730.append(quay_buffer_c24ffc4)
                        quay_parsing_brackets_f365836 = False
                        quay_buffer_c24ffc4 = ''
            elif quay_c_a83b4bd in quay_type_encodings or quay_c_a83b4bd == '^':
                quay_tokens_3b6f730.append(quay_c_a83b4bd)
            elif quay_c_a83b4bd == '{':
                quay_buffer_c24ffc4 += '{'
                quay_parsing_brackets_f365836 = True
                quay_bracket_count_0dd9ee0 += 1
            elif quay_c_a83b4bd == '"':
                try:
                    quay_tokens_3b6f730 = [quay_type_to_tokenize_e6c408d.split('@', 1)[1]]
                except Exception as quay_ex_3fefc18:
                    _name_boundary.attributes(quay_log)['warning'](f'Failed to process type {quay_type_to_tokenize_e6c408d} with {quay_ex_3fefc18}')
                    return []
                break
        return quay_tokens_3b6f730

@_name_boundary.class_contract('Ivar', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'serialize': 'quay_serialize', '_renderable_type': 'quay__renderable_type', 'name': 'quay_name', 'typestr': 'quay_typestr', 'is_id': 'quay_is_id', 'offset': 'quay_offset', 'type': 'quay_type'})
class quay_Ivar(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_09ecdf1', 'objc_image': 'quay_objc_image_faa90f2', 'ivar': 'quay_ivar_b2f9d40'}, 'from_image')
    def quay_from_image(quay_cls_09ecdf1, quay_objc_image_faa90f2: quay_ObjCImage, quay_ivar_b2f9d40: quay_objc2_ivar):
        quay_name_950a0ca: str = _name_boundary.attributes(quay_objc_image_faa90f2)['read_cstr'](_name_boundary.attributes(quay_ivar_b2f9d40)['name'], 0, vm=True)
        quay_type_string_ab6a489: str = _name_boundary.attributes(quay_objc_image_faa90f2)['read_cstr'](_name_boundary.attributes(quay_ivar_b2f9d40)['type'], 0, vm=True)
        quay_offset_e6bff2c = _name_boundary.attributes(quay_ivar_b2f9d40)['offs']
        return quay_cls_09ecdf1(quay_name_950a0ca, quay_type_string_ab6a489, _name_boundary.attributes(quay_objc_image_faa90f2)['tp'], offset=quay_offset_e6bff2c)

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_fa07c48', 'name': 'quay_name_d2fe42e', 'type_encoding': 'quay_type_encoding_19f93c5', 'type_processor': 'quay_type_processor_5d69c47', 'offset': 'quay_offset_a5eeac1'}, 'from_values')
    def quay_from_values(quay_cls_fa07c48, quay_name_d2fe42e, quay_type_encoding_19f93c5, quay_type_processor_5d69c47=None, quay_offset_a5eeac1=0):
        if not quay_type_processor_5d69c47:
            quay_type_processor_5d69c47 = quay_TypeProcessor()
        return quay_cls_fa07c48(quay_name_d2fe42e, quay_type_encoding_19f93c5, quay_type_processor_5d69c47, offset=quay_offset_a5eeac1)

    @_name_boundary.callable_contract({'self': 'quay_self_e0bbc48'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_e0bbc48):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_a1033cd', 'name': 'quay_name_a56911a', 'type_encoding': 'quay_type_encoding_8e4d71f', 'type_processor': 'quay_type_processor_2a68351', 'offset': 'quay_offset_eec56f6'}, '__init__')
    def __init__(quay_self_a1033cd, quay_name_a56911a, quay_type_encoding_8e4d71f, quay_type_processor_2a68351, quay_offset_eec56f6=0):
        _name_boundary.attributes(quay_self_a1033cd)['name']: str = quay_name_a56911a
        quay_type_string_c4fac6a: str = quay_type_encoding_8e4d71f
        _name_boundary.attributes(quay_self_a1033cd)['typestr'] = quay_type_string_c4fac6a
        if len(quay_type_string_c4fac6a) == 0:
            _name_boundary.attributes(quay_self_a1033cd)['is_id'] = False
            _name_boundary.attributes(quay_self_a1033cd)['type'] = '?'
            return
        _name_boundary.attributes(quay_self_a1033cd)['is_id']: bool = quay_type_string_c4fac6a[0] == '@'
        try:
            _name_boundary.attributes(quay_self_a1033cd)['type']: str = _name_boundary.attributes(quay_self_a1033cd)['_renderable_type'](_name_boundary.attributes(quay_type_processor_2a68351)['process'](quay_type_string_c4fac6a)[0])
        except IndexError:
            _name_boundary.attributes(quay_self_a1033cd)['type']: str = '?'
        except TypeError:
            _name_boundary.attributes(quay_self_a1033cd)['type']: str = '?'
        _name_boundary.attributes(quay_self_a1033cd)['offset'] = quay_offset_eec56f6

    @_name_boundary.callable_contract({'self': 'quay_self_d7a247d'}, 'serialize')
    def quay_serialize(quay_self_d7a247d):
        return {'name': _name_boundary.attributes(quay_self_d7a247d)['name'], 'type': _name_boundary.attributes(quay_self_d7a247d)['type'], 'type_is_id': _name_boundary.attributes(quay_self_d7a247d)['type'], 'typestring': _name_boundary.attributes(quay_self_d7a247d)['typestr'], 'rendered': str(quay_self_d7a247d)}

    @_name_boundary.callable_contract({'self': 'quay_self_6e000b7'}, '__str__')
    def __str__(quay_self_6e000b7):
        quay_ret_de008f5 = ''
        if _name_boundary.attributes(quay_self_6e000b7)['type'].startswith('<'):
            quay_ret_de008f5 += 'id'
        quay_ret_de008f5 += _name_boundary.attributes(quay_self_6e000b7)['type'] + ' '
        if _name_boundary.attributes(quay_self_6e000b7)['is_id']:
            quay_ret_de008f5 += '*'
        quay_ret_de008f5 += _name_boundary.attributes(quay_self_6e000b7)['name']
        return quay_ret_de008f5

    @staticmethod
    @_name_boundary.callable_contract({'ivar_type': 'quay_ivar_type_cba1a8a'}, '_renderable_type')
    def quay__renderable_type(quay_ivar_type_cba1a8a: quay_Type) -> str:
        if _name_boundary.attributes(quay_ivar_type_cba1a8a)['type'] == quay_EncodedType.NORMAL:
            return str(quay_ivar_type_cba1a8a)
        elif _name_boundary.attributes(quay_ivar_type_cba1a8a)['type'] == quay_EncodedType.STRUCT:
            quay_ptr_addition_7a01423 = ''
            for quay_i_2a42173 in range(0, _name_boundary.attributes(quay_ivar_type_cba1a8a)['pointer_count']):
                quay_ptr_addition_7a01423 += '*'
            return quay_ptr_addition_7a01423 + _name_boundary.attributes(_name_boundary.attributes(quay_ivar_type_cba1a8a)['value'])['name']
        return str(quay_ivar_type_cba1a8a)

@_name_boundary.class_contract('MethodList', {'CUSTOM_RMS_BASE': 'quay_CUSTOM_RMS_BASE', '_process_methlist': 'quay__process_methlist', 'objc_image': 'quay_objc_image', 'methlist_head': 'quay_methlist_head', 'meta': 'quay_meta', 'name': 'quay_name', 'load_errors': 'quay_load_errors', 'methods': 'quay_methods', 'struct_list': 'quay_struct_list'})
class quay_MethodList:
    quay_CUSTOM_RMS_BASE = None

    @_name_boundary.callable_contract({'self': 'quay_self_107d4e7', 'image': 'quay_image_46a547c', 'methlist_head': 'quay_methlist_head_c1f261b', 'base_meths': 'quay_base_meths_5d6533c', 'class_meta': 'quay_class_meta_ec0c0ae', 'class_name': 'quay_class_name_f9f578b'}, '__init__')
    def __init__(quay_self_107d4e7, quay_image_46a547c: quay_ObjCImage, quay_methlist_head_c1f261b, quay_base_meths_5d6533c, quay_class_meta_ec0c0ae, quay_class_name_f9f578b):
        quay_base_meths_5d6533c = quay_base_meths_5d6533c & 68719476735
        _name_boundary.attributes(quay_log)['info'](f'Opening method list ({str(quay_methlist_head_c1f261b)}) at {hex(quay_base_meths_5d6533c)}')
        _name_boundary.attributes(quay_self_107d4e7)['objc_image'] = quay_image_46a547c
        _name_boundary.attributes(quay_self_107d4e7)['methlist_head'] = quay_methlist_head_c1f261b
        _name_boundary.attributes(quay_self_107d4e7)['meta'] = quay_class_meta_ec0c0ae
        _name_boundary.attributes(quay_self_107d4e7)['name'] = quay_class_name_f9f578b
        _name_boundary.attributes(quay_self_107d4e7)['load_errors'] = []
        _name_boundary.attributes(quay_self_107d4e7)['methods'] = []
        _name_boundary.attributes(quay_self_107d4e7)['struct_list'] = []
        if quay_base_meths_5d6533c != 0:
            _name_boundary.attributes(quay_self_107d4e7)['methods'] = _name_boundary.attributes(quay_self_107d4e7)['_process_methlist'](quay_base_meths_5d6533c)

    @_name_boundary.callable_contract({'self': 'quay_self_325b3e1', 'base_meths': 'quay_base_meths_f9a2484'}, '_process_methlist')
    def quay__process_methlist(quay_self_325b3e1, quay_base_meths_f9a2484):
        quay_methods_68c9400 = []
        quay_ea_3fcfd12 = _name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['methlist_head'])['off']
        quay_vm_ea_c84bd0c = quay_base_meths_f9a2484
        quay_uses_relative_methods_30d13a1 = _name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['methlist_head'])['entrysize'] & quay_METHOD_LIST_FLAGS_MASK & quay_RELATIVE_METHOD_FLAG != 0
        quay_rms_are_direct_5df842a = _name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['methlist_head'])['entrysize'] & quay_METHOD_LIST_FLAGS_MASK & quay_RELATIVE_METHODS_SELECTORS_ARE_DIRECT_FLAG != 0
        quay_ea_3fcfd12 += _name_boundary.attributes(quay_objc2_meth_list)['size'](_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['image'])['ptr_size'])
        quay_vm_ea_c84bd0c += _name_boundary.attributes(quay_objc2_meth_list)['size'](_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['image'])['ptr_size'])
        for quay_i_be57b47 in range(1, _name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['methlist_head'])['count'] + 1):
            if quay_uses_relative_methods_30d13a1:
                quay_sel_e05e6e0 = _name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['read_uint'](quay_ea_3fcfd12, 4, vm=False)
                quay_sel_e05e6e0 = quay_usi32_to_si32(quay_sel_e05e6e0)
                quay_types_f89afc9 = _name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['read_uint'](quay_ea_3fcfd12 + 4, 4, vm=False)
                quay_types_f89afc9 = quay_usi32_to_si32(quay_types_f89afc9)
                quay_imp_4f752fe = _name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['read_uint'](quay_ea_3fcfd12 + 8, 4, vm=False)
                quay_imp_4f752fe = quay_usi32_to_si32(quay_imp_4f752fe)
            else:
                quay_sel_e05e6e0 = _name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['read_ptr'](quay_ea_3fcfd12, vm=False)
                quay_types_f89afc9 = _name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['read_ptr'](quay_ea_3fcfd12 + _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['image'])['ptr_size'], vm=False)
                quay_imp_4f752fe = _name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['read_ptr'](quay_ea_3fcfd12 + _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['image'])['ptr_size'] * 2, vm=False)
            try:
                quay_method_11f3e6c = _name_boundary.attributes(quay_Method)['from_image'](_name_boundary.attributes(quay_self_325b3e1)['objc_image'], quay_sel_e05e6e0, quay_types_f89afc9, quay_imp_4f752fe, _name_boundary.attributes(quay_self_325b3e1)['meta'], quay_vm_ea_c84bd0c, quay_uses_relative_methods_30d13a1, quay_rms_are_direct_5df842a, _name_boundary.attributes(quay_MethodList)['CUSTOM_RMS_BASE'])
                quay_methods_68c9400.append(quay_method_11f3e6c)
                if _name_boundary.attributes(quay_method_11f3e6c)['types']:
                    for quay_method_type_0ef89ad in _name_boundary.attributes(quay_method_11f3e6c)['types']:
                        if _name_boundary.attributes(quay_method_type_0ef89ad)['type'] == quay_EncodedType.STRUCT:
                            _name_boundary.attributes(quay_self_325b3e1)['struct_list'].append(_name_boundary.attributes(quay_method_type_0ef89ad)['value'])
            except quay_VMAddressingError as quay_ex_3519ff1:
                if _name_boundary.attributes(quay_opts)['OBJC_LOAD_ERRORS_SEND_TO_DEBUG']:
                    _name_boundary.attributes(quay_log)['debug'](f"Failed to load a method at {quay_sel_e05e6e0} with {_name_boundary.attributes(quay_ex_3519ff1.__class__)['__name__']}: {str(quay_ex_3519ff1)}")
                else:
                    _name_boundary.attributes(quay_log)['warning'](f"Failed to load a method at {quay_sel_e05e6e0} with {_name_boundary.attributes(quay_ex_3519ff1.__class__)['__name__']}: {str(quay_ex_3519ff1)}")
                _name_boundary.attributes(quay_self_325b3e1)['load_errors'].append(f"Failed to load a method with {_name_boundary.attributes(quay_ex_3519ff1.__class__)['__name__']}: {str(quay_ex_3519ff1)}")
            except Exception as quay_ex_3519ff1:
                if not _name_boundary.attributes(quay_ignore)['OBJC_ERRORS']:
                    raise quay_ex_3519ff1
                if _name_boundary.attributes(quay_opts)['OBJC_LOAD_ERRORS_SEND_TO_DEBUG']:
                    _name_boundary.attributes(quay_log)['debug'](f"Failed to load method in {_name_boundary.attributes(quay_self_325b3e1)['name']} with {str(quay_ex_3519ff1)}")
                else:
                    _name_boundary.attributes(quay_log)['warning'](f"Failed to load method in {_name_boundary.attributes(quay_self_325b3e1)['name']} with {str(quay_ex_3519ff1)}")
                _name_boundary.attributes(quay_self_325b3e1)['load_errors'].append(f'Failed to load a method with {str(quay_ex_3519ff1)}')
            if quay_uses_relative_methods_30d13a1:
                quay_ea_3fcfd12 += _name_boundary.attributes(quay_objc2_meth_list_entry)['size'](_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['image'])['ptr_size'])
                quay_vm_ea_c84bd0c += _name_boundary.attributes(quay_objc2_meth_list_entry)['size'](_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['image'])['ptr_size'])
            else:
                quay_ea_3fcfd12 += _name_boundary.attributes(quay_objc2_meth)['size'](_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['image'])['ptr_size'])
                quay_vm_ea_c84bd0c += _name_boundary.attributes(quay_objc2_meth)['size'](_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_325b3e1)['objc_image'])['image'])['ptr_size'])
        return quay_methods_68c9400

@_name_boundary.class_contract('Method', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'serialize': 'quay_serialize', '_renderable_type': 'quay__renderable_type', '_build_method_signature': 'quay__build_method_signature', 'meta': 'quay_meta', 'sel': 'quay_sel', 'type_string': 'quay_type_string', 'types': 'quay_types', 'imp': 'quay_imp', 'signature': 'quay_signature', 'return_string': 'quay_return_string', 'arguments': 'quay_arguments'})
class quay_Method(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_d917aa2', 'objc_image': 'quay_objc_image_3b605ef', 'sel_addr': 'quay_sel_addr_fe81cb4', 'types_addr': 'quay_types_addr_d5e1aaa', 'imp': 'quay_imp_e1934ec', 'is_meta': 'quay_is_meta_bf93d77', 'vm_addr': 'quay_vm_addr_77aff1c', 'rms': 'quay_rms_a820e71', 'rms_are_direct': 'quay_rms_are_direct_db28ea8', 'rms_base': 'quay_rms_base_bde2b80'}, 'from_image')
    def quay_from_image(quay_cls_d917aa2, quay_objc_image_3b605ef: quay_ObjCImage, quay_sel_addr_fe81cb4, quay_types_addr_d5e1aaa, quay_imp_e1934ec, quay_is_meta_bf93d77, quay_vm_addr_77aff1c, quay_rms_a820e71, quay_rms_are_direct_db28ea8, quay_rms_base_bde2b80=None):
        if quay_rms_a820e71:
            if not quay_rms_base_bde2b80:
                quay_rms_base_bde2b80 = quay_vm_addr_77aff1c
            quay_imp_e1934ec = quay_imp_e1934ec + 8 + quay_rms_base_bde2b80
            if quay_rms_are_direct_db28ea8:
                try:
                    if _name_boundary.attributes(quay_opts)['USE_SYMTAB_INSTEAD_OF_SELECTORS']:
                        raise AssertionError
                    quay_sel_8ea73d9 = _name_boundary.attributes(quay_objc_image_3b605ef)['read_cstr'](quay_sel_addr_fe81cb4 + quay_rms_base_bde2b80, 0, vm=True)
                except Exception as quay_ex_c33c710:
                    try:
                        if quay_imp_e1934ec in _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_3b605ef)['image'])['symbols']:
                            quay_sel_8ea73d9 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_objc_image_3b605ef)['image'])['symbols'][quay_imp_e1934ec])['fullname'].split(' ')[-1][:-1]
                        else:
                            raise quay_ex_c33c710
                    except Exception:
                        raise quay_ex_c33c710
                quay_type_string_9f3dc6f = _name_boundary.attributes(quay_objc_image_3b605ef)['read_cstr'](quay_types_addr_d5e1aaa + quay_vm_addr_77aff1c + 4, 0, vm=True)
            else:
                quay_selector_pointer_8e93058 = _name_boundary.attributes(quay_objc_image_3b605ef)['read_ptr'](quay_sel_addr_fe81cb4 + quay_vm_addr_77aff1c, vm=True)
                try:
                    if _name_boundary.attributes(quay_opts)['USE_SYMTAB_INSTEAD_OF_SELECTORS']:
                        raise AssertionError
                    quay_sel_8ea73d9 = _name_boundary.attributes(quay_objc_image_3b605ef)['read_cstr'](quay_selector_pointer_8e93058, 0, vm=True)
                except Exception as quay_ex_c33c710:
                    try:
                        if quay_imp_e1934ec in _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_3b605ef)['image'])['symbols']:
                            quay_sel_8ea73d9 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_objc_image_3b605ef)['image'])['symbols'][quay_imp_e1934ec])['fullname'].split(' ')[-1][:-1]
                        else:
                            raise quay_ex_c33c710
                    except Exception:
                        raise quay_ex_c33c710
                quay_type_string_9f3dc6f = _name_boundary.attributes(quay_objc_image_3b605ef)['read_cstr'](quay_types_addr_d5e1aaa + quay_vm_addr_77aff1c + 4, 0, vm=True)
        else:
            quay_sel_8ea73d9 = _name_boundary.attributes(quay_objc_image_3b605ef)['read_cstr'](quay_sel_addr_fe81cb4, 0, vm=True)
            quay_type_string_9f3dc6f = _name_boundary.attributes(quay_objc_image_3b605ef)['read_cstr'](quay_types_addr_d5e1aaa, 0, vm=True)
        return quay_cls_d917aa2(quay_is_meta_bf93d77, quay_sel_8ea73d9, quay_type_string_9f3dc6f, _name_boundary.attributes(quay_objc_image_3b605ef)['tp'], quay_imp_e1934ec)

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_a7e241e', 'sel': 'quay_sel_658f7df', 'type_string': 'quay_type_string_8e1b3c7', 'is_meta': 'quay_is_meta_12b1085', 'type_processor': 'quay_type_processor_16e635a', 'imp': 'quay_imp_a0c5f8f'}, 'from_values')
    def quay_from_values(quay_cls_a7e241e, quay_sel_658f7df, quay_type_string_8e1b3c7, quay_is_meta_12b1085=False, quay_type_processor_16e635a=None, quay_imp_a0c5f8f=None):
        if not quay_type_processor_16e635a:
            quay_type_processor_16e635a = quay_TypeProcessor()
        return quay_cls_a7e241e(quay_is_meta_12b1085, quay_sel_658f7df, quay_type_string_8e1b3c7, quay_type_processor_16e635a, quay_imp_a0c5f8f)

    @_name_boundary.callable_contract({'self': 'quay_self_335fe9a'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_335fe9a):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_d0f4847', 'meta': 'quay_meta_cbf2283', 'sel': 'quay_sel_2dde67b', 'type_string': 'quay_type_string_7fb958c', 'type_processor': 'quay_type_processor_8824c7e', 'imp': 'quay_imp_13e3f45'}, '__init__')
    def __init__(quay_self_d0f4847, quay_meta_cbf2283, quay_sel_2dde67b, quay_type_string_7fb958c, quay_type_processor_8824c7e, quay_imp_13e3f45):
        _name_boundary.attributes(quay_self_d0f4847)['meta'] = quay_meta_cbf2283
        _name_boundary.attributes(quay_self_d0f4847)['sel'] = quay_sel_2dde67b
        _name_boundary.attributes(quay_self_d0f4847)['type_string'] = quay_type_string_7fb958c
        _name_boundary.attributes(quay_self_d0f4847)['types'] = _name_boundary.attributes(quay_type_processor_8824c7e)['process'](quay_type_string_7fb958c)
        _name_boundary.attributes(quay_self_d0f4847)['imp'] = quay_imp_13e3f45
        try:
            _name_boundary.attributes(quay_self_d0f4847)['return_string'] = _name_boundary.attributes(quay_self_d0f4847)['_renderable_type'](_name_boundary.attributes(quay_self_d0f4847)['types'][0])
        except TypeError:
            _name_boundary.attributes(quay_self_d0f4847)['return_string'] = '?'
        try:
            _name_boundary.attributes(quay_self_d0f4847)['arguments'] = [_name_boundary.attributes(quay_self_d0f4847)['_renderable_type'](quay_i_0981b8a) for quay_i_0981b8a in _name_boundary.attributes(quay_self_d0f4847)['types'][1:]]
        except TypeError:
            _name_boundary.attributes(quay_self_d0f4847)['arguments'] = ['?' for quay_i_0b108c3 in range(_name_boundary.attributes(_name_boundary.attributes(quay_self_d0f4847)['sel'])['count'](':'))]
        _name_boundary.attributes(quay_self_d0f4847)['signature'] = _name_boundary.attributes(quay_self_d0f4847)['_build_method_signature']()

    @_name_boundary.callable_contract({'self': 'quay_self_f9349cc'}, 'serialize')
    def quay_serialize(quay_self_f9349cc):
        return {'selector': _name_boundary.attributes(quay_self_f9349cc)['sel'], 'arguments': _name_boundary.attributes(quay_self_f9349cc)['arguments'], 'return_type': _name_boundary.attributes(quay_self_f9349cc)['return_string'], 'signature': _name_boundary.attributes(quay_self_f9349cc)['signature'], 'typestring': _name_boundary.attributes(quay_self_f9349cc)['type_string']}

    @_name_boundary.callable_contract({'self': 'quay_self_6751def'}, '__str__')
    def __str__(quay_self_6751def):
        quay_ret_7f0e300 = ''
        quay_ret_7f0e300 += _name_boundary.attributes(quay_self_6751def)['signature']
        return quay_ret_7f0e300

    @staticmethod
    @_name_boundary.callable_contract({'method_type': 'quay_method_type_03e62eb'}, '_renderable_type')
    def quay__renderable_type(quay_method_type_03e62eb: quay_Type):
        if _name_boundary.attributes(quay_method_type_03e62eb)['type'] == quay_EncodedType.NORMAL:
            return str(quay_method_type_03e62eb)
        elif _name_boundary.attributes(quay_method_type_03e62eb)['type'] == quay_EncodedType.STRUCT:
            quay_ptr_addition_7088484 = ''
            for quay_i_9fc3361 in range(0, _name_boundary.attributes(quay_method_type_03e62eb)['pointer_count']):
                quay_ptr_addition_7088484 += '*'
            return 'struct ' + _name_boundary.attributes(_name_boundary.attributes(quay_method_type_03e62eb)['value'])['name'] + ' ' + quay_ptr_addition_7088484

    @_name_boundary.callable_contract({'self': 'quay_self_3d34168'}, '_build_method_signature')
    def quay__build_method_signature(quay_self_3d34168):
        quay_dash_3a089b6 = '+' if _name_boundary.attributes(quay_self_3d34168)['meta'] else '-'
        quay_ret_dea5c53 = '(' + _name_boundary.attributes(quay_self_3d34168)['return_string'] + ')'
        if len(_name_boundary.attributes(quay_self_3d34168)['arguments']) == 0:
            return quay_dash_3a089b6 + quay_ret_dea5c53 + _name_boundary.attributes(quay_self_3d34168)['sel']
        quay_segments_7990d55 = []
        for quay_i_b1ea338, quay_item_bb45675 in enumerate(_name_boundary.attributes(quay_self_3d34168)['sel'].split(':')):
            if quay_item_bb45675 == '':
                continue
            try:
                quay_segments_7990d55.append(quay_item_bb45675 + ':' + '(' + _name_boundary.attributes(quay_self_3d34168)['arguments'][quay_i_b1ea338 + 2] + ')' + 'arg' + str(quay_i_b1ea338) + ' ')
            except IndexError:
                quay_segments_7990d55.append(quay_item_bb45675)
        quay_sig_b572a48 = ''.join(quay_segments_7990d55)
        return quay_dash_3a089b6 + quay_ret_dea5c53 + quay_sig_b572a48

@_name_boundary.class_contract('LinkedClass', {'classname': 'quay_classname', 'libname': 'quay_libname'})
class quay_LinkedClass:

    @_name_boundary.callable_contract({'self': 'quay_self_22e67bf', 'classname': 'quay_classname_bdc5236', 'libname': 'quay_libname_8a9fc32'}, '__init__')
    def __init__(quay_self_22e67bf, quay_classname_bdc5236, quay_libname_8a9fc32):
        _name_boundary.attributes(quay_self_22e67bf)['classname'] = quay_classname_bdc5236
        _name_boundary.attributes(quay_self_22e67bf)['libname'] = quay_libname_8a9fc32

@_name_boundary.class_contract('Class', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'serialize': 'quay_serialize', '_load_linked_libraries': 'quay__load_linked_libraries', 'name': 'quay_name', 'meta': 'quay_meta', 'superclass': 'quay_superclass', 'loc': 'quay_loc', 'load_errors': 'quay_load_errors', 'struct_list': 'quay_struct_list', 'linkedlibs': 'quay_linkedlibs', 'linked_classes': 'quay_linked_classes', 'fdec_classes': 'quay_fdec_classes', 'fdec_prots': 'quay_fdec_prots', 'methods': 'quay_methods', 'properties': 'quay_properties', 'protocols': 'quay_protocols', 'ivars': 'quay_ivars'})
class quay_Class(quay_Constructable):
    """
    """

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_e401853', 'objc_image': 'quay_objc_image_24aab4c', 'class_ptr': 'quay_class_ptr_6df384f', 'meta': 'quay_meta_2d7d4f0', 'class_ptr_is_direct': 'quay_class_ptr_is_direct_aa35a91'}, 'from_image')
    def quay_from_image(quay_cls_e401853, quay_objc_image_24aab4c: quay_ObjCImage, quay_class_ptr_6df384f: int, quay_meta_2d7d4f0=False, quay_class_ptr_is_direct_aa35a91=False) -> quay_Optional['Class']:
        if quay_class_ptr_6df384f in _name_boundary.attributes(quay_objc_image_24aab4c)['class_map']:
            return _name_boundary.attributes(quay_objc_image_24aab4c)['class_map'][quay_class_ptr_6df384f]
        quay_load_errors_da3819d = []
        quay_struct_list_da270bb = []
        if not quay_meta_2d7d4f0:
            _name_boundary.attributes(quay_log)['debug_more'](f'Loading Class From {hex(quay_class_ptr_6df384f)}')
        else:
            _name_boundary.attributes(quay_log)['debug_more'](f'Loading metaclass From {hex(quay_class_ptr_6df384f)}')
        if not quay_class_ptr_is_direct_aa35a91:
            quay_objc2_class_location_41d009b = _name_boundary.attributes(quay_objc_image_24aab4c)['read_ptr'](quay_class_ptr_6df384f, vm=True)
        else:
            quay_objc2_class_location_41d009b = quay_class_ptr_6df384f
        if quay_objc2_class_location_41d009b == 0 or not _name_boundary.attributes(quay_objc_image_24aab4c)['vm_check'](quay_objc2_class_location_41d009b):
            if _name_boundary.attributes(quay_opts)['OBJC_LOAD_ERRORS_SEND_TO_DEBUG']:
                _name_boundary.attributes(quay_log)['debug'](f"Loading a class @ {hex(quay_class_ptr_6df384f)} {(_name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['symbols'][quay_class_ptr_6df384f] if quay_class_ptr_6df384f in _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['symbols'] else '`?`')} failed")
            else:
                _name_boundary.attributes(quay_log)['error'](f"Loading a class @ {hex(quay_class_ptr_6df384f)} {(_name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['symbols'][quay_class_ptr_6df384f] if quay_class_ptr_6df384f in _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['symbols'] else '`?`')} failed")
            _name_boundary.attributes(quay_objc_image_24aab4c)['class_map'][quay_class_ptr_6df384f] = None
            return None
        quay_objc2_class_item_bb8a151: quay_objc2_class = _name_boundary.attributes(quay_objc_image_24aab4c)['read_struct'](quay_objc2_class_location_41d009b, quay_objc2_class, vm=True)
        quay_superclass_f378aee = None
        if not quay_meta_2d7d4f0:
            if quay_objc2_class_location_41d009b + _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['ptr_size'] in _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['import_table']:
                quay_symbol_770fbfa = _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['import_table'][quay_objc2_class_location_41d009b + _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['ptr_size']]
                quay_superclass_name_34e3375 = _name_boundary.attributes(quay_symbol_770fbfa)['name'][1:]
            elif _name_boundary.attributes(quay_objc2_class_item_bb8a151)['superclass'] in _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['export_table']:
                quay_symbol_770fbfa = _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['export_table'][_name_boundary.attributes(quay_objc2_class_item_bb8a151)['superclass']]
                quay_superclass_name_34e3375 = _name_boundary.attributes(quay_symbol_770fbfa)['name'][1:]
            else:
                if _name_boundary.attributes(quay_objc_image_24aab4c)['vm_check'](_name_boundary.attributes(quay_objc2_class_item_bb8a151)['superclass']):
                    try:
                        quay_superclass_f378aee = _name_boundary.attributes(quay_Class)['from_image'](quay_objc_image_24aab4c, quay_objc2_class_location_41d009b + _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['ptr_size'])
                    except Exception:
                        pass
                if quay_superclass_f378aee is not None:
                    quay_superclass_name_34e3375 = _name_boundary.attributes(quay_superclass_f378aee)['name']
                elif _name_boundary.attributes(quay_objc2_class_item_bb8a151)['superclass'] in _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['import_table']:
                    quay_symbol_770fbfa = _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['import_table'][_name_boundary.attributes(quay_objc2_class_item_bb8a151)['superclass']]
                    quay_superclass_name_34e3375 = _name_boundary.attributes(quay_symbol_770fbfa)['name'][1:]
                else:
                    quay_superclass_name_34e3375 = 'NSObject'
        else:
            quay_superclass_name_34e3375 = ''
        quay_ro_location_b81ebe2 = _name_boundary.attributes(quay_objc2_class_item_bb8a151)['info'] >> 2 << 2
        try:
            quay_objc2_class_ro_item_f8eb501 = _name_boundary.attributes(quay_objc_image_24aab4c)['read_struct'](quay_ro_location_b81ebe2, quay_objc2_class_ro, vm=True)
        except ValueError:
            _name_boundary.attributes(quay_log)['warn'](f"Class Data (c: {hex(_name_boundary.attributes(quay_objc2_class_item_bb8a151)['off'])}) is off-image")
            return None
        if not quay_meta_2d7d4f0:
            try:
                quay_name_71849c4 = _name_boundary.attributes(quay_objc_image_24aab4c)['read_cstr'](_name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['name'], 0, vm=True)
            except ValueError:
                _name_boundary.attributes(quay_log)['warning'](f'Classname out of bounds')
                quay_name_71849c4 = ''
        else:
            quay_name_71849c4 = ''
        quay_methods_0c9736d = []
        quay_properties_06a9068 = []
        if _name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['base_props'] != 0:
            quay_proplist_head_80e3f69 = _name_boundary.attributes(quay_objc_image_24aab4c)['read_struct'](_name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['base_props'], quay_objc2_prop_list)
            quay_ea_d1eeec1 = _name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['base_props']
            quay_ea_d1eeec1 += _name_boundary.attributes(quay_objc2_prop_list)['size'](_name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['ptr_size'])
            for quay_i_132111a in range(1, _name_boundary.attributes(quay_proplist_head_80e3f69)['count'] + 1):
                quay_prop_9d60027 = _name_boundary.attributes(quay_objc_image_24aab4c)['read_struct'](quay_ea_d1eeec1, quay_objc2_prop, vm=True)
                if _name_boundary.attributes(quay_proplist_head_80e3f69)['count'] > 1000:
                    _name_boundary.attributes(quay_log)['warning'](f"Class {quay_name_71849c4} has too many properties ({_name_boundary.attributes(quay_proplist_head_80e3f69)['count']}), skipping loading properties")
                    break
                try:
                    quay_property_abd455f = _name_boundary.attributes(quay_Property)['from_image'](quay_objc_image_24aab4c, quay_prop_9d60027)
                    quay_properties_06a9068.append(quay_property_abd455f)
                    if _name_boundary.has_attribute(quay_property_abd455f, 'attr') and _name_boundary.attributes(quay_property_abd455f)['attr']:
                        if _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_property_abd455f)['attr'])['type'])['type'] == quay_EncodedType.STRUCT:
                            quay_struct_list_da270bb.append(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_property_abd455f)['attr'])['type'])['value'])
                except quay_VMAddressingError as quay_ex_f7b8504:
                    if _name_boundary.attributes(quay_opts)['OBJC_LOAD_ERRORS_SEND_TO_DEBUG']:
                        _name_boundary.attributes(quay_log)['debug'](f"Failed to load a property in {quay_name_71849c4} with {_name_boundary.attributes(quay_ex_f7b8504.__class__)['__name__']}: {str(quay_ex_f7b8504)}")
                    else:
                        _name_boundary.attributes(quay_log)['warning'](f"Failed to load a property in {quay_name_71849c4} with {_name_boundary.attributes(quay_ex_f7b8504.__class__)['__name__']}: {str(quay_ex_f7b8504)}")
                    quay_load_errors_da3819d.append(f"Failed to load a property with {_name_boundary.attributes(quay_ex_f7b8504.__class__)['__name__']}: {str(quay_ex_f7b8504)}")
                except Exception as quay_ex_f7b8504:
                    if not _name_boundary.attributes(quay_ignore)['OBJC_ERRORS']:
                        raise quay_ex_f7b8504
                    _name_boundary.attributes(quay_log)['warning'](f"Failed to load a property in {quay_name_71849c4} with {_name_boundary.attributes(quay_ex_f7b8504.__class__)['__name__']}: {str(quay_ex_f7b8504)}")
                    quay_load_errors_da3819d.append(f"Failed to load a property with {_name_boundary.attributes(quay_ex_f7b8504.__class__)['__name__']}: {str(quay_ex_f7b8504)}")
                quay_ea_d1eeec1 += _name_boundary.attributes(quay_objc2_prop)['size'](_name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['ptr_size'])
        if _name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['base_meths'] != 0:
            quay_methlist_head_d42d608 = _name_boundary.attributes(quay_objc_image_24aab4c)['read_struct'](_name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['base_meths'], quay_objc2_meth_list)
            if _name_boundary.attributes(quay_methlist_head_d42d608)['count'] > 1000:
                _name_boundary.attributes(quay_log)['warning'](f"Class {quay_name_71849c4} has too many methods ({_name_boundary.attributes(quay_methlist_head_d42d608)['count']}), skipping loading methods")
                return None
            quay_methlist_7a3edc6 = quay_MethodList(quay_objc_image_24aab4c, quay_methlist_head_d42d608, _name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['base_meths'], quay_meta_2d7d4f0, quay_name_71849c4)
            quay_load_errors_da3819d += _name_boundary.attributes(quay_methlist_7a3edc6)['load_errors']
            quay_struct_list_da270bb += _name_boundary.attributes(quay_methlist_7a3edc6)['struct_list']
            quay_methods_0c9736d += _name_boundary.attributes(quay_methlist_7a3edc6)['methods']
        _name_boundary.attributes(quay_log)['debug_more'](f"metaclass for {quay_name_71849c4} at {hex(_name_boundary.attributes(quay_objc2_class_item_bb8a151)['isa'])}")
        if _name_boundary.attributes(quay_objc2_class_item_bb8a151)['isa'] != 0 and (not quay_meta_2d7d4f0):
            quay_metaclass_a2b41ac = _name_boundary.attributes(quay_Class)['from_image'](quay_objc_image_24aab4c, _name_boundary.attributes(quay_objc2_class_item_bb8a151)['isa'], meta=True, class_ptr_is_direct=True)
            if quay_metaclass_a2b41ac:
                quay_methods_0c9736d += _name_boundary.attributes(quay_metaclass_a2b41ac)['methods']
        quay_prots_f7c85eb = []
        if _name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['base_prots'] != 0:
            quay_protlist_2342eb3: quay_objc2_prot_list = _name_boundary.attributes(quay_objc_image_24aab4c)['read_struct'](_name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['base_prots'], quay_objc2_prot_list)
            quay_ea_d1eeec1 = _name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['base_prots']
            for quay_i_132111a in range(1, _name_boundary.attributes(quay_protlist_2342eb3)['cnt'] + 1):
                quay_prot_loc_56bb1b2 = _name_boundary.attributes(quay_objc_image_24aab4c)['read_ptr'](quay_ea_d1eeec1 + quay_i_132111a * _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['ptr_size'], vm=True)
                if quay_prot_loc_56bb1b2 in _name_boundary.attributes(quay_objc_image_24aab4c)['prot_map']:
                    quay_prots_f7c85eb.append(_name_boundary.attributes(quay_objc_image_24aab4c)['prot_map'][quay_prot_loc_56bb1b2])
                else:
                    quay_prot_455198c = _name_boundary.attributes(quay_objc_image_24aab4c)['read_struct'](quay_prot_loc_56bb1b2, quay_objc2_prot, vm=True)
                    try:
                        quay_p_826533a = _name_boundary.attributes(quay_Protocol)['from_image'](quay_objc_image_24aab4c, quay_prot_455198c, quay_prot_loc_56bb1b2)
                        quay_prots_f7c85eb.append(quay_p_826533a)
                        _name_boundary.attributes(quay_objc_image_24aab4c)['prot_map'][quay_prot_loc_56bb1b2] = quay_p_826533a
                    except Exception as quay_ex_f7b8504:
                        if not _name_boundary.attributes(quay_ignore)['OBJC_ERRORS']:
                            raise quay_ex_f7b8504
                        if _name_boundary.attributes(quay_opts)['OBJC_LOAD_ERRORS_SEND_TO_DEBUG']:
                            _name_boundary.attributes(quay_log)['debug'](f'Failed to load protocol with {str(quay_ex_f7b8504)}')
                        else:
                            _name_boundary.attributes(quay_log)['warning'](f'Failed to load protocol with {str(quay_ex_f7b8504)}')
                        quay_load_errors_da3819d.append(f'Failed to load a protocol with {str(quay_ex_f7b8504)}')
        quay_ivars_1f75c3a = []
        if _name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['ivars'] != 0:
            quay_ivarlist_de11628: quay_objc2_ivar_list = _name_boundary.attributes(quay_objc_image_24aab4c)['read_struct'](_name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['ivars'], quay_objc2_ivar_list)
            quay_ea_d1eeec1 = _name_boundary.attributes(quay_objc2_class_ro_item_f8eb501)['ivars'] + _name_boundary.attributes(quay_objc2_ivar_list)['size'](_name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['ptr_size'])
            for quay_i_132111a in range(1, _name_boundary.attributes(quay_ivarlist_de11628)['cnt'] + 1):
                quay_ivar_loc_2ae774c = quay_ea_d1eeec1 + _name_boundary.attributes(quay_objc2_ivar)['size'](ptr_size=_name_boundary.attributes(_name_boundary.attributes(quay_objc_image_24aab4c)['image'])['ptr_size']) * (quay_i_132111a - 1)
                quay_ivar_a01d5f2 = _name_boundary.attributes(quay_objc_image_24aab4c)['read_struct'](quay_ivar_loc_2ae774c, quay_objc2_ivar, vm=True)
                try:
                    quay_ivar_object_5cb1173 = _name_boundary.attributes(quay_Ivar)['from_image'](quay_objc_image_24aab4c, quay_ivar_a01d5f2)
                    quay_ivars_1f75c3a.append(quay_ivar_object_5cb1173)
                except Exception as quay_ex_f7b8504:
                    if not _name_boundary.attributes(quay_ignore)['OBJC_ERRORS']:
                        raise quay_ex_f7b8504
                    _name_boundary.attributes(quay_log)['warning'](f'Failed to load ivar with {str(quay_ex_f7b8504)}')
                    quay_load_errors_da3819d.append(f'Failed to load an ivar with {str(quay_ex_f7b8504)}')
        return quay_cls_e401853(quay_name_71849c4, quay_meta_2d7d4f0, quay_superclass_name_34e3375, quay_methods_0c9736d, quay_properties_06a9068, quay_ivars_1f75c3a, quay_prots_f7c85eb, quay_load_errors_da3819d, quay_struct_list_da270bb, loc=quay_objc2_class_location_41d009b)

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_3f587e4', 'name': 'quay_name_d81dfe8', 'superclass_name': 'quay_superclass_name_d4ef3ce', 'methods': 'quay_methods_d9f3075', 'properties': 'quay_properties_f9833d4', 'ivars': 'quay_ivars_dd585a6', 'protocols': 'quay_protocols_5db894e', 'load_errors': 'quay_load_errors_178d308', 'structs': 'quay_structs_7cc0d21'}, 'from_values')
    def quay_from_values(quay_cls_3f587e4, quay_name_d81dfe8, quay_superclass_name_d4ef3ce, quay_methods_d9f3075: quay_List[quay_Method], quay_properties_f9833d4: quay_List['Property'], quay_ivars_dd585a6: quay_List['Ivar'], quay_protocols_5db894e: quay_List['Protocol'], quay_load_errors_178d308=None, quay_structs_7cc0d21=None):
        return quay_cls_3f587e4(quay_name_d81dfe8, False, quay_superclass_name_d4ef3ce, quay_methods_d9f3075, quay_properties_f9833d4, quay_ivars_dd585a6, quay_protocols_5db894e, quay_load_errors_178d308, quay_structs_7cc0d21)

    @_name_boundary.callable_contract({'self': 'quay_self_f1373b8'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_f1373b8):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_a161720', 'name': 'quay_name_1e806c9', 'is_meta': 'quay_is_meta_b9de06f', 'superclass_name': 'quay_superclass_name_f7bd45c', 'methods': 'quay_methods_bfbfaa7', 'properties': 'quay_properties_3c2cd3d', 'ivars': 'quay_ivars_e6eab56', 'protocols': 'quay_protocols_abd32e7', 'load_errors': 'quay_load_errors_432585d', 'structs': 'quay_structs_64b3c75', 'loc': 'quay_loc_6600d27'}, '__init__')
    def __init__(quay_self_a161720, quay_name_1e806c9, quay_is_meta_b9de06f, quay_superclass_name_f7bd45c, quay_methods_bfbfaa7, quay_properties_3c2cd3d, quay_ivars_e6eab56, quay_protocols_abd32e7, quay_load_errors_432585d=None, quay_structs_64b3c75=None, quay_loc_6600d27=0):
        if quay_structs_64b3c75 is None:
            quay_structs_64b3c75 = []
        if quay_load_errors_432585d is None:
            quay_load_errors_432585d = []
        _name_boundary.attributes(quay_self_a161720)['name'] = quay_name_1e806c9
        _name_boundary.attributes(quay_self_a161720)['meta'] = quay_is_meta_b9de06f
        _name_boundary.attributes(quay_self_a161720)['superclass'] = quay_superclass_name_f7bd45c
        _name_boundary.attributes(quay_self_a161720)['loc'] = quay_loc_6600d27
        _name_boundary.attributes(quay_self_a161720)['load_errors'] = quay_load_errors_432585d
        _name_boundary.attributes(quay_self_a161720)['struct_list'] = quay_structs_64b3c75
        _name_boundary.attributes(quay_self_a161720)['linkedlibs'] = []
        _name_boundary.attributes(quay_self_a161720)['linked_classes'] = []
        _name_boundary.attributes(quay_self_a161720)['fdec_classes'] = []
        _name_boundary.attributes(quay_self_a161720)['fdec_prots'] = []
        _name_boundary.attributes(quay_self_a161720)['methods'] = quay_methods_bfbfaa7
        _name_boundary.attributes(quay_self_a161720)['properties'] = quay_properties_3c2cd3d
        _name_boundary.attributes(quay_self_a161720)['protocols'] = quay_protocols_abd32e7
        _name_boundary.attributes(quay_self_a161720)['ivars'] = quay_ivars_e6eab56

    @_name_boundary.callable_contract({'self': 'quay_self_3cc2058'}, 'serialize')
    def quay_serialize(quay_self_3cc2058):
        return {'name': _name_boundary.attributes(quay_self_3cc2058)['name'], 'superclass': _name_boundary.attributes(quay_self_3cc2058)['superclass'], 'methods': [_name_boundary.attributes(quay_meth_c7626ff)['serialize']() for quay_meth_c7626ff in _name_boundary.attributes(quay_self_3cc2058)['methods']], 'properties': [_name_boundary.attributes(quay_prop_adb3207)['serialize']() for quay_prop_adb3207 in _name_boundary.attributes(quay_self_3cc2058)['properties']], 'protocols': [_name_boundary.attributes(quay_prot_edce63e)['name'] for quay_prot_edce63e in _name_boundary.attributes(quay_self_3cc2058)['protocols']], 'ivars': [_name_boundary.attributes(quay_ivar_986f5aa)['serialize']() for quay_ivar_986f5aa in _name_boundary.attributes(quay_self_3cc2058)['ivars']]}

    @_name_boundary.callable_contract({'self': 'quay_self_dd1c448'}, '__str__')
    def __str__(quay_self_dd1c448):
        quay_ret_07b7c4d = ''
        quay_ret_07b7c4d += _name_boundary.attributes(quay_self_dd1c448)['name']
        return quay_ret_07b7c4d

    @_name_boundary.callable_contract({'self': 'quay_self_2828b1d'}, '_load_linked_libraries')
    def quay__load_linked_libraries(quay_self_2828b1d):
        pass
quay_attr_encodings = {'&': 'retain', 'N': 'nonatomic', 'W': 'weak', 'R': 'readonly', 'C': 'copy'}
quay_property_attr = _name_boundary.named_record('property_attr', ['type', 'attributes', 'ivar', 'is_id', 'typestr', 'getter', 'setter', 'is_dynamic'])

@_name_boundary.class_contract('Property', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'serialize': 'quay_serialize', '_renderable_type': 'quay__renderable_type', 'decode_property_attributes': 'quay_decode_property_attributes', 'name': 'quay_name', 'is_id': 'quay_is_id', 'attr': 'quay_attr', 'attr_string': 'quay_attr_string', 'type': 'quay_type', 'attributes': 'quay_attributes', 'ivarname': 'quay_ivarname', 'getter': 'quay_getter', 'setter': 'quay_setter'})
class quay_Property(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_c6280b1', 'objc_image': 'quay_objc_image_e862dda', 'property': 'quay_property_43e8962'}, 'from_image')
    def quay_from_image(quay_cls_c6280b1, quay_objc_image_e862dda: quay_ObjCImage, quay_property_43e8962: quay_objc2_prop):
        quay_name_7b1d2de = _name_boundary.attributes(quay_objc_image_e862dda)['read_cstr'](_name_boundary.attributes(quay_property_43e8962)['name'], 0, vm=True)
        quay_attr_string_ad1b3ae = _name_boundary.attributes(quay_objc_image_e862dda)['read_cstr'](_name_boundary.attributes(quay_property_43e8962)['attr'], 0, vm=True)
        return quay_cls_c6280b1(quay_name_7b1d2de, quay_attr_string_ad1b3ae, _name_boundary.attributes(quay_objc_image_e862dda)['tp'])

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_766877f', 'name': 'quay_name_360194a', 'attr_string': 'quay_attr_string_9195985', 'type_processor': 'quay_type_processor_a209541'}, 'from_values')
    def quay_from_values(quay_cls_766877f, quay_name_360194a, quay_attr_string_9195985, quay_type_processor_a209541=None):
        if not quay_type_processor_a209541:
            quay_type_processor_a209541 = quay_TypeProcessor()
        return quay_cls_766877f(quay_name_360194a, quay_attr_string_9195985, quay_type_processor_a209541)

    @_name_boundary.callable_contract({'self': 'quay_self_b4fdf56'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_b4fdf56):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_d1ae588', 'name': 'quay_name_2f67d2b', 'attr_string': 'quay_attr_string_ed86bda', 'type_processor': 'quay_type_processor_021e7dc'}, '__init__')
    def __init__(quay_self_d1ae588, quay_name_2f67d2b, quay_attr_string_ed86bda, quay_type_processor_021e7dc):
        _name_boundary.attributes(quay_self_d1ae588)['name']: str = quay_name_2f67d2b
        try:
            _name_boundary.attributes(quay_self_d1ae588)['attr'] = _name_boundary.attributes(quay_self_d1ae588)['decode_property_attributes'](quay_type_processor_021e7dc, quay_attr_string_ed86bda)
            _name_boundary.attributes(quay_self_d1ae588)['attr_string'] = quay_attr_string_ed86bda
            _name_boundary.attributes(quay_self_d1ae588)['type'] = _name_boundary.attributes(quay_self_d1ae588)['_renderable_type'](_name_boundary.attributes(_name_boundary.attributes(quay_self_d1ae588)['attr'])['type'])
            _name_boundary.attributes(quay_self_d1ae588)['is_id'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_d1ae588)['attr'])['is_id']
            _name_boundary.attributes(quay_self_d1ae588)['attributes'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_d1ae588)['attr'])['attributes']
            _name_boundary.attributes(quay_self_d1ae588)['ivarname'] = _name_boundary.attributes(quay_self_d1ae588)['attr'].ivar
            if _name_boundary.attributes(_name_boundary.attributes(quay_self_d1ae588)['attr'])['getter']:
                _name_boundary.attributes(quay_self_d1ae588)['getter'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_d1ae588)['attr'])['getter']
            else:
                _name_boundary.attributes(quay_self_d1ae588)['getter'] = _name_boundary.attributes(quay_self_d1ae588)['name']
            if _name_boundary.attributes(_name_boundary.attributes(quay_self_d1ae588)['attr'])['setter']:
                _name_boundary.attributes(quay_self_d1ae588)['setter'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_d1ae588)['attr'])['setter']
            else:
                _name_boundary.attributes(quay_self_d1ae588)['setter'] = 'set' + _name_boundary.attributes(quay_self_d1ae588)['name'][0].upper() + _name_boundary.attributes(quay_self_d1ae588)['name'][1:]
        except IndexError:
            _name_boundary.attributes(quay_log)['warn'](f"issue with property {_name_boundary.attributes(quay_self_d1ae588)['name']} attr {quay_attr_string_ed86bda}")
            _name_boundary.attributes(quay_self_d1ae588)['type'] = '?'
            _name_boundary.attributes(quay_self_d1ae588)['attr_string'] = ''
            _name_boundary.attributes(quay_self_d1ae588)['is_id'] = False
            _name_boundary.attributes(quay_self_d1ae588)['attributes'] = []
            _name_boundary.attributes(quay_self_d1ae588)['ivarname'] = ''
            _name_boundary.attributes(quay_self_d1ae588)['getter'] = ''
            _name_boundary.attributes(quay_self_d1ae588)['setter'] = ''
            _name_boundary.attributes(quay_self_d1ae588)['attr'] = None
        except TypeError:
            _name_boundary.attributes(quay_log)['warn'](f"issue with property {_name_boundary.attributes(quay_self_d1ae588)['name']} attr {quay_attr_string_ed86bda}")
            _name_boundary.attributes(quay_self_d1ae588)['type'] = '?'
            _name_boundary.attributes(quay_self_d1ae588)['attr_string'] = ''
            _name_boundary.attributes(quay_self_d1ae588)['is_id'] = False
            _name_boundary.attributes(quay_self_d1ae588)['attributes'] = []
            _name_boundary.attributes(quay_self_d1ae588)['ivarname'] = ''
            _name_boundary.attributes(quay_self_d1ae588)['getter'] = ''
            _name_boundary.attributes(quay_self_d1ae588)['setter'] = ''
            _name_boundary.attributes(quay_self_d1ae588)['attr'] = None

    @_name_boundary.callable_contract({'self': 'quay_self_b4a6a6a'}, 'serialize')
    def quay_serialize(quay_self_b4a6a6a):
        return {'name': _name_boundary.attributes(quay_self_b4a6a6a)['name'], 'type': _name_boundary.attributes(quay_self_b4a6a6a)['type'], 'is_id': _name_boundary.attributes(quay_self_b4a6a6a)['is_id'], 'ivar_name': _name_boundary.attributes(quay_self_b4a6a6a)['ivarname'], 'attributes': _name_boundary.attributes(quay_self_b4a6a6a)['attributes'], 'attr_string': _name_boundary.attributes(quay_self_b4a6a6a)['attr_string'], 'getter': _name_boundary.attributes(quay_self_b4a6a6a)['getter'], 'setter': _name_boundary.attributes(quay_self_b4a6a6a)['setter'], 'rendered': str(quay_self_b4a6a6a)}

    @_name_boundary.callable_contract({'self': 'quay_self_9da66a0'}, '__str__')
    def __str__(quay_self_9da66a0):
        if not _name_boundary.has_attribute(quay_self_9da66a0, 'attributes'):
            return f"// Something went wrong loading property {_name_boundary.attributes(quay_self_9da66a0)['name']}"
        quay_ret_9fb84d5 = '@property '
        if len(_name_boundary.attributes(quay_self_9da66a0)['attributes']) > 0:
            quay_ret_9fb84d5 += '(' + ', '.join(_name_boundary.attributes(quay_self_9da66a0)['attributes']) + ') '
        if _name_boundary.attributes(quay_self_9da66a0)['type'].startswith('<'):
            quay_ret_9fb84d5 += 'NSObject'
        quay_ret_9fb84d5 += _name_boundary.attributes(quay_self_9da66a0)['type'] + ' '
        if _name_boundary.attributes(quay_self_9da66a0)['is_id']:
            quay_ret_9fb84d5 += '*'
        quay_ret_9fb84d5 += _name_boundary.attributes(quay_self_9da66a0)['name']
        return quay_ret_9fb84d5

    @staticmethod
    @_name_boundary.callable_contract({'_type': 'quay__type_e102412'}, '_renderable_type')
    def quay__renderable_type(quay__type_e102412: quay_Type):
        if _name_boundary.attributes(quay__type_e102412)['type'] == quay_EncodedType.NORMAL:
            return str(quay__type_e102412)
        elif _name_boundary.attributes(quay__type_e102412)['type'] == quay_EncodedType.STRUCT:
            quay_ptraddon_16215a1 = ''
            for quay_i_cdcb938 in range(0, _name_boundary.attributes(quay__type_e102412)['pointer_count']):
                quay_ptraddon_16215a1 += '*'
            return quay_ptraddon_16215a1 + _name_boundary.attributes(_name_boundary.attributes(quay__type_e102412)['value'])['name']
        return str(quay__type_e102412)

    @staticmethod
    @_name_boundary.callable_contract({'type_processor': 'quay_type_processor_925572e', 'type_str': 'quay_type_str_342fcfd'}, 'decode_property_attributes')
    def quay_decode_property_attributes(quay_type_processor_925572e, quay_type_str_342fcfd: str):
        quay_attribute_strings_e240d15 = quay_type_str_342fcfd.split(',')
        quay_ptype_664d984 = ''
        quay_is_id_0414c59 = False
        quay_ivar_786e3f2 = ''
        quay_property_attributes_5a5bbc4 = []
        quay_getter_9d17421 = None
        quay_setter_2ef1a55 = None
        quay_is_dynamic_3419e52 = False
        for quay_attribute_7bdf7fc in quay_attribute_strings_e240d15:
            quay_indicator_760b810 = quay_attribute_7bdf7fc[0]
            if quay_indicator_760b810 == 'T':
                quay_ptype_664d984 = _name_boundary.attributes(quay_type_processor_925572e)['process'](quay_attribute_7bdf7fc[1:])[0]
                if quay_ptype_664d984 == '{':
                    print(quay_attribute_7bdf7fc)
                quay_is_id_0414c59 = quay_attribute_7bdf7fc[1] == '@'
                continue
            if quay_indicator_760b810 == 'V':
                quay_ivar_786e3f2 = quay_attribute_7bdf7fc[1:]
            if quay_indicator_760b810 == 'G':
                quay_getter_9d17421 = quay_attribute_7bdf7fc[1:]
            if quay_indicator_760b810 == 'S':
                quay_setter_2ef1a55 = quay_attribute_7bdf7fc[1:]
            if quay_indicator_760b810 == 'D':
                quay_is_dynamic_3419e52 = True
            if quay_indicator_760b810 in quay_attr_encodings:
                quay_property_attributes_5a5bbc4.append(quay_attr_encodings[quay_indicator_760b810])
        if quay_getter_9d17421:
            quay_property_attributes_5a5bbc4.append(f'getter={quay_getter_9d17421}')
        if quay_setter_2ef1a55:
            quay_property_attributes_5a5bbc4.append(f'setter={quay_setter_2ef1a55}')
        return quay_property_attr(quay_ptype_664d984, quay_property_attributes_5a5bbc4, quay_ivar_786e3f2, quay_is_id_0414c59, quay_type_str_342fcfd, quay_getter_9d17421, quay_setter_2ef1a55, quay_is_dynamic_3419e52)

@_name_boundary.class_contract('Category', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'serialize': 'quay_serialize', 'name': 'quay_name', 'classname': 'quay_classname', 'loc': 'quay_loc', 'load_errors': 'quay_load_errors', 'struct_list': 'quay_struct_list', 'methods': 'quay_methods', 'properties': 'quay_properties', 'protocols': 'quay_protocols'})
class quay_Category(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_fe3e086', 'objc_image': 'quay_objc_image_0b6011c', 'category_ptr': 'quay_category_ptr_e176e00'}, 'from_image')
    def quay_from_image(quay_cls_fe3e086, quay_objc_image_0b6011c: quay_ObjCImage, quay_category_ptr_e176e00):
        try:
            quay_loc_47b669b = _name_boundary.attributes(quay_objc_image_0b6011c)['read_ptr'](quay_category_ptr_e176e00, vm=True)
            quay_struct_1e26930: quay_objc2_category = _name_boundary.attributes(quay_objc_image_0b6011c)['read_struct'](quay_loc_47b669b, quay_objc2_category, vm=True)
            quay_name_c0b2a58 = _name_boundary.attributes(quay_objc_image_0b6011c)['read_cstr'](_name_boundary.attributes(quay_struct_1e26930)['name'], vm=True)
        except ValueError as quay_ex_86a3ef7:
            _name_boundary.attributes(quay_log)['error']("Couldn't load basic info about a Category: " + str(quay_ex_86a3ef7))
            return None
        quay_classname_48392f7 = ''
        try:
            quay_sym_6ce97e7 = _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_0b6011c)['image'])['import_table'][quay_loc_47b669b + _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_0b6011c)['image'])['ptr_size']]
            quay_classname_48392f7 = _name_boundary.attributes(quay_sym_6ce97e7)['name'][1:]
        except KeyError:
            pass
        quay_methods_b8c52f4 = []
        quay_properties_755be18 = []
        quay_load_errors_011311c = []
        quay_struct_list_7519c83 = []
        if _name_boundary.attributes(quay_struct_1e26930)['inst_meths'] != 0:
            try:
                quay_methlist_head_a75dc85 = _name_boundary.attributes(quay_objc_image_0b6011c)['read_struct'](_name_boundary.attributes(quay_struct_1e26930)['inst_meths'], quay_objc2_meth_list)
                quay_methlist_b728cf7 = quay_MethodList(quay_objc_image_0b6011c, quay_methlist_head_a75dc85, _name_boundary.attributes(quay_struct_1e26930)['inst_meths'], False, f'{quay_classname_48392f7}+{quay_name_c0b2a58}')
                quay_load_errors_011311c += _name_boundary.attributes(quay_methlist_b728cf7)['load_errors']
                quay_struct_list_7519c83 += _name_boundary.attributes(quay_methlist_b728cf7)['struct_list']
                quay_methods_b8c52f4 += _name_boundary.attributes(quay_methlist_b728cf7)['methods']
            except ValueError:
                _name_boundary.attributes(quay_log)['warn']('Methods for this category are off-image.')
        if _name_boundary.attributes(quay_struct_1e26930)['class_meths'] != 0:
            try:
                quay_methlist_head_a75dc85 = _name_boundary.attributes(quay_objc_image_0b6011c)['read_struct'](_name_boundary.attributes(quay_struct_1e26930)['class_meths'], quay_objc2_meth_list)
                quay_methlist_b728cf7 = quay_MethodList(quay_objc_image_0b6011c, quay_methlist_head_a75dc85, _name_boundary.attributes(quay_struct_1e26930)['class_meths'], True, f'{quay_classname_48392f7}+{quay_name_c0b2a58}')
                quay_load_errors_011311c += _name_boundary.attributes(quay_methlist_b728cf7)['load_errors']
                quay_struct_list_7519c83 += _name_boundary.attributes(quay_methlist_b728cf7)['struct_list']
                quay_methods_b8c52f4 += _name_boundary.attributes(quay_methlist_b728cf7)['methods']
            except ValueError:
                _name_boundary.attributes(quay_log)['warn']('Methods for this category are off-image.')
        if _name_boundary.attributes(quay_struct_1e26930)['props'] != 0:
            try:
                quay_proplist_head_6a9591f = _name_boundary.attributes(quay_objc_image_0b6011c)['read_struct'](_name_boundary.attributes(quay_struct_1e26930)['props'], quay_objc2_prop_list)
                quay_ea_30702b2 = _name_boundary.attributes(quay_struct_1e26930)['props']
                quay_ea_30702b2 += _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_0b6011c)['image'])['ptr_size']
                for quay_i_721fbfd in range(1, _name_boundary.attributes(quay_proplist_head_6a9591f)['count'] + 1):
                    quay_prop_eab19d2 = _name_boundary.attributes(quay_objc_image_0b6011c)['read_struct'](quay_ea_30702b2, quay_objc2_prop, vm=True)
                    try:
                        quay_properties_755be18.append(_name_boundary.attributes(quay_Property)['from_image'](quay_objc_image_0b6011c, quay_prop_eab19d2))
                    except Exception as quay_ex_86a3ef7:
                        _name_boundary.attributes(quay_log)['warning'](f'Failed to load property with {str(quay_ex_86a3ef7)}')
                    quay_ea_30702b2 += _name_boundary.attributes(quay_objc2_prop)['size'](_name_boundary.attributes(_name_boundary.attributes(quay_objc_image_0b6011c)['image'])['ptr_size'])
            except ValueError:
                _name_boundary.attributes(quay_log)['warn']('Properties for this category are off-image.')
        return quay_cls_fe3e086(quay_classname_48392f7, quay_name_c0b2a58, quay_methods_b8c52f4, quay_properties_755be18, loc=quay_loc_47b669b)

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_e7ad1a1', 'classname': 'quay_classname_99deede', 'name': 'quay_name_8aecc58', 'methods': 'quay_methods_6968569', 'properties': 'quay_properties_f75cba2', 'load_errors': 'quay_load_errors_188195e', 'struct_list': 'quay_struct_list_b4a363e'}, 'from_values')
    def quay_from_values(quay_cls_e7ad1a1, quay_classname_99deede, quay_name_8aecc58, quay_methods_6968569, quay_properties_f75cba2, quay_load_errors_188195e=None, quay_struct_list_b4a363e=None):
        return quay_cls_e7ad1a1(quay_classname_99deede, quay_name_8aecc58, quay_methods_6968569, quay_properties_f75cba2, quay_load_errors_188195e, quay_struct_list_b4a363e)

    @_name_boundary.callable_contract({'self': 'quay_self_8714230'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_8714230):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_f9a34fa', 'classname': 'quay_classname_0da078d', 'name': 'quay_name_b08cacd', 'methods': 'quay_methods_30263c7', 'properties': 'quay_properties_6247c40', 'load_errors': 'quay_load_errors_6f3273b', 'struct_list': 'quay_struct_list_d1ecfba', 'loc': 'quay_loc_cc2ea73'}, '__init__')
    def __init__(quay_self_f9a34fa, quay_classname_0da078d, quay_name_b08cacd, quay_methods_30263c7, quay_properties_6247c40, quay_load_errors_6f3273b=None, quay_struct_list_d1ecfba=None, quay_loc_cc2ea73=0):
        if quay_load_errors_6f3273b is None:
            quay_load_errors_6f3273b = []
        if quay_struct_list_d1ecfba is None:
            quay_struct_list_d1ecfba = []
        _name_boundary.attributes(quay_self_f9a34fa)['name'] = quay_name_b08cacd
        _name_boundary.attributes(quay_self_f9a34fa)['classname'] = quay_classname_0da078d
        _name_boundary.attributes(quay_self_f9a34fa)['loc'] = quay_loc_cc2ea73
        _name_boundary.attributes(quay_self_f9a34fa)['load_errors'] = quay_load_errors_6f3273b
        _name_boundary.attributes(quay_self_f9a34fa)['struct_list'] = quay_struct_list_d1ecfba
        _name_boundary.attributes(quay_self_f9a34fa)['methods'] = quay_methods_30263c7
        _name_boundary.attributes(quay_self_f9a34fa)['properties'] = quay_properties_6247c40
        _name_boundary.attributes(quay_self_f9a34fa)['protocols'] = []

    @_name_boundary.callable_contract({'self': 'quay_self_751a15a'}, 'serialize')
    def quay_serialize(quay_self_751a15a):
        return {'name': _name_boundary.attributes(quay_self_751a15a)['name'], 'classname': _name_boundary.attributes(quay_self_751a15a)['classname'], 'methods': [_name_boundary.attributes(quay_method_6d29952)['serialize']() for quay_method_6d29952 in _name_boundary.attributes(quay_self_751a15a)['methods']], 'properties': [_name_boundary.attributes(quay_prop_eeeabca)['serialize']() for quay_prop_eeeabca in _name_boundary.attributes(quay_self_751a15a)['properties']], 'protocols': [_name_boundary.attributes(quay_prot_dfaeb86)['name'] for quay_prot_dfaeb86 in _name_boundary.attributes(quay_self_751a15a)['protocols']]}

@_name_boundary.class_contract('Protocol', {'from_image': 'quay_from_image', 'load_methods': 'quay_load_methods', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'serialize': 'quay_serialize', 'name': 'quay_name', 'loc': 'quay_loc', 'load_errors': 'quay_load_errors', 'struct_list': 'quay_struct_list', 'methods': 'quay_methods', 'opt_methods': 'quay_opt_methods', 'properties': 'quay_properties'})
class quay_Protocol(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_a68b1f9', 'objc_image': 'quay_objc_image_56a59df', 'protocol': 'quay_protocol_7fff9cc', 'loc': 'quay_loc_72867b2'}, 'from_image')
    def quay_from_image(quay_cls_a68b1f9, quay_objc_image_56a59df: 'ObjCImage', quay_protocol_7fff9cc: quay_objc2_prot, quay_loc_72867b2):
        if quay_loc_72867b2 in _name_boundary.attributes(quay_objc_image_56a59df)['prot_map']:
            return _name_boundary.attributes(quay_objc_image_56a59df)['prot_map'][quay_loc_72867b2]
        try:
            quay_name_adc4717 = _name_boundary.attributes(quay_objc_image_56a59df)['read_cstr'](_name_boundary.attributes(quay_protocol_7fff9cc)['name'], 0, vm=True)
        except ValueError as quay_ex_91bf63e:
            _name_boundary.attributes(quay_log)['error']("Couldn't load basic info about a Category: " + str(quay_ex_91bf63e))
            return None
        quay_load_errors_9c7c9ef = []
        quay_struct_list_a8f8b8e = []
        quay_methods_e03db4f = []
        quay_opt_methods_3d403b5 = []
        quay_properties_0f80cf9 = []
        quay_methlist_779c3c4 = _name_boundary.attributes(quay_Protocol)['load_methods'](quay_objc_image_56a59df, quay_name_adc4717, _name_boundary.attributes(quay_protocol_7fff9cc)['inst_meths'])
        quay_load_errors_9c7c9ef += _name_boundary.attributes(quay_methlist_779c3c4)['load_errors']
        quay_struct_list_a8f8b8e += _name_boundary.attributes(quay_methlist_779c3c4)['struct_list']
        quay_methods_e03db4f += _name_boundary.attributes(quay_methlist_779c3c4)['methods']
        quay_methlist_779c3c4 = _name_boundary.attributes(quay_Protocol)['load_methods'](quay_objc_image_56a59df, quay_name_adc4717, _name_boundary.attributes(quay_protocol_7fff9cc)['class_meths'], True)
        quay_load_errors_9c7c9ef += _name_boundary.attributes(quay_methlist_779c3c4)['load_errors']
        quay_struct_list_a8f8b8e += _name_boundary.attributes(quay_methlist_779c3c4)['struct_list']
        quay_methods_e03db4f += _name_boundary.attributes(quay_methlist_779c3c4)['methods']
        quay_methlist_779c3c4 = _name_boundary.attributes(quay_Protocol)['load_methods'](quay_objc_image_56a59df, quay_name_adc4717, _name_boundary.attributes(quay_protocol_7fff9cc)['opt_inst_meths'])
        quay_load_errors_9c7c9ef += _name_boundary.attributes(quay_methlist_779c3c4)['load_errors']
        quay_struct_list_a8f8b8e += _name_boundary.attributes(quay_methlist_779c3c4)['struct_list']
        quay_opt_methods_3d403b5 += _name_boundary.attributes(quay_methlist_779c3c4)['methods']
        quay_methlist_779c3c4 = _name_boundary.attributes(quay_Protocol)['load_methods'](quay_objc_image_56a59df, quay_name_adc4717, _name_boundary.attributes(quay_protocol_7fff9cc)['opt_class_meths'], True)
        quay_load_errors_9c7c9ef += _name_boundary.attributes(quay_methlist_779c3c4)['load_errors']
        quay_struct_list_a8f8b8e += _name_boundary.attributes(quay_methlist_779c3c4)['struct_list']
        quay_opt_methods_3d403b5 += _name_boundary.attributes(quay_methlist_779c3c4)['methods']
        if _name_boundary.attributes(quay_protocol_7fff9cc)['inst_props'] != 0:
            quay_proplist_head_9ffc9f9 = _name_boundary.attributes(quay_objc_image_56a59df)['read_struct'](_name_boundary.attributes(quay_protocol_7fff9cc)['inst_props'], quay_objc2_prop_list)
            quay_ea_36b1cf5 = _name_boundary.attributes(quay_protocol_7fff9cc)['inst_props']
            quay_ea_36b1cf5 += _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_56a59df)['image'])['ptr_size']
            for quay_i_c7240b5 in range(1, _name_boundary.attributes(quay_proplist_head_9ffc9f9)['count'] + 1):
                quay_prop_0e6373c = _name_boundary.attributes(quay_objc_image_56a59df)['read_struct'](quay_ea_36b1cf5, quay_objc2_prop, vm=True)
                try:
                    quay_properties_0f80cf9.append(_name_boundary.attributes(quay_Property)['from_image'](quay_objc_image_56a59df, quay_prop_0e6373c))
                except Exception as quay_ex_91bf63e:
                    _name_boundary.attributes(quay_log)['warning'](f'Failed to load property with {str(quay_ex_91bf63e)}')
                quay_ea_36b1cf5 += _name_boundary.attributes(quay_objc2_prop)['size'](_name_boundary.attributes(_name_boundary.attributes(quay_objc_image_56a59df)['image'])['ptr_size'])
        return quay_cls_a68b1f9(quay_name_adc4717, quay_methods_e03db4f, quay_opt_methods_3d403b5, quay_properties_0f80cf9, quay_load_errors_9c7c9ef, quay_struct_list_a8f8b8e, loc=quay_loc_72867b2)

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_0b69aed', 'objc_image': 'quay_objc_image_197243d', 'name': 'quay_name_34fa678', 'loc': 'quay_loc_290820d', 'meta': 'quay_meta_3378157'}, 'load_methods')
    def quay_load_methods(quay_cls_0b69aed, quay_objc_image_197243d, quay_name_34fa678, quay_loc_290820d, quay_meta_3378157=False):
        quay_vm_ea_e61fe48 = quay_loc_290820d
        if quay_loc_290820d != 0:
            quay_methlist_head_f30242a = _name_boundary.attributes(quay_objc_image_197243d)['read_struct'](quay_loc_290820d, quay_objc2_meth_list)
        else:
            quay_methlist_head_f30242a = None
        quay_methlist_6f1e7cc = quay_MethodList(quay_objc_image_197243d, quay_methlist_head_f30242a, quay_vm_ea_e61fe48, quay_meta_3378157, quay_name_34fa678)
        return quay_methlist_6f1e7cc

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_d9c0dbc', 'name': 'quay_name_e43e23c', 'methods': 'quay_methods_7eb0bd8', 'opt_methods': 'quay_opt_methods_f1dd4a8', 'properties': 'quay_properties_aeab008', 'load_errors': 'quay_load_errors_fd9d7b4', 'struct_list': 'quay_struct_list_0a78090'}, 'from_values')
    def quay_from_values(quay_cls_d9c0dbc, quay_name_e43e23c, quay_methods_7eb0bd8, quay_opt_methods_f1dd4a8, quay_properties_aeab008, quay_load_errors_fd9d7b4=None, quay_struct_list_0a78090=None):
        return quay_cls_d9c0dbc(quay_name_e43e23c, quay_methods_7eb0bd8, quay_opt_methods_f1dd4a8, quay_properties_aeab008, quay_load_errors_fd9d7b4, quay_struct_list_0a78090)

    @_name_boundary.callable_contract({'self': 'quay_self_8e0d9ee'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_8e0d9ee):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_6105775', 'name': 'quay_name_617a3f4', 'methods': 'quay_methods_d3674f8', 'opt_methods': 'quay_opt_methods_929cd2d', 'properties': 'quay_properties_0812e93', 'load_errors': 'quay_load_errors_c57ac91', 'struct_list': 'quay_struct_list_b9c1942', 'loc': 'quay_loc_6d6f080'}, '__init__')
    def __init__(quay_self_6105775, quay_name_617a3f4, quay_methods_d3674f8, quay_opt_methods_929cd2d, quay_properties_0812e93, quay_load_errors_c57ac91=None, quay_struct_list_b9c1942=None, quay_loc_6d6f080=0):
        if quay_struct_list_b9c1942 is None:
            quay_struct_list_b9c1942 = []
        if quay_load_errors_c57ac91 is None:
            quay_load_errors_c57ac91 = []
        _name_boundary.attributes(quay_self_6105775)['name'] = quay_name_617a3f4
        _name_boundary.attributes(quay_self_6105775)['loc'] = quay_loc_6d6f080
        _name_boundary.attributes(quay_self_6105775)['load_errors'] = quay_load_errors_c57ac91
        _name_boundary.attributes(quay_self_6105775)['struct_list'] = quay_struct_list_b9c1942
        _name_boundary.attributes(quay_self_6105775)['methods'] = quay_methods_d3674f8
        _name_boundary.attributes(quay_self_6105775)['opt_methods'] = quay_opt_methods_929cd2d
        _name_boundary.attributes(quay_self_6105775)['properties'] = quay_properties_0812e93

    @_name_boundary.callable_contract({'self': 'quay_self_53285b8'}, 'serialize')
    def quay_serialize(quay_self_53285b8):
        return {'name': _name_boundary.attributes(quay_self_53285b8)['name'], 'methods': [_name_boundary.attributes(quay_meth_35972bf)['serialize']() for quay_meth_35972bf in _name_boundary.attributes(quay_self_53285b8)['methods']], 'optional-methods': [_name_boundary.attributes(quay_meth_bf08763)['serialize']() for quay_meth_bf08763 in _name_boundary.attributes(quay_self_53285b8)['opt_methods']], 'properties': [_name_boundary.attributes(quay_prop_b8e84cc)['serialize']() for quay_prop_b8e84cc in _name_boundary.attributes(quay_self_53285b8)['properties']]}

    @_name_boundary.callable_contract({'self': 'quay_self_d35f112'}, '__str__')
    def __str__(quay_self_d35f112):
        return _name_boundary.attributes(quay_self_d35f112)['name']
_name_boundary.module_contract(globals(), {'LinkedClass': 'quay_LinkedClass', 'Protocol': 'quay_Protocol', 'Type': 'quay_Type', 'METHOD_LIST_FLAGS_MASK': 'quay_METHOD_LIST_FLAGS_MASK', 'Image': 'quay_Image', 'attr_encodings': 'quay_attr_encodings', 'type_encodings': 'quay_type_encodings', 'EncodedType': 'quay_EncodedType', 'RELATIVE_METHOD_FLAG': 'quay_RELATIVE_METHOD_FLAG', 'EncodingType': 'quay_EncodingType', 'Queue': 'quay_Queue', 'Method': 'quay_Method', 'ignore': 'quay_ignore', 'namedtuple': 'quay_namedtuple', 'MethodList': 'quay_MethodList', 'Constructable': 'quay_Constructable', 'Ivar': 'quay_Ivar', 'usi32_to_si32': 'quay_usi32_to_si32', 'RELATIVE_METHODS_SELECTORS_ARE_DIRECT_FLAG': 'quay_RELATIVE_METHODS_SELECTORS_ARE_DIRECT_FLAG', 'opts': 'quay_opts', 'Struct_Representation': 'quay_Struct_Representation', 'Property': 'quay_Property', 'Enum': 'quay_Enum', 'Optional': 'quay_Optional', 'ObjCImage': 'quay_ObjCImage', 'List': 'quay_List', 'VMAddressingError': 'quay_VMAddressingError', 'Class': 'quay_Class', 'Dict': 'quay_Dict', 'TypeProcessor': 'quay_TypeProcessor', 'property_attr': 'quay_property_attr', 'Category': 'quay_Category', 'QueueItem': 'quay_QueueItem', 'log': 'quay_log'})
