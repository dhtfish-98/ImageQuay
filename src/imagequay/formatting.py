# Derived from src/ktool/util.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  util.py
#
#  This file contains miscellaneous utilities used around ktool
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary
import concurrent.futures as _boundary_import_concurrent_futures
import concurrent as quay_concurrent
import inspect as quay_inspect
import os as quay_os
import sys as quay_sys
import time as quay_time
from enum import Enum as quay_Enum
from typing import List as quay_List, Union as quay_Union
import re as quay_re
import shutil as quay_shutil
from imagequay_layout import quay_Struct as quay_Struct, quay_FAT_CIGAM as quay_FAT_CIGAM, quay_FAT_MAGIC as quay_FAT_MAGIC, quay_MH_CIGAM as quay_MH_CIGAM, quay_MH_CIGAM_64 as quay_MH_CIGAM_64, quay_MH_MAGIC as quay_MH_MAGIC, quay_MH_MAGIC_64 as quay_MH_MAGIC_64
from imagequay.failure_types import *
import importlib.metadata as quay_distribution_metadata
import imagequay_support.diagnostics as quay_log
from pygments import highlight as quay_highlight
from pygments.formatters.terminal import TerminalFormatter as quay_TerminalFormatter
try:
    from pygments.lexers.data import YamlLexer as quay_YamlLexer, JsonLexer as quay_JsonLexer
    from pygments.lexers.html import XmlLexer as quay_XmlLexer
except:
    quay_YamlLexer = None
    quay_XmlLexer = None
    quay_JsonLexer = None
try:
    quay_IMAGEQUAY_VERSION = quay_distribution_metadata.version('imagequay')
except quay_distribution_metadata.PackageNotFoundError:
    quay_IMAGEQUAY_VERSION = '1.0.5'
quay_THREAD_COUNT = max(1, (quay_os.cpu_count() or 1) - 1)
quay_OUT_IS_TTY = quay_sys.stdout.isatty()
quay_MY_DIR = __file__

@_name_boundary.callable_contract({}, 'get_terminal_size')
def quay_get_terminal_size():
    try:
        return quay_os.get_terminal_size()
    except OSError:
        return quay_shutil.get_terminal_size()

@_name_boundary.callable_contract({}, 'version_output')
def quay_version_output():
    if quay_OUT_IS_TTY:
        pass
    print(f'ImageQuay v{quay_IMAGEQUAY_VERSION}; maintained by dhtfish98; derived from ktool by cynder/0cyn')

@_name_boundary.class_contract('ignore', {'MALFORMED': 'quay_MALFORMED', 'OBJC_ERRORS': 'quay_OBJC_ERRORS'})
class quay_ignore:
    quay_MALFORMED = False
    quay_OBJC_ERRORS = True

@_name_boundary.class_contract('opts', {'DISABLE_COLOR': 'quay_DISABLE_COLOR', 'USE_SYMTAB_INSTEAD_OF_SELECTORS': 'quay_USE_SYMTAB_INSTEAD_OF_SELECTORS', 'OBJC_LOAD_ERRORS_SEND_TO_DEBUG': 'quay_OBJC_LOAD_ERRORS_SEND_TO_DEBUG'})
class quay_opts:
    quay_DISABLE_COLOR = False
    quay_USE_SYMTAB_INSTEAD_OF_SELECTORS = False
    quay_OBJC_LOAD_ERRORS_SEND_TO_DEBUG = False

@_name_boundary.class_contract('QueueItem', {'args': 'quay_args', 'func': 'quay_func'})
class quay_QueueItem:

    @_name_boundary.callable_contract({'self': 'quay_self_f4a366e'}, '__init__')
    def __init__(quay_self_f4a366e):
        _name_boundary.attributes(quay_self_f4a366e)['args'] = []
        _name_boundary.attributes(quay_self_f4a366e)['func'] = None

@_name_boundary.class_contract('Queue', {'process_item': 'quay_process_item', 'go': 'quay_go', 'items': 'quay_items', 'returns': 'quay_returns', 'multithread': 'quay_multithread'})
class quay_Queue:

    @_name_boundary.callable_contract({'self': 'quay_self_797e1b0'}, '__init__')
    def __init__(quay_self_797e1b0):
        _name_boundary.attributes(quay_self_797e1b0)['items']: quay_List[quay_QueueItem] = []
        _name_boundary.attributes(quay_self_797e1b0)['returns']: quay_List = []
        _name_boundary.attributes(quay_self_797e1b0)['multithread'] = False

    @_name_boundary.callable_contract({'self': 'quay_self_889a97c', 'item': 'quay_item_9a2cbee'}, 'process_item')
    def quay_process_item(quay_self_889a97c, quay_item_9a2cbee: quay_QueueItem):
        try:
            return _name_boundary.attributes(quay_item_9a2cbee)['func'](*_name_boundary.attributes(quay_item_9a2cbee)['args'])
        except Exception as quay_ex_f95b358:
            if not _name_boundary.attributes(quay_ignore)['OBJC_ERRORS']:
                raise quay_ex_f95b358
            _name_boundary.attributes(_name_boundary.attributes(quay_log)['log'])['error']('Queueitem failed to process for some unhandled reason.')
            return None

    @_name_boundary.callable_contract({'self': 'quay_self_56aea35'}, 'go')
    def quay_go(quay_self_56aea35):
        if _name_boundary.attributes(quay_self_56aea35)['multithread']:
            quay_futures_2d92829 = []
            with quay_concurrent.futures.ThreadPoolExecutor(max_workers=quay_THREAD_COUNT) as quay_executor_e01d5c3:
                for quay_item_e48d619 in _name_boundary.attributes(quay_self_56aea35)['items']:
                    quay_futures_2d92829.append(quay_executor_e01d5c3.submit(_name_boundary.attributes(quay_item_e48d619)['func'], *_name_boundary.attributes(quay_item_e48d619)['args']))
            _name_boundary.attributes(quay_self_56aea35)['returns'] = [quay_f_6b6eb41.result() for quay_f_6b6eb41 in quay_futures_2d92829]
        else:
            _name_boundary.attributes(quay_self_56aea35)['returns'] = [_name_boundary.attributes(quay_self_56aea35)['process_item'](quay_item_b20c7c3) for quay_item_b20c7c3 in _name_boundary.attributes(quay_self_56aea35)['items']]

