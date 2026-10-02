#!/usr/bin/env python3
# Derived from src/ktool/ktool_script.py; original copyright and license in ORIGIN.md and LICENSE.

#
#  ktool | MAIN SCRIPT
#  ktool
#
#  This file is the main command-line script providing utilities for using ktool.
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary
import json as quay_json
import os as quay_os
import os.path as _boundary_import_os_path
import os as quay_os
import sys as quay_sys
import threading as quay_threading
import urllib.request as _boundary_import_urllib_request
import urllib as quay_urllib
from argparse import ArgumentParser as quay_ArgumentParser
from collections import namedtuple as quay_namedtuple
from enum import Enum as quay_Enum
from typing import Union as quay_Union
from packaging import version as quay_packaging_version
from imagequay.file_ops import safe_open as open, metadata_leaf, set_overwrite
from imagequay.update_reader import read_release
from imagequay.toolkit_api import patch_image_header
import imagequay as quay_imagequay
from imagequay_layout import quay_LOAD_COMMAND as quay_LOAD_COMMAND
from imagequay import quay_MachOFileType as quay_MachOFileType, quay_IMAGEQUAY_VERSION as quay_IMAGEQUAY_VERSION, quay_ignore as quay_ignore, quay_LogLevel as quay_LogLevel, quay_Table as quay_Table
from imagequay_support.diagnostics import quay_log as quay_log
from imagequay.swift_model import *
from imagequay.failure_types import *
from imagequay.stub_documents import quay_FatMachOGenerator as quay_FatMachOGenerator
from imagequay.formatting import quay_opts as quay_opts, quay_version_output as quay_version_output, quay_imagequay_print as quay_imagequay_print, quay_get_terminal_size as quay_get_terminal_size
from imagequay.terminal_views import quay_ImageQuayScreen as quay_ImageQuayScreen, quay_external_hard_fault_teardown as quay_external_hard_fault_teardown
from imagequay.kernel_images import quay_KernelCache as quay_KernelCache, quay_Kext as quay_Kext, quay_EmbeddedKext as quay_EmbeddedKext
from imagequay_layout.binary_records import *
quay_UPDATE_AVAILABLE = False
quay_MAIN_PARSER = None
quay_MMAP_ENABLED = False
quay_print = quay_imagequay_print

@_name_boundary.callable_contract({'version': 'quay_version_891781d'}, 'handle_version')
def quay_handle_version(quay_version_891781d: str):
    """ Used by check_for_update """
    return quay_packaging_version.parse(quay_version_891781d)

def quay_check_for_update():
    global quay_UPDATE_AVAILABLE
    release = read_release(quay_IMAGEQUAY_VERSION)
    quay_UPDATE_AVAILABLE = bool(release)
    return release

@_name_boundary.class_contract('KToolError', {})
class quay_ImageQuayError(quay_Enum):
    ArgumentError = 1
    FiletypeError = 2
    MalformedMachOError = 3
    ProcessingError = 4

@_name_boundary.callable_contract({'error': 'quay_error_8650721', 'msg': 'quay_msg_36049ff'}, 'exit_with_error')
def quay_exit_with_error(quay_error_8650721: quay_ImageQuayError, quay_msg_36049ff):
    quay_print(f"Encountered an Error ({_name_boundary.attributes(quay_error_8650721)['name']}):\n" + f'{quay_msg_36049ff}', file=quay_sys.stderr)
    exit(_name_boundary.attributes(quay_error_8650721)['value'])

@_name_boundary.callable_contract({'parser': 'quay_parser_59e36ff', 'dest': 'quay_dest_73f6eef'}, 'arg_dest_to_name')
def quay_arg_dest_to_name(quay_parser_59e36ff: quay_Union[None, quay_ArgumentParser], quay_dest_73f6eef):
    """
    Convert dest (an argument destination variable name) to the actual flag used to set it (do_headers -> --headers)

    Uses internal properties from argparse, this also iterates through all subparsers

    :param parser: main argument parser to pull the original flag from
    :param dest: destination variable name
    :return:
    """
    quay_args_23daa86 = {}
    for quay_k_784e676, quay_v_bd92ed0 in _name_boundary.attributes(quay_parser_59e36ff._option_string_actions)['items']():
        quay_args_23daa86[str(quay_v_bd92ed0.dest)] = quay_k_784e676
    for quay_parser_name_e875f26, quay_sparser_077688e in _name_boundary.attributes(quay_parser_59e36ff._subparsers._group_actions[0].choices)['items']():
        for quay_k_784e676, quay_v_bd92ed0 in _name_boundary.attributes(quay_sparser_077688e._option_string_actions)['items']():
            quay_args_23daa86[str(quay_v_bd92ed0.dest)] = quay_k_784e676
    if quay_dest_73f6eef not in quay_args_23daa86:
        raise AttributeError(f'{quay_dest_73f6eef} destination not in any arguments.')
    return quay_args_23daa86[quay_dest_73f6eef]

@_name_boundary.callable_contract({'args': 'quay_args_be948ee', 'always': 'quay_always_b8c02a0', 'one_of': 'quay_one_of_4f96c67'}, 'require_args')
def quay_require_args(quay_args_be948ee, quay_always_b8c02a0=None, quay_one_of_4f96c67=None):
    """
    This is a quick macro to enforce argument requirements for different commands.

    If a check fails, it'll print usage for the subcommand and exit the program.

    :param args: Parsed argument object
    :param always: Arguments that *must* be passed
    :param one_of: At least one of these arguments must be passed, and must evaluate as True
    :return:
    """
    if quay_always_b8c02a0:
        quay_missing_502e327 = []
        for quay_i_1430961 in quay_always_b8c02a0:
            if not _name_boundary.has_attribute(quay_args_be948ee, quay_i_1430961):
                quay_missing_502e327.append(quay_i_1430961)
            elif not _name_boundary.read_attribute(quay_args_be948ee, quay_i_1430961):
                quay_missing_502e327.append(quay_i_1430961)
        if len(quay_missing_502e327) > 0:
            quay_print(_name_boundary.attributes(quay_args_be948ee)['func'].__doc__)
            if len(quay_missing_502e327) == 1:
                quay_error_str_2c0abfd = f'Missing required argument {quay_arg_dest_to_name(quay_MAIN_PARSER, quay_missing_502e327[0])}'
                quay_exit_with_error(quay_ImageQuayError.ArgumentError, quay_error_str_2c0abfd)
            else:
                quay_error_str_2c0abfd = 'Missing required arguments: '
                quay_error_str_2c0abfd += ', '.join([quay_arg_dest_to_name(quay_MAIN_PARSER, quay_i_e62361b) for quay_i_e62361b in quay_missing_502e327])
                quay_exit_with_error(quay_ImageQuayError.ArgumentError, quay_error_str_2c0abfd)
    if quay_one_of_4f96c67:
        quay_found_one_31946b3 = False
        for quay_i_1430961 in quay_one_of_4f96c67:
            if _name_boundary.has_attribute(quay_args_be948ee, quay_i_1430961):
                if _name_boundary.read_attribute(quay_args_be948ee, quay_i_1430961):
                    quay_found_one_31946b3 = True
                    break
        if not quay_found_one_31946b3:
            quay_print(_name_boundary.attributes(quay_args_be948ee)['func'].__doc__)
            quay_missing_args_0af5c63 = ', '.join([quay_arg_dest_to_name(quay_MAIN_PARSER, quay_i_125c904) for quay_i_125c904 in quay_one_of_4f96c67])
            quay_exit_with_error(quay_ImageQuayError.ArgumentError, f'Missing one of {quay_missing_args_0af5c63}')

