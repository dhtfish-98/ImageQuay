# Derived from src/ktool/swift.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  swift.py
#
#  Swift type processing
#
#  Comments here are currently from me reverse engineering type ser
#
#  I have a habit of REing things that are technically publicly available,
#       because this is the way I like to write these parsers, it's far less boring,
#       and gives me a better initial understanding/foothold.
#
#  So please note that comments, etc may be inaccurate until I eventually get around to
#       diving into the swift compiler.
#
#  https://belkadan.com/blog/2020/09/Swift-Runtime-Type-Metadata/
#  https://knight.sc/reverse%20engineering/2019/07/17/swift-metadata.html
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary
from imagequay_layout.record_contract import quay_Constructable as quay_Constructable
from imagequay_swift.metadata_records import *
from imagequay_swift.name_decoder import quay_demangle as quay_demangle
from imagequay.metadata_reader import quay_Image as quay_Image
from imagequay.container_io import quay_Section as quay_Section
from imagequay.objc_model import quay_Class as quay_Class
from imagequay_support.diagnostics import quay_log as quay_log
from imagequay.formatting import quay_uint_to_int as quay_uint_to_int

@_name_boundary.class_contract('Field', {'flags': 'quay_flags', 'type_name': 'quay_type_name', 'name': 'quay_name'})
class quay_Field:

    @_name_boundary.callable_contract({'self': 'quay_self_79ef526', 'flags': 'quay_flags_1bcc93b', 'type_name': 'quay_type_name_ff158f7', 'name': 'quay_name_3783761'}, '__init__')
    def __init__(quay_self_79ef526, quay_flags_1bcc93b, quay_type_name_ff158f7, quay_name_3783761):
        _name_boundary.attributes(quay_self_79ef526)['flags'] = quay_flags_1bcc93b
        _name_boundary.attributes(quay_self_79ef526)['type_name'] = quay_type_name_ff158f7
        _name_boundary.attributes(quay_self_79ef526)['name'] = quay_name_3783761

    @_name_boundary.callable_contract({'self': 'quay_self_47f94ee'}, '__str__')
    def __str__(quay_self_47f94ee):
        return f"{_name_boundary.attributes(quay_self_47f94ee)['name']} : {_name_boundary.attributes(quay_self_47f94ee)['type_name']} ({hex(_name_boundary.attributes(quay_self_47f94ee)['flags'])})"

