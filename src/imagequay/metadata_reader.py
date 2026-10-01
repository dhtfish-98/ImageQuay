# Derived from src/ktool/loader.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  loader.py
#
#  This file includes a lot of utilities, classes, and abstractions
#  designed for replicating certain functionality within dyld.
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
from typing import List as quay_List, Union as quay_Union, Dict as quay_Dict, Tuple as quay_Tuple, Optional as quay_Optional
import imagequay as quay_imagequay
from imagequay_layout import quay_MH_FLAGS as quay_MH_FLAGS, quay_MH_FILETYPE as quay_MH_FILETYPE, quay_LOAD_COMMAND as quay_LOAD_COMMAND, quay_BINDING_OPCODE as quay_BINDING_OPCODE, quay_LOAD_COMMAND_MAP as quay_LOAD_COMMAND_MAP, quay_BIND_SUBOPCODE_THREADED_SET_BIND_ORDINAL_TABLE_SIZE_ULEB as quay_BIND_SUBOPCODE_THREADED_SET_BIND_ORDINAL_TABLE_SIZE_ULEB, quay_BIND_SUBOPCODE_THREADED_APPLY as quay_BIND_SUBOPCODE_THREADED_APPLY, quay_MH_MAGIC_64 as quay_MH_MAGIC_64, quay_CPUType as quay_CPUType, quay_CPUSubTypeARM64 as quay_CPUSubTypeARM64, quay_MH_MAGIC as quay_MH_MAGIC
from imagequay_layout.record_contract import quay_Constructable as quay_Constructable
from imagequay_layout.pointer_records import *
from imagequay.signing_reader import quay_CodesignInfo as quay_CodesignInfo
from imagequay.failure_types import quay_MachOAlignmentError as quay_MachOAlignmentError
from imagequay.container_io import quay_Segment as quay_Segment, quay_Slice as quay_Slice, quay_MachOImageHeader as quay_MachOImageHeader, quay_PlatformType as quay_PlatformType
from imagequay_support.diagnostics import quay_log as quay_log
from imagequay.formatting import quay_macho_is_malformed as quay_macho_is_malformed, quay_ignore as quay_ignore, quay_bytes_to_hex as quay_bytes_to_hex
from imagequay.parsed_image import quay_Image as quay_Image, quay_os_version as quay_os_version, quay_LinkedImage as quay_LinkedImage, quay_MisalignedVM as quay_MisalignedVM