@_name_boundary.callable_contract({'input': 'quay_input_5d3302b'}, 'highlight_xml')
def quay_highlight_xml(quay_input_5d3302b):
    if quay_XmlLexer:
        quay_formatter_73ba4cb = quay_TerminalFormatter()
        return quay_highlight(quay_input_5d3302b, quay_XmlLexer(), quay_formatter_73ba4cb)
    else:
        return quay_input_5d3302b

@_name_boundary.callable_contract({'input': 'quay_input_fc8a9e3'}, 'highlight_json')
def quay_highlight_json(quay_input_fc8a9e3):
    if quay_JsonLexer:
        quay_formatter_aa104ea = quay_TerminalFormatter()
        return quay_highlight(quay_input_fc8a9e3, quay_JsonLexer(), quay_formatter_aa104ea)
    else:
        return quay_input_fc8a9e3

@_name_boundary.callable_contract({}, 'macho_is_malformed')
def quay_macho_is_malformed():
    """Raise MalformedMachOException *if* we dont want to ignore bad mach-os

    :return:
    """
    if not _name_boundary.attributes(quay_ignore)['MALFORMED']:
        raise quay_MalformedMachOException

@_name_boundary.callable_contract({'val': 'quay_val_65b3ce1', 'bits': 'quay_bits_68ab937'}, 'uint_to_int')
def quay_uint_to_int(quay_val_65b3ce1, quay_bits_68ab937):
    """
    Assume an int was read from binary as an unsigned int,

    decode it as a two's compliment signed integer

    :param uint:
    :param bits:
    :return:
    """
    if quay_val_65b3ce1 & 1 << quay_bits_68ab937 - 1 != 0:
        quay_val_65b3ce1 = quay_val_65b3ce1 - (1 << quay_bits_68ab937)
    return quay_val_65b3ce1

@_name_boundary.callable_contract({'val': 'quay_val_2c5c78b'}, 'usi32_to_si32')
def quay_usi32_to_si32(quay_val_2c5c78b):
    """
    Quick hack to read the signed val of an unsigned int (Image loads all ints from bytes as unsigned ints)

    :param val:
    :return:
    """
    quay_bits_73b6b76 = 32
    if quay_val_2c5c78b & 1 << quay_bits_73b6b76 - 1 != 0:
        quay_val_2c5c78b = quay_val_2c5c78b - (1 << quay_bits_73b6b76)
    return quay_val_2c5c78b

@_name_boundary.class_contract('FileType', {})
class quay_FileType(quay_Enum):
    MachOFileType = 0
    FatMachOFileType = 1
    KCacheFileType = 2
    IMG4FileType = 64
    SharedCacheFileType = 128
    UnknownFileType = 512

@_name_boundary.callable_contract({'fp': 'quay_fp_92a678d'}, 'detect_filetype')
def quay_detect_filetype(quay_fp_92a678d) -> quay_FileType:
    quay_magic_387e39e = _name_boundary.attributes(quay_fp_92a678d)['read'](4)
    if quay_magic_387e39e in [quay_FAT_MAGIC, quay_FAT_CIGAM]:
        return quay_FileType.FatMachOFileType
    elif quay_magic_387e39e in [quay_MH_MAGIC, quay_MH_CIGAM, quay_MH_MAGIC_64, quay_MH_CIGAM_64]:
        quay_first1k_5dbac00 = _name_boundary.attributes(quay_fp_92a678d)['read'](4096)
        quay_fp_92a678d.seek(0)
        if b'__BOOTDATA\x00\x00\x00\x00\x00\x00' in quay_first1k_5dbac00:
            return quay_FileType.KCacheFileType
        else:
            return _name_boundary.attributes(quay_FileType)['MachOFileType']
    elif quay_magic_387e39e == b'dyld':
        return quay_FileType.SharedCacheFileType