@_name_boundary.class_contract('_FieldDescriptor', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'fields': 'quay_fields', 'desc': 'quay_desc'})
class quay__FieldDescriptor(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_d4c45e2', 'objc_image': 'quay_objc_image_dac82d1', 'location': 'quay_location_00542f2'}, 'from_image')
    def quay_from_image(quay_cls_d4c45e2, quay_objc_image_dac82d1, quay_location_00542f2):
        quay_image_b27d478 = _name_boundary.attributes(quay_objc_image_dac82d1)['image']
        quay_fields_efb2cfe = []
        quay_fd_9f70386 = _name_boundary.attributes(quay_image_b27d478)['read_struct'](quay_location_00542f2, quay_FieldDescriptor, vm=True)
        for quay_i_13cfd55 in range(_name_boundary.attributes(quay_fd_9f70386)['NumFields']):
            quay_ea_f0ab59a = quay_location_00542f2 + _name_boundary.attributes(quay_FieldDescriptor)['size']() + quay_i_13cfd55 * 12
            quay_record_78a80c5 = _name_boundary.attributes(quay_image_b27d478)['read_struct'](quay_ea_f0ab59a, quay_FieldRecord, vm=True, force_reload=True)
            quay_flags_3e8f0d2 = _name_boundary.attributes(quay_record_78a80c5)['Flags']
            quay_type_name_loc_aceb05b = quay_ea_f0ab59a + 4 + _name_boundary.attributes(quay_record_78a80c5)['MangledTypeName']
            quay_name_loc_5f52b02 = quay_ea_f0ab59a + 8 + _name_boundary.attributes(quay_record_78a80c5)['FieldName']
            try:
                quay_name_8c2fb7e = _name_boundary.attributes(quay_image_b27d478)['read_cstr'](quay_name_loc_5f52b02, vm=True)
            except ValueError:
                quay_name_8c2fb7e = ''
            except IndexError:
                quay_name_8c2fb7e = ''
            try:
                quay_type_name_b1c61b3 = _name_boundary.attributes(quay_image_b27d478)['read_cstr'](quay_type_name_loc_aceb05b, vm=True)
            except ValueError:
                quay_type_name_b1c61b3 = ''
            except IndexError:
                quay_type_name_b1c61b3 = ''
            quay_fields_efb2cfe.append(quay_Field(quay_flags_3e8f0d2, quay_type_name_b1c61b3, quay_name_8c2fb7e))
        return quay_cls_d4c45e2(quay_fields_efb2cfe, quay_fd_9f70386)

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_0bbade8', 'args': 'quay_args_786dc49', 'kwargs': 'quay_kwargs_b5d130b'}, 'from_values')
    def quay_from_values(quay_cls_0bbade8, *quay_args_786dc49, **quay_kwargs_b5d130b):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_126b96a'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_126b96a):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_c61e584', 'fields': 'quay_fields_576881f', 'desc': 'quay_desc_b415093'}, '__init__')
    def __init__(quay_self_c61e584, quay_fields_576881f, quay_desc_b415093):
        _name_boundary.attributes(quay_self_c61e584)['fields'] = quay_fields_576881f
        _name_boundary.attributes(quay_self_c61e584)['desc'] = quay_desc_b415093

@_name_boundary.class_contract('SwiftStruct', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'name': 'quay_name', 'field_desc': 'quay_field_desc', 'fields': 'quay_fields'})
class quay_SwiftStruct(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_7201d26', 'objc_image': 'quay_objc_image_5194efd', 'type_location': 'quay_type_location_45dddc1'}, 'from_image')
    def quay_from_image(quay_cls_7201d26, quay_objc_image_5194efd: 'ObjCImage', quay_type_location_45dddc1):
        quay_image_06b7d89 = _name_boundary.attributes(quay_objc_image_5194efd)['image']
        quay_struct_desc_fc8529d = _name_boundary.attributes(quay_image_06b7d89)['read_struct'](quay_type_location_45dddc1, quay_StructDescriptor, vm=True)
        quay_name_1e5ad70 = _name_boundary.attributes(quay_image_06b7d89)['read_cstr'](quay_type_location_45dddc1 + 8 + _name_boundary.attributes(quay_struct_desc_fc8529d)['Name'], vm=True)
        quay_field_desc_7ab19de = _name_boundary.attributes(quay__FieldDescriptor)['from_image'](quay_objc_image_5194efd, quay_type_location_45dddc1 + 4 * 4 + _name_boundary.attributes(quay_struct_desc_fc8529d)['FieldDescriptor'])
        return quay_cls_7201d26(quay_name_1e5ad70, quay_field_desc_7ab19de)

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_348dc7e', 'args': 'quay_args_89f1df6', 'kwargs': 'quay_kwargs_288e24a'}, 'from_values')
    def quay_from_values(quay_cls_348dc7e, *quay_args_89f1df6, **quay_kwargs_288e24a):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_8d326b3'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_8d326b3):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_8c67bc1', 'name': 'quay_name_0d39635', 'field_desc': 'quay_field_desc_ca6591a'}, '__init__')
    def __init__(quay_self_8c67bc1, quay_name_0d39635, quay_field_desc_ca6591a: quay__FieldDescriptor):
        _name_boundary.attributes(quay_self_8c67bc1)['name'] = quay_name_0d39635
        _name_boundary.attributes(quay_self_8c67bc1)['field_desc'] = quay_field_desc_ca6591a
        _name_boundary.attributes(quay_self_8c67bc1)['fields'] = _name_boundary.attributes(quay_field_desc_ca6591a)['fields']