@_name_boundary.class_contract('MachOImageLoader', {'SYMTAB_LOADER': 'quay_SYMTAB_LOADER', 'load': 'quay_load', '_parse_load_commands': 'quay__parse_load_commands', '_process_image': 'quay__process_image'})
class quay_MachOImageLoader:
    """
    This class takes our initialized "Image" object, parses through the raw data behind it, and fills out its properties.

    """
    quay_SYMTAB_LOADER = None

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_731daa4', 'macho_slice': 'quay_macho_slice_9f8aef7', 'load_symtab': 'quay_load_symtab_2023fd0', 'load_imports': 'quay_load_imports_461910b', 'load_exports': 'quay_load_exports_bbf2c9a', 'force_misaligned_vm': 'quay_force_misaligned_vm_d20367b'}, 'load')
    def quay_load(quay_cls_731daa4, quay_macho_slice_9f8aef7: quay_Slice, quay_load_symtab_2023fd0=True, quay_load_imports_461910b=True, quay_load_exports_bbf2c9a=True, quay_force_misaligned_vm_d20367b=False) -> quay_Image:
        """
        Take a slice of a macho file and process it using the dyld functions

        :param force_misaligned_vm:
        :param load_exports: Load Exports
        :param load_imports: Load Imports
        :param load_symtab: Load Symbol Table
        :param macho_slice: Slice to load. If your image is not fat, that'll be MachOFile.slices[0]
        :type macho_slice: Slice
        :return: Processed image object
        :rtype: Image
        """
        _name_boundary.attributes(quay_MachOImageLoader)['SYMTAB_LOADER'] = quay_SymbolTable
        _name_boundary.attributes(quay_log)['info']('Loading image')
        quay_image_3da7aa2 = quay_Image(quay_macho_slice_9f8aef7, quay_force_misaligned_vm_d20367b)
        if quay_force_misaligned_vm_d20367b:
            _name_boundary.attributes(quay_image_3da7aa2)['vm'] = quay_MisalignedVM()
        _name_boundary.attributes(quay_log)['info']('Processing Load Commands')
        _name_boundary.attributes(quay_MachOImageLoader)['_parse_load_commands'](quay_image_3da7aa2, quay_load_symtab_2023fd0, quay_load_imports_461910b, quay_load_exports_bbf2c9a)
        _name_boundary.attributes(quay_log)['info']('Processing Image')
        _name_boundary.attributes(quay_MachOImageLoader)['_process_image'](quay_image_3da7aa2)
        return quay_image_3da7aa2

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_563b3fb', 'image': 'quay_image_e82ca28', 'load_symtab': 'quay_load_symtab_c90fb80', 'load_imports': 'quay_load_imports_c3a2884', 'load_exports': 'quay_load_exports_b2afef4'}, '_parse_load_commands')
    def quay__parse_load_commands(quay_cls_563b3fb, quay_image_e82ca28: quay_Image, quay_load_symtab_c90fb80=True, quay_load_imports_c3a2884=True, quay_load_exports_b2afef4=True) -> None:
        quay_fixups_f096173 = None
        _name_boundary.attributes(quay_log)['info'](f"registered {len(_name_boundary.attributes(_name_boundary.attributes(quay_image_e82ca28)['macho_header'])['load_commands'])} Load Commands")
        for quay_cmd_ed94d81 in _name_boundary.attributes(_name_boundary.attributes(quay_image_e82ca28)['macho_header'])['load_commands']:
            try:
                quay_load_command_612ac06 = quay_LOAD_COMMAND(_name_boundary.attributes(quay_cmd_ed94d81)['cmd'])
            except ValueError:
                continue
            if quay_load_command_612ac06 == quay_LOAD_COMMAND.SEGMENT_64 or quay_load_command_612ac06 == quay_LOAD_COMMAND.SEGMENT:
                _name_boundary.attributes(quay_log)['debug_tm']('Loading Segment')
                quay_segment_e386e4b = quay_Segment(quay_image_e82ca28, quay_cmd_ed94d81)
                _name_boundary.attributes(quay_log)['info'](f"Loaded Segment {_name_boundary.attributes(quay_segment_e386e4b)['name']}")
                try:
                    _name_boundary.attributes(_name_boundary.attributes(quay_image_e82ca28)['vm'])['add_segment'](quay_segment_e386e4b)
                except quay_MachOAlignmentError:
                    _name_boundary.attributes(quay_image_e82ca28)['vm'] = _name_boundary.attributes(_name_boundary.attributes(quay_image_e82ca28)['vm'])['fallback']
                    _name_boundary.attributes(_name_boundary.attributes(quay_image_e82ca28)['vm'])['add_segment'](quay_segment_e386e4b)
                _name_boundary.attributes(quay_image_e82ca28)['segments'][_name_boundary.attributes(quay_segment_e386e4b)['name']] = quay_segment_e386e4b
            elif quay_load_command_612ac06 in [quay_LOAD_COMMAND.THREAD, quay_LOAD_COMMAND.UNIXTHREAD]:
                quay_thread_state_beb4f3c = []
                for quay_i_e7666ac in range(_name_boundary.attributes(quay_cmd_ed94d81)['count']):
                    quay_off_ebfceb2 = _name_boundary.attributes(quay_cmd_ed94d81)['off'] + 16 + quay_i_e7666ac * 4
                    quay_val_14cc871 = _name_boundary.attributes(quay_image_e82ca28)['read_uint'](quay_off_ebfceb2, 4)
                    quay_thread_state_beb4f3c.append(quay_val_14cc871)
                _name_boundary.attributes(quay_image_e82ca28)['thread_state'] = quay_thread_state_beb4f3c
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.CODE_SIGNATURE:
                _name_boundary.attributes(quay_image_e82ca28)['_codesign_cmd'] = quay_cmd_ed94d81
                _name_boundary.attributes(quay_image_e82ca28)['codesign_info'] = _name_boundary.attributes(quay_CodesignInfo)['from_image'](quay_image_e82ca28, quay_cmd_ed94d81)
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.MAIN:
                _name_boundary.attributes(quay_image_e82ca28)['_entry_off'] = _name_boundary.attributes(quay_cmd_ed94d81)['entryoff']
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.DYLD_INFO_ONLY:
                _name_boundary.attributes(quay_image_e82ca28)['info'] = quay_cmd_ed94d81
                if quay_load_imports_c3a2884:
                    _name_boundary.attributes(quay_log)['info']('Loading Binding Info')
                    _name_boundary.attributes(quay_image_e82ca28)['binding_table'] = quay_BindingTable(quay_image_e82ca28, _name_boundary.attributes(quay_cmd_ed94d81)['bind_off'], _name_boundary.attributes(quay_cmd_ed94d81)['bind_size'])
                    _name_boundary.attributes(quay_image_e82ca28)['weak_binding_table'] = quay_BindingTable(quay_image_e82ca28, _name_boundary.attributes(quay_cmd_ed94d81)['weak_bind_off'], _name_boundary.attributes(quay_cmd_ed94d81)['weak_bind_size'])
                    _name_boundary.attributes(quay_image_e82ca28)['lazy_binding_table'] = quay_BindingTable(quay_image_e82ca28, _name_boundary.attributes(quay_cmd_ed94d81)['lazy_bind_off'], _name_boundary.attributes(quay_cmd_ed94d81)['lazy_bind_size'])
                if quay_load_exports_b2afef4:
                    _name_boundary.attributes(quay_log)['info']('Loading Export Trie')
                    try:
                        _name_boundary.attributes(quay_image_e82ca28)['export_trie'] = _name_boundary.attributes(quay_ExportTrie)['from_image'](quay_image_e82ca28, _name_boundary.attributes(quay_cmd_ed94d81)['export_off'], _name_boundary.attributes(quay_cmd_ed94d81)['export_size'])
                    except Exception as quay_e_407aeb2:
                        _name_boundary.attributes(quay_log)['error'](f'Error loading export trie: {quay_e_407aeb2}')
                        import traceback as quay_traceback_237730b
                        print(quay_traceback_237730b.format_exc())
                        _name_boundary.attributes(quay_image_e82ca28)['export_trie'] = None
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.FUNCTION_STARTS:
                quay_fs_start_2a01215 = _name_boundary.attributes(quay_cmd_ed94d81)['dataoff']
                quay_fs_size_51f0c60 = _name_boundary.attributes(quay_cmd_ed94d81)['datasize']
                quay_read_head_12943d5 = quay_fs_start_2a01215
                quay_fs_addr_f5bd476 = _name_boundary.attributes(_name_boundary.attributes(quay_image_e82ca28)['vm'])['vm_base_addr']
                while quay_read_head_12943d5 < quay_fs_start_2a01215 + quay_fs_size_51f0c60:
                    quay_fs_r_addr_401f3ea, quay_read_head_12943d5 = _name_boundary.attributes(quay_image_e82ca28)['read_uleb128'](quay_read_head_12943d5)
                    quay_fs_addr_f5bd476 += quay_fs_r_addr_401f3ea
                    _name_boundary.attributes(quay_image_e82ca28)['function_starts'].append(quay_fs_addr_f5bd476)
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.LC_DYLD_EXPORTS_TRIE:
                _name_boundary.attributes(quay_log)['info']('Loading Export Trie')
                _name_boundary.attributes(quay_image_e82ca28)['export_trie'] = _name_boundary.attributes(quay_ExportTrie)['from_image'](quay_image_e82ca28, _name_boundary.attributes(quay_cmd_ed94d81)['dataoff'], _name_boundary.attributes(quay_cmd_ed94d81)['datasize'])
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.LC_DYLD_CHAINED_FIXUPS:
                if quay_load_imports_c3a2884:
                    _name_boundary.attributes(quay_image_e82ca28)['chained_fixups'] = _name_boundary.attributes(quay_ChainedFixups)['from_image'](quay_image_e82ca28, quay_cmd_ed94d81)
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.SYMTAB:
                if quay_load_symtab_c90fb80:
                    _name_boundary.attributes(quay_log)['info']('Loading Symbol Table')
                    _name_boundary.attributes(quay_image_e82ca28)['symbol_table'] = _name_boundary.attributes(quay_MachOImageLoader)['SYMTAB_LOADER'](quay_image_e82ca28, quay_cmd_ed94d81)
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.DYSYMTAB:
                pass
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.UUID:
                _name_boundary.attributes(quay_image_e82ca28)['uuid'] = _name_boundary.attributes(quay_cmd_ed94d81)['uuid']
                _name_boundary.attributes(quay_log)['info'](f"image UUID: {_name_boundary.attributes(quay_image_e82ca28)['uuid']}")
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.SUB_CLIENT:
                quay_string_7881846 = _name_boundary.attributes(quay_image_e82ca28)['read_cstr'](_name_boundary.attributes(quay_cmd_ed94d81)['off'] + _name_boundary.attributes(quay_cmd_ed94d81)['offset'])
                _name_boundary.attributes(quay_image_e82ca28)['allowed_clients'].append(quay_string_7881846)
                _name_boundary.attributes(quay_log)['debug'](f'Loaded Subclient "{quay_string_7881846}"')
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.RPATH:
                quay_string_7881846 = _name_boundary.attributes(quay_image_e82ca28)['read_cstr'](_name_boundary.attributes(quay_cmd_ed94d81)['off'] + _name_boundary.attributes(quay_cmd_ed94d81)['path'])
                _name_boundary.attributes(quay_image_e82ca28)['rpath'] = quay_string_7881846
                _name_boundary.attributes(quay_log)['info'](f'image Resource Path: {quay_string_7881846}')
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.BUILD_VERSION:
                _name_boundary.attributes(quay_image_e82ca28)['platform'] = quay_PlatformType(_name_boundary.attributes(quay_cmd_ed94d81)['platform'])
                _name_boundary.attributes(quay_image_e82ca28)['minos'] = quay_os_version(x=_name_boundary.attributes(quay_image_e82ca28)['read_uint'](_name_boundary.attributes(quay_cmd_ed94d81)['off'] + 14, 2), y=_name_boundary.attributes(quay_image_e82ca28)['read_uint'](_name_boundary.attributes(quay_cmd_ed94d81)['off'] + 13, 1), z=_name_boundary.attributes(quay_image_e82ca28)['read_uint'](_name_boundary.attributes(quay_cmd_ed94d81)['off'] + 12, 1))
                _name_boundary.attributes(quay_image_e82ca28)['sdk_version'] = quay_os_version(x=_name_boundary.attributes(quay_image_e82ca28)['read_uint'](_name_boundary.attributes(quay_cmd_ed94d81)['off'] + 18, 2), y=_name_boundary.attributes(quay_image_e82ca28)['read_uint'](_name_boundary.attributes(quay_cmd_ed94d81)['off'] + 17, 1), z=_name_boundary.attributes(quay_image_e82ca28)['read_uint'](_name_boundary.attributes(quay_cmd_ed94d81)['off'] + 16, 1))
                _name_boundary.attributes(quay_log)['info'](f"Loaded platform {_name_boundary.attributes(_name_boundary.attributes(quay_image_e82ca28)['platform'])['name']} | Minimum OS {_name_boundary.attributes(_name_boundary.attributes(quay_image_e82ca28)['minos'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_image_e82ca28)['minos'])['y']}.{_name_boundary.attributes(quay_image_e82ca28)['minos'].z} | SDK Version {_name_boundary.attributes(_name_boundary.attributes(quay_image_e82ca28)['sdk_version'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_image_e82ca28)['sdk_version'])['y']}.{_name_boundary.attributes(quay_image_e82ca28)['sdk_version'].z}")
            elif isinstance(quay_cmd_ed94d81, quay_version_min_command):
                if _name_boundary.attributes(quay_image_e82ca28)['platform'] == quay_PlatformType.UNK:
                    if quay_load_command_612ac06 == quay_LOAD_COMMAND.VERSION_MIN_MACOSX:
                        _name_boundary.attributes(quay_image_e82ca28)['platform'] = quay_PlatformType.MACOS
                    elif quay_load_command_612ac06 == quay_LOAD_COMMAND.VERSION_MIN_IPHONEOS:
                        _name_boundary.attributes(quay_image_e82ca28)['platform'] = quay_PlatformType.IOS
                    elif quay_load_command_612ac06 == quay_LOAD_COMMAND.VERSION_MIN_TVOS:
                        _name_boundary.attributes(quay_image_e82ca28)['platform'] = quay_PlatformType.TVOS
                    elif quay_load_command_612ac06 == quay_LOAD_COMMAND.VERSION_MIN_WATCHOS:
                        _name_boundary.attributes(quay_image_e82ca28)['platform'] = quay_PlatformType.WATCHOS
                    _name_boundary.attributes(quay_image_e82ca28)['minos'] = quay_os_version(x=_name_boundary.attributes(quay_image_e82ca28)['read_uint'](_name_boundary.attributes(quay_cmd_ed94d81)['off'] + 10, 2), y=_name_boundary.attributes(quay_image_e82ca28)['read_uint'](_name_boundary.attributes(quay_cmd_ed94d81)['off'] + 9, 1), z=_name_boundary.attributes(quay_image_e82ca28)['read_uint'](_name_boundary.attributes(quay_cmd_ed94d81)['off'] + 8, 1))
            elif quay_load_command_612ac06 == quay_LOAD_COMMAND.ID_DYLIB:
                _name_boundary.attributes(quay_image_e82ca28)['dylib'] = quay_LinkedImage(quay_image_e82ca28, quay_cmd_ed94d81)
                _name_boundary.attributes(quay_log)['debug'](f"Loaded local dylib_command with install_name {_name_boundary.attributes(_name_boundary.attributes(quay_image_e82ca28)['dylib'])['install_name']}")
            elif isinstance(quay_cmd_ed94d81, quay_dylib_command):
                quay_external_dylib_52b655a = quay_LinkedImage(quay_image_e82ca28, quay_cmd_ed94d81)
                _name_boundary.attributes(quay_image_e82ca28)['linked_images'].append(quay_external_dylib_52b655a)
                _name_boundary.attributes(quay_log)['debug'](f"Loaded linked dylib_command with install name {_name_boundary.attributes(quay_external_dylib_52b655a)['install_name']}")

    @staticmethod
    @_name_boundary.callable_contract({'image': 'quay_image_466e9b4'}, '_process_image')
    def quay__process_image(quay_image_466e9b4: quay_Image) -> None:
        """
        Once all load commands have been processed, process the results.
        This is mainly for things which need to be done once *all* lcs have been processed.

        :param image:
        :return:
        """
        if _name_boundary.attributes(quay_image_466e9b4)['dylib'] is not None:
            _name_boundary.attributes(quay_image_466e9b4)['name'] = _name_boundary.attributes(_name_boundary.attributes(quay_image_466e9b4)['dylib'])['install_name'].split('/')[-1]
            _name_boundary.attributes(quay_image_466e9b4)['base_name'] = _name_boundary.attributes(_name_boundary.attributes(quay_image_466e9b4)['dylib'])['install_name'].split('/')[-1]
            _name_boundary.attributes(quay_image_466e9b4)['install_name'] = _name_boundary.attributes(_name_boundary.attributes(quay_image_466e9b4)['dylib'])['install_name']
        else:
            _name_boundary.attributes(quay_image_466e9b4)['name'] = ''
            _name_boundary.attributes(quay_image_466e9b4)['base_name'] = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_image_466e9b4)['slice'])['file'])['name']
            _name_boundary.attributes(quay_image_466e9b4)['install_name'] = ''
        if _name_boundary.attributes(quay_image_466e9b4)['export_trie']:
            for quay_symbol_addf870 in _name_boundary.attributes(_name_boundary.attributes(quay_image_466e9b4)['export_trie'])['symbols']:
                _name_boundary.attributes(quay_image_466e9b4)['exports'].append(quay_symbol_addf870)
                _name_boundary.attributes(quay_image_466e9b4)['export_table'][_name_boundary.attributes(quay_symbol_addf870)['address']] = quay_symbol_addf870
        if _name_boundary.attributes(quay_image_466e9b4)['binding_table']:
            for quay_symbol_addf870 in _name_boundary.attributes(_name_boundary.attributes(quay_image_466e9b4)['binding_table'])['symbol_table']:
                _name_boundary.attributes(quay_symbol_addf870)['attr'] = ''
                _name_boundary.attributes(quay_image_466e9b4)['imports'].append(quay_symbol_addf870)
                _name_boundary.attributes(quay_image_466e9b4)['import_table'][_name_boundary.attributes(quay_symbol_addf870)['address']] = quay_symbol_addf870
            for quay_symbol_addf870 in _name_boundary.attributes(_name_boundary.attributes(quay_image_466e9b4)['weak_binding_table'])['symbol_table']:
                _name_boundary.attributes(quay_symbol_addf870)['attr'] = 'Weak'
                _name_boundary.attributes(quay_image_466e9b4)['imports'].append(quay_symbol_addf870)
                _name_boundary.attributes(quay_image_466e9b4)['import_table'][_name_boundary.attributes(quay_symbol_addf870)['address']] = quay_symbol_addf870
            for quay_symbol_addf870 in _name_boundary.attributes(_name_boundary.attributes(quay_image_466e9b4)['lazy_binding_table'])['symbol_table']:
                _name_boundary.attributes(quay_symbol_addf870)['attr'] = 'Lazy'
                _name_boundary.attributes(quay_image_466e9b4)['imports'].append(quay_symbol_addf870)
                _name_boundary.attributes(quay_image_466e9b4)['import_table'][_name_boundary.attributes(quay_symbol_addf870)['address']] = quay_symbol_addf870
        if _name_boundary.attributes(quay_image_466e9b4)['chained_fixups']:
            for quay_symbol_addf870 in _name_boundary.attributes(_name_boundary.attributes(quay_image_466e9b4)['chained_fixups'])['symbols']:
                _name_boundary.attributes(quay_symbol_addf870)['attr'] = ''
                _name_boundary.attributes(quay_image_466e9b4)['imports'].append(quay_symbol_addf870)
                _name_boundary.attributes(quay_image_466e9b4)['import_table'][_name_boundary.attributes(quay_symbol_addf870)['address']] = quay_symbol_addf870
        if _name_boundary.attributes(quay_image_466e9b4)['symbol_table']:
            for quay_symbol_addf870 in _name_boundary.attributes(_name_boundary.attributes(quay_image_466e9b4)['symbol_table'])['table']:
                _name_boundary.attributes(quay_image_466e9b4)['symbols'][_name_boundary.attributes(quay_symbol_addf870)['address']] = quay_symbol_addf870
        if len(_name_boundary.attributes(quay_image_466e9b4)['thread_state']) > 0:
            _name_boundary.attributes(quay_image_466e9b4)['entry_point'] = _name_boundary.attributes(quay_image_466e9b4)['thread_state'][-4] if _name_boundary.attributes(_name_boundary.attributes(quay_image_466e9b4)['macho_header'])['is64'] else _name_boundary.attributes(quay_image_466e9b4)['thread_state'][-2]
        elif _name_boundary.attributes(quay_image_466e9b4)['_entry_off'] > 0:
            _name_boundary.attributes(quay_image_466e9b4)['entry_point'] = _name_boundary.attributes(_name_boundary.attributes(quay_image_466e9b4)['vm'])['vm_base_addr'] + _name_boundary.attributes(quay_image_466e9b4)['_entry_off']