@_name_boundary.class_contract('TapiYAMLWriter', {'write_out': 'quay_write_out', 'serialize_export_arch': 'quay_serialize_export_arch', 'serialize_list': 'quay_serialize_list'})
class quay_TapiYAMLWriter:

    @staticmethod
    @_name_boundary.callable_contract({'tapi_dict': 'quay_tapi_dict_64c4e5b'}, 'write_out')
    def quay_write_out(quay_tapi_dict_64c4e5b: dict):
        quay_text_7fe5ed3 = ['---', 'archs:'.ljust(23) + _name_boundary.attributes(quay_TapiYAMLWriter)['serialize_list'](quay_tapi_dict_64c4e5b['archs']), 'platform:'.ljust(23) + quay_tapi_dict_64c4e5b['platform'], 'install-name:'.ljust(23) + quay_tapi_dict_64c4e5b['install-name'], 'current-version:'.ljust(23) + str(quay_tapi_dict_64c4e5b['current-version']), 'compatibility-version: ' + str(quay_tapi_dict_64c4e5b['compatibility-version']), 'exports:']
        for quay_arch_3d85d1d in quay_tapi_dict_64c4e5b['exports']:
            quay_text_7fe5ed3.append(_name_boundary.attributes(quay_TapiYAMLWriter)['serialize_export_arch'](quay_arch_3d85d1d))
        quay_text_7fe5ed3.append('...')
        quay_formatter_5f98405 = quay_TerminalFormatter()
        quay_highlighted_text_e2c29bd = quay_highlight('\n'.join(quay_text_7fe5ed3), quay_YamlLexer(), quay_formatter_5f98405)
        return quay_highlighted_text_e2c29bd

    @staticmethod
    @_name_boundary.callable_contract({'export_dict': 'quay_export_dict_aa801da'}, 'serialize_export_arch')
    def quay_serialize_export_arch(quay_export_dict_aa801da):
        quay_text_f2f75a9 = ['  - ' + 'archs:'.ljust(22) + _name_boundary.attributes(quay_TapiYAMLWriter)['serialize_list'](quay_export_dict_aa801da['archs'])]
        if 'allowed-clients' in quay_export_dict_aa801da:
            quay_text_f2f75a9.append('    ' + 'allowed-clients:'.ljust(22) + _name_boundary.attributes(quay_TapiYAMLWriter)['serialize_list'](quay_export_dict_aa801da['allowed-clients']))
        if 'symbols' in quay_export_dict_aa801da:
            quay_text_f2f75a9.append('    ' + 'symbols:'.ljust(22) + _name_boundary.attributes(quay_TapiYAMLWriter)['serialize_list'](quay_export_dict_aa801da['symbols']))
        if 'objc-classes' in quay_export_dict_aa801da:
            quay_text_f2f75a9.append('    ' + 'objc-classes:'.ljust(22) + _name_boundary.attributes(quay_TapiYAMLWriter)['serialize_list'](quay_export_dict_aa801da['objc-classes']))
        if 'objc-ivars' in quay_export_dict_aa801da:
            quay_text_f2f75a9.append('    ' + 'objc-ivars:'.ljust(22) + _name_boundary.attributes(quay_TapiYAMLWriter)['serialize_list'](quay_export_dict_aa801da['objc-ivars']))
        return '\n'.join(quay_text_f2f75a9)

    @staticmethod
    @_name_boundary.callable_contract({'slist': 'quay_slist_ddffb83'}, 'serialize_list')
    def quay_serialize_list(quay_slist_ddffb83):
        quay_text_9b11e42 = '[ '
        quay_wraplen_13eeb1d = 55
        quay_lpad_7571632 = 28
        quay_stack_cdee36f = []
        for quay_item_1b629fd in quay_slist_ddffb83:
            if len(', '.join(quay_stack_cdee36f)) + len(quay_item_1b629fd) > quay_wraplen_13eeb1d and len(quay_stack_cdee36f) > 0:
                quay_text_9b11e42 += ', '.join(quay_stack_cdee36f) + ',\n' + ''.ljust(quay_lpad_7571632)
                quay_stack_cdee36f = []
            quay_stack_cdee36f.append(quay_item_1b629fd)
        quay_text_9b11e42 += ', '.join(quay_stack_cdee36f) + ' ]'
        return quay_text_9b11e42

