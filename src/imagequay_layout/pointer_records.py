# Derived from src/ktool_macho/fixups.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool_macho
#  fixups.py
#
#
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary
from enum import Enum as quay_Enum
from imagequay_layout.binary_records import *

@_name_boundary.class_contract('dyld_chained_fixups_header', {'_FIELDNAMES': 'quay__FIELDNAMES', '_SIZES': 'quay__SIZES', 'SIZE': 'quay_SIZE', 'fixups_version': 'quay_fixups_version', 'starts_offset': 'quay_starts_offset', 'imports_offset': 'quay_imports_offset', 'symbols_offset': 'quay_symbols_offset', 'imports_count': 'quay_imports_count', 'imports_format': 'quay_imports_format', 'symbols_format': 'quay_symbols_format'})
class quay_dyld_chained_fixups_header(quay_Struct):
    quay__FIELDNAMES = ['fixups_version', 'starts_offset', 'imports_offset', 'symbols_offset', 'imports_count', 'imports_format', 'symbols_format']
    quay__SIZES = [4, 4, 4, 4, 4, 4, 4]
    quay_SIZE = sum(quay__SIZES)

    @_name_boundary.callable_contract({'self': 'quay_self_e4b0153', 'byte_order': 'quay_byte_order_86a33c3'}, '__init__')
    def __init__(quay_self_e4b0153, quay_byte_order_86a33c3='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_e4b0153)['_FIELDNAMES'], sizes=_name_boundary.attributes(quay_self_e4b0153)['_SIZES'], byte_order=quay_byte_order_86a33c3)

@_name_boundary.class_contract('dyld_chained_starts_in_image', {'_FIELDNAMES': 'quay__FIELDNAMES', '_SIZES': 'quay__SIZES', 'SIZE': 'quay_SIZE', 'seg_count': 'quay_seg_count', 'seg_info_offset': 'quay_seg_info_offset'})
class quay_dyld_chained_starts_in_image(quay_Struct):
    quay__FIELDNAMES = ['seg_count', 'seg_info_offset']
    quay__SIZES = [4, 4]
    quay_SIZE = sum(quay__SIZES)

    @_name_boundary.callable_contract({'self': 'quay_self_3fcfeb5', 'byte_order': 'quay_byte_order_9c0e976'}, '__init__')
    def __init__(quay_self_3fcfeb5, quay_byte_order_9c0e976='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_3fcfeb5)['_FIELDNAMES'], sizes=_name_boundary.attributes(quay_self_3fcfeb5)['_SIZES'], byte_order=quay_byte_order_9c0e976)

@_name_boundary.class_contract('dyld_chained_starts_in_segment', {'_FIELDNAMES': 'quay__FIELDNAMES', '_SIZES': 'quay__SIZES', 'SIZE': 'quay_SIZE', 'size': 'quay_size', 'page_size': 'quay_page_size', 'pointer_format': 'quay_pointer_format', 'segment_offset': 'quay_segment_offset', 'max_valid_pointer': 'quay_max_valid_pointer', 'page_count': 'quay_page_count', 'page_starts': 'quay_page_starts'})
class quay_dyld_chained_starts_in_segment(quay_Struct):
    quay__FIELDNAMES = ['size', 'page_size', 'pointer_format', 'segment_offset', 'max_valid_pointer', 'page_count', 'page_starts']
    quay__SIZES = [4, 2, 2, 8, 4, 2, 2]
    quay_SIZE = sum(quay__SIZES)

    @_name_boundary.callable_contract({'self': 'quay_self_a20ce94', 'byte_order': 'quay_byte_order_ff2686e'}, '__init__')
    def __init__(quay_self_a20ce94, quay_byte_order_ff2686e='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_a20ce94)['_FIELDNAMES'], sizes=_name_boundary.attributes(quay_self_a20ce94)['_SIZES'], byte_order=quay_byte_order_ff2686e)
quay_DYLD_CHAINED_PTR_START_NONE = 65535
quay_DYLD_CHAINED_PTR_START_MULTI = 32768
quay_DYLD_CHAINED_PTR_START_LAST = 32768

@_name_boundary.class_contract('dyld_chained_start_offsets', {'_FIELDNAMES': 'quay__FIELDNAMES', '_SIZES': 'quay__SIZES', 'SIZE': 'quay_SIZE', 'pointer_format': 'quay_pointer_format', 'starts_count': 'quay_starts_count', 'chain_starts': 'quay_chain_starts'})
class quay_dyld_chained_start_offsets(quay_Struct):
    quay__FIELDNAMES = ['pointer_format', 'starts_count', 'chain_starts']
    quay__SIZES = [4, 4, 4]
    quay_SIZE = sum(quay__SIZES)

    @_name_boundary.callable_contract({'self': 'quay_self_816fcdd', 'byte_order': 'quay_byte_order_c7a2d94'}, '__init__')
    def __init__(quay_self_816fcdd, quay_byte_order_c7a2d94='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_816fcdd)['_FIELDNAMES'], sizes=_name_boundary.attributes(quay_self_816fcdd)['_SIZES'], byte_order=quay_byte_order_c7a2d94)
"\nenum {\n    DYLD_CHAINED_PTR_ARM64E                 =  1,    // stride 8, unauth target is vmaddr\n    DYLD_CHAINED_PTR_64                     =  2,    // target is vmaddr\n    DYLD_CHAINED_PTR_32                     =  3,\n    DYLD_CHAINED_PTR_32_CACHE               =  4,\n    DYLD_CHAINED_PTR_32_FIRMWARE            =  5,\n    DYLD_CHAINED_PTR_64_OFFSET              =  6,    // target is vm offset\n    DYLD_CHAINED_PTR_ARM64E_OFFSET          =  7,    // old name\n    DYLD_CHAINED_PTR_ARM64E_KERNEL          =  7,    // stride 4, unauth target is vm offset\n    DYLD_CHAINED_PTR_64_KERNEL_CACHE        =  8,\n    DYLD_CHAINED_PTR_ARM64E_USERLAND        =  9,    // stride 8, unauth target is vm offset\n    DYLD_CHAINED_PTR_ARM64E_FIRMWARE        = 10,    // stride 4, unauth target is vmaddr\n    DYLD_CHAINED_PTR_X86_64_KERNEL_CACHE    = 11,    // stride 1, x86_64 kernel caches\n    there is apparently a 12. it is not in xnu source. i found it in an arm64e userland (Console.app M1) bin, so we're assuming its\n                                                        like, 1 I guess. \n};"

@_name_boundary.class_contract('dyld_chained_ptr_format', {})
class quay_dyld_chained_ptr_format(quay_Enum):
    DYLD_CHAINED_PTR_ARM64E = 1
    DYLD_CHAINED_PTR_64 = 2
    DYLD_CHAINED_PTR_32 = 3
    DYLD_CHAINED_PTR_32_CACHE = 4
    DYLD_CHAINED_PTR_32_FIRMWARE = 5
    DYLD_CHAINED_PTR_64_OFFSET = 6
    DYLD_CHAINED_PTR_ARM64E_OFFSET = 7
    DYLD_CHAINED_PTR_ARM64E_KERNEL = 7
    DYLD_CHAINED_PTR_64_KERNEL_CACHE = 8
    DYLD_CHAINED_PTR_ARM64E_USERLAND = 9
    DYLD_CHAINED_PTR_ARM64E_FIRMWARE = 10
    DYLD_CHAINED_PTR_x86_64_KERNEL_CACHE = 11
    DYLD_CHAINED_PTR_ARM64E_USERLAND24 = 12

@_name_boundary.class_contract('dyld_chained_import_format', {})
class quay_dyld_chained_import_format(quay_Enum):
    DYLD_CHAINED_IMPORT = 1
    DYLD_CHAINED_IMPORT_ADDEND = 2
    DYLD_CHAINED_IMPORT_ADDEND64 = 3

@_name_boundary.class_contract('ChainedFixupPointerGeneric', {})
class quay_ChainedFixupPointerGeneric(quay_Enum):
    GenericArm64eFixupFormat = 0
    Generic64FixupFormat = 1
    Generic32FixupFormat = 2
    Firmware32FixupFormat = 3
    Kernel64FixupFormat = 4
    Error = 5

@_name_boundary.class_contract('dyld_chained_import', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'lib_ordinal': 'quay_lib_ordinal', 'weak_import': 'quay_weak_import', 'name_offset': 'quay_name_offset'})
class quay_dyld_chained_import(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'lib_ordinal': 8, 'weak_import': 1, 'name_offset': 23})}
    quay_SIZE = quay_uint32_t

    @_name_boundary.callable_contract({'self': 'quay_self_c4b8bb7', 'byte_order': 'quay_byte_order_ad4d5ff'}, '__init__')
    def __init__(quay_self_c4b8bb7, quay_byte_order_ad4d5ff='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_c4b8bb7)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_c4b8bb7)['_FIELDS'].values(), byte_order=quay_byte_order_ad4d5ff)

@_name_boundary.class_contract('dyld_chained_import_addend', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'addend': 'quay_addend', 'lib_ordinal': 'quay_lib_ordinal', 'weak_import': 'quay_weak_import', 'name_offset': 'quay_name_offset'})
class quay_dyld_chained_import_addend(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'lib_ordinal': 8, 'weak_import': 1, 'name_offset': 23}), 'addend': quay_int32_t}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_071ff7f', 'byte_order': 'quay_byte_order_6fd5ee6'}, '__init__')
    def __init__(quay_self_071ff7f, quay_byte_order_6fd5ee6='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_071ff7f)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_071ff7f)['_FIELDS'].values(), byte_order=quay_byte_order_6fd5ee6)

@_name_boundary.class_contract('dyld_chained_import_addend64', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'addend': 'quay_addend', 'lib_ordinal': 'quay_lib_ordinal', 'weak_import': 'quay_weak_import', 'reserved': 'quay_reserved', 'name_offset': 'quay_name_offset'})
class quay_dyld_chained_import_addend64(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'lib_ordinal': 16, 'weak_import': 1, 'reserved': 15, 'name_offset': 32}), 'addend': quay_uint64_t}
    quay_SIZE = 16

    @_name_boundary.callable_contract({'self': 'quay_self_83cf679', 'byte_order': 'quay_byte_order_20d455f'}, '__init__')
    def __init__(quay_self_83cf679, quay_byte_order_20d455f='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_83cf679)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_83cf679)['_FIELDS'].values(), byte_order=quay_byte_order_20d455f)

@_name_boundary.class_contract('dyld_chained_ptr', {'_FIELDNAMES': 'quay__FIELDNAMES', '_SIZES': 'quay__SIZES', 'SIZE': 'quay_SIZE', 'ptr': 'quay_ptr'})
class quay_dyld_chained_ptr(quay_Struct):
    quay__FIELDNAMES = ['ptr']
    quay__SIZES = [8]
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_f74fef7', 'byte_order': 'quay_byte_order_f035216'}, '__init__')
    def __init__(quay_self_f74fef7, quay_byte_order_f035216='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_f74fef7)['_FIELDNAMES'], sizes=_name_boundary.attributes(quay_self_f74fef7)['_SIZES'], byte_order=quay_byte_order_f035216)

@_name_boundary.class_contract('dyld_chained_ptr_arm64e', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'bind': 'quay_bind', 'auth': 'quay_auth', 'reserved': 'quay_reserved'})
class quay_dyld_chained_ptr_arm64e(quay_Struct):
    quay__FIELDS = {'reserved': quay_Bitfield({'reserved': 62, 'bind': 1, 'auth': 1})}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_5d08f4c', 'byte_order': 'quay_byte_order_0d9eeb0'}, '__init__')
    def __init__(quay_self_5d08f4c, quay_byte_order_0d9eeb0='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_5d08f4c)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_5d08f4c)['_FIELDS'].values(), byte_order=quay_byte_order_0d9eeb0)
        _name_boundary.attributes(quay_self_5d08f4c)['bind'] = 0
        _name_boundary.attributes(quay_self_5d08f4c)['auth'] = 0

@_name_boundary.class_contract('dyld_chained_ptr_arm64e_rebase', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'target': 'quay_target', 'high8': 'quay_high8', 'next': 'quay_next', 'bind': 'quay_bind', 'auth': 'quay_auth'})
class quay_dyld_chained_ptr_arm64e_rebase(quay_Struct):
    quay__FIELDS = {'target': quay_Bitfield({'target': 43, 'high8': 8, 'next': 11, 'bind': 1, 'auth': 1})}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_c65b0af', 'byte_order': 'quay_byte_order_049e8b9'}, '__init__')
    def __init__(quay_self_c65b0af, quay_byte_order_049e8b9='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_c65b0af)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_c65b0af)['_FIELDS'].values(), byte_order=quay_byte_order_049e8b9)

@_name_boundary.class_contract('dyld_chained_ptr_arm64e_bind', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'ordinal': 'quay_ordinal', 'zero': 'quay_zero', 'addend': 'quay_addend', 'next': 'quay_next', 'bind': 'quay_bind', 'auth': 'quay_auth'})
class quay_dyld_chained_ptr_arm64e_bind(quay_Struct):
    quay__FIELDS = {'ordinal': quay_Bitfield({'ordinal': 16, 'zero': 16, 'addend': 19, 'next': 11, 'bind': 1, 'auth': 1})}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_0bae988', 'byte_order': 'quay_byte_order_2cc0754'}, '__init__')
    def __init__(quay_self_0bae988, quay_byte_order_2cc0754='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_0bae988)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_0bae988)['_FIELDS'].values(), byte_order=quay_byte_order_2cc0754)

@_name_boundary.class_contract('dyld_chained_ptr_arm64e_auth_rebase', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'target': 'quay_target', 'diversity': 'quay_diversity', 'addrDiv': 'quay_addrDiv', 'key': 'quay_key', 'next': 'quay_next', 'bind': 'quay_bind', 'auth': 'quay_auth'})
class quay_dyld_chained_ptr_arm64e_auth_rebase(quay_Struct):
    quay__FIELDS = {'target': quay_Bitfield({'target': 32, 'diversity': 16, 'addrDiv': 1, 'key': 2, 'next': 11, 'bind': 1, 'auth': 1})}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_9523bf3', 'byte_order': 'quay_byte_order_21e5ff5'}, '__init__')
    def __init__(quay_self_9523bf3, quay_byte_order_21e5ff5='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_9523bf3)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_9523bf3)['_FIELDS'].values(), byte_order=quay_byte_order_21e5ff5)

@_name_boundary.class_contract('dyld_chained_ptr_arm64e_auth_bind', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'ordinal': 'quay_ordinal', 'zero': 'quay_zero', 'diversity': 'quay_diversity', 'addrDiv': 'quay_addrDiv', 'key': 'quay_key', 'next': 'quay_next', 'bind': 'quay_bind', 'auth': 'quay_auth'})
class quay_dyld_chained_ptr_arm64e_auth_bind(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'ordinal': 16, 'zero': 16, 'diversity': 16, 'addrDiv': 1, 'key': 2, 'next': 11, 'bind': 1, 'auth': 1})}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_411e4b2', 'byte_order': 'quay_byte_order_266e0ed'}, '__init__')
    def __init__(quay_self_411e4b2, quay_byte_order_266e0ed='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_411e4b2)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_411e4b2)['_FIELDS'].values(), byte_order=quay_byte_order_266e0ed)

@_name_boundary.class_contract('dyld_chained_ptr_64', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'reserved': 'quay_reserved', 'bind': 'quay_bind'})
class quay_dyld_chained_ptr_64(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'reserved': 63, 'bind': 1})}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_2bb5317', 'byte_order': 'quay_byte_order_6954d38'}, '__init__')
    def __init__(quay_self_2bb5317, quay_byte_order_6954d38='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_2bb5317)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_2bb5317)['_FIELDS'].values(), byte_order=quay_byte_order_6954d38)

@_name_boundary.class_contract('dyld_chained_ptr_64_rebase', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'target': 'quay_target', 'high8': 'quay_high8', 'reserved': 'quay_reserved', 'next': 'quay_next', 'bind': 'quay_bind'})
class quay_dyld_chained_ptr_64_rebase(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'target': 36, 'high8': 8, 'reserved': 7, 'next': 12, 'bind': 1})}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_7e31782', 'byte_order': 'quay_byte_order_d3ec287'}, '__init__')
    def __init__(quay_self_7e31782, quay_byte_order_d3ec287='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_7e31782)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_7e31782)['_FIELDS'].values(), byte_order=quay_byte_order_d3ec287)

@_name_boundary.class_contract('dyld_chained_ptr_64_bind', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'ordinal': 'quay_ordinal', 'addend': 'quay_addend', 'reserved': 'quay_reserved', 'next': 'quay_next', 'bind': 'quay_bind'})
class quay_dyld_chained_ptr_64_bind(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'ordinal': 24, 'addend': 8, 'reserved': 19, 'next': 12, 'bind': 1})}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_bd98b7a', 'byte_order': 'quay_byte_order_3fb94ba'}, '__init__')
    def __init__(quay_self_bd98b7a, quay_byte_order_3fb94ba='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_bd98b7a)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_bd98b7a)['_FIELDS'].values(), byte_order=quay_byte_order_3fb94ba)

@_name_boundary.class_contract('dyld_chained_ptr_arm64e_bind24', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'ordinal': 'quay_ordinal', 'zero': 'quay_zero', 'addend': 'quay_addend', 'next': 'quay_next', 'bind': 'quay_bind', 'auth': 'quay_auth'})
class quay_dyld_chained_ptr_arm64e_bind24(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'ordinal': 24, 'zero': 8, 'addend': 19, 'next': 11, 'bind': 1, 'auth': 1})}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_a22a6f7', 'byte_order': 'quay_byte_order_8c68280'}, '__init__')
    def __init__(quay_self_a22a6f7, quay_byte_order_8c68280='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_a22a6f7)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_a22a6f7)['_FIELDS'].values(), byte_order=quay_byte_order_8c68280)

@_name_boundary.class_contract('dyld_chained_ptr_arm64e_auth_bind24', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'ordinal': 'quay_ordinal', 'zero': 'quay_zero', 'diversity': 'quay_diversity', 'addrDiv': 'quay_addrDiv', 'key': 'quay_key', 'next': 'quay_next', 'bind': 'quay_bind', 'auth': 'quay_auth'})
class quay_dyld_chained_ptr_arm64e_auth_bind24(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'ordinal': 24, 'zero': 8, 'diversity': 16, 'addrDiv': 1, 'key': 2, 'next': 11, 'bind': 1, 'auth': 1})}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_1d2395c', 'byte_order': 'quay_byte_order_1821ed6'}, '__init__')
    def __init__(quay_self_1d2395c, quay_byte_order_1821ed6='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_1d2395c)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_1d2395c)['_FIELDS'].values(), byte_order=quay_byte_order_1821ed6)

@_name_boundary.class_contract('dyld_chained_ptr_32_rebase', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'target': 'quay_target', 'next': 'quay_next', 'bind': 'quay_bind'})
class quay_dyld_chained_ptr_32_rebase(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'target': 26, 'next': 5, 'bind': 1})}
    quay_SIZE = 4

    @_name_boundary.callable_contract({'self': 'quay_self_d65f97a', 'byte_order': 'quay_byte_order_fd29a01'}, '__init__')
    def __init__(quay_self_d65f97a, quay_byte_order_fd29a01='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_d65f97a)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_d65f97a)['_FIELDS'].values(), byte_order=quay_byte_order_fd29a01)

@_name_boundary.class_contract('dyld_chained_ptr_32_bind', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'ordinal': 'quay_ordinal', 'addend': 'quay_addend', 'next': 'quay_next', 'bind': 'quay_bind'})
class quay_dyld_chained_ptr_32_bind(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'ordinal': 20, 'addend': 6, 'next': 5, 'bind': 1})}
    quay_SIZE = 4

    @_name_boundary.callable_contract({'self': 'quay_self_0ad619d', 'byte_order': 'quay_byte_order_9a90640'}, '__init__')
    def __init__(quay_self_0ad619d, quay_byte_order_9a90640='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_0ad619d)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_0ad619d)['_FIELDS'].values(), byte_order=quay_byte_order_9a90640)

@_name_boundary.class_contract('dyld_chained_ptr_32_cache_rebase', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'target': 'quay_target', 'next': 'quay_next'})
class quay_dyld_chained_ptr_32_cache_rebase(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'target': 30, 'next': 2})}
    quay_SIZE = 4

    @_name_boundary.callable_contract({'self': 'quay_self_be6dcd4', 'byte_order': 'quay_byte_order_dfe7feb'}, '__init__')
    def __init__(quay_self_be6dcd4, quay_byte_order_dfe7feb='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_be6dcd4)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_be6dcd4)['_FIELDS'].values(), byte_order=quay_byte_order_dfe7feb)

@_name_boundary.class_contract('dyld_chained_ptr_32_firmware_rebase', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'target': 'quay_target', 'next': 'quay_next'})
class quay_dyld_chained_ptr_32_firmware_rebase(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'target': 26, 'next': 6})}
    quay_SIZE = 4

    @_name_boundary.callable_contract({'self': 'quay_self_8ad722f', 'byte_order': 'quay_byte_order_b95263b'}, '__init__')
    def __init__(quay_self_8ad722f, quay_byte_order_b95263b='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_8ad722f)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_8ad722f)['_FIELDS'].values(), byte_order=quay_byte_order_b95263b)

@_name_boundary.class_contract('ChainedPointerArm64E', {'SIZE': 'quay_SIZE'})
class quay_ChainedPointerArm64E(quay_StructUnion):
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_b3ec558'}, '__init__')
    def __init__(quay_self_b3ec558):
        super().__init__(quay_uint64_t, [quay_dyld_chained_ptr_arm64e_auth_rebase, quay_dyld_chained_ptr_arm64e_auth_bind, quay_dyld_chained_ptr_arm64e_rebase, quay_dyld_chained_ptr_arm64e_bind, quay_dyld_chained_ptr_arm64e_bind24, quay_dyld_chained_ptr_arm64e_auth_bind24])

@_name_boundary.class_contract('ChainedPointerGeneric64', {'SIZE': 'quay_SIZE'})
class quay_ChainedPointerGeneric64(quay_StructUnion):
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_0302cb5'}, '__init__')
    def __init__(quay_self_0302cb5):
        super().__init__(quay_uint64_t, [quay_dyld_chained_ptr_64_rebase, quay_dyld_chained_ptr_64_bind])

@_name_boundary.class_contract('ChainedPointerGeneric32', {'SIZE': 'quay_SIZE'})
class quay_ChainedPointerGeneric32(quay_StructUnion):
    quay_SIZE = 4

    @_name_boundary.callable_contract({'self': 'quay_self_71fe0e0'}, '__init__')
    def __init__(quay_self_71fe0e0):
        super().__init__(quay_uint32_t, [quay_dyld_chained_ptr_32_rebase, quay_dyld_chained_ptr_32_bind, quay_dyld_chained_ptr_32_firmware_rebase])

@_name_boundary.class_contract('ChainedFixupPointer64Union', {'SIZE': 'quay_SIZE'})
class quay_ChainedFixupPointer64Union(quay_StructUnion):
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_da35c91'}, '__init__')
    def __init__(quay_self_da35c91):
        super().__init__(quay_uint64_t, [quay_ChainedPointerArm64E, quay_ChainedPointerGeneric64])

@_name_boundary.class_contract('ChainedFixupPointer32', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'generic32': 'quay_generic32'})
class quay_ChainedFixupPointer32(quay_Struct):
    quay__FIELDS = {'generic32': quay_ChainedPointerGeneric32}
    quay_SIZE = 4

    @_name_boundary.callable_contract({'self': 'quay_self_a487a4a', 'byte_order': 'quay_byte_order_2f90bd3'}, '__init__')
    def __init__(quay_self_a487a4a, quay_byte_order_2f90bd3='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_a487a4a)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_a487a4a)['_FIELDS'].values(), byte_order=quay_byte_order_2f90bd3)

@_name_boundary.class_contract('ChainedFixupPointer64', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'generic64': 'quay_generic64'})
class quay_ChainedFixupPointer64(quay_Struct):
    quay__FIELDS = {'generic64': quay_ChainedFixupPointer64Union}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_d24f526', 'byte_order': 'quay_byte_order_79c5881'}, '__init__')
    def __init__(quay_self_d24f526, quay_byte_order_79c5881='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_d24f526)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_d24f526)['_FIELDS'].values(), byte_order=quay_byte_order_79c5881)

@_name_boundary.class_contract('ChainedFixupKernel64', {'_FIELDS': 'quay__FIELDS', 'SIZE': 'quay_SIZE', 'value': 'quay_value', 'target': 'quay_target', 'cacheLevel': 'quay_cacheLevel', 'diversity': 'quay_diversity', 'addrDiv': 'quay_addrDiv', 'key': 'quay_key', 'next': 'quay_next', 'auth': 'quay_auth'})
class quay_ChainedFixupKernel64(quay_Struct):
    quay__FIELDS = {'value': quay_Bitfield({'target': 30, 'cacheLevel': 2, 'diversity': 16, 'addrDiv': 1, 'key': 2, 'next': 12, 'auth': 1})}
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_9df0053', 'byte_order': 'quay_byte_order_d7969f0'}, '__init__')
    def __init__(quay_self_9df0053, quay_byte_order_d7969f0='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_9df0053)['_FIELDS'].keys(), sizes=_name_boundary.attributes(quay_self_9df0053)['_FIELDS'].values(), byte_order=quay_byte_order_d7969f0)
_name_boundary.module_contract(globals(), {'dyld_chained_import_addend64': 'quay_dyld_chained_import_addend64', 'dyld_chained_ptr_arm64e': 'quay_dyld_chained_ptr_arm64e', 'dyld_chained_starts_in_image': 'quay_dyld_chained_starts_in_image', 'dyld_chained_ptr_arm64e_bind': 'quay_dyld_chained_ptr_arm64e_bind', 'dyld_chained_import_addend': 'quay_dyld_chained_import_addend', 'dyld_chained_start_offsets': 'quay_dyld_chained_start_offsets', 'ChainedPointerArm64E': 'quay_ChainedPointerArm64E', 'ChainedPointerGeneric64': 'quay_ChainedPointerGeneric64', 'ChainedFixupKernel64': 'quay_ChainedFixupKernel64', 'DYLD_CHAINED_PTR_START_LAST': 'quay_DYLD_CHAINED_PTR_START_LAST', 'dyld_chained_ptr_64': 'quay_dyld_chained_ptr_64', 'dyld_chained_import': 'quay_dyld_chained_import', 'dyld_chained_ptr_format': 'quay_dyld_chained_ptr_format', 'dyld_chained_ptr_arm64e_auth_rebase': 'quay_dyld_chained_ptr_arm64e_auth_rebase', 'ChainedFixupPointer64Union': 'quay_ChainedFixupPointer64Union', 'dyld_chained_ptr': 'quay_dyld_chained_ptr', 'dyld_chained_ptr_arm64e_rebase': 'quay_dyld_chained_ptr_arm64e_rebase', 'dyld_chained_ptr_arm64e_auth_bind': 'quay_dyld_chained_ptr_arm64e_auth_bind', 'dyld_chained_ptr_32_rebase': 'quay_dyld_chained_ptr_32_rebase', 'dyld_chained_ptr_arm64e_auth_bind24': 'quay_dyld_chained_ptr_arm64e_auth_bind24', 'dyld_chained_ptr_32_bind': 'quay_dyld_chained_ptr_32_bind', 'dyld_chained_ptr_32_cache_rebase': 'quay_dyld_chained_ptr_32_cache_rebase', 'dyld_chained_ptr_64_bind': 'quay_dyld_chained_ptr_64_bind', 'Enum': 'quay_Enum', 'dyld_chained_fixups_header': 'quay_dyld_chained_fixups_header', 'dyld_chained_ptr_32_firmware_rebase': 'quay_dyld_chained_ptr_32_firmware_rebase', 'dyld_chained_import_format': 'quay_dyld_chained_import_format', 'ChainedPointerGeneric32': 'quay_ChainedPointerGeneric32', 'dyld_chained_ptr_arm64e_bind24': 'quay_dyld_chained_ptr_arm64e_bind24', 'ChainedFixupPointerGeneric': 'quay_ChainedFixupPointerGeneric', 'ChainedFixupPointer32': 'quay_ChainedFixupPointer32', 'dyld_chained_starts_in_segment': 'quay_dyld_chained_starts_in_segment', 'ChainedFixupPointer64': 'quay_ChainedFixupPointer64', 'DYLD_CHAINED_PTR_START_MULTI': 'quay_DYLD_CHAINED_PTR_START_MULTI', 'dyld_chained_ptr_64_rebase': 'quay_dyld_chained_ptr_64_rebase', 'DYLD_CHAINED_PTR_START_NONE': 'quay_DYLD_CHAINED_PTR_START_NONE'})