@_name_boundary.class_contract('SymbolType', {})
class quay_SymbolType(quay_Enum):
    CLASS = 0
    METACLASS = 1
    IVAR = 2
    FUNC = 3
    UNK = 4

@_name_boundary.class_contract('Symbol', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'serialize': 'quay_serialize', 'fullname': 'quay_fullname', 'name': 'quay_name', 'dec_type': 'quay_dec_type', 'address': 'quay_address', 'entry': 'quay_entry', 'ordinal': 'quay_ordinal', 'types': 'quay_types', 'external': 'quay_external', 'attr': 'quay_attr'})
class quay_Symbol(quay_Constructable):
    """
    This class can represent several types of symbols.

    """

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_38a9652', 'image': 'quay_image_3ec6ab8', 'cmd': 'quay_cmd_47938ba', 'entry': 'quay_entry_f5de662'}, 'from_image')
    def quay_from_image(quay_cls_38a9652, quay_image_3ec6ab8, quay_cmd_47938ba, quay_entry_f5de662):
        quay_fullname_61ba025 = _name_boundary.attributes(quay_image_3ec6ab8)['read_cstr'](_name_boundary.attributes(quay_entry_f5de662)['str_index'] + _name_boundary.attributes(quay_cmd_47938ba)['stroff'])
        quay_addr_90a2434 = _name_boundary.attributes(quay_entry_f5de662)['value']
        quay_symbol_ea83700 = _name_boundary.attributes(quay_cls_38a9652)['from_values'](quay_fullname_61ba025, quay_addr_90a2434)
        quay_N_STAB_82480c6 = 224
        quay_N_PEXT_e27b44e = 16
        quay_N_TYPE_6ec7f6d = 14
        quay_N_EXT_63162d0 = 1
        quay_type_masked_64720ba = quay_N_TYPE_6ec7f6d & _name_boundary.attributes(quay_entry_f5de662)['type']
        for quay_name_921c0c0, quay_flag_12a250e in _name_boundary.attributes({'N_UNDF': 0, 'N_ABS': 2, 'N_SECT': 14, 'N_PBUD': 12, 'N_INDR': 10})['items']():
            if quay_type_masked_64720ba & quay_flag_12a250e:
                _name_boundary.attributes(quay_symbol_ea83700)['types'].append(quay_name_921c0c0)
        if _name_boundary.attributes(quay_entry_f5de662)['type'] & quay_N_EXT_63162d0:
            _name_boundary.attributes(quay_symbol_ea83700)['external'] = True
        return quay_symbol_ea83700

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_aa21974', 'fullname': 'quay_fullname_239e9c3', 'value': 'quay_value_486f21a', 'external': 'quay_external_8c13470', 'ordinal': 'quay_ordinal_b250558'}, 'from_values')
    def quay_from_values(quay_cls_aa21974, quay_fullname_239e9c3, quay_value_486f21a, quay_external_8c13470=False, quay_ordinal_b250558=0):
        if '_$_' in quay_fullname_239e9c3:
            if quay_fullname_239e9c3.startswith('_OBJC_CLASS_$'):
                quay_dec_type_dc1cc15 = quay_SymbolType.CLASS
            elif quay_fullname_239e9c3.startswith('_OBJC_METACLASS_$'):
                quay_dec_type_dc1cc15 = quay_SymbolType.METACLASS
            elif quay_fullname_239e9c3.startswith('_OBJC_IVAR_$'):
                quay_dec_type_dc1cc15 = quay_SymbolType.IVAR
            else:
                quay_dec_type_dc1cc15 = quay_SymbolType.UNK
            quay_name_ceae3b4 = quay_fullname_239e9c3.split('$')[1]
        else:
            quay_name_ceae3b4 = quay_fullname_239e9c3
            quay_dec_type_dc1cc15 = quay_SymbolType.FUNC
        return quay_cls_aa21974(quay_fullname_239e9c3, name=quay_name_ceae3b4, dec_type=quay_dec_type_dc1cc15, external=quay_external_8c13470, value=quay_value_486f21a, ordinal=quay_ordinal_b250558)

    @_name_boundary.callable_contract({'self': 'quay_self_0eb646a'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_0eb646a):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_a18d947'}, 'serialize')
    def quay_serialize(quay_self_a18d947):
        return {'name': _name_boundary.attributes(quay_self_a18d947)['fullname'], 'address': _name_boundary.attributes(quay_self_a18d947)['address'], 'external': _name_boundary.attributes(quay_self_a18d947)['external'], 'ordinal': _name_boundary.attributes(quay_self_a18d947)['ordinal']}

    @_name_boundary.callable_contract({'self': 'quay_self_2d13806', 'fullname': 'quay_fullname_13fbc9a', 'name': 'quay_name_2c31011', 'dec_type': 'quay_dec_type_00e5a2d', 'external': 'quay_external_061e299', 'value': 'quay_value_e990532', 'ordinal': 'quay_ordinal_faaf9e3'}, '__init__')
    def __init__(quay_self_2d13806, quay_fullname_13fbc9a=None, quay_name_2c31011=None, quay_dec_type_00e5a2d=None, quay_external_061e299=False, quay_value_e990532=0, quay_ordinal_faaf9e3=0):
        _name_boundary.attributes(quay_self_2d13806)['fullname'] = quay_fullname_13fbc9a
        _name_boundary.attributes(quay_self_2d13806)['name'] = quay_name_2c31011
        _name_boundary.attributes(quay_self_2d13806)['dec_type'] = quay_dec_type_00e5a2d
        _name_boundary.attributes(quay_self_2d13806)['address'] = quay_value_e990532
        _name_boundary.attributes(quay_self_2d13806)['entry'] = None
        _name_boundary.attributes(quay_self_2d13806)['ordinal'] = quay_ordinal_faaf9e3
        _name_boundary.attributes(quay_self_2d13806)['types'] = []
        _name_boundary.attributes(quay_self_2d13806)['external'] = quay_external_061e299
        _name_boundary.attributes(quay_self_2d13806)['attr'] = None

@_name_boundary.class_contract('SymbolTable', {'_load_symbol_table': 'quay__load_symbol_table', 'image': 'quay_image', 'cmd': 'quay_cmd', 'ext': 'quay_ext', 'table': 'quay_table'})
class quay_SymbolTable:
    """
    This class represents the symbol table declared in the MachO File

    .table contains the symbol table

    .ext contains exported symbols, i think?

    This class is incomplete

    """

    @_name_boundary.callable_contract({'self': 'quay_self_a5800e0', 'image': 'quay_image_23e4bd2', 'cmd': 'quay_cmd_9c2aa86'}, '__init__')
    def __init__(quay_self_a5800e0, quay_image_23e4bd2: quay_Image, quay_cmd_9c2aa86: quay_symtab_command):
        _name_boundary.attributes(quay_self_a5800e0)['image']: quay_Image = quay_image_23e4bd2
        _name_boundary.attributes(quay_self_a5800e0)['cmd']: quay_symtab_command = quay_cmd_9c2aa86
        _name_boundary.attributes(quay_self_a5800e0)['ext']: quay_List[quay_Symbol] = []
        _name_boundary.attributes(quay_self_a5800e0)['table']: quay_List[quay_Symbol] = _name_boundary.attributes(quay_self_a5800e0)['_load_symbol_table']()

    @_name_boundary.callable_contract({'self': 'quay_self_fd00f8a'}, '_load_symbol_table')
    def quay__load_symbol_table(quay_self_fd00f8a) -> quay_List[quay_Symbol]:
        quay_symbol_table_629221d = []
        quay_read_address_0878e1b = _name_boundary.attributes(_name_boundary.attributes(quay_self_fd00f8a)['cmd'])['symoff']
        quay_typing_81c5ce9 = quay_symtab_entry if _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_fd00f8a)['image'])['macho_header'])['is64'] else quay_symtab_entry_32
        for quay_i_39ae3a7 in range(0, _name_boundary.attributes(_name_boundary.attributes(quay_self_fd00f8a)['cmd'])['nsyms']):
            quay_entry_40e4d61 = _name_boundary.attributes(_name_boundary.attributes(quay_self_fd00f8a)['image'])['read_struct'](quay_read_address_0878e1b + _name_boundary.attributes(quay_typing_81c5ce9)['size']() * quay_i_39ae3a7, quay_typing_81c5ce9)
            quay_symbol_99aa1f1 = _name_boundary.attributes(quay_Symbol)['from_image'](_name_boundary.attributes(quay_self_fd00f8a)['image'], _name_boundary.attributes(quay_self_fd00f8a)['cmd'], quay_entry_40e4d61)
            quay_symbol_table_629221d.append(quay_symbol_99aa1f1)
            if _name_boundary.attributes(quay_symbol_99aa1f1)['external']:
                _name_boundary.attributes(quay_self_fd00f8a)['ext'].append(quay_symbol_99aa1f1)
            _name_boundary.attributes(quay_log)['debug_tm'](f"Symbol Table: Loaded symbol:{_name_boundary.attributes(quay_symbol_99aa1f1)['name']} ordinal:{_name_boundary.attributes(quay_symbol_99aa1f1)['ordinal']} type:{_name_boundary.attributes(quay_symbol_99aa1f1)['dec_type']}")
            _name_boundary.attributes(quay_log)['debug_tm'](str(quay_entry_40e4d61))
        return quay_symbol_table_629221d