@_name_boundary.class_contract('Table', {'preheat': 'quay_preheat', 'fetch_all': 'quay_fetch_all', 'fetch': 'quay_fetch', 'render': 'quay_render', 'titles': 'quay_titles', 'rows': 'quay_rows', 'size_pinned_columns': 'quay_size_pinned_columns', 'dividers': 'quay_dividers', 'avoid_wrapping_titles': 'quay_avoid_wrapping_titles', 'ansi_borders': 'quay_ansi_borders', 'column_pad': 'quay_column_pad', 'column_maxes': 'quay_column_maxes', 'most_recent_adjusted_maxes': 'quay_most_recent_adjusted_maxes', 'rendered_row_cache': 'quay_rendered_row_cache', 'header_cache': 'quay_header_cache'})
class quay_Table:
    """
    ASCII Table Renderer
    .titles = a list of titles for each column
    .rows is a list of lists, each "sublist" representing each column, .e.g self.rows.append(['col1thing', 'col2thing'])

    .column_pad (default is 2 (without dividers))

    This can be used with and without curses;
        you just need to set the max width it can be rendered at on the render call.
        (shutil.get_terminal_size)
    """

    @_name_boundary.callable_contract({'self': 'quay_self_42414c7', 'dividers': 'quay_dividers_f769da4', 'avoid_wrapping_titles': 'quay_avoid_wrapping_titles_f786861'}, '__init__')
    def __init__(quay_self_42414c7, quay_dividers_f769da4=False, quay_avoid_wrapping_titles_f786861=False):
        _name_boundary.attributes(quay_self_42414c7)['titles'] = []
        _name_boundary.attributes(quay_self_42414c7)['rows'] = []
        _name_boundary.attributes(quay_self_42414c7)['size_pinned_columns'] = []
        _name_boundary.attributes(quay_self_42414c7)['dividers'] = quay_dividers_f769da4
        _name_boundary.attributes(quay_self_42414c7)['avoid_wrapping_titles'] = quay_avoid_wrapping_titles_f786861
        _name_boundary.attributes(quay_self_42414c7)['ansi_borders'] = True
        _name_boundary.attributes(quay_self_42414c7)['column_pad'] = 3 if quay_dividers_f769da4 else 2
        _name_boundary.attributes(quay_self_42414c7)['column_maxes'] = []
        _name_boundary.attributes(quay_self_42414c7)['most_recent_adjusted_maxes'] = []
        _name_boundary.attributes(quay_self_42414c7)['rendered_row_cache'] = {}
        _name_boundary.attributes(quay_self_42414c7)['header_cache'] = {}

    @_name_boundary.callable_contract({'self': 'quay_self_eed1fb5'}, 'preheat')
    def quay_preheat(quay_self_eed1fb5):
        """
        Call this whenever there's a second to do so, to pre-run a few width-independent calculations

        :return:
        """
        _name_boundary.attributes(quay_self_eed1fb5)['column_maxes'] = [0 for quay___6389614 in _name_boundary.attributes(quay_self_eed1fb5)['titles']]
        _name_boundary.attributes(quay_self_eed1fb5)['most_recent_adjusted_maxes'] = [*_name_boundary.attributes(quay_self_eed1fb5)['column_maxes']]
        for quay_row_2a326a1 in _name_boundary.attributes(quay_self_eed1fb5)['rows']:
            for quay_index_b17559d, quay_col_3cc4e38 in enumerate(quay_row_2a326a1):
                quay_col_size_d310679 = max([len(quay_i_b918362) + _name_boundary.attributes(quay_self_eed1fb5)['column_pad'] for quay_i_b918362 in quay_col_3cc4e38.split('\n')])
                _name_boundary.attributes(quay_self_eed1fb5)['column_maxes'][quay_index_b17559d] = max(quay_col_size_d310679, _name_boundary.attributes(quay_self_eed1fb5)['column_maxes'][quay_index_b17559d])
        for quay_i_635e038, quay_title_f5c766d in enumerate(_name_boundary.attributes(quay_self_eed1fb5)['titles']):
            _name_boundary.attributes(quay_self_eed1fb5)['column_maxes'][quay_i_635e038] = max(_name_boundary.attributes(quay_self_eed1fb5)['column_maxes'][quay_i_635e038], len(quay_title_f5c766d) + 1 + len(_name_boundary.attributes(quay_self_eed1fb5)['titles']))

    @_name_boundary.callable_contract({'self': 'quay_self_d7fd38b', 'screen_width': 'quay_screen_width_b637e80'}, 'fetch_all')
    def quay_fetch_all(quay_self_d7fd38b, quay_screen_width_b637e80):
        """
        Render the entirety of the table for a screen width

        (avoid calling this in GUI, only use it in CLI)

        :param screen_width:
        :return:
        """
        return _name_boundary.attributes(quay_self_d7fd38b)['fetch'](0, len(_name_boundary.attributes(quay_self_d7fd38b)['rows']), quay_screen_width_b637e80)

    @_name_boundary.callable_contract({'self': 'quay_self_6fe1f23', 'row_start': 'quay_row_start_19587d4', 'row_count': 'quay_row_count_4f11395', 'screen_width': 'quay_screen_width_3b9a34c'}, 'fetch')
    def quay_fetch(quay_self_6fe1f23, quay_row_start_19587d4, quay_row_count_4f11395, quay_screen_width_3b9a34c):
        """
        Cache-based batch processing and rendering

        Will spit out a generated table for screen_width containing row_count rows.

        :param row_start: Start index to load
        :param row_count: Amount from index to load
        :param screen_width: Screen width
        :return:
        """
        quay_cgrey_aed7f65 = '\x1b[0m\x1b[38;5;242m'
        quay_reset_a7ef4d5 = '\x1b[0m'
        quay_cwhitebold_d79d759 = '\x1b[0m\x1b[1m'
        quay_cend_17c61a0 = '\x1b[0m\x1b[39m'
        if _name_boundary.attributes(quay_opts)['DISABLE_COLOR']:
            quay_cgrey_aed7f65 = quay_reset_a7ef4d5
            quay_cend_17c61a0 = quay_reset_a7ef4d5
        if quay_row_count_4f11395 == 0:
            return ''
        quay_rows_3328d2f = []
        if quay_screen_width_3b9a34c in _name_boundary.attributes(quay_self_6fe1f23)['rendered_row_cache']:
            for quay_i_9e95dd6 in range(quay_row_start_19587d4, quay_row_start_19587d4 + quay_row_count_4f11395):
                if str(quay_i_9e95dd6) in _name_boundary.attributes(quay_self_6fe1f23)['rendered_row_cache'][quay_screen_width_3b9a34c]:
                    quay_rows_3328d2f.append(_name_boundary.attributes(quay_self_6fe1f23)['rendered_row_cache'][quay_screen_width_3b9a34c][str(quay_i_9e95dd6)])
                else:
                    break
        else:
            _name_boundary.attributes(quay_self_6fe1f23)['rendered_row_cache'][quay_screen_width_3b9a34c] = {}
        quay_r_row_count_0cb83cb = quay_row_count_4f11395 - len(quay_rows_3328d2f)
        quay_r_start_8bebb9e = quay_row_start_19587d4 + len(quay_rows_3328d2f)
        quay_rows_text_8967378 = ''.join([quay_i_4458662 + '\n' for quay_i_4458662 in quay_rows_3328d2f])
        quay_sep_line_1789e51 = ''
        quay_rows_text_8967378 += _name_boundary.attributes(quay_self_6fe1f23)['render'](_name_boundary.attributes(quay_self_6fe1f23)['rows'][quay_r_start_8bebb9e:quay_r_start_8bebb9e + quay_r_row_count_0cb83cb], quay_screen_width_3b9a34c, quay_r_start_8bebb9e)
        if _name_boundary.attributes(quay_self_6fe1f23)['dividers']:
            quay_rows_text_8967378 = quay_rows_text_8967378[:-1]
            quay_sep_line_1789e51 = '┣━'
            for quay_size_f2cf152 in _name_boundary.attributes(quay_self_6fe1f23)['most_recent_adjusted_maxes']:
                quay_sep_line_1789e51 += ''.ljust(quay_size_f2cf152 - 2, '━') + '╋━'
            quay_sep_line_1789e51 = quay_cgrey_aed7f65 + quay_sep_line_1789e51[:-_name_boundary.attributes(quay_self_6fe1f23)['column_pad']].ljust(quay_screen_width_3b9a34c - 1, '━')[:-_name_boundary.attributes(quay_self_6fe1f23)['column_pad']] + '━━━┫' + quay_cend_17c61a0
            quay_rows_text_8967378 = quay_rows_text_8967378[:-len(quay_sep_line_1789e51)]
            quay_rows_text_8967378 += quay_sep_line_1789e51.replace('┣', '┗').replace('╋', '┻').replace('┫', '┛')
        if quay_screen_width_3b9a34c in _name_boundary.attributes(quay_self_6fe1f23)['header_cache']:
            quay_rows_text_8967378 = _name_boundary.attributes(quay_self_6fe1f23)['header_cache'][quay_screen_width_3b9a34c] + quay_rows_text_8967378
        else:
            quay_title_row_edfc6dd = ''
            for quay_i_9e95dd6, quay_title_38ac965 in enumerate(_name_boundary.attributes(quay_self_6fe1f23)['titles']):
                if _name_boundary.attributes(quay_self_6fe1f23)['dividers']:
                    try:
                        quay_title_row_edfc6dd += quay_cgrey_aed7f65 + '┃ ' + quay_cwhitebold_d79d759 + quay_title_38ac965.ljust(_name_boundary.attributes(quay_self_6fe1f23)['most_recent_adjusted_maxes'][quay_i_9e95dd6], ' ')[:-(_name_boundary.attributes(quay_self_6fe1f23)['column_pad'] - 1)]
                    except IndexError:
                        quay_title_row_edfc6dd = ''
                else:
                    try:
                        quay_title_row_edfc6dd += ' ' + quay_title_38ac965.ljust(_name_boundary.attributes(quay_self_6fe1f23)['most_recent_adjusted_maxes'][quay_i_9e95dd6], ' ')[:-(_name_boundary.attributes(quay_self_6fe1f23)['column_pad'] - 1)]
                    except IndexError:
                        quay_title_row_edfc6dd = ''
            quay_header_text_258bf43 = ''
            if _name_boundary.attributes(quay_self_6fe1f23)['dividers']:
                quay_header_text_258bf43 += quay_cgrey_aed7f65 + quay_sep_line_1789e51.replace('┣', '┏').replace('╋', '┳').replace('┫', '┓') + quay_cwhitebold_d79d759 + '\n'
            quay_header_text_258bf43 += quay_title_row_edfc6dd.ljust(quay_screen_width_3b9a34c - 1)[:-1] + quay_cgrey_aed7f65 + '  ┃\n' + quay_cwhitebold_d79d759 if _name_boundary.attributes(quay_self_6fe1f23)['dividers'] else quay_cwhitebold_d79d759 + quay_title_row_edfc6dd + quay_reset_a7ef4d5 + '\n'
            if _name_boundary.attributes(quay_self_6fe1f23)['dividers']:
                quay_header_text_258bf43 += quay_sep_line_1789e51 + '\n'
            _name_boundary.attributes(quay_self_6fe1f23)['header_cache'][quay_screen_width_3b9a34c] = quay_header_text_258bf43
            quay_rows_text_8967378 = quay_header_text_258bf43 + quay_rows_text_8967378
        quay_rows_text_8967378 = quay_rows_text_8967378.replace('┣', quay_cgrey_aed7f65 + '┣').replace('┫', '┫' + quay_cend_17c61a0)
        return quay_rows_text_8967378

    @_name_boundary.callable_contract({'self': 'quay_self_cd4ffe8', '_rows': 'quay__rows_2493c6f', 'width': 'quay_width_83e5b11', 'row_start': 'quay_row_start_7d4b40f'}, 'render')
    def quay_render(quay_self_cd4ffe8, quay__rows_2493c6f, quay_width_83e5b11, quay_row_start_7d4b40f):
        """
        Render a list of rows for screen_width

        :param _rows: list of rows to be rendered
        :param width: Screen width
        :param row_start: Starting index of rows (for the sake of cacheing)
        :return:
        """
        quay_width_83e5b11 -= 1
        if len(quay__rows_2493c6f) == 0:
            return ''
        if not len(_name_boundary.attributes(quay_self_cd4ffe8)['column_maxes']) > 0:
            _name_boundary.attributes(quay_self_cd4ffe8)['preheat']()
        quay_column_maxes_ee4eb09 = [*_name_boundary.attributes(quay_self_cd4ffe8)['column_maxes']]
        if sum(quay_column_maxes_ee4eb09) < quay_width_83e5b11:
            quay_column_maxes_ee4eb09[-1] += quay_width_83e5b11 - sum(quay_column_maxes_ee4eb09) + 1
        quay_col_min_3b5f71c = min(quay_column_maxes_ee4eb09)
        quay_last_sum_7588833 = 0
        while sum(quay_column_maxes_ee4eb09) >= quay_width_83e5b11:
            for quay_index_1653c69, quay_i_9a38a93 in enumerate(quay_column_maxes_ee4eb09):
                if quay_index_1653c69 in _name_boundary.attributes(quay_self_cd4ffe8)['size_pinned_columns']:
                    continue
                if _name_boundary.attributes(quay_self_cd4ffe8)['avoid_wrapping_titles']:
                    quay_column_maxes_ee4eb09[quay_index_1653c69] = max(quay_col_min_3b5f71c, quay_column_maxes_ee4eb09[quay_index_1653c69] - 1, len(_name_boundary.attributes(quay_self_cd4ffe8)['titles'][quay_index_1653c69]) + 3)
                else:
                    quay_column_maxes_ee4eb09[quay_index_1653c69] = max(quay_col_min_3b5f71c, quay_column_maxes_ee4eb09[quay_index_1653c69] - 1)
            if sum(quay_column_maxes_ee4eb09) == quay_last_sum_7588833:
                return 'Width too small to render table'
            quay_last_sum_7588833 = sum(quay_column_maxes_ee4eb09)
        _name_boundary.attributes(quay_self_cd4ffe8)['most_recent_adjusted_maxes'] = [*quay_column_maxes_ee4eb09]

        @_name_boundary.callable_contract({'input_string': 'quay_input_string_20ac89c', 'split_length': 'quay_split_length_44abc5d'}, 'split_handling_ansi')
        def quay_split_handling_ansi_d52ec93(quay_input_string_20ac89c, quay_split_length_44abc5d):
            """
            Splits the input_string into chunks of split_length, taking into account
            ANSI escape sequences and trying to wrap whole words.
            """
            quay_parts_a3e825f = []
            quay_current_part_87ea037 = ''
            quay_current_length_7838cba = 0
            quay_current_color_e9008ee = '\x1b[0m'
            quay_i_444777f = 0
            while quay_i_444777f < len(quay_input_string_20ac89c):
                quay_match_dc95b6f = quay_ansi_escape.match(quay_input_string_20ac89c, quay_i_444777f)
                if quay_match_dc95b6f:
                    quay_current_color_e9008ee = quay_match_dc95b6f.group()
                    quay_current_part_87ea037 += quay_match_dc95b6f.group()
                    quay_i_444777f += len(quay_match_dc95b6f.group())
                else:
                    quay_space_pos_f85fcf7 = _name_boundary.attributes(quay_input_string_20ac89c)['find'](' ', quay_i_444777f)
                    quay_newline_pos_8267f39 = _name_boundary.attributes(quay_input_string_20ac89c)['find']('\n', quay_i_444777f)
                    quay_next_break_540f8b6 = min(quay_space_pos_f85fcf7 if quay_space_pos_f85fcf7 != -1 else len(quay_input_string_20ac89c), quay_newline_pos_8267f39 if quay_newline_pos_8267f39 != -1 else len(quay_input_string_20ac89c))
                    quay_word_end_22246e5 = quay_next_break_540f8b6 if quay_next_break_540f8b6 != -1 else len(quay_input_string_20ac89c)
                    quay_word_length_d09b400 = quay_strip_ansi(quay_input_string_20ac89c[quay_i_444777f:quay_word_end_22246e5]).__len__()
                    if quay_current_length_7838cba + quay_word_length_d09b400 + 6 <= quay_split_length_44abc5d or quay_current_length_7838cba == 0:
                        quay_current_part_87ea037 += quay_input_string_20ac89c[quay_i_444777f:quay_word_end_22246e5]
                        quay_current_length_7838cba += quay_word_length_d09b400
                        quay_i_444777f = quay_word_end_22246e5
                    else:
                        quay_parts_a3e825f.append(quay_current_part_87ea037)
                        quay_current_part_87ea037 = quay_current_color_e9008ee
                        quay_current_length_7838cba = 0
                    if quay_input_string_20ac89c[quay_i_444777f:quay_i_444777f + 1] == ' ':
                        quay_current_part_87ea037 += ' '
                        quay_i_444777f += 1
                    elif quay_input_string_20ac89c[quay_i_444777f:quay_i_444777f + 1] == '\n':
                        quay_parts_a3e825f.append(quay_current_part_87ea037)
                        quay_current_part_87ea037 = quay_current_color_e9008ee
                        quay_current_length_7838cba = 0
                        quay_i_444777f += 1
            if quay_strip_ansi(quay_current_part_87ea037):
                quay_parts_a3e825f.append(quay_current_part_87ea037)
            return quay_parts_a3e825f
        quay_rows_6fd8313 = []
        for quay_row_i_39e336f, quay_row_34fa887 in enumerate(quay__rows_2493c6f):
            quay_cols_c8c7960 = []
            quay_max_line_count_in_row_ed602fd = 0
            for quay_col_i_738cd81, quay_col_6b6a84f in enumerate(quay_row_34fa887):
                quay_lines_73eb88f = []
                quay_column_width_d6cc2a1 = quay_column_maxes_ee4eb09[quay_col_i_738cd81] - _name_boundary.attributes(quay_self_cd4ffe8)['column_pad']
                quay_wrapped_lines_5d662a1 = quay_split_handling_ansi_d52ec93(quay_col_6b6a84f, quay_column_width_d6cc2a1)
                for quay_line_2e5a0c3 in quay_wrapped_lines_5d662a1:
                    quay_lines_73eb88f.extend(quay_line_2e5a0c3.split('\n'))
                quay_max_line_count_in_row_ed602fd = max(len(quay_lines_73eb88f), quay_max_line_count_in_row_ed602fd)
                quay_cols_c8c7960.append(quay_lines_73eb88f)
            for quay_col_6b6a84f in quay_cols_c8c7960:
                while len(quay_col_6b6a84f) < quay_max_line_count_in_row_ed602fd:
                    quay_col_6b6a84f.append('')
            quay_rows_6fd8313.append(quay_cols_c8c7960)
        quay_lines_73eb88f = ''
        quay_sep_line_86d70fa = ''
        quay_cgrey_02233a4 = '\x1b[0m\x1b[38;5;242m'
        quay_reset_3160a46 = '\x1b[0m'
        quay_cend_099c427 = '\x1b[0m\x1b[39m'
        if _name_boundary.attributes(quay_opts)['DISABLE_COLOR']:
            quay_cgrey_02233a4 = quay_reset_3160a46
            quay_cend_099c427 = quay_reset_3160a46
        if _name_boundary.attributes(quay_self_cd4ffe8)['dividers']:
            quay_sep_line_86d70fa = '┣━'
            for quay_size_faa94ef in quay_column_maxes_ee4eb09:
                quay_sep_line_86d70fa += ''.ljust(quay_size_faa94ef - 2, '━') + '╋━'
            quay_sep_line_86d70fa = quay_sep_line_86d70fa[:-_name_boundary.attributes(quay_self_cd4ffe8)['column_pad']].ljust(quay_width_83e5b11, '━')[:-_name_boundary.attributes(quay_self_cd4ffe8)['column_pad']] + '━━━┫'
        if _name_boundary.attributes(quay_self_cd4ffe8)['dividers']:
            quay_lines_73eb88f += quay_sep_line_86d70fa + '\n'
        for quay_row_index_0bfeb70, quay_row_34fa887 in enumerate(quay_rows_6fd8313):
            quay_row_lines_36ffdf8 = []
            quay_column_count_0b6e2c7 = len(quay_row_34fa887[0])
            for quay_i_9a38a93 in range(0, quay_column_count_0b6e2c7):
                quay_line_2e5a0c3 = ''
                for quay_j_b933f38, quay_col_6b6a84f in enumerate(quay_row_34fa887):
                    quay_diff_b28ed35 = quay_column_maxes_ee4eb09[quay_j_b933f38] - len(quay_strip_ansi(quay_col_6b6a84f[quay_i_9a38a93]))
                    quay_line_2e5a0c3 += quay_col_6b6a84f[quay_i_9a38a93] + ' ' * quay_diff_b28ed35
                    if _name_boundary.attributes(quay_self_cd4ffe8)['dividers']:
                        quay_line_2e5a0c3 = quay_line_2e5a0c3[:-_name_boundary.attributes(quay_self_cd4ffe8)['column_pad']] + f' ┃ '
                if _name_boundary.attributes(quay_self_cd4ffe8)['dividers']:
                    quay_diff_b28ed35 = quay_width_83e5b11 - len(quay_strip_ansi(quay_line_2e5a0c3))
                    quay_line_2e5a0c3 = quay_cgrey_02233a4 + '┃ ' + quay_reset_3160a46 + (quay_line_2e5a0c3 + ' ' * quay_diff_b28ed35)[:-_name_boundary.attributes(quay_self_cd4ffe8)['column_pad']] + quay_cgrey_02233a4 + ' ┃ ' + quay_cend_099c427
                    quay_line_2e5a0c3 = quay_line_2e5a0c3.replace('┃', quay_cgrey_02233a4 + '┃' + quay_reset_3160a46)
                else:
                    quay_line_2e5a0c3 = ' ' + quay_line_2e5a0c3[:-_name_boundary.attributes(quay_self_cd4ffe8)['column_pad']].ljust(quay_width_83e5b11, ' ')[:-_name_boundary.attributes(quay_self_cd4ffe8)['column_pad']] + ' ' * _name_boundary.attributes(quay_self_cd4ffe8)['column_pad']
                quay_row_lines_36ffdf8.append(quay_line_2e5a0c3)
            if _name_boundary.attributes(quay_self_cd4ffe8)['dividers']:
                quay_row_lines_36ffdf8.append(quay_cgrey_02233a4 + quay_sep_line_86d70fa + quay_cend_099c427)
            _name_boundary.attributes(quay_self_cd4ffe8)['rendered_row_cache'][quay_width_83e5b11 + 1][str(quay_row_index_0bfeb70 + quay_row_start_7d4b40f)] = '\n'.join(quay_row_lines_36ffdf8)
            quay_lines_73eb88f += '\n'.join(quay_row_lines_36ffdf8)
            quay_lines_73eb88f += '\n'
        return quay_lines_73eb88f
