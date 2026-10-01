# Derived from src/ktool/window.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  window.py
#
#  This is what happens when you work retail for like a year and try to stay sane.
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#

# # # # #
#
# Comments:::
#   I'm not a huge fan of python-curses' cryptic, C-style abstractions, so I abstracted them out myself with a proper
#       OOP approach, which also serves to fix the curses (Y, X) coordinate handling crap.
#
# CURRENT TO-DO LIST:::
# TODO: Properly Abstract out Mouse Clicks / clean up mouse handler code
#
# CURRENT FEATURE TO-DO LIST:::
# TODO: Implement the title bar menu actions
#
# # # # #
import imagequay_boundary as _name_boundary
import curses as quay_curses
import os as quay_os
import pprint as quay_pprint
from datetime import datetime as quay_datetime
from math import ceil as quay_ceil
from pygments import highlight as quay_highlight
from pygments.formatters.terminal import TerminalFormatter as quay_TerminalFormatter
from pygments.formatters.terminal256 import Terminal256Formatter as quay_Terminal256Formatter
from pygments.lexers.objective import ObjectiveCLexer as quay_ObjectiveCLexer
import imagequay.toolkit_api as _boundary_import_ktool_ktool
import imagequay as quay_imagequay
from imagequay.swift_model import quay_SwiftClass as quay_SwiftClass
from imagequay_layout import quay_LOAD_COMMAND as quay_LOAD_COMMAND
from imagequay.container_io import quay_MachOFile as quay_MachOFile
from imagequay.metadata_reader import quay_MachOImageLoader as quay_MachOImageLoader
from imagequay.objc_model import quay_ObjCImage as quay_ObjCImage
from imagequay.header_documents import quay_HeaderGenerator as quay_HeaderGenerator
from imagequay.formatting import quay_Table as quay_Table
from imagequay.kernel_images import quay_KernelCache as quay_KernelCache, quay_Kext as quay_Kext
quay_VERT_LINE = '│'
quay_WINDOW_NAME = 'imagequay'
quay_BOX_CHARS = ['┦', '─', '━', '│', '┃', '┄', '┅', '┆', '┇', '┈', '┉', '┊', '┋', '┌', '┍', '┎', '┏', '┐', '┑', '┒', '┓', '└', '┕', '┖', '┗', '┘', '┙', '┚', '┛', '├', '┝', '┞', '┟', '┠', '┡', '┢', '┣', '┤', '┥', '┦', '┧', '┨', '┩', '┪', '┫', '┬', '┭', '┮', '┯', '┰', '┱', '┲', '┳', '┴', '┵', '┶', '┷', '┸', '┹', '┺', '┻', '┼', '┽', '┾', '┿', '╀', '╁', '╂', '╃', '╄', '╅', '╆', '╇', '╈', '╉', '╊', '╋', '╌', '╍', '╎', '╏', '═', '║', '╒', '╓', '╔', '╕', '╖', '╗', '╘', '╙', '╚', '╛', '╜', '╝', '╞', '╟', '╠', '╡', '╢', '╣', '╤', '╥', '╦', '╧', '╨', '╩', '╪', '╫', '╬', '╭', '╮', '╯', '╰', '╱', '╲', '╳', '╴', '╵', '╶', '╷', '╸', '╹', '╺', '╻', '╼', '╽', '╾', '╿']
quay_SIDEBAR_WIDTH = 40
quay_MAIN_TEXT = 'imagequay ------\n\nThis is a *very* pre-release version of the GUI Tool, and it has a long ways to go. \n\nStay Updated with `python3 -m pip install --upgrade k2l` !\n\nMouse support is a WIP; quite a few things support mouse interaction already.\n\nNavigate the sidebar with arrow keys or mouse. You can use left/right arrow, or spacebar, to expand/collapse submenus.\n\nHit tab to swap between the sidebar context and main context. Scroll the main context with up/down keys.\n\nBackspace to exit (or click the X in the top right corner).\n'
quay_PANIC_STRING = ''

@_name_boundary.callable_contract({'msg': 'quay_msg_c6d2e98'}, 'panic')
def quay_panic(quay_msg_c6d2e98):
    global quay_PANIC_STRING
    quay_PANIC_STRING = quay_msg_c6d2e98
    raise quay_PanicException
quay_ATTR_STRING_DEBUG = False

@_name_boundary.class_contract('ColorRep', {'get_attr': 'quay_get_attr', 'n': 'quay_n'})
class quay_ColorRep:

    @_name_boundary.callable_contract({'self': 'quay_self_e802f96', 'n': 'quay_n_2940d72'}, '__init__')
    def __init__(quay_self_e802f96, quay_n_2940d72):
        _name_boundary.attributes(quay_self_e802f96)['n'] = quay_n_2940d72

    @_name_boundary.callable_contract({'self': 'quay_self_b34cfc0'}, 'get_attr')
    def quay_get_attr(quay_self_b34cfc0):
        return quay_curses.color_pair(_name_boundary.attributes(quay_self_b34cfc0)['n'])

@_name_boundary.class_contract('Attribute', {'HIGHLIGHTED': 'quay_HIGHLIGHTED', 'UNDERLINED': 'quay_UNDERLINED', 'COLOR_1': 'quay_COLOR_1', 'COLOR_2': 'quay_COLOR_2', 'COLOR_3': 'quay_COLOR_3', 'COLOR_4': 'quay_COLOR_4', 'COLOR_5': 'quay_COLOR_5', 'COLOR_6': 'quay_COLOR_6', 'COLOR_7': 'quay_COLOR_7'})
class quay_Attribute:
    quay_HIGHLIGHTED = quay_curses.A_STANDOUT
    quay_UNDERLINED = quay_curses.A_UNDERLINE
    quay_COLOR_1 = quay_ColorRep(1)
    quay_COLOR_2 = quay_ColorRep(2)
    quay_COLOR_3 = quay_ColorRep(3)
    quay_COLOR_4 = quay_ColorRep(4)
    quay_COLOR_5 = quay_ColorRep(5)
    quay_COLOR_6 = quay_ColorRep(6)
    quay_COLOR_7 = quay_ColorRep(7)

@_name_boundary.class_contract('AttributedString', {'ansi_to_attrstr': 'quay_ansi_to_attrstr', 'fix_256_code': 'quay_fix_256_code', 'set_attr': 'quay_set_attr', 'string': 'quay_string', 'attrs': 'quay_attrs'})
class quay_AttributedString:

    @_name_boundary.callable_contract({'self': 'quay_self_a2130ff', 'string': 'quay_string_b6ea324'}, '__init__')
    def __init__(quay_self_a2130ff, quay_string_b6ea324: str):
        _name_boundary.attributes(quay_self_a2130ff)['string'] = quay_string_b6ea324
        _name_boundary.attributes(quay_self_a2130ff)['attrs'] = []

    @staticmethod
    @_name_boundary.callable_contract({'ansi_str': 'quay_ansi_str_b526f2d'}, 'ansi_to_attrstr')
    def quay_ansi_to_attrstr(quay_ansi_str_b526f2d):
        """This function translates ansi escaped strings (or manually specified ones, by replacing the "escape[" with §),
                to our Attributed String Format.

        :param ansi_str:
        :return:
        """
        quay_pos_2050b65 = 0
        quay_ansi_str_b526f2d = list(quay_ansi_str_b526f2d)
        while quay_pos_2050b65 < len(quay_ansi_str_b526f2d):
            if ord(quay_ansi_str_b526f2d[quay_pos_2050b65]) == 27:
                quay_ansi_str_b526f2d[quay_pos_2050b65] = '§'
            quay_pos_2050b65 += 1
        quay_ansi_str_b526f2d = ''.join(quay_ansi_str_b526f2d)
        quay_ansi_str_b526f2d = quay_ansi_str_b526f2d.replace('§[', '§')
        if quay_ATTR_STRING_DEBUG:
            return quay_ansi_str_b526f2d
        quay_pos_2050b65 = 0
        quay_bland_pos_7b8c7fa = 0
        quay_attr_str_46b82f6 = quay_AttributedString(quay_ansi_str_b526f2d)
        quay_bland_str_6673e28 = ''
        quay_attr_start_a3722ca = 0
        quay_attr_end_0aebc13 = 0
        quay_attr_color_62b54ac = 0
        while quay_pos_2050b65 < len(quay_ansi_str_b526f2d):
            if quay_ansi_str_b526f2d[quay_pos_2050b65] == '§':
                quay_ansi_escape_code_f5cee71 = ''
                quay_pos_2050b65 += 1
                if quay_pos_2050b65 == len(quay_ansi_str_b526f2d):
                    quay_panic(quay_ansi_str_b526f2d)
                while quay_ansi_str_b526f2d[quay_pos_2050b65] != 'm':
                    quay_ansi_escape_code_f5cee71 += quay_ansi_str_b526f2d[quay_pos_2050b65]
                    quay_pos_2050b65 += 1
                quay_ansi_list_739aef6 = quay_ansi_escape_code_f5cee71.split(';')
                quay_is_reset_e6a0a4f = False
                quay_first_item_450de42 = quay_ansi_list_739aef6[0]
                try:
                    int(quay_first_item_450de42)
                except ValueError:
                    quay_panic(str(quay_ansi_list_739aef6) + '\n' + quay_ansi_str_b526f2d)
                if quay_first_item_450de42 == '38':
                    quay_attr_color_62b54ac = _name_boundary.attributes(quay_AttributedString)['fix_256_code'](int(quay_ansi_list_739aef6[2]))
                elif quay_first_item_450de42 == '39' or quay_first_item_450de42 == '0':
                    quay_is_reset_e6a0a4f = True
                elif 30 <= int(quay_first_item_450de42) <= 37:
                    quay_attr_color_62b54ac = int(quay_first_item_450de42) - 30 + 8
                if quay_is_reset_e6a0a4f:
                    quay_attr_end_0aebc13 = quay_bland_pos_7b8c7fa
                    _name_boundary.attributes(quay_attr_str_46b82f6)['set_attr'](quay_attr_start_a3722ca, quay_attr_end_0aebc13, quay_curses.color_pair(quay_attr_color_62b54ac))
                else:
                    quay_attr_start_a3722ca = quay_bland_pos_7b8c7fa
                    _name_boundary.attributes(quay_attr_str_46b82f6)['set_attr'](quay_attr_end_0aebc13, quay_attr_start_a3722ca, quay_curses.A_NORMAL)
                quay_pos_2050b65 += 1
            else:
                quay_bland_str_6673e28 += quay_ansi_str_b526f2d[quay_pos_2050b65]
                quay_bland_pos_7b8c7fa += 1
                quay_pos_2050b65 += 1
        _name_boundary.attributes(quay_attr_str_46b82f6)['string'] = quay_bland_str_6673e28
        return quay_attr_str_46b82f6

    @staticmethod
    @_name_boundary.callable_contract({'code': 'quay_code_770a6f5'}, 'fix_256_code')
    def quay_fix_256_code(quay_code_770a6f5):
        """Pygments 256 formatter sucks.

        :param code:
        :return:
        """
        if quay_code_770a6f5 == 125:
            return 168
        if quay_code_770a6f5 == 21:
            return 151
        if quay_code_770a6f5 == 28:
            return 118
        return quay_code_770a6f5

    @_name_boundary.callable_contract({'self': 'quay_self_cd191ec', 'start': 'quay_start_500cb00', 'end': 'quay_end_cba8492', 'attr': 'quay_attr_8ed1350'}, 'set_attr')
    def quay_set_attr(quay_self_cd191ec, quay_start_500cb00, quay_end_cba8492, quay_attr_8ed1350):
        _name_boundary.attributes(quay_self_cd191ec)['attrs'].append([[quay_start_500cb00, quay_end_cba8492], quay_attr_8ed1350])

    @_name_boundary.callable_contract({'self': 'quay_self_c8c44db'}, '__str__')
    def __str__(quay_self_c8c44db):
        return _name_boundary.attributes(quay_self_c8c44db)['string']

@_name_boundary.class_contract('ExitProgramException', {})
class quay_ExitProgramException(Exception):
    """Raise this within the run-loop to cleanly exit the program
    """

    @_name_boundary.callable_contract({'self': 'quay_self_c3cd866'}, '__init__')
    def __init__(quay_self_c3cd866):
        pass

@_name_boundary.class_contract('RebuildAllException', {})
class quay_RebuildAllException(Exception):
    """Raise this to invoke a rebuild
    """

@_name_boundary.class_contract('PresentDebugMenuException', {})
class quay_PresentDebugMenuException(Exception):
    """Raise this within the runloop to present the debug menu
    """

@_name_boundary.class_contract('PresentTitleMenuException', {})
class quay_PresentTitleMenuException(Exception):
    """Raise this within the runloop to invoke the Title Bar Menu Rendering code
    """

@_name_boundary.class_contract('FileBrowserOpenNewFileException', {})
class quay_FileBrowserOpenNewFileException(Exception):
    """

    """

@_name_boundary.class_contract('HelpMenuException', {})
class quay_HelpMenuException(Exception):
    """"""

@_name_boundary.class_contract('DestroyTitleMenuException', {})
class quay_DestroyTitleMenuException(Exception):
    """Raise this to destroy the menu overlay
    """

@_name_boundary.class_contract('PanicException', {})
class quay_PanicException(Exception):
    """Raise this within the program and set the global PANIC_STRING to panic the window,
            and print the string after cleaning up the window display.
    """

@_name_boundary.class_contract('HexDumpTable', {'fetch': 'quay_fetch', 'titles': 'quay_titles', 'hex': 'quay_hex', 'rows': 'quay_rows', 'rendered_row_cache': 'quay_rendered_row_cache', 'preheat': 'quay_preheat', 'column_maxes': 'quay_column_maxes'})
class quay_HexDumpTable(quay_Table):
    """
    Subclass of table, just set the .hex value to a bytearray and it'll handle rendering it.

    """

    @_name_boundary.callable_contract({'self': 'quay_self_004b6ea'}, '__init__')
    def __init__(quay_self_004b6ea):
        super().__init__()
        _name_boundary.attributes(quay_self_004b6ea)['titles'] = ['Raw Data', 'ASCII']
        _name_boundary.attributes(quay_self_004b6ea)['hex'] = bytearray(b'')

    @_name_boundary.callable_contract({'self': 'quay_self_f3d5c61', 'row_start': 'quay_row_start_c1d4f10', 'row_count': 'quay_row_count_cdc1485', 'screen_width': 'quay_screen_width_272b86c'}, 'fetch')
    def quay_fetch(quay_self_f3d5c61, quay_row_start_c1d4f10, quay_row_count_cdc1485, quay_screen_width_272b86c):
        quay_col_count_f7005d3 = 2
        _name_boundary.attributes(quay_self_f3d5c61)['rows'] = []
        quay_stack_3ed6395 = ''
        quay_decode_stack_1dfa389 = ''
        quay_stack_div_2ade7b4 = ''
        quay_decode_stack_div_9f64dfb = ''
        for quay_i_2b431c9, quay_byte_e856d0e in enumerate(_name_boundary.attributes(quay_self_f3d5c61)['hex'][quay_row_start_c1d4f10 * 8:quay_row_start_c1d4f10 * 8 + quay_row_count_cdc1485 * 8]):
            quay_stack_div_2ade7b4 += hex(quay_byte_e856d0e)[2:].rjust(2, '0')
            quay_decode_stack_div_9f64dfb += quay_byte_e856d0e.to_bytes(1, 'big').decode('ascii') + ' ' if quay_byte_e856d0e in range(32, 127) else '. '
            if len(quay_stack_div_2ade7b4) >= 8:
                quay_stack_3ed6395 += quay_stack_div_2ade7b4 + '  '
                quay_decode_stack_1dfa389 += quay_decode_stack_div_9f64dfb + '  '
                quay_stack_div_2ade7b4 = ''
                quay_decode_stack_div_9f64dfb = ''
            if len(quay_stack_3ed6395) >= 10 * quay_col_count_f7005d3:
                _name_boundary.attributes(quay_self_f3d5c61)['rows'].append([quay_stack_3ed6395, quay_decode_stack_1dfa389])
                quay_stack_3ed6395 = ''
                quay_decode_stack_1dfa389 = ''
        _name_boundary.attributes(quay_self_f3d5c61)['rows'].append([quay_stack_3ed6395, quay_decode_stack_1dfa389])
        if not len(_name_boundary.attributes(quay_self_f3d5c61)['column_maxes']) > 0:
            _name_boundary.attributes(quay_self_f3d5c61)['preheat']()
        quay_fetched_70acd85 = _name_boundary.attributes(super())['fetch'](0, quay_row_count_cdc1485, quay_screen_width_272b86c)
        _name_boundary.attributes(quay_self_f3d5c61)['rendered_row_cache'] = {}
        return quay_fetched_70acd85

@_name_boundary.class_contract('LazilyProcessedTextBuffer', {'go': 'quay_go', 'lines': 'quay_lines', 'processed': 'quay_processed', 'target': 'quay_target', 'target_args': 'quay_target_args'})
class quay_LazilyProcessedTextBuffer:

    @_name_boundary.callable_contract({'self': 'quay_self_4dcc6d9'}, '__init__')
    def __init__(quay_self_4dcc6d9):
        _name_boundary.attributes(quay_self_4dcc6d9)['lines'] = []
        _name_boundary.attributes(quay_self_4dcc6d9)['processed'] = False
        _name_boundary.attributes(quay_self_4dcc6d9)['target'] = None
        _name_boundary.attributes(quay_self_4dcc6d9)['target_args'] = []

    @_name_boundary.callable_contract({'self': 'quay_self_d71898e'}, 'go')
    def quay_go(quay_self_d71898e):
        _name_boundary.attributes(quay_self_d71898e)['lines'] = _name_boundary.attributes(quay_self_d71898e)['target'](*_name_boundary.attributes(quay_self_d71898e)['target_args'])
        _name_boundary.attributes(quay_self_d71898e)['processed'] = True

@_name_boundary.class_contract('RootBox', {'coord_translate': 'quay_coord_translate', 'write': 'quay_write', 'stdscr': 'quay_stdscr'})
class quay_RootBox:
    """
    The Root Box is an abstraction of the regular box, with no bounds/x-y coordinates

    It represents the entire terminal window itself and handles actually writing to/from the curses standard screen.
    """

    @_name_boundary.callable_contract({'self': 'quay_self_76d92cd', 'stdscr': 'quay_stdscr_64dca84'}, '__init__')
    def __init__(quay_self_76d92cd, quay_stdscr_64dca84):
        _name_boundary.attributes(quay_self_76d92cd)['stdscr'] = quay_stdscr_64dca84

    @_name_boundary.callable_contract({'self': 'quay_self_4e19cfc', 'x': 'quay_x_a7b60ae', 'y': 'quay_y_73a9c0b'}, 'coord_translate')
    def quay_coord_translate(quay_self_4e19cfc, quay_x_a7b60ae, quay_y_73a9c0b):
        return (quay_x_a7b60ae, quay_y_73a9c0b)

    @_name_boundary.callable_contract({'self': 'quay_self_6bd0cd8', 'x': 'quay_x_8c73fce', 'y': 'quay_y_3be128d', 'string': 'quay_string_4e6638c', 'attr': 'quay_attr_99b8040'}, 'write')
    def quay_write(quay_self_6bd0cd8, quay_x_8c73fce, quay_y_3be128d, quay_string_4e6638c, quay_attr_99b8040):
        try:
            _name_boundary.attributes(quay_self_6bd0cd8)['stdscr'].addstr(quay_y_3be128d, quay_x_8c73fce, quay_string_4e6638c, quay_attr_99b8040)
        except _name_boundary.attributes(quay_curses)['error']:
            global quay_PANIC_STRING
            quay_PANIC_STRING = f'Rendering Error while writing {quay_string_4e6638c} @ {quay_x_8c73fce}, {quay_y_3be128d}\nScreen Bounds: {quay_curses.COLS}x{quay_curses.LINES}\nProgram Panicked'
            raise quay_PanicException

@_name_boundary.class_contract('Box', {'coord_translate': 'quay_coord_translate', 'write': 'quay_write', 'is_click_inbounds': 'quay_is_click_inbounds', 'parent': 'quay_parent', 'x': 'quay_x', 'y': 'quay_y', 'width': 'quay_width', 'height': 'quay_height'})
class quay_Box:
    """
    A Box is an abstraction of an area on the screen to write to.

    It's defined with a standard set of coords/dimensions, and writes to it are relative from those defined dimensions
    """

    @_name_boundary.callable_contract({'self': 'quay_self_2ef58ac', 'parent': 'quay_parent_d1d6c81', 'x': 'quay_x_5021b6a', 'y': 'quay_y_41d1f47', 'width': 'quay_width_6f378c4', 'height': 'quay_height_8658aca'}, '__init__')
    def __init__(quay_self_2ef58ac, quay_parent_d1d6c81, quay_x_5021b6a, quay_y_41d1f47, quay_width_6f378c4, quay_height_8658aca):
        _name_boundary.attributes(quay_self_2ef58ac)['parent'] = quay_parent_d1d6c81
        _name_boundary.attributes(quay_self_2ef58ac)['x'] = quay_x_5021b6a
        _name_boundary.attributes(quay_self_2ef58ac)['y'] = quay_y_41d1f47
        _name_boundary.attributes(quay_self_2ef58ac)['width'] = quay_width_6f378c4
        _name_boundary.attributes(quay_self_2ef58ac)['height'] = quay_height_8658aca

    @_name_boundary.callable_contract({'self': 'quay_self_7021788', 'x': 'quay_x_afba009', 'y': 'quay_y_87526c5'}, 'coord_translate')
    def quay_coord_translate(quay_self_7021788, quay_x_afba009, quay_y_87526c5):
        quay_px_ae389d6, quay_py_9cce8c9 = _name_boundary.attributes(_name_boundary.attributes(quay_self_7021788)['parent'])['coord_translate'](_name_boundary.attributes(quay_self_7021788)['x'], _name_boundary.attributes(quay_self_7021788)['y'])
        return (quay_x_afba009 - quay_px_ae389d6, quay_y_87526c5 - quay_py_9cce8c9)

    @_name_boundary.callable_contract({'self': 'quay_self_39d2bd3', 'x': 'quay_x_8d43ffd', 'y': 'quay_y_b6f9b0e', 'string': 'quay_string_07d98d5', 'attr': 'quay_attr_f8fb20c'}, 'write')
    def quay_write(quay_self_39d2bd3, quay_x_8d43ffd, quay_y_b6f9b0e, quay_string_07d98d5, quay_attr_f8fb20c):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_39d2bd3)['parent'])['write'](_name_boundary.attributes(quay_self_39d2bd3)['x'] + quay_x_8d43ffd, _name_boundary.attributes(quay_self_39d2bd3)['y'] + quay_y_b6f9b0e, quay_string_07d98d5, quay_attr_f8fb20c)

    @_name_boundary.callable_contract({'self': 'quay_self_2a7bf98', 'x': 'quay_x_9bac300', 'y': 'quay_y_285341c'}, 'is_click_inbounds')
    def quay_is_click_inbounds(quay_self_2a7bf98, quay_x_9bac300, quay_y_285341c):
        quay_min_x_7a97b98 = _name_boundary.attributes(quay_self_2a7bf98)['x']
        quay_max_x_228053d = _name_boundary.attributes(quay_self_2a7bf98)['x'] + _name_boundary.attributes(quay_self_2a7bf98)['width']
        quay_min_y_21f7189 = _name_boundary.attributes(quay_self_2a7bf98)['y']
        quay_max_y_2d4d402 = _name_boundary.attributes(quay_self_2a7bf98)['y'] + _name_boundary.attributes(quay_self_2a7bf98)['width']
        if quay_min_x_7a97b98 <= quay_x_9bac300 <= quay_max_x_228053d:
            if quay_min_y_21f7189 <= quay_y_285341c <= quay_max_y_2d4d402:
                return True
        return False