@_name_boundary.class_contract('ChainedFixups', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'symbols': 'quay_symbols', 'rebases': 'quay_rebases'})
class quay_ChainedFixups(quay_Constructable):

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_d293e50', 'image': 'quay_image_f2d6319', 'chained_fixup_cmd': 'quay_chained_fixup_cmd_3afc574'}, 'from_image')
    def quay_from_image(quay_cls_d293e50, quay_image_f2d6319: quay_Image, quay_chained_fixup_cmd_3afc574: quay_linkedit_data_command):
        quay_syms_14b01a1 = []
        quay_rebases_07f1425 = {}
        quay_fixup_header_56d514b = _name_boundary.attributes(quay_image_f2d6319)['read_struct'](_name_boundary.attributes(quay_chained_fixup_cmd_3afc574)['dataoff'], quay_dyld_chained_fixups_header)
        _name_boundary.attributes(quay_log)['debug_tm'](f"{_name_boundary.attributes(quay_fixup_header_56d514b)['render_indented']()}")
        if _name_boundary.attributes(quay_fixup_header_56d514b)['fixups_version'] > 0:
            _name_boundary.attributes(quay_log)['error']('Unknown Fixup Format')
            return quay_cls_d293e50([])
        quay_import_table_size_4e3f24a = _name_boundary.attributes(quay_fixup_header_56d514b)['imports_count'] * _name_boundary.attributes(quay_dyld_chained_import)['size']()
        if quay_import_table_size_4e3f24a > _name_boundary.attributes(quay_chained_fixup_cmd_3afc574)['datasize']:
            _name_boundary.attributes(quay_log)['error']('Chained fixup import table is larger than chained fixup linkedit region')
            return quay_cls_d293e50([])
        if _name_boundary.attributes(quay_fixup_header_56d514b)['imports_format'] != _name_boundary.attributes(quay_dyld_chained_import_format.DYLD_CHAINED_IMPORT)['value']:
            _name_boundary.attributes(quay_log)['error']('Unknown or unhandled import format')
        quay_imports_address_8dac123 = _name_boundary.attributes(quay_fixup_header_56d514b)['off'] + _name_boundary.attributes(quay_fixup_header_56d514b)['imports_offset']
        quay_symbols_address_1067a6f = _name_boundary.attributes(quay_fixup_header_56d514b)['off'] + _name_boundary.attributes(quay_fixup_header_56d514b)['symbols_offset']
        quay_import_entry_t_a60a93c = _name_boundary.named_record('import_entry_t', ['ord', 'weak', 'name'])
        quay_import_table_4f71561 = []
        for quay_i_af548f6 in range(0, _name_boundary.attributes(quay_fixup_header_56d514b)['imports_count']):
            quay_i_addr_4861e63 = quay_i_af548f6 * 4 + quay_imports_address_8dac123
            quay_i_entry_3038789 = _name_boundary.attributes(quay_image_f2d6319)['read_struct'](quay_i_addr_4861e63, quay_dyld_chained_import)
            quay_lib_ord_d8d26c2 = _name_boundary.attributes(quay_i_entry_3038789)['lib_ordinal']
            quay_is_weak_d5249a5 = _name_boundary.attributes(quay_i_entry_3038789)['weak_import']
            quay_name_addr_2777957 = quay_symbols_address_1067a6f + _name_boundary.attributes(quay_i_entry_3038789)['name_offset']
            quay_sym_name_afcba33 = _name_boundary.attributes(quay_image_f2d6319)['read_cstr'](quay_name_addr_2777957)
            quay_entry_1b684bd = quay_import_entry_t_a60a93c(quay_lib_ord_d8d26c2, quay_is_weak_d5249a5, quay_sym_name_afcba33)
            quay_import_table_4f71561.append(quay_entry_1b684bd)
            _name_boundary.attributes(quay_log)['debug_tm'](f'ChFx:ImportTable: {quay_sym_name_afcba33} @ ord {quay_lib_ord_d8d26c2}')
        quay_fixup_starts_address_f1a27aa = _name_boundary.attributes(quay_chained_fixup_cmd_3afc574)['dataoff'] + _name_boundary.attributes(quay_fixup_header_56d514b)['starts_offset']
        quay_segment_count_578fce4 = _name_boundary.attributes(quay_image_f2d6319)['read_uint'](quay_fixup_starts_address_f1a27aa, 4)
        quay_seg_info_offsets_350cde3 = []
        quay_cursor_4cd5767 = quay_fixup_starts_address_f1a27aa + 4
        for quay_i_af548f6 in range(0, quay_segment_count_578fce4):
            quay_seg_info_offsets_350cde3.append(_name_boundary.attributes(quay_image_f2d6319)['read_uint'](quay_cursor_4cd5767, 4))
            quay_cursor_4cd5767 += 4
        for quay_off_fd0bd05 in quay_seg_info_offsets_350cde3:
            if quay_off_fd0bd05 == 0:
                continue
            quay_segstarts_addr_d159920 = quay_fixup_starts_address_f1a27aa + quay_off_fd0bd05
            quay_starts_3d31dbe = _name_boundary.attributes(quay_image_f2d6319)['read_struct'](quay_segstarts_addr_d159920, quay_dyld_chained_starts_in_segment, endian='little')
            quay_stride_size_3891437: int = 0
            quay_ptr_format_2a6cf22: quay_ChainedFixupPointerGeneric = quay_ChainedFixupPointerGeneric.Error
            if _name_boundary.attributes(quay_starts_3d31dbe)['pointer_format'] in [_name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E)['value'], _name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E_USERLAND)['value'], _name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E_USERLAND24)['value']]:
                quay_stride_size_3891437 = 8
                quay_ptr_format_2a6cf22 = quay_ChainedFixupPointerGeneric.GenericArm64eFixupFormat
            elif _name_boundary.attributes(quay_starts_3d31dbe)['pointer_format'] == _name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E_KERNEL)['value']:
                quay_stride_size_3891437 = 4
                quay_ptr_format_2a6cf22 = quay_ChainedFixupPointerGeneric.GenericArm64eFixupFormat
            elif _name_boundary.attributes(quay_starts_3d31dbe)['pointer_format'] in [_name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_64)['value'], _name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_64_OFFSET)['value']]:
                quay_stride_size_3891437 = 4
                quay_ptr_format_2a6cf22 = quay_ChainedFixupPointerGeneric.Generic64FixupFormat
            elif _name_boundary.attributes(quay_starts_3d31dbe)['pointer_format'] in [_name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_32)['value'], _name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_32_CACHE)['value']]:
                quay_stride_size_3891437 = 4
                quay_ptr_format_2a6cf22 = quay_ChainedFixupPointerGeneric.Generic32FixupFormat
            elif _name_boundary.attributes(quay_starts_3d31dbe)['pointer_format'] == _name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_32_FIRMWARE)['value']:
                quay_stride_size_3891437 = 4
                quay_ptr_format_2a6cf22 = quay_ChainedFixupPointerGeneric.Generic64FixupFormat
            elif _name_boundary.attributes(quay_starts_3d31dbe)['pointer_format'] == _name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_64_KERNEL_CACHE)['value']:
                quay_stride_size_3891437 = 4
                quay_ptr_format_2a6cf22 = quay_ChainedFixupPointerGeneric.Kernel64FixupFormat
            elif _name_boundary.attributes(quay_starts_3d31dbe)['pointer_format'] == _name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_x86_64_KERNEL_CACHE)['value']:
                quay_stride_size_3891437 = 1
                quay_ptr_format_2a6cf22 = quay_ChainedFixupPointerGeneric.Kernel64FixupFormat
            else:
                _name_boundary.attributes(quay_log)['error'](f"Unsupported Pointer Format {_name_boundary.attributes(quay_starts_3d31dbe)['pointer_format']}")
                _name_boundary.attributes(quay_log)['error'](f"{hex(_name_boundary.attributes(quay_fixup_header_56d514b)['off'])} @ {_name_boundary.attributes(quay_fixup_header_56d514b)['render_indented']()}")
                _name_boundary.attributes(quay_log)['error'](f"{_name_boundary.attributes(quay_starts_3d31dbe)['render_indented']()}")
                return quay_cls_d293e50([])
            _name_boundary.attributes(quay_log)['debug_tm'](f'Stride Size: {quay_stride_size_3891437}')
            quay_page_start_offsets_f8715be: quay_List[quay_List[int]] = []
            for quay_i_af548f6 in range(0, _name_boundary.attributes(quay_starts_3d31dbe)['page_count']):
                quay_page_start_table_start_address_b05a5a0 = quay_segstarts_addr_d159920 + 22
                quay_i_addr_4861e63 = quay_page_start_table_start_address_b05a5a0 + 2 * quay_i_af548f6
                quay_start_54f0809 = _name_boundary.attributes(quay_image_f2d6319)['read_uint'](quay_i_addr_4861e63, 2)
                if quay_start_54f0809 & quay_DYLD_CHAINED_PTR_START_MULTI and quay_start_54f0809 != quay_DYLD_CHAINED_PTR_START_NONE:
                    quay_overflow_index_f9bce88 = quay_start_54f0809 & ~quay_DYLD_CHAINED_PTR_START_MULTI
                    quay_page_start_sub_starts_2551e00: quay_List[int] = []
                    quay_cursor_4cd5767 = quay_page_start_table_start_address_b05a5a0 + quay_overflow_index_f9bce88 * 2
                    quay_done_e03fda6 = False
                    while not quay_done_e03fda6:
                        quay_sub_page_start_6972be1 = _name_boundary.attributes(quay_image_f2d6319)['read_uint'](quay_cursor_4cd5767, 2)
                        quay_cursor_4cd5767 += 2
                        if quay_sub_page_start_6972be1 & quay_DYLD_CHAINED_PTR_START_LAST:
                            quay_page_start_sub_starts_2551e00.append(quay_sub_page_start_6972be1 & ~quay_DYLD_CHAINED_PTR_START_LAST)
                            quay_done_e03fda6 = True
                        else:
                            quay_page_start_sub_starts_2551e00.append(quay_sub_page_start_6972be1)
                    quay_page_start_offsets_f8715be.append(quay_page_start_sub_starts_2551e00)
                else:
                    quay_page_start_offsets_f8715be.append([quay_start_54f0809])
            quay_i_af548f6 = -1
            for quay_page_starts_7041ed7 in quay_page_start_offsets_f8715be:
                quay_i_af548f6 += 1
                quay_page_addr_8a818a4 = _name_boundary.attributes(quay_starts_3d31dbe)['segment_offset'] + quay_i_af548f6 * _name_boundary.attributes(quay_starts_3d31dbe)['page_size']
                for quay_start_54f0809 in quay_page_starts_7041ed7:
                    if quay_start_54f0809 == quay_DYLD_CHAINED_PTR_START_NONE:
                        continue
                    quay_chain_entry_address_b63c0e0 = quay_page_addr_8a818a4 + quay_start_54f0809
                    quay_fixups_done_b5c693e = False
                    while not quay_fixups_done_b5c693e:
                        quay_cursor_4cd5767 = quay_chain_entry_address_b63c0e0
                        quay_mapped_cursor_c112130 = _name_boundary.attributes(_name_boundary.attributes(quay_image_f2d6319)['vm'])['de_translate'](quay_cursor_4cd5767)
                        quay_pointer32_8077cdf: quay_ChainedFixupPointer32 = None
                        quay_pointer64_02a6b25: quay_ChainedFixupPointer64 = None
                        quay_pointerKern64_305ecab: quay_ChainedFixupKernel64 = None
                        if quay_ptr_format_2a6cf22 in [quay_ChainedFixupPointerGeneric.Generic32FixupFormat, quay_ChainedFixupPointerGeneric.Firmware32FixupFormat]:
                            quay_pointer32_8077cdf = _name_boundary.attributes(quay_image_f2d6319)['read_struct'](quay_cursor_4cd5767, quay_ChainedFixupPointer32)
                        elif quay_ptr_format_2a6cf22 == quay_ChainedFixupPointerGeneric.Kernel64FixupFormat:
                            quay_pointerKern64_305ecab = _name_boundary.attributes(quay_image_f2d6319)['read_struct'](quay_cursor_4cd5767, quay_ChainedFixupKernel64)
                        else:
                            quay_pointer64_02a6b25 = _name_boundary.attributes(quay_image_f2d6319)['read_struct'](quay_cursor_4cd5767, quay_ChainedFixupPointer64)
                        quay_bind_8bd2283: bool = False
                        quay_next_entry_stride_count_699e44f = 0
                        if quay_ptr_format_2a6cf22 == quay_ChainedFixupPointerGeneric.Generic32FixupFormat:
                            quay_bind_8bd2283 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer32_8077cdf)['generic32'])['dyld_chained_ptr_32_bind'])['bind'] != 0
                            quay_next_entry_stride_count_699e44f = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer32_8077cdf)['generic32'])['dyld_chained_ptr_32_rebase'])['next']
                        elif quay_ptr_format_2a6cf22 == quay_ChainedFixupPointerGeneric.Generic64FixupFormat:
                            quay_bind_8bd2283 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerGeneric64'])['dyld_chained_ptr_64_bind'])['bind'] != 0
                            quay_next_entry_stride_count_699e44f = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerGeneric64'])['dyld_chained_ptr_64_rebase'])['next']
                        elif quay_ptr_format_2a6cf22 == quay_ChainedFixupPointerGeneric.GenericArm64eFixupFormat:
                            quay_bind_8bd2283 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerArm64E'])['dyld_chained_ptr_arm64e_bind'])['bind'] != 0
                            quay_next_entry_stride_count_699e44f = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerArm64E'])['dyld_chained_ptr_arm64e_bind'])['next']
                        elif quay_ptr_format_2a6cf22 == quay_ChainedFixupPointerGeneric.Firmware32FixupFormat:
                            quay_bind_8bd2283 = False
                            quay_next_entry_stride_count_699e44f = _name_boundary.attributes(_name_boundary.attributes(quay_pointer32_8077cdf)['generic32'])['dyld_chained_ptr_32_firmware_rebase']
                        elif quay_ptr_format_2a6cf22 == quay_ChainedFixupPointerGeneric.Kernel64FixupFormat:
                            quay_bind_8bd2283 = False
                            quay_next_entry_stride_count_699e44f = _name_boundary.attributes(quay_pointerKern64_305ecab)['next']
                        else:
                            _name_boundary.attributes(quay_log)['error']('unreachable')
                            return quay_cls_d293e50([])
                        if quay_bind_8bd2283:
                            quay_ordinal_05c5125 = 0
                            if _name_boundary.attributes(quay_starts_3d31dbe)['pointer_format'] in [_name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_64)['value'], _name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_64_OFFSET)['value']]:
                                quay_ordinal_05c5125 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerGeneric64'])['dyld_chained_ptr_64_bind'])['ordinal']
                            elif _name_boundary.attributes(quay_starts_3d31dbe)['pointer_format'] in [_name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E)['value'], _name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E_USERLAND)['value'], _name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E_KERNEL)['value']]:
                                if _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerArm64E'])['dyld_chained_ptr_arm64e_bind'])['auth'] != 0:
                                    quay_ordinal_05c5125 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerArm64E'])['dyld_chained_ptr_arm64e_auth_bind24'])['ordinal'] if _name_boundary.attributes(quay_starts_3d31dbe)['pointer_format'] == quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E_USERLAND24 else _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerArm64E'])['dyld_chained_ptr_arm64e_auth_bind'])['ordinal']
                                else:
                                    quay_ordinal_05c5125 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerArm64E'])['dyld_chained_ptr_arm64e_bind24'])['ordinal'] if _name_boundary.attributes(quay_starts_3d31dbe)['pointer_format'] == quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E_USERLAND24 else _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerArm64E'])['dyld_chained_ptr_arm64e_bind'])['ordinal']
                            elif _name_boundary.attributes(quay_starts_3d31dbe)['pointer_format'] == _name_boundary.attributes(quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_32)['value']:
                                quay_ordinal_05c5125 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer32_8077cdf)['generic32'])['dyld_chained_ptr_32_bind'])['ordinal']
                            else:
                                _name_boundary.attributes(quay_log)['error']('Unknown bind pointer format')
                                return quay_cls_d293e50([])
                            if quay_ordinal_05c5125 < len(quay_import_table_4f71561):
                                quay_entry_1b684bd = quay_import_table_4f71561[quay_ordinal_05c5125]
                                quay_target_addr_9ab40a4 = quay_mapped_cursor_c112130
                                quay_sym_4be4c81 = _name_boundary.attributes(quay_Symbol)['from_values'](_name_boundary.attributes(quay_entry_1b684bd)['name'], quay_target_addr_9ab40a4, external=True, ordinal=quay_entry_1b684bd.ord)
                                quay_syms_14b01a1.append(quay_sym_4be4c81)
                                quay_rebases_07f1425[quay_mapped_cursor_c112130 + _name_boundary.attributes(_name_boundary.attributes(quay_image_f2d6319)['vm'])['vm_base_addr']] = 0
                        else:
                            quay_entry_offset_baee312 = 0
                            if quay_dyld_chained_ptr_format(_name_boundary.attributes(quay_starts_3d31dbe)['pointer_format']) in [quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E, quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E_KERNEL, quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E_USERLAND, quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E_USERLAND24]:
                                if _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerArm64E'])['dyld_chained_ptr_arm64e_auth_rebase'])['auth'] == 1:
                                    quay_entry_offset_baee312 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerArm64E'])['dyld_chained_ptr_arm64e_auth_rebase'])['target']
                                else:
                                    quay_entry_offset_baee312 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerArm64E'])['dyld_chained_ptr_arm64e_rebase'])['target']
                                if quay_dyld_chained_ptr_format(_name_boundary.attributes(quay_starts_3d31dbe)['pointer_format']) != quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_ARM64E or _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerArm64E'])['dyld_chained_ptr_arm64e_auth_rebase'])['auth']:
                                    quay_entry_offset_baee312 += _name_boundary.attributes(_name_boundary.attributes(quay_image_f2d6319)['vm'])['vm_base_addr']
                            elif quay_dyld_chained_ptr_format(_name_boundary.attributes(quay_starts_3d31dbe)['pointer_format']) == quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_64:
                                quay_entry_offset_baee312 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerGeneric64'])['dyld_chained_ptr_64_rebase'])['target']
                            elif quay_dyld_chained_ptr_format(_name_boundary.attributes(quay_starts_3d31dbe)['pointer_format']) == quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_64_OFFSET:
                                quay_entry_offset_baee312 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer64_02a6b25)['generic64'])['ChainedPointerGeneric64'])['dyld_chained_ptr_64_rebase'])['target'] + _name_boundary.attributes(_name_boundary.attributes(quay_image_f2d6319)['vm'])['vm_base_addr']
                            elif quay_dyld_chained_ptr_format(_name_boundary.attributes(quay_starts_3d31dbe)['pointer_format']) == quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_32 or quay_dyld_chained_ptr_format(_name_boundary.attributes(quay_starts_3d31dbe)['pointer_format']) == quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_32_CACHE:
                                quay_entry_offset_baee312 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer32_8077cdf)['generic32'])['dyld_chained_ptr_32_rebase'])['target']
                            elif quay_dyld_chained_ptr_format(_name_boundary.attributes(quay_starts_3d31dbe)['pointer_format']) == quay_dyld_chained_ptr_format.DYLD_CHAINED_PTR_32_CACHE:
                                quay_entry_offset_baee312 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_pointer32_8077cdf)['generic32'])['dyld_chained_ptr_32_firmware_rebase'])['target']
                            else:
                                print(f"Unknown rebase pointer format {_name_boundary.attributes(quay_starts_3d31dbe)['pointer_format']}")
                            quay_rebases_07f1425[_name_boundary.attributes(quay_pointer64_02a6b25)['off'] + _name_boundary.attributes(_name_boundary.attributes(quay_image_f2d6319)['vm'])['vm_base_addr']] = quay_entry_offset_baee312
                        quay_chain_entry_address_b63c0e0 += quay_next_entry_stride_count_699e44f * quay_stride_size_3891437
                        if quay_chain_entry_address_b63c0e0 > quay_page_addr_8a818a4 + _name_boundary.attributes(quay_starts_3d31dbe)['page_size']:
                            _name_boundary.attributes(quay_log)['error']('Pointer left page, bailing fixup processing, binary is malformed')
                            quay_fixups_done_b5c693e = True
                        if quay_next_entry_stride_count_699e44f == 0:
                            quay_fixups_done_b5c693e = True
        return quay_cls_d293e50(quay_syms_14b01a1, quay_rebases_07f1425)

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_613ebfa', 'args': 'quay_args_c07b7c5', 'kwargs': 'quay_kwargs_f28826b'}, 'from_values')
    def quay_from_values(quay_cls_613ebfa, *quay_args_c07b7c5, **quay_kwargs_f28826b):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_39ff616'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_39ff616):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_fb36143', 'symbols': 'quay_symbols_a10091c', 'rebases': 'quay_rebases_dd276b4'}, '__init__')
    def __init__(quay_self_fb36143, quay_symbols_a10091c, quay_rebases_dd276b4=None):
        if quay_rebases_dd276b4 is None:
            quay_rebases_dd276b4 = {}
        _name_boundary.attributes(quay_self_fb36143)['symbols'] = quay_symbols_a10091c
        _name_boundary.attributes(quay_self_fb36143)['rebases'] = quay_rebases_dd276b4