quay_ansi_escape = quay_re.compile('(?:\\x1B[@-_]|[\\x80-\\x9F])[0-?]*[ -/]*[@-~]')

@_name_boundary.callable_contract({'msg': 'quay_msg_8ba2be5'}, 'strip_ansi')
def quay_strip_ansi(quay_msg_8ba2be5):
    return quay_ansi_escape.sub('', quay_msg_8ba2be5)

@_name_boundary.callable_contract({'data': 'quay_data_69e61c9'}, 'bytes_to_hex')
def quay_bytes_to_hex(quay_data_69e61c9: quay_Union[bytes, bytearray]) -> str:
    return _name_boundary.attributes(quay_data_69e61c9)['hex']()

@_name_boundary.callable_contract({'msg': 'quay_msg_513d05e', 'file': 'quay_file_c6b3c22'}, 'ktool_print')
def quay_imagequay_print(quay_msg_513d05e, quay_file_c6b3c22=quay_sys.stdout):
    if quay_file_c6b3c22.isatty():
        print(quay_msg_513d05e, file=quay_file_c6b3c22)
    else:
        print(quay_strip_ansi(quay_msg_513d05e), file=quay_file_c6b3c22)

@_name_boundary.callable_contract({'msg': 'quay_msg_5492a4b'}, 'print_err')
def quay_print_err(quay_msg_5492a4b):
    print(quay_msg_5492a4b, file=quay_sys.stderr)