@_name_boundary.class_contract('ScrollingDisplayBuffer', {'find_clean_breakpoint': 'quay_find_clean_breakpoint', 'process_lines': 'quay_process_lines', 'draw_lines': 'quay_draw_lines', 'rendered_lines_from': 'quay_rendered_lines_from', 'box': 'quay_box', 'scrollcursor': 'quay_scrollcursor', 'parent': 'quay_parent', 'x': 'quay_x', 'y': 'quay_y', 'width': 'quay_width', 'height': 'quay_height', 'render_attr': 'quay_render_attr', 'lines': 'quay_lines', 'processed_lines': 'quay_processed_lines', 'pinned_lines': 'quay_pinned_lines', 'wrap': 'quay_wrap', 'clean_wrap': 'quay_clean_wrap', 'filled_line_count': 'quay_filled_line_count'})
class quay_ScrollingDisplayBuffer:
    """
    A ScrollingDisplayBuffer is a text-rendering abstraction to be placed within a standard Box.

    Set its `.lines` attribute, call .draw_lines(), and it will render those lines, cleanly wrapping them and
        implementing scrolling logic to move up and down the rendered buffer.
    """

    @_name_boundary.callable_contract({'self': 'quay_self_2811611', 'parent': 'quay_parent_360381d', 'x': 'quay_x_4a9b1cd', 'y': 'quay_y_cbf3bf0', 'width': 'quay_width_4e7261d', 'height': 'quay_height_b55efe4'}, '__init__')
    def __init__(quay_self_2811611, quay_parent_360381d, quay_x_4a9b1cd, quay_y_cbf3bf0, quay_width_4e7261d, quay_height_b55efe4):
        _name_boundary.attributes(quay_self_2811611)['box'] = quay_Box(quay_parent_360381d, quay_x_4a9b1cd, quay_y_cbf3bf0 + 1, quay_width_4e7261d, quay_height_b55efe4)
        _name_boundary.attributes(quay_self_2811611)['scrollcursor'] = 0
        _name_boundary.attributes(quay_self_2811611)['parent'] = quay_parent_360381d
        _name_boundary.attributes(quay_self_2811611)['x'] = _name_boundary.attributes(quay_parent_360381d)['x']
        _name_boundary.attributes(quay_self_2811611)['y'] = _name_boundary.attributes(quay_parent_360381d)['y']
        _name_boundary.attributes(quay_self_2811611)['width'] = quay_width_4e7261d
        _name_boundary.attributes(quay_self_2811611)['height'] = quay_height_b55efe4
        _name_boundary.attributes(quay_self_2811611)['render_attr'] = quay_curses.A_NORMAL
        _name_boundary.attributes(quay_self_2811611)['lines'] = []
        _name_boundary.attributes(quay_self_2811611)['processed_lines'] = []
        _name_boundary.attributes(quay_self_2811611)['pinned_lines'] = []
        _name_boundary.attributes(quay_self_2811611)['wrap'] = True
        _name_boundary.attributes(quay_self_2811611)['clean_wrap'] = True
        _name_boundary.attributes(quay_self_2811611)['filled_line_count'] = 0

    @staticmethod
    @_name_boundary.callable_contract({'text': 'quay_text_7b47a2a', 'maxwidth': 'quay_maxwidth_3ea6c2b'}, 'find_clean_breakpoint')
    def quay_find_clean_breakpoint(quay_text_7b47a2a, quay_maxwidth_3ea6c2b):
        """Find a clean place to wrap a line, if one exists

        :param text:
        :param maxwidth:
        :return:
        """
        if isinstance(quay_text_7b47a2a, quay_AttributedString):
            quay_text_7b47a2a = _name_boundary.attributes(quay_text_7b47a2a)['string']
        quay_max_text_f6dd9c4 = quay_text_7b47a2a[:quay_maxwidth_3ea6c2b]
        quay_max_text_f6dd9c4 = quay_max_text_f6dd9c4.strip()
        quay_break_index_61022a2 = quay_maxwidth_3ea6c2b
        for quay_bindex_3249b1e, quay_c_f27a264 in enumerate(quay_max_text_f6dd9c4[::-1]):
            if quay_c_f27a264 == ' ':
                quay_break_index_61022a2 = quay_maxwidth_3ea6c2b - quay_bindex_3249b1e
                break
        if quay_break_index_61022a2 == quay_maxwidth_3ea6c2b:
            for quay_bindex_3249b1e, quay_c_f27a264 in enumerate(quay_max_text_f6dd9c4[::-1]):
                if quay_c_f27a264 == '/':
                    quay_break_index_61022a2 = quay_maxwidth_3ea6c2b - quay_bindex_3249b1e - 1
                    break
        return quay_break_index_61022a2

    @_name_boundary.callable_contract({'self': 'quay_self_d4ee6f0'}, 'process_lines')
    def quay_process_lines(quay_self_d4ee6f0):
        """Process raw lines into a cleanly wrapped version that fits within our buffer's bounds.

        This method is intensive, *do not!* call it on every redraw, it will destroy performance. Call it as little
            as possible

        :return:
        """
        _name_boundary.attributes(quay_self_d4ee6f0)['pinned_lines'] = []
        if _name_boundary.attributes(quay_self_d4ee6f0)['wrap']:
            quay_wrapped_lines_8d27bdc = []
            if len(_name_boundary.attributes(quay_self_d4ee6f0)['lines']) > 0 and isinstance(_name_boundary.attributes(quay_self_d4ee6f0)['lines'][0], quay_LazilyProcessedTextBuffer):
                if not _name_boundary.attributes(_name_boundary.attributes(quay_self_d4ee6f0)['lines'][0])['processed']:
                    _name_boundary.attributes(_name_boundary.attributes(quay_self_d4ee6f0)['lines'][0])['go']()
                _name_boundary.attributes(quay_self_d4ee6f0)['lines'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_d4ee6f0)['lines'][0])['lines'] + _name_boundary.attributes(quay_self_d4ee6f0)['lines'][1:]
            for quay_line_3f7502c in _name_boundary.attributes(quay_self_d4ee6f0)['lines']:
                if isinstance(quay_line_3f7502c, quay_Table):
                    quay_wrapped_lines_8d27bdc.append(quay_line_3f7502c)
                    _name_boundary.attributes(quay_self_d4ee6f0)['filled_line_count'] = -1
                    continue
                if not isinstance(quay_line_3f7502c, quay_AttributedString):
                    quay_line_3f7502c = quay_AttributedString(quay_line_3f7502c)
                quay_max_size_60ac0f5 = _name_boundary.attributes(quay_self_d4ee6f0)['width']
                quay_indent_size_837a593 = 10
                quay_indenting_017a5ec = False
                quay_lines_15d8be8 = []
                quay_curs_197dad1 = 0
                while True:
                    quay_slice_size_9e67cb3 = quay_max_size_60ac0f5 if not quay_indenting_017a5ec else quay_max_size_60ac0f5 - quay_indent_size_837a593
                    quay_slice_size_9e67cb3 = min(quay_slice_size_9e67cb3, len(_name_boundary.attributes(quay_line_3f7502c)['string']) - quay_curs_197dad1)
                    if len(_name_boundary.attributes(quay_line_3f7502c)['string']) + 10 - quay_curs_197dad1 > quay_max_size_60ac0f5:
                        quay_slice_size_9e67cb3 = _name_boundary.attributes(quay_self_d4ee6f0)['find_clean_breakpoint'](_name_boundary.attributes(quay_line_3f7502c)['string'][quay_curs_197dad1:quay_curs_197dad1 + quay_slice_size_9e67cb3], quay_slice_size_9e67cb3)
                    quay_text_f6a1297 = _name_boundary.attributes(quay_line_3f7502c)['string'][quay_curs_197dad1:quay_curs_197dad1 + quay_slice_size_9e67cb3]
                    if quay_indenting_017a5ec:
                        quay_text_f6a1297 = ' ' * 10 + quay_text_f6a1297
                    quay_lines_15d8be8.append(quay_text_f6a1297)
                    quay_curs_197dad1 += quay_slice_size_9e67cb3
                    if len(_name_boundary.attributes(quay_line_3f7502c)['string']) + 10 - quay_curs_197dad1 <= quay_max_size_60ac0f5:
                        quay_text_f6a1297 = _name_boundary.attributes(quay_line_3f7502c)['string'][quay_curs_197dad1:]
                        if quay_text_f6a1297.strip() == '':
                            break
                        quay_text_f6a1297 = ' ' * 10 + quay_text_f6a1297
                        quay_lines_15d8be8.append(quay_text_f6a1297)
                        break
                    quay_indenting_017a5ec = True
                if quay_lines_15d8be8[-1] == '' and len(quay_lines_15d8be8) > 1:
                    quay_lines_15d8be8.pop()
                if len(_name_boundary.attributes(quay_line_3f7502c)['attrs']) > 0:
                    quay_attributes_3c3ad8f = _name_boundary.attributes(quay_line_3f7502c)['attrs']
                    quay_curs_197dad1 = 0
                    quay_alines_e5f78e4 = []
                    quay_indenting_017a5ec = False
                    for quay_wline_f328d0f in quay_lines_15d8be8:
                        if len(quay_wline_f328d0f) > _name_boundary.attributes(quay_self_d4ee6f0)['width']:
                            global quay_PANIC_STRING
                            quay_PANIC_STRING = 'Line wrapping code failed sanity check: String width was larger than window size'
                            raise quay_PanicException
                        quay_attr_str_344e15a = quay_AttributedString(quay_wline_f328d0f)
                        for quay_attr_d5128fa in quay_attributes_3c3ad8f:
                            quay_attr_start_72f4f65 = max(quay_attr_d5128fa[0][0] - quay_curs_197dad1, 0)
                            quay_attr_end_a7000c3 = quay_attr_d5128fa[0][1] - quay_curs_197dad1
                            if quay_attr_end_a7000c3 > 0:
                                if quay_indenting_017a5ec:
                                    quay_attr_start_72f4f65 += 10
                                    quay_attr_end_a7000c3 += 10
                                _name_boundary.attributes(quay_attr_str_344e15a)['set_attr'](quay_attr_start_72f4f65, quay_attr_end_a7000c3, quay_attr_d5128fa[1])
                        quay_alines_e5f78e4.append(quay_attr_str_344e15a)
                        quay_curs_197dad1 += len(quay_wline_f328d0f)
                        quay_indenting_017a5ec = True
                    quay_lines_15d8be8 = quay_alines_e5f78e4
                quay_wrapped_lines_8d27bdc += quay_lines_15d8be8
            if not _name_boundary.attributes(quay_self_d4ee6f0)['filled_line_count'] == -1:
                _name_boundary.attributes(quay_self_d4ee6f0)['filled_line_count'] = len(quay_wrapped_lines_8d27bdc)
            _name_boundary.attributes(quay_self_d4ee6f0)['processed_lines'] = quay_wrapped_lines_8d27bdc
        else:
            quay_trunc_lines_bceb499 = []
            for quay_line_3f7502c in _name_boundary.attributes(quay_self_d4ee6f0)['lines']:
                if not isinstance(quay_line_3f7502c, quay_AttributedString):
                    quay_line_3f7502c = quay_AttributedString(quay_line_3f7502c)
                if len(_name_boundary.attributes(quay_line_3f7502c)['string']) > _name_boundary.attributes(quay_self_d4ee6f0)['width']:
                    quay_slice_size_9e67cb3 = _name_boundary.attributes(quay_self_d4ee6f0)['width']
                    _name_boundary.attributes(quay_line_3f7502c)['string'] = _name_boundary.attributes(quay_line_3f7502c)['string'][0:quay_slice_size_9e67cb3 - 3] + '...'
                    quay_trunc_lines_bceb499.append(quay_line_3f7502c)
                else:
                    quay_trunc_lines_bceb499.append(quay_line_3f7502c)
            _name_boundary.attributes(quay_self_d4ee6f0)['filled_line_count'] = len(_name_boundary.attributes(quay_self_d4ee6f0)['lines'])
            _name_boundary.attributes(quay_self_d4ee6f0)['processed_lines'] = quay_trunc_lines_bceb499

    @_name_boundary.callable_contract({'self': 'quay_self_3396bf1'}, 'draw_lines')
    def quay_draw_lines(quay_self_3396bf1):
        """Update the internal representation of lines to be displayed.

        :return:
        """
        quay_x_9b5fc5d = 0
        quay_display_lines_4dcf686 = _name_boundary.attributes(quay_self_3396bf1)['rendered_lines_from'](_name_boundary.attributes(quay_self_3396bf1)['processed_lines'], _name_boundary.attributes(quay_self_3396bf1)['scrollcursor'])
        for quay_y_19e6b76, quay_line_fc0a10e in enumerate(quay_display_lines_4dcf686):
            if isinstance(quay_line_fc0a10e, quay_AttributedString):
                quay_text_644cf25 = _name_boundary.attributes(quay_line_fc0a10e)['string']
                _name_boundary.attributes(_name_boundary.attributes(quay_self_3396bf1)['box'])['write'](quay_x_9b5fc5d, quay_y_19e6b76, quay_text_644cf25, _name_boundary.attributes(quay_self_3396bf1)['render_attr'])
                for quay_attribute_9b2d6db in _name_boundary.attributes(quay_line_fc0a10e)['attrs']:
                    quay_attr_start_e699137 = quay_attribute_9b2d6db[0][0]
                    if quay_attr_start_e699137 < 0:
                        continue
                    quay_attr_end_d61dfe6 = max(quay_attribute_9b2d6db[0][1], _name_boundary.attributes(_name_boundary.attributes(quay_self_3396bf1)['box'])['width'])
                    quay_attr_c5c105a = quay_attribute_9b2d6db[1]
                    try:
                        _name_boundary.attributes(_name_boundary.attributes(quay_self_3396bf1)['box'])['write'](quay_x_9b5fc5d + quay_attr_start_e699137, quay_y_19e6b76, quay_text_644cf25[quay_attr_start_e699137:quay_attr_end_d61dfe6 - 1], quay_attr_c5c105a)
                    except quay_PanicException:
                        pass
            else:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_3396bf1)['box'])['write'](quay_x_9b5fc5d, quay_y_19e6b76, quay_line_fc0a10e.ljust(_name_boundary.attributes(quay_self_3396bf1)['width'], ' '), _name_boundary.attributes(quay_self_3396bf1)['render_attr'])

    @_name_boundary.callable_contract({'self': 'quay_self_119eced', 'lines': 'quay_lines_c4d8c66', 'start_line': 'quay_start_line_c4696c1'}, 'rendered_lines_from')
    def quay_rendered_lines_from(quay_self_119eced, quay_lines_c4d8c66, quay_start_line_c4696c1):
        """Return slice of lines based on window height

        :param lines: Full set of lines
        :param start_line: Line start
        :return: Slice of lines
        """
        quay_end_line_dbb893f = quay_start_line_c4696c1 + _name_boundary.attributes(quay_self_119eced)['height'] - 1
        quay_pincount_b4d0082 = 0
        quay_pins_904803a = []
        quay_prop_lines_2a841d8 = [*quay_lines_c4d8c66]
        for quay_i_631c38a, quay_line_485025d in enumerate(quay_lines_c4d8c66):
            if isinstance(quay_line_485025d, quay_Table):
                quay_prop_lines_2a841d8 = quay_lines_c4d8c66[:quay_i_631c38a]
                quay_table_lines_02f25ae = _name_boundary.attributes(quay_line_485025d)['fetch'](quay_start_line_c4696c1, int(_name_boundary.attributes(quay_self_119eced)['height']), _name_boundary.attributes(quay_self_119eced)['width']).split('\n')
                quay_table_attr_lines_18bc188 = []
                for quay__line_39c2314 in quay_table_lines_02f25ae:
                    quay_table_attr_lines_18bc188.append(_name_boundary.attributes(quay_AttributedString)['ansi_to_attrstr'](quay__line_39c2314))
                quay_prop_lines_2a841d8 += quay_table_attr_lines_18bc188
                quay_start_line_c4696c1 = 0
                quay_end_line_dbb893f = _name_boundary.attributes(quay_self_119eced)['height'] - 1
        return quay_pins_904803a + quay_prop_lines_2a841d8[quay_start_line_c4696c1 + quay_pincount_b4d0082:quay_end_line_dbb893f]

@_name_boundary.class_contract('View', {'add_subview': 'quay_add_subview', 'coord_translate': 'quay_coord_translate', 'redraw': 'quay_redraw', 'handle_key_press': 'quay_handle_key_press', 'handle_mouse': 'quay_handle_mouse', 'box': 'quay_box', 'children': 'quay_children', 'draw': 'quay_draw'})
class quay_View:
    """
    Base View Class - Used for views that don't require too much complex functionality to render.
    """

    @_name_boundary.callable_contract({'self': 'quay_self_081dc9a'}, '__init__')
    def __init__(quay_self_081dc9a):
        _name_boundary.attributes(quay_self_081dc9a)['box'] = None
        _name_boundary.attributes(quay_self_081dc9a)['children'] = []
        _name_boundary.attributes(quay_self_081dc9a)['draw'] = True

    @_name_boundary.callable_contract({'self': 'quay_self_5f73642', 'view': 'quay_view_8b30240'}, 'add_subview')
    def quay_add_subview(quay_self_5f73642, quay_view_8b30240):
        if quay_view_8b30240 not in _name_boundary.attributes(quay_self_5f73642)['children']:
            _name_boundary.attributes(quay_self_5f73642)['children'].append(quay_view_8b30240)

    @_name_boundary.callable_contract({'self': 'quay_self_a08078a', 'x': 'quay_x_266e623', 'y': 'quay_y_153f887'}, 'coord_translate')
    def quay_coord_translate(quay_self_a08078a, quay_x_266e623, quay_y_153f887):
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_a08078a)['box'])['coord_translate'](quay_x_266e623, quay_y_153f887)

    @_name_boundary.callable_contract({'self': 'quay_self_ec7d96a'}, 'redraw')
    def quay_redraw(quay_self_ec7d96a):
        """
        The .redraw() method is called by the view controller and should be implemented by subclasses to
            re-update the self.box property with its contents. This is how all Views should handle updating/changing
            their content.

        :return:
        """
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_96418fd', 'key': 'quay_key_202c842'}, 'handle_key_press')
    def quay_handle_key_press(quay_self_96418fd, quay_key_202c842):
        """
        This method is called by the View Controller and is passed key-press events.

        key-press events are passed if the View Controller or higher-priority views dont absorb the keypress event.
        If this view decides it should handle it (by returning True), the key-press will be "handled" and not passed
            to any other Views.

        :param key: Key ordinal
        :return: True or False; whether the keypress was handled by this View
        """
        return False

    @_name_boundary.callable_contract({'self': 'quay_self_3bae4e0', 'x': 'quay_x_2f8a248', 'y': 'quay_y_0b6cae0'}, 'handle_mouse')
    def quay_handle_mouse(quay_self_3bae4e0, quay_x_2f8a248, quay_y_0b6cae0):
        """
        This method is called by the View Controller and is passed mouse events.

        Mouse events are passed if the VC itself or higher-priority views dont absorb the mouse event.
        If this view decides it should handle it (by returning True), the mouse event will be "handled" and not passed
            to any other Views.

        :param x: X coordinate of the mouse-press
        :param y: Y coordinate of the mouse-press
        :return: True or False; whether the keypress was handled by this View
        """
        for quay_child_0c277f2 in _name_boundary.attributes(quay_self_3bae4e0)['children']:
            if _name_boundary.attributes(quay_child_0c277f2)['handle_mouse'](quay_x_2f8a248, quay_y_0b6cae0):
                return True
        return False

@_name_boundary.class_contract('ScrollView', {'scroll_view': 'quay_scroll_view', 'scroll_view_text_buffer': 'quay_scroll_view_text_buffer', 'scroll_cursor': 'quay_scroll_cursor'})
class quay_ScrollView(quay_View):
    """
    ScrollView - Used for views which may display text/lists that require scrolling functionality
    """

    @_name_boundary.callable_contract({'self': 'quay_self_ff7a4de'}, '__init__')
    def __init__(quay_self_ff7a4de):
        super().__init__()
        _name_boundary.attributes(quay_self_ff7a4de)['scroll_view'] = None
        _name_boundary.attributes(quay_self_ff7a4de)['scroll_view_text_buffer'] = None
        _name_boundary.attributes(quay_self_ff7a4de)['scroll_cursor'] = 0

@_name_boundary.class_contract('Button', {'set_text': 'quay_set_text', 'redraw': 'quay_redraw', 'handle_mouse': 'quay_handle_mouse', 'action': 'quay_action', 'text': 'quay_text', 'box': 'quay_box'})
class quay_Button(quay_View):

    @_name_boundary.callable_contract({'self': 'quay_self_bc0d216', 'parent': 'quay_parent_24e98bd', 'x': 'quay_x_d61e48a', 'y': 'quay_y_5aa7ca8', 'height': 'quay_height_e387ecf'}, '__init__')
    def __init__(quay_self_bc0d216, quay_parent_24e98bd, quay_x_d61e48a, quay_y_5aa7ca8, quay_height_e387ecf):
        super().__init__()
        _name_boundary.attributes(quay_self_bc0d216)['text'] = ''
        _name_boundary.attributes(quay_self_bc0d216)['box'] = quay_Box(_name_boundary.attributes(quay_parent_24e98bd)['box'], quay_x_d61e48a, quay_y_5aa7ca8, 0, quay_height_e387ecf)

    @_name_boundary.callable_contract({'self': 'quay_self_8fbef5d', 'text': 'quay_text_a09cb41'}, 'set_text')
    def quay_set_text(quay_self_8fbef5d, quay_text_a09cb41):
        _name_boundary.attributes(quay_self_8fbef5d)['text'] = quay_text_a09cb41
        _name_boundary.attributes(_name_boundary.attributes(quay_self_8fbef5d)['box'])['width'] = len(quay_text_a09cb41)

    @_name_boundary.callable_contract({'self': 'quay_self_0b942ce'}, 'redraw')
    def quay_redraw(quay_self_0b942ce):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0b942ce)['box'])['write'](0, 0, _name_boundary.attributes(quay_self_0b942ce)['text'], quay_curses.A_NORMAL)

    @_name_boundary.callable_contract({'self': 'quay_self_e1f0247', 'x': 'quay_x_bdee7b0', 'y': 'quay_y_dc0220a'}, 'handle_mouse')
    def quay_handle_mouse(quay_self_e1f0247, quay_x_bdee7b0, quay_y_dc0220a):
        quay_tx_4964da4, quay_ty_240d657 = _name_boundary.attributes(_name_boundary.attributes(quay_self_e1f0247)['box'])['coord_translate'](quay_x_bdee7b0, quay_y_dc0220a)
        if 0 <= quay_tx_4964da4 <= _name_boundary.attributes(_name_boundary.attributes(quay_self_e1f0247)['box'])['width']:
            if 0 <= quay_ty_240d657 <= _name_boundary.attributes(_name_boundary.attributes(quay_self_e1f0247)['box'])['height']:
                _name_boundary.attributes(quay_self_e1f0247)['action']()
                return True
        return False

    @_name_boundary.callable_contract({'self': 'quay_self_b767cfe'}, 'action')
    def quay_action(quay_self_b767cfe):
        pass

@_name_boundary.class_contract('TitleBarMenuItem', {'text': 'quay_text', 'rend_text': 'quay_rend_text', 'rend_width': 'quay_rend_width', 'menu_items': 'quay_menu_items'})
class quay_TitleBarMenuItem:

    @_name_boundary.callable_contract({'self': 'quay_self_9a18f2d', 'text': 'quay_text_fc354c7'}, '__init__')
    def __init__(quay_self_9a18f2d, quay_text_fc354c7):
        _name_boundary.attributes(quay_self_9a18f2d)['text'] = quay_text_fc354c7
        _name_boundary.attributes(quay_self_9a18f2d)['rend_text'] = f' {quay_text_fc354c7} '
        _name_boundary.attributes(quay_self_9a18f2d)['rend_width'] = len(_name_boundary.attributes(quay_self_9a18f2d)['rend_text'])
        _name_boundary.attributes(quay_self_9a18f2d)['menu_items'] = []

@_name_boundary.class_contract('HelpMenuItem', {'function': 'quay_function'})
class quay_HelpMenuItem(quay_TitleBarMenuItem):

    @_name_boundary.callable_contract({'self': 'quay_self_0418153'}, '__init__')
    def __init__(quay_self_0418153):
        super().__init__('Help')

    @_name_boundary.callable_contract({'self': 'quay_self_9b1a112'}, 'function')
    def quay_function(quay_self_9b1a112):
        raise quay_HelpMenuException