@_name_boundary.callable_contract({}, 'main')
def quay_main():
    quay_parser_dcbfa10 = quay_ArgumentParser(description='imagequay')
    quay_parser_dcbfa10.add_argument('--bench', dest='bench', action='store_true')
    quay_parser_dcbfa10.add_argument('--membench', dest='membench', action='store_true')
    quay_parser_dcbfa10.add_argument('-v', dest='logging_level', type=int)
    quay_parser_dcbfa10.add_argument('-c', dest='no_color', action='store_true')
    quay_parser_dcbfa10.add_argument('-f', dest='force_load', action='store_true')
    quay_parser_dcbfa10.add_argument('-V', dest='get_vers', action='store_true')
    quay_parser_dcbfa10.add_argument('--check-updates', action='store_true', help='Explicitly query ImageQuay release metadata; no software is downloaded')
    quay_parser_dcbfa10.add_argument('--overwrite', action='store_true', help='Atomically replace existing regular output files')
    quay_parser_dcbfa10.add_argument('--mmap', dest='mmap', action='store_true', help='Compatibility option; uses bounded private snapshot IO')
    quay_parser_dcbfa10.set_defaults(func=quay_help_prompt, bench=False, membench=False, force_load=False, mmap=False, logging_level=1, get_vers=False)
    quay_subparsers_aaffb0e = quay_parser_dcbfa10.add_subparsers(help='sub-command help')
    quay_commands_3070ec3 = quay_MachOFileCommands
    quay_parser_open_ce10caf = quay_subparsers_aaffb0e.add_parser('open', help='open imagequay GUI and browse file')
    quay_parser_open_ce10caf.add_argument('filename', nargs='?', default='')
    quay_parser_open_ce10caf.add_argument('--hard-fail', dest='hard_fail', action='store_true')
    quay_parser_open_ce10caf.set_defaults(func=_name_boundary.attributes(quay_commands_3070ec3)['_open'], hard_fail=False)
    quay_parser_json_61bc9c5 = quay_subparsers_aaffb0e.add_parser('json', help='Dump Image metadata as json')
    quay_parser_json_61bc9c5.add_argument('--with-objc', dest='with_objc', action='store_true')
    quay_parser_json_61bc9c5.add_argument('filename', nargs='?', default='')
    quay_parser_json_61bc9c5.set_defaults(func=_name_boundary.attributes(quay_commands_3070ec3)['serialize'], with_objc=False)
    quay_parser_insert_d48e048 = quay_subparsers_aaffb0e.add_parser('insert', help='Insert data into MachO Binary')
    quay_parser_insert_d48e048.add_argument('filename', nargs='?', default='')
    quay_parser_insert_d48e048.add_argument('--lc', dest='lc', help='Type of Load Command to insert')
    quay_parser_insert_d48e048.add_argument('--payload', dest='payload', help='Payload (if required) for insertion')
    quay_parser_insert_d48e048.add_argument('--out', dest='out', help='Output file destination for patches')
    quay_parser_insert_d48e048.set_defaults(func=_name_boundary.attributes(quay_commands_3070ec3)['insert'], out=None, lc=None, payload=None)
    quay_parser_edit_edad4d1 = quay_subparsers_aaffb0e.add_parser('edit', help='Edit attributes of the MachO')
    quay_parser_edit_edad4d1.add_argument('filename', nargs='?', default='')
    quay_parser_edit_edad4d1.add_argument('--iname', dest='iname', help='Modify the Install Name of a image')
    quay_parser_edit_edad4d1.add_argument('--apad', dest='apad', help='Add MachO Header Padding (not yet implemented, ignore this flag please)')
    quay_parser_edit_edad4d1.add_argument('--out', dest='out', help='Output file destination for patches')
    quay_parser_edit_edad4d1.set_defaults(func=_name_boundary.attributes(quay_commands_3070ec3)['edit'], out=None, iname=None, apad=None)
    quay_parser_lipo_45b0baa = quay_subparsers_aaffb0e.add_parser('lipo', help='Extract/Combine slices')
    quay_parser_lipo_45b0baa.add_argument('--extract', dest='extract', type=str, help='Extract a slice (--extract arm64)')
    quay_parser_lipo_45b0baa.add_argument('--out', dest='out', help='Output File')
    quay_parser_lipo_45b0baa.add_argument('--create', dest='combine', action='store_true', help='Combine files to create a fat mach-o image')
    quay_parser_lipo_45b0baa.add_argument('filename', nargs='*', default='')
    quay_parser_lipo_45b0baa.set_defaults(func=_name_boundary.attributes(quay_commands_3070ec3)['lipo'], out='', combine=False)
    quay_parser_info_2428030 = quay_subparsers_aaffb0e.add_parser('info', help='Print Info about a MachO image')
    quay_parser_info_2428030.add_argument('--slice', dest='slice_index', type=int, help='Specify Index of Slice (in FAT MachO) to examine')
    quay_parser_info_2428030.add_argument('--file', dest='get_fileinfo', action='store_true', help='Print basic file info')
    quay_parser_info_2428030.add_argument('--vm', dest='get_vm', action='store_true', help='Print VM Mapping for MachO image')
    quay_parser_info_2428030.add_argument('filename', nargs='?', default='')
    quay_parser_info_2428030.set_defaults(func=_name_boundary.attributes(quay_commands_3070ec3)['info'], get_vm=False, get_lcs=False, slice_index=0)
    quay_parser_dump_4b1334d = quay_subparsers_aaffb0e.add_parser('dump', help='Dump items (headers) from binary')
    quay_parser_dump_4b1334d.add_argument('--slice', dest='slice_index', type=int, help='Specify Index of Slice (in FAT MachO) to examine')
    quay_parser_dump_4b1334d.add_argument('--headers', dest='do_headers', action='store_true')
    quay_parser_dump_4b1334d.add_argument('--class', dest='get_class')
    quay_parser_dump_4b1334d.add_argument('--fdec', dest='forward_declare', action='store_true')
    quay_parser_dump_4b1334d.add_argument('--use-stab-for-sel', dest='usfs', action='store_true')
    quay_parser_dump_4b1334d.add_argument('--hard-fail', dest='hard_fail', action='store_true')
    quay_parser_dump_4b1334d.add_argument('--sorted', dest='sort_headers', action='store_true')
    quay_parser_dump_4b1334d.add_argument('--tbd', dest='do_tbd', action='store_true')
    quay_parser_dump_4b1334d.add_argument('--out', dest='outdir', help='Directory to dump headers into')
    quay_parser_dump_4b1334d.add_argument('--force-misaligned-vm', dest='force_misaligned', action='store_true', help='Force misaligned VM')
    quay_parser_dump_4b1334d.add_argument('filename', nargs='?', default='')
    quay_parser_dump_4b1334d.set_defaults(func=_name_boundary.attributes(quay_commands_3070ec3)['dump'], do_headers=False, usfs=False, sort_headers=False, do_tbd=False, slice_index=0, hard_fail=False, get_class=None, forward_declare=False, force_misaligned=False)
    quay_parser_list_bdaab44 = quay_subparsers_aaffb0e.add_parser('list', help='Print various lists')
    quay_parser_list_bdaab44.add_argument('--slice', dest='slice_index', type=int, help='Specify Index of Slice (in FAT MachO) to examine')
    quay_parser_list_bdaab44.add_argument('--classes', dest='get_classes', action='store_true', help='Print class list')
    quay_parser_list_bdaab44.add_argument('--protocols', dest='get_protos', action='store_true', help='Print Protocol list')
    quay_parser_list_bdaab44.add_argument('--stypes', dest='get_swift_types', action='store_true', help='Print Swift Types')
    quay_parser_list_bdaab44.add_argument('--linked', dest='get_linked', action='store_true', help='Print list of linked libraries')
    quay_parser_list_bdaab44.add_argument('--cmds', dest='get_lcs', action='store_true', help='Print Load Commands')
    quay_parser_list_bdaab44.add_argument('--funcs', dest='get_fstarts', action='store_true', help='Print Function Starts')
    quay_parser_list_bdaab44.add_argument('filename', nargs='?', default='')
    quay_parser_list_bdaab44.set_defaults(func=_name_boundary.attributes(quay_commands_3070ec3)['_list'], get_lcs=False, get_classes=False, get_protos=False, get_linked=False, slice_index=0, get_swift_types=False)
    quay_parser_symbols_d9ec4bf = quay_subparsers_aaffb0e.add_parser('symbols', help='Print various symbols')
    quay_parser_symbols_d9ec4bf.add_argument('--imports', dest='get_imports', action='store_true', help='Print Imports')
    quay_parser_symbols_d9ec4bf.add_argument('--imp-acts', dest='get_actions', action='store_true', help='Print Raw Binding Imports')
    quay_parser_symbols_d9ec4bf.add_argument('--symtab', dest='get_symtab', action='store_true', help='Print out the symtab')
    quay_parser_symbols_d9ec4bf.add_argument('--exports', dest='get_exports', action='store_true', help='Print exports')
    quay_parser_symbols_d9ec4bf.add_argument('--slice', dest='slice_index', type=int, help='Specify Index of Slice (in FAT MachO) to examine')
    quay_parser_symbols_d9ec4bf.add_argument('filename', nargs='?', default='')
    quay_parser_symbols_d9ec4bf.set_defaults(func=_name_boundary.attributes(quay_commands_3070ec3)['symbols'], get_imports=False, get_actions=False, get_exports=False, get_symtab=False, slice_index=0)
    quay_parser_kcache_bb3a9df = quay_subparsers_aaffb0e.add_parser('kcache', help='Kernel Cache Processing')
    quay_parser_kcache_bb3a9df.add_argument('--info', dest='get_info', action='store_true', help='Basic KCache Info')
    quay_parser_kcache_bb3a9df.add_argument('--kexts', dest='get_kexts', action='store_true', help='List kexts embedded')
    quay_parser_kcache_bb3a9df.add_argument('--kext', dest='get_kext')
    quay_parser_kcache_bb3a9df.add_argument('--extract', dest='do_extract')
    quay_parser_kcache_bb3a9df.add_argument('filename', nargs='?', default='')
    quay_parser_kcache_bb3a9df.set_defaults(func=_name_boundary.attributes(quay_commands_3070ec3)['kcache'], get_kext=None, get_info=False, do_extract=None, get_kexts=False)
    quay_parser_ent_55c6d95 = quay_subparsers_aaffb0e.add_parser('cs', help='Codesign processing')
    quay_parser_ent_55c6d95.add_argument('--ent', dest='get_ent', action='store_true')
    quay_parser_ent_55c6d95.add_argument('--slice', dest='slice_index', type=int, help='Specify Index of Slice (in FAT MachO) to examine')
    quay_parser_ent_55c6d95.add_argument('filename', nargs='?', default='')
    quay_parser_ent_55c6d95.set_defaults(func=_name_boundary.attributes(quay_commands_3070ec3)['ent'], get_ent=False, slice_index=0)
    quay_parser_trie_unwrap_c94ba3d = quay_subparsers_aaffb0e.add_parser('untrie', help='Unwrap export trie')
    quay_parser_trie_unwrap_c94ba3d.add_argument('filename', nargs='?', default='')
    quay_parser_trie_unwrap_c94ba3d.add_argument('--slice', dest='slice_index', type=int, help='Specify Index of Slice (in FAT MachO) to examine')
    quay_parser_trie_unwrap_c94ba3d.set_defaults(func=_name_boundary.attributes(quay_commands_3070ec3)['trie_unwrap'], slice_index=0)
    quay_parser_dcbfa10.print_help = quay_help_prompt
    quay_args_4f71994 = quay_parser_dcbfa10.parse_args()
    global quay_MAIN_PARSER
    quay_MAIN_PARSER = quay_parser_dcbfa10
    set_overwrite(quay_args_4f71994.overwrite)
    if quay_args_4f71994.check_updates:
        release = quay_check_for_update()
        if release:
            quay_print(f'ImageQuay release available: {release}')
    if quay_args_4f71994.get_vers:
        quay_version_output()
        exit()
    if quay_args_4f71994.no_color:
        _name_boundary.attributes(quay_opts)['DISABLE_COLOR'] = True
    if not _name_boundary.has_attribute(quay_args_4f71994, 'filename'):
        quay_help_prompt()
        exit()
    if not _name_boundary.attributes(quay_args_4f71994)['filename'] or _name_boundary.attributes(quay_args_4f71994)['filename'] == '':
        quay_print(_name_boundary.attributes(quay_args_4f71994)['func'].__doc__)
        exit()
    _name_boundary.attributes(quay_log)['LOG_LEVEL'] = quay_LogLevel(max(min(quay_args_4f71994.logging_level, 5), -1))
    if quay_args_4f71994.force_load:
        _name_boundary.attributes(quay_ignore)['MALFORMED'] = True
    if quay_args_4f71994.mmap:
        global quay_MMAP_ENABLED
        quay_MMAP_ENABLED = True
    if quay_args_4f71994.membench:
        import tracemalloc as quay_tracemalloc_41568d0
        _name_boundary.attributes(quay_tracemalloc_41568d0)['start'](10)
        _name_boundary.attributes(quay_args_4f71994)['func'](quay_args_4f71994)
        quay_snapshot_dd17b0c = quay_tracemalloc_41568d0.take_snapshot()
        quay_top_stats_96298dd = quay_snapshot_dd17b0c.statistics('lineno')
        quay_print('[ Top 10 ]')
        for quay_stat_9f11671 in quay_top_stats_96298dd[:10]:
            quay_print(quay_stat_9f11671)
    elif quay_args_4f71994.bench:
        import cProfile as quay_cProfile_c466b65
        import pstats as quay_pstats_eeb1b35
        quay_profile_a2233df = quay_cProfile_c466b65.Profile()
        quay_profile_a2233df.runcall(_name_boundary.attributes(quay_args_4f71994)['func'], quay_args_4f71994)
        quay_ps_d2ac0c3 = quay_pstats_eeb1b35.Stats(quay_profile_a2233df)
        quay_ps_d2ac0c3.sort_stats('time', 'cumtime')
        quay_ps_d2ac0c3.print_stats(10)
    else:
        try:
            _name_boundary.attributes(quay_args_4f71994)['func'](quay_args_4f71994)
        except quay_UnsupportedFiletypeException:
            quay_exit_with_error(quay_ImageQuayError.FiletypeError, f"{_name_boundary.attributes(quay_args_4f71994)['filename']} is not a valid MachO Binary")
        except FileNotFoundError as quay_ex_a867a75:
            quay_exit_with_error(quay_ImageQuayError.ArgumentError, f"{_name_boundary.attributes(quay_args_4f71994)['filename']} does not exist")
        except (OSError, ValueError) as local_error:
            quay_exit_with_error(quay_ImageQuayError.ProcessingError, str(local_error))
        except quay_MalformedMachOException:
            quay_exit_with_error(quay_ImageQuayError.MalformedMachOError, 'Malformed Mach-O. Bounds checks cannot be bypassed by -f.')
    if quay_UPDATE_AVAILABLE:
        quay_print(f'\n\nUpdate Available ---')
        quay_print('Review ImageQuay releases at https://github.com/dhtfish-98/ImageQuay/releases')
    exit(0)