_name_boundary.module_contract(globals(), {'THREAD_COUNT': 'quay_THREAD_COUNT', 'os': 'quay_os', 'MH_CIGAM_64': 'quay_MH_CIGAM_64', 'Table': 'quay_Table', 'MH_MAGIC_64': 'quay_MH_MAGIC_64', 'macho_is_malformed': 'quay_macho_is_malformed', 'print_err': 'quay_print_err', 'version_output': 'quay_version_output', 'get_terminal_size': 'quay_get_terminal_size', 'ansi_escape': 'quay_ansi_escape', 'ktool_print': 'quay_imagequay_print', 'FAT_CIGAM': 'quay_FAT_CIGAM', 'Queue': 'quay_Queue', 'highlight': 'quay_highlight', 'Union': 'quay_Union', 'ignore': 'quay_ignore', 'TapiYAMLWriter': 'quay_TapiYAMLWriter', 'MH_MAGIC': 'quay_MH_MAGIC', 'OUT_IS_TTY': 'quay_OUT_IS_TTY', 'MY_DIR': 'quay_MY_DIR', 'shutil': 'quay_shutil', 'usi32_to_si32': 'quay_usi32_to_si32', 'opts': 'quay_opts', 'MH_CIGAM': 'quay_MH_CIGAM', 'sys': 'quay_sys', 'Struct': 'quay_Struct', 'time': 'quay_time', 'Enum': 'quay_Enum', 'inspect': 'quay_inspect', 'List': 'quay_List', 'concurrent': 'quay_concurrent', 'TerminalFormatter': 'quay_TerminalFormatter', 'FileType': 'quay_FileType', 'strip_ansi': 'quay_strip_ansi', 'QueueItem': 'quay_QueueItem', 'highlight_xml': 'quay_highlight_xml', 'bytes_to_hex': 'quay_bytes_to_hex', 're': 'quay_re', 'highlight_json': 'quay_highlight_json', 'uint_to_int': 'quay_uint_to_int', 'FAT_MAGIC': 'quay_FAT_MAGIC', 'log': 'quay_log', 'detect_filetype': 'quay_detect_filetype'})