@_name_boundary.class_contract('FileMenuItem', {'open': 'quay_open', 'save': 'quay_save', 'menu_items': 'quay_menu_items'})
class quay_FileMenuItem(quay_TitleBarMenuItem):

    @_name_boundary.callable_contract({'self': 'quay_self_3e444a8'}, '__init__')
    def __init__(quay_self_3e444a8):
        super().__init__('File')
        _name_boundary.attributes(quay_self_3e444a8)['menu_items'].append(('Open', _name_boundary.attributes(quay_self_3e444a8)['open']))
        _name_boundary.attributes(quay_self_3e444a8)['menu_items'].append(('Save Edits', _name_boundary.attributes(quay_self_3e444a8)['save']))

    @_name_boundary.callable_contract({'self': 'quay_self_2f40b81'}, 'open')
    def quay_open(quay_self_2f40b81):
        raise quay_FileBrowserOpenNewFileException

    @_name_boundary.callable_contract({'self': 'quay_self_102f963'}, 'save')
    def quay_save(quay_self_102f963):
        pass

@_name_boundary.class_contract('EditMenuItem', {'delete': 'quay_delete', 'menu_items': 'quay_menu_items'})
class quay_EditMenuItem(quay_TitleBarMenuItem):

    @_name_boundary.callable_contract({'self': 'quay_self_fbd31d1'}, '__init__')
    def __init__(quay_self_fbd31d1):
        super().__init__('Edit')
        _name_boundary.attributes(quay_self_fbd31d1)['menu_items'].append(('Delete Item', _name_boundary.attributes(quay_self_fbd31d1)['delete']))

    @_name_boundary.callable_contract({'self': 'quay_self_1af46c8'}, 'delete')
    def quay_delete(quay_self_1af46c8):
        pass

@_name_boundary.class_contract('DumpMenuItem', {'headers': 'quay_headers', 'tbd': 'quay_tbd', 'menu_items': 'quay_menu_items'})
class quay_DumpMenuItem(quay_TitleBarMenuItem):

    @_name_boundary.callable_contract({'self': 'quay_self_357d01b'}, '__init__')
    def __init__(quay_self_357d01b):
        super().__init__('Dump')
        _name_boundary.attributes(quay_self_357d01b)['menu_items'].append(('Dump Headers', _name_boundary.attributes(quay_self_357d01b)['headers']))
        _name_boundary.attributes(quay_self_357d01b)['menu_items'].append(('Dump TAPI stub', _name_boundary.attributes(quay_self_357d01b)['tbd']))

    @_name_boundary.callable_contract({'self': 'quay_self_5efb437'}, 'headers')
    def quay_headers(quay_self_5efb437):
        pass

    @_name_boundary.callable_contract({'self': 'quay_self_c9e66d7'}, 'tbd')
    def quay_tbd(quay_self_c9e66d7):
        pass

@_name_boundary.class_contract('TitleBar', {'MENUS_START': 'quay_MENUS_START', 'exit': 'quay_exit', 'add_menu_item': 'quay_add_menu_item', 'redraw': 'quay_redraw', 'handle_key_press': 'quay_handle_key_press', 'handle_mouse': 'quay_handle_mouse', 'menu_items': 'quay_menu_items', 'menu_item_xy_map': 'quay_menu_item_xy_map', 'pres_menu_item': 'quay_pres_menu_item', 'pres_menu_item_index': 'quay_pres_menu_item_index', 'exit_button': 'quay_exit_button', 'children': 'quay_children', 'add_subview': 'quay_add_subview', 'box': 'quay_box'})
class quay_TitleBar(quay_View):
    """
    The Title Bar represents the top 1st line of the window.
    It's responsible for displaying the window title and menus
    """
    quay_MENUS_START = 10

    @_name_boundary.callable_contract({'self': 'quay_self_4ae6801'}, '__init__')
    def __init__(quay_self_4ae6801):
        super().__init__()
        _name_boundary.attributes(quay_self_4ae6801)['menu_items'] = []
        _name_boundary.attributes(quay_self_4ae6801)['menu_item_xy_map'] = {}
        _name_boundary.attributes(quay_self_4ae6801)['pres_menu_item'] = None
        _name_boundary.attributes(quay_self_4ae6801)['pres_menu_item_index'] = -1
        _name_boundary.attributes(quay_self_4ae6801)['add_menu_item'](quay_HelpMenuItem())
        _name_boundary.attributes(quay_self_4ae6801)['exit_button'] = quay_Button(quay_self_4ae6801, 0, 0, 1)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_4ae6801)['exit_button'])['set_text'](' Exit ')
        _name_boundary.attributes(_name_boundary.attributes(quay_self_4ae6801)['exit_button'])['action'] = _name_boundary.attributes(quay_self_4ae6801)['exit']
        _name_boundary.attributes(quay_self_4ae6801)['add_subview'](_name_boundary.attributes(quay_self_4ae6801)['exit_button'])

    @_name_boundary.callable_contract({'self': 'quay_self_274c349'}, 'exit')
    def quay_exit(quay_self_274c349):
        raise quay_ExitProgramException

    @_name_boundary.callable_contract({'self': 'quay_self_14e93d5', 'item': 'quay_item_bf624ee'}, 'add_menu_item')
    def quay_add_menu_item(quay_self_14e93d5, quay_item_bf624ee):
        if len(_name_boundary.attributes(quay_self_14e93d5)['menu_items']) > 0:
            quay_top_item_e79139c = _name_boundary.attributes(quay_self_14e93d5)['menu_items'][-1]
            quay_start_x_38f1ff6 = _name_boundary.attributes(quay_self_14e93d5)['menu_item_xy_map'][quay_top_item_e79139c][0] + _name_boundary.attributes(quay_top_item_e79139c)['rend_width'] + 2
        else:
            quay_start_x_38f1ff6 = _name_boundary.attributes(quay_TitleBar)['MENUS_START'] + 3
        _name_boundary.attributes(quay_self_14e93d5)['menu_items'].append(quay_item_bf624ee)
        _name_boundary.attributes(quay_self_14e93d5)['menu_item_xy_map'][quay_item_bf624ee] = [quay_start_x_38f1ff6, 0]

    @_name_boundary.callable_contract({'self': 'quay_self_7cb1dc0'}, 'redraw')
    def quay_redraw(quay_self_7cb1dc0):
        if not _name_boundary.attributes(quay_self_7cb1dc0)['box']:
            return
        _name_boundary.attributes(_name_boundary.attributes(quay_self_7cb1dc0)['box'])['write'](0, 0, '╒' + '═'.ljust(quay_curses.COLS - 3, '═') + '╕', quay_curses.color_pair(9))
        _name_boundary.attributes(_name_boundary.attributes(quay_self_7cb1dc0)['box'])['write'](2, 0, f' {quay_WINDOW_NAME} ', quay_curses.A_NORMAL)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_7cb1dc0)['box'])['write'](0, 1, '┟' + ''.ljust(quay_curses.COLS - 3, '━') + '┦', quay_curses.color_pair(9))
        _name_boundary.attributes(_name_boundary.attributes(quay_self_7cb1dc0)['box'])['write'](_name_boundary.attributes(quay_TitleBar)['MENUS_START'], 0, '╤', quay_curses.color_pair(9))
        _name_boundary.attributes(_name_boundary.attributes(quay_self_7cb1dc0)['box'])['write'](_name_boundary.attributes(quay_TitleBar)['MENUS_START'], 1, '┸', quay_curses.color_pair(9))
        quay_x_a40f702 = _name_boundary.attributes(quay_TitleBar)['MENUS_START'] + 3
        for quay_item_37e4053 in _name_boundary.attributes(quay_self_7cb1dc0)['menu_items']:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_7cb1dc0)['box'])['write'](quay_x_a40f702, 0, _name_boundary.attributes(quay_item_37e4053)['rend_text'], quay_curses.A_NORMAL)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_7cb1dc0)['box'])['write'](quay_x_a40f702 + 1, 0, _name_boundary.attributes(quay_item_37e4053)['rend_text'][1], quay_curses.A_UNDERLINE)
            quay_x_a40f702 += _name_boundary.attributes(quay_item_37e4053)['rend_width'] + 2
        for quay_child_6f946e4 in _name_boundary.attributes(quay_self_7cb1dc0)['children']:
            _name_boundary.attributes(quay_child_6f946e4)['redraw']()

    @_name_boundary.callable_contract({'self': 'quay_self_b8da8b5', 'key': 'quay_key_f733a78'}, 'handle_key_press')
    def quay_handle_key_press(quay_self_b8da8b5, quay_key_f733a78):
        if _name_boundary.attributes(quay_self_b8da8b5)['pres_menu_item_index'] < 0:
            return False
        if quay_key_f733a78 == quay_curses.KEY_LEFT:
            if _name_boundary.attributes(quay_self_b8da8b5)['pres_menu_item_index'] > 0:
                quay_n_ind_8e44f94 = _name_boundary.attributes(quay_self_b8da8b5)['pres_menu_item_index'] - 1
                quay_n_item_e33e103 = _name_boundary.attributes(quay_self_b8da8b5)['menu_items'][quay_n_ind_8e44f94]
                quay_coords_35463e8 = _name_boundary.attributes(quay_self_b8da8b5)['menu_item_xy_map'][quay_n_item_e33e103]
                _name_boundary.attributes(quay_self_b8da8b5)['pres_menu_item'] = (quay_n_item_e33e103, quay_coords_35463e8[0])
                _name_boundary.attributes(quay_self_b8da8b5)['pres_menu_item_index'] = quay_n_ind_8e44f94
                raise quay_PresentTitleMenuException
        elif quay_key_f733a78 == quay_curses.KEY_RIGHT:
            if not _name_boundary.attributes(quay_self_b8da8b5)['pres_menu_item_index'] + 1 >= len(_name_boundary.attributes(quay_self_b8da8b5)['menu_items']):
                quay_n_ind_8e44f94 = _name_boundary.attributes(quay_self_b8da8b5)['pres_menu_item_index'] + 1
                quay_n_item_e33e103 = _name_boundary.attributes(quay_self_b8da8b5)['menu_items'][quay_n_ind_8e44f94]
                quay_coords_35463e8 = _name_boundary.attributes(quay_self_b8da8b5)['menu_item_xy_map'][quay_n_item_e33e103]
                _name_boundary.attributes(quay_self_b8da8b5)['pres_menu_item'] = (quay_n_item_e33e103, quay_coords_35463e8[0])
                _name_boundary.attributes(quay_self_b8da8b5)['pres_menu_item_index'] = quay_n_ind_8e44f94
                raise quay_PresentTitleMenuException
        return False

    @_name_boundary.callable_contract({'self': 'quay_self_34fa545', 'x': 'quay_x_97042b6', 'y': 'quay_y_ee4727d'}, 'handle_mouse')
    def quay_handle_mouse(quay_self_34fa545, quay_x_97042b6, quay_y_ee4727d):
        quay_handle_f2c150f = False
        if quay_y_ee4727d < 1:
            if _name_boundary.attributes(super())['handle_mouse'](quay_x_97042b6, quay_y_ee4727d):
                return True
            quay_handle_f2c150f = True
            if quay_x_97042b6 < 10:
                raise quay_PresentDebugMenuException
            quay_i_dc59f57 = 0
            for quay_item_30ba8b4, quay_coords_ed63b5b in _name_boundary.attributes(_name_boundary.attributes(quay_self_34fa545)['menu_item_xy_map'])['items']():
                if quay_coords_ed63b5b[0] <= quay_x_97042b6 <= quay_coords_ed63b5b[0] + _name_boundary.attributes(quay_item_30ba8b4)['rend_width']:
                    _name_boundary.attributes(quay_self_34fa545)['pres_menu_item'] = (quay_item_30ba8b4, quay_coords_ed63b5b[0])
                    _name_boundary.attributes(quay_self_34fa545)['pres_menu_item_index'] = quay_i_dc59f57
                    raise quay_PresentTitleMenuException
                quay_i_dc59f57 += 1
        return quay_handle_f2c150f

@_name_boundary.class_contract('FooterBar', {'MENUS_START': 'quay_MENUS_START', 'redraw': 'quay_redraw', 'show_debug': 'quay_show_debug', 'debug_text': 'quay_debug_text', 'hi_text': 'quay_hi_text', 'now': 'quay_now', 'box': 'quay_box'})
class quay_FooterBar(quay_View):
    quay_MENUS_START = 40

    @_name_boundary.callable_contract({'self': 'quay_self_47d7f25'}, '__init__')
    def __init__(quay_self_47d7f25):
        super().__init__()
        _name_boundary.attributes(quay_self_47d7f25)['show_debug'] = False
        _name_boundary.attributes(quay_self_47d7f25)['debug_text'] = ''
        _name_boundary.attributes(quay_self_47d7f25)['hi_text'] = ''
        _name_boundary.attributes(quay_self_47d7f25)['now'] = _name_boundary.attributes(quay_datetime)['now']().time()
        quay_graveyard_97f38e1 = 'hope your night is going well'
        quay_morning_5ae26c6 = 'good morning! :)'
        quay_afternoon_4d88ade = 'good afternoon'
        quay_evening_76179d2 = 'good evening ~'
        quay_msgmap_b0fd37b = {(22, 24): quay_graveyard_97f38e1, (0, 4): quay_graveyard_97f38e1, (5, 11): quay_morning_5ae26c6, (12, 16): quay_afternoon_4d88ade, (17, 21): quay_evening_76179d2}
        for quay_key_52ce53b, quay_val_86e965b in _name_boundary.attributes(quay_msgmap_b0fd37b)['items']():
            if _name_boundary.attributes(quay_self_47d7f25)['now'].hour in range(quay_key_52ce53b[0], quay_key_52ce53b[1] + 1):
                _name_boundary.attributes(quay_self_47d7f25)['hi_text'] = f' {quay_val_86e965b} '

    @_name_boundary.callable_contract({'self': 'quay_self_fd96531'}, 'redraw')
    def quay_redraw(quay_self_fd96531):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_fd96531)['box'])['write'](0, 0, '╘' + '═'.ljust(quay_curses.COLS - 3, '═') + '╛', quay_curses.color_pair(9))
        _name_boundary.attributes(_name_boundary.attributes(quay_self_fd96531)['box'])['write'](_name_boundary.attributes(quay_FooterBar)['MENUS_START'], 0, '╧', quay_curses.color_pair(9))
        if _name_boundary.attributes(quay_self_fd96531)['show_debug']:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_fd96531)['box'])['write'](_name_boundary.attributes(_name_boundary.attributes(quay_self_fd96531)['box'])['width'] - len(_name_boundary.attributes(quay_self_fd96531)['debug_text']) - 5, 0, _name_boundary.attributes(quay_self_fd96531)['debug_text'], quay_curses.A_NORMAL)
        else:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_fd96531)['box'])['write'](_name_boundary.attributes(_name_boundary.attributes(quay_self_fd96531)['box'])['width'] - len(_name_boundary.attributes(quay_self_fd96531)['hi_text']) - 5, 0, _name_boundary.attributes(quay_self_fd96531)['hi_text'], quay_curses.color_pair(9))

@_name_boundary.class_contract('SidebarMenuItem', {'parse_mmc': 'quay_parse_mmc', 'item_list_with_children': 'quay_item_list_with_children', 'name': 'quay_name', 'rend_name': 'quay_rend_name', 'content': 'quay_content', 'parent': 'quay_parent', 'children': 'quay_children', 'show_children': 'quay_show_children', 'selected': 'quay_selected'})
class quay_SidebarMenuItem:

    @_name_boundary.callable_contract({'self': 'quay_self_fa8c808', 'name': 'quay_name_8483fb2', 'menu_content': 'quay_menu_content_310b958', 'parent': 'quay_parent_78eb441'}, '__init__')
    def __init__(quay_self_fa8c808, quay_name_8483fb2: str, quay_menu_content_310b958, quay_parent_78eb441=None):
        _name_boundary.attributes(quay_self_fa8c808)['name'] = quay_name_8483fb2
        _name_boundary.attributes(quay_self_fa8c808)['rend_name'] = quay_name_8483fb2
        _name_boundary.attributes(quay_self_fa8c808)['content'] = quay_menu_content_310b958
        _name_boundary.attributes(quay_self_fa8c808)['parent'] = quay_parent_78eb441
        _name_boundary.attributes(quay_self_fa8c808)['children'] = []
        _name_boundary.attributes(quay_self_fa8c808)['show_children'] = False
        _name_boundary.attributes(quay_self_fa8c808)['selected'] = False

    @_name_boundary.callable_contract({'self': 'quay_self_0d8f96f'}, 'parse_mmc')
    def quay_parse_mmc(quay_self_0d8f96f):
        quay_lines_eb1a4ce = []
        for quay_item_097c5fa in _name_boundary.attributes(_name_boundary.attributes(quay_self_0d8f96f)['content'])['lines']:
            if isinstance(quay_item_097c5fa, str):
                quay_lines_eb1a4ce += quay_item_097c5fa.split('\n')
            else:
                quay_lines_eb1a4ce.append(quay_item_097c5fa)
        quay_attrib_content_458841b = []
        for quay_item_097c5fa in quay_lines_eb1a4ce:
            if isinstance(quay_item_097c5fa, str):
                quay_item_097c5fa = quay_item_097c5fa.replace('\t', '    ')
                quay_attrib_content_458841b.append(_name_boundary.attributes(quay_AttributedString)['ansi_to_attrstr'](quay_item_097c5fa))
            else:
                quay_attrib_content_458841b.append(quay_item_097c5fa)
        _name_boundary.attributes(quay_self_0d8f96f)['content'] = quay_MainMenuContentItem(quay_attrib_content_458841b)

    @staticmethod
    @_name_boundary.callable_contract({'menu_item': 'quay_menu_item_61ec647', 'depth': 'quay_depth_415ab6c'}, 'item_list_with_children')
    def quay_item_list_with_children(quay_menu_item_61ec647, quay_depth_415ab6c=1):
        """
        Recursive function that returns a single, non-nested, ordered list of items and their children for display.

        :param depth:
        :param menu_item: Root item to recurse through children of.
        :return: List of items generated
        """
        quay_items_92f0806 = [quay_menu_item_61ec647]
        if _name_boundary.attributes(quay_menu_item_61ec647)['show_children']:
            for quay_child_1bd9f62 in _name_boundary.attributes(quay_menu_item_61ec647)['children']:
                _name_boundary.attributes(quay_child_1bd9f62)['rend_name'] = '  ' * quay_depth_415ab6c + _name_boundary.attributes(quay_child_1bd9f62)['name']
                quay_items_92f0806 += _name_boundary.attributes(quay_SidebarMenuItem)['item_list_with_children'](quay_child_1bd9f62, quay_depth_415ab6c + 1)
        return quay_items_92f0806

@_name_boundary.class_contract('Sidebar', {'WIDTH': 'quay_WIDTH', 'redraw': 'quay_redraw', 'select_item': 'quay_select_item', 'update_item_listing': 'quay_update_item_listing', 'add_menu_item': 'quay_add_menu_item', 'collapse_index': 'quay_collapse_index', 'handle_key_press': 'quay_handle_key_press', 'handle_mouse': 'quay_handle_mouse', 'selected_index': 'quay_selected_index', 'current_sidebar_item_count': 'quay_current_sidebar_item_count', 'processed_items': 'quay_processed_items', 'items': 'quay_items', 'scroll_view_text_buffer': 'quay_scroll_view_text_buffer', 'box': 'quay_box'})
class quay_Sidebar(quay_ScrollView):
    quay_WIDTH = quay_SIDEBAR_WIDTH

    @_name_boundary.callable_contract({'self': 'quay_self_458c660'}, '__init__')
    def __init__(quay_self_458c660):
        super().__init__()
        _name_boundary.attributes(quay_self_458c660)['selected_index'] = 0
        _name_boundary.attributes(quay_self_458c660)['current_sidebar_item_count'] = 0
        _name_boundary.attributes(quay_self_458c660)['processed_items'] = []
        _name_boundary.attributes(quay_self_458c660)['items'] = []

    @_name_boundary.callable_contract({'self': 'quay_self_d145961'}, 'redraw')
    def quay_redraw(quay_self_d145961):
        _name_boundary.attributes(quay_self_d145961)['update_item_listing']()
        for quay_index_be02dd8 in range(0, quay_curses.LINES - 2):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_d145961)['box'])['write'](0, quay_index_be02dd8, quay_VERT_LINE, quay_curses.color_pair(9))
            _name_boundary.attributes(_name_boundary.attributes(quay_self_d145961)['box'])['write'](_name_boundary.attributes(quay_Sidebar)['WIDTH'], quay_index_be02dd8, quay_VERT_LINE, quay_curses.color_pair(9))
        _name_boundary.attributes(_name_boundary.attributes(quay_self_d145961)['box'])['write'](quay_SIDEBAR_WIDTH, 0, '┰', quay_curses.color_pair(9))

    @_name_boundary.callable_contract({'self': 'quay_self_3aaea1d', 'index': 'quay_index_4cb897d'}, 'select_item')
    def quay_select_item(quay_self_3aaea1d, quay_index_4cb897d):
        """
        Update selected item index and redraw the item listing.

        :param index:
        :return:
        """
        _name_boundary.attributes(quay_self_3aaea1d)['selected_index'] = quay_index_4cb897d
        _name_boundary.attributes(quay_self_3aaea1d)['update_item_listing']()

    @_name_boundary.callable_contract({'self': 'quay_self_9bc3ea5'}, 'update_item_listing')
    def quay_update_item_listing(quay_self_9bc3ea5):
        """
        Re-process the entire item listing to generate the content to be displayed.

        :return:
        """
        _name_boundary.attributes(quay_self_9bc3ea5)['processed_items'] = []
        for quay_item_d9d2430 in _name_boundary.attributes(quay_self_9bc3ea5)['items']:
            _name_boundary.attributes(quay_self_9bc3ea5)['processed_items'] += _name_boundary.attributes(quay_SidebarMenuItem)['item_list_with_children'](quay_item_d9d2430)
        _name_boundary.attributes(quay_self_9bc3ea5)['current_sidebar_item_count'] = len(_name_boundary.attributes(quay_self_9bc3ea5)['processed_items'])
        _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['lines'] = []
        for quay_index_2286432, quay_item_d9d2430 in enumerate(_name_boundary.attributes(quay_self_9bc3ea5)['processed_items']):
            quay_name_0695513 = _name_boundary.attributes(quay_item_d9d2430)['rend_name'].ljust(quay_SIDEBAR_WIDTH - 6, ' ')
            if len(_name_boundary.attributes(quay_item_d9d2430)['children']) > 0:
                if _name_boundary.attributes(quay_item_d9d2430)['show_children']:
                    quay_name_0695513 = quay_name_0695513 + '-'
                else:
                    quay_name_0695513 = quay_name_0695513 + '+'
            else:
                quay_name_0695513 = quay_name_0695513 + ' '
            if _name_boundary.attributes(quay_self_9bc3ea5)['selected_index'] == quay_index_2286432:
                quay_name_0695513 = quay_AttributedString(quay_name_0695513)
                _name_boundary.attributes(quay_name_0695513)['set_attr'](0, len(_name_boundary.attributes(quay_name_0695513)['string']) - 1, _name_boundary.attributes(quay_Attribute)['HIGHLIGHTED'])
                _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['lines'].append(quay_name_0695513)
            else:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['lines'].append(quay_name_0695513)
        quay_scroll_view_height_64eb0a2 = _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['height']
        if _name_boundary.attributes(quay_self_9bc3ea5)['selected_index'] - quay_scroll_view_height_64eb0a2 + 4 > _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['scrollcursor']:
            while _name_boundary.attributes(quay_self_9bc3ea5)['selected_index'] - quay_scroll_view_height_64eb0a2 + 4 > _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['scrollcursor']:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['scrollcursor'] += 1
        elif _name_boundary.attributes(quay_self_9bc3ea5)['selected_index'] < _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['scrollcursor'] + 2 and _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['scrollcursor'] > 0:
            while _name_boundary.attributes(quay_self_9bc3ea5)['selected_index'] < _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['scrollcursor'] + 2 and _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['scrollcursor'] > 0:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['scrollcursor'] -= 1
        _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['process_lines']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_9bc3ea5)['scroll_view_text_buffer'])['draw_lines']()

    @_name_boundary.callable_contract({'self': 'quay_self_f9ad9b0', 'item': 'quay_item_646e245'}, 'add_menu_item')
    def quay_add_menu_item(quay_self_f9ad9b0, quay_item_646e245):
        """
        Add a root menu item to the Sidebar and update the list.

        :param item:
        :return:
        """
        _name_boundary.attributes(quay_self_f9ad9b0)['items'].append(quay_item_646e245)
        _name_boundary.attributes(quay_self_f9ad9b0)['update_item_listing']()

    @_name_boundary.callable_contract({'self': 'quay_self_2db8822', 'index': 'quay_index_e35260f'}, 'collapse_index')
    def quay_collapse_index(quay_self_2db8822, quay_index_e35260f):
        """
        Collapse item at index if it is open.

        :param index:
        :return:
        """
        quay_item_8a32e01 = _name_boundary.attributes(quay_self_2db8822)['processed_items'][quay_index_e35260f]
        if len(_name_boundary.attributes(quay_item_8a32e01)['children']) > 0 and _name_boundary.attributes(quay_item_8a32e01)['show_children']:
            _name_boundary.attributes(quay_item_8a32e01)['show_children'] = False
            _name_boundary.attributes(quay_self_2db8822)['update_item_listing']()
        else:
            quay_swap_to_index_79c62ee = 0
            for quay_index_e35260f, quay_pitem_26f04ee in enumerate(_name_boundary.attributes(quay_self_2db8822)['processed_items']):
                if quay_pitem_26f04ee == _name_boundary.attributes(quay_item_8a32e01)['parent']:
                    quay_swap_to_index_79c62ee = quay_index_e35260f
                    break
            quay_pitem_26f04ee = _name_boundary.attributes(quay_self_2db8822)['processed_items'][quay_swap_to_index_79c62ee]
            _name_boundary.attributes(quay_pitem_26f04ee)['show_children'] = False
            _name_boundary.attributes(quay_self_2db8822)['update_item_listing']()
            _name_boundary.attributes(quay_self_2db8822)['select_item'](quay_swap_to_index_79c62ee)
            _name_boundary.attributes(quay_self_2db8822)['update_item_listing']()

    @_name_boundary.callable_contract({'self': 'quay_self_611373f', 'key': 'quay_key_1f28334'}, 'handle_key_press')
    def quay_handle_key_press(quay_self_611373f, quay_key_1f28334):
        if quay_key_1f28334 == quay_curses.KEY_UP:
            quay_index_a6a84d9 = _name_boundary.attributes(quay_self_611373f)['selected_index']
            if quay_index_a6a84d9 - 1 in range(0, _name_boundary.attributes(quay_self_611373f)['current_sidebar_item_count']):
                _name_boundary.attributes(quay_self_611373f)['select_item'](quay_index_a6a84d9 - 1)
        elif quay_key_1f28334 == quay_curses.KEY_DOWN:
            quay_index_a6a84d9 = _name_boundary.attributes(quay_self_611373f)['selected_index']
            if quay_index_a6a84d9 + 1 in range(0, _name_boundary.attributes(quay_self_611373f)['current_sidebar_item_count']):
                _name_boundary.attributes(quay_self_611373f)['select_item'](quay_index_a6a84d9 + 1)
        elif quay_key_1f28334 == quay_curses.KEY_LEFT:
            quay_index_a6a84d9 = _name_boundary.attributes(quay_self_611373f)['selected_index']
            _name_boundary.attributes(quay_self_611373f)['collapse_index'](quay_index_a6a84d9)
        elif quay_key_1f28334 == quay_curses.KEY_RIGHT:
            quay_index_a6a84d9 = _name_boundary.attributes(quay_self_611373f)['selected_index']
            quay_item_aaaef17 = _name_boundary.attributes(quay_self_611373f)['processed_items'][quay_index_a6a84d9]
            if len(_name_boundary.attributes(quay_item_aaaef17)['children']) > 0:
                _name_boundary.attributes(quay_item_aaaef17)['show_children'] = True
                _name_boundary.attributes(quay_self_611373f)['update_item_listing']()
        elif quay_key_1f28334 == ord(' '):
            quay_index_a6a84d9 = _name_boundary.attributes(quay_self_611373f)['selected_index']
            quay_item_aaaef17 = _name_boundary.attributes(quay_self_611373f)['processed_items'][quay_index_a6a84d9]
            if _name_boundary.attributes(quay_item_aaaef17)['show_children']:
                _name_boundary.attributes(quay_self_611373f)['collapse_index'](quay_index_a6a84d9)
            elif len(_name_boundary.attributes(quay_item_aaaef17)['children']) > 0:
                _name_boundary.attributes(quay_item_aaaef17)['show_children'] = True
                _name_boundary.attributes(quay_self_611373f)['update_item_listing']()
        else:
            return False
        return True

    @_name_boundary.callable_contract({'self': 'quay_self_ee6b180', 'x': 'quay_x_88ec27d', 'y': 'quay_y_9c64608'}, 'handle_mouse')
    def quay_handle_mouse(quay_self_ee6b180, quay_x_88ec27d, quay_y_9c64608):
        quay_absorb_d2a8681 = False
        if quay_x_88ec27d < quay_SIDEBAR_WIDTH and quay_y_9c64608 > _name_boundary.attributes(_name_boundary.attributes(quay_self_ee6b180)['box'])['y']:
            quay_absorb_d2a8681 = True
            quay_y_9c64608 = quay_y_9c64608 - 3
            quay_x_88ec27d = quay_x_88ec27d - 2
            if -1 <= quay_x_88ec27d - quay_SIDEBAR_WIDTH + 6 <= 1 and quay_y_9c64608 < len(_name_boundary.attributes(quay_self_ee6b180)['processed_items']):
                quay_index_15bf3ab = quay_y_9c64608
                quay_item_ceaa579 = _name_boundary.attributes(quay_self_ee6b180)['processed_items'][quay_index_15bf3ab]
                if len(_name_boundary.attributes(quay_item_ceaa579)['children']) > 0:
                    if _name_boundary.attributes(quay_item_ceaa579)['show_children']:
                        _name_boundary.attributes(quay_self_ee6b180)['selected_index'] = quay_y_9c64608
                        _name_boundary.attributes(quay_self_ee6b180)['collapse_index'](quay_y_9c64608)
                    else:
                        _name_boundary.attributes(quay_item_ceaa579)['show_children'] = True
                        _name_boundary.attributes(quay_self_ee6b180)['update_item_listing']()
            elif quay_y_9c64608 < len(_name_boundary.attributes(quay_self_ee6b180)['processed_items']):
                _name_boundary.attributes(quay_self_ee6b180)['select_item'](quay_y_9c64608)
        return quay_absorb_d2a8681

