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

@_name_boundary.class_contract('FatMachOGenerator', {'_fat_arch_for_slice':'quay__fat_arch_for_slice', 'slices':'quay_slices', 'fat_archs':'quay_fat_archs', 'fat_head':'quay_fat_head'})
class quay_FatMachOGenerator:
    """Plan finite, nonoverlapping FAT32 output without loading dyld/ObjC metadata."""
    def __init__(self, slices):
        from imagequay.container_io import MAX_INPUT_BYTES, MAX_ARCHITECTURES
        from imagequay.failure_types import quay_MalformedMachOException
        self.slices = list(slices)
        if not 1 <= len(self.slices) <= MAX_ARCHITECTURES:
            raise quay_MalformedMachOException('combine needs between 1 and 4096 slices')
        table_size = quay_fat_header.size() + len(self.slices) * quay_fat_arch.size()
        cursor, identities = table_size, set()
        self.fat_archs = []
        for value in self.slices:
            record = self.quay__fat_arch_for_slice(value, self.fat_archs[-1] if self.fat_archs else None)
            alignment = 1 << record.align
            offset = (cursor + alignment - 1) // alignment * alignment
            identity = (record.cpu_type, record.cpu_subtype)
            if identity in identities:
                raise quay_MalformedMachOException('combine contains a duplicate architecture identity')
            identities.add(identity)
            if offset > MAX_INPUT_BYTES or record.size > MAX_INPUT_BYTES - offset:
                raise quay_MalformedMachOException('combined container exceeds the 1 GiB budget')
            record = quay_fat_arch_for_slice(value, record.cpu_type, record.cpu_subtype, offset, record.size, record.align)
            self.fat_archs.append(record)
            cursor = offset + record.size
        self.fat_head = bytearray(quay_Struct.create_with_values(quay_fat_header, [b'\xca\xfe\xba\xbe', len(self.fat_archs)], 'big').raw)
        for record in self.fat_archs:
            self.fat_head.extend(quay_Struct.create_with_values(quay_fat_arch, [record.cpu_type, record.cpu_subtype, record.offset, record.size, record.align], 'big').raw)

    @staticmethod
    def quay__fat_arch_for_slice(fat_slice, previous_fat_arch=None):
        from imagequay.container_io import quay_MachOImageHeader, MAX_INPUT_BYTES
        from imagequay.failure_types import quay_MalformedMachOException
        header = quay_MachOImageHeader.from_image(fat_slice).dyld_header
        if fat_slice.arch_struct and len(fat_slice.macho_file.slices) > 1:
            directive = fat_slice.arch_struct.align
        else:
            directive = 14 if header.cpu_type == 0x0100000c else 12
        if not 0 <= directive <= 30:
            raise quay_MalformedMachOException('fat alignment exponent exceeds its supported width')
        alignment = 1 << directive
        cursor = previous_fat_arch.offset + previous_fat_arch.size if previous_fat_arch else alignment
        offset = (cursor + alignment - 1) // alignment * alignment
        if fat_slice.size > MAX_INPUT_BYTES - offset:
            raise quay_MalformedMachOException('combined container exceeds the 1 GiB budget')
        return quay_fat_arch_for_slice(fat_slice, header.cpu_type, header.cpu_subtype, offset, fat_slice.size, directive)

_name_boundary.module_contract(globals(), {'os': 'quay_os', 'fat_arch_for_slice': 'quay_fat_arch_for_slice', 'Image': 'quay_Image', 'TBDGenerator': 'quay_TBDGenerator', 'MachOImageLoader': 'quay_MachOImageLoader', 'Slice': 'quay_Slice', 'namedtuple': 'quay_namedtuple', 'SymbolType': 'quay_SymbolType', 'FatMachOGenerator': 'quay_FatMachOGenerator', 'log': 'quay_log', 'ObjCImage': 'quay_ObjCImage'})
