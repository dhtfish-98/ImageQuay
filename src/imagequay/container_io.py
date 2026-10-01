# Derived from src/ktool/macho.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  macho.py
#
#  This file contains utilities for basic parsing of MachO File headers and such.
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
from enum import Enum as quay_Enum
from io import BytesIO as quay_BytesIO
from typing import Tuple as quay_Tuple, Dict as quay_Dict, Union as quay_Union, BinaryIO as quay_BinaryIO, List as quay_List
from imagequay_layout import *
from imagequay_layout.record_contract import quay_Constructable as quay_Constructable
from imagequay_layout.binary_records import *
from imagequay_layout.command_models import quay_SegmentLoadCommand as quay_SegmentLoadCommand
from imagequay.failure_types import *
from imagequay_support.diagnostics import quay_log as quay_log
from imagequay.formatting import quay_ignore as quay_ignore
quay_mmap = None

@_name_boundary.class_contract('MachOFileType', {})
class quay_MachOFileType(quay_Enum):
    FAT = 0
    THIN = 1

@_name_boundary.class_contract('BackingFile', {'read_bytes': 'quay_read_bytes', 'read_int': 'quay_read_int', 'write': 'quay_write', 'close': 'quay_close', 'fp': 'quay_fp', 'name': 'quay_name', 'file': 'quay_file', 'size': 'quay_size'})
class quay_BackingFile:

    @_name_boundary.callable_contract({'self': 'quay_self_ffe1026', 'fp': 'quay_fp_4dd4c13', 'use_mmaped_io': 'quay_use_mmaped_io_a3c7188'}, '__init__')
    def __init__(quay_self_ffe1026, quay_fp_4dd4c13: quay_Union[quay_BinaryIO, quay_BytesIO], quay_use_mmaped_io_a3c7188=False):
        _name_boundary.attributes(quay_self_ffe1026)['fp'] = quay_fp_4dd4c13
        if isinstance(quay_fp_4dd4c13, quay_BytesIO):
            quay_use_mmaped_io_a3c7188 = False
            assert quay_fp_4dd4c13.getbuffer().nbytes > 0
        if _name_boundary.has_attribute(quay_fp_4dd4c13, 'name'):
            _name_boundary.attributes(quay_self_ffe1026)['name'] = _name_boundary.attributes(quay_os)['path'].basename(_name_boundary.attributes(quay_fp_4dd4c13)['name'])
        else:
            _name_boundary.attributes(quay_self_ffe1026)['name'] = ''
        if quay_use_mmaped_io_a3c7188:
            assert not isinstance(quay_fp_4dd4c13, quay_BytesIO)
            global quay_mmap
            import mmap as quay_mmap
            _name_boundary.attributes(quay_self_ffe1026)['file'] = quay_mmap.mmap(quay_fp_4dd4c13.fileno(), 0, access=quay_mmap.ACCESS_COPY)
            quay_f_66d032c = quay_fp_4dd4c13
            quay_old_file_position_0174b3f = quay_f_66d032c.tell()
            quay_f_66d032c.seek(0, quay_os.SEEK_END)
            _name_boundary.attributes(quay_self_ffe1026)['size'] = quay_f_66d032c.tell()
            quay_f_66d032c.seek(quay_old_file_position_0174b3f)
        if not quay_use_mmaped_io_a3c7188:
            quay_fp_4dd4c13.seek(0)
            quay_data_d2a69ba = _name_boundary.attributes(quay_fp_4dd4c13)['read']()
            _name_boundary.attributes(quay_self_ffe1026)['file'] = bytearray(quay_data_d2a69ba)
            assert len(_name_boundary.attributes(quay_self_ffe1026)['file']) > 0
            _name_boundary.attributes(quay_self_ffe1026)['size'] = len(_name_boundary.attributes(quay_self_ffe1026)['file'])

    @_name_boundary.callable_contract({'self': 'quay_self_1e587c9', 'location': 'quay_location_59737b6', 'count': 'quay_count_6ced326'}, 'read_bytes')
    def quay_read_bytes(quay_self_1e587c9, quay_location_59737b6, quay_count_6ced326):
        return bytes(_name_boundary.attributes(quay_self_1e587c9)['file'][quay_location_59737b6:quay_location_59737b6 + quay_count_6ced326])

    @_name_boundary.callable_contract({'self': 'quay_self_7444e23', 'location': 'quay_location_0f6995c', 'count': 'quay_count_091f77a', 'endian': 'quay_endian_fc2d355'}, 'read_int')
    def quay_read_int(quay_self_7444e23, quay_location_0f6995c, quay_count_091f77a, quay_endian_fc2d355='big'):
        return int.from_bytes(_name_boundary.attributes(quay_self_7444e23)['read_bytes'](quay_location_0f6995c, quay_count_091f77a), quay_endian_fc2d355)

    @_name_boundary.callable_contract({'self': 'quay_self_d543b3f', 'location': 'quay_location_314bf2c', 'data': 'quay_data_1e079bd'}, 'write')
    def quay_write(quay_self_d543b3f, quay_location_314bf2c, quay_data_1e079bd: bytes):
        quay_data_1e079bd = bytearray(quay_data_1e079bd)
        if isinstance(_name_boundary.attributes(quay_self_d543b3f)['file'], bytearray):
            quay_count_0aa26e6 = len(quay_data_1e079bd)
            for quay_i_a0626fd in range(quay_count_0aa26e6):
                _name_boundary.attributes(quay_self_d543b3f)['file'][quay_location_314bf2c + quay_i_a0626fd] = quay_data_1e079bd[quay_i_a0626fd]
        else:
            assert isinstance(_name_boundary.attributes(quay_self_d543b3f)['file'], quay_mmap.mmap)
            _name_boundary.attributes(quay_self_d543b3f)['file'].seek(quay_location_314bf2c)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_d543b3f)['file'])['write'](quay_data_1e079bd)
            _name_boundary.attributes(quay_self_d543b3f)['file'].seek(0)

    @_name_boundary.callable_contract({'self': 'quay_self_453ede4'}, 'close')
    def quay_close(quay_self_453ede4):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_453ede4)['fp'])['close']()

@_name_boundary.class_contract('SlicedBackingFile', {'read_bytes': 'quay_read_bytes', 'read_int': 'quay_read_int', 'write': 'quay_write', 'file': 'quay_file', 'size': 'quay_size', 'name': 'quay_name'})
class quay_SlicedBackingFile:

    @_name_boundary.callable_contract({'self': 'quay_self_32d30cc', 'backing_file': 'quay_backing_file_2881ff3', 'offset': 'quay_offset_ff31dc2', 'size': 'quay_size_20854fc'}, '__init__')
    def __init__(quay_self_32d30cc, quay_backing_file_2881ff3: quay_BackingFile, quay_offset_ff31dc2, quay_size_20854fc):
        _name_boundary.attributes(quay_self_32d30cc)['file'] = bytearray(_name_boundary.attributes(quay_backing_file_2881ff3)['read_bytes'](quay_offset_ff31dc2, quay_size_20854fc))
        _name_boundary.attributes(quay_self_32d30cc)['size'] = quay_size_20854fc
        _name_boundary.attributes(quay_self_32d30cc)['name'] = _name_boundary.attributes(quay_backing_file_2881ff3)['name']

    @_name_boundary.callable_contract({'self': 'quay_self_8037452', 'location': 'quay_location_34b4548', 'count': 'quay_count_8795229'}, 'read_bytes')
    def quay_read_bytes(quay_self_8037452, quay_location_34b4548, quay_count_8795229):
        return bytes(_name_boundary.attributes(quay_self_8037452)['file'][quay_location_34b4548:quay_location_34b4548 + quay_count_8795229])

    @_name_boundary.callable_contract({'self': 'quay_self_741d5f7', 'location': 'quay_location_13e475d', 'count': 'quay_count_bd12226', 'endian': 'quay_endian_3132c30'}, 'read_int')
    def quay_read_int(quay_self_741d5f7, quay_location_13e475d, quay_count_bd12226, quay_endian_3132c30='big'):
        return int.from_bytes(_name_boundary.attributes(quay_self_741d5f7)['read_bytes'](quay_location_13e475d, quay_count_bd12226), quay_endian_3132c30)

    @_name_boundary.callable_contract({'self': 'quay_self_55b1b4d', 'location': 'quay_location_6deef80', 'data': 'quay_data_cad2bbf'}, 'write')
    def quay_write(quay_self_55b1b4d, quay_location_6deef80, quay_data_cad2bbf: bytes):
        quay_count_8c51c26 = len(quay_data_cad2bbf)
        for quay_i_3c3e341 in range(quay_count_8c51c26):
            _name_boundary.attributes(quay_self_55b1b4d)['file'][quay_location_6deef80 + quay_i_3c3e341] = quay_data_cad2bbf[quay_i_3c3e341]