@_name_boundary.class_contract('MainMenuContentItem', {'lines': 'quay_lines'})
class quay_MainMenuContentItem:
    """
    Just holds the unprocessed lines to be displayed in the Main Menu.

    These are generated at the start and stored in Sidebar Menu Items, from which the View Controller pulls them out and
        displays the in the Main Screen.
    """

    @_name_boundary.callable_contract({'self': 'quay_self_30fc8e4', 'lines': 'quay_lines_9af2a4e'}, '__init__')
    def __init__(quay_self_30fc8e4, quay_lines_9af2a4e=None):
        if quay_lines_9af2a4e is None:
            quay_lines_9af2a4e = []
        _name_boundary.attributes(quay_self_30fc8e4)['lines'] = quay_lines_9af2a4e

@_name_boundary.class_contract('MainScreen', {'set_tab_name': 'quay_set_tab_name', 'redraw': 'quay_redraw', 'handle_key_press': 'quay_handle_key_press', 'info_box': 'quay_info_box', 'tabname': 'quay_tabname', 'highlighted': 'quay_highlighted', 'currently_displayed_index': 'quay_currently_displayed_index', 'scroll_view_text_buffer': 'quay_scroll_view_text_buffer', 'box': 'quay_box'})
class quay_MainScreen(quay_ScrollView):
    """
    Displays the currently relevant text from the context.
    """

    @_name_boundary.callable_contract({'self': 'quay_self_fca7c36'}, '__init__')
    def __init__(quay_self_fca7c36):
        super().__init__()
        _name_boundary.attributes(quay_self_fca7c36)['info_box'] = None
        _name_boundary.attributes(quay_self_fca7c36)['tabname'] = ''
        _name_boundary.attributes(quay_self_fca7c36)['highlighted'] = False
        _name_boundary.attributes(quay_self_fca7c36)['currently_displayed_index'] = 0

    @_name_boundary.callable_contract({'self': 'quay_self_e84cba9', 'name': 'quay_name_a9a8412'}, 'set_tab_name')
    def quay_set_tab_name(quay_self_e84cba9, quay_name_a9a8412):
        """
        Update the tab name

        :param name:
        :return:
        """
        _name_boundary.attributes(quay_self_e84cba9)['tabname'] = quay_name_a9a8412

    @_name_boundary.callable_contract({'self': 'quay_self_0348204'}, 'redraw')
    def quay_redraw(quay_self_0348204):
        quay_width_d53f04d = quay_curses.COLS - _name_boundary.attributes(quay_Sidebar)['WIDTH'] - 2
        for quay_index_e3d3c78 in range(0, quay_curses.LINES - 2):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_0348204)['box'])['write'](quay_width_d53f04d, quay_index_e3d3c78, quay_VERT_LINE, quay_curses.color_pair(9))
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0348204)['scroll_view_text_buffer'])['draw_lines']()
        quay_width_d53f04d = quay_curses.COLS - _name_boundary.attributes(quay_Sidebar)['WIDTH'] - 3
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0348204)['info_box'])['write'](-1, 1, '╞' + ''.ljust(quay_width_d53f04d, '═') + '╡', quay_curses.color_pair(9))
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0348204)['info_box'])['write'](2, 1, f"╡ {_name_boundary.attributes(quay_self_0348204)['tabname'].strip()} ╞", quay_curses.color_pair(9))
        _name_boundary.attributes(_name_boundary.attributes(quay_self_0348204)['info_box'])['write'](3, 1, f" {_name_boundary.attributes(quay_self_0348204)['tabname'].strip()} ", quay_curses.A_NORMAL if not _name_boundary.attributes(quay_self_0348204)['highlighted'] else quay_curses.A_STANDOUT)

    @_name_boundary.callable_contract({'self': 'quay_self_8843666', 'key': 'quay_key_b074219'}, 'handle_key_press')
    def quay_handle_key_press(quay_self_8843666, quay_key_b074219):
        if quay_key_b074219 == quay_curses.KEY_UP:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['scrollcursor'] = max(0, _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['scrollcursor'] - 1)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['draw_lines']()
            return True
        elif quay_key_b074219 == quay_curses.KEY_PPAGE:
            quay_j_height_4390d7e = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['box'])['height'] - 3
            for quay_i_abb44c4 in range(quay_j_height_4390d7e):
                _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['scrollcursor'] = max(0, _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['scrollcursor'] - 1)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['draw_lines']()
            return True
        elif quay_key_b074219 == quay_curses.KEY_DOWN:
            if _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['filled_line_count'] == -1:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['scrollcursor'] += 1
            else:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['scrollcursor'] = min(_name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['filled_line_count'] - _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['height'] + 1, _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['scrollcursor'] + 1)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['draw_lines']()
            return True
        elif quay_key_b074219 == quay_curses.KEY_NPAGE:
            quay_j_height_4390d7e = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['box'])['height'] - 3
            for quay_i_abb44c4 in range(quay_j_height_4390d7e):
                if _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['filled_line_count'] == -1:
                    _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['scrollcursor'] += 1
                else:
                    _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['scrollcursor'] = min(_name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['filled_line_count'] - _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['height'] + 1, _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['scrollcursor'] + 1)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_8843666)['scroll_view_text_buffer'])['draw_lines']()
            return True
        elif quay_key_b074219 == ord('d'):
            global quay_ATTR_STRING_DEBUG
            quay_ATTR_STRING_DEBUG = True
            raise quay_RebuildAllException
        return False

@_name_boundary.class_contract('DebugMenu', {'parse_lines': 'quay_parse_lines', 'redraw': 'quay_redraw', 'handle_key_press': 'quay_handle_key_press', 'handle_mouse': 'quay_handle_mouse', 'draw': 'quay_draw', 'scroll_view_text_buffer': 'quay_scroll_view_text_buffer', 'box': 'quay_box'})
class quay_DebugMenu(quay_ScrollView):

    @_name_boundary.callable_contract({'self': 'quay_self_ab7bcd6'}, '__init__')
    def __init__(quay_self_ab7bcd6):
        super().__init__()
        _name_boundary.attributes(quay_self_ab7bcd6)['draw'] = False

    @_name_boundary.callable_contract({'self': 'quay_self_a2c0e16'}, 'parse_lines')
    def quay_parse_lines(quay_self_a2c0e16):
        quay_attrib_content_cce915c = []
        for quay_item_2cac662 in _name_boundary.attributes(_name_boundary.attributes(quay_self_a2c0e16)['scroll_view_text_buffer'])['lines']:
            if isinstance(quay_item_2cac662, str):
                quay_attrib_content_cce915c.append(_name_boundary.attributes(quay_AttributedString)['ansi_to_attrstr'](quay_item_2cac662))
            else:
                quay_attrib_content_cce915c.append(quay_item_2cac662)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_a2c0e16)['scroll_view_text_buffer'])['lines'] = quay_attrib_content_cce915c

    @_name_boundary.callable_contract({'self': 'quay_self_2491a4f'}, 'redraw')
    def quay_redraw(quay_self_2491a4f):
        quay_width_42fe76c = _name_boundary.attributes(_name_boundary.attributes(quay_self_2491a4f)['box'])['width'] - 10
        quay_height_9104aa7 = _name_boundary.attributes(_name_boundary.attributes(quay_self_2491a4f)['box'])['height']
        quay_lc_042ac51 = '╒'
        quay_rc_3f3c84e = '╕'
        quay_div_e80f2a7 = '═'
        quay_bl_c5be8e0 = '╘'
        quay_br_cf8c0bd = '╛'
        quay_bgcolor_0833d5e = quay_curses.color_pair(1)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2491a4f)['box'])['write'](0, 0, quay_lc_042ac51 + ''.ljust(quay_width_42fe76c - 2, quay_div_e80f2a7) + quay_rc_3f3c84e, quay_bgcolor_0833d5e)
        for quay_line_80ceb00 in range(1, quay_height_9104aa7):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_2491a4f)['box'])['write'](0, quay_line_80ceb00, quay_VERT_LINE + ''.ljust(quay_width_42fe76c - 2, ' ') + quay_VERT_LINE, quay_bgcolor_0833d5e)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2491a4f)['box'])['write'](0, quay_height_9104aa7, quay_bl_c5be8e0 + ''.ljust(quay_width_42fe76c - 2, quay_div_e80f2a7) + quay_br_cf8c0bd, quay_bgcolor_0833d5e)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2491a4f)['scroll_view_text_buffer'])['process_lines']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2491a4f)['scroll_view_text_buffer'])['draw_lines']()

    @_name_boundary.callable_contract({'self': 'quay_self_6f50571', 'key': 'quay_key_afa6dc9'}, 'handle_key_press')
    def quay_handle_key_press(quay_self_6f50571, quay_key_afa6dc9):
        if quay_key_afa6dc9 == quay_curses.KEY_UP:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_6f50571)['scroll_view_text_buffer'])['scrollcursor'] = max(0, _name_boundary.attributes(_name_boundary.attributes(quay_self_6f50571)['scroll_view_text_buffer'])['scrollcursor'] - 1)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_6f50571)['scroll_view_text_buffer'])['draw_lines']()
            return True
        elif quay_key_afa6dc9 == quay_curses.KEY_DOWN:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_6f50571)['scroll_view_text_buffer'])['scrollcursor'] = min(_name_boundary.attributes(_name_boundary.attributes(quay_self_6f50571)['scroll_view_text_buffer'])['filled_line_count'] - _name_boundary.attributes(_name_boundary.attributes(quay_self_6f50571)['scroll_view_text_buffer'])['height'] + 1, _name_boundary.attributes(_name_boundary.attributes(quay_self_6f50571)['scroll_view_text_buffer'])['scrollcursor'] + 1)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_6f50571)['scroll_view_text_buffer'])['draw_lines']()
            return True
        return False

    @_name_boundary.callable_contract({'self': 'quay_self_51ad70e', 'x': 'quay_x_6aa1ec2', 'y': 'quay_y_808fa2b'}, 'handle_mouse')
    def quay_handle_mouse(quay_self_51ad70e, quay_x_6aa1ec2, quay_y_808fa2b):
        quay_x_6aa1ec2 = quay_x_6aa1ec2 - _name_boundary.attributes(_name_boundary.attributes(quay_self_51ad70e)['box'])['x']
        quay_y_808fa2b = quay_y_808fa2b - _name_boundary.attributes(_name_boundary.attributes(quay_self_51ad70e)['box'])['y']
        quay_handle_33f0a07 = False
        if not _name_boundary.attributes(quay_self_51ad70e)['draw']:
            return quay_handle_33f0a07
        if quay_y_808fa2b == 0:
            quay_handle_33f0a07 = True
            if -1 <= quay_x_6aa1ec2 - _name_boundary.attributes(_name_boundary.attributes(quay_self_51ad70e)['box'])['width'] + 15 <= 1:
                _name_boundary.attributes(quay_self_51ad70e)['draw'] = False
        return quay_handle_33f0a07

@_name_boundary.class_contract('HelpMenu', {'parse_lines': 'quay_parse_lines', 'redraw': 'quay_redraw', 'handle_key_press': 'quay_handle_key_press', 'handle_mouse': 'quay_handle_mouse', 'draw': 'quay_draw', 'scroll_view_text_buffer': 'quay_scroll_view_text_buffer', 'box': 'quay_box'})
class quay_HelpMenu(quay_ScrollView):

    @_name_boundary.callable_contract({'self': 'quay_self_73cfb2b'}, '__init__')
    def __init__(quay_self_73cfb2b):
        super().__init__()
        _name_boundary.attributes(quay_self_73cfb2b)['draw'] = False

    @_name_boundary.callable_contract({'self': 'quay_self_cd0946b'}, 'parse_lines')
    def quay_parse_lines(quay_self_cd0946b):
        quay_attrib_content_b149789 = []
        for quay_item_a27ee32 in _name_boundary.attributes(_name_boundary.attributes(quay_self_cd0946b)['scroll_view_text_buffer'])['lines']:
            if isinstance(quay_item_a27ee32, str):
                quay_attrib_content_b149789.append(_name_boundary.attributes(quay_AttributedString)['ansi_to_attrstr'](quay_item_a27ee32))
            else:
                quay_attrib_content_b149789.append(quay_item_a27ee32)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_cd0946b)['scroll_view_text_buffer'])['lines'] = quay_attrib_content_b149789

    @_name_boundary.callable_contract({'self': 'quay_self_2868100'}, 'redraw')
    def quay_redraw(quay_self_2868100):
        quay_width_5673bd1 = _name_boundary.attributes(_name_boundary.attributes(quay_self_2868100)['box'])['width'] - 10
        quay_height_8e3aba7 = _name_boundary.attributes(_name_boundary.attributes(quay_self_2868100)['box'])['height']
        quay_lc_c2f4277 = '╒'
        quay_rc_968b351 = '╕'
        quay_div_fe9211f = '═'
        quay_bl_550fabf = '╘'
        quay_br_e6d831d = '╛'
        quay_bgcolor_f6fa5b2 = quay_curses.color_pair(1)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2868100)['box'])['write'](0, 0, quay_lc_c2f4277 + ''.ljust(quay_width_5673bd1 - 2, quay_div_fe9211f) + quay_rc_968b351, quay_bgcolor_f6fa5b2)
        for quay_line_67a464c in range(1, quay_height_8e3aba7):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_2868100)['box'])['write'](0, quay_line_67a464c, quay_VERT_LINE + ''.ljust(quay_width_5673bd1 - 2, ' ') + quay_VERT_LINE, quay_bgcolor_f6fa5b2)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2868100)['box'])['write'](0, quay_height_8e3aba7, quay_bl_550fabf + ''.ljust(quay_width_5673bd1 - 2, quay_div_fe9211f) + quay_br_e6d831d, quay_bgcolor_f6fa5b2)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2868100)['scroll_view_text_buffer'])['process_lines']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_2868100)['scroll_view_text_buffer'])['draw_lines']()

    @_name_boundary.callable_contract({'self': 'quay_self_c9a0733', 'key': 'quay_key_cdfb9c3'}, 'handle_key_press')
    def quay_handle_key_press(quay_self_c9a0733, quay_key_cdfb9c3):
        if quay_key_cdfb9c3 == quay_curses.KEY_UP:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_c9a0733)['scroll_view_text_buffer'])['scrollcursor'] = max(0, _name_boundary.attributes(_name_boundary.attributes(quay_self_c9a0733)['scroll_view_text_buffer'])['scrollcursor'] - 1)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_c9a0733)['scroll_view_text_buffer'])['draw_lines']()
            return True
        elif quay_key_cdfb9c3 == quay_curses.KEY_DOWN:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_c9a0733)['scroll_view_text_buffer'])['scrollcursor'] = min(_name_boundary.attributes(_name_boundary.attributes(quay_self_c9a0733)['scroll_view_text_buffer'])['filled_line_count'] - _name_boundary.attributes(_name_boundary.attributes(quay_self_c9a0733)['scroll_view_text_buffer'])['height'] + 1, _name_boundary.attributes(_name_boundary.attributes(quay_self_c9a0733)['scroll_view_text_buffer'])['scrollcursor'] + 1)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_c9a0733)['scroll_view_text_buffer'])['draw_lines']()
            return True
        return False

    @_name_boundary.callable_contract({'self': 'quay_self_62e9530', 'x': 'quay_x_e28c9eb', 'y': 'quay_y_a5ae152'}, 'handle_mouse')
    def quay_handle_mouse(quay_self_62e9530, quay_x_e28c9eb, quay_y_a5ae152):
        quay_x_e28c9eb = quay_x_e28c9eb - _name_boundary.attributes(_name_boundary.attributes(quay_self_62e9530)['box'])['x']
        quay_y_a5ae152 = quay_y_a5ae152 - _name_boundary.attributes(_name_boundary.attributes(quay_self_62e9530)['box'])['y']
        quay_handle_f1c5d50 = False
        if not _name_boundary.attributes(quay_self_62e9530)['draw']:
            return quay_handle_f1c5d50
        if quay_x_e28c9eb < 0 or quay_x_e28c9eb > _name_boundary.attributes(_name_boundary.attributes(quay_self_62e9530)['box'])['width'] or quay_y_a5ae152 < 0 or (quay_y_a5ae152 > _name_boundary.attributes(_name_boundary.attributes(quay_self_62e9530)['box'])['height']):
            _name_boundary.attributes(quay_self_62e9530)['draw'] = False
            quay_handle_f1c5d50 = True
        if quay_y_a5ae152 == 0:
            quay_handle_f1c5d50 = True
            if -1 <= quay_x_e28c9eb - _name_boundary.attributes(_name_boundary.attributes(quay_self_62e9530)['box'])['width'] + 15 <= 1:
                _name_boundary.attributes(quay_self_62e9530)['draw'] = False
        return quay_handle_f1c5d50

@_name_boundary.class_contract('LoaderStatusView', {'redraw': 'quay_redraw', 'draw': 'quay_draw', 'status_string': 'quay_status_string', 'box': 'quay_box'})
class quay_LoaderStatusView(quay_View):

    @_name_boundary.callable_contract({'self': 'quay_self_c19acee'}, '__init__')
    def __init__(quay_self_c19acee):
        super().__init__()
        _name_boundary.attributes(quay_self_c19acee)['draw'] = False
        _name_boundary.attributes(quay_self_c19acee)['status_string'] = 'Loading...'

    @_name_boundary.callable_contract({'self': 'quay_self_16f05e9'}, 'redraw')
    def quay_redraw(quay_self_16f05e9):
        if not _name_boundary.attributes(quay_self_16f05e9)['draw']:
            return
        quay_box_width_059642f = max(40, len(_name_boundary.attributes(quay_self_16f05e9)['status_string']) + 10)
        quay_start_x_f9d17ef = quay_ceil(_name_boundary.attributes(_name_boundary.attributes(quay_self_16f05e9)['box'])['width'] / 2 - quay_box_width_059642f / 2)
        quay_height_43ac7a1 = 4
        quay_start_y_99e92b3 = quay_ceil(_name_boundary.attributes(_name_boundary.attributes(quay_self_16f05e9)['box'])['height'] / 2 - quay_height_43ac7a1 / 2)
        for quay_i_8dd55eb in range(quay_start_y_99e92b3, quay_start_y_99e92b3 + quay_height_43ac7a1 + 1):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_16f05e9)['box'])['write'](quay_start_x_f9d17ef, quay_i_8dd55eb, ' ' * quay_box_width_059642f, quay_curses.A_STANDOUT)
        quay_i_8dd55eb = 0
        for quay_line_d311705 in _name_boundary.attributes(quay_self_16f05e9)['status_string'].split('\n'):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_16f05e9)['box'])['write'](quay_start_x_f9d17ef + 1, quay_start_y_99e92b3 + 1 + quay_i_8dd55eb, quay_line_d311705, quay_curses.A_STANDOUT)
            quay_i_8dd55eb += 1