@_name_boundary.class_contract('SwiftClass', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'name': 'quay_name', 'fields': 'quay_fields', 'class_desc': 'quay_class_desc', 'field_desc': 'quay_field_desc', 'ivars': 'quay_ivars'})
class quay_SwiftClass(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_3b56cda', 'image': 'quay_image_fa0e225', 'objc_image': 'quay_objc_image_b782145', 'type_location': 'quay_type_location_7958a9f'}, 'from_image')
    def quay_from_image(quay_cls_3b56cda, quay_image_fa0e225: quay_Image, quay_objc_image_b782145: 'ObjCImage', quay_type_location_7958a9f):
        quay_class_descriptor_18c09fd = _name_boundary.attributes(quay_image_fa0e225)['read_struct'](quay_type_location_7958a9f, quay_ClassDescriptor, vm=True)
        quay_name_9167853 = _name_boundary.attributes(quay_image_fa0e225)['read_cstr'](quay_type_location_7958a9f + 8 + _name_boundary.attributes(quay_class_descriptor_18c09fd)['Name'], vm=True)
        quay_fd_loc_8bf8909 = _name_boundary.attributes(quay_class_descriptor_18c09fd)['FieldDescriptor'] + quay_type_location_7958a9f + 16
        quay_field_descriptor_cc7103b = _name_boundary.attributes(quay__FieldDescriptor)['from_image'](quay_objc_image_b782145, quay_fd_loc_8bf8909)
        quay_ivars_8c59bfe = []
        for quay_objc_class_2dc01fb in _name_boundary.attributes(quay_objc_image_b782145)['classlist']:
            quay_mangled_name_032e2d2 = _name_boundary.attributes(quay_objc_class_2dc01fb)['name']
            quay_project_a66e35c, quay_classname_b2966f8 = quay_demangle(quay_mangled_name_032e2d2)
            if quay_classname_b2966f8 == quay_name_9167853:
                quay_objc_backing_class_f6a9a17: quay_Class = quay_objc_class_2dc01fb
                quay_ivars_8c59bfe = _name_boundary.attributes(quay_objc_backing_class_f6a9a17)['ivars']
                quay_name_9167853 = f'{quay_project_a66e35c}.{quay_name_9167853}'
        return quay_cls_3b56cda(quay_name_9167853, _name_boundary.attributes(quay_field_descriptor_cc7103b)['fields'], quay_class_descriptor_18c09fd, quay_field_descriptor_cc7103b, quay_ivars_8c59bfe)

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_5d552c7', 'args': 'quay_args_533f8e3', 'kwargs': 'quay_kwargs_144fcb9'}, 'from_values')
    def quay_from_values(quay_cls_5d552c7, *quay_args_533f8e3, **quay_kwargs_144fcb9):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_4647e2a'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_4647e2a):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_4b08c32', 'name': 'quay_name_9ba5e6a', 'fields': 'quay_fields_879f79d', 'class_descriptor': 'quay_class_descriptor_17b9fb5', 'field_descriptor': 'quay_field_descriptor_2f75b48', 'ivars': 'quay_ivars_ec01d69'}, '__init__')
    def __init__(quay_self_4b08c32, quay_name_9ba5e6a, quay_fields_879f79d, quay_class_descriptor_17b9fb5=None, quay_field_descriptor_2f75b48=None, quay_ivars_ec01d69=None):
        _name_boundary.attributes(quay_self_4b08c32)['name'] = quay_name_9ba5e6a
        _name_boundary.attributes(quay_self_4b08c32)['fields'] = quay_fields_879f79d
        _name_boundary.attributes(quay_self_4b08c32)['class_desc'] = quay_class_descriptor_17b9fb5
        _name_boundary.attributes(quay_self_4b08c32)['field_desc'] = quay_field_descriptor_2f75b48
        _name_boundary.attributes(quay_self_4b08c32)['ivars'] = quay_ivars_ec01d69