@_name_boundary.class_contract('MachOFile', {'_load_struct': 'quay__load_struct', 'file_object': 'quay_file_object', 'uses_mmaped_io': 'quay_uses_mmaped_io', 'file': 'quay_file', 'slices': 'quay_slices', 'magic': 'quay_magic', 'filename': 'quay_filename', 'type': 'quay_type', 'header': 'quay_header'})
class quay_MachOFile:

    @_name_boundary.callable_contract({'self': 'quay_self_bc2a9ab', 'file': 'quay_file_d168eed', 'use_mmaped_io': 'quay_use_mmaped_io_440cf29'}, '__init__')
    def __init__(quay_self_bc2a9ab, quay_file_d168eed, quay_use_mmaped_io_440cf29=True):
        _name_boundary.attributes(quay_self_bc2a9ab)['file_object'] = quay_file_d168eed
        _name_boundary.attributes(quay_self_bc2a9ab)['uses_mmaped_io'] = quay_use_mmaped_io_440cf29
        if _name_boundary.has_attribute(quay_file_d168eed, 'name'):
            _name_boundary.attributes(quay_self_bc2a9ab)['filename'] = _name_boundary.attributes(quay_os)['path'].basename(_name_boundary.attributes(quay_file_d168eed)['name'])
        else:
            _name_boundary.attributes(quay_self_bc2a9ab)['filename'] = ''
        _name_boundary.attributes(quay_self_bc2a9ab)['file'] = quay_BackingFile(quay_file_d168eed, quay_use_mmaped_io_440cf29)
        _name_boundary.attributes(quay_self_bc2a9ab)['slices'] = []
        _name_boundary.attributes(quay_self_bc2a9ab)['magic'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_bc2a9ab)['file'])['read_int'](0, 4)
        if _name_boundary.attributes(quay_self_bc2a9ab)['magic'] in [quay_FAT_MAGIC, quay_FAT_CIGAM]:
            _name_boundary.attributes(quay_self_bc2a9ab)['type'] = quay_MachOFileType.FAT
        elif _name_boundary.attributes(quay_self_bc2a9ab)['magic'] in [quay_MH_MAGIC, quay_MH_CIGAM, quay_MH_MAGIC_64, quay_MH_CIGAM_64]:
            _name_boundary.attributes(quay_self_bc2a9ab)['type'] = quay_MachOFileType.THIN
        else:
            _name_boundary.attributes(quay_log)['error'](f"Bad Magic: {hex(_name_boundary.attributes(quay_self_bc2a9ab)['magic'])}")
            raise quay_UnsupportedFiletypeException
        if _name_boundary.attributes(quay_self_bc2a9ab)['type'] == quay_MachOFileType.FAT:
            _name_boundary.attributes(quay_self_bc2a9ab)['header']: quay_fat_header = _name_boundary.attributes(quay_self_bc2a9ab)['_load_struct'](0, quay_fat_header, 'big')
            for quay_off_e250ef3 in range(0, _name_boundary.attributes(_name_boundary.attributes(quay_self_bc2a9ab)['header'])['nfat_archs']):
                quay_offset_fe95008 = _name_boundary.attributes(quay_fat_header)['size']() + quay_off_e250ef3 * _name_boundary.attributes(quay_fat_arch)['size']()
                quay_arch_struct_2026045: quay_fat_arch = _name_boundary.attributes(quay_self_bc2a9ab)['_load_struct'](quay_offset_fe95008, quay_fat_arch, 'big')
                if not _name_boundary.attributes(_name_boundary.attributes(quay_self_bc2a9ab)['file'])['read_int'](_name_boundary.attributes(quay_arch_struct_2026045)['offset'], 4) in [quay_MH_MAGIC, quay_MH_CIGAM, quay_MH_MAGIC_64, quay_MH_CIGAM_64]:
                    _name_boundary.attributes(quay_log)['error'](f"Slice {quay_off_e250ef3} has bad magic {hex(_name_boundary.attributes(_name_boundary.attributes(quay_self_bc2a9ab)['file'])['read_int'](_name_boundary.attributes(quay_arch_struct_2026045)['offset'], 4))}")
                    continue
                quay_sliced_backing_file_f3564ab = quay_SlicedBackingFile(_name_boundary.attributes(quay_self_bc2a9ab)['file'], _name_boundary.attributes(quay_arch_struct_2026045)['offset'], _name_boundary.attributes(quay_arch_struct_2026045)['size'])
                _name_boundary.attributes(quay_log)['debug_more'](str(quay_arch_struct_2026045))
                _name_boundary.attributes(quay_self_bc2a9ab)['slices'].append(quay_Slice(quay_self_bc2a9ab, quay_sliced_backing_file_f3564ab, quay_arch_struct_2026045))
        else:
            _name_boundary.attributes(quay_self_bc2a9ab)['slices'].append(quay_Slice(quay_self_bc2a9ab, _name_boundary.attributes(quay_self_bc2a9ab)['file'], None))

    @_name_boundary.callable_contract({'self': 'quay_self_6ff75f5', 'address': 'quay_address_b660ba2', 'struct_type': 'quay_struct_type_a5a5041', 'endian': 'quay_endian_1baadb9'}, '_load_struct')
    def quay__load_struct(quay_self_6ff75f5, quay_address_b660ba2: int, quay_struct_type_a5a5041, quay_endian_1baadb9='little'):
        quay_size_6830994 = _name_boundary.attributes(quay_struct_type_a5a5041)['size']()
        quay_data_a247c79 = _name_boundary.attributes(_name_boundary.attributes(quay_self_6ff75f5)['file'])['read_bytes'](quay_address_b660ba2, quay_size_6830994)
        quay_struct_3a546e1 = _name_boundary.attributes(quay_Struct)['create_with_bytes'](quay_struct_type_a5a5041, quay_data_a247c79, quay_endian_1baadb9)
        _name_boundary.attributes(quay_struct_3a546e1)['off'] = quay_address_b660ba2
        return quay_struct_3a546e1

    @_name_boundary.callable_contract({'self': 'quay_self_e8ea784'}, '__del__')
    def __del__(quay_self_e8ea784):
        if _name_boundary.has_attribute(quay_self_e8ea784, 'file') and _name_boundary.has_attribute(_name_boundary.attributes(quay_self_e8ea784)['file'], 'close'):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ea784)['file'])['close']()

@_name_boundary.class_contract('Section', {'SectionIterator': 'quay_SectionIterator', 'serialize': 'quay_serialize', 'cmd': 'quay_cmd', 'segment': 'quay_segment', 'name': 'quay_name', 'vm_address': 'quay_vm_address', 'file_address': 'quay_file_address', 'size': 'quay_size', 'ptr_size': 'quay_ptr_size', 'start': 'quay_start', 'end': 'quay_end', 'pos': 'quay_pos'})
class quay_Section:
    """

    """

    @_name_boundary.class_contract('SectionIterator', {'ptr_size': 'quay_ptr_size', 'start': 'quay_start', 'end': 'quay_end', 'pos': 'quay_pos'})
    class quay_SectionIterator:

        @_name_boundary.callable_contract({'self': 'quay_self_3af4dc8', 'sect': 'quay_sect_c2028ad', 'vm': 'quay_vm_572d0ea', 'ptr_size': 'quay_ptr_size_9140ea9'}, '__init__')
        def __init__(quay_self_3af4dc8, quay_sect_c2028ad: 'Section', quay_vm_572d0ea=False, quay_ptr_size_9140ea9=8):
            _name_boundary.attributes(quay_self_3af4dc8)['ptr_size'] = quay_ptr_size_9140ea9
            _name_boundary.attributes(quay_self_3af4dc8)['start'] = _name_boundary.attributes(quay_sect_c2028ad)['vm_address'] if quay_vm_572d0ea else _name_boundary.attributes(quay_sect_c2028ad)['file_address']
            _name_boundary.attributes(quay_self_3af4dc8)['end'] = (_name_boundary.attributes(quay_sect_c2028ad)['vm_address'] if quay_vm_572d0ea else _name_boundary.attributes(quay_sect_c2028ad)['file_address']) + _name_boundary.attributes(quay_sect_c2028ad)['size']
            _name_boundary.attributes(quay_self_3af4dc8)['pos'] = _name_boundary.attributes(quay_self_3af4dc8)['start'] - _name_boundary.attributes(quay_self_3af4dc8)['ptr_size']

        @_name_boundary.callable_contract({'self': 'quay_self_6639c8e'}, '__iter__')
        def __iter__(quay_self_6639c8e):
            return quay_self_6639c8e

        @_name_boundary.callable_contract({'self': 'quay_self_66025ed'}, '__next__')
        def __next__(quay_self_66025ed):
            _name_boundary.attributes(quay_self_66025ed)['pos'] += _name_boundary.attributes(quay_self_66025ed)['ptr_size']
            if _name_boundary.attributes(quay_self_66025ed)['pos'] >= _name_boundary.attributes(quay_self_66025ed)['end']:
                _name_boundary.attributes(quay_self_66025ed)['pos'] = _name_boundary.attributes(quay_self_66025ed)['start']
                raise StopIteration
            return _name_boundary.attributes(quay_self_66025ed)['pos']

    @_name_boundary.callable_contract({'self': 'quay_self_15a85cf', 'segment': 'quay_segment_172a553', 'cmd': 'quay_cmd_b474c39', 'ptr_size': 'quay_ptr_size_3803293'}, '__init__')
    def __init__(quay_self_15a85cf, quay_segment_172a553, quay_cmd_b474c39, quay_ptr_size_3803293):
        _name_boundary.attributes(quay_self_15a85cf)['cmd'] = quay_cmd_b474c39
        _name_boundary.attributes(quay_self_15a85cf)['segment'] = quay_segment_172a553
        _name_boundary.attributes(quay_self_15a85cf)['name'] = _name_boundary.attributes(quay_cmd_b474c39)['sectname']
        _name_boundary.attributes(quay_self_15a85cf)['vm_address'] = _name_boundary.attributes(quay_cmd_b474c39)['addr']
        _name_boundary.attributes(quay_self_15a85cf)['file_address'] = _name_boundary.attributes(quay_cmd_b474c39)['offset']
        _name_boundary.attributes(quay_self_15a85cf)['size'] = _name_boundary.attributes(quay_cmd_b474c39)['size']
        _name_boundary.attributes(quay_self_15a85cf)['ptr_size'] = quay_ptr_size_3803293

    @_name_boundary.callable_contract({'self': 'quay_self_9fd69ed'}, '__iter__')
    def __iter__(quay_self_9fd69ed):
        return _name_boundary.attributes(quay_Section)['SectionIterator'](quay_self_9fd69ed, False, _name_boundary.attributes(quay_self_9fd69ed)['ptr_size'])

    @_name_boundary.callable_contract({'self': 'quay_self_d81976a'}, 'serialize')
    def quay_serialize(quay_self_d81976a):
        return {'command': _name_boundary.attributes(_name_boundary.attributes(quay_self_d81976a)['cmd'])['serialize'](), 'name': _name_boundary.attributes(quay_self_d81976a)['name'], 'vm_address': _name_boundary.attributes(quay_self_d81976a)['vm_address'], 'file_address': _name_boundary.attributes(quay_self_d81976a)['file_address'], 'size': _name_boundary.attributes(quay_self_d81976a)['size']}