@_name_boundary.class_contract('UserInputPrompt', {'redraw': 'quay_redraw', 'handle_mouse': 'quay_handle_mouse', 'draw': 'quay_draw', 'prompt_string': 'quay_prompt_string', 'user_input_is_string': 'quay_user_input_is_string', 'active_render_subbox': 'quay_active_render_subbox', 'response': 'quay_response', 'box': 'quay_box'})
class quay_UserInputPrompt(quay_View):

    @_name_boundary.callable_contract({'self': 'quay_self_f454251'}, '__init__')
    def __init__(quay_self_f454251):
        super().__init__()
        _name_boundary.attributes(quay_self_f454251)['draw'] = False
        _name_boundary.attributes(quay_self_f454251)['prompt_string'] = ''
        _name_boundary.attributes(quay_self_f454251)['user_input_is_string'] = False
        _name_boundary.attributes(quay_self_f454251)['active_render_subbox'] = None
        _name_boundary.attributes(quay_self_f454251)['response'] = None

    @_name_boundary.callable_contract({'self': 'quay_self_f4d0e09'}, 'redraw')
    def quay_redraw(quay_self_f4d0e09):
        if not _name_boundary.attributes(quay_self_f4d0e09)['draw']:
            return
        quay_box_width_2b045b0 = max(40, len(_name_boundary.attributes(quay_self_f4d0e09)['prompt_string']) + 10)
        quay_start_x_f8f6e97 = quay_ceil(_name_boundary.attributes(_name_boundary.attributes(quay_self_f4d0e09)['box'])['width'] / 2 - quay_box_width_2b045b0 / 2)
        quay_height_4aa915c = 4
        quay_start_y_e43b969 = quay_ceil(_name_boundary.attributes(_name_boundary.attributes(quay_self_f4d0e09)['box'])['height'] / 2 - quay_height_4aa915c / 2)
        _name_boundary.attributes(quay_self_f4d0e09)['active_render_subbox'] = quay_Box(None, quay_start_x_f8f6e97, quay_start_y_e43b969, quay_box_width_2b045b0, quay_height_4aa915c)
        for quay_i_3979629 in range(quay_start_y_e43b969, quay_start_y_e43b969 + quay_height_4aa915c + 1):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_f4d0e09)['box'])['write'](quay_start_x_f8f6e97, quay_i_3979629, ' ' * quay_box_width_2b045b0, quay_curses.A_STANDOUT)
        quay_xof_fb76570 = 2
        for quay_msg_029c6ad in ['YES', 'NO', 'CANCEL']:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_f4d0e09)['box'])['write'](quay_xof_fb76570, quay_height_4aa915c, quay_msg_029c6ad, quay_curses.A_STANDOUT)
            quay_xof_fb76570 += len(quay_msg_029c6ad) + 2

    @_name_boundary.callable_contract({'self': 'quay_self_227d9b8', 'x': 'quay_x_99ad691', 'y': 'quay_y_516317b'}, 'handle_mouse')
    def quay_handle_mouse(quay_self_227d9b8, quay_x_99ad691, quay_y_516317b):
        if not _name_boundary.attributes(quay_self_227d9b8)['draw']:
            return False
        if _name_boundary.attributes(_name_boundary.attributes(quay_self_227d9b8)['active_render_subbox'])['is_click_inbounds'](quay_x_99ad691, quay_y_516317b) and quay_y_516317b - _name_boundary.attributes(_name_boundary.attributes(quay_self_227d9b8)['active_render_subbox'])['y'] == 4:
            quay_xof_43a0268 = 2
            quay_xp_acd9ad3 = quay_x_99ad691 - _name_boundary.attributes(_name_boundary.attributes(quay_self_227d9b8)['active_render_subbox'])['x']
            quay_height_f180161 = 4
            for quay_msg_598b253 in ['YES', 'NO', 'CANCEL']:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_227d9b8)['box'])['write'](quay_xof_43a0268, quay_height_f180161, quay_msg_598b253, quay_curses.A_STANDOUT)
                quay_wid_829cb08 = len(quay_msg_598b253)
                if quay_xp_acd9ad3 in range(quay_xof_43a0268, quay_xof_43a0268 + quay_wid_829cb08 + 1):
                    if quay_msg_598b253 == 'YES':
                        _name_boundary.attributes(quay_self_227d9b8)['response'] = 'y'
                    elif quay_msg_598b253 == 'NO':
                        _name_boundary.attributes(quay_self_227d9b8)['response'] = 'n'
                    else:
                        _name_boundary.attributes(quay_self_227d9b8)['response'] = 'c'
                    return True
                quay_xof_43a0268 += len(quay_msg_598b253) + 2
        return False

@_name_boundary.class_contract('MenuOverlayRenderingView', {'redraw': 'quay_redraw', 'handle_mouse': 'quay_handle_mouse', 'draw': 'quay_draw', 'active_render_menu': 'quay_active_render_menu', 'active_menu_start_x': 'quay_active_menu_start_x', 'active_render_subbox': 'quay_active_render_subbox', 'box': 'quay_box'})
class quay_MenuOverlayRenderingView(quay_View):

    @_name_boundary.callable_contract({'self': 'quay_self_5c48d74'}, '__init__')
    def __init__(quay_self_5c48d74):
        super().__init__()
        _name_boundary.attributes(quay_self_5c48d74)['draw'] = False
        _name_boundary.attributes(quay_self_5c48d74)['active_render_menu'] = None
        _name_boundary.attributes(quay_self_5c48d74)['active_menu_start_x'] = 0
        _name_boundary.attributes(quay_self_5c48d74)['active_render_subbox'] = None

    @_name_boundary.callable_contract({'self': 'quay_self_3e7f016'}, 'redraw')
    def quay_redraw(quay_self_3e7f016):
        if not _name_boundary.attributes(quay_self_3e7f016)['draw'] or not _name_boundary.attributes(quay_self_3e7f016)['active_render_menu']:
            return
        if len(_name_boundary.attributes(_name_boundary.attributes(quay_self_3e7f016)['active_render_menu'])['menu_items']) == 0:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_3e7f016)['active_render_menu'])['function']()
            _name_boundary.attributes(quay_self_3e7f016)['draw'] = False
        quay_start_a923806 = (_name_boundary.attributes(quay_self_3e7f016)['active_menu_start_x'] + 1, 1)
        quay_width_38d4191 = 30
        quay_height_d0e1607 = len(_name_boundary.attributes(_name_boundary.attributes(quay_self_3e7f016)['active_render_menu'])['menu_items']) + 2
        _name_boundary.attributes(quay_self_3e7f016)['active_render_subbox'] = quay_Box(None, quay_start_a923806[0], quay_start_a923806[1], quay_width_38d4191, quay_height_d0e1607)
        for quay_line_5562ef0 in range(quay_start_a923806[1], quay_start_a923806[1] + quay_height_d0e1607):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_3e7f016)['box'])['write'](quay_start_a923806[0], quay_line_5562ef0, ' ' * quay_width_38d4191, quay_curses.A_STANDOUT)
        for quay_linen_b680b90, quay_item_e39baae in enumerate([quay_i_14efc91[0] for quay_i_14efc91 in _name_boundary.attributes(_name_boundary.attributes(quay_self_3e7f016)['active_render_menu'])['menu_items']]):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_3e7f016)['box'])['write'](quay_start_a923806[0] + 1, quay_start_a923806[1] + 1 + quay_linen_b680b90, f'{quay_item_e39baae}', quay_curses.A_STANDOUT)

    @_name_boundary.callable_contract({'self': 'quay_self_bb48ade', 'x': 'quay_x_10971b4', 'y': 'quay_y_17423d7'}, 'handle_mouse')
    def quay_handle_mouse(quay_self_bb48ade, quay_x_10971b4, quay_y_17423d7):
        if not _name_boundary.attributes(quay_self_bb48ade)['draw'] or not _name_boundary.attributes(quay_self_bb48ade)['active_render_menu']:
            return False
        if _name_boundary.attributes(_name_boundary.attributes(quay_self_bb48ade)['active_render_subbox'])['is_click_inbounds'](quay_x_10971b4, quay_y_17423d7):
            quay_y_17423d7 = quay_y_17423d7 - _name_boundary.attributes(_name_boundary.attributes(quay_self_bb48ade)['active_render_subbox'])['y'] - 1
            if quay_y_17423d7 < 0:
                return False
            if quay_y_17423d7 > len(_name_boundary.attributes(_name_boundary.attributes(quay_self_bb48ade)['active_render_menu'])['menu_items']):
                raise quay_DestroyTitleMenuException
            if quay_y_17423d7 == len(_name_boundary.attributes(_name_boundary.attributes(quay_self_bb48ade)['active_render_menu'])['menu_items']):
                return False
            quay_item_tup_1e8d8e4 = _name_boundary.attributes(_name_boundary.attributes(quay_self_bb48ade)['active_render_menu'])['menu_items'][quay_y_17423d7]
            quay_item_tup_1e8d8e4[1]()
            return True
        raise quay_DestroyTitleMenuException

@_name_boundary.class_contract('FileSystemBrowserOverlayView', {'redraw': 'quay_redraw', 'handle_key_press': 'quay_handle_key_press', 'draw': 'quay_draw', 'current_dir_path': 'quay_current_dir_path', 'select_file': 'quay_select_file', 'callback': 'quay_callback', 'selected_index': 'quay_selected_index', 'scroll_view_text_buffer': 'quay_scroll_view_text_buffer', 'box': 'quay_box'})
class quay_FileSystemBrowserOverlayView(quay_ScrollView):

    @_name_boundary.callable_contract({'self': 'quay_self_d645d5f'}, '__init__')
    def __init__(quay_self_d645d5f):
        super().__init__()
        _name_boundary.attributes(quay_self_d645d5f)['draw'] = False
        _name_boundary.attributes(quay_self_d645d5f)['current_dir_path'] = quay_os.getcwd()
        _name_boundary.attributes(quay_self_d645d5f)['select_file'] = True
        _name_boundary.attributes(quay_self_d645d5f)['callback'] = None
        _name_boundary.attributes(quay_self_d645d5f)['selected_index'] = 0

    @_name_boundary.callable_contract({'self': 'quay_self_92ee64b'}, 'redraw')
    def quay_redraw(quay_self_92ee64b):
        quay_start_x_9595d73 = 3
        quay_width_fc46236 = _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['box'])['width'] - 2 * quay_start_x_9595d73
        quay_start_y_9bd1a80 = quay_start_x_9595d73
        quay_height_cc0fd4f = _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['box'])['height'] - 2 * quay_start_y_9bd1a80
        quay_lc_bfd2a19 = '╒'
        quay_rc_4ce14d0 = '╕'
        quay_div_785fc5f = '═'
        quay_bl_4e78153 = '╘'
        quay_br_321bfc8 = '╛'
        quay_lj_c63ec28 = '╞'
        quay_rj_c7de547 = '╡'
        quay_bgcolor_6d61b0a = quay_curses.A_NORMAL
        _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['box'])['write'](quay_start_x_9595d73, quay_start_y_9bd1a80, quay_lc_bfd2a19 + ''.ljust(quay_width_fc46236 - 2, quay_div_785fc5f) + quay_rc_4ce14d0, quay_bgcolor_6d61b0a)
        for quay_line_0f571c6 in range(quay_start_y_9bd1a80 + 1, quay_start_y_9bd1a80 + quay_height_cc0fd4f + 1):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['box'])['write'](quay_start_x_9595d73, quay_line_0f571c6, quay_VERT_LINE + ''.ljust(quay_width_fc46236 - 2, ' ') + quay_VERT_LINE, quay_bgcolor_6d61b0a)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['box'])['write'](quay_start_x_9595d73, quay_start_y_9bd1a80 + quay_height_cc0fd4f, quay_bl_4e78153 + ''.ljust(quay_width_fc46236 - 2, quay_div_785fc5f) + quay_br_321bfc8, quay_bgcolor_6d61b0a)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['box'])['write'](quay_start_x_9595d73, quay_start_y_9bd1a80 + quay_height_cc0fd4f - 2, quay_lj_c63ec28 + ''.ljust(quay_width_fc46236 - 2, quay_div_785fc5f) + quay_rj_c7de547, quay_bgcolor_6d61b0a)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['box'])['write'](quay_start_x_9595d73 + quay_width_fc46236 - 10, quay_start_y_9bd1a80 + quay_height_cc0fd4f - 1, ' SELECT ', quay_curses.A_STANDOUT)
        quay_lines_240cf41 = ['..'] + [quay_i_9e51b3e for quay_i_9e51b3e in quay_os.listdir(_name_boundary.attributes(quay_self_92ee64b)['current_dir_path'])]
        quay_nlines_a452c99 = []
        for quay_item_8fd0d62 in quay_lines_240cf41:
            if _name_boundary.attributes(quay_os)['path'].isdir(quay_item_8fd0d62):
                quay_nlines_a452c99.append(f'{quay_item_8fd0d62}/')
            else:
                quay_nlines_a452c99.append(quay_item_8fd0d62)
        for quay_index_680331c, quay_name_9731af9 in enumerate(quay_nlines_a452c99):
            if _name_boundary.attributes(quay_self_92ee64b)['selected_index'] == quay_index_680331c:
                quay_name_9731af9 = quay_AttributedString(quay_name_9731af9)
                _name_boundary.attributes(quay_name_9731af9)['set_attr'](0, len(_name_boundary.attributes(quay_name_9731af9)['string']) - 1, _name_boundary.attributes(quay_Attribute)['HIGHLIGHTED'])
                _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['lines'].append(quay_name_9731af9)
            else:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['lines'].append(quay_name_9731af9)
        quay_scroll_view_height_ecd24d3 = _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['height']
        if _name_boundary.attributes(quay_self_92ee64b)['selected_index'] - quay_scroll_view_height_ecd24d3 + 4 > _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['scrollcursor']:
            while _name_boundary.attributes(quay_self_92ee64b)['selected_index'] - quay_scroll_view_height_ecd24d3 + 4 > _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['scrollcursor']:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['scrollcursor'] += 1
        elif _name_boundary.attributes(quay_self_92ee64b)['selected_index'] < _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['scrollcursor'] + 2 and _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['scrollcursor'] > 0:
            while _name_boundary.attributes(quay_self_92ee64b)['selected_index'] < _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['scrollcursor'] + 2 and _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['scrollcursor'] > 0:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['scrollcursor'] -= 1
        _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['process_lines']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_92ee64b)['scroll_view_text_buffer'])['draw_lines']()

    @_name_boundary.callable_contract({'self': 'quay_self_8476b4b', 'key': 'quay_key_6112b81'}, 'handle_key_press')
    def quay_handle_key_press(quay_self_8476b4b, quay_key_6112b81):
        if not _name_boundary.attributes(quay_self_8476b4b)['draw']:
            return False
        if quay_key_6112b81 == quay_curses.KEY_UP:
            quay_index_dcf355b = _name_boundary.attributes(quay_self_8476b4b)['selected_index']
            if quay_index_dcf355b - 1 in range(0, len(_name_boundary.attributes(_name_boundary.attributes(quay_self_8476b4b)['scroll_view_text_buffer'])['lines'])):
                _name_boundary.attributes(quay_self_8476b4b)['selected_index'] -= 1
            return True
        elif quay_key_6112b81 == quay_curses.KEY_DOWN:
            quay_index_dcf355b = _name_boundary.attributes(quay_self_8476b4b)['selected_index']
            if quay_index_dcf355b + 1 in range(0, len(_name_boundary.attributes(_name_boundary.attributes(quay_self_8476b4b)['scroll_view_text_buffer'])['lines'])):
                _name_boundary.attributes(quay_self_8476b4b)['selected_index'] += 1
            return True
        return False