quay_export_node = _name_boundary.named_record('export_node', ['text', 'offset', 'flags'])

@_name_boundary.class_contract('ExportNode', {'name': 'quay_name', 'offset': 'quay_offset', 'flags': 'quay_flags', 'children': 'quay_children'})
class quay_ExportNode:
    """
    Tree node for export trie entries, with name segment, offset, flags, and children.
    """

    @_name_boundary.callable_contract({'self': 'quay_self_e90eb32', 'name': 'quay_name_146381b', 'offset': 'quay_offset_e67df06', 'flags': 'quay_flags_1aeea39'}, '__init__')
    def __init__(quay_self_e90eb32, quay_name_146381b: str, quay_offset_e67df06: quay_Optional[int], quay_flags_1aeea39: quay_Optional[int]):
        _name_boundary.attributes(quay_self_e90eb32)['name'] = quay_name_146381b
        _name_boundary.attributes(quay_self_e90eb32)['offset'] = quay_offset_e67df06
        _name_boundary.attributes(quay_self_e90eb32)['flags'] = quay_flags_1aeea39
        _name_boundary.attributes(quay_self_e90eb32)['children']: quay_List['ExportNode'] = []

    @_name_boundary.callable_contract({'self': 'quay_self_15cd325'}, '__repr__')
    def __repr__(quay_self_15cd325):
        return f"ExportNode(name={_name_boundary.attributes(quay_self_15cd325)['name']!r}, offset={_name_boundary.attributes(quay_self_15cd325)['offset']}, flags={_name_boundary.attributes(quay_self_15cd325)['flags']}, children={len(_name_boundary.attributes(quay_self_15cd325)['children'])})"