@_name_boundary.class_contract('Segment', {'serialize': 'quay_serialize', '_process_sections': 'quay__process_sections', 'image': 'quay_image', 'is64': 'quay_is64', 'cmd': 'quay_cmd', 'vm_address': 'quay_vm_address', 'file_address': 'quay_file_address', 'size': 'quay_size', 'file_size': 'quay_file_size', 'name': 'quay_name', 'sections': 'quay_sections', 'type': 'quay_type'})
class quay_Segment:
    """

    """

    @_name_boundary.callable_contract({'self': 'quay_self_f2a36de', 'image': 'quay_image_8ea370c', 'cmd': 'quay_cmd_240a23b'}, '__init__')
    def __init__(quay_self_f2a36de, quay_image_8ea370c, quay_cmd_240a23b):
        _name_boundary.attributes(quay_self_f2a36de)['image'] = quay_image_8ea370c
        _name_boundary.attributes(quay_self_f2a36de)['is64'] = isinstance(quay_cmd_240a23b, quay_segment_command_64)
        _name_boundary.attributes(quay_self_f2a36de)['cmd'] = quay_cmd_240a23b
        _name_boundary.attributes(quay_self_f2a36de)['vm_address'] = _name_boundary.attributes(quay_cmd_240a23b)['vmaddr']
        _name_boundary.attributes(quay_self_f2a36de)['file_address'] = _name_boundary.attributes(quay_cmd_240a23b)['fileoff']
        _name_boundary.attributes(quay_self_f2a36de)['size'] = _name_boundary.attributes(quay_cmd_240a23b)['vmsize']
        _name_boundary.attributes(quay_self_f2a36de)['file_size'] = _name_boundary.attributes(quay_cmd_240a23b)['filesize']
        _name_boundary.attributes(quay_self_f2a36de)['name'] = _name_boundary.attributes(quay_cmd_240a23b)['segname']
        _name_boundary.attributes(quay_self_f2a36de)['sections']: quay_Dict[str, quay_Section] = _name_boundary.attributes(quay_self_f2a36de)['_process_sections']()
        _name_boundary.attributes(quay_self_f2a36de)['type'] = quay_SectionType(quay_S_FLAGS_MASKS.SECTION_TYPE & _name_boundary.attributes(_name_boundary.attributes(quay_self_f2a36de)['cmd'])['flags'])

    @_name_boundary.callable_contract({'self': 'quay_self_f6dc18b'}, '__str__')
    def __str__(quay_self_f6dc18b):
        return f"Segment {_name_boundary.attributes(quay_self_f6dc18b)['name']} at {hex(_name_boundary.attributes(quay_self_f6dc18b)['vm_address'])}\n"

    @_name_boundary.callable_contract({'self': 'quay_self_cd41bb5'}, 'serialize')
    def quay_serialize(quay_self_cd41bb5):
        quay_segment_2865197 = {'command': _name_boundary.attributes(_name_boundary.attributes(quay_self_cd41bb5)['cmd'])['serialize'](), 'name': _name_boundary.attributes(quay_self_cd41bb5)['name'], 'vm_address': _name_boundary.attributes(quay_self_cd41bb5)['vm_address'], 'file_address': _name_boundary.attributes(quay_self_cd41bb5)['file_address'], 'size': _name_boundary.attributes(quay_self_cd41bb5)['size'], 'type': _name_boundary.attributes(_name_boundary.attributes(quay_self_cd41bb5)['type'])['name']}
        quay_sects_9333f21 = {}
        for quay_section_name_3ee6937, quay_sect_871aa98 in _name_boundary.attributes(_name_boundary.attributes(quay_self_cd41bb5)['sections'])['items']():
            quay_sects_9333f21[quay_section_name_3ee6937] = _name_boundary.attributes(quay_sect_871aa98)['serialize']()
        quay_segment_2865197['sections'] = quay_sects_9333f21
        return quay_segment_2865197

    @_name_boundary.callable_contract({'self': 'quay_self_923f315'}, '_process_sections')
    def quay__process_sections(quay_self_923f315) -> quay_Dict[str, quay_Section]:
        quay_sections_2d76d73 = {}
        quay_ea_26e10e7 = _name_boundary.attributes(_name_boundary.attributes(quay_self_923f315)['cmd'])['off'] + _name_boundary.attributes(_name_boundary.attributes(quay_self_923f315)['cmd'])['size']()
        for quay_sect_123d617 in range(0, _name_boundary.attributes(_name_boundary.attributes(quay_self_923f315)['cmd'])['nsects']):
            quay_sect_123d617 = _name_boundary.attributes(_name_boundary.attributes(quay_self_923f315)['image'])['read_struct'](quay_ea_26e10e7, quay_section_64 if _name_boundary.attributes(quay_self_923f315)['is64'] else quay_section)
            quay_sect_123d617 = quay_Section(quay_self_923f315, quay_sect_123d617, 8 if _name_boundary.attributes(quay_self_923f315)['is64'] else 4)
            quay_sections_2d76d73[_name_boundary.attributes(quay_sect_123d617)['name']] = quay_sect_123d617
            quay_ea_26e10e7 += _name_boundary.attributes(quay_section_64)['size']() if _name_boundary.attributes(quay_self_923f315)['is64'] else _name_boundary.attributes(quay_section)['size']()
        return quay_sections_2d76d73

