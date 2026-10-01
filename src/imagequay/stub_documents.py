# Derived from src/ktool/generator.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  generator.py
#
#  Holds some miscellaneous generators for certain filetypes
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary
import os as quay_os
from collections import namedtuple as quay_namedtuple
from imagequay_layout.binary_records import *
from imagequay_support.diagnostics import quay_log as quay_log
from imagequay.metadata_reader import quay_MachOImageLoader as quay_MachOImageLoader, quay_SymbolType as quay_SymbolType, quay_Image as quay_Image
from imagequay.container_io import quay_Slice as quay_Slice
from imagequay.objc_model import quay_ObjCImage as quay_ObjCImage

@_name_boundary.class_contract('TBDGenerator', {'_generate_dict': 'quay__generate_dict', 'image': 'quay_image', 'objc_lib': 'quay_objc_lib', 'general': 'quay_general', 'dict': 'quay_dict'})
class quay_TBDGenerator:

    @_name_boundary.callable_contract({'self': 'quay_self_771d608', 'image': 'quay_image_f96c357', 'general': 'quay_general_7fe3cb5', 'objc_lib': 'quay_objc_lib_6f90991'}, '__init__')
    def __init__(quay_self_771d608, quay_image_f96c357: quay_Image, quay_general_7fe3cb5=True, quay_objc_lib_6f90991: quay_ObjCImage=None):
        """
        The TBD Generator is a generator that creates TAPI formatted text based stubs for libraries.

        It is currently fairly incomplete, although its output should still be perfectly functional in an SDK.

        After processing, its .dict attribute can be dumped by a TAPI YAML serializer (located in imagequay.util) to
            produce a functional .tbd

        :param image: image being processed
        :type image: image
        :param general: Should the generator create a .tbd for usage in SDKs?
        :type general: bool
        :param objc_lib: Pass an objc image to the generator. If none is passed it will generate its own
        """
        _name_boundary.attributes(quay_self_771d608)['image'] = quay_image_f96c357
        _name_boundary.attributes(quay_self_771d608)['objc_lib'] = quay_objc_lib_6f90991
        _name_boundary.attributes(quay_self_771d608)['general'] = quay_general_7fe3cb5
        _name_boundary.attributes(quay_self_771d608)['dict'] = _name_boundary.attributes(quay_self_771d608)['_generate_dict']()

    @_name_boundary.callable_contract({'self': 'quay_self_ee0cd73'}, '_generate_dict')
    def quay__generate_dict(quay_self_ee0cd73):
        """
        This function simply parses through the image and creates the tbd dict

        :return: The text-based-stub dictionary representation
        """
        quay_tbd_c82693e = {}
        if _name_boundary.attributes(quay_self_ee0cd73)['general']:
            quay_tbd_c82693e['archs'] = ['armv7', 'armv7s', 'arm64', 'arm64e']
            quay_tbd_c82693e['platform'] = '(null)'
            quay_tbd_c82693e['install-name'] = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_ee0cd73)['image'])['dylib'])['install_name']
            quay_tbd_c82693e['current-version'] = 1
            quay_tbd_c82693e['compatibility-version'] = 1
            quay_export_dict_31775d4 = {'archs': ['armv7', 'armv7s', 'arm64', 'arm64e']}
            if len(_name_boundary.attributes(_name_boundary.attributes(quay_self_ee0cd73)['image'])['allowed_clients']) > 0:
                quay_export_dict_31775d4['allowed-clients'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_ee0cd73)['image'])['allowed_clients']
            quay_symbols_353e6b6 = []
            quay_classes_3cbf8ba = []
            quay_ivars_5d3bd8a = []
            for quay_sym_27d18db in _name_boundary.attributes(_name_boundary.attributes(quay_self_ee0cd73)['image'])['exports']:
                if _name_boundary.attributes(quay_sym_27d18db)['dec_type'] == quay_SymbolType.FUNC:
                    quay_symbols_353e6b6.append(_name_boundary.attributes(quay_sym_27d18db)['name'])
                elif _name_boundary.attributes(quay_sym_27d18db)['dec_type'] == quay_SymbolType.CLASS:
                    quay_classes_3cbf8ba.append(_name_boundary.attributes(quay_sym_27d18db)['name'])
                elif _name_boundary.attributes(quay_sym_27d18db)['dec_type'] == quay_SymbolType.IVAR:
                    quay_ivars_5d3bd8a.append(_name_boundary.attributes(quay_sym_27d18db)['name'])
            quay_export_dict_31775d4['symbols'] = quay_symbols_353e6b6
            quay_export_dict_31775d4['objc-classes'] = quay_classes_3cbf8ba
            quay_export_dict_31775d4['objc-ivars'] = quay_ivars_5d3bd8a
            quay_tbd_c82693e['exports'] = [quay_export_dict_31775d4]
        return quay_tbd_c82693e