@_name_boundary.class_contract('ExportTrie', {'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes', 'from_image': 'quay_from_image', '_read_node_tree_iter': 'quay__read_node_tree_iter', 'print_tree': 'quay_print_tree', 'raw': 'quay_raw', 'nodes': 'quay_nodes', 'symbols': 'quay_symbols', 'root': 'quay_root'})
class quay_ExportTrie(quay_Constructable):

    @_name_boundary.callable_contract({'self': 'quay_self_fe64a13'}, '__init__')
    def __init__(quay_self_fe64a13):
        _name_boundary.attributes(quay_self_fe64a13)['raw'] = bytearray()
        _name_boundary.attributes(quay_self_fe64a13)['nodes']: quay_List[quay_export_node] = []
        _name_boundary.attributes(quay_self_fe64a13)['symbols']: quay_List[quay_Symbol] = []
        _name_boundary.attributes(quay_self_fe64a13)['root']: quay_Optional[quay_ExportNode] = None

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_776bda1', 'args': 'quay_args_4c7afb3', 'kwargs': 'quay_kwargs_786866b'}, 'from_values')
    def quay_from_values(quay_cls_776bda1, *quay_args_4c7afb3, **quay_kwargs_786866b):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_2305fbd'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_2305fbd):
        return _name_boundary.attributes(quay_self_2305fbd)['raw']

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_644554c', 'image': 'quay_image_62eaf6e', 'export_start': 'quay_export_start_57eed4f', 'export_size': 'quay_export_size_a1c02ff'}, 'from_image')
    def quay_from_image(quay_cls_644554c, quay_image_62eaf6e: quay_Image, quay_export_start_57eed4f: int, quay_export_size_a1c02ff: int) -> 'ExportTrie':
        quay_trie_172fc40 = quay_ExportTrie()
        quay_endpoint_1f23066 = quay_export_start_57eed4f + quay_export_size_a1c02ff
        _name_boundary.attributes(quay_trie_172fc40)['root'] = _name_boundary.attributes(quay_cls_644554c)['_read_node_tree_iter'](quay_image_62eaf6e, quay_export_start_57eed4f, quay_endpoint_1f23066)
        quay_flat_5ce84aa: quay_List[quay_export_node] = []
        quay_symbols_4a65150: quay_List[quay_Symbol] = []
        quay_stack_1be153f = [_name_boundary.attributes(quay_trie_172fc40)['root']]
        while quay_stack_1be153f:
            quay_node_3ffa9b0 = quay_stack_1be153f.pop()
            if _name_boundary.attributes(quay_node_3ffa9b0)['offset'] is not None:
                quay_flat_5ce84aa.append(quay_export_node(_name_boundary.attributes(quay_node_3ffa9b0)['name'], _name_boundary.attributes(quay_node_3ffa9b0)['offset'], _name_boundary.attributes(quay_node_3ffa9b0)['flags']))
                quay_symbols_4a65150.append(_name_boundary.attributes(quay_Symbol)['from_values'](_name_boundary.attributes(quay_node_3ffa9b0)['name'], _name_boundary.attributes(quay_node_3ffa9b0)['offset'], False))
            quay_stack_1be153f.extend(_name_boundary.attributes(quay_node_3ffa9b0)['children'][::-1])
        _name_boundary.attributes(quay_trie_172fc40)['nodes'] = quay_flat_5ce84aa
        _name_boundary.attributes(quay_trie_172fc40)['symbols'] = quay_symbols_4a65150
        _name_boundary.attributes(quay_trie_172fc40)['raw'] = _name_boundary.attributes(quay_image_62eaf6e)['read_bytearray'](quay_export_start_57eed4f, quay_export_size_a1c02ff)
        return quay_trie_172fc40

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_d4c14ab', 'image': 'quay_image_18e1cc9', 'trie_start': 'quay_trie_start_cea7cc3', 'endpoint': 'quay_endpoint_4c0f319'}, '_read_node_tree_iter')
    def quay__read_node_tree_iter(quay_cls_d4c14ab, quay_image_18e1cc9: quay_Image, quay_trie_start_cea7cc3: int, quay_endpoint_4c0f319: int) -> quay_ExportNode:
        """
        Read a trie node and build an ExportNode tree using an explicit stack
        instead of recursion.
        """
        quay_root_b921f70 = quay_ExportNode('', None, None)
        quay_stack_6788f59: quay_List[quay_ExportNode, int] = [(quay_root_b921f70, quay_trie_start_cea7cc3)]
        while quay_stack_6788f59:
            quay_node_111dc93, quay_cursor_cb6cbd5 = quay_stack_6788f59.pop()
            quay_terminal_size_02ce414, quay_cursor_cb6cbd5 = _name_boundary.attributes(quay_image_18e1cc9)['read_uleb128'](quay_cursor_cb6cbd5)
            quay_child_start_82d1446 = quay_cursor_cb6cbd5 + quay_terminal_size_02ce414
            if quay_terminal_size_02ce414 != 0:
                quay___aec01c7, quay_cursor_cb6cbd5 = _name_boundary.attributes(quay_image_18e1cc9)['read_uleb128'](quay_cursor_cb6cbd5)
                quay_flags_463f87f = _name_boundary.attributes(quay_image_18e1cc9)['read_uint'](quay_cursor_cb6cbd5, 1)
                quay_cursor_cb6cbd5 += 1
                quay_offset_27a2c9d, quay_cursor_cb6cbd5 = _name_boundary.attributes(quay_image_18e1cc9)['read_uleb128'](quay_cursor_cb6cbd5)
                _name_boundary.attributes(quay_node_111dc93)['offset'] = quay_offset_27a2c9d
                _name_boundary.attributes(quay_node_111dc93)['flags'] = quay_flags_463f87f
            quay_cursor_cb6cbd5 = quay_child_start_82d1446
            quay_branches_b7b378a = _name_boundary.attributes(quay_image_18e1cc9)['read_uint'](quay_cursor_cb6cbd5, 1)
            quay_cursor_cb6cbd5 += 1
            quay_branch_infos_9e0b6cf: quay_List[str, int] = []
            for quay___aec01c7 in range(quay_branches_b7b378a):
                quay_proc_str_6f55f0d = _name_boundary.attributes(quay_image_18e1cc9)['read_cstr'](quay_cursor_cb6cbd5)
                quay_cursor_cb6cbd5 += len(quay_proc_str_6f55f0d) + 1
                quay_offset_loc_3923948, quay_cursor_cb6cbd5 = _name_boundary.attributes(quay_image_18e1cc9)['read_uleb128'](quay_cursor_cb6cbd5)
                if quay_offset_loc_3923948 == 0:
                    _name_boundary.attributes(quay_log)['error']('Export trie has zero offset, table is malformed and unparsable')
                    return quay_ExportNode('', None, None)
                quay_branch_infos_9e0b6cf.append((quay_proc_str_6f55f0d, quay_offset_loc_3923948))
            for quay_proc_str_6f55f0d, quay_offset_loc_3923948 in reversed(quay_branch_infos_9e0b6cf):
                quay_child_6d396b0 = quay_ExportNode(_name_boundary.attributes(quay_node_111dc93)['name'] + quay_proc_str_6f55f0d, None, None)
                _name_boundary.attributes(quay_node_111dc93)['children'].append(quay_child_6d396b0)
                quay_stack_6788f59.append((quay_child_6d396b0, quay_trie_start_cea7cc3 + quay_offset_loc_3923948))
        return quay_root_b921f70

    @_name_boundary.callable_contract({'self': 'quay_self_6ff5975'}, 'print_tree')
    def quay_print_tree(quay_self_6ff5975):
        """
        Print the export trie as an ASCII tree starting from the root,
        using an explicit stack instead of recursion.
        """
        if not _name_boundary.attributes(quay_self_6ff5975)['root']:
            print('<empty export trie>')
            return
        quay_stack_e8d56a0 = [(_name_boundary.attributes(quay_self_6ff5975)['root'], '', True)]
        while quay_stack_e8d56a0:
            quay_node_7e55181, quay_prefix_79efa98, quay_is_last_63a9ac0 = quay_stack_e8d56a0.pop()
            quay_connector_9b6fa1c = '└── ' if quay_is_last_63a9ac0 else '├── '
            if _name_boundary.attributes(quay_node_7e55181)['offset'] is not None:
                quay_label_3a8c873 = f"{_name_boundary.attributes(quay_node_7e55181)['name']} (offset=0x{_name_boundary.attributes(quay_node_7e55181)['offset']:x}, flags=0x{_name_boundary.attributes(quay_node_7e55181)['flags']:x})"
            else:
                quay_label_3a8c873 = _name_boundary.attributes(quay_node_7e55181)['name'] or '<root>'
            print(quay_prefix_79efa98 + quay_connector_9b6fa1c + quay_label_3a8c873)
            quay_child_prefix_ac3eb20 = quay_prefix_79efa98 + ('    ' if quay_is_last_63a9ac0 else '│   ')
            for quay_idx_cf5586e, quay_child_a83f3b8 in enumerate(reversed(_name_boundary.attributes(quay_node_7e55181)['children'])):
                quay_last_818acf4 = quay_idx_cf5586e == 0
                quay_stack_e8d56a0.append((quay_child_a83f3b8, quay_child_prefix_ac3eb20, quay_last_818acf4))