@_name_boundary.class_contract('Slice', {'patch': 'quay_patch', 'full_bytes_for_slice': 'quay_full_bytes_for_slice', 'find': 'quay_find', 'read_struct': 'quay_read_struct', 'read_uint': 'quay_read_uint', 'read_bytearray': 'quay_read_bytearray', 'read_fixed_len_str': 'quay_read_fixed_len_str', 'read_cstr': 'quay_read_cstr', 'read_uleb128': 'quay_read_uleb128', '_load_type': 'quay__load_type', '_load_subtype': 'quay__load_subtype', 'file': 'quay_file', 'macho_file': 'quay_macho_file', 'arch_struct': 'quay_arch_struct', 'ptr_size': 'quay_ptr_size', 'size': 'quay_size', 'byte_order': 'quay_byte_order', '_cstring_cache': 'quay__cstring_cache', 'offset': 'quay_offset', 'type': 'quay_type', 'subtype': 'quay_subtype'})
class quay_Slice:

    @_name_boundary.callable_contract({'self': 'quay_self_3786757', 'macho_file': 'quay_macho_file_9f88f5f', 'sliced_backing_file': 'quay_sliced_backing_file_7cf2941', 'arch_struct': 'quay_arch_struct_8671984', 'offset': 'quay_offset_e658e17'}, '__init__')
    def __init__(quay_self_3786757, quay_macho_file_9f88f5f, quay_sliced_backing_file_7cf2941: quay_Union[quay_BackingFile, quay_SlicedBackingFile], quay_arch_struct_8671984: quay_fat_arch=None, quay_offset_e658e17=0):
        _name_boundary.attributes(quay_self_3786757)['file'] = quay_sliced_backing_file_7cf2941
        _name_boundary.attributes(quay_self_3786757)['macho_file'] = quay_macho_file_9f88f5f
        _name_boundary.attributes(quay_self_3786757)['arch_struct']: quay_fat_arch = quay_arch_struct_8671984
        if _name_boundary.attributes(quay_self_3786757)['arch_struct']:
            _name_boundary.attributes(quay_self_3786757)['offset'] = _name_boundary.attributes(quay_arch_struct_8671984)['offset']
            _name_boundary.attributes(quay_self_3786757)['type'] = _name_boundary.attributes(quay_self_3786757)['_load_type']()
            _name_boundary.attributes(quay_self_3786757)['subtype'] = _name_boundary.attributes(quay_self_3786757)['_load_subtype'](_name_boundary.attributes(quay_self_3786757)['type'])
        else:
            _name_boundary.attributes(quay_self_3786757)['offset'] = quay_offset_e658e17
            quay_hdr_458c89a = _name_boundary.attributes(quay_Struct)['create_with_bytes'](quay_mach_header, _name_boundary.attributes(quay_self_3786757)['read_bytearray'](0, 28))
            _name_boundary.attributes(quay_self_3786757)['arch_struct'] = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_fat_arch, [_name_boundary.attributes(quay_hdr_458c89a)['cpu_type'], _name_boundary.attributes(quay_hdr_458c89a)['cpu_subtype'], 0, 0, 0])
            _name_boundary.attributes(quay_self_3786757)['type'] = _name_boundary.attributes(quay_self_3786757)['_load_type']()
            _name_boundary.attributes(quay_self_3786757)['subtype'] = _name_boundary.attributes(quay_self_3786757)['_load_subtype'](_name_boundary.attributes(quay_self_3786757)['type'])
        _name_boundary.attributes(quay_self_3786757)['ptr_size'] = 8
        if _name_boundary.attributes(quay_self_3786757)['type'] in [quay_CPUType.ARM, quay_CPUType.X86, quay_CPUType.POWERPC, quay_CPUType.ARM6432]:
            _name_boundary.attributes(quay_self_3786757)['ptr_size'] = 4
        _name_boundary.attributes(quay_self_3786757)['size'] = _name_boundary.attributes(quay_sliced_backing_file_7cf2941)['size']
        _name_boundary.attributes(quay_self_3786757)['byte_order'] = 'little' if _name_boundary.attributes(quay_self_3786757)['read_uint'](0, 4, 'little') in [quay_MH_MAGIC, quay_MH_MAGIC_64] else 'big'
        _name_boundary.attributes(quay_self_3786757)['_cstring_cache'] = {}

    @_name_boundary.callable_contract({'self': 'quay_self_e429344', 'address': 'quay_address_6827ce7', 'raw': 'quay_raw_92e0284'}, 'patch')
    def quay_patch(quay_self_e429344, quay_address_6827ce7: int, quay_raw_92e0284: bytes):
        _name_boundary.attributes(quay_log)['debug_tm'](f'Wrote {str(quay_raw_92e0284)} @ {quay_address_6827ce7}')
        _name_boundary.attributes(_name_boundary.attributes(quay_self_e429344)['file'])['write'](quay_address_6827ce7, quay_raw_92e0284)
        assert _name_boundary.attributes(_name_boundary.attributes(quay_self_e429344)['file'])['read_bytes'](quay_address_6827ce7, len(quay_raw_92e0284)) == quay_raw_92e0284

    @_name_boundary.callable_contract({'self': 'quay_self_0347e04'}, 'full_bytes_for_slice')
    def quay_full_bytes_for_slice(quay_self_0347e04):
        return bytes(_name_boundary.attributes(_name_boundary.attributes(quay_self_0347e04)['file'])['read_bytes'](0, _name_boundary.attributes(_name_boundary.attributes(quay_self_0347e04)['file'])['size']))

    @_name_boundary.callable_contract({'self': 'quay_self_322df66', 'pattern': 'quay_pattern_776bbf7'}, 'find')
    def quay_find(quay_self_322df66, quay_pattern_776bbf7: quay_Union[str, bytes]):
        if isinstance(quay_pattern_776bbf7, str):
            quay_pattern_776bbf7 = quay_pattern_776bbf7.encode('utf-8')
        return _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_322df66)['file'])['file'])['find'](quay_pattern_776bbf7)

    @_name_boundary.callable_contract({'self': 'quay_self_784a9cd', 'addr': 'quay_addr_49dc7dc', 'struct_type': 'quay_struct_type_bc46523', 'endian': 'quay_endian_cac4ef5'}, 'read_struct')
    def quay_read_struct(quay_self_784a9cd, quay_addr_49dc7dc: int, quay_struct_type_bc46523, quay_endian_cac4ef5='little'):
        quay_size_6548557 = _name_boundary.attributes(quay_struct_type_bc46523)['size'](_name_boundary.attributes(quay_self_784a9cd)['ptr_size'])
        quay_data_dc8690d = _name_boundary.attributes(quay_self_784a9cd)['read_bytearray'](quay_addr_49dc7dc, quay_size_6548557)
        quay_struct_f2adddd = _name_boundary.attributes(quay_Struct)['create_with_bytes'](quay_struct_type_bc46523, quay_data_dc8690d, quay_endian_cac4ef5, ptr_size=_name_boundary.attributes(quay_self_784a9cd)['ptr_size'])
        _name_boundary.attributes(quay_struct_f2adddd)['off'] = quay_addr_49dc7dc
        return quay_struct_f2adddd

    @_name_boundary.callable_contract({'self': 'quay_self_f36cbe0', 'addr': 'quay_addr_9d28cd2', 'count': 'quay_count_285d1e1', 'endian': 'quay_endian_90c2b4b'}, 'read_uint')
    def quay_read_uint(quay_self_f36cbe0, quay_addr_9d28cd2: int, quay_count_285d1e1: int, quay_endian_90c2b4b='little'):
        return int.from_bytes(_name_boundary.attributes(_name_boundary.attributes(quay_self_f36cbe0)['file'])['read_bytes'](quay_addr_9d28cd2, quay_count_285d1e1), quay_endian_90c2b4b)

    @_name_boundary.callable_contract({'self': 'quay_self_5eb3d4a', 'addr': 'quay_addr_9489637', 'count': 'quay_count_211a267'}, 'read_bytearray')
    def quay_read_bytearray(quay_self_5eb3d4a, quay_addr_9489637: int, quay_count_211a267: int):
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_5eb3d4a)['file'])['read_bytes'](quay_addr_9489637, quay_count_211a267)

    @_name_boundary.callable_contract({'self': 'quay_self_1abf42d', 'addr': 'quay_addr_9b4b2e0', 'count': 'quay_count_1668c75', 'force': 'quay_force_5d6bc90'}, 'read_fixed_len_str')
    def quay_read_fixed_len_str(quay_self_1abf42d, quay_addr_9b4b2e0: int, quay_count_1668c75: int, quay_force_5d6bc90=False) -> str:
        if quay_force_5d6bc90:
            quay_data_e3be36c = _name_boundary.attributes(_name_boundary.attributes(quay_self_1abf42d)['file'])['file'][quay_addr_9b4b2e0:quay_addr_9b4b2e0 + quay_count_1668c75]
            quay_string_25c1487 = ''
            for quay_ch_8a06b54 in quay_data_e3be36c:
                try:
                    quay_string_25c1487 += bytes(quay_ch_8a06b54).decode()
                except UnicodeDecodeError:
                    quay_string_25c1487 += '?'
            return quay_string_25c1487
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_1abf42d)['file'])['file'][quay_addr_9b4b2e0:quay_addr_9b4b2e0 + quay_count_1668c75].decode().rstrip('\x00')

    @_name_boundary.callable_contract({'self': 'quay_self_5409111', 'addr': 'quay_addr_911a019', 'limit': 'quay_limit_7fe519c'}, 'read_cstr')
    def quay_read_cstr(quay_self_5409111, quay_addr_911a019: int, quay_limit_7fe519c: int=0):
        quay_ea_e758af4 = quay_addr_911a019
        if quay_addr_911a019 in _name_boundary.attributes(quay_self_5409111)['_cstring_cache']:
            return _name_boundary.attributes(quay_self_5409111)['_cstring_cache'][quay_addr_911a019]
        quay_count_cd466f9 = 0
        while True:
            if _name_boundary.attributes(_name_boundary.attributes(quay_self_5409111)['file'])['file'][quay_ea_e758af4] != 0:
                quay_count_cd466f9 += 1
                quay_ea_e758af4 += 1
            else:
                break
        quay_text_3a4bed7 = _name_boundary.attributes(quay_self_5409111)['read_fixed_len_str'](quay_addr_911a019, quay_count_cd466f9)
        _name_boundary.attributes(quay_self_5409111)['_cstring_cache'][quay_addr_911a019] = quay_text_3a4bed7
        return quay_text_3a4bed7

    @_name_boundary.callable_contract({'self': 'quay_self_af0fc29', 'read_head': 'quay_read_head_9a617bd'}, 'read_uleb128')
    def quay_read_uleb128(quay_self_af0fc29, quay_read_head_9a617bd: int) -> quay_Tuple[int, int]:
        quay_value_02d9787 = 0
        quay_shift_200c908 = 0
        while True:
            quay_byte_f4c3836 = _name_boundary.attributes(quay_self_af0fc29)['read_uint'](quay_read_head_9a617bd, 1)
            quay_value_02d9787 |= (quay_byte_f4c3836 & 127) << quay_shift_200c908
            quay_read_head_9a617bd += 1
            quay_shift_200c908 += 7
            if quay_byte_f4c3836 & 128 == 0:
                break
        return (quay_value_02d9787, quay_read_head_9a617bd)

    @_name_boundary.callable_contract({'self': 'quay_self_b52cb56'}, '_load_type')
    def quay__load_type(quay_self_b52cb56) -> quay_CPUType:
        quay_cpu_type_823a4bd = _name_boundary.attributes(_name_boundary.attributes(quay_self_b52cb56)['arch_struct'])['cpu_type']
        return quay_CPUType(quay_cpu_type_823a4bd)

    @_name_boundary.callable_contract({'self': 'quay_self_7a0fd3d', 'cputype': 'quay_cputype_3ade690'}, '_load_subtype')
    def quay__load_subtype(quay_self_7a0fd3d, quay_cputype_3ade690: quay_CPUType):
        quay_cpu_subtype_aafa94b = _name_boundary.attributes(_name_boundary.attributes(quay_self_7a0fd3d)['arch_struct'])['cpu_subtype']
        quay_cpu_subtype_aafa94b = quay_cpu_subtype_aafa94b & 65535
        try:
            quay_sub_4888f94 = quay_CPU_SUBTYPES[quay_cputype_3ade690]
            return quay_sub_4888f94(quay_cpu_subtype_aafa94b)
        except KeyError:
            _name_boundary.attributes(quay_log)['error'](f"Unknown CPU SubType ({hex(quay_cpu_subtype_aafa94b)}) ({_name_boundary.attributes(quay_self_7a0fd3d)['arch_struct']}). File an issue at https://github.com/cxnder/imagequay")
            return quay_CPUSubTypeARM64.ALL

