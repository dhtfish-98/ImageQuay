# Derived from src/lib0cyn/log.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | lib0cyn
#  log.py
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
from enum import Enum as quay_Enum
import sys as quay_sys
import inspect as quay_inspect
import os as quay_os
from imagequay_support.record_engine import quay_Struct as quay_Struct

@_name_boundary.class_contract('LogLevel', {})
class quay_LogLevel(quay_Enum):
    NONE = -1
    ERROR = 0
    WARN = 1
    INFO = 2
    DEBUG = 3
    DEBUG_MORE = 4
    DEBUG_TOO_MUCH = 5

@_name_boundary.callable_contract({'msg': 'quay_msg_f90f46b'}, 'print_err')
def quay_print_err(quay_msg_f90f46b):
    print(quay_msg_f90f46b, file=quay_sys.stderr)

@_name_boundary.class_contract('log', {'LOG_LEVEL': 'quay_LOG_LEVEL', 'LOG_FUNC': 'quay_LOG_FUNC', 'LOG_ERR': 'quay_LOG_ERR', 'get_class_from_frame': 'quay_get_class_from_frame', 'line': 'quay_line', 'debug': 'quay_debug', 'debug_more': 'quay_debug_more', 'debug_tm': 'quay_debug_tm', 'info': 'quay_info', 'warn': 'quay_warn', 'warning': 'quay_warning', 'error': 'quay_error'})
class quay_log:
    """
    Python's default logging image is absolute garbage

    so we use this.
    """
    quay_LOG_LEVEL = quay_LogLevel.ERROR
    quay_LOG_FUNC = print
    quay_LOG_ERR = quay_print_err

    @staticmethod
    @_name_boundary.callable_contract({'fr': 'quay_fr_baf3594'}, 'get_class_from_frame')
    def quay_get_class_from_frame(quay_fr_baf3594):
        return _name_boundary.frame_class(quay_fr_baf3594)

    @staticmethod
    @_name_boundary.callable_contract({}, 'line')
    def quay_line():
        quay_application_frames = _name_boundary.application_frames()
        quay_stack_frame = quay_application_frames[2]
        quay_source_label = quay_os.path.basename(quay_stack_frame.filename).split('.')[0]
        quay_line_label = f'L#{quay_stack_frame.lineno}'
        quay_caller_class = _name_boundary.frame_class(quay_stack_frame)
        quay_caller_label = (quay_caller_class + ':' if quay_caller_class is not None else '') + quay_stack_frame.function
        return 'imagequay.' + quay_source_label + ':' + quay_line_label + ':' + quay_caller_label + '()'

    @staticmethod
    @_name_boundary.callable_contract({'msg': 'quay_msg_94d9877'}, 'debug')
    def quay_debug(quay_msg_94d9877=''):
        if _name_boundary.attributes(_name_boundary.attributes(quay_log)['LOG_LEVEL'])['value'] >= _name_boundary.attributes(quay_LogLevel.DEBUG)['value']:
            if issubclass(quay_msg_94d9877.__class__, quay_Struct):
                quay_msg_94d9877 = str(quay_msg_94d9877)
            _name_boundary.attributes(quay_log)['LOG_FUNC'](f"DEBUG - {_name_boundary.attributes(quay_log)['line']()} - {quay_msg_94d9877}")

    @staticmethod
    @_name_boundary.callable_contract({'msg': 'quay_msg_e95c5b5'}, 'debug_more')
    def quay_debug_more(quay_msg_e95c5b5: str=''):
        if _name_boundary.attributes(_name_boundary.attributes(quay_log)['LOG_LEVEL'])['value'] >= _name_boundary.attributes(quay_LogLevel.DEBUG_MORE)['value']:
            if issubclass(quay_msg_e95c5b5.__class__, quay_Struct):
                quay_msg_e95c5b5 = str(quay_msg_e95c5b5)
            _name_boundary.attributes(quay_log)['LOG_FUNC'](f"DEBUG-2 - {_name_boundary.attributes(quay_log)['line']()} - {quay_msg_e95c5b5}")

    @staticmethod
    @_name_boundary.callable_contract({'msg': 'quay_msg_4510289'}, 'debug_tm')
    def quay_debug_tm(quay_msg_4510289: str=''):
        if _name_boundary.attributes(_name_boundary.attributes(quay_log)['LOG_LEVEL'])['value'] >= _name_boundary.attributes(quay_LogLevel.DEBUG_TOO_MUCH)['value']:
            if issubclass(quay_msg_4510289.__class__, quay_Struct):
                quay_msg_4510289 = str(quay_msg_4510289)
            _name_boundary.attributes(quay_log)['LOG_FUNC'](f"DEBUG-3 - {_name_boundary.attributes(quay_log)['line']()} - {quay_msg_4510289}")

    @staticmethod
    @_name_boundary.callable_contract({'msg': 'quay_msg_25dd33f'}, 'info')
    def quay_info(quay_msg_25dd33f: str=''):
        if _name_boundary.attributes(_name_boundary.attributes(quay_log)['LOG_LEVEL'])['value'] >= _name_boundary.attributes(quay_LogLevel.INFO)['value']:
            if issubclass(quay_msg_25dd33f.__class__, quay_Struct):
                quay_msg_25dd33f = str(quay_msg_25dd33f)
            _name_boundary.attributes(quay_log)['LOG_FUNC'](f"INFO - {_name_boundary.attributes(quay_log)['line']()} - {quay_msg_25dd33f}")

    @staticmethod
    @_name_boundary.callable_contract({'msg': 'quay_msg_07076d8'}, 'warn')
    def quay_warn(quay_msg_07076d8: str=''):
        if _name_boundary.attributes(_name_boundary.attributes(quay_log)['LOG_LEVEL'])['value'] >= _name_boundary.attributes(quay_LogLevel.WARN)['value']:
            if issubclass(quay_msg_07076d8.__class__, quay_Struct):
                quay_msg_07076d8 = str(quay_msg_07076d8)
            _name_boundary.attributes(quay_log)['LOG_ERR'](f"WARN - {_name_boundary.attributes(quay_log)['line']()} - {quay_msg_07076d8}")

    @staticmethod
    @_name_boundary.callable_contract({'msg': 'quay_msg_ee9a6e2'}, 'warning')
    def quay_warning(quay_msg_ee9a6e2: str=''):
        if _name_boundary.attributes(_name_boundary.attributes(quay_log)['LOG_LEVEL'])['value'] >= _name_boundary.attributes(quay_LogLevel.WARN)['value']:
            if issubclass(quay_msg_ee9a6e2.__class__, quay_Struct):
                quay_msg_ee9a6e2 = str(quay_msg_ee9a6e2)
            _name_boundary.attributes(quay_log)['LOG_ERR'](f"WARN - {_name_boundary.attributes(quay_log)['line']()} - {quay_msg_ee9a6e2}")

    @staticmethod
    @_name_boundary.callable_contract({'msg': 'quay_msg_7dbe1d5'}, 'error')
    def quay_error(quay_msg_7dbe1d5: str=''):
        if _name_boundary.attributes(_name_boundary.attributes(quay_log)['LOG_LEVEL'])['value'] >= _name_boundary.attributes(quay_LogLevel.ERROR)['value']:
            if issubclass(quay_msg_7dbe1d5.__class__, quay_Struct):
                quay_msg_7dbe1d5 = str(quay_msg_7dbe1d5)
            _name_boundary.attributes(quay_log)['LOG_ERR'](f"ERROR - {_name_boundary.attributes(quay_log)['line']()} - {quay_msg_7dbe1d5}")
_name_boundary.module_contract(globals(), {'log': 'quay_log', 'LogLevel': 'quay_LogLevel', 'os': 'quay_os', 'print_err': 'quay_print_err', 'sys': 'quay_sys', 'Struct': 'quay_Struct', 'Enum': 'quay_Enum', 'inspect': 'quay_inspect'})