@_name_boundary.class_contract('SwiftEnum', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'name': 'quay_name', 'field_desc': 'quay_field_desc', 'fields': 'quay_fields'})
class quay_SwiftEnum(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_1aaf455', 'objc_image': 'quay_objc_image_5c04634', 'type_location': 'quay_type_location_09038cc'}, 'from_image')
    def quay_from_image(quay_cls_1aaf455, quay_objc_image_5c04634, quay_type_location_09038cc):
        quay_image_67b1c60 = _name_boundary.attributes(quay_objc_image_5c04634)['image']
        quay_enum_descriptor_ac16f39 = _name_boundary.attributes(quay_image_67b1c60)['read_struct'](quay_type_location_09038cc, quay_EnumDescriptor, vm=True)
        quay_name_1c31597 = _name_boundary.attributes(quay_image_67b1c60)['read_cstr'](quay_type_location_09038cc + 8 + _name_boundary.attributes(quay_enum_descriptor_ac16f39)['Name'], vm=True)
        quay_field_desc_b6541ae = None
        if _name_boundary.attributes(quay_enum_descriptor_ac16f39)['FieldDescriptor'] != 0:
            quay_field_desc_b6541ae = _name_boundary.attributes(quay__FieldDescriptor)['from_image'](quay_objc_image_5c04634, quay_type_location_09038cc + 4 * 4 + _name_boundary.attributes(quay_enum_descriptor_ac16f39)['FieldDescriptor'])
        return quay_cls_1aaf455(quay_name_1c31597, quay_field_desc_b6541ae)

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_215e893', 'args': 'quay_args_c3ee8e3', 'kwargs': 'quay_kwargs_193163b'}, 'from_values')
    def quay_from_values(quay_cls_215e893, *quay_args_c3ee8e3, **quay_kwargs_193163b):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_01fbbbd'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_01fbbbd):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_6fd487e', 'name': 'quay_name_50fab0b', 'field_desc': 'quay_field_desc_0640598'}, '__init__')
    def __init__(quay_self_6fd487e, quay_name_50fab0b, quay_field_desc_0640598: quay__FieldDescriptor):
        _name_boundary.attributes(quay_self_6fd487e)['name'] = quay_name_50fab0b
        _name_boundary.attributes(quay_self_6fd487e)['field_desc'] = quay_field_desc_0640598
        _name_boundary.attributes(quay_self_6fd487e)['fields'] = _name_boundary.attributes(quay_field_desc_0640598)['fields'] if _name_boundary.attributes(quay_self_6fd487e)['field_desc'] is not None else []

@_name_boundary.class_contract('SwiftType', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'name': 'quay_name', 'kind': 'quay_kind', 'typedesc': 'quay_typedesc', 'field_desc': 'quay_field_desc'})
class quay_SwiftType(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_e3f162a', 'image': 'quay_image_0d94024', 'objc_image': 'quay_objc_image_c3213f7', 'type_location': 'quay_type_location_ff15e02'}, 'from_image')
    def quay_from_image(quay_cls_e3f162a, quay_image_0d94024: quay_Image, quay_objc_image_c3213f7, quay_type_location_ff15e02):
        quay_kind_9eb444e = quay_ContextDescriptorKind(_name_boundary.attributes(quay_image_0d94024)['read_uint'](quay_type_location_ff15e02, 1, vm=True) & 31)
        if quay_kind_9eb444e == _name_boundary.attributes(quay_ContextDescriptorKind)['Class']:
            return _name_boundary.attributes(quay_SwiftClass)['from_image'](quay_image_0d94024, quay_objc_image_c3213f7, quay_type_location_ff15e02)
        elif quay_kind_9eb444e == _name_boundary.attributes(quay_ContextDescriptorKind)['Struct']:
            return _name_boundary.attributes(quay_SwiftStruct)['from_image'](quay_objc_image_c3213f7, quay_type_location_ff15e02)
        elif quay_kind_9eb444e == quay_ContextDescriptorKind.Enum:
            return _name_boundary.attributes(quay_SwiftEnum)['from_image'](quay_objc_image_c3213f7, quay_type_location_ff15e02)
        else:
            return None

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_8a3dc61', 'args': 'quay_args_b51e1e3', 'kwargs': 'quay_kwargs_cdede1e'}, 'from_values')
    def quay_from_values(quay_cls_8a3dc61, *quay_args_b51e1e3, **quay_kwargs_cdede1e):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_e46646e'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_e46646e):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_244b8ea', 'name': 'quay_name_9488507', 'kind': 'quay_kind_075c936', 'typedesc': 'quay_typedesc_1a43237', 'field_desc': 'quay_field_desc_afe3128'}, '__init__')
    def __init__(quay_self_244b8ea, quay_name_9488507, quay_kind_075c936, quay_typedesc_1a43237=None, quay_field_desc_afe3128=None):
        _name_boundary.attributes(quay_self_244b8ea)['name'] = quay_name_9488507
        _name_boundary.attributes(quay_self_244b8ea)['kind'] = quay_kind_075c936
        _name_boundary.attributes(quay_self_244b8ea)['typedesc'] = quay_typedesc_1a43237
        _name_boundary.attributes(quay_self_244b8ea)['field_desc'] = quay_field_desc_afe3128