@_name_boundary.class_contract('KToolMachOLoader', {'SUPPORTS_256': 'quay_SUPPORTS_256', 'SUPPORTS_COLOR': 'quay_SUPPORTS_COLOR', 'HARD_FAIL': 'quay_HARD_FAIL', 'CUR_SL': 'quay_CUR_SL', 'SL_CNT': 'quay_SL_CNT', 'parent_count': 'quay_parent_count', 'contents_for_file': 'quay_contents_for_file', 'contents_for_image': 'quay_contents_for_image', 'slice_item': 'quay_slice_item', 'segments': 'quay_segments', '_file': 'quay__file', 'linked': 'quay_linked', 'codesign': 'quay_codesign', 'load_cmds': 'quay_load_cmds', 'symtab': 'quay_symtab', 'vm_map': 'quay_vm_map', 'objc_items': 'quay_objc_items', 'swift_items': 'quay_swift_items', 'swift_types': 'quay_swift_types', 'imports': 'quay_imports', 'exports': 'quay_exports', 'get_header_item': 'quay_get_header_item', 'get_header_text': 'quay_get_header_text', 'objc_headers': 'quay_objc_headers'})
class quay_ImageQuayMachOLoader:
    quay_SUPPORTS_256 = False
    quay_SUPPORTS_COLOR = True
    quay_HARD_FAIL = False
    quay_CUR_SL = 0
    quay_SL_CNT = 0

    @staticmethod
    @_name_boundary.callable_contract({'item': 'quay_item_b90e0db'}, 'parent_count')
    def quay_parent_count(quay_item_b90e0db):
        quay_count_d3a921d = 0
        quay_item_b90e0db = quay_item_b90e0db
        while _name_boundary.attributes(quay_item_b90e0db)['parent'] is not None:
            quay_count_d3a921d += 1
            quay_item_b90e0db = _name_boundary.attributes(quay_item_b90e0db)['parent']
        return quay_count_d3a921d

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_44b46a4', 'fd': 'quay_fd_295e3eb', 'callback': 'quay_callback_6fa228e', 'mmap': 'quay_mmap_6df1f6e'}, 'contents_for_file')
    def quay_contents_for_file(quay_cls_44b46a4, quay_fd_295e3eb, quay_callback_6fa228e, quay_mmap_6df1f6e=True):
        quay_machofile_60e7f61 = quay_MachOFile(quay_fd_295e3eb, use_mmaped_io=quay_mmap_6df1f6e)
        quay_items_88850cd = []
        _name_boundary.attributes(quay_ImageQuayMachOLoader)['SL_CNT'] = len(_name_boundary.attributes(quay_machofile_60e7f61)['slices'])
        for quay_macho_slice_0b7856c in _name_boundary.attributes(quay_machofile_60e7f61)['slices']:
            _name_boundary.attributes(quay_ImageQuayMachOLoader)['CUR_SL'] += 1
            try:
                quay_items_88850cd.append(_name_boundary.attributes(quay_cls_44b46a4)['slice_item'](quay_macho_slice_0b7856c, quay_callback_6fa228e))
            except Exception as quay_ex_24a7723:
                raise quay_ex_24a7723
        return quay_items_88850cd

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_e54a5e8', 'image': 'quay_image_953362e', 'callback': 'quay_callback_2687c43'}, 'contents_for_image')
    def quay_contents_for_image(quay_cls_e54a5e8, quay_image_953362e, quay_callback_2687c43):
        quay_items_b2860f9 = []
        quay_items_b2860f9.append(_name_boundary.attributes(quay_cls_e54a5e8)['slice_item'](None, quay_callback_2687c43, quay_image_953362e))
        return quay_items_b2860f9

    @staticmethod
    @_name_boundary.callable_contract({'macho_slice': 'quay_macho_slice_b3a6f7d', 'callback': 'quay_callback_9bac2ab', 'loaded_image': 'quay_loaded_image_75cbe25'}, 'slice_item')
    def quay_slice_item(quay_macho_slice_b3a6f7d, quay_callback_9bac2ab, quay_loaded_image_75cbe25=None):
        if not quay_loaded_image_75cbe25:
            quay_loaded_image_75cbe25 = _name_boundary.attributes(quay_MachOImageLoader)['load'](quay_macho_slice_b3a6f7d)
        if _name_boundary.has_attribute(quay_macho_slice_b3a6f7d, 'type'):
            quay_slice_nick_53db918 = f"{_name_boundary.attributes(_name_boundary.attributes(quay_macho_slice_b3a6f7d)['type'])['name']}:{_name_boundary.attributes(_name_boundary.attributes(quay_macho_slice_b3a6f7d)['subtype'])['name']}" + ' Slice'
        else:
            quay_slice_nick_53db918 = 'Thin MachO'
        quay_callback_9bac2ab(f"Slice {_name_boundary.attributes(quay_ImageQuayMachOLoader)['CUR_SL']}/{_name_boundary.attributes(quay_ImageQuayMachOLoader)['SL_CNT']}\nLoading MachO Image")
        quay_slice_item_70c540e = quay_SidebarMenuItem(f'{quay_slice_nick_53db918}', None, None)
        _name_boundary.attributes(quay_slice_item_70c540e)['content'] = _name_boundary.attributes(_name_boundary.attributes(quay_ImageQuayMachOLoader)['_file'](quay_loaded_image_75cbe25, quay_slice_item_70c540e, quay_callback_9bac2ab))['content']
        quay_items_81ff7ac = [_name_boundary.attributes(quay_ImageQuayMachOLoader)['load_cmds'], _name_boundary.attributes(quay_ImageQuayMachOLoader)['segments'], _name_boundary.attributes(quay_ImageQuayMachOLoader)['codesign'], _name_boundary.attributes(quay_ImageQuayMachOLoader)['linked'], _name_boundary.attributes(quay_ImageQuayMachOLoader)['imports'], _name_boundary.attributes(quay_ImageQuayMachOLoader)['exports'], _name_boundary.attributes(quay_ImageQuayMachOLoader)['symtab']]
        for quay_item_2a61787 in quay_items_81ff7ac:
            try:
                _name_boundary.attributes(quay_slice_item_70c540e)['children'].append(quay_item_2a61787(quay_loaded_image_75cbe25, quay_slice_item_70c540e, quay_callback_9bac2ab))
            except Exception as quay_ex_35e022e:
                if _name_boundary.attributes(quay_ImageQuayMachOLoader)['HARD_FAIL']:
                    raise quay_ex_35e022e
                else:
                    pass
        try:
            _name_boundary.attributes(quay_slice_item_70c540e)['children'] += _name_boundary.attributes(quay_ImageQuayMachOLoader)['objc_items'](quay_loaded_image_75cbe25, quay_slice_item_70c540e, quay_callback_9bac2ab)
        except Exception as quay_ex_35e022e:
            if _name_boundary.attributes(quay_ImageQuayMachOLoader)['HARD_FAIL']:
                raise quay_ex_35e022e
            else:
                pass
        try:
            _name_boundary.attributes(quay_slice_item_70c540e)['children'] += _name_boundary.attributes(quay_ImageQuayMachOLoader)['swift_items'](quay_loaded_image_75cbe25, quay_slice_item_70c540e, quay_callback_9bac2ab)
        except Exception as quay_ex_35e022e:
            if _name_boundary.attributes(quay_ImageQuayMachOLoader)['HARD_FAIL']:
                pass
            else:
                pass
        _name_boundary.attributes(quay_slice_item_70c540e)['show_children'] = True
        return quay_slice_item_70c540e

    @staticmethod
    @_name_boundary.callable_contract({'lib': 'quay_lib_5dc6870', 'parent': 'quay_parent_4989ae1', 'callback': 'quay_callback_1e215c7'}, 'segments')
    def quay_segments(quay_lib_5dc6870, quay_parent_4989ae1=None, quay_callback_1e215c7=None):
        quay_callback_1e215c7(f"Slice {_name_boundary.attributes(quay_ImageQuayMachOLoader)['CUR_SL']}/{_name_boundary.attributes(quay_ImageQuayMachOLoader)['SL_CNT']}\nLoading Segments & Generating Hexdumps")
        quay_smmci_9c40d30 = quay_MainMenuContentItem()
        quay_ssmi_b0f4269 = quay_SidebarMenuItem('Segments', quay_smmci_9c40d30, quay_parent_4989ae1)
        quay_table_aafb864 = quay_Table()
        _name_boundary.attributes(quay_table_aafb864)['titles'] = ['Segment Name', 'VM Address', 'Size', 'File Address']
        for quay_segname_57406c7, quay_segm_7ec7fbd in _name_boundary.attributes(_name_boundary.attributes(quay_lib_5dc6870)['segments'])['items']():
            _name_boundary.attributes(quay_table_aafb864)['rows'].append([quay_segname_57406c7, hex(_name_boundary.attributes(quay_segm_7ec7fbd)['vm_address']), hex(_name_boundary.attributes(quay_segm_7ec7fbd)['size']), hex(_name_boundary.attributes(quay_segm_7ec7fbd)['file_address'])])
            quay_segtable_0ff911e = quay_Table()
            _name_boundary.attributes(quay_segtable_0ff911e)['titles'] = ['Section Name', 'VM Address', 'Size', 'File Address']
            quay_mmci_befeeba = quay_MainMenuContentItem()
            quay_item_2a30164 = quay_SidebarMenuItem(f"{quay_segname_57406c7} [{len(_name_boundary.attributes(_name_boundary.attributes(quay_segm_7ec7fbd)['sections'])['items']())} Sections]", quay_mmci_befeeba, quay_ssmi_b0f4269)
            for quay_secname_aefbb22, quay_sect_57c7465 in _name_boundary.attributes(_name_boundary.attributes(quay_segm_7ec7fbd)['sections'])['items']():
                _name_boundary.attributes(quay_segtable_0ff911e)['rows'].append([quay_secname_aefbb22, hex(_name_boundary.attributes(quay_sect_57c7465)['vm_address']), hex(_name_boundary.attributes(quay_sect_57c7465)['size']), hex(_name_boundary.attributes(quay_sect_57c7465)['file_address'])])
                quay_hextab_d3e8d3b = quay_HexDumpTable()
                _name_boundary.attributes(quay_hextab_d3e8d3b)['hex'] = _name_boundary.attributes(_name_boundary.attributes(quay_lib_5dc6870)['slice'])['read_bytearray'](_name_boundary.attributes(quay_sect_57c7465)['file_address'], _name_boundary.attributes(quay_sect_57c7465)['size'])
                quay_itm_1f7132a = quay_MainMenuContentItem()
                _name_boundary.attributes(quay_itm_1f7132a)['lines'].append(quay_hextab_d3e8d3b)
                _name_boundary.attributes(quay_item_2a30164)['children'].append(quay_SidebarMenuItem(quay_secname_aefbb22, quay_itm_1f7132a, quay_item_2a30164))
            _name_boundary.attributes(quay_ssmi_b0f4269)['children'].append(quay_item_2a30164)
            if len(_name_boundary.attributes(_name_boundary.attributes(quay_segm_7ec7fbd)['sections'])['items']()) == 0:
                if 'PAGEZERO' not in quay_segname_57406c7:
                    quay_hextab_d3e8d3b = quay_HexDumpTable()
                    _name_boundary.attributes(quay_hextab_d3e8d3b)['hex'] = _name_boundary.attributes(_name_boundary.attributes(quay_lib_5dc6870)['slice'])['read_bytearray'](_name_boundary.attributes(quay_segm_7ec7fbd)['file_address'], _name_boundary.attributes(quay_segm_7ec7fbd)['size'])
                    _name_boundary.attributes(quay_mmci_befeeba)['lines'].append(quay_hextab_d3e8d3b)
            else:
                _name_boundary.attributes(quay_mmci_befeeba)['lines'].append(quay_segtable_0ff911e)
        _name_boundary.attributes(quay_smmci_9c40d30)['lines'].append(quay_table_aafb864)
        _name_boundary.attributes(quay_ssmi_b0f4269)['parse_mmc']()
        return quay_ssmi_b0f4269

    @staticmethod
    @_name_boundary.callable_contract({'lib': 'quay_lib_ff5090c', 'parent': 'quay_parent_bbc55e0', 'callback': 'quay_callback_a13787b'}, '_file')
    def quay__file(quay_lib_ff5090c, quay_parent_bbc55e0=None, quay_callback_a13787b=None):
        quay_file_content_item_23eb0b0 = quay_MainMenuContentItem()
        _name_boundary.attributes(quay_file_content_item_23eb0b0)['lines'].append(f"Install Name: §35m{_name_boundary.attributes(quay_lib_ff5090c)['install_name']}§39m")
        _name_boundary.attributes(quay_file_content_item_23eb0b0)['lines'].append(f"Filetype: §35m{_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_lib_ff5090c)['macho_header'])['filetype'])['name']}§39m")
        _name_boundary.attributes(quay_file_content_item_23eb0b0)['lines'].append(f"Flags: §35m{'§39m, §35m'.join([_name_boundary.attributes(quay_i_323a698)['name'] for quay_i_323a698 in _name_boundary.attributes(_name_boundary.attributes(quay_lib_ff5090c)['macho_header'])['flags']])}§39m")
        if _name_boundary.attributes(quay_lib_ff5090c)['uuid']:
            _name_boundary.attributes(quay_file_content_item_23eb0b0)['lines'].append(f"UUID: §35m{_name_boundary.attributes(_name_boundary.attributes(quay_lib_ff5090c)['uuid'])['hex']().upper()}§39m")
        _name_boundary.attributes(quay_file_content_item_23eb0b0)['lines'].append(f"Platform: §35m{_name_boundary.attributes(_name_boundary.attributes(quay_lib_ff5090c)['platform'])['name']}§39m")
        _name_boundary.attributes(quay_file_content_item_23eb0b0)['lines'].append(f"Minimum OS: §35m{_name_boundary.attributes(_name_boundary.attributes(quay_lib_ff5090c)['minos'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_lib_ff5090c)['minos'])['y']}.{_name_boundary.attributes(quay_lib_ff5090c)['minos'].z}§39m")
        _name_boundary.attributes(quay_file_content_item_23eb0b0)['lines'].append(f"SDK Version: §35m{_name_boundary.attributes(_name_boundary.attributes(quay_lib_ff5090c)['sdk_version'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_lib_ff5090c)['sdk_version'])['y']}.{_name_boundary.attributes(quay_lib_ff5090c)['sdk_version'].z}§39m")
        _name_boundary.attributes(quay_file_content_item_23eb0b0)['lines'].append('')
        _name_boundary.attributes(quay_file_content_item_23eb0b0)['lines'].append(f"macho_header: {str(_name_boundary.attributes(_name_boundary.attributes(quay_lib_ff5090c)['macho_header'])['dyld_header'])}")
        quay_menuitem_0809962 = quay_SidebarMenuItem('File Info', quay_file_content_item_23eb0b0, quay_parent_bbc55e0)
        _name_boundary.attributes(quay_menuitem_0809962)['parse_mmc']()
        return quay_menuitem_0809962

    @staticmethod
    @_name_boundary.callable_contract({'lib': 'quay_lib_61e0db0', 'parent': 'quay_parent_61ab613', 'callback': 'quay_callback_bb836d0'}, 'linked')
    def quay_linked(quay_lib_61e0db0, quay_parent_61ab613=None, quay_callback_bb836d0=None):
        quay_callback_bb836d0(f"Slice {_name_boundary.attributes(quay_ImageQuayMachOLoader)['CUR_SL']}/{_name_boundary.attributes(quay_ImageQuayMachOLoader)['SL_CNT']}\nLoading Linked Libs")
        quay_linked_libs_item_47f6695 = quay_MainMenuContentItem()
        for quay_exlib_6dfd524 in _name_boundary.attributes(quay_lib_61e0db0)['linked_images']:
            _name_boundary.attributes(quay_linked_libs_item_47f6695)['lines'].append('§31m(Weak)§39m ' + _name_boundary.attributes(quay_exlib_6dfd524)['install_name'] if _name_boundary.attributes(quay_exlib_6dfd524)['weak'] else '' + _name_boundary.attributes(quay_exlib_6dfd524)['install_name'])
        quay_menuitem_b9cd8f2 = quay_SidebarMenuItem('Linked Libraries', quay_linked_libs_item_47f6695, quay_parent_61ab613)
        _name_boundary.attributes(quay_menuitem_b9cd8f2)['parse_mmc']()
        return quay_menuitem_b9cd8f2

    @staticmethod
    @_name_boundary.callable_contract({'lib': 'quay_lib_d6112af', 'parent': 'quay_parent_5e5bebd', 'callback': 'quay_callback_5cfec6c'}, 'codesign')
    def quay_codesign(quay_lib_d6112af, quay_parent_5e5bebd=None, quay_callback_5cfec6c=None):
        quay_callback_5cfec6c(f'Codesign Info')
        quay_cs_58cba14 = quay_MainMenuContentItem()
        quay_image_beb257a = quay_lib_d6112af
        quay_lines_6d8f598 = []
        quay_lines_6d8f598 += _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_image_beb257a)['codesign_info'])['superblob'])['render_indented']().split('\n')
        quay_lines_6d8f598.append('')
        for quay_slot_9b953e2 in _name_boundary.attributes(_name_boundary.attributes(quay_image_beb257a)['codesign_info'])['slots']:
            quay_lines_6d8f598 += _name_boundary.attributes(quay_slot_9b953e2)['render_indented']().split('\n')
            quay_lines_6d8f598.append('')
        _name_boundary.attributes(quay_cs_58cba14)['lines'] = quay_lines_6d8f598
        quay_smi_c7d9780 = quay_SidebarMenuItem('Codesign Info', quay_cs_58cba14, quay_parent_5e5bebd)
        quay_ent_mmci_31248b9 = quay_MainMenuContentItem()
        _name_boundary.attributes(quay_ent_mmci_31248b9)['lines'].append(_name_boundary.attributes(_name_boundary.attributes(quay_image_beb257a)['codesign_info'])['entitlements'])
        quay_ent_smi_b2a23f2 = quay_SidebarMenuItem('Entitlements', quay_ent_mmci_31248b9, quay_smi_c7d9780)
        _name_boundary.attributes(quay_ent_smi_b2a23f2)['parse_mmc']()
        _name_boundary.attributes(quay_smi_c7d9780)['children'].append(quay_ent_smi_b2a23f2)
        quay_req_mmci_1a175a5 = quay_MainMenuContentItem()
        quay_hexdump_008294a = quay_HexDumpTable()
        _name_boundary.attributes(quay_hexdump_008294a)['hex'] = bytearray(_name_boundary.attributes(_name_boundary.attributes(quay_image_beb257a)['codesign_info'])['req_dat'])
        _name_boundary.attributes(quay_req_mmci_1a175a5)['lines'].append(quay_hexdump_008294a)
        quay_req_smi_3f85d2b = quay_SidebarMenuItem('Requirements', quay_req_mmci_1a175a5, quay_smi_c7d9780)
        _name_boundary.attributes(quay_smi_c7d9780)['children'].append(quay_req_smi_3f85d2b)
        _name_boundary.attributes(quay_smi_c7d9780)['parse_mmc']()
        return quay_smi_c7d9780

    @staticmethod
    @_name_boundary.callable_contract({'lib': 'quay_lib_da5f1c1', 'parent': 'quay_parent_5c146fb', 'callback': 'quay_callback_dbd4946'}, 'load_cmds')
    def quay_load_cmds(quay_lib_da5f1c1, quay_parent_5c146fb=None, quay_callback_dbd4946=None):
        quay_callback_dbd4946(f"Slice {_name_boundary.attributes(quay_ImageQuayMachOLoader)['CUR_SL']}/{_name_boundary.attributes(quay_ImageQuayMachOLoader)['SL_CNT']}\nProcessing Load Commands")
        quay_load_cmds_65bc7b5 = quay_MainMenuContentItem()
        quay_lines_712e122 = [f"Load Command Count: {len(_name_boundary.attributes(_name_boundary.attributes(quay_lib_da5f1c1)['macho_header'])['load_commands'])}"]
        _name_boundary.attributes(quay_load_cmds_65bc7b5)['lines'] = quay_lines_712e122
        quay_menuitem_cc884af = quay_SidebarMenuItem('Load Commands', quay_load_cmds_65bc7b5, quay_parent_5c146fb)
        for quay_cmd_67837dc in _name_boundary.attributes(_name_boundary.attributes(quay_lib_da5f1c1)['macho_header'])['load_commands']:
            quay_mmci_3bb366b = quay_MainMenuContentItem()
            _name_boundary.attributes(quay_mmci_3bb366b)['lines'] = _name_boundary.attributes(quay_cmd_67837dc)['render_indented']().split('\n')
            _name_boundary.attributes(quay_mmci_3bb366b)['lines'].append('')
            quay_raw_b3bbcac: bytes = _name_boundary.attributes(_name_boundary.attributes(quay_lib_da5f1c1)['slice'])['read_bytearray'](_name_boundary.attributes(quay_cmd_67837dc)['off'], _name_boundary.attributes(quay_cmd_67837dc)['cmdsize'])
            quay_hexdump_98d1ddf = quay_HexDumpTable()
            _name_boundary.attributes(quay_hexdump_98d1ddf)['hex'] = bytearray(quay_raw_b3bbcac)
            _name_boundary.attributes(quay_mmci_3bb366b)['lines'].append(quay_hexdump_98d1ddf)
            try:
                quay_item_name_286d1d6 = _name_boundary.attributes(quay_LOAD_COMMAND(_name_boundary.attributes(quay_cmd_67837dc)['cmd']))['name']
            except ValueError:
                quay_item_name_286d1d6 = str(_name_boundary.attributes(quay_cmd_67837dc)['cmd'])
            quay_lc_menu_item_154636f = quay_SidebarMenuItem(quay_item_name_286d1d6, quay_mmci_3bb366b, quay_menuitem_cc884af)
            _name_boundary.attributes(quay_menuitem_cc884af)['children'].append(quay_lc_menu_item_154636f)
        _name_boundary.attributes(quay_menuitem_cc884af)['parse_mmc']()
        return quay_menuitem_cc884af

    @staticmethod
    @_name_boundary.callable_contract({'lib': 'quay_lib_a8676f7', 'parent': 'quay_parent_73652f5', 'callback': 'quay_callback_e482d0f'}, 'symtab')
    def quay_symtab(quay_lib_a8676f7, quay_parent_73652f5=None, quay_callback_e482d0f=None):
        quay_callback_e482d0f(f"Slice {_name_boundary.attributes(quay_ImageQuayMachOLoader)['CUR_SL']}/{_name_boundary.attributes(quay_ImageQuayMachOLoader)['SL_CNT']}\nProcessing Symtab")
        quay_mmci_9ad6d3f = quay_MainMenuContentItem()
        quay_tab_856ccaf = quay_Table()
        _name_boundary.attributes(quay_tab_856ccaf)['titles'] = ['Address', 'Name']
        for quay_sym_3fefb0f in _name_boundary.attributes(_name_boundary.attributes(quay_lib_a8676f7)['symbol_table'])['table']:
            _name_boundary.attributes(quay_tab_856ccaf)['rows'].append([hex(_name_boundary.attributes(quay_sym_3fefb0f)['address']), _name_boundary.attributes(quay_sym_3fefb0f)['fullname']])
        _name_boundary.attributes(quay_mmci_9ad6d3f)['lines'].append(quay_tab_856ccaf)
        quay_menuitem_670a568 = quay_SidebarMenuItem('Symbol Table', quay_mmci_9ad6d3f, quay_parent_73652f5)
        _name_boundary.attributes(quay_menuitem_670a568)['parse_mmc']()
        return quay_menuitem_670a568

    @staticmethod
    @_name_boundary.callable_contract({'lib': 'quay_lib_855de70', 'parent': 'quay_parent_b3a41cc', 'callback': 'quay_callback_44db76f'}, 'vm_map')
    def quay_vm_map(quay_lib_855de70, quay_parent_b3a41cc=None, quay_callback_44db76f=None):
        quay_mmci_d9fc370 = quay_MainMenuContentItem()
        _name_boundary.attributes(quay_mmci_d9fc370)['lines'] = str(_name_boundary.attributes(quay_lib_855de70)['vm']).split('\n')
        quay_menuitem_75e1c2d = quay_SidebarMenuItem('VM Memory Map', quay_mmci_d9fc370, quay_parent_b3a41cc)
        _name_boundary.attributes(quay_menuitem_75e1c2d)['parse_mmc']()
        return quay_menuitem_75e1c2d

    @staticmethod
    @_name_boundary.callable_contract({'lib': 'quay_lib_c62fdbc', 'parent': 'quay_parent_95818cf', 'callback': 'quay_callback_2f738a8'}, 'objc_items')
    def quay_objc_items(quay_lib_c62fdbc, quay_parent_95818cf=None, quay_callback_2f738a8=None):
        quay_objc_lib_b579b84 = _name_boundary.attributes(quay_ObjCImage)['from_image'](quay_lib_c62fdbc)
        return [_name_boundary.attributes(quay_ImageQuayMachOLoader)['objc_headers'](quay_objc_lib_b579b84, quay_parent_95818cf, quay_callback_2f738a8)]

    @staticmethod
    @_name_boundary.callable_contract({'lib': 'quay_lib_4fd6682', 'parent': 'quay_parent_3de621b', 'callback': 'quay_callback_5ef3eed'}, 'swift_items')
    def quay_swift_items(quay_lib_4fd6682, quay_parent_3de621b=None, quay_callback_5ef3eed=None):
        return [_name_boundary.attributes(quay_ImageQuayMachOLoader)['swift_types'](quay_lib_4fd6682, quay_parent_3de621b, quay_callback_5ef3eed)]

    @staticmethod
    @_name_boundary.callable_contract({'lib': 'quay_lib_d7a1f88', 'parent': 'quay_parent_24f0441', 'callback': 'quay_callback_f3e844c'}, 'swift_types')
    def quay_swift_types(quay_lib_d7a1f88, quay_parent_24f0441=None, quay_callback_f3e844c=None):
        quay_callback_f3e844c(f'Loading Swift Types')
        quay_root_mmci_3f35790 = quay_MainMenuContentItem()
        quay_types_573336f = _name_boundary.attributes(quay_imagequay.ktool.load_swift_metadata(quay_lib_d7a1f88))['types']
        _name_boundary.attributes(quay_root_mmci_3f35790)['lines'] = [f"{_name_boundary.attributes(quay_i_521910c)['name']}::{_name_boundary.attributes(quay_i_521910c.__class__)['__name__']}" for quay_i_521910c in quay_types_573336f]
        quay_smi_8fcf140 = quay_SidebarMenuItem('Swift Types', quay_root_mmci_3f35790, quay_parent_24f0441)
        for quay__type_918ea92 in quay_types_573336f:
            quay_mmci_8c2f35c = quay_MainMenuContentItem()
            _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(f"{_name_boundary.attributes(quay__type_918ea92.__class__)['__name__']}")
            _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(f'')
            if isinstance(quay__type_918ea92, quay_SwiftClass):
                _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(str(_name_boundary.attributes(quay__type_918ea92)['class_desc']))
                _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(f'')
                _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(str([str(quay_i_77f802a) for quay_i_77f802a in _name_boundary.attributes(_name_boundary.attributes(quay__type_918ea92)['field_desc'])['fields']]))
                _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(f'')
                _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(str([str(quay_i_6317c0b) for quay_i_6317c0b in _name_boundary.attributes(quay__type_918ea92)['ivars']]))
                _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(f'')
            else:
                _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(str(_name_boundary.attributes(quay__type_918ea92)['typedesc']))
                _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append('')
                _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(str(_name_boundary.attributes(_name_boundary.attributes(quay__type_918ea92)['field_desc'])['desc']))
                _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(f'')
                _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(str([str(quay_i_1448301) for quay_i_1448301 in _name_boundary.attributes(_name_boundary.attributes(quay__type_918ea92)['field_desc'])['fields']]))
                _name_boundary.attributes(quay_mmci_8c2f35c)['lines'].append(f'')
            quay_ssmi_7a2cb09 = quay_SidebarMenuItem(_name_boundary.attributes(quay__type_918ea92)['name'], quay_mmci_8c2f35c, quay_smi_8fcf140)
            _name_boundary.attributes(quay_smi_8fcf140)['children'].append(quay_ssmi_7a2cb09)
        _name_boundary.attributes(quay_smi_8fcf140)['parse_mmc']()
        return quay_smi_8fcf140

    @staticmethod
    @_name_boundary.callable_contract({'lib': 'quay_lib_7e4306b', 'parent': 'quay_parent_7f8f87a', 'callback': 'quay_callback_08e7257'}, 'imports')
    def quay_imports(quay_lib_7e4306b, quay_parent_7f8f87a=None, quay_callback_08e7257=None):
        quay_callback_08e7257(f"Slice {_name_boundary.attributes(quay_ImageQuayMachOLoader)['CUR_SL']}/{_name_boundary.attributes(quay_ImageQuayMachOLoader)['SL_CNT']}\nProcessing Imports")
        quay_mmci_2fd4f37 = quay_MainMenuContentItem()
        quay_table_33f2f95 = quay_Table()
        _name_boundary.attributes(quay_table_33f2f95)['titles'] = ['Address', 'Symbol', 'Library']
        for quay_symbol_36f9798 in _name_boundary.attributes(quay_lib_7e4306b)['imports']:
            _name_boundary.attributes(quay_table_33f2f95)['rows'].append([hex(_name_boundary.attributes(quay_symbol_36f9798)['address']), _name_boundary.attributes(quay_symbol_36f9798)['fullname'], _name_boundary.attributes(_name_boundary.attributes(quay_lib_7e4306b)['linked_images'][int(_name_boundary.attributes(quay_symbol_36f9798)['ordinal']) - 1])['install_name']])
        _name_boundary.attributes(quay_mmci_2fd4f37)['lines'].append(quay_table_33f2f95)
        quay_menuitem_4a980fb = quay_SidebarMenuItem('Imports', quay_mmci_2fd4f37, quay_parent_7f8f87a)
        _name_boundary.attributes(quay_menuitem_4a980fb)['parse_mmc']()
        return quay_menuitem_4a980fb

    @staticmethod
    @_name_boundary.callable_contract({'lib': 'quay_lib_51a86fb', 'parent': 'quay_parent_d308d4a', 'callback': 'quay_callback_e4e2df2'}, 'exports')
    def quay_exports(quay_lib_51a86fb, quay_parent_d308d4a=None, quay_callback_e4e2df2=None):
        quay_callback_e4e2df2(f"Slice {_name_boundary.attributes(quay_ImageQuayMachOLoader)['CUR_SL']}/{_name_boundary.attributes(quay_ImageQuayMachOLoader)['SL_CNT']}\nProcessing Exports")
        quay_mmci_d293926 = quay_MainMenuContentItem()
        quay_table_142a8e7 = quay_Table()
        _name_boundary.attributes(quay_table_142a8e7)['titles'] = ['Address', 'Symbol']
        for quay_symbol_d556c2c in _name_boundary.attributes(quay_lib_51a86fb)['exports']:
            _name_boundary.attributes(quay_table_142a8e7)['rows'].append([hex(_name_boundary.attributes(quay_symbol_d556c2c)['address']), _name_boundary.attributes(quay_symbol_d556c2c)['fullname']])
        _name_boundary.attributes(quay_mmci_d293926)['lines'].append(quay_table_142a8e7)
        quay_menuitem_fb5f463 = quay_SidebarMenuItem('Exports', quay_mmci_d293926, quay_parent_d308d4a)
        _name_boundary.attributes(quay_menuitem_fb5f463)['parse_mmc']()
        return quay_menuitem_fb5f463

    @staticmethod
    @_name_boundary.callable_contract({'text': 'quay_text_5257cf4', 'name': 'quay_name_1c36fe4'}, 'get_header_item')
    def quay_get_header_item(quay_text_5257cf4, quay_name_1c36fe4):
        quay_mmci_87ade6c = quay_MainMenuContentItem()
        quay_formatter_6578754 = quay_Terminal256Formatter() if _name_boundary.attributes(quay_ImageQuayMachOLoader)['SUPPORTS_256'] else quay_TerminalFormatter()
        quay_text_5257cf4 = quay_highlight(quay_text_5257cf4, quay_ObjectiveCLexer(), quay_formatter_6578754)
        quay_lines_cbac0f1 = quay_text_5257cf4.split('\n')
        _name_boundary.attributes(quay_mmci_87ade6c)['lines'] = quay_lines_cbac0f1
        quay_h_menu_item_7d39787 = quay_SidebarMenuItem(quay_name_1c36fe4, quay_mmci_87ade6c, None)
        return quay_h_menu_item_7d39787

    @staticmethod
    @_name_boundary.callable_contract({'text': 'quay_text_c850437'}, 'get_header_text')
    def quay_get_header_text(quay_text_c850437):
        quay_formatter_3655de1 = quay_Terminal256Formatter() if _name_boundary.attributes(quay_ImageQuayMachOLoader)['SUPPORTS_256'] else quay_TerminalFormatter()
        quay_text_c850437 = quay_highlight(quay_text_c850437, quay_ObjectiveCLexer(), quay_formatter_3655de1)
        quay_lines_138881c = []
        for quay_item_7e37473 in quay_text_c850437.split('\n'):
            quay_lines_138881c.append(_name_boundary.attributes(quay_AttributedString)['ansi_to_attrstr'](quay_item_7e37473))
        return quay_lines_138881c

    @staticmethod
    @_name_boundary.callable_contract({'objc_lib': 'quay_objc_lib_6d82c21', 'parent': 'quay_parent_8fd1cbf', 'callback': 'quay_callback_42ea22e'}, 'objc_headers')
    def quay_objc_headers(quay_objc_lib_6d82c21, quay_parent_8fd1cbf=None, quay_callback_42ea22e=None):
        quay_generator_22a40ea = quay_HeaderGenerator(quay_objc_lib_6d82c21)
        quay_hnci_2e9ad84 = quay_MainMenuContentItem()
        _name_boundary.attributes(quay_hnci_2e9ad84)['lines'] = _name_boundary.attributes(quay_generator_22a40ea)['headers'].keys()
        quay_menuitem_bbe849a = quay_SidebarMenuItem('ObjC Headers', quay_hnci_2e9ad84, quay_parent_8fd1cbf)
        quay_count_682cbf7 = len(_name_boundary.attributes(quay_generator_22a40ea)['headers'].keys())
        quay_callback_42ea22e(f"Slice {_name_boundary.attributes(quay_ImageQuayMachOLoader)['CUR_SL']}/{_name_boundary.attributes(quay_ImageQuayMachOLoader)['SL_CNT']}\nProcessing {quay_count_682cbf7} ObjC Headers")
        quay_items_3234c0a = []
        quay_i_4e71b0a = 1
        for quay_header_name_d06cf7d, quay_header_54b6a27 in _name_boundary.attributes(_name_boundary.attributes(quay_generator_22a40ea)['headers'])['items']():
            quay_callback_42ea22e(f"Slice {_name_boundary.attributes(quay_ImageQuayMachOLoader)['CUR_SL']}/{_name_boundary.attributes(quay_ImageQuayMachOLoader)['SL_CNT']}\nProcessing {quay_count_682cbf7} ObjC Headers\n{quay_i_4e71b0a}/{quay_count_682cbf7}")
            quay_mmci_65fbf18 = quay_MainMenuContentItem()
            quay_buffer_7d37b02 = quay_LazilyProcessedTextBuffer()
            _name_boundary.attributes(quay_buffer_7d37b02)['target'] = _name_boundary.attributes(quay_ImageQuayMachOLoader)['get_header_text']
            _name_boundary.attributes(quay_buffer_7d37b02)['target_args'] = [str(quay_header_54b6a27)]
            _name_boundary.attributes(quay_mmci_65fbf18)['lines'] = [quay_buffer_7d37b02]
            quay_sbmi_cd39db5 = quay_SidebarMenuItem(quay_header_name_d06cf7d, quay_mmci_65fbf18, quay_menuitem_bbe849a)
            quay_items_3234c0a.append(quay_sbmi_cd39db5)
            quay_i_4e71b0a += 1
        _name_boundary.attributes(quay_menuitem_bbe849a)['children'] = quay_items_3234c0a
        _name_boundary.attributes(quay_menuitem_bbe849a)['parse_mmc']()
        return quay_menuitem_bbe849a

