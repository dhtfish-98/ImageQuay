# Derived from src/ktool_macho/load_commands.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  load_commands.py
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
from typing import Union as quay_Union
from imagequay_layout import quay_segment_command as quay_segment_command, quay_segment_command_64 as quay_segment_command_64, quay_section_64 as quay_section_64, quay_section as quay_section, quay_SectionType as quay_SectionType, quay_S_FLAGS_MASKS as quay_S_FLAGS_MASKS, quay_Struct as quay_Struct, quay_symtab_command as quay_symtab_command, quay_LOAD_COMMAND as quay_LOAD_COMMAND
from imagequay_layout.record_contract import quay_Constructable as quay_Constructable

@_name_boundary.class_contract('LoadCommand', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes'})
class quay_LoadCommand(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_33e0de7', 'args': 'quay_args_11d350a', 'kwargs': 'quay_kwargs_45f4d16'}, 'from_image')
    def quay_from_image(quay_cls_33e0de7, *quay_args_11d350a, **quay_kwargs_45f4d16):
        pass

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_8f8d933', 'args': 'quay_args_fe50aac', 'kwargs': 'quay_kwargs_3872ba7'}, 'from_values')
    def quay_from_values(quay_cls_8f8d933, *quay_args_fe50aac, **quay_kwargs_3872ba7):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_9147f7a'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_9147f7a):
        pass

@_name_boundary.class_contract('Section', {'serialize': 'quay_serialize', 'cmd': 'quay_cmd', 'name': 'quay_name', 'vm_address': 'quay_vm_address', 'file_address': 'quay_file_address', 'size': 'quay_size'})
class quay_Section:
    """

    """

    @_name_boundary.callable_contract({'self': 'quay_self_8a5ee66', 'cmd': 'quay_cmd_f84b4e1'}, '__init__')
    def __init__(quay_self_8a5ee66, quay_cmd_f84b4e1):
        _name_boundary.attributes(quay_self_8a5ee66)['cmd'] = quay_cmd_f84b4e1
        _name_boundary.attributes(quay_self_8a5ee66)['name'] = _name_boundary.attributes(quay_cmd_f84b4e1)['sectname']
        _name_boundary.attributes(quay_self_8a5ee66)['vm_address'] = _name_boundary.attributes(quay_cmd_f84b4e1)['addr']
        _name_boundary.attributes(quay_self_8a5ee66)['file_address'] = _name_boundary.attributes(quay_cmd_f84b4e1)['offset']
        _name_boundary.attributes(quay_self_8a5ee66)['size'] = _name_boundary.attributes(quay_cmd_f84b4e1)['size']

    @_name_boundary.callable_contract({'self': 'quay_self_04ec23d'}, 'serialize')
    def quay_serialize(quay_self_04ec23d):
        return {'command': _name_boundary.attributes(_name_boundary.attributes(quay_self_04ec23d)['cmd'])['serialize'](), 'name': _name_boundary.attributes(quay_self_04ec23d)['name'], 'vm_address': _name_boundary.attributes(quay_self_04ec23d)['vm_address'], 'file_address': _name_boundary.attributes(quay_self_04ec23d)['file_address'], 'size': _name_boundary.attributes(quay_self_04ec23d)['size']}

@_name_boundary.class_contract('SegmentLoadCommand', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'cmd': 'quay_cmd', 'is64': 'quay_is64', 'vm_address': 'quay_vm_address', 'file_address': 'quay_file_address', 'size': 'quay_size', 'name': 'quay_name', 'type': 'quay_type', 'sections': 'quay_sections'})
class quay_SegmentLoadCommand(quay_LoadCommand):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_36b98f5', 'image': 'quay_image_9118b8d', 'command': 'quay_command_9fed16e'}, 'from_image')
    def quay_from_image(quay_cls_36b98f5, quay_image_9118b8d, quay_command_9fed16e: quay_Union[quay_segment_command, quay_segment_command_64]) -> 'SegmentLoadCommand':
        quay_lc_9150517 = quay_SegmentLoadCommand()
        _name_boundary.attributes(quay_lc_9150517)['cmd'] = quay_command_9fed16e
        _name_boundary.attributes(quay_lc_9150517)['vm_address'] = _name_boundary.attributes(quay_command_9fed16e)['vmaddr']
        _name_boundary.attributes(quay_lc_9150517)['file_address'] = _name_boundary.attributes(quay_command_9fed16e)['fileoff']
        _name_boundary.attributes(quay_lc_9150517)['size'] = _name_boundary.attributes(quay_command_9fed16e)['vmsize']
        _name_boundary.attributes(quay_lc_9150517)['name'] = _name_boundary.attributes(quay_command_9fed16e)['segname']
        _name_boundary.attributes(quay_lc_9150517)['type'] = quay_SectionType(quay_S_FLAGS_MASKS.SECTION_TYPE & _name_boundary.attributes(quay_command_9fed16e)['flags'])
        _name_boundary.attributes(quay_lc_9150517)['is64'] = isinstance(quay_command_9fed16e, quay_segment_command_64)
        quay_ea_dea3b91 = _name_boundary.attributes(quay_command_9fed16e)['off'] + _name_boundary.attributes(quay_command_9fed16e)['size']()
        for quay_sect_36166b6 in range(_name_boundary.attributes(quay_command_9fed16e)['nsects']):
            quay_sect_36166b6 = _name_boundary.attributes(quay_image_9118b8d)['read_struct'](quay_ea_dea3b91, quay_section_64 if _name_boundary.attributes(quay_lc_9150517)['is64'] else quay_section)
            quay__section_913f2c9 = quay_Section(quay_sect_36166b6)
            _name_boundary.attributes(quay_lc_9150517)['sections'][_name_boundary.attributes(quay_sect_36166b6)['name']] = quay__section_913f2c9
            quay_ea_dea3b91 += _name_boundary.attributes(quay_section_64)['size']() if _name_boundary.attributes(quay_lc_9150517)['is64'] else _name_boundary.attributes(quay_section)['size']()
        return quay_lc_9150517

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_18c97ae', 'is_64': 'quay_is_64_2d6843c', 'name': 'quay_name_cae609b', 'vm_addr': 'quay_vm_addr_c9bede4', 'vm_size': 'quay_vm_size_1086c63', 'file_addr': 'quay_file_addr_5969466', 'file_size': 'quay_file_size_53b8af2', 'maxprot': 'quay_maxprot_6ede6cd', 'initprot': 'quay_initprot_afba73d', 'flags': 'quay_flags_8e679b5', 'sections': 'quay_sections_c2819f0'}, 'from_values')
    def quay_from_values(quay_cls_18c97ae, quay_is_64_2d6843c, quay_name_cae609b, quay_vm_addr_c9bede4, quay_vm_size_1086c63, quay_file_addr_5969466, quay_file_size_53b8af2, quay_maxprot_6ede6cd, quay_initprot_afba73d, quay_flags_8e679b5, quay_sections_c2819f0):
        quay_lc_215c982 = quay_SegmentLoadCommand()
        assert len(quay_name_cae609b) <= 16
        quay_command_type_5387987 = quay_segment_command_64 if quay_is_64_2d6843c else quay_segment_command
        quay_section_type_5532cee = quay_section_64 if quay_is_64_2d6843c else quay_section
        quay_cmd_5c39d67 = 25 if quay_is_64_2d6843c else 1
        quay_cmdsize_05762f0 = _name_boundary.attributes(quay_command_type_5387987)['size']()
        quay_cmdsize_05762f0 += len(quay_sections_c2819f0) * _name_boundary.attributes(quay_section_type_5532cee)['size']()
        quay_command_35c212f = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_command_type_5387987, [quay_cmd_5c39d67, quay_cmdsize_05762f0, quay_name_cae609b, quay_vm_addr_c9bede4, quay_vm_size_1086c63, quay_file_addr_5969466, quay_file_size_53b8af2, quay_maxprot_6ede6cd, quay_initprot_afba73d, len(quay_sections_c2819f0), quay_flags_8e679b5])
        _name_boundary.attributes(quay_lc_215c982)['cmd'] = quay_command_35c212f
        _name_boundary.attributes(quay_lc_215c982)['vm_address'] = _name_boundary.attributes(quay_command_35c212f)['vmaddr']
        _name_boundary.attributes(quay_lc_215c982)['file_address'] = _name_boundary.attributes(quay_command_35c212f)['fileoff']
        _name_boundary.attributes(quay_lc_215c982)['size'] = _name_boundary.attributes(quay_command_35c212f)['vmsize']
        _name_boundary.attributes(quay_lc_215c982)['name'] = _name_boundary.attributes(quay_command_35c212f)['segname']
        _name_boundary.attributes(quay_lc_215c982)['type'] = quay_SectionType(quay_S_FLAGS_MASKS.SECTION_TYPE & _name_boundary.attributes(quay_command_35c212f)['flags'])
        _name_boundary.attributes(quay_lc_215c982)['is64'] = isinstance(quay_command_35c212f, quay_segment_command_64)
        _name_boundary.attributes(quay_lc_215c982)['sections'] = {_name_boundary.attributes(quay__section_12381e8)['name']: quay__section_12381e8 for quay__section_12381e8 in quay_sections_c2819f0}
        return quay_lc_215c982

    @_name_boundary.callable_contract({'self': 'quay_self_166969c'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_166969c):
        quay_data_363304a = bytearray()
        quay_data_363304a += bytearray(_name_boundary.attributes(_name_boundary.attributes(quay_self_166969c)['cmd'])['raw'])
        for quay__section_96367c3 in _name_boundary.attributes(quay_self_166969c)['sections'].values():
            quay_data_363304a += bytearray(_name_boundary.attributes(_name_boundary.attributes(quay__section_96367c3)['cmd'])['raw'])
        return quay_data_363304a

    @_name_boundary.callable_contract({'self': 'quay_self_a11b0aa'}, '__init__')
    def __init__(quay_self_a11b0aa):
        _name_boundary.attributes(quay_self_a11b0aa)['cmd'] = None
        _name_boundary.attributes(quay_self_a11b0aa)['is64'] = False
        _name_boundary.attributes(quay_self_a11b0aa)['vm_address'] = 0
        _name_boundary.attributes(quay_self_a11b0aa)['file_address'] = 0
        _name_boundary.attributes(quay_self_a11b0aa)['size'] = 0
        _name_boundary.attributes(quay_self_a11b0aa)['name'] = ''
        _name_boundary.attributes(quay_self_a11b0aa)['type'] = None
        _name_boundary.attributes(quay_self_a11b0aa)['sections'] = {}

@_name_boundary.class_contract('SymtabLoadCommand', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'cmd': 'quay_cmd', 'symtab_offset': 'quay_symtab_offset', 'symtab_entry_count': 'quay_symtab_entry_count', 'string_table_offset': 'quay_string_table_offset', 'string_table_size': 'quay_string_table_size'})
class quay_SymtabLoadCommand(quay_LoadCommand):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_028b1ef', 'command': 'quay_command_a4612d7'}, 'from_image')
    def quay_from_image(quay_cls_028b1ef, quay_command_a4612d7: quay_symtab_command):
        quay_lc_55a4dfa = quay_SymtabLoadCommand()
        _name_boundary.attributes(quay_lc_55a4dfa)['cmd'] = quay_command_a4612d7
        _name_boundary.attributes(quay_lc_55a4dfa)['symtab_offset'] = _name_boundary.attributes(quay_command_a4612d7)['symoff']
        _name_boundary.attributes(quay_lc_55a4dfa)['symtab_entry_count'] = _name_boundary.attributes(quay_command_a4612d7)['nsyms']
        _name_boundary.attributes(quay_lc_55a4dfa)['string_table_offset'] = _name_boundary.attributes(quay_command_a4612d7)['stroff']
        _name_boundary.attributes(quay_lc_55a4dfa)['string_table_size'] = _name_boundary.attributes(quay_command_a4612d7)['strsize']
        return quay_lc_55a4dfa

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_67b9c0e', 'symtab_offset': 'quay_symtab_offset_0791348', 'symtab_size': 'quay_symtab_size_661eae9', 'string_table_offset': 'quay_string_table_offset_b135fb5', 'string_table_size': 'quay_string_table_size_7911614'}, 'from_values')
    def quay_from_values(quay_cls_67b9c0e, quay_symtab_offset_0791348, quay_symtab_size_661eae9, quay_string_table_offset_b135fb5, quay_string_table_size_7911614):
        quay_cmd_3f3c125 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_symtab_command, [_name_boundary.attributes(quay_LOAD_COMMAND.SYMTAB)['value'], _name_boundary.attributes(quay_symtab_command)['size'](), quay_symtab_offset_0791348, quay_symtab_size_661eae9, quay_string_table_offset_b135fb5, quay_string_table_size_7911614])
        return _name_boundary.attributes(quay_cls_67b9c0e)['from_image'](quay_cmd_3f3c125)

    @_name_boundary.callable_contract({'self': 'quay_self_55e069f'}, '__init__')
    def __init__(quay_self_55e069f):
        _name_boundary.attributes(quay_self_55e069f)['cmd'] = None
        _name_boundary.attributes(quay_self_55e069f)['symtab_offset'] = 0
        _name_boundary.attributes(quay_self_55e069f)['symtab_entry_count'] = 0
        _name_boundary.attributes(quay_self_55e069f)['string_table_offset'] = 0
        _name_boundary.attributes(quay_self_55e069f)['string_table_size'] = 0

    @_name_boundary.callable_contract({'self': 'quay_self_ea1ee80'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_ea1ee80):
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_ea1ee80)['cmd'])['raw']
_name_boundary.module_contract(globals(), {'LOAD_COMMAND': 'quay_LOAD_COMMAND', 'SegmentLoadCommand': 'quay_SegmentLoadCommand', 'segment_command': 'quay_segment_command', 'LoadCommand': 'quay_LoadCommand', 'Section': 'quay_Section', 'symtab_command': 'quay_symtab_command', 'Constructable': 'quay_Constructable', 'SymtabLoadCommand': 'quay_SymtabLoadCommand', 'SectionType': 'quay_SectionType', 'S_FLAGS_MASKS': 'quay_S_FLAGS_MASKS', 'Union': 'quay_Union', 'section': 'quay_section', 'Struct': 'quay_Struct', 'segment_command_64': 'quay_segment_command_64', 'section_64': 'quay_section_64'})