quay_action = _name_boundary.named_record('action', ['vmaddr', 'libname', 'item'])
quay_record = _name_boundary.named_record('record', ['off', 'seg_index', 'seg_offset', 'lib_ordinal', 'type', 'flags', 'name', 'addend', 'special_dylib'])

@_name_boundary.class_contract('BindingTable', {'_load_symbol_table': 'quay__load_symbol_table', '_create_action_list': 'quay__create_action_list', '_load_binding_info': 'quay__load_binding_info', 'image': 'quay_image', 'import_stack': 'quay_import_stack', 'actions': 'quay_actions', 'lookup_table': 'quay_lookup_table', 'link_table': 'quay_link_table', 'symbol_table': 'quay_symbol_table'})
class quay_BindingTable:
    """
    The binding table contains a ton of information related to the binding info in the image

    .lookup_table - Contains a map of address -> Symbol declarations which should be used for processing off-image
    symbol decorations

    .symbol_table - Contains a full list of symbols declared in the binding info. Avoid iterating through this for
    speed purposes.

    .actions - contains a list of, you guessed it, actions.

    .import_stack - contains a fairly raw unprocessed list of binding info commands

    """

    @_name_boundary.callable_contract({'self': 'quay_self_7761955', 'image': 'quay_image_b066be5', 'table_start': 'quay_table_start_6b3351e', 'table_size': 'quay_table_size_efd2cf5'}, '__init__')
    def __init__(quay_self_7761955, quay_image_b066be5: quay_Image, quay_table_start_6b3351e: int, quay_table_size_efd2cf5: int):
        """
        Pass a image to be processed

        :param image: image to be processed
        :type image: Image
        """
        _name_boundary.attributes(quay_self_7761955)['image'] = quay_image_b066be5
        _name_boundary.attributes(quay_self_7761955)['import_stack'] = _name_boundary.attributes(quay_self_7761955)['_load_binding_info'](quay_table_start_6b3351e, quay_table_size_efd2cf5)
        _name_boundary.attributes(quay_self_7761955)['actions'] = _name_boundary.attributes(quay_self_7761955)['_create_action_list']()
        _name_boundary.attributes(quay_self_7761955)['lookup_table'] = {}
        _name_boundary.attributes(quay_self_7761955)['link_table'] = {}
        _name_boundary.attributes(quay_self_7761955)['symbol_table'] = _name_boundary.attributes(quay_self_7761955)['_load_symbol_table']()

    @_name_boundary.callable_contract({'self': 'quay_self_4fca821'}, '_load_symbol_table')
    def quay__load_symbol_table(quay_self_4fca821) -> quay_List[quay_Symbol]:
        quay_table_77fe244 = []
        for quay_act_d37e14d in _name_boundary.attributes(quay_self_4fca821)['actions']:
            if quay_act_d37e14d.item:
                quay_sym_2dec87c = _name_boundary.attributes(quay_Symbol)['from_values'](quay_act_d37e14d.item, _name_boundary.attributes(quay_act_d37e14d)['vmaddr'], external=True, ordinal=_name_boundary.attributes(quay_act_d37e14d)['libname'])
                quay_table_77fe244.append(quay_sym_2dec87c)
                _name_boundary.attributes(quay_self_4fca821)['lookup_table'][_name_boundary.attributes(quay_act_d37e14d)['vmaddr']] = quay_sym_2dec87c
        return quay_table_77fe244

    @_name_boundary.callable_contract({'self': 'quay_self_1717a14'}, '_create_action_list')
    def quay__create_action_list(quay_self_1717a14) -> quay_List[quay_action]:
        quay_actions_2f3d4f2 = []
        for quay_bind_command_7de67a0 in _name_boundary.attributes(quay_self_1717a14)['import_stack']:
            quay_segment_3c573d7 = list(_name_boundary.attributes(_name_boundary.attributes(quay_self_1717a14)['image'])['segments'].values())[quay_bind_command_7de67a0.seg_index]
            quay_vm_address_f459b83 = _name_boundary.attributes(quay_segment_3c573d7)['vm_address'] + quay_bind_command_7de67a0.seg_offset
            try:
                quay_lib_4fda5f3 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_1717a14)['image'])['linked_images'][_name_boundary.attributes(quay_bind_command_7de67a0)['lib_ordinal'] - 1])['install_name']
            except IndexError:
                quay_lib_4fda5f3 = str(_name_boundary.attributes(quay_bind_command_7de67a0)['lib_ordinal'])
            quay_item_cf162a0 = _name_boundary.attributes(quay_bind_command_7de67a0)['name']
            quay_actions_2f3d4f2.append(quay_action(quay_vm_address_f459b83 & 68719476735, quay_lib_4fda5f3, quay_item_cf162a0))
        return quay_actions_2f3d4f2

    @_name_boundary.callable_contract({'self': 'quay_self_e8ee232', 'table_start': 'quay_table_start_41c98ec', 'table_size': 'quay_table_size_3469038'}, '_load_binding_info')
    def quay__load_binding_info(quay_self_e8ee232, quay_table_start_41c98ec: int, quay_table_size_3469038: int) -> quay_List[quay_record]:
        quay_read_address_8699fb3 = quay_table_start_41c98ec
        quay_import_stack_39d98bc = []
        quay_threaded_stack_be53686 = []
        quay_uses_threaded_bind_6f6861d = False
        while True:
            if quay_read_address_8699fb3 - quay_table_size_3469038 >= quay_table_start_41c98ec:
                break
            quay_seg_index_d15482f = 0
            quay_seg_offset_2356fba = 0
            quay_lib_ordinal_68c3919 = 0
            quay_btype_ef14905 = 0
            quay_flags_4c6901b = 0
            quay_name_3fb5973 = ''
            quay_addend_751bbd4 = 0
            quay_special_dylib_2495b2d = 0
            while True:
                quay_binding_opcode_f4e891b = _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['read_uint'](quay_read_address_8699fb3, 1) & 240
                quay_value_aa9f27d = _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['read_uint'](quay_read_address_8699fb3, 1) & 15
                _name_boundary.attributes(quay_log)['debug_tm'](f"{_name_boundary.attributes(quay_BINDING_OPCODE(quay_binding_opcode_f4e891b))['name']}: {hex(quay_value_aa9f27d)}")
                quay_cmd_start_addr_5413880 = quay_read_address_8699fb3
                quay_read_address_8699fb3 += 1
                if _name_boundary.attributes(quay_log)['LOG_LEVEL'] == _name_boundary.attributes(quay_imagequay)['LogLevel'].DEBUG_TOO_MUCH:
                    quay_segment_8f2935e = list(_name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['segments'].values())[quay_seg_index_d15482f]
                    quay_vm_address_c371d36 = _name_boundary.attributes(quay_segment_8f2935e)['vm_address'] + quay_seg_offset_2356fba
                    _name_boundary.attributes(quay_log)['debug_tm'](f"@ {hex(quay_cmd_start_addr_5413880)} (-> {hex(quay_vm_address_c371d36)}) op->{_name_boundary.attributes(quay_BINDING_OPCODE(quay_binding_opcode_f4e891b))['name']} current->{quay_name_3fb5973}")
                if quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.THREADED:
                    if quay_value_aa9f27d == quay_BIND_SUBOPCODE_THREADED_SET_BIND_ORDINAL_TABLE_SIZE_ULEB:
                        quay_a_table_size_b501e92, quay_read_address_8699fb3 = _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['read_uleb128'](quay_read_address_8699fb3)
                        quay_uses_threaded_bind_6f6861d = True
                    elif quay_value_aa9f27d == quay_BIND_SUBOPCODE_THREADED_APPLY:
                        pass
                if quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.DONE:
                    quay_import_stack_39d98bc.append(quay_record(quay_cmd_start_addr_5413880, quay_seg_index_d15482f, quay_seg_offset_2356fba, quay_lib_ordinal_68c3919, quay_btype_ef14905, quay_flags_4c6901b, quay_name_3fb5973, quay_addend_751bbd4, quay_special_dylib_2495b2d))
                    break
                elif quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.SET_DYLIB_ORDINAL_IMM:
                    quay_lib_ordinal_68c3919 = quay_value_aa9f27d
                elif quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.SET_DYLIB_ORDINAL_ULEB:
                    quay_lib_ordinal_68c3919, quay_read_address_8699fb3 = _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['read_uleb128'](quay_read_address_8699fb3)
                elif quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.SET_DYLIB_SPECIAL_IMM:
                    quay_special_dylib_2495b2d = 1
                    quay_lib_ordinal_68c3919 = quay_value_aa9f27d
                elif quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.SET_SYMBOL_TRAILING_FLAGS_IMM:
                    quay_flags_4c6901b = quay_value_aa9f27d
                    quay_name_3fb5973 = _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['read_cstr'](quay_read_address_8699fb3)
                    quay_read_address_8699fb3 += len(quay_name_3fb5973) + 1
                elif quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.SET_TYPE_IMM:
                    quay_btype_ef14905 = quay_value_aa9f27d
                elif quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.SET_ADDEND_SLEB:
                    quay_addend_751bbd4, quay_read_address_8699fb3 = _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['read_uleb128'](quay_read_address_8699fb3)
                elif quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.SET_SEGMENT_AND_OFFSET_ULEB:
                    quay_seg_index_d15482f = quay_value_aa9f27d
                    quay_seg_offset_2356fba, quay_read_address_8699fb3 = _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['read_uleb128'](quay_read_address_8699fb3)
                elif quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.ADD_ADDR_ULEB:
                    quay_o_b97edfd, quay_read_address_8699fb3 = _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['read_uleb128'](quay_read_address_8699fb3)
                    quay_seg_offset_2356fba += quay_o_b97edfd
                elif quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.DO_BIND_ADD_ADDR_ULEB:
                    quay_import_stack_39d98bc.append(quay_record(quay_cmd_start_addr_5413880, quay_seg_index_d15482f, quay_seg_offset_2356fba, quay_lib_ordinal_68c3919, quay_btype_ef14905, quay_flags_4c6901b, quay_name_3fb5973, quay_addend_751bbd4, quay_special_dylib_2495b2d))
                    quay_seg_offset_2356fba += _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['ptr_size']
                    quay_o_b97edfd, quay_read_address_8699fb3 = _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['read_uleb128'](quay_read_address_8699fb3)
                    quay_seg_offset_2356fba += quay_o_b97edfd
                elif quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.DO_BIND_ADD_ADDR_IMM_SCALED:
                    quay_import_stack_39d98bc.append(quay_record(quay_cmd_start_addr_5413880, quay_seg_index_d15482f, quay_seg_offset_2356fba, quay_lib_ordinal_68c3919, quay_btype_ef14905, quay_flags_4c6901b, quay_name_3fb5973, quay_addend_751bbd4, quay_special_dylib_2495b2d))
                    quay_seg_offset_2356fba = quay_seg_offset_2356fba + quay_value_aa9f27d * _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['ptr_size'] + _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['ptr_size']
                elif quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.DO_BIND_ULEB_TIMES_SKIPPING_ULEB:
                    quay_count_1221439, quay_read_address_8699fb3 = _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['read_uleb128'](quay_read_address_8699fb3)
                    quay_skip_611aa0e, quay_read_address_8699fb3 = _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['read_uleb128'](quay_read_address_8699fb3)
                    for quay_i_89c187e in range(0, quay_count_1221439):
                        quay_import_stack_39d98bc.append(quay_record(quay_cmd_start_addr_5413880, quay_seg_index_d15482f, quay_seg_offset_2356fba, quay_lib_ordinal_68c3919, quay_btype_ef14905, quay_flags_4c6901b, quay_name_3fb5973, quay_addend_751bbd4, quay_special_dylib_2495b2d))
                        quay_seg_offset_2356fba += quay_skip_611aa0e + _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['ptr_size']
                elif quay_binding_opcode_f4e891b == quay_BINDING_OPCODE.DO_BIND:
                    if not quay_uses_threaded_bind_6f6861d:
                        quay_import_stack_39d98bc.append(quay_record(quay_cmd_start_addr_5413880, quay_seg_index_d15482f, quay_seg_offset_2356fba, quay_lib_ordinal_68c3919, quay_btype_ef14905, quay_flags_4c6901b, quay_name_3fb5973, quay_addend_751bbd4, quay_special_dylib_2495b2d))
                        quay_seg_offset_2356fba += _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['ptr_size']
                    else:
                        quay_threaded_stack_be53686.append(quay_record(quay_cmd_start_addr_5413880, quay_seg_index_d15482f, quay_seg_offset_2356fba, quay_lib_ordinal_68c3919, quay_btype_ef14905, quay_flags_4c6901b, quay_name_3fb5973, quay_addend_751bbd4, quay_special_dylib_2495b2d))
                        quay_seg_offset_2356fba += _name_boundary.attributes(_name_boundary.attributes(quay_self_e8ee232)['image'])['ptr_size']
        return quay_import_stack_39d98bc