@_name_boundary.class_contract('MachOImageHeader', {'MachOLoadCommandIterator': 'quay_MachOLoadCommandIterator', 'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'serialize': 'quay_serialize', 'raw_bytes': 'quay_raw_bytes', 'insert_load_command': 'quay_insert_load_command', 'remove_load_command': 'quay_remove_load_command', 'replace_load_command': 'quay_replace_load_command', 'is64': 'quay_is64', 'dyld_header': 'quay_dyld_header', 'filetype': 'quay_filetype', 'flags': 'quay_flags', 'load_commands': 'quay_load_commands', 'raw': 'quay_raw', 'pos': 'quay_pos', 'hdr': 'quay_hdr'})
class quay_MachOImageHeader(quay_Constructable):

    @_name_boundary.class_contract('MachOLoadCommandIterator', {'pos': 'quay_pos', 'hdr': 'quay_hdr'})
    class quay_MachOLoadCommandIterator:

        @_name_boundary.callable_contract({'self': 'quay_self_a31c5b7', 'hdr': 'quay_hdr_0ccb95f'}, '__init__')
        def __init__(quay_self_a31c5b7, quay_hdr_0ccb95f: 'MachOImageHeader'):
            _name_boundary.attributes(quay_self_a31c5b7)['pos'] = -1
            _name_boundary.attributes(quay_self_a31c5b7)['hdr'] = quay_hdr_0ccb95f

        @_name_boundary.callable_contract({'self': 'quay_self_5404370'}, '__iter__')
        def __iter__(quay_self_5404370):
            return quay_self_5404370

        @_name_boundary.callable_contract({'self': 'quay_self_c3e4415'}, '__next__')
        def __next__(quay_self_c3e4415):
            _name_boundary.attributes(quay_self_c3e4415)['pos'] += 1
            if _name_boundary.attributes(quay_self_c3e4415)['pos'] >= len(_name_boundary.attributes(_name_boundary.attributes(quay_self_c3e4415)['hdr'])['load_commands']):
                _name_boundary.attributes(quay_self_c3e4415)['pos'] = -1
                raise StopIteration
            return _name_boundary.attributes(_name_boundary.attributes(quay_self_c3e4415)['hdr'])['load_commands'][_name_boundary.attributes(quay_self_c3e4415)['pos']]
    "\n    This class represents the Mach-O Header\n    It contains the basic header info along with all load commands within it.\n\n    It doesn't handle complex abstraction logic, it simply loads in the load commands as their raw structs\n    "

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_1de6d88', 'macho_slice': 'quay_macho_slice_8aaa6cb', 'offset': 'quay_offset_64d864b'}, 'from_image')
    def quay_from_image(quay_cls_1de6d88, quay_macho_slice_8aaa6cb, quay_offset_64d864b=0) -> 'ImageHeader':
        quay_image_header_851502a = quay_cls_1de6d88()
        quay_header_20b9e32: quay_mach_header = _name_boundary.attributes(quay_macho_slice_8aaa6cb)['read_struct'](quay_offset_64d864b, quay_mach_header)
        if _name_boundary.attributes(quay_header_20b9e32)['magic'] == quay_MH_MAGIC_64:
            quay_header_20b9e32: quay_mach_header_64 = _name_boundary.attributes(quay_macho_slice_8aaa6cb)['read_struct'](quay_offset_64d864b, quay_mach_header_64)
            _name_boundary.attributes(quay_image_header_851502a)['is64'] = True
        quay_raw_6b63ba5 = _name_boundary.attributes(quay_header_20b9e32)['raw']
        _name_boundary.attributes(quay_image_header_851502a)['filetype'] = quay_MH_FILETYPE(_name_boundary.attributes(quay_header_20b9e32)['filetype'])
        for quay_flag_831a4e2 in quay_MH_FLAGS:
            if _name_boundary.attributes(quay_header_20b9e32)['flags'] & _name_boundary.attributes(quay_flag_831a4e2)['value']:
                _name_boundary.attributes(quay_image_header_851502a)['flags'].append(quay_flag_831a4e2)
        quay_offset_64d864b += _name_boundary.attributes(quay_header_20b9e32)['size']()
        quay_load_commands_1ea0cb1 = []
        for quay_i_6599e37 in range(1, _name_boundary.attributes(quay_header_20b9e32)['loadcnt'] + 1):
            quay_cmd_e2a0c79 = _name_boundary.attributes(quay_macho_slice_8aaa6cb)['read_uint'](quay_offset_64d864b, 4)
            quay_cmd_size_366d4ef = _name_boundary.attributes(quay_macho_slice_8aaa6cb)['read_uint'](quay_offset_64d864b + 4, 4)
            quay_cmd_raw_58851d6 = _name_boundary.attributes(quay_macho_slice_8aaa6cb)['read_bytearray'](quay_offset_64d864b, quay_cmd_size_366d4ef)
            try:
                quay_load_cmd_e316e99 = _name_boundary.attributes(quay_Struct)['create_with_bytes'](quay_LOAD_COMMAND_MAP[quay_LOAD_COMMAND(quay_cmd_e2a0c79)], quay_cmd_raw_58851d6)
                _name_boundary.attributes(quay_load_cmd_e316e99)['off'] = quay_offset_64d864b
            except ValueError as quay_ex_3fa4cb6:
                if not _name_boundary.attributes(quay_ignore)['MALFORMED']:
                    _name_boundary.attributes(quay_log)['error'](f'Bad Load Command at {hex(quay_offset_64d864b)} index {quay_i_6599e37 - 1}\n        {hex(quay_cmd_e2a0c79)} - {hex(quay_cmd_size_366d4ef)}')
                quay_unk_lc_ccca959 = _name_boundary.attributes(quay_macho_slice_8aaa6cb)['read_struct'](quay_offset_64d864b, quay_unk_command)
                quay_load_cmd_e316e99 = quay_unk_lc_ccca959
            except KeyError as quay_ex_3fa4cb6:
                if not _name_boundary.attributes(quay_ignore)['MALFORMED']:
                    _name_boundary.attributes(quay_log)['error']()
                    _name_boundary.attributes(quay_log)['error'](f"Load Command {str(quay_LOAD_COMMAND(quay_cmd_e2a0c79))} doesn't have a mapped struct type")
                    _name_boundary.attributes(quay_log)['error']('*Please* file an issue on the github @ https://github.com/cxnder/imagequay')
                    _name_boundary.attributes(quay_log)['error']()
                    _name_boundary.attributes(quay_log)['error'](f'Run with the -f flag to hide this warning.')
                    _name_boundary.attributes(quay_log)['error']()
                quay_unk_lc_ccca959 = _name_boundary.attributes(quay_macho_slice_8aaa6cb)['read_struct'](quay_offset_64d864b, quay_unk_command)
                quay_load_cmd_e316e99 = quay_unk_lc_ccca959
            quay_load_commands_1ea0cb1.append(quay_load_cmd_e316e99)
            quay_raw_6b63ba5 += quay_cmd_raw_58851d6
            quay_offset_64d864b += _name_boundary.attributes(quay_load_cmd_e316e99)['cmdsize']
        _name_boundary.attributes(quay_image_header_851502a)['raw'] = quay_raw_6b63ba5
        _name_boundary.attributes(quay_image_header_851502a)['dyld_header'] = quay_header_20b9e32
        _name_boundary.attributes(quay_image_header_851502a)['load_commands'] = quay_load_commands_1ea0cb1
        return quay_image_header_851502a

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_9dc19a7', 'is_64': 'quay_is_64_10784af', 'cpu_type': 'quay_cpu_type_7f5b3ff', 'cpu_subtype': 'quay_cpu_subtype_4ba9e8a', 'filetype': 'quay_filetype_f5b1f55', 'flags': 'quay_flags_d1cd2a5', 'load_commands': 'quay_load_commands_c53cd59'}, 'from_values')
    def quay_from_values(quay_cls_9dc19a7, quay_is_64_10784af: bool, quay_cpu_type_7f5b3ff, quay_cpu_subtype_4ba9e8a, quay_filetype_f5b1f55: quay_MH_FILETYPE, quay_flags_d1cd2a5: quay_List[quay_MH_FLAGS], quay_load_commands_c53cd59: quay_List):
        if isinstance(quay_cpu_type_7f5b3ff, int):
            quay_cpu_type_7f5b3ff = quay_CPUType(quay_cpu_type_7f5b3ff)
        if isinstance(quay_cpu_subtype_4ba9e8a, int):
            quay_cpu_subtype_4ba9e8a = quay_CPU_SUBTYPES[quay_cpu_type_7f5b3ff](quay_cpu_subtype_4ba9e8a)
        if isinstance(quay_filetype_f5b1f55, int):
            quay_filetype_f5b1f55 = quay_MH_FILETYPE(quay_filetype_f5b1f55)
        quay_image_header_4c48653 = quay_cls_9dc19a7()
        quay_struct_type_8543304 = quay_mach_header_64 if quay_is_64_10784af else quay_mach_header
        quay_full_load_cmds_raw_5b1bf0a = bytearray()
        quay_lcs_71ab354 = []
        quay_lc_count_ac530b1 = 0
        quay_off_4670b3c = _name_boundary.attributes(quay_struct_type_8543304)['size']()
        for quay_lc_96c3b92 in quay_load_commands_c53cd59:
            if issubclass(quay_lc_96c3b92.__class__, quay_Struct):
                assert len(_name_boundary.attributes(quay_lc_96c3b92)['raw']) == _name_boundary.attributes(quay_lc_96c3b92.__class__)['size']()
                assert _name_boundary.has_attribute(quay_lc_96c3b92, 'cmdsize')
                _name_boundary.attributes(quay_lc_96c3b92)['off'] = quay_off_4670b3c
                quay_lcs_71ab354.append(quay_lc_96c3b92)
                quay_full_load_cmds_raw_5b1bf0a += bytearray(_name_boundary.attributes(quay_lc_96c3b92)['raw'])
                quay_lc_count_ac530b1 += 1
                quay_off_4670b3c += _name_boundary.attributes(quay_lc_96c3b92)['cmdsize']
            elif isinstance(quay_lc_96c3b92, bytes) or isinstance(quay_lc_96c3b92, bytearray):
                quay_full_load_cmds_raw_5b1bf0a += bytearray(quay_lc_96c3b92)
            elif isinstance(quay_lc_96c3b92, quay_Segment) or isinstance(quay_lc_96c3b92, quay_SegmentLoadCommand):
                _name_boundary.attributes(_name_boundary.attributes(quay_lc_96c3b92)['cmd'])['off'] = quay_off_4670b3c
                quay_lcs_71ab354.append(_name_boundary.attributes(quay_lc_96c3b92)['cmd'])
                quay_dat_da63b48 = bytearray(_name_boundary.attributes(_name_boundary.attributes(quay_lc_96c3b92)['cmd'])['raw'])
                quay_lc_count_ac530b1 += 1
                for quay_sect_0bd3d0e in _name_boundary.attributes(quay_lc_96c3b92)['sections'].values():
                    quay_dat_da63b48 += _name_boundary.attributes(_name_boundary.attributes(quay_sect_0bd3d0e)['cmd'])['raw']
                assert len(quay_dat_da63b48) == _name_boundary.attributes(_name_boundary.attributes(quay_lc_96c3b92)['cmd'])['cmdsize'], f"{_name_boundary.attributes(quay_lc_96c3b92)['cmd']}, \n[{','.join([str(_name_boundary.attributes(quay_i_da864ef)['cmd']) for quay_i_da864ef in _name_boundary.attributes(quay_lc_96c3b92)['sections'].values()])}]"
                quay_full_load_cmds_raw_5b1bf0a += quay_dat_da63b48
                quay_off_4670b3c += _name_boundary.attributes(_name_boundary.attributes(quay_lc_96c3b92)['cmd'])['cmdsize']
        quay_embedded_flag_dc19307 = 0
        for quay_flag_2f8af22 in quay_flags_d1cd2a5:
            quay_embedded_flag_dc19307 |= _name_boundary.attributes(quay_flag_2f8af22)['value']
        if quay_is_64_10784af:
            quay_header_2b95ef7 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_struct_type_8543304, [quay_MH_MAGIC_64, _name_boundary.attributes(quay_cpu_type_7f5b3ff)['value'], _name_boundary.attributes(quay_cpu_subtype_4ba9e8a)['value'], _name_boundary.attributes(quay_filetype_f5b1f55)['value'], quay_lc_count_ac530b1, len(quay_full_load_cmds_raw_5b1bf0a), quay_embedded_flag_dc19307, 0])
        else:
            quay_header_2b95ef7 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_struct_type_8543304, [quay_MH_MAGIC, _name_boundary.attributes(quay_cpu_type_7f5b3ff)['value'], _name_boundary.attributes(quay_cpu_subtype_4ba9e8a)['value'], _name_boundary.attributes(quay_filetype_f5b1f55)['value'], quay_lc_count_ac530b1, len(quay_full_load_cmds_raw_5b1bf0a), quay_embedded_flag_dc19307])
        _name_boundary.attributes(quay_image_header_4c48653)['dyld_header'] = quay_header_2b95ef7
        _name_boundary.attributes(quay_image_header_4c48653)['filetype'] = quay_MH_FILETYPE(_name_boundary.attributes(quay_header_2b95ef7)['filetype'])
        for quay_flag_2f8af22 in quay_MH_FLAGS:
            if _name_boundary.attributes(quay_header_2b95ef7)['flags'] & _name_boundary.attributes(quay_flag_2f8af22)['value']:
                _name_boundary.attributes(quay_image_header_4c48653)['flags'].append(quay_flag_2f8af22)
        _name_boundary.attributes(quay_image_header_4c48653)['load_commands'] = quay_lcs_71ab354
        _name_boundary.attributes(quay_image_header_4c48653)['raw'] = bytearray(_name_boundary.attributes(quay_header_2b95ef7)['raw']) + quay_full_load_cmds_raw_5b1bf0a
        return quay_image_header_4c48653

    @_name_boundary.callable_contract({'self': 'quay_self_8193e7e'}, '__str__')
    def __str__(quay_self_8193e7e):
        return f"MachO Header - 64 bit VM: {_name_boundary.attributes(quay_self_8193e7e)['is64']} | File Type: {_name_boundary.attributes(quay_self_8193e7e)['filetype']} | Flags: {_name_boundary.attributes(quay_self_8193e7e)['flags']} | Load Cmd Count: {len(_name_boundary.attributes(quay_self_8193e7e)['load_commands'])}"

    @_name_boundary.callable_contract({'self': 'quay_self_b4651cc'}, '__init__')
    def __init__(quay_self_b4651cc):
        _name_boundary.attributes(quay_self_b4651cc)['is64'] = False
        _name_boundary.attributes(quay_self_b4651cc)['dyld_header']: quay_Union[quay_mach_header, quay_mach_header_64, None] = None
        _name_boundary.attributes(quay_self_b4651cc)['filetype'] = quay_MH_FILETYPE(0)
        _name_boundary.attributes(quay_self_b4651cc)['flags']: quay_List[quay_MH_FLAGS] = []
        _name_boundary.attributes(quay_self_b4651cc)['load_commands'] = []
        _name_boundary.attributes(quay_self_b4651cc)['raw'] = bytearray()

    @_name_boundary.callable_contract({'self': 'quay_self_1d54c91'}, '__iter__')
    def __iter__(quay_self_1d54c91):
        return _name_boundary.attributes(quay_MachOImageHeader)['MachOLoadCommandIterator'](quay_self_1d54c91)

    @_name_boundary.callable_contract({'self': 'quay_self_d2974b3'}, 'serialize')
    def quay_serialize(quay_self_d2974b3):
        return {'filetype': _name_boundary.attributes(_name_boundary.attributes(quay_self_d2974b3)['filetype'])['name'], 'flags': [_name_boundary.attributes(quay_flag_22431de)['name'] for quay_flag_22431de in _name_boundary.attributes(quay_self_d2974b3)['flags']], 'is_64_bit': _name_boundary.attributes(quay_self_d2974b3)['is64'], 'dyld_header': _name_boundary.attributes(_name_boundary.attributes(quay_self_d2974b3)['dyld_header'])['serialize'](), 'load_commands': [_name_boundary.attributes(quay_cmd_5e3be30)['serialize']() for quay_cmd_5e3be30 in _name_boundary.attributes(quay_self_d2974b3)['load_commands']]}

    @_name_boundary.callable_contract({'self': 'quay_self_26e368c'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_26e368c) -> bytes:
        return _name_boundary.attributes(quay_self_26e368c)['raw']

    @_name_boundary.callable_contract({'self': 'quay_self_7a75c5c', 'load_command': 'quay_load_command_db70d71', 'index': 'quay_index_112037e', 'suffix': 'quay_suffix_857f27e'}, 'insert_load_command')
    def quay_insert_load_command(quay_self_7a75c5c, quay_load_command_db70d71, quay_index_112037e=-1, quay_suffix_857f27e=None):
        quay_image_header_ea831a3 = quay_self_7a75c5c
        quay_flags_18c5591 = _name_boundary.attributes(quay_image_header_ea831a3)['flags']
        quay_filetype_65f9add = _name_boundary.attributes(quay_image_header_ea831a3)['filetype']
        quay_cpu_type_cfdedb1 = _name_boundary.attributes(_name_boundary.attributes(quay_self_7a75c5c)['dyld_header'])['cpu_type']
        quay_cpu_subtype_3476364 = _name_boundary.attributes(_name_boundary.attributes(quay_self_7a75c5c)['dyld_header'])['cpu_subtype']
        quay_load_command_items_770859b = []
        quay_current_lc_index_fcfb3b7 = 0
        for quay_command_34e63e5 in _name_boundary.attributes(quay_self_7a75c5c)['load_commands']:
            if quay_current_lc_index_fcfb3b7 == quay_index_112037e:
                if isinstance(quay_load_command_db70d71, quay_SegmentLoadCommand):
                    quay_load_command_items_770859b.append(quay_load_command_db70d71)
                elif quay_load_command_db70d71.__class__ in [quay_dylib_command, quay_rpath_command]:
                    assert quay_suffix_857f27e is not None, 'Inserting dylib_command requires suffix'
                    quay_encoded_c241f3d = quay_suffix_857f27e.encode('utf-8') + b'\x00'
                    while (len(quay_encoded_c241f3d) + _name_boundary.attributes(quay_load_command_db70d71.__class__)['size']()) % 8 != 0:
                        quay_encoded_c241f3d += b'\x00'
                    quay_cmdsize_ad3cfe5 = _name_boundary.attributes(quay_load_command_db70d71.__class__)['size']() + len(quay_encoded_c241f3d)
                    _name_boundary.attributes(quay_load_command_db70d71)['cmdsize'] = quay_cmdsize_ad3cfe5
                    quay_load_command_items_770859b.append(quay_load_command_db70d71)
                    quay_load_command_items_770859b.append(quay_encoded_c241f3d)
                elif quay_load_command_db70d71.__class__ in [quay_dylinker_command, quay_build_version_command]:
                    quay_load_command_items_770859b.append(quay_load_command_db70d71)
                    assert quay_suffix_857f27e is not None, f"Inserting {_name_boundary.attributes(quay_load_command_db70d71.__class__)['__name__']} currently requires a byte suffix "
                    quay_load_command_items_770859b.append(quay_suffix_857f27e)
            if isinstance(quay_command_34e63e5, quay_segment_command) or isinstance(quay_command_34e63e5, quay_segment_command_64):
                quay_sects_3536a90 = []
                quay_sect_data_988e212 = _name_boundary.attributes(quay_self_7a75c5c)['raw'][_name_boundary.attributes(quay_command_34e63e5)['off'] + _name_boundary.attributes(quay_command_34e63e5.__class__)['size']():]
                quay_struct_class_597b2fe = quay_section_64 if isinstance(quay_command_34e63e5, quay_segment_command_64) else quay_section
                for quay_i_056246a in range(_name_boundary.attributes(quay_command_34e63e5)['nsects']):
                    quay_sects_3536a90.append(quay_Section(None, _name_boundary.attributes(quay_Struct)['create_with_bytes'](quay_struct_class_597b2fe, quay_sect_data_988e212[quay_i_056246a * _name_boundary.attributes(quay_struct_class_597b2fe)['size']():(quay_i_056246a + 1) * _name_boundary.attributes(quay_struct_class_597b2fe)['size']()], 'little'), 8 if _name_boundary.attributes(quay_self_7a75c5c)['is64'] else 4))
                quay_seg_a934559 = _name_boundary.attributes(quay_SegmentLoadCommand)['from_values'](isinstance(quay_command_34e63e5, quay_segment_command_64), _name_boundary.attributes(quay_command_34e63e5)['segname'], _name_boundary.attributes(quay_command_34e63e5)['vmaddr'], _name_boundary.attributes(quay_command_34e63e5)['vmsize'], _name_boundary.attributes(quay_command_34e63e5)['fileoff'], _name_boundary.attributes(quay_command_34e63e5)['filesize'], _name_boundary.attributes(quay_command_34e63e5)['maxprot'], _name_boundary.attributes(quay_command_34e63e5)['initprot'], _name_boundary.attributes(quay_command_34e63e5)['flags'], quay_sects_3536a90)
                quay_load_command_items_770859b.append(quay_seg_a934559)
            elif quay_command_34e63e5.__class__ in [quay_dylib_command, quay_rpath_command]:
                quay__suffix_be62664 = ''
                quay_i_056246a = 0
                while _name_boundary.attributes(quay_self_7a75c5c)['raw'][_name_boundary.attributes(quay_command_34e63e5)['off'] + _name_boundary.attributes(quay_command_34e63e5.__class__)['size']() + quay_i_056246a] != 0:
                    quay__suffix_be62664 += chr(_name_boundary.attributes(quay_self_7a75c5c)['raw'][_name_boundary.attributes(quay_command_34e63e5)['off'] + _name_boundary.attributes(quay_command_34e63e5.__class__)['size']() + quay_i_056246a])
                    quay_i_056246a += 1
                quay_encoded_c241f3d = quay__suffix_be62664.encode('utf-8') + b'\x00'
                while (len(quay_encoded_c241f3d) + _name_boundary.attributes(quay_command_34e63e5.__class__)['size']()) % 8 != 0:
                    quay_encoded_c241f3d += b'\x00'
                quay_load_command_items_770859b.append(quay_command_34e63e5)
                quay_load_command_items_770859b.append(quay_encoded_c241f3d)
            elif quay_command_34e63e5.__class__ in [quay_dylinker_command, quay_build_version_command]:
                quay_load_command_items_770859b.append(quay_command_34e63e5)
                quay_actual_size_21e0433 = _name_boundary.attributes(quay_command_34e63e5)['cmdsize']
                quay_dat_87a3edf = _name_boundary.attributes(quay_self_7a75c5c)['raw'][_name_boundary.attributes(quay_command_34e63e5)['off'] + _name_boundary.attributes(quay_command_34e63e5)['size']():_name_boundary.attributes(quay_command_34e63e5)['off'] + _name_boundary.attributes(quay_command_34e63e5)['size']() + quay_actual_size_21e0433 - _name_boundary.attributes(quay_command_34e63e5)['size']()]
                quay_load_command_items_770859b.append(quay_dat_87a3edf)
            else:
                quay_load_command_items_770859b.append(quay_command_34e63e5)
            quay_current_lc_index_fcfb3b7 += 1
        if quay_index_112037e == -1:
            if isinstance(quay_load_command_db70d71, quay_SegmentLoadCommand):
                quay_load_command_items_770859b.append(quay_load_command_db70d71)
            elif quay_load_command_db70d71.__class__ in [quay_dylib_command, quay_rpath_command]:
                quay_load_command_items_770859b.append(quay_load_command_db70d71)
                assert quay_suffix_857f27e is not None, f"Inserting {_name_boundary.attributes(quay_load_command_db70d71.__class__)['__name__']} requires suffix"
                quay_encoded_c241f3d = quay_suffix_857f27e.encode('utf-8') + b'\x00'
                while (len(quay_encoded_c241f3d) + _name_boundary.attributes(quay_load_command_db70d71.__class__)['size']()) % 8 != 0:
                    quay_encoded_c241f3d += b'\x00'
                quay_cmdsize_ad3cfe5 = _name_boundary.attributes(quay_load_command_db70d71.__class__)['size']() + len(quay_encoded_c241f3d)
                _name_boundary.attributes(quay_load_command_db70d71)['cmdsize'] = quay_cmdsize_ad3cfe5
                quay_load_command_items_770859b.append(quay_encoded_c241f3d)
            elif quay_load_command_db70d71.__class__ in [quay_dylinker_command, quay_build_version_command]:
                quay_load_command_items_770859b.append(quay_load_command_db70d71)
                assert quay_suffix_857f27e is not None, f"Inserting {_name_boundary.attributes(quay_load_command_db70d71.__class__)['__name__']} currently requires a byte suffix"
                quay_load_command_items_770859b.append(quay_suffix_857f27e)
        return _name_boundary.attributes(quay_MachOImageHeader)['from_values'](_name_boundary.attributes(quay_self_7a75c5c)['is64'], quay_cpu_type_cfdedb1, quay_cpu_subtype_3476364, quay_filetype_65f9add, quay_flags_18c5591, quay_load_command_items_770859b)

    @_name_boundary.callable_contract({'self': 'quay_self_096aae3', 'index': 'quay_index_584668e'}, 'remove_load_command')
    def quay_remove_load_command(quay_self_096aae3, quay_index_584668e):
        quay_image_header_cd78cd6 = quay_self_096aae3
        quay_flags_2f1e336 = _name_boundary.attributes(quay_image_header_cd78cd6)['flags']
        quay_filetype_28630c9 = _name_boundary.attributes(quay_image_header_cd78cd6)['filetype']
        quay_cpu_type_7612cd6 = _name_boundary.attributes(_name_boundary.attributes(quay_self_096aae3)['dyld_header'])['cpu_type']
        quay_cpu_subtype_88afe24 = _name_boundary.attributes(_name_boundary.attributes(quay_self_096aae3)['dyld_header'])['cpu_subtype']
        quay_load_command_items_0bf7b58 = []
        quay_current_lc_index_1b984ee = 0
        for quay_command_5c06aaa in _name_boundary.attributes(quay_self_096aae3)['load_commands']:
            if quay_current_lc_index_1b984ee == quay_index_584668e:
                quay_current_lc_index_1b984ee += 1
                continue
            if isinstance(quay_command_5c06aaa, quay_segment_command) or isinstance(quay_command_5c06aaa, quay_segment_command_64):
                quay_sects_78c509f = []
                quay_sect_data_982116f = _name_boundary.attributes(quay_self_096aae3)['raw'][_name_boundary.attributes(quay_command_5c06aaa)['off'] + _name_boundary.attributes(quay_command_5c06aaa.__class__)['size']():]
                quay_struct_class_38541f1 = quay_section_64 if isinstance(quay_command_5c06aaa, quay_segment_command_64) else quay_section
                for quay_i_66af36b in range(_name_boundary.attributes(quay_command_5c06aaa)['nsects']):
                    quay_sects_78c509f.append(quay_Section(None, _name_boundary.attributes(quay_Struct)['create_with_bytes'](quay_struct_class_38541f1, quay_sect_data_982116f[quay_i_66af36b * _name_boundary.attributes(quay_struct_class_38541f1)['size']():(quay_i_66af36b + 1) * _name_boundary.attributes(quay_struct_class_38541f1)['size']()], 'little'), 8 if _name_boundary.attributes(quay_self_096aae3)['is64'] else 4))
                quay_seg_2b4d73a = _name_boundary.attributes(quay_SegmentLoadCommand)['from_values'](isinstance(quay_command_5c06aaa, quay_segment_command_64), _name_boundary.attributes(quay_command_5c06aaa)['segname'], _name_boundary.attributes(quay_command_5c06aaa)['vmaddr'], _name_boundary.attributes(quay_command_5c06aaa)['vmsize'], _name_boundary.attributes(quay_command_5c06aaa)['fileoff'], _name_boundary.attributes(quay_command_5c06aaa)['filesize'], _name_boundary.attributes(quay_command_5c06aaa)['maxprot'], _name_boundary.attributes(quay_command_5c06aaa)['initprot'], _name_boundary.attributes(quay_command_5c06aaa)['flags'], quay_sects_78c509f)
                quay_load_command_items_0bf7b58.append(quay_seg_2b4d73a)
            elif quay_command_5c06aaa.__class__ in [quay_dylib_command, quay_rpath_command]:
                quay_suffix_2246a4f = ''
                quay_i_66af36b = 0
                while _name_boundary.attributes(quay_self_096aae3)['raw'][_name_boundary.attributes(quay_command_5c06aaa)['off'] + _name_boundary.attributes(quay_command_5c06aaa.__class__)['size']() + quay_i_66af36b] != 0:
                    quay_suffix_2246a4f += chr(_name_boundary.attributes(quay_self_096aae3)['raw'][_name_boundary.attributes(quay_command_5c06aaa)['off'] + _name_boundary.attributes(quay_command_5c06aaa.__class__)['size']() + quay_i_66af36b])
                    quay_i_66af36b += 1
                quay_encoded_be13ec3 = quay_suffix_2246a4f.encode('utf-8') + b'\x00'
                while (len(quay_encoded_be13ec3) + _name_boundary.attributes(quay_command_5c06aaa.__class__)['size']()) % 8 != 0:
                    quay_encoded_be13ec3 += b'\x00'
                quay_load_command_items_0bf7b58.append(quay_command_5c06aaa)
                quay_load_command_items_0bf7b58.append(quay_encoded_be13ec3)
            elif quay_command_5c06aaa.__class__ in [quay_dylinker_command, quay_build_version_command]:
                quay_load_command_items_0bf7b58.append(quay_command_5c06aaa)
                quay_actual_size_6466909 = _name_boundary.attributes(quay_command_5c06aaa)['cmdsize']
                quay_dat_3ed2abe = _name_boundary.attributes(quay_self_096aae3)['raw'][_name_boundary.attributes(quay_command_5c06aaa)['off'] + _name_boundary.attributes(quay_command_5c06aaa)['size']():_name_boundary.attributes(quay_command_5c06aaa)['off'] + _name_boundary.attributes(quay_command_5c06aaa)['size']() + quay_actual_size_6466909 - _name_boundary.attributes(quay_command_5c06aaa)['size']()]
                quay_load_command_items_0bf7b58.append(quay_dat_3ed2abe)
            else:
                quay_load_command_items_0bf7b58.append(quay_command_5c06aaa)
            quay_current_lc_index_1b984ee += 1
        return _name_boundary.attributes(quay_MachOImageHeader)['from_values'](_name_boundary.attributes(quay_self_096aae3)['is64'], quay_cpu_type_7612cd6, quay_cpu_subtype_88afe24, quay_filetype_28630c9, quay_flags_2f1e336, quay_load_command_items_0bf7b58)

    @_name_boundary.callable_contract({'self': 'quay_self_39cc3dc', 'load_command': 'quay_load_command_8d51eaa', 'index': 'quay_index_668fddf', 'suffix': 'quay_suffix_d087619'}, 'replace_load_command')
    def quay_replace_load_command(quay_self_39cc3dc, quay_load_command_8d51eaa, quay_index_668fddf=-1, quay_suffix_d087619=None):
        quay_image_header_5159a37 = quay_self_39cc3dc
        quay_flags_0472ec8 = _name_boundary.attributes(quay_image_header_5159a37)['flags']
        quay_filetype_e47ea95 = _name_boundary.attributes(quay_image_header_5159a37)['filetype']
        quay_cpu_type_8577895 = _name_boundary.attributes(_name_boundary.attributes(quay_self_39cc3dc)['dyld_header'])['cpu_type']
        quay_cpu_subtype_7fcf0ab = _name_boundary.attributes(_name_boundary.attributes(quay_self_39cc3dc)['dyld_header'])['cpu_subtype']
        quay_load_command_items_ab00754 = []
        quay_current_lc_index_26f619e = 0
        for quay_command_82fbef7 in _name_boundary.attributes(quay_self_39cc3dc)['load_commands']:
            if quay_current_lc_index_26f619e == quay_index_668fddf:
                if isinstance(quay_load_command_8d51eaa, quay_SegmentLoadCommand):
                    quay_load_command_items_ab00754.append(quay_load_command_8d51eaa)
                elif quay_load_command_8d51eaa.__class__ in [quay_dylib_command, quay_rpath_command]:
                    assert quay_suffix_d087619 is not None, 'Inserting dylib_command requires suffix'
                    quay_encoded_65110be = quay_suffix_d087619.encode('utf-8') + b'\x00'
                    while (len(quay_encoded_65110be) + _name_boundary.attributes(quay_load_command_8d51eaa.__class__)['size']()) % 8 != 0:
                        quay_encoded_65110be += b'\x00'
                    quay_cmdsize_6c845ca = _name_boundary.attributes(quay_load_command_8d51eaa.__class__)['size']() + len(quay_encoded_65110be)
                    _name_boundary.attributes(quay_load_command_8d51eaa)['cmdsize'] = quay_cmdsize_6c845ca
                    quay_load_command_items_ab00754.append(quay_load_command_8d51eaa)
                    quay_load_command_items_ab00754.append(quay_encoded_65110be)
                elif quay_load_command_8d51eaa.__class__ in [quay_dylinker_command, quay_build_version_command]:
                    quay_load_command_items_ab00754.append(quay_load_command_8d51eaa)
                    assert quay_suffix_d087619 is not None, f"Inserting {_name_boundary.attributes(quay_load_command_8d51eaa.__class__)['__name__']} currently requires a byte suffix "
                    quay_load_command_items_ab00754.append(quay_suffix_d087619)
                quay_current_lc_index_26f619e += 1
                continue
            if isinstance(quay_command_82fbef7, quay_segment_command) or isinstance(quay_command_82fbef7, quay_segment_command_64):
                quay_sects_e5535b5 = []
                quay_sect_data_fd98733 = _name_boundary.attributes(quay_self_39cc3dc)['raw'][_name_boundary.attributes(quay_command_82fbef7)['off'] + _name_boundary.attributes(quay_command_82fbef7.__class__)['size']():]
                quay_struct_class_1b51fe6 = quay_section_64 if isinstance(quay_command_82fbef7, quay_segment_command_64) else quay_section
                for quay_i_7210ae8 in range(_name_boundary.attributes(quay_command_82fbef7)['nsects']):
                    quay_sects_e5535b5.append(quay_Section(None, _name_boundary.attributes(quay_Struct)['create_with_bytes'](quay_struct_class_1b51fe6, quay_sect_data_fd98733[quay_i_7210ae8 * _name_boundary.attributes(quay_struct_class_1b51fe6)['size']():(quay_i_7210ae8 + 1) * _name_boundary.attributes(quay_struct_class_1b51fe6)['size']()], 'little'), 8 if _name_boundary.attributes(quay_self_39cc3dc)['is64'] else 4))
                quay_seg_93e5595 = _name_boundary.attributes(quay_SegmentLoadCommand)['from_values'](isinstance(quay_command_82fbef7, quay_segment_command_64), _name_boundary.attributes(quay_command_82fbef7)['segname'], _name_boundary.attributes(quay_command_82fbef7)['vmaddr'], _name_boundary.attributes(quay_command_82fbef7)['vmsize'], _name_boundary.attributes(quay_command_82fbef7)['fileoff'], _name_boundary.attributes(quay_command_82fbef7)['filesize'], _name_boundary.attributes(quay_command_82fbef7)['maxprot'], _name_boundary.attributes(quay_command_82fbef7)['initprot'], _name_boundary.attributes(quay_command_82fbef7)['flags'], quay_sects_e5535b5)
                quay_load_command_items_ab00754.append(quay_seg_93e5595)
            elif quay_command_82fbef7.__class__ in [quay_dylib_command, quay_rpath_command]:
                quay__suffix_3e03d8e = ''
                quay_i_7210ae8 = 0
                while _name_boundary.attributes(quay_self_39cc3dc)['raw'][_name_boundary.attributes(quay_command_82fbef7)['off'] + _name_boundary.attributes(quay_command_82fbef7.__class__)['size']() + quay_i_7210ae8] != 0:
                    quay__suffix_3e03d8e += chr(_name_boundary.attributes(quay_self_39cc3dc)['raw'][_name_boundary.attributes(quay_command_82fbef7)['off'] + _name_boundary.attributes(quay_command_82fbef7.__class__)['size']() + quay_i_7210ae8])
                    quay_i_7210ae8 += 1
                quay_encoded_65110be = quay__suffix_3e03d8e.encode('utf-8') + b'\x00'
                while (len(quay_encoded_65110be) + _name_boundary.attributes(quay_command_82fbef7.__class__)['size']()) % 8 != 0:
                    quay_encoded_65110be += b'\x00'
                quay_load_command_items_ab00754.append(quay_command_82fbef7)
                quay_load_command_items_ab00754.append(quay_encoded_65110be)
            elif quay_command_82fbef7.__class__ in [quay_dylinker_command, quay_build_version_command]:
                quay_load_command_items_ab00754.append(quay_command_82fbef7)
                quay_actual_size_f0a2249 = _name_boundary.attributes(quay_command_82fbef7)['cmdsize']
                quay_dat_ba1a963 = _name_boundary.attributes(quay_self_39cc3dc)['raw'][_name_boundary.attributes(quay_command_82fbef7)['off'] + _name_boundary.attributes(quay_command_82fbef7)['size']():_name_boundary.attributes(quay_command_82fbef7)['off'] + _name_boundary.attributes(quay_command_82fbef7)['size']() + quay_actual_size_f0a2249 - _name_boundary.attributes(quay_command_82fbef7)['size']()]
                quay_load_command_items_ab00754.append(quay_dat_ba1a963)
            else:
                quay_load_command_items_ab00754.append(quay_command_82fbef7)
            quay_current_lc_index_26f619e += 1
        if quay_index_668fddf == -1:
            if isinstance(quay_load_command_8d51eaa, quay_SegmentLoadCommand):
                quay_load_command_items_ab00754.append(quay_load_command_8d51eaa)
            elif quay_load_command_8d51eaa.__class__ in [quay_dylib_command, quay_rpath_command]:
                quay_load_command_items_ab00754.append(quay_load_command_8d51eaa)
                assert quay_suffix_d087619 is not None, 'Inserting dylib_command requires suffix'
                quay_encoded_65110be = quay_suffix_d087619.encode('utf-8') + b'\x00'
                while (len(quay_encoded_65110be) + _name_boundary.attributes(quay_load_command_8d51eaa.__class__)['size']()) % 8 != 0:
                    quay_encoded_65110be += b'\x00'
                quay_cmdsize_6c845ca = _name_boundary.attributes(quay_load_command_8d51eaa.__class__)['size']() + len(quay_encoded_65110be)
                _name_boundary.attributes(quay_load_command_8d51eaa)['cmdsize'] = quay_cmdsize_6c845ca
                quay_load_command_items_ab00754.append(quay_encoded_65110be)
            elif quay_load_command_8d51eaa.__class__ in [quay_dylinker_command, quay_build_version_command]:
                quay_load_command_items_ab00754.append(quay_load_command_8d51eaa)
                assert quay_suffix_d087619 is not None, f"Inserting {_name_boundary.attributes(quay_load_command_8d51eaa.__class__)['__name__']} currently requires a byte suffix"
                quay_load_command_items_ab00754.append(quay_suffix_d087619)
        return _name_boundary.attributes(quay_MachOImageHeader)['from_values'](_name_boundary.attributes(quay_self_39cc3dc)['is64'], quay_cpu_type_8577895, quay_cpu_subtype_7fcf0ab, quay_filetype_e47ea95, quay_flags_0472ec8, quay_load_command_items_ab00754)

@_name_boundary.class_contract('PlatformType', {})
class quay_PlatformType(quay_Enum):
    MACOS = 1
    IOS = 2
    TVOS = 3
    WATCHOS = 4
    BRIDGE_OS = 5
    MAC_CATALYST = 6
    IOS_SIMULATOR = 7
    TVOS_SIMULATOR = 8
    WATCHOS_SIMULATOR = 9
    DRIVER_KIT = 10
    UNK = 64

@_name_boundary.class_contract('ToolType', {})
class quay_ToolType(quay_Enum):
    CLANG = 1
    SWIFT = 2
    LD = 3
_name_boundary.module_contract(globals(), {'os': 'quay_os', 'ToolType': 'quay_ToolType', 'Tuple': 'quay_Tuple', 'MachOFileType': 'quay_MachOFileType', 'mmap': 'quay_mmap', 'Union': 'quay_Union', 'ignore': 'quay_ignore', 'BackingFile': 'quay_BackingFile', 'MachOImageHeader': 'quay_MachOImageHeader', 'BytesIO': 'quay_BytesIO', 'PlatformType': 'quay_PlatformType', 'Section': 'quay_Section', 'Constructable': 'quay_Constructable', 'BinaryIO': 'quay_BinaryIO', 'Slice': 'quay_Slice', 'SlicedBackingFile': 'quay_SlicedBackingFile', 'Enum': 'quay_Enum', 'List': 'quay_List', 'SegmentLoadCommand': 'quay_SegmentLoadCommand', 'Dict': 'quay_Dict', 'Segment': 'quay_Segment', 'MachOFile': 'quay_MachOFile', 'log': 'quay_log'})