@_name_boundary.class_contract('KToolKernelCacheLoader', {'slice_item': 'quay_slice_item', '_file': 'quay__file', 'get_kexts': 'quay_get_kexts'})
class quay_ImageQuayKernelCacheLoader(quay_ImageQuayMachOLoader):

    @staticmethod
    @_name_boundary.callable_contract({'macho_slice': 'quay_macho_slice_c62c299', 'callback': 'quay_callback_c2aaf42'}, 'slice_item')
    def quay_slice_item(quay_macho_slice_c62c299, quay_callback_c2aaf42):
        quay_loaded_image_f9602c6 = _name_boundary.attributes(quay_MachOImageLoader)['load'](quay_macho_slice_c62c299)
        quay_slice_nick_40d6bd9 = f'Kernel Cache'
        quay_callback_c2aaf42(f'Kernel Cache\nLoading MachO Image')
        quay_slice_item_d8249fe = quay_SidebarMenuItem(f'Kernel Cache', None, None)
        quay_kcache_aa0c3e0 = quay_KernelCache(_name_boundary.attributes(quay_macho_slice_c62c299)['macho_file'])
        _name_boundary.attributes(quay_slice_item_d8249fe)['content'] = _name_boundary.attributes(_name_boundary.attributes(quay_ImageQuayKernelCacheLoader)['_file'](quay_kcache_aa0c3e0, quay_slice_item_d8249fe, quay_callback_c2aaf42))['content']
        quay_items_73d0a11 = [_name_boundary.attributes(quay_ImageQuayMachOLoader)['load_cmds'], _name_boundary.attributes(quay_ImageQuayMachOLoader)['segments'], _name_boundary.attributes(quay_ImageQuayMachOLoader)['symtab']]
        for quay_item_af53e8a in quay_items_73d0a11:
            try:
                _name_boundary.attributes(quay_slice_item_d8249fe)['children'].append(quay_item_af53e8a(quay_loaded_image_f9602c6, quay_slice_item_d8249fe, quay_callback_c2aaf42))
            except Exception as quay_ex_35b3f01:
                if _name_boundary.attributes(quay_ImageQuayMachOLoader)['HARD_FAIL']:
                    raise quay_ex_35b3f01
                else:
                    pass
        quay_kernel_items_4944751 = [_name_boundary.attributes(quay_ImageQuayKernelCacheLoader)['get_kexts']]
        for quay_item_af53e8a in quay_kernel_items_4944751:
            try:
                _name_boundary.attributes(quay_slice_item_d8249fe)['children'].append(quay_item_af53e8a(quay_kcache_aa0c3e0, quay_slice_item_d8249fe, quay_callback_c2aaf42))
            except Exception as quay_ex_35b3f01:
                if _name_boundary.attributes(quay_ImageQuayMachOLoader)['HARD_FAIL']:
                    raise quay_ex_35b3f01
                else:
                    pass
        _name_boundary.attributes(quay_slice_item_d8249fe)['show_children'] = True
        return quay_slice_item_d8249fe

    @staticmethod
    @_name_boundary.callable_contract({'kcache': 'quay_kcache_d79467f', 'parent': 'quay_parent_1f91d7c', 'callback': 'quay_callback_b906845'}, '_file')
    def quay__file(quay_kcache_d79467f, quay_parent_1f91d7c=None, quay_callback_b906845=None):
        quay_file_content_item_6368eda = quay_MainMenuContentItem()
        quay_lib_25ab3ef = _name_boundary.attributes(quay_kcache_d79467f)['mach_kernel']
        _name_boundary.attributes(quay_file_content_item_6368eda)['lines'].append(f"Release Type: §35m{_name_boundary.attributes(quay_kcache_d79467f)['release_type']}§39m")
        _name_boundary.attributes(quay_file_content_item_6368eda)['lines'].append(f"SOC: §35m{_name_boundary.attributes(quay_kcache_d79467f)['soc']}§39m")
        _name_boundary.attributes(quay_file_content_item_6368eda)['lines'].append(f"Arch: §35m{_name_boundary.attributes(quay_kcache_d79467f)['arch']}§39m")
        _name_boundary.attributes(quay_file_content_item_6368eda)['lines'].append('')
        _name_boundary.attributes(quay_file_content_item_6368eda)['lines'].append(f"Kernel Version: §35m{_name_boundary.attributes(quay_kcache_d79467f)['version']}§39m")
        _name_boundary.attributes(quay_file_content_item_6368eda)['lines'].append(f"{_name_boundary.attributes(quay_kcache_d79467f)['version_str']}")
        if _name_boundary.attributes(quay_lib_25ab3ef)['uuid']:
            _name_boundary.attributes(quay_file_content_item_6368eda)['lines'].append(f"UUID: §35m{_name_boundary.attributes(_name_boundary.attributes(quay_lib_25ab3ef)['uuid'])['hex']().upper()}§39m")
        _name_boundary.attributes(quay_file_content_item_6368eda)['lines'].append(f"Platform: §35m{_name_boundary.attributes(_name_boundary.attributes(quay_lib_25ab3ef)['platform'])['name']}§39m")
        _name_boundary.attributes(quay_file_content_item_6368eda)['lines'].append(f"Minimum OS: §35m{_name_boundary.attributes(_name_boundary.attributes(quay_lib_25ab3ef)['minos'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_lib_25ab3ef)['minos'])['y']}.{_name_boundary.attributes(quay_lib_25ab3ef)['minos'].z}§39m")
        _name_boundary.attributes(quay_file_content_item_6368eda)['lines'].append(f"SDK Version: §35m{_name_boundary.attributes(_name_boundary.attributes(quay_lib_25ab3ef)['sdk_version'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_lib_25ab3ef)['sdk_version'])['y']}.{_name_boundary.attributes(quay_lib_25ab3ef)['sdk_version'].z}§39m")
        quay_menuitem_63b4161 = quay_SidebarMenuItem('File Info', quay_file_content_item_6368eda, quay_parent_1f91d7c)
        _name_boundary.attributes(quay_menuitem_63b4161)['parse_mmc']()
        return quay_menuitem_63b4161

    @staticmethod
    @_name_boundary.callable_contract({'kcache': 'quay_kcache_64a2840', 'parent': 'quay_parent_ef6e2e2', 'callback': 'quay_callback_56ef57c'}, 'get_kexts')
    def quay_get_kexts(quay_kcache_64a2840: quay_KernelCache, quay_parent_ef6e2e2=None, quay_callback_56ef57c=None):
        quay_hnci_0f09955 = quay_MainMenuContentItem()
        _name_boundary.attributes(quay_hnci_0f09955)['lines'] = [_name_boundary.attributes(quay_kext_25215e5)['name'] for quay_kext_25215e5 in _name_boundary.attributes(quay_kcache_64a2840)['kexts']]
        quay_menuitem_133dcab = quay_SidebarMenuItem('KEXTs', quay_hnci_0f09955, quay_parent_ef6e2e2)
        quay_count_70689fc = len(_name_boundary.attributes(quay_kcache_64a2840)['kexts'])
        quay_callback_56ef57c(f'Kernel Cache\nProcessing {quay_count_70689fc} KEXTs')
        quay_items_c1eeb58 = []
        quay_i_635cf56 = 1
        for quay_kext_4566d1e in _name_boundary.attributes(quay_kcache_64a2840)['kexts']:
            quay_callback_56ef57c(f'Kernel Cache\nProcessing {quay_count_70689fc} KEXT \n{quay_i_635cf56}/{quay_count_70689fc}')
            quay_mmci_65700f1 = quay_MainMenuContentItem()
            _name_boundary.attributes(quay_mmci_65700f1)['lines'] = []
            _name_boundary.attributes(quay_mmci_65700f1)['lines'].append(f"ID: {_name_boundary.attributes(quay_kext_4566d1e)['name']}")
            _name_boundary.attributes(quay_mmci_65700f1)['lines'].append(f"Embedded Version: {_name_boundary.attributes(quay_kext_4566d1e)['version']}")
            if _name_boundary.attributes(quay_kext_4566d1e)['prelink_info']:
                quay_bundle_text_b167254 = f"Executable Name: {_name_boundary.attributes(quay_kext_4566d1e)['executable_name']}\n{_name_boundary.attributes(quay_kext_4566d1e)['info_string']}\nVersion: {_name_boundary.attributes(quay_kext_4566d1e)['version_str']}\nStart Address: {hex(_name_boundary.attributes(quay_kext_4566d1e)['start_addr'] | (18446462598732840960 if _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_kcache_64a2840)['mach_kernel'])['vm'])['detag_kern_64'] else 0))}".split('\n')
                quay_bundle_text_b167254 += ['', '']
                quay_bundle_text_b167254 += quay_pprint.pformat(_name_boundary.attributes(quay_kext_4566d1e)['prelink_info']).split('\n')
                _name_boundary.attributes(quay_mmci_65700f1)['lines'] += quay_bundle_text_b167254
            quay_sbmi_c0ee395 = quay_SidebarMenuItem(_name_boundary.attributes(quay_kext_4566d1e)['name'], quay_mmci_65700f1, quay_menuitem_133dcab)
            quay_items_c1eeb58.append(quay_sbmi_c0ee395)
            quay_i_635cf56 += 1
        _name_boundary.attributes(quay_menuitem_133dcab)['children'] = quay_items_c1eeb58
        _name_boundary.attributes(quay_menuitem_133dcab)['parse_mmc']()
        return quay_menuitem_133dcab