quay_fat_arch_for_slice = _name_boundary.named_record('fat_arch_for_slice', ['slice', 'cpu_type', 'cpu_subtype', 'offset', 'size', 'align'])

@_name_boundary.class_contract('FatMachOGenerator', {'_fat_arch_for_slice': 'quay__fat_arch_for_slice', 'slices': 'quay_slices', 'fat_archs': 'quay_fat_archs', 'fat_head': 'quay_fat_head'})
class quay_FatMachOGenerator:
    """

    """

    @_name_boundary.callable_contract({'self': 'quay_self_fc5a100', 'slices': 'quay_slices_dc083b8'}, '__init__')
    def __init__(quay_self_fc5a100, quay_slices_dc083b8):
        _name_boundary.attributes(quay_self_fc5a100)['slices'] = quay_slices_dc083b8
        _name_boundary.attributes(quay_self_fc5a100)['fat_archs'] = []
        quay_pfa_4b192c3 = None
        for quay_fat_slice_c3ba167 in quay_slices_dc083b8:
            quay_fat_arch_item_12c8fe5 = _name_boundary.attributes(quay_self_fc5a100)['_fat_arch_for_slice'](quay_fat_slice_c3ba167, quay_pfa_4b192c3)
            quay_pfa_4b192c3 = quay_fat_arch_item_12c8fe5
            _name_boundary.attributes(quay_self_fc5a100)['fat_archs'].append(quay_fat_arch_item_12c8fe5)
        quay_fat_head_4af1920 = bytearray()
        quay_fh_d834bb9 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_fat_header, [b'\xca\xfe\xba\xbe', len(_name_boundary.attributes(quay_self_fc5a100)['fat_archs'])], 'big')
        quay_fat_head_4af1920 += _name_boundary.attributes(quay_fh_d834bb9)['raw']
        for quay_fat_arch_item_12c8fe5 in _name_boundary.attributes(quay_self_fc5a100)['fat_archs']:
            quay_fa_cddcb14 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_fat_arch, [_name_boundary.attributes(quay_fat_arch_item_12c8fe5)['cpu_type'], _name_boundary.attributes(quay_fat_arch_item_12c8fe5)['cpu_subtype'], _name_boundary.attributes(quay_fat_arch_item_12c8fe5)['offset'], _name_boundary.attributes(quay_fat_arch_item_12c8fe5)['size'], _name_boundary.attributes(quay_fat_arch_item_12c8fe5)['align']], 'big')
            quay_fat_head_4af1920 += _name_boundary.attributes(quay_fa_cddcb14)['raw']
        _name_boundary.attributes(quay_self_fc5a100)['fat_head'] = quay_fat_head_4af1920

    @staticmethod
    @_name_boundary.callable_contract({'fat_slice': 'quay_fat_slice_2c10be2', 'previous_fat_arch': 'quay_previous_fat_arch_67a42c7'}, '_fat_arch_for_slice')
    def quay__fat_arch_for_slice(quay_fat_slice_2c10be2: quay_Slice, quay_previous_fat_arch_67a42c7: quay_fat_arch_for_slice) -> quay_fat_arch_for_slice:
        """
        :param fat_slice: Fat slice
        :type fat_slice: Slice
        :param previous_fat_arch: Previous item returned by this func, or None if first.
        :type previous_fat_arch: fat_arch_for_slice
        :return: fat_arch_for_slice item.
        :rtype: fat_arch_for_slice
        """
        quay_lib_a426049 = _name_boundary.attributes(quay_MachOImageLoader)['load'](quay_fat_slice_2c10be2)
        quay_cpu_type_8ef5b30 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_lib_a426049)['macho_header'])['dyld_header'])['cpu_type']
        quay_cpu_subtype_982bd50 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_lib_a426049)['macho_header'])['dyld_header'])['cpu_subtype']
        if len(_name_boundary.attributes(_name_boundary.attributes(quay_fat_slice_2c10be2)['macho_file'])['slices']) > 1:
            quay_size_b85527b = _name_boundary.attributes(_name_boundary.attributes(quay_fat_slice_2c10be2)['arch_struct'])['size']
            quay_align_c20f8a6 = pow(2, _name_boundary.attributes(_name_boundary.attributes(quay_fat_slice_2c10be2)['arch_struct'])['align'])
            quay_align_directive_853b578 = _name_boundary.attributes(_name_boundary.attributes(quay_fat_slice_2c10be2)['arch_struct'])['align']
        else:
            quay_f_3b19b39 = _name_boundary.attributes(_name_boundary.attributes(quay_fat_slice_2c10be2)['macho_file'])['file_object']
            quay_old_file_position_5d3ca6d = quay_f_3b19b39.tell()
            quay_f_3b19b39.seek(0, quay_os.SEEK_END)
            quay_size_b85527b = quay_f_3b19b39.tell()
            quay_f_3b19b39.seek(quay_old_file_position_5d3ca6d, quay_os.SEEK_SET)
            if quay_cpu_type_8ef5b30 == 16777228:
                quay_align_c20f8a6 = pow(2, 14)
                quay_align_directive_853b578 = 14
            elif quay_cpu_type_8ef5b30 == 16777223:
                quay_align_c20f8a6 = pow(2, 12)
                quay_align_directive_853b578 = 12
            else:
                print(quay_cpu_type_8ef5b30)
                raise AssertionError('not yet implemented')
        if quay_previous_fat_arch_67a42c7 is None:
            quay_offset_079c0f8 = quay_align_c20f8a6
        else:
            quay_offset_079c0f8 = 0
            while True:
                quay_offset_079c0f8 += quay_align_c20f8a6
                if quay_offset_079c0f8 > _name_boundary.attributes(quay_previous_fat_arch_67a42c7)['offset'] + _name_boundary.attributes(quay_previous_fat_arch_67a42c7)['size']:
                    break
        _name_boundary.attributes(quay_log)['debug'](f'Create arch with offset {hex(quay_offset_079c0f8)} and size {hex(quay_size_b85527b)}')
        return quay_fat_arch_for_slice(quay_fat_slice_2c10be2, quay_cpu_type_8ef5b30, quay_cpu_subtype_982bd50, quay_offset_079c0f8, quay_size_b85527b, quay_align_directive_853b578)
_name_boundary.module_contract(globals(), {'os': 'quay_os', 'fat_arch_for_slice': 'quay_fat_arch_for_slice', 'Image': 'quay_Image', 'TBDGenerator': 'quay_TBDGenerator', 'MachOImageLoader': 'quay_MachOImageLoader', 'Slice': 'quay_Slice', 'namedtuple': 'quay_namedtuple', 'SymbolType': 'quay_SymbolType', 'FatMachOGenerator': 'quay_FatMachOGenerator', 'log': 'quay_log', 'ObjCImage': 'quay_ObjCImage'})