@_name_boundary.callable_contract({}, 'help_prompt')
def quay_help_prompt():
    """Usage: imagequay <global flags> [command] <flags> [filename]

Commands:

GUI (Still in active development) ---
    imagequay open [filename] - Open the imagequay command line GUI and browse a file

MachO Editing ---
    insert - Utils for inserting load commands into MachO Binaries
    edit - Utils for editing MachO Binaries
    lipo - Utilities for combining/separating slices in fat MachO files.

MachO Analysis ---
    dump - Tools to reconstruct certain files (headers, .tbds) from compiled MachOs
    json - Dump image metadata as json
    cs - Codesigning info
    kcache - Kernel cache specific tools
    list - Print various lists (ObjC Classes, etc.)
    symbols - Print various tables (Symbols, imports, exports)
    info - Print misc info about the target mach-o

Run `imagequay [command]` for info/examples on using that command

Global Flags:
    -f - Hide unsupported-command warnings; binary bounds remain enforced.
    --check-updates - Explicitly query ImageQuay release metadata.
    --overwrite - Atomically replace existing regular output files.
    -v [-1 through 5] - Log verbosiy. -1 completely silences logging.
    -V - Print version string (`imagequay -V | cat`) to disable the animation
        """
    quay_print(quay_help_prompt.__doc__)

@_name_boundary.callable_contract({'image': 'quay_image_91d6ed8'}, 'process_patches')
def quay_process_patches(quay_image_91d6ed8) -> 'Image':
    try:
        return quay_imagequay.reload_image(quay_image_91d6ed8)
    except quay_MalformedMachOException:
        quay_exit_with_error(quay_ImageQuayError.ProcessingError, 'Reloading MachO after patch failed. This is an issue with my patch code. Please file an issue on https://github.com/kritantadev/imagequay.')