@_name_boundary.class_contract('KToolScreen', {'ktool_dbg_print_func': 'quay_imagequay_dbg_print_func', 'ktool_dbg_print_err_func': 'quay_imagequay_dbg_print_err_func', 'setup': 'quay_setup', 'teardown': 'quay_teardown', 'update_mainscreen_text': 'quay_update_mainscreen_text', 'update_load_status': 'quay_update_load_status', 'load_image': 'quay_load_image', 'load_file': 'quay_load_file', 'rebuild_all': 'quay_rebuild_all', 'redraw_all': 'quay_redraw_all', 'handle_present_menu_exception': 'quay_handle_present_menu_exception', 'handle_mouse': 'quay_handle_mouse', 'handle_key_press': 'quay_handle_key_press', 'program_loop': 'quay_program_loop', 'supports_color': 'quay_supports_color', 'supported_colors': 'quay_supported_colors', 'hard_fail': 'quay_hard_fail', 'stdscr': 'quay_stdscr', 'root': 'quay_root', 'filename': 'quay_filename', 'titlebar': 'quay_titlebar', 'sidebar': 'quay_sidebar', 'mainscreen': 'quay_mainscreen', 'footerbar': 'quay_footerbar', 'debug_menu': 'quay_debug_menu', 'help_menu': 'quay_help_menu', 'title_menu_overlay': 'quay_title_menu_overlay', 'loader_status': 'quay_loader_status', 'file_browser': 'quay_file_browser', 'input_overlay': 'quay_input_overlay', 'is_showing_menu_overlay': 'quay_is_showing_menu_overlay', 'active_key_handler': 'quay_active_key_handler', 'key_handlers': 'quay_key_handlers', 'mouse_handlers': 'quay_mouse_handlers', 'last_mouse_event': 'quay_last_mouse_event', 'render_group': 'quay_render_group'})
class quay_ImageQuayScreen:

    @_name_boundary.callable_contract({'self': 'quay_self_3a0cd3a', 'hard_fail': 'quay_hard_fail_8145f05'}, '__init__')
    def __init__(quay_self_3a0cd3a, quay_hard_fail_8145f05=False):
        _name_boundary.attributes(quay_self_3a0cd3a)['supports_color'] = False
        _name_boundary.attributes(quay_self_3a0cd3a)['supported_colors'] = 0
        _name_boundary.attributes(quay_self_3a0cd3a)['hard_fail'] = quay_hard_fail_8145f05
        _name_boundary.attributes(quay_ImageQuayMachOLoader)['HARD_FAIL'] = quay_hard_fail_8145f05
        _name_boundary.attributes(quay_self_3a0cd3a)['stdscr'] = _name_boundary.attributes(quay_self_3a0cd3a)['setup']()
        _name_boundary.attributes(quay_self_3a0cd3a)['root'] = quay_RootBox(_name_boundary.attributes(quay_self_3a0cd3a)['stdscr'])
        _name_boundary.attributes(quay_self_3a0cd3a)['filename'] = ''
        _name_boundary.attributes(quay_self_3a0cd3a)['titlebar'] = quay_TitleBar()
        _name_boundary.attributes(quay_self_3a0cd3a)['sidebar'] = quay_Sidebar()
        _name_boundary.attributes(quay_self_3a0cd3a)['mainscreen'] = quay_MainScreen()
        _name_boundary.attributes(quay_self_3a0cd3a)['footerbar'] = quay_FooterBar()
        _name_boundary.attributes(quay_self_3a0cd3a)['debug_menu'] = quay_DebugMenu()
        _name_boundary.attributes(quay_self_3a0cd3a)['help_menu'] = quay_HelpMenu()
        _name_boundary.attributes(quay_self_3a0cd3a)['title_menu_overlay'] = quay_MenuOverlayRenderingView()
        _name_boundary.attributes(quay_self_3a0cd3a)['loader_status'] = quay_LoaderStatusView()
        _name_boundary.attributes(quay_self_3a0cd3a)['file_browser'] = quay_FileSystemBrowserOverlayView()
        _name_boundary.attributes(quay_self_3a0cd3a)['input_overlay'] = quay_UserInputPrompt()
        _name_boundary.attributes(quay_self_3a0cd3a)['is_showing_menu_overlay'] = False
        _name_boundary.attributes(quay_self_3a0cd3a)['active_key_handler'] = _name_boundary.attributes(quay_self_3a0cd3a)['sidebar']
        _name_boundary.attributes(quay_self_3a0cd3a)['key_handlers'] = []
        _name_boundary.attributes(quay_self_3a0cd3a)['mouse_handlers'] = []
        _name_boundary.attributes(quay_self_3a0cd3a)['last_mouse_event'] = ''
        _name_boundary.attributes(quay_self_3a0cd3a)['render_group'] = [_name_boundary.attributes(quay_self_3a0cd3a)['titlebar'], _name_boundary.attributes(quay_self_3a0cd3a)['sidebar'], _name_boundary.attributes(quay_self_3a0cd3a)['mainscreen'], _name_boundary.attributes(quay_self_3a0cd3a)['footerbar'], _name_boundary.attributes(quay_self_3a0cd3a)['title_menu_overlay'], _name_boundary.attributes(quay_self_3a0cd3a)['debug_menu'], _name_boundary.attributes(quay_self_3a0cd3a)['help_menu'], _name_boundary.attributes(quay_self_3a0cd3a)['loader_status'], _name_boundary.attributes(quay_self_3a0cd3a)['file_browser'], _name_boundary.attributes(quay_self_3a0cd3a)['input_overlay']]
        _name_boundary.attributes(quay_self_3a0cd3a)['rebuild_all']()
        _name_boundary.attributes(quay_self_3a0cd3a)['stdscr'].refresh()

    @_name_boundary.callable_contract({'self': 'quay_self_4c8a497', 'msg': 'quay_msg_da8ace1'}, 'ktool_dbg_print_func')
    def quay_imagequay_dbg_print_func(quay_self_4c8a497, quay_msg_da8ace1):
        _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_4c8a497)['debug_menu'])['scroll_view_text_buffer'])['lines'].append(quay_msg_da8ace1)

    @_name_boundary.callable_contract({'self': 'quay_self_47d2ec9', 'msg': 'quay_msg_c6d62b2'}, 'ktool_dbg_print_err_func')
    def quay_imagequay_dbg_print_err_func(quay_self_47d2ec9, quay_msg_c6d62b2):
        _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_47d2ec9)['debug_menu'])['scroll_view_text_buffer'])['lines'].append('§32m' + quay_msg_c6d62b2 + '§39m')

    @_name_boundary.callable_contract({'self': 'quay_self_591697b'}, 'setup')
    def quay_setup(quay_self_591697b):
        """
        Perform the curses initialization ritual
        :return: curses standard screen instance.
        """
        quay_stdscr_31e0411 = quay_curses.initscr()
        quay_curses.noecho()
        quay_curses.cbreak()
        quay_stdscr_31e0411.keypad(True)
        quay_curses.mousemask(quay_curses.ALL_MOUSE_EVENTS)
        quay_curses.start_color()
        quay_curses.use_default_colors()
        quay_curses.curs_set(0)
        _name_boundary.attributes(quay_self_591697b)['supports_color'] = quay_curses.has_colors()
        for quay_i_b374948 in range(0, quay_curses.COLORS):
            try:
                quay_curses.init_pair(quay_i_b374948 + 1, quay_i_b374948, -1)
                _name_boundary.attributes(quay_self_591697b)['supported_colors'] += 1
            except ValueError:
                pass
        return quay_stdscr_31e0411

    @_name_boundary.callable_contract({'self': 'quay_self_673e375'}, 'teardown')
    def quay_teardown(quay_self_673e375):
        """
        Perform the exact opposite of the setup() task. Return terminal to normalcy.

        IT IS ABSOLUTELY CRITICAL THAT THIS GETS CALLED ON EXIT. DO ABSOLUTELY EVERYTHING POSSIBLE TO TRY AND MAKE THAT
            HAPPEN. NOT DOING SO WILL REALLY FUCK UP TERM DISPLAY.
        :return:
        """
        quay_curses.echo()
        quay_curses.nocbreak()
        _name_boundary.attributes(quay_self_673e375)['stdscr'].keypad(False)
        quay_curses.mousemask(0)
        quay_curses.curs_set(1)
        quay_curses.endwin()

    @_name_boundary.callable_contract({'self': 'quay_self_6212242'}, 'update_mainscreen_text')
    def quay_update_mainscreen_text(quay_self_6212242):
        """
        Pull lines from currently selected sidebar item and copy them over into the Main Screen.

        :return:
        """
        if len(_name_boundary.attributes(_name_boundary.attributes(quay_self_6212242)['sidebar'])['processed_items']) < 1:
            return
        quay_item_4bc5992 = _name_boundary.attributes(_name_boundary.attributes(quay_self_6212242)['sidebar'])['processed_items'][_name_boundary.attributes(_name_boundary.attributes(quay_self_6212242)['sidebar'])['selected_index']]
        _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_6212242)['mainscreen'])['scroll_view_text_buffer'])['lines'] = _name_boundary.attributes(_name_boundary.attributes(quay_item_4bc5992)['content'])['lines']
        if _name_boundary.attributes(_name_boundary.attributes(quay_self_6212242)['mainscreen'])['currently_displayed_index'] != _name_boundary.attributes(_name_boundary.attributes(quay_self_6212242)['sidebar'])['selected_index']:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_6212242)['mainscreen'])['currently_displayed_index'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_6212242)['sidebar'])['selected_index']
            _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_6212242)['mainscreen'])['scroll_view_text_buffer'])['scrollcursor'] = 0
            _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_6212242)['mainscreen'])['scroll_view_text_buffer'])['process_lines']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_6212242)['mainscreen'])['set_tab_name'](_name_boundary.attributes(quay_item_4bc5992)['name'])

    @_name_boundary.callable_contract({'self': 'quay_self_920328d', 'msg': 'quay_msg_a31aee8'}, 'update_load_status')
    def quay_update_load_status(quay_self_920328d, quay_msg_a31aee8):
        _name_boundary.attributes(_name_boundary.attributes(quay_self_920328d)['loader_status'])['status_string'] = quay_msg_a31aee8
        _name_boundary.attributes(quay_self_920328d)['redraw_all']()

    @_name_boundary.callable_contract({'self': 'quay_self_9f4488c', 'image': 'quay_image_5d5ab25', 'filename': 'quay_filename_a54834b'}, 'load_image')
    def quay_load_image(quay_self_9f4488c, quay_image_5d5ab25, quay_filename_a54834b):
        """
         Load an Image into the GUI.

         :param filename:
         :return:
         """
        try:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_9f4488c)['loader_status'])['draw'] = True
            _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_9f4488c)['mainscreen'])['scroll_view_text_buffer'])['lines'] = [f'Loading {quay_filename_a54834b}...']
            _name_boundary.attributes(quay_self_9f4488c)['redraw_all']()
            _name_boundary.attributes(_name_boundary.attributes(quay_self_9f4488c)['mainscreen'])['set_tab_name'](quay_filename_a54834b)
            for quay_item_978f64b in _name_boundary.attributes(quay_ImageQuayMachOLoader)['contents_for_image'](quay_image_5d5ab25, _name_boundary.attributes(quay_self_9f4488c)['update_load_status']):
                _name_boundary.attributes(_name_boundary.attributes(quay_self_9f4488c)['sidebar'])['add_menu_item'](quay_item_978f64b)
            _name_boundary.attributes(quay_self_9f4488c)['active_key_handler'] = _name_boundary.attributes(quay_self_9f4488c)['sidebar']
            _name_boundary.attributes(quay_self_9f4488c)['key_handlers'] = [_name_boundary.attributes(quay_self_9f4488c)['sidebar'], _name_boundary.attributes(quay_self_9f4488c)['mainscreen'], _name_boundary.attributes(quay_self_9f4488c)['titlebar'], _name_boundary.attributes(quay_self_9f4488c)['file_browser']]
            _name_boundary.attributes(quay_self_9f4488c)['mouse_handlers'] = [_name_boundary.attributes(quay_self_9f4488c)['sidebar'], _name_boundary.attributes(quay_self_9f4488c)['titlebar'], _name_boundary.attributes(quay_self_9f4488c)['title_menu_overlay'], _name_boundary.attributes(quay_self_9f4488c)['debug_menu'], _name_boundary.attributes(quay_self_9f4488c)['input_overlay'], _name_boundary.attributes(quay_self_9f4488c)['help_menu']]
            _name_boundary.attributes(_name_boundary.attributes(quay_self_9f4488c)['loader_status'])['draw'] = False
            _name_boundary.attributes(_name_boundary.attributes(quay_self_9f4488c)['input_overlay'])['draw'] = False
            _name_boundary.attributes(quay_self_9f4488c)['redraw_all']()
            _name_boundary.attributes(quay_self_9f4488c)['program_loop']()
        except Exception as quay_ex_db7042d:
            _name_boundary.attributes(quay_self_9f4488c)['teardown']()
            raise quay_ex_db7042d

    @_name_boundary.callable_contract({'self': 'quay_self_4ef31b5', 'filename': 'quay_filename_7d051cb', 'mmap': 'quay_mmap_c4b74f6'}, 'load_file')
    def quay_load_file(quay_self_4ef31b5, quay_filename_7d051cb, quay_mmap_c4b74f6=True):
        """
        Load a file by filename into the GUI.

        :param filename:
        :return:
        """
        try:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_4ef31b5)['loader_status'])['draw'] = True
            _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_4ef31b5)['mainscreen'])['scroll_view_text_buffer'])['lines'] = [f'Loading {quay_filename_7d051cb}...']
            _name_boundary.attributes(quay_self_4ef31b5)['redraw_all']()
            quay_fd_2b4d305 = open(quay_filename_7d051cb, 'rb')
            _name_boundary.attributes(_name_boundary.attributes(quay_self_4ef31b5)['mainscreen'])['set_tab_name'](quay_filename_7d051cb)
            quay_filename_base_908dc2e = _name_boundary.attributes(quay_os)['path'].basename(quay_filename_7d051cb)
            quay_first1k_2c4600e = _name_boundary.attributes(quay_fd_2b4d305)['read'](4096)
            quay_fd_2b4d305.seek(0)
            if b'__BOOTDATA\x00\x00\x00\x00\x00\x00' in quay_first1k_2c4600e:
                for quay_item_f073c98 in _name_boundary.attributes(quay_ImageQuayKernelCacheLoader)['contents_for_file'](quay_fd_2b4d305, _name_boundary.attributes(quay_self_4ef31b5)['update_load_status']):
                    _name_boundary.attributes(_name_boundary.attributes(quay_self_4ef31b5)['sidebar'])['add_menu_item'](quay_item_f073c98)
            else:
                for quay_item_f073c98 in _name_boundary.attributes(quay_ImageQuayMachOLoader)['contents_for_file'](quay_fd_2b4d305, _name_boundary.attributes(quay_self_4ef31b5)['update_load_status'], quay_mmap_c4b74f6):
                    _name_boundary.attributes(_name_boundary.attributes(quay_self_4ef31b5)['sidebar'])['add_menu_item'](quay_item_f073c98)
            _name_boundary.attributes(quay_self_4ef31b5)['active_key_handler'] = _name_boundary.attributes(quay_self_4ef31b5)['sidebar']
            _name_boundary.attributes(quay_self_4ef31b5)['key_handlers'] = [_name_boundary.attributes(quay_self_4ef31b5)['sidebar'], _name_boundary.attributes(quay_self_4ef31b5)['mainscreen'], _name_boundary.attributes(quay_self_4ef31b5)['titlebar'], _name_boundary.attributes(quay_self_4ef31b5)['file_browser']]
            _name_boundary.attributes(quay_self_4ef31b5)['mouse_handlers'] = [_name_boundary.attributes(quay_self_4ef31b5)['sidebar'], _name_boundary.attributes(quay_self_4ef31b5)['titlebar'], _name_boundary.attributes(quay_self_4ef31b5)['title_menu_overlay'], _name_boundary.attributes(quay_self_4ef31b5)['debug_menu'], _name_boundary.attributes(quay_self_4ef31b5)['input_overlay'], _name_boundary.attributes(quay_self_4ef31b5)['help_menu']]
            _name_boundary.attributes(_name_boundary.attributes(quay_self_4ef31b5)['loader_status'])['draw'] = False
            _name_boundary.attributes(_name_boundary.attributes(quay_self_4ef31b5)['input_overlay'])['draw'] = False
            _name_boundary.attributes(quay_self_4ef31b5)['redraw_all']()
            _name_boundary.attributes(quay_self_4ef31b5)['program_loop']()
        except Exception as quay_ex_0319a57:
            _name_boundary.attributes(quay_self_4ef31b5)['teardown']()
            raise quay_ex_0319a57

    @_name_boundary.callable_contract({'self': 'quay_self_bf9637d'}, 'rebuild_all')
    def quay_rebuild_all(quay_self_bf9637d):
        """
        Reconstruct all Views from the ground up (almost).

        This can be called on terminal resize to update the sizes of views/scroll buffers properly.

        Note: calls redraw_all() and refreshes the screen once finished.

        :return:
        """
        _name_boundary.attributes(quay_self_bf9637d)['stdscr'].clear()
        quay_lines_4d82923, quay_cols_fad11b7 = _name_boundary.attributes(quay_self_bf9637d)['stdscr'].getmaxyx()
        quay_curses.LINES = quay_lines_4d82923
        quay_curses.COLS = quay_cols_fad11b7
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['title_menu_overlay'])['box'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], 0, 0, quay_curses.COLS, quay_curses.LINES)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['loader_status'])['box'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], 0, 0, quay_curses.COLS, quay_curses.LINES)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['titlebar'])['box'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], 0, 0, quay_curses.COLS, 1)
        _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['titlebar'])['exit_button'])['box'])['x'] = quay_curses.COLS - 10
        _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['titlebar'])['exit_button'])['box'])['parent'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['titlebar'])['box']
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['sidebar'])['box'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], 0, 1, _name_boundary.attributes(quay_Sidebar)['WIDTH'], quay_curses.LINES - 2)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['sidebar'])['scroll_view'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], 1, 2, _name_boundary.attributes(quay_Sidebar)['WIDTH'] - 2, quay_curses.LINES - 4)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['sidebar'])['scroll_view_text_buffer'] = quay_ScrollingDisplayBuffer(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['sidebar'])['scroll_view'], 1, 0, _name_boundary.attributes(quay_Sidebar)['WIDTH'] - 4, quay_curses.LINES - 5)
        _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['sidebar'])['scroll_view_text_buffer'])['wrap'] = False
        quay_width_4c4d4dd = quay_curses.COLS - _name_boundary.attributes(quay_Sidebar)['WIDTH'] - 2
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['mainscreen'])['box'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], _name_boundary.attributes(quay_Sidebar)['WIDTH'], 1, quay_width_4c4d4dd, quay_curses.LINES - 2)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['mainscreen'])['info_box'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], _name_boundary.attributes(quay_Sidebar)['WIDTH'] + 1, 1, quay_width_4c4d4dd - 1, 1)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['mainscreen'])['scroll_view'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], _name_boundary.attributes(quay_Sidebar)['WIDTH'] + 2, 3, quay_width_4c4d4dd - 6, quay_curses.LINES - 4)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['mainscreen'])['scroll_view_text_buffer'] = quay_ScrollingDisplayBuffer(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['mainscreen'])['scroll_view'], 1, 0, quay_width_4c4d4dd - 8, quay_curses.LINES - 5)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['debug_menu'])['box'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], 5, 5, quay_curses.COLS - 10, quay_curses.LINES - 10)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['debug_menu'])['scroll_view'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], 7, 6, quay_curses.COLS - 12, quay_curses.LINES - 12)
        quay_ls_79540b4 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['debug_menu'])['scroll_view_text_buffer'])['lines'] if _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['debug_menu'])['scroll_view_text_buffer'] else []
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['debug_menu'])['scroll_view_text_buffer'] = quay_ScrollingDisplayBuffer(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['debug_menu'])['scroll_view'], 0, 0, quay_curses.COLS - 22, quay_curses.LINES - 12)
        _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['debug_menu'])['scroll_view_text_buffer'])['render_attr'] = quay_curses.color_pair(1)
        _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['debug_menu'])['scroll_view_text_buffer'])['lines'] = quay_ls_79540b4
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['debug_menu'])['parse_lines']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['help_menu'])['box'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], 5, 5, quay_curses.COLS - 10, quay_curses.LINES - 10)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['help_menu'])['scroll_view'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], 7, 6, quay_curses.COLS - 12, quay_curses.LINES - 12)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['help_menu'])['scroll_view_text_buffer'] = quay_ScrollingDisplayBuffer(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['help_menu'])['scroll_view'], 0, 0, quay_curses.COLS - 22, quay_curses.LINES - 12)
        _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['help_menu'])['scroll_view_text_buffer'])['lines'] = quay_MAIN_TEXT.split('\n')
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['file_browser'])['box'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], 0, 0, quay_curses.COLS, quay_curses.LINES)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['file_browser'])['scroll_view'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], 5, 4, quay_curses.COLS - 10, quay_curses.LINES - 8)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['file_browser'])['scroll_view_text_buffer'] = quay_ScrollingDisplayBuffer(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['file_browser'])['scroll_view'], 0, 0, quay_curses.COLS - 10, quay_curses.LINES - 10)
        _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['file_browser'])['scroll_view_text_buffer'])['wrap'] = False
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['mainscreen'])['currently_displayed_index'] = -1
        _name_boundary.attributes(quay_self_bf9637d)['update_mainscreen_text']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_bf9637d)['footerbar'])['box'] = quay_Box(_name_boundary.attributes(quay_self_bf9637d)['root'], 0, quay_curses.LINES - 1, quay_curses.COLS, 1)
        _name_boundary.attributes(quay_self_bf9637d)['redraw_all']()

    @_name_boundary.callable_contract({'self': 'quay_self_7904353'}, 'redraw_all')
    def quay_redraw_all(quay_self_7904353):
        """
        Wipe the screen and have the views redraw their contents

        :return:
        """
        _name_boundary.attributes(quay_self_7904353)['stdscr'].erase()
        _name_boundary.attributes(quay_self_7904353)['update_mainscreen_text']()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_7904353)['footerbar'])['debug_text'] = f"{quay_curses.COLS}x{quay_curses.LINES} | {_name_boundary.attributes(_name_boundary.attributes(quay_self_7904353)['sidebar'])['selected_index']} | {_name_boundary.attributes(quay_self_7904353)['last_mouse_event']} | self.titlebar.pres_menu_item = {str(_name_boundary.attributes(_name_boundary.attributes(quay_self_7904353)['titlebar'])['pres_menu_item'])} "
        _name_boundary.attributes(_name_boundary.attributes(quay_self_7904353)['debug_menu'])['lines'] = [f"•Sself.titlebar.pres_menu_item = {str(_name_boundary.attributes(_name_boundary.attributes(quay_self_7904353)['titlebar'])['pres_menu_item'])}"]
        for quay_item_4cc9f84 in _name_boundary.attributes(quay_self_7904353)['render_group']:
            if _name_boundary.attributes(quay_item_4cc9f84)['draw']:
                _name_boundary.attributes(quay_item_4cc9f84)['redraw']()
        _name_boundary.attributes(quay_self_7904353)['stdscr'].refresh()

    @_name_boundary.callable_contract({'self': 'quay_self_ad2e9d4', 'yes': 'quay_yes_6bd32bb'}, 'handle_present_menu_exception')
    def quay_handle_present_menu_exception(quay_self_ad2e9d4, quay_yes_6bd32bb):
        if not quay_yes_6bd32bb:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_ad2e9d4)['title_menu_overlay'])['draw'] = False
            _name_boundary.attributes(quay_self_ad2e9d4)['is_showing_menu_overlay'] = False
            _name_boundary.attributes(_name_boundary.attributes(quay_self_ad2e9d4)['titlebar'])['pres_menu_item_index'] = -1
            _name_boundary.attributes(quay_self_ad2e9d4)['active_key_handler'] = _name_boundary.attributes(quay_self_ad2e9d4)['sidebar']
        else:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_ad2e9d4)['title_menu_overlay'])['draw'] = True
            _name_boundary.attributes(_name_boundary.attributes(quay_self_ad2e9d4)['title_menu_overlay'])['active_render_menu'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_ad2e9d4)['titlebar'])['pres_menu_item'][0]
            _name_boundary.attributes(_name_boundary.attributes(quay_self_ad2e9d4)['title_menu_overlay'])['active_menu_start_x'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_ad2e9d4)['titlebar'])['pres_menu_item'][1]
            _name_boundary.attributes(quay_self_ad2e9d4)['is_showing_menu_overlay'] = True
            _name_boundary.attributes(quay_self_ad2e9d4)['active_key_handler'] = _name_boundary.attributes(quay_self_ad2e9d4)['titlebar']

    @_name_boundary.callable_contract({'self': 'quay_self_277fd3f', 'x': 'quay_x_73e3f02', 'y': 'quay_y_f6ee124'}, 'handle_mouse')
    def quay_handle_mouse(quay_self_277fd3f, quay_x_73e3f02, quay_y_f6ee124):
        _name_boundary.attributes(quay_self_277fd3f)['last_mouse_event'] = f'M: x={quay_x_73e3f02}, y={quay_y_f6ee124}'
        for quay_handler_908a8b8 in _name_boundary.attributes(quay_self_277fd3f)['mouse_handlers'][::-1]:
            if _name_boundary.attributes(quay_handler_908a8b8)['handle_mouse'](quay_x_73e3f02, quay_y_f6ee124):
                break

    @_name_boundary.callable_contract({'self': 'quay_self_b6f0cb2', 'c': 'quay_c_4a3d951'}, 'handle_key_press')
    def quay_handle_key_press(quay_self_b6f0cb2, quay_c_4a3d951):
        """
        Handle 'important' keys, pass the rest to current active subview

        :param c:
        :return:
        """
        if not _name_boundary.attributes(_name_boundary.attributes(quay_self_b6f0cb2)['active_key_handler'])['draw']:
            _name_boundary.attributes(quay_self_b6f0cb2)['active_key_handler'] = _name_boundary.attributes(quay_self_b6f0cb2)['sidebar']
        if quay_c_4a3d951 == quay_curses.KEY_EXIT or quay_c_4a3d951 == quay_curses.KEY_BACKSPACE:
            raise quay_ExitProgramException
        elif quay_c_4a3d951 == quay_curses.KEY_RESIZE:
            raise quay_RebuildAllException
        if quay_c_4a3d951 == quay_curses.KEY_MOUSE:
            quay___63ca9f7, quay_mx_a1344e7, quay_my_27dc96e, quay___63ca9f7, quay___63ca9f7 = quay_curses.getmouse()
            _name_boundary.attributes(quay_self_b6f0cb2)['handle_mouse'](quay_mx_a1344e7, quay_my_27dc96e)
        elif quay_c_4a3d951 == ord('d'):
            if _name_boundary.attributes(_name_boundary.attributes(quay_self_b6f0cb2)['footerbar'])['show_debug']:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_b6f0cb2)['footerbar'])['show_debug'] = False
            else:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_b6f0cb2)['footerbar'])['show_debug'] = True
        elif quay_c_4a3d951 == 9:
            if _name_boundary.attributes(quay_self_b6f0cb2)['active_key_handler'] == _name_boundary.attributes(quay_self_b6f0cb2)['sidebar']:
                _name_boundary.attributes(quay_self_b6f0cb2)['active_key_handler'] = _name_boundary.attributes(quay_self_b6f0cb2)['mainscreen']
                _name_boundary.attributes(_name_boundary.attributes(quay_self_b6f0cb2)['mainscreen'])['highlighted'] = True
            else:
                _name_boundary.attributes(quay_self_b6f0cb2)['active_key_handler'] = _name_boundary.attributes(quay_self_b6f0cb2)['sidebar']
                _name_boundary.attributes(_name_boundary.attributes(quay_self_b6f0cb2)['mainscreen'])['highlighted'] = False
        elif not _name_boundary.attributes(_name_boundary.attributes(quay_self_b6f0cb2)['active_key_handler'])['handle_key_press'](quay_c_4a3d951):
            for quay_handler_34976af in _name_boundary.attributes(quay_self_b6f0cb2)['key_handlers'][::-1]:
                if _name_boundary.attributes(quay_handler_34976af)['handle_key_press'](quay_c_4a3d951):
                    break

    @_name_boundary.callable_contract({'self': 'quay_self_ef7a944'}, 'program_loop')
    def quay_program_loop(quay_self_ef7a944):
        """
        Main Program Loop.

        1. Get a keypress ("keypress" includes mouse events because curses)
        2. Send the keypress to the handler, which will update object models, etc.
        2.5 Handle any exceptions raised by the keypress event.
        3. Redraw all of the views to update the contents of them.

        :return:
        """
        _name_boundary.attributes(quay_self_ef7a944)['rebuild_all']()
        while True:
            try:
                quay_c_3079e0c = _name_boundary.attributes(quay_self_ef7a944)['stdscr'].getch()
                _name_boundary.attributes(quay_self_ef7a944)['handle_key_press'](quay_c_3079e0c)
                _name_boundary.attributes(quay_self_ef7a944)['redraw_all']()
            except quay_FileBrowserOpenNewFileException:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_ef7a944)['file_browser'])['draw'] = True
                _name_boundary.attributes(quay_self_ef7a944)['handle_present_menu_exception'](False)
                _name_boundary.attributes(quay_self_ef7a944)['active_key_handler'] = _name_boundary.attributes(quay_self_ef7a944)['file_browser']
                _name_boundary.attributes(quay_self_ef7a944)['redraw_all']()
            except quay_RebuildAllException:
                _name_boundary.attributes(quay_self_ef7a944)['rebuild_all']()
            except quay_PresentTitleMenuException:
                _name_boundary.attributes(quay_self_ef7a944)['handle_present_menu_exception'](True)
                try:
                    _name_boundary.attributes(quay_self_ef7a944)['redraw_all']()
                except quay_HelpMenuException:
                    _name_boundary.attributes(quay_self_ef7a944)['handle_present_menu_exception'](False)
                    _name_boundary.attributes(_name_boundary.attributes(quay_self_ef7a944)['help_menu'])['draw'] = True
                    _name_boundary.attributes(quay_self_ef7a944)['active_key_handler'] = _name_boundary.attributes(quay_self_ef7a944)['help_menu']
                    try:
                        _name_boundary.attributes(quay_self_ef7a944)['redraw_all']()
                    except quay_PanicException:
                        _name_boundary.attributes(quay_self_ef7a944)['teardown']()
                        print(quay_PANIC_STRING)
                        exit(1)
            except quay_DestroyTitleMenuException:
                _name_boundary.attributes(quay_self_ef7a944)['handle_present_menu_exception'](False)
                _name_boundary.attributes(quay_self_ef7a944)['redraw_all']()
            except quay_PresentDebugMenuException:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_ef7a944)['debug_menu'])['draw'] = True
                _name_boundary.attributes(quay_self_ef7a944)['active_key_handler'] = _name_boundary.attributes(quay_self_ef7a944)['debug_menu']
                try:
                    _name_boundary.attributes(quay_self_ef7a944)['redraw_all']()
                except quay_PanicException:
                    _name_boundary.attributes(quay_self_ef7a944)['teardown']()
                    print(quay_PANIC_STRING)
                    exit(1)
            except quay_ExitProgramException:
                break
            except KeyboardInterrupt:
                break
            except quay_PanicException:
                _name_boundary.attributes(quay_self_ef7a944)['teardown']()
                print(quay_PANIC_STRING)
                exit(1)
            except Exception as quay_ex_3a051a5:
                _name_boundary.attributes(quay_self_ef7a944)['teardown']()
                raise quay_ex_3a051a5
        _name_boundary.attributes(quay_self_ef7a944)['teardown']()

@_name_boundary.callable_contract({}, 'external_hard_fault_teardown')
def quay_external_hard_fault_teardown():
    """
    Call this from outside of this file wherever the Screen is being loaded from, if it catches an Exception
        (it should never do that, so something went very wrong, and we need to attempt to unfuck the terminal).

    :return:
    """
    quay_curses.echo()
    quay_curses.nocbreak()
    quay_curses.mousemask(0)
    quay_curses.curs_set(1)
    quay_curses.endwin()
_name_boundary.module_contract(globals(), {'KToolScreen': 'quay_ImageQuayScreen', 'ceil': 'quay_ceil', 'Button': 'quay_Button', 'HelpMenuItem': 'quay_HelpMenuItem', 'os': 'quay_os', 'ATTR_STRING_DEBUG': 'quay_ATTR_STRING_DEBUG', 'SidebarMenuItem': 'quay_SidebarMenuItem', 'HeaderGenerator': 'quay_HeaderGenerator', 'Table': 'quay_Table', 'pprint': 'quay_pprint', 'MainMenuContentItem': 'quay_MainMenuContentItem', 'KToolKernelCacheLoader': 'quay_ImageQuayKernelCacheLoader', 'external_hard_fault_teardown': 'quay_external_hard_fault_teardown', 'PresentTitleMenuException': 'quay_PresentTitleMenuException', 'MAIN_TEXT': 'quay_MAIN_TEXT', 'DebugMenu': 'quay_DebugMenu', 'View': 'quay_View', 'EditMenuItem': 'quay_EditMenuItem', 'ExitProgramException': 'quay_ExitProgramException', 'ColorRep': 'quay_ColorRep', 'SIDEBAR_WIDTH': 'quay_SIDEBAR_WIDTH', 'LazilyProcessedTextBuffer': 'quay_LazilyProcessedTextBuffer', 'AttributedString': 'quay_AttributedString', 'MainScreen': 'quay_MainScreen', 'KToolMachOLoader': 'quay_ImageQuayMachOLoader', 'DestroyTitleMenuException': 'quay_DestroyTitleMenuException', 'FooterBar': 'quay_FooterBar', 'DumpMenuItem': 'quay_DumpMenuItem', 'highlight': 'quay_highlight', 'Terminal256Formatter': 'quay_Terminal256Formatter', 'PanicException': 'quay_PanicException', 'UserInputPrompt': 'quay_UserInputPrompt', 'RootBox': 'quay_RootBox', 'MachOImageLoader': 'quay_MachOImageLoader', 'curses': 'quay_curses', 'FileSystemBrowserOverlayView': 'quay_FileSystemBrowserOverlayView', 'TitleBarMenuItem': 'quay_TitleBarMenuItem', 'ObjectiveCLexer': 'quay_ObjectiveCLexer', 'LOAD_COMMAND': 'quay_LOAD_COMMAND', 'Attribute': 'quay_Attribute', 'TitleBar': 'quay_TitleBar', 'HexDumpTable': 'quay_HexDumpTable', 'Sidebar': 'quay_Sidebar', 'ktool': 'quay_imagequay', 'ScrollView': 'quay_ScrollView', 'MenuOverlayRenderingView': 'quay_MenuOverlayRenderingView', 'KernelCache': 'quay_KernelCache', 'Kext': 'quay_Kext', 'BOX_CHARS': 'quay_BOX_CHARS', 'RebuildAllException': 'quay_RebuildAllException', 'WINDOW_NAME': 'quay_WINDOW_NAME', 'ObjCImage': 'quay_ObjCImage', 'SwiftClass': 'quay_SwiftClass', 'FileBrowserOpenNewFileException': 'quay_FileBrowserOpenNewFileException', 'FileMenuItem': 'quay_FileMenuItem', 'HelpMenu': 'quay_HelpMenu', 'TerminalFormatter': 'quay_TerminalFormatter', 'PANIC_STRING': 'quay_PANIC_STRING', 'panic': 'quay_panic', 'Box': 'quay_Box', 'LoaderStatusView': 'quay_LoaderStatusView', 'MachOFile': 'quay_MachOFile', 'VERT_LINE': 'quay_VERT_LINE', 'PresentDebugMenuException': 'quay_PresentDebugMenuException', 'ScrollingDisplayBuffer': 'quay_ScrollingDisplayBuffer', 'HelpMenuException': 'quay_HelpMenuException', 'datetime': 'quay_datetime'})