@_name_boundary.class_contract('SwiftImage', {'raw_bytes': 'quay_raw_bytes', 'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'types': 'quay_types'})
class quay_SwiftImage(quay_Constructable):

    @_name_boundary.callable_contract({'self': 'quay_self_e4c4c0e'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_e4c4c0e):
        pass

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_007412a', 'objc_image': 'quay_objc_image_cbefe4b'}, 'from_image')
    def quay_from_image(quay_cls_007412a, quay_objc_image_cbefe4b: 'ObjCImage'):
        quay_types_1ee2037: quay_List[quay_SwiftType] = []
        quay_image_08016ab = _name_boundary.attributes(quay_objc_image_cbefe4b)['image']
        quay_swift_type_seg_start_sect_be25907: quay_Section = _name_boundary.attributes(_name_boundary.attributes(quay_image_08016ab)['segments']['__TEXT'])['sections']['__swift5_types']
        for quay_addr_0221ac7 in _name_boundary.attributes(quay_Section)['SectionIterator'](quay_swift_type_seg_start_sect_be25907, vm=True, ptr_size=4):
            quay_type_rel_0243037 = _name_boundary.attributes(quay_image_08016ab)['read_int'](quay_addr_0221ac7, 4)
            quay_type_off_7461d47 = quay_addr_0221ac7 + quay_type_rel_0243037
            quay_types_1ee2037.append(_name_boundary.attributes(quay_SwiftType)['from_image'](quay_image_08016ab, quay_objc_image_cbefe4b, quay_type_off_7461d47))
        return quay_cls_007412a(quay_types_1ee2037)

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_830781f'}, 'from_values')
    def quay_from_values(quay_cls_830781f):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_6b01b30', 'types': 'quay_types_b7b38b4'}, '__init__')
    def __init__(quay_self_6b01b30, quay_types_b7b38b4):
        _name_boundary.attributes(quay_self_6b01b30)['types'] = quay_types_b7b38b4
_name_boundary.module_contract(globals(), {'SwiftImage': 'quay_SwiftImage', 'Section': 'quay_Section', 'uint_to_int': 'quay_uint_to_int', 'Class': 'quay_Class', 'Constructable': 'quay_Constructable', 'SwiftEnum': 'quay_SwiftEnum', 'SwiftStruct': 'quay_SwiftStruct', 'SwiftType': 'quay_SwiftType', 'Image': 'quay_Image', '_FieldDescriptor': 'quay__FieldDescriptor', 'Field': 'quay_Field', 'demangle': 'quay_demangle', 'log': 'quay_log', 'SwiftClass': 'quay_SwiftClass'})