_name_boundary.module_contract(globals(), {'action': 'quay_action', 'MH_MAGIC_64': 'quay_MH_MAGIC_64', 'macho_is_malformed': 'quay_macho_is_malformed', 'ExportTrie': 'quay_ExportTrie', 'CPUType': 'quay_CPUType', 'CodesignInfo': 'quay_CodesignInfo', 'Image': 'quay_Image', 'Tuple': 'quay_Tuple', 'ExportNode': 'quay_ExportNode', 'MH_FLAGS': 'quay_MH_FLAGS', 'Union': 'quay_Union', 'ignore': 'quay_ignore', 'MachOImageLoader': 'quay_MachOImageLoader', 'MachOImageHeader': 'quay_MachOImageHeader', 'ChainedFixups': 'quay_ChainedFixups', 'namedtuple': 'quay_namedtuple', 'PlatformType': 'quay_PlatformType', 'BIND_SUBOPCODE_THREADED_SET_BIND_ORDINAL_TABLE_SIZE_ULEB': 'quay_BIND_SUBOPCODE_THREADED_SET_BIND_ORDINAL_TABLE_SIZE_ULEB', 'MisalignedVM': 'quay_MisalignedVM', 'BindingTable': 'quay_BindingTable', 'export_node': 'quay_export_node', 'LOAD_COMMAND': 'quay_LOAD_COMMAND', 'BINDING_OPCODE': 'quay_BINDING_OPCODE', 'BIND_SUBOPCODE_THREADED_APPLY': 'quay_BIND_SUBOPCODE_THREADED_APPLY', 'Constructable': 'quay_Constructable', 'ktool': 'quay_imagequay', 'SymbolTable': 'quay_SymbolTable', 'Slice': 'quay_Slice', 'record': 'quay_record', 'SymbolType': 'quay_SymbolType', 'Optional': 'quay_Optional', 'LOAD_COMMAND_MAP': 'quay_LOAD_COMMAND_MAP', 'List': 'quay_List', 'LinkedImage': 'quay_LinkedImage', 'CPUSubTypeARM64': 'quay_CPUSubTypeARM64', 'Dict': 'quay_Dict', 'Segment': 'quay_Segment', 'MachOAlignmentError': 'quay_MachOAlignmentError', 'Symbol': 'quay_Symbol', 'MH_FILETYPE': 'quay_MH_FILETYPE', 'os_version': 'quay_os_version', 'bytes_to_hex': 'quay_bytes_to_hex', 'MH_MAGIC': 'quay_MH_MAGIC', 'log': 'quay_log'})