@_name_boundary.class_contract('MachOFileCommands', {'_open': 'quay__open', 'serialize': 'quay_serialize', 'ent': 'quay_ent', 'symbols': 'quay_symbols', 'insert': 'quay_insert', 'edit': 'quay_edit', 'lipo': 'quay_lipo', '_list': 'quay__list', 'info': 'quay_info', 'dump': 'quay_dump', 'kcache': 'quay_kcache', 'trie_unwrap': 'quay_trie_unwrap'})
class quay_MachOFileCommands:

    @staticmethod
    @_name_boundary.callable_contract({'args': 'quay_args_3762b00'}, '_open')
    def quay__open(quay_args_3762b00):
        """
    imagequay open [filename]
        """
        try:
            _name_boundary.attributes(quay_log)['LOG_LEVEL'] = quay_LogLevel.DEBUG
            quay_screen_3d2b659 = quay_ImageQuayScreen(_name_boundary.attributes(quay_args_3762b00)['hard_fail'])
            _name_boundary.attributes(quay_log)['LOG_FUNC'] = _name_boundary.attributes(quay_screen_3d2b659)['ktool_dbg_print_func']
            _name_boundary.attributes(quay_log)['LOG_ERR'] = _name_boundary.attributes(quay_screen_3d2b659)['ktool_dbg_print_err_func']
            _name_boundary.attributes(quay_screen_3d2b659)['load_file'](_name_boundary.attributes(quay_args_3762b00)['filename'], quay_MMAP_ENABLED)
        except KeyboardInterrupt:
            quay_external_hard_fault_teardown()
            quay_print('Hard Faulted. This was likely due to a curses error causing a freeze while rendering.')
            exit(64)
        except Exception as quay_ex_45400c5:
            quay_external_hard_fault_teardown()
            quay_print('Hard fault in GUI due to uncaught exception:')
            raise quay_ex_45400c5
        quay_external_hard_fault_teardown()

    @staticmethod
    @_name_boundary.callable_contract({'args': 'quay_args_f9f8cd7'}, 'serialize')
    def quay_serialize(quay_args_f9f8cd7):
        """
    ----------
    Dump image metadata as json

    > imagequay json [filename]

    Dump image metadata including objc metadata

    > imagequay json --with-objc [filename]
        """
        quay_require_args(quay_args_f9f8cd7, one_of=['filename'])
        _name_boundary.attributes(quay_log)['LOG_LEVEL'] = quay_LogLevel(-1)
        with open(_name_boundary.attributes(quay_args_f9f8cd7)['filename'], 'rb') as quay_fp_7a7db60:
            quay_macho_file_02ce159 = quay_imagequay.load_macho_file(quay_fp_7a7db60, use_mmaped_io=quay_MMAP_ENABLED)
            quay_out_dict_17e0fe9 = {'filetype': _name_boundary.attributes(_name_boundary.attributes(quay_macho_file_02ce159)['type'])['name']}
            quay_slices_55021ee = []
            for quay_macho_slice_26b9088 in _name_boundary.attributes(quay_macho_file_02ce159)['slices']:
                quay_image_2563097 = _name_boundary.attributes(quay_imagequay)['load_image'](quay_macho_slice_26b9088)
                quay_image_dict_24dc865 = _name_boundary.attributes(quay_image_2563097)['serialize']()
                quay_slice_dict_6e8faa2 = {'offset': _name_boundary.attributes(quay_macho_slice_26b9088)['offset'], 'size': _name_boundary.attributes(quay_macho_slice_26b9088)['size'], 'type': _name_boundary.attributes(_name_boundary.attributes(quay_macho_slice_26b9088)['type'])['name'], 'subtype': _name_boundary.attributes(_name_boundary.attributes(quay_macho_slice_26b9088)['subtype'])['name'], 'image': quay_image_dict_24dc865}
                quay_slices_55021ee.append(quay_slice_dict_6e8faa2)
            quay_out_dict_17e0fe9['slices'] = quay_slices_55021ee
            if quay_args_f9f8cd7.with_objc:
                quay_objc_image_6d4d8f6 = quay_imagequay.load_objc_metadata(quay_image_2563097)
                quay_out_dict_17e0fe9['objc'] = _name_boundary.attributes(quay_objc_image_6d4d8f6)['serialize']()
            if quay_imagequay.util.OUT_IS_TTY:
                quay_print(quay_imagequay.util.highlight_json(quay_json.dumps(quay_out_dict_17e0fe9, indent=4, sort_keys=True)))
            else:
                quay_print(quay_json.dumps(quay_out_dict_17e0fe9, indent=4, sort_keys=True))

    @staticmethod
    @_name_boundary.callable_contract({'args': 'quay_args_5899664'}, 'ent')
    def quay_ent(quay_args_5899664):
        """
    ----------
    Interact with codesigning info

    Dump entitlements
    > imagequay cs --ent [filename]
        """
        quay_require_args(quay_args_5899664, one_of=['get_ent'])
        if quay_args_5899664.get_ent:
            with open(_name_boundary.attributes(quay_args_5899664)['filename'], 'rb') as quay_fd_781e06d:
                quay_image_60f0909 = _name_boundary.attributes(quay_imagequay)['load_image'](quay_fd_781e06d, quay_args_5899664.slice_index, load_symtab=False, load_imports=False, use_mmaped_io=quay_MMAP_ENABLED)
                quay_ents_17269e3 = _name_boundary.attributes(_name_boundary.attributes(quay_image_60f0909)['codesign_info'])['entitlements']
                if quay_imagequay.util.OUT_IS_TTY:
                    quay_print(quay_imagequay.util.highlight_xml(quay_ents_17269e3))
                else:
                    quay_print(quay_ents_17269e3)

    @staticmethod
    @_name_boundary.callable_contract({'args': 'quay_args_9677310'}, 'symbols')
    def quay_symbols(quay_args_9677310):
        """
    ----------
    List symbol imports/exports

    Print the list of imported symbols
    > imagequay symbols --imports [filename]

    Print the list of exported symbols
    > imagequay symbols --exports [filename]

    Print the symbol table
    > imagequay symbols --symtab [filename]
        """
        quay_require_args(quay_args_9677310, one_of=['get_imports', 'get_actions', 'get_exports', 'get_symtab'])
        if quay_args_9677310.get_exports:
            with open(_name_boundary.attributes(quay_args_9677310)['filename'], 'rb') as quay_fd_a1893bd:
                quay_image_9a8a69e = _name_boundary.attributes(quay_imagequay)['load_image'](quay_fd_a1893bd, quay_args_9677310.slice_index, load_symtab=False, load_imports=False, use_mmaped_io=quay_MMAP_ENABLED)
                quay_table_4067a60 = quay_Table()
                _name_boundary.attributes(quay_table_4067a60)['titles'] = ['Address', 'Symbol']
                for quay_symbol_da9d4e4 in _name_boundary.attributes(quay_image_9a8a69e)['exports']:
                    _name_boundary.attributes(quay_table_4067a60)['rows'].append([hex(_name_boundary.attributes(quay_symbol_da9d4e4)['address']), _name_boundary.attributes(quay_symbol_da9d4e4)['fullname']])
                quay_print(_name_boundary.attributes(quay_table_4067a60)['fetch_all'](quay_get_terminal_size().columns))
        if quay_args_9677310.get_symtab:
            with open(_name_boundary.attributes(quay_args_9677310)['filename'], 'rb') as quay_fd_a1893bd:
                quay_image_9a8a69e = _name_boundary.attributes(quay_imagequay)['load_image'](quay_fd_a1893bd, quay_args_9677310.slice_index, load_imports=False, load_exports=False, use_mmaped_io=quay_MMAP_ENABLED)
                quay_table_4067a60 = quay_Table()
                _name_boundary.attributes(quay_table_4067a60)['titles'] = ['Address', 'Name']
                for quay_sym_218e447 in _name_boundary.attributes(_name_boundary.attributes(quay_image_9a8a69e)['symbol_table'])['table']:
                    _name_boundary.attributes(quay_table_4067a60)['rows'].append([hex(_name_boundary.attributes(quay_sym_218e447)['address']), _name_boundary.attributes(quay_sym_218e447)['fullname']])
                quay_print(_name_boundary.attributes(quay_table_4067a60)['fetch_all'](quay_get_terminal_size().columns - 1))
        if quay_args_9677310.get_imports:
            with open(_name_boundary.attributes(quay_args_9677310)['filename'], 'rb') as quay_fd_a1893bd:
                quay_image_9a8a69e = _name_boundary.attributes(quay_imagequay)['load_image'](quay_fd_a1893bd, quay_args_9677310.slice_index, load_exports=False, load_symtab=False, use_mmaped_io=quay_MMAP_ENABLED)
                quay_import_symbols_25a1a52 = {}
                quay_symbol_da9d4e4 = _name_boundary.named_record('symbol', ['addr', 'name', 'image', 'from_table'])
                for quay_addr_e9fa383, quay_sym_218e447 in _name_boundary.attributes(_name_boundary.attributes(quay_image_9a8a69e)['import_table'])['items']():
                    try:
                        quay_import_symbols_25a1a52[hex(quay_addr_e9fa383)] = quay_symbol_da9d4e4(hex(quay_addr_e9fa383), _name_boundary.attributes(quay_sym_218e447)['fullname'], _name_boundary.attributes(_name_boundary.attributes(quay_image_9a8a69e)['linked_images'][int(_name_boundary.attributes(quay_sym_218e447)['ordinal']) - 1])['install_name'], _name_boundary.attributes(quay_sym_218e447)['attr'])
                    except IndexError:
                        quay_import_symbols_25a1a52[hex(quay_addr_e9fa383)] = quay_symbol_da9d4e4(hex(quay_addr_e9fa383), _name_boundary.attributes(quay_sym_218e447)['fullname'], 'ordinal: ' + str(int(_name_boundary.attributes(quay_sym_218e447)['ordinal'])), _name_boundary.attributes(quay_sym_218e447)['attr'])
                quay_table_4067a60 = quay_Table()
                _name_boundary.attributes(quay_table_4067a60)['titles'] = ['Addr', 'Symbol', 'Image', 'Binding']
                for quay___cf34d85, quay_sym_218e447 in _name_boundary.attributes(quay_import_symbols_25a1a52)['items']():
                    _name_boundary.attributes(quay_table_4067a60)['rows'].append([_name_boundary.attributes(quay_sym_218e447)['addr'], _name_boundary.attributes(quay_sym_218e447)['name'], _name_boundary.attributes(quay_sym_218e447)['image'], quay_sym_218e447.from_table])
                quay_print(_name_boundary.attributes(quay_table_4067a60)['fetch_all'](quay_get_terminal_size().columns))
        elif quay_args_9677310.get_actions:
            with open(_name_boundary.attributes(quay_args_9677310)['filename'], 'rb') as quay_fd_a1893bd:
                quay_image_9a8a69e = _name_boundary.attributes(quay_imagequay)['load_image'](quay_fd_a1893bd, quay_args_9677310.slice_index, use_mmaped_io=quay_MMAP_ENABLED)
                quay_print('\nBinding Info'.ljust(60, '-') + '\n')
                for quay_sym_218e447 in _name_boundary.attributes(_name_boundary.attributes(quay_image_9a8a69e)['binding_table'])['symbol_table']:
                    try:
                        quay_print(f"{hex(_name_boundary.attributes(quay_sym_218e447)['address']).ljust(15, ' ')} | {_name_boundary.attributes(_name_boundary.attributes(quay_image_9a8a69e)['linked_images'][int(_name_boundary.attributes(quay_sym_218e447)['ordinal']) - 1])['install_name']} | {_name_boundary.attributes(quay_sym_218e447)['name'].ljust(20, ' ')} | {_name_boundary.attributes(quay_sym_218e447)['dec_type']}")
                    except IndexError:
                        pass
                quay_print('\nWeak Binding Info'.ljust(60, '-') + '\n')
                for quay_sym_218e447 in _name_boundary.attributes(_name_boundary.attributes(quay_image_9a8a69e)['weak_binding_table'])['symbol_table']:
                    try:
                        quay_print(f"{hex(_name_boundary.attributes(quay_sym_218e447)['address']).ljust(15, ' ')} | {_name_boundary.attributes(_name_boundary.attributes(quay_image_9a8a69e)['linked_images'][int(_name_boundary.attributes(quay_sym_218e447)['ordinal']) - 1])['install_name']} | {_name_boundary.attributes(quay_sym_218e447)['name'].ljust(20, ' ')} | {_name_boundary.attributes(quay_sym_218e447)['dec_type']}")
                    except IndexError:
                        pass
                quay_print('\nLazy Binding Info'.ljust(60, '-') + '\n')
                for quay_sym_218e447 in _name_boundary.attributes(_name_boundary.attributes(quay_image_9a8a69e)['lazy_binding_table'])['symbol_table']:
                    try:
                        quay_print(f"{hex(_name_boundary.attributes(quay_sym_218e447)['address']).ljust(15, ' ')} | {_name_boundary.attributes(_name_boundary.attributes(quay_image_9a8a69e)['linked_images'][int(_name_boundary.attributes(quay_sym_218e447)['ordinal']) - 1])['install_name']} | {_name_boundary.attributes(quay_sym_218e447)['name'].ljust(20, ' ')} | {_name_boundary.attributes(quay_sym_218e447)['dec_type']}")
                    except IndexError:
                        pass

    @staticmethod
    @_name_boundary.callable_contract({'args': 'quay_args_7ac92ac'}, 'insert')
    def quay_insert(quay_args_7ac92ac):
        """
    ----------
    Utils for inserting load commands into mach-o binaries

    insert a LOAD_DYLIB command
    > imagequay insert --lc load --payload /Dylib/Install/Name/Here.dylib --out <output filename> [filename]

    commands currently supported:
        load: LOAD_DYLIB
        load-weak: LOAD_WEAK_DYLIB
        lazy-load: LAZY_LOAD_DYLIB
        load-upward: LOAD_UPWARD_DYLIB
        """
        quay_require_args(quay_args_7ac92ac, always=['lc'])
        quay_lc_90ad0bb = None
        if quay_args_7ac92ac.lc == 'load':
            quay_lc_90ad0bb = quay_LOAD_COMMAND.LOAD_DYLIB
        elif quay_args_7ac92ac.lc == 'load-weak' or quay_args_7ac92ac.lc == 'load_weak':
            quay_lc_90ad0bb = quay_LOAD_COMMAND.LOAD_WEAK_DYLIB
        elif quay_args_7ac92ac.lc in ['load_lazy', 'load-lazy', 'lazy-load', 'lazy_load']:
            quay_lc_90ad0bb = quay_LOAD_COMMAND.LAZY_LOAD_DYLIB
        elif quay_args_7ac92ac.lc == 'load-upward' or quay_args_7ac92ac.lc == 'load_upward':
            quay_lc_90ad0bb = quay_LOAD_COMMAND.LOAD_UPWARD_DYLIB
        quay_patched_libraries_6b7150e = []
        with open(_name_boundary.attributes(quay_args_7ac92ac)['filename'], 'rb') as quay_fp_d791fba:
            quay_macho_file_ec7f357 = quay_imagequay.load_macho_file(quay_fp_d791fba, use_mmaped_io=quay_MMAP_ENABLED)
            for quay_macho_slice_2db4d0d in _name_boundary.attributes(quay_macho_file_ec7f357)['slices']:
                quay_image_470a639 = _name_boundary.attributes(quay_imagequay)['load_image'](quay_macho_slice_2db4d0d)
                quay_last_dylib_command_index_4140c1c = -1
                for quay_i_dbbf445, quay_cmd_937462b in enumerate(_name_boundary.attributes(_name_boundary.attributes(quay_image_470a639)['macho_header'])['load_commands']):
                    if isinstance(quay_cmd_937462b, quay_dylib_command):
                        quay_last_dylib_command_index_4140c1c = quay_i_dbbf445 + 1
                quay_dylib_item_727cd48 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_dylib, [24, 2, 65536, 65536])
                quay_dylib_cmd_abafa7f = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_dylib_command, [_name_boundary.attributes(quay_lc_90ad0bb)['value'], 0, _name_boundary.attributes(quay_dylib_item_727cd48)['raw']])
                quay_new_header_66c052b = _name_boundary.attributes(_name_boundary.attributes(quay_image_470a639)['macho_header'])['insert_load_command'](quay_dylib_cmd_abafa7f, quay_last_dylib_command_index_4140c1c, suffix=quay_args_7ac92ac.payload)
                patch_image_header(quay_image_470a639, quay_new_header_66c052b)
                _name_boundary.attributes(quay_log)['info']('Reloading MachO Slice to verify integrity')
                quay_image_470a639 = quay_process_patches(quay_image_470a639)
                quay_patched_libraries_6b7150e.append(quay_image_470a639)
        with open(quay_args_7ac92ac.out, 'wb') as quay_fd_5e7a32f:
            if len(quay_patched_libraries_6b7150e) > 1:
                quay_slices_f197c99 = [_name_boundary.attributes(quay_image_2f462de)['slice'] for quay_image_2f462de in quay_patched_libraries_6b7150e]
                quay_fat_generator_c65af08 = quay_FatMachOGenerator(quay_slices_f197c99)
                _name_boundary.attributes(quay_fd_5e7a32f)['write'](_name_boundary.attributes(quay_fat_generator_c65af08)['fat_head'])
                for quay_arch_dd80e7a in _name_boundary.attributes(quay_fat_generator_c65af08)['fat_archs']:
                    quay_fd_5e7a32f.seek(_name_boundary.attributes(quay_arch_dd80e7a)['offset'])
                    _name_boundary.attributes(quay_fd_5e7a32f)['write'](_name_boundary.attributes(_name_boundary.attributes(quay_arch_dd80e7a)['slice'])['full_bytes_for_slice']())
            else:
                _name_boundary.attributes(quay_fd_5e7a32f)['write'](_name_boundary.attributes(_name_boundary.attributes(quay_patched_libraries_6b7150e[0])['slice'])['full_bytes_for_slice']())

    @staticmethod
    @_name_boundary.callable_contract({'args': 'quay_args_982fb76'}, 'edit')
    def quay_edit(quay_args_982fb76):
        """
    ----------
    Utils for editing MachO Binaries

    Modify the install name of a image
    > imagequay edit --iname [Desired Install Name] --out <Output Filename> [filename]
        """
        quay_require_args(quay_args_982fb76, one_of=['iname', 'apad'])
        quay_patched_libraries_2c5b1dd = []
        if quay_args_982fb76.iname:
            quay_new_iname_1a721c5 = quay_args_982fb76.iname
            with open(_name_boundary.attributes(quay_args_982fb76)['filename'], 'rb') as quay_fp_d906ddc:
                quay_macho_file_ac1b725 = quay_imagequay.load_macho_file(quay_fp_d906ddc, use_mmaped_io=quay_MMAP_ENABLED)
                for quay_macho_slice_a085bea in _name_boundary.attributes(quay_macho_file_ac1b725)['slices']:
                    quay_image_26d299f = _name_boundary.attributes(quay_imagequay)['load_image'](quay_macho_slice_a085bea)
                    quay_id_dylib_index_ab170eb = -1
                    for quay_i_a9e031e, quay_cmd_84f53dd in enumerate(_name_boundary.attributes(_name_boundary.attributes(quay_image_26d299f)['macho_header'])['load_commands']):
                        if _name_boundary.attributes(quay_cmd_84f53dd)['cmd'] == 13:
                            quay_id_dylib_index_ab170eb = quay_i_a9e031e
                            break
                    quay_dylib_item_472f1e9 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_dylib, [24, 1, 0, 0])
                    quay_new_cmd_420ebc9 = _name_boundary.attributes(quay_Struct)['create_with_values'](quay_dylib_command, [quay_LOAD_COMMAND.ID_DYLIB, 0, _name_boundary.attributes(quay_dylib_item_472f1e9)['raw']])
                    quay_new_header_67306cf = _name_boundary.attributes(_name_boundary.attributes(quay_image_26d299f)['macho_header'])['replace_load_command'](quay_new_cmd_420ebc9, quay_id_dylib_index_ab170eb, quay_new_iname_1a721c5)
                    patch_image_header(quay_image_26d299f, quay_new_header_67306cf)
                    quay_patched_libraries_2c5b1dd.append(quay_image_26d299f)
            with open(quay_args_982fb76.out, 'wb') as quay_fd_11ed48c:
                if len(quay_patched_libraries_2c5b1dd) > 1:
                    quay_slices_a4d1637 = [_name_boundary.attributes(quay_image_f5440cf)['slice'] for quay_image_f5440cf in quay_patched_libraries_2c5b1dd]
                    quay_fat_generator_c7bd4ad = quay_FatMachOGenerator(quay_slices_a4d1637)
                    _name_boundary.attributes(quay_fd_11ed48c)['write'](_name_boundary.attributes(quay_fat_generator_c7bd4ad)['fat_head'])
                    for quay_arch_79d6e6d in _name_boundary.attributes(quay_fat_generator_c7bd4ad)['fat_archs']:
                        quay_fd_11ed48c.seek(_name_boundary.attributes(quay_arch_79d6e6d)['offset'])
                        _name_boundary.attributes(quay_fd_11ed48c)['write'](_name_boundary.attributes(_name_boundary.attributes(quay_arch_79d6e6d)['slice'])['full_bytes_for_slice']())
                else:
                    _name_boundary.attributes(quay_fd_11ed48c)['write'](_name_boundary.attributes(_name_boundary.attributes(quay_patched_libraries_2c5b1dd[0])['slice'])['full_bytes_for_slice']())

    @staticmethod
    @_name_boundary.callable_contract({'args': 'quay_args_80e3b9e'}, 'lipo')
    def quay_lipo(quay_args_80e3b9e):
        """
    ----------
    Utilities for combining/separating slices in fat MachO files.

    Extract a slice from a fat binary
    > imagequay lipo --extract [slice_name] [filename]

    Create a fat Macho Binary from multiple thin binaries
    > imagequay lipo --create [--out filename] [filenames]
        """
        quay_require_args(quay_args_80e3b9e, one_of=['combine', 'extract'])
        if quay_args_80e3b9e.combine:
            quay_output_4f66a7e = quay_args_80e3b9e.out
            if quay_output_4f66a7e == '':
                quay_output_4f66a7e = _name_boundary.attributes(quay_args_80e3b9e)['filename'][0] + '.fat'
            quay_slices_9f06043 = []
            for quay_filename_b978d4f in _name_boundary.attributes(quay_args_80e3b9e)['filename']:
                quay_fd_9c6fa1a = open(quay_filename_b978d4f, 'rb')
                quay_macho_file_fccc870 = quay_imagequay.load_macho_file(quay_fd_9c6fa1a, use_mmaped_io=quay_MMAP_ENABLED)
                if _name_boundary.attributes(quay_macho_file_fccc870)['type'] != quay_MachOFileType.THIN:
                    quay_exit_with_error(quay_ImageQuayError.ArgumentError, 'Fat mach-o passed to --create')
                quay_slices_9f06043.append(_name_boundary.attributes(quay_macho_file_fccc870)['slices'][0])
            with open(quay_output_4f66a7e, 'wb') as quay_fd_9c6fa1a:
                _name_boundary.attributes(quay_fd_9c6fa1a)['write'](_name_boundary.attributes(quay_imagequay.macho_combine(quay_slices_9f06043))['read']())
        elif quay_args_80e3b9e.extract != '':
            with open(_name_boundary.attributes(quay_args_80e3b9e)['filename'][0], 'rb') as quay_fd_9c6fa1a:
                quay_macho_file_fccc870 = quay_imagequay.load_macho_file(quay_fd_9c6fa1a, use_mmaped_io=quay_MMAP_ENABLED)
                quay_output_4f66a7e = quay_args_80e3b9e.out
                if quay_output_4f66a7e == '':
                    quay_output_4f66a7e = _name_boundary.attributes(quay_args_80e3b9e)['filename'][0] + '.' + quay_args_80e3b9e.extract.lower()
                for quay_macho_slice_eb031fc in _name_boundary.attributes(quay_macho_file_fccc870)['slices']:
                    if _name_boundary.attributes(_name_boundary.attributes(quay_macho_slice_eb031fc)['type'])['name'].lower() == quay_args_80e3b9e.extract:
                        with open(quay_output_4f66a7e, 'wb') as quay_out_625f8dd:
                            _name_boundary.attributes(quay_out_625f8dd)['write'](_name_boundary.attributes(quay_macho_slice_eb031fc)['full_bytes_for_slice']())
                        return
                quay_macho_slices_list_4822155 = [_name_boundary.attributes(_name_boundary.attributes(quay_macho_slice_b3db318)['type'])['name'].lower() for quay_macho_slice_b3db318 in _name_boundary.attributes(quay_macho_file_fccc870)['slices']]
                quay_exit_with_error(quay_ImageQuayError.ArgumentError, f'Architecture {quay_args_80e3b9e.extract} was not found (found: {quay_macho_slices_list_4822155})')

    @staticmethod
    @_name_boundary.callable_contract({'args': 'quay_args_1ed4e05'}, '_list')
    def quay__list(quay_args_1ed4e05):
        """
    ----------
    Tools for printing various lists

    To print the list of classes
    > imagequay list --classes [filename]

    To print the list of protocols
    > imagequay list --protocols [filename]

    To print a  list of linked libraries
    > imagequay list --linked [filename]

    To print a list of Load Commands and their data
    > imagequay list --cmds [filename]

    Print the list of function starts
    > imagequay list --funcs [filename]
        """
        quay_require_args(quay_args_1ed4e05, one_of=['get_classes', 'get_protos', 'get_linked', 'get_lcs', 'get_swift_types', 'get_fstarts'])
        with open(_name_boundary.attributes(quay_args_1ed4e05)['filename'], 'rb') as quay_fd_d101c1b:
            if not quay_args_1ed4e05.get_lcs and (not quay_args_1ed4e05.get_linked):
                quay_image_709e47c = _name_boundary.attributes(quay_imagequay)['load_image'](quay_fd_d101c1b, quay_args_1ed4e05.slice_index, use_mmaped_io=quay_MMAP_ENABLED)
                quay_objc_image_6fa4c47 = quay_imagequay.load_objc_metadata(quay_image_709e47c)
            else:
                quay_image_709e47c = _name_boundary.attributes(quay_imagequay)['load_image'](quay_fd_d101c1b, quay_args_1ed4e05.slice_index, False, False, False)
            if quay_args_1ed4e05.get_lcs:
                quay_table_d4951be = quay_Table(dividers=True, avoid_wrapping_titles=True)
                _name_boundary.attributes(quay_table_d4951be)['titles'] = ['Index', 'Load Command', 'Data']
                _name_boundary.attributes(quay_table_d4951be)['size_pinned_columns'] = [0, 1]
                for quay_i_d89e228, quay_lc_f3db3fe in enumerate(_name_boundary.attributes(_name_boundary.attributes(quay_image_709e47c)['macho_header'])['load_commands']):
                    quay_lc_dat_45ae441 = str(quay_lc_f3db3fe) if _name_boundary.attributes(quay_opts)['DISABLE_COLOR'] else _name_boundary.attributes(quay_lc_f3db3fe)['render_color']()
                    if quay_LOAD_COMMAND(_name_boundary.attributes(quay_lc_f3db3fe)['cmd']) in [quay_LOAD_COMMAND.LOAD_DYLIB, quay_LOAD_COMMAND.ID_DYLIB, quay_LOAD_COMMAND.SUB_CLIENT]:
                        quay_lc_dat_45ae441 += ' \n"' + _name_boundary.attributes(quay_image_709e47c)['read_cstr'](_name_boundary.attributes(quay_lc_f3db3fe)['off'] + _name_boundary.attributes(quay_lc_f3db3fe)['size'](), vm=False) + '"'
                    _name_boundary.attributes(quay_table_d4951be)['rows'].append([str(quay_i_d89e228), _name_boundary.attributes(quay_LOAD_COMMAND(_name_boundary.attributes(quay_lc_f3db3fe)['cmd']))['name'].ljust(15, ' '), quay_lc_dat_45ae441])
                quay_print(_name_boundary.attributes(quay_table_d4951be)['fetch_all'](quay_get_terminal_size().columns - 5))
            elif quay_args_1ed4e05.get_classes:
                for quay_obj_class_bf495ea in _name_boundary.attributes(quay_objc_image_6fa4c47)['classlist']:
                    quay_print(f"{_name_boundary.attributes(quay_obj_class_bf495ea)['name']}")
            elif quay_args_1ed4e05.get_swift_types:
                quay_print(f'Swift Types')
                quay_swift_image_f7f7669 = quay_imagequay.ktool.load_swift_metadata(quay_objc_image_6fa4c47)
                for quay__type_924453d in _name_boundary.attributes(quay_swift_image_f7f7669)['types']:
                    if quay__type_924453d is None:
                        continue
                    quay_print(f"{_name_boundary.attributes(quay__type_924453d)['name']} ({_name_boundary.attributes(quay__type_924453d.__class__)['__name__']})")
                    for quay_field_477f657 in _name_boundary.attributes(quay__type_924453d)['fields']:
                        quay_print('  ' + str(quay_field_477f657))
            elif quay_args_1ed4e05.get_protos:
                for quay_objc_proto_f062fc4 in _name_boundary.attributes(quay_objc_image_6fa4c47)['protolist']:
                    quay_print(f"{_name_boundary.attributes(quay_objc_proto_f062fc4)['name']}")
            elif quay_args_1ed4e05.get_linked:
                for quay_extlib_8caa84d in _name_boundary.attributes(quay_image_709e47c)['linked_images']:
                    quay_print('(Weak) ' + _name_boundary.attributes(quay_extlib_8caa84d)['install_name'] if _name_boundary.attributes(quay_extlib_8caa84d)['weak'] else '' + _name_boundary.attributes(quay_extlib_8caa84d)['install_name'])
            elif quay_args_1ed4e05.get_fstarts:
                for quay_addr_12a6240 in _name_boundary.attributes(quay_image_709e47c)['function_starts']:
                    quay_print(f"{hex(quay_addr_12a6240)} -> {(_name_boundary.attributes(_name_boundary.attributes(quay_image_709e47c)['symbols'][quay_addr_12a6240])['fullname'] if quay_addr_12a6240 in _name_boundary.attributes(quay_image_709e47c)['symbols'] else '')}")

    @staticmethod
    @_name_boundary.callable_contract({'args': 'quay_args_9ff9742'}, 'info')
    def quay_info(quay_args_9ff9742):
        """
    ----------
    Some misc info about the target mach-o

    Print generic info about a MachO file
    > imagequay info [--slice n] [filename]

    Print info about slices
    > imagequay info --file [filename]

    Print VM -> Slice -> Filename address mapping for a slice
    of a MachO file
    > imagequay info [--slice n] --vm [filename]
        """
        with open(_name_boundary.attributes(quay_args_9ff9742)['filename'], 'rb') as quay_fp_45b0f53:
            quay_image_7582a60 = _name_boundary.attributes(quay_imagequay)['load_image'](quay_fp_45b0f53, quay_args_9ff9742.slice_index, load_symtab=False, load_imports=False, load_exports=False, use_mmaped_io=quay_MMAP_ENABLED)
            if quay_args_9ff9742.get_vm:
                quay_print(_name_boundary.attributes(quay_image_7582a60)['vm'])
            elif quay_args_9ff9742.get_fileinfo:
                with open(_name_boundary.attributes(quay_args_9ff9742)['filename'], 'rb') as quay_fp_45b0f53:
                    quay_macho_file_7325425 = quay_imagequay.load_macho_file(quay_fp_45b0f53, use_mmaped_io=quay_MMAP_ENABLED)
                    quay_table_b397e7b = quay_Table()
                    _name_boundary.attributes(quay_table_b397e7b)['titles'] = ['Address', 'CPU Type', 'CPU Subtype']
                    for quay_macho_slice_c59dc3a in _name_boundary.attributes(quay_macho_file_7325425)['slices']:
                        _name_boundary.attributes(quay_table_b397e7b)['rows'].append([f"{hex(_name_boundary.attributes(quay_macho_slice_c59dc3a)['offset'])}", f"{_name_boundary.attributes(_name_boundary.attributes(quay_macho_slice_c59dc3a)['type'])['name']}", f"{_name_boundary.attributes(_name_boundary.attributes(quay_macho_slice_c59dc3a)['subtype'])['name']}"])
                    quay_print(_name_boundary.attributes(quay_table_b397e7b)['fetch_all'](quay_get_terminal_size().columns))
            else:
                quay_message_6d83227 = f"\x1b[38;5;109m{_name_boundary.attributes(quay_image_7582a60)['base_name']} \x1b[38;5;110m--- \n\x1b[38;5;109mInstall Name: \x1b[38;5;110m{_name_boundary.attributes(quay_image_7582a60)['install_name']}\n\x1b[38;5;109mFiletype: \x1b[38;5;110m{_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_image_7582a60)['macho_header'])['filetype'])['name']}\n\x1b[38;5;109mFlags: \x1b[38;5;110m{', '.join([_name_boundary.attributes(quay_i_0cf06e5)['name'] for quay_i_0cf06e5 in _name_boundary.attributes(_name_boundary.attributes(quay_image_7582a60)['macho_header'])['flags']])}\n\x1b[38;5;109mmUUID: \x1b[38;5;110m{_name_boundary.attributes(_name_boundary.attributes(quay_image_7582a60)['uuid'])['hex']().upper()}\n\x1b[38;5;109mPlatform: \x1b[38;5;110m{_name_boundary.attributes(_name_boundary.attributes(quay_image_7582a60)['platform'])['name']}\n\x1b[38;5;109mMinimum OS: \x1b[38;5;110m{_name_boundary.attributes(_name_boundary.attributes(quay_image_7582a60)['minos'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_image_7582a60)['minos'])['y']}.{_name_boundary.attributes(quay_image_7582a60)['minos'].z}\n\x1b[38;5;109mSDK Version: \x1b[38;5;110m{_name_boundary.attributes(_name_boundary.attributes(quay_image_7582a60)['sdk_version'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_image_7582a60)['sdk_version'])['y']}.{_name_boundary.attributes(quay_image_7582a60)['sdk_version'].z}"
                quay_print(quay_message_6d83227)

    @staticmethod
    @_name_boundary.callable_contract({'args': 'quay_args_662825f'}, 'dump')
    def quay_dump(quay_args_662825f):
        """
    ------
    Tools to reconstruct certain files from compiled MachOs

    Dump header for a single class
    > imagequay dump --class <classname> [filename]

    To dump a full set of headers for a bin/framework
    > imagequay dump --headers --fdec --out <directory> [filename]

    To dump .tbd files for a framework
    > imagequay dump --tbd [filename]
        """
        quay_require_args(quay_args_662825f, one_of=['do_headers', 'get_class', 'do_tbd'])
        if quay_args_662825f.get_class:
            with open(_name_boundary.attributes(quay_args_662825f)['filename'], 'rb') as quay_fp_ab23151:
                quay_image_80a1119 = _name_boundary.attributes(quay_imagequay)['load_image'](quay_fp_ab23151, quay_args_662825f.slice_index, use_mmaped_io=quay_MMAP_ENABLED, force_misaligned_vm=quay_args_662825f.force_misaligned)
                if _name_boundary.attributes(quay_image_80a1119)['name'] == '':
                    _name_boundary.attributes(quay_image_80a1119)['name'] = _name_boundary.attributes(quay_os)['path'].basename(_name_boundary.attributes(quay_args_662825f)['filename'])
                quay_objc_image_09e64c8 = quay_imagequay.load_objc_metadata(quay_image_80a1119)
                quay_objc_headers_49243eb = quay_imagequay.generate_headers(quay_objc_image_09e64c8, sort_items=quay_args_662825f.sort_headers, forward_declare_private_imports=quay_args_662825f.forward_declare)
                quay_found_e90fedc = False
                for quay_header_name_66f6264, quay_header_c5ac74b in _name_boundary.attributes(quay_objc_headers_49243eb)['items']():
                    if quay_args_662825f.get_class.lower() == quay_header_name_66f6264[:-2].lower():
                        if quay_imagequay.util.OUT_IS_TTY:
                            quay_print(_name_boundary.attributes(quay_header_c5ac74b)['generate_highlighted_text']())
                        else:
                            quay_print(quay_imagequay.util.strip_ansi(_name_boundary.attributes(quay_header_c5ac74b)['generate_highlighted_text']()))
                        quay_found_e90fedc = True
                        break
                if not quay_found_e90fedc:
                    quay_print(f'{quay_args_662825f.get_class} not found', file=quay_sys.stderr)
        if quay_args_662825f.do_headers:
            if _name_boundary.attributes(quay_args_662825f)['hard_fail']:
                _name_boundary.attributes(quay_ignore)['OBJC_ERRORS'] = False
            if quay_args_662825f.usfs:
                _name_boundary.attributes(quay_opts)['USE_SYMTAB_INSTEAD_OF_SELECTORS'] = True
            with open(_name_boundary.attributes(quay_args_662825f)['filename'], 'rb') as quay_fp_ab23151:
                quay_image_80a1119 = _name_boundary.attributes(quay_imagequay)['load_image'](quay_fp_ab23151, quay_args_662825f.slice_index, use_mmaped_io=quay_MMAP_ENABLED)
                if _name_boundary.attributes(quay_image_80a1119)['name'] == '':
                    _name_boundary.attributes(quay_image_80a1119)['name'] = _name_boundary.attributes(quay_os)['path'].basename(_name_boundary.attributes(quay_args_662825f)['filename'])
                quay_objc_image_09e64c8 = quay_imagequay.load_objc_metadata(quay_image_80a1119)
                quay_objc_headers_49243eb = quay_imagequay.generate_headers(quay_objc_image_09e64c8, sort_items=quay_args_662825f.sort_headers, forward_declare_private_imports=quay_args_662825f.forward_declare)
                for quay_header_name_66f6264, quay_header_c5ac74b in _name_boundary.attributes(quay_objc_headers_49243eb)['items']():
                    if not quay_args_662825f.outdir:
                        quay_print(f'\n\n{quay_header_name_66f6264}\n{quay_header_c5ac74b}')
                    elif quay_args_662825f.outdir == 'ndbg':
                        pass
                    else:
                        quay_os.makedirs(quay_args_662825f.outdir, exist_ok=True)
                        with open(quay_args_662825f.outdir + '/' + metadata_leaf(quay_header_name_66f6264), 'w') as quay_out_6f02b53:
                            _name_boundary.attributes(quay_out_6f02b53)['write'](str(quay_header_c5ac74b))
                    if quay_args_662825f.bench:
                        pass
        elif quay_args_662825f.do_tbd:
            with open(_name_boundary.attributes(quay_args_662825f)['filename'], 'rb') as quay_fp_ab23151:
                quay_image_80a1119 = _name_boundary.attributes(quay_imagequay)['load_image'](quay_fp_ab23151, quay_args_662825f.slice_index, use_mmaped_io=quay_MMAP_ENABLED)
                if _name_boundary.has_attribute(quay_args_662825f, 'filename'):
                    if quay_imagequay.util.OUT_IS_TTY:
                        quay_print(quay_imagequay.generate_text_based_stub(quay_image_80a1119, compatibility=True))
                    else:
                        quay_print(quay_imagequay.util.strip_ansi(quay_imagequay.generate_text_based_stub(quay_image_80a1119, compatibility=True)))

    @staticmethod
    @_name_boundary.callable_contract({'args': 'quay_args_8061661'}, 'kcache')
    def quay_kcache(quay_args_8061661):
        """
    ------
    KernelCache specific tools

    List Kext IDS (And versions, and executable names if they were found)
    > imagequay kcache --kexts [filename]

    Dump info for a specific kext
    > imagequay kcache --kext [Bundle ID or Executable Name] [filename]
        """
        quay_require_args(quay_args_8061661, one_of=['get_info', 'get_kexts', 'get_kext', 'do_extract'])
        quay_fp_45defb5 = open(_name_boundary.attributes(quay_args_8061661)['filename'], 'rb')
        quay_macho_file_0648a14 = quay_imagequay.load_macho_file(quay_fp_45defb5)
        quay_kernel_cache_194c17e = quay_KernelCache(quay_macho_file_0648a14)
        if quay_args_8061661.get_info:
            quay_print(_name_boundary.attributes(quay_kernel_cache_194c17e)['version_str'])
        elif _name_boundary.attributes(quay_args_8061661)['get_kexts']:
            for quay_kext_b5343ec in _name_boundary.attributes(quay_kernel_cache_194c17e)['kexts']:
                quay_print(f"{_name_boundary.attributes(quay_kext_b5343ec)['name']} -> {_name_boundary.attributes(quay_kext_b5343ec)['executable_name']} ({_name_boundary.attributes(quay_kext_b5343ec)['version']})")
        elif quay_args_8061661.get_kext:
            quay_kext_b5343ec = None
            for quay__kext_a66d0f4 in _name_boundary.attributes(quay_kernel_cache_194c17e)['kexts']:
                if quay_args_8061661.get_kext == _name_boundary.attributes(quay__kext_a66d0f4)['executable_name']:
                    quay_kext_b5343ec = quay__kext_a66d0f4
                    break
            if not quay_kext_b5343ec:
                for quay__kext_a66d0f4 in _name_boundary.attributes(quay_kernel_cache_194c17e)['kexts']:
                    if quay_args_8061661.get_kext == _name_boundary.attributes(quay__kext_a66d0f4)['id']:
                        quay_kext_b5343ec = quay__kext_a66d0f4
                        break
            if isinstance(quay_kext_b5343ec, quay_Kext):
                quay_bundle_text_a91f345 = f"Bundle ID: {_name_boundary.attributes(quay_kext_b5343ec)['id']}\nExecutable Name: {_name_boundary.attributes(quay_kext_b5343ec)['executable_name']}\n{_name_boundary.attributes(quay_kext_b5343ec)['info_string']}\nVersion: {_name_boundary.attributes(quay_kext_b5343ec)['version_str']}\nStart Address: {hex(_name_boundary.attributes(quay_kext_b5343ec)['start_addr'] | 18446462598732840960)}"
                quay_print(quay_bundle_text_a91f345)
            else:
                quay_print('Kext Not Found')
        elif quay_args_8061661.do_extract:
            quay_kext_b5343ec = None
            for quay__kext_a66d0f4 in _name_boundary.attributes(quay_kernel_cache_194c17e)['kexts']:
                if quay_args_8061661.do_extract == _name_boundary.attributes(quay__kext_a66d0f4)['executable_name']:
                    quay_kext_b5343ec = quay__kext_a66d0f4
                    break
            if not quay_kext_b5343ec:
                for quay__kext_a66d0f4 in _name_boundary.attributes(quay_kernel_cache_194c17e)['kexts']:
                    if quay_args_8061661.do_extract == _name_boundary.attributes(quay__kext_a66d0f4)['id']:
                        quay_kext_b5343ec = quay__kext_a66d0f4
                        break
            if isinstance(quay_kext_b5343ec, quay_EmbeddedKext):
                with open(metadata_leaf(_name_boundary.attributes(quay_kext_b5343ec)['id'].split('.')[-1]), 'wb') as quay_out_8078798:
                    _name_boundary.attributes(quay_out_8078798)['write'](_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_kext_b5343ec)['image'])['slice'])['full_bytes_for_slice']())
            else:
                quay_print('Kext Not Found')

    @staticmethod
    @_name_boundary.callable_contract({'args': 'quay_args_e874f62'}, 'trie_unwrap')
    def quay_trie_unwrap(quay_args_e874f62):
        """

        :return:
        """
        quay_require_args(quay_args_e874f62, one_of=['filename'])
        with open(_name_boundary.attributes(quay_args_e874f62)['filename'], 'rb') as quay_fd_23b5527:
            quay_image_af083c0 = _name_boundary.attributes(quay_imagequay)['load_image'](quay_fd_23b5527, quay_args_e874f62.slice_index, use_mmaped_io=quay_MMAP_ENABLED)
            _name_boundary.attributes(_name_boundary.attributes(quay_image_af083c0)['export_trie'])['print_tree']()
