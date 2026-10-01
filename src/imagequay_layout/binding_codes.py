# Derived from src/ktool_macho/binding.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool_macho
#  macho.py
#
#  This file contains pythonized representations of certain #defines and enums from dyld source
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary
from enum import IntEnum as quay_IntEnum

@_name_boundary.class_contract('REBASE_OPCODE', {})
class quay_REBASE_OPCODE(quay_IntEnum):
    DONE = 0
    SET_TYPE_IMM = 16
    SET_SEGMENT_AND_OFFSET_ULEB = 32
    ADD_ADDR_ULEB = 48
    ADD_ADDR_IMM_SCALED = 64
    DO_REBASE_IMM_TIMES = 80
    DO_REBASE_ULEB_TIMES = 96
    DO_REBASE_ADD_ADDR_ULEB = 112
    DO_REBASE_ULEB_TIMES_SKIPPING_ULEB = 128

@_name_boundary.class_contract('BINDING_OPCODE', {})
class quay_BINDING_OPCODE(quay_IntEnum):
    DONE = 0
    SET_DYLIB_ORDINAL_IMM = 16
    SET_DYLIB_ORDINAL_ULEB = 32
    SET_DYLIB_SPECIAL_IMM = 48
    SET_SYMBOL_TRAILING_FLAGS_IMM = 64
    SET_TYPE_IMM = 80
    SET_ADDEND_SLEB = 96
    SET_SEGMENT_AND_OFFSET_ULEB = 112
    ADD_ADDR_ULEB = 128
    DO_BIND = 144
    DO_BIND_ADD_ADDR_ULEB = 160
    DO_BIND_ADD_ADDR_IMM_SCALED = 176
    DO_BIND_ULEB_TIMES_SKIPPING_ULEB = 192
    THREADED = 208
quay_BIND_SUBOPCODE_THREADED_SET_BIND_ORDINAL_TABLE_SIZE_ULEB = 0
quay_BIND_SUBOPCODE_THREADED_APPLY = 1
_name_boundary.module_contract(globals(), {'BINDING_OPCODE': 'quay_BINDING_OPCODE', 'BIND_SUBOPCODE_THREADED_APPLY': 'quay_BIND_SUBOPCODE_THREADED_APPLY', 'IntEnum': 'quay_IntEnum', 'REBASE_OPCODE': 'quay_REBASE_OPCODE', 'BIND_SUBOPCODE_THREADED_SET_BIND_ORDINAL_TABLE_SIZE_ULEB': 'quay_BIND_SUBOPCODE_THREADED_SET_BIND_ORDINAL_TABLE_SIZE_ULEB'})