if __name__ == '__main__':
    quay_main()
_name_boundary.module_contract(globals(), {'KToolScreen': 'quay_ImageQuayScreen', 'os': 'quay_os', 'UPDATE_AVAILABLE': 'quay_UPDATE_AVAILABLE', 'Table': 'quay_Table', 'external_hard_fault_teardown': 'quay_external_hard_fault_teardown', 'version_output': 'quay_version_output', 'MachOFileCommands': 'quay_MachOFileCommands', 'get_terminal_size': 'quay_get_terminal_size', 'EmbeddedKext': 'quay_EmbeddedKext', 'MachOFileType': 'quay_MachOFileType', 'print': 'quay_print', 'ArgumentParser': 'quay_ArgumentParser', 'ktool_print': 'quay_imagequay_print', 'MMAP_ENABLED': 'quay_MMAP_ENABLED', 'KTOOL_VERSION': 'quay_IMAGEQUAY_VERSION', 'Union': 'quay_Union', 'ignore': 'quay_ignore', 'namedtuple': 'quay_namedtuple', 'LOAD_COMMAND': 'quay_LOAD_COMMAND', 'arg_dest_to_name': 'quay_arg_dest_to_name', 'main': 'quay_main', 'ktool': 'quay_imagequay', 'opts': 'quay_opts', 'check_for_update': 'quay_check_for_update', 'help_prompt': 'quay_help_prompt', 'KernelCache': 'quay_KernelCache', 'Kext': 'quay_Kext', 'exit_with_error': 'quay_exit_with_error', 'sys': 'quay_sys', 'require_args': 'quay_require_args', 'FatMachOGenerator': 'quay_FatMachOGenerator', 'Enum': 'quay_Enum', 'threading': 'quay_threading', 'urllib': 'quay_urllib', 'LogLevel': 'quay_LogLevel', 'process_patches': 'quay_process_patches', 'handle_version': 'quay_handle_version', 'json': 'quay_json', 'MAIN_PARSER': 'quay_MAIN_PARSER', 'log': 'quay_log', 'KToolError': 'quay_ImageQuayError'})
