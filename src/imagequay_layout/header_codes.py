# Derived from src/ktool_macho/mach_header.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool_macho
#  mach_header.py
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
from enum import IntEnum as quay_IntEnum
from imagequay_layout.binary_records import *
quay_MH_MAGIC = 4277009102
quay_MH_CIGAM = 3472551422
quay_MH_MAGIC_64 = 4277009103
quay_MH_CIGAM_64 = 3489328638
quay_FAT_MAGIC = 3405691582
quay_FAT_CIGAM = 3199925962

@_name_boundary.class_contract('MH_FLAGS', {})
class quay_MH_FLAGS(quay_IntEnum):
    NOUNDEFS = 1
    INCRLINK = 2
    DYLDLINK = 4
    BINDATLOAD = 8
    PREBOUND = 16
    SPLIT_SEGS = 32
    LAZY_INIT = 64
    TWOLEVEL = 128
    FORCE_FLAT = 256
    NOMULTIEFS = 512
    NOFIXPREBINDING = 1024
    PREBINDABLE = 2048
    ALLMODSBOUND = 4096
    SUBSECTIONS_VIA_SYMBOLS = 8192
    CANONICAL = 16384
    WEAK_DEFINES = 32768
    BINDS_TO_WEAK = 65536
    ALLOW_STACK_EXECUTION = 131072
    ROOT_SAFE = 262144
    SETUID_SAFE = 524288
    NO_REEXPORTED_DYLIBS = 1048576
    PIE = 2097152
    DEAD_STRIPPABLE_DYLIB = 4194304
    HAS_TLV_DESCRIPTORS = 8388608
    NO_HEAP_EXECUTION = 16777216
    APP_EXTENSION_SAFE = 33554432
    NLIST_OUTOFSYNC_WITH_DYLDINFO = 67108864
    SIM_SUPPORT = 134217728

@_name_boundary.class_contract('MH_FILETYPE', {})
class quay_MH_FILETYPE(quay_IntEnum):
    UNK = 0
    OBJECT = 1
    EXECUTE = 2
    FVMLIB = 3
    CORE = 4
    PRELOAD = 5
    DYLIB = 6
    DYLINKER = 7
    BUNDLE = 8
    DYLIB_STUB = 9
    DSYM = 10
    KEXT_BUNDLE = 11
quay_LC_REQ_DYLD = 2147483648

@_name_boundary.class_contract('LOAD_COMMAND', {})
class quay_LOAD_COMMAND(quay_IntEnum):
    SEGMENT = 1
    SYMTAB = 2
    SYMSEG = 3
    THREAD = 4
    UNIXTHREAD = 5
    LOADFVMLIB = 6
    IDFVMLIB = 7
    IDENT = 8
    FVMFILE = 9
    PREPAGE = 10
    DYSYMTAB = 11
    LOAD_DYLIB = 12
    ID_DYLIB = 13
    LOAD_DYLINKER = 14
    ID_DYLINKER = 15
    PREBOUND_DYLIB = 16
    ROUTINES = 17
    SUB_FRAMEWORK = 18
    SUB_UMBRELLA = 19
    SUB_CLIENT = 20
    SUB_image = 21
    TWOLEVEL_HINTS = 22
    PREBIND_CKSUM = 23
    LOAD_WEAK_DYLIB = 24 | quay_LC_REQ_DYLD
    SEGMENT_64 = 25
    ROUTINES_64 = 26
    UUID = 27
    RPATH = 28 | quay_LC_REQ_DYLD
    CODE_SIGNATURE = 29
    SEGMENT_SPLIT_INFO = 30
    REEXPORT_DYLIB = 31 | quay_LC_REQ_DYLD
    LAZY_LOAD_DYLIB = 32
    ENCRYPTION_INFO = 33
    DYLD_INFO = 34
    DYLD_INFO_ONLY = 34 | quay_LC_REQ_DYLD
    LOAD_UPWARD_DYLIB = 35 | quay_LC_REQ_DYLD
    VERSION_MIN_MACOSX = 36
    VERSION_MIN_IPHONEOS = 37
    FUNCTION_STARTS = 38
    DYLD_ENVIRONMENT = 39
    MAIN = 40 | quay_LC_REQ_DYLD
    DATA_IN_CODE = 41
    SOURCE_VERSION = 42
    DYLIB_CODE_SIGN_DRS = 43
    ENCRYPTION_INFO_64 = 44
    LINKER_OPTION = 45
    LINKER_OPTIMIZATION_HINT = 46
    VERSION_MIN_TVOS = 47
    VERSION_MIN_WATCHOS = 48
    NOTE = 49
    BUILD_VERSION = 50
    LC_DYLD_EXPORTS_TRIE = 51 | quay_LC_REQ_DYLD
    LC_DYLD_CHAINED_FIXUPS = 52 | quay_LC_REQ_DYLD
quay_LOAD_COMMAND_MAP = {quay_LOAD_COMMAND.SEGMENT: quay_segment_command, quay_LOAD_COMMAND.SYMTAB: quay_symtab_command, quay_LOAD_COMMAND.DYSYMTAB: quay_dysymtab_command, quay_LOAD_COMMAND.THREAD: quay_thread_command, quay_LOAD_COMMAND.UNIXTHREAD: quay_thread_command, quay_LOAD_COMMAND.LOAD_DYLIB: quay_dylib_command, quay_LOAD_COMMAND.ID_DYLIB: quay_dylib_command, quay_LOAD_COMMAND.REEXPORT_DYLIB: quay_dylib_command, quay_LOAD_COMMAND.LOAD_DYLINKER: quay_dylinker_command, quay_LOAD_COMMAND.SUB_CLIENT: quay_sub_client_command, quay_LOAD_COMMAND.LOAD_WEAK_DYLIB: quay_dylib_command, quay_LOAD_COMMAND.LOAD_UPWARD_DYLIB: quay_dylib_command, quay_LOAD_COMMAND.SEGMENT_64: quay_segment_command_64, quay_LOAD_COMMAND.UUID: quay_uuid_command, quay_LOAD_COMMAND.CODE_SIGNATURE: quay_linkedit_data_command, quay_LOAD_COMMAND.SEGMENT_SPLIT_INFO: quay_linkedit_data_command, quay_LOAD_COMMAND.SOURCE_VERSION: quay_source_version_command, quay_LOAD_COMMAND.DYLD_INFO_ONLY: quay_dyld_info_command, quay_LOAD_COMMAND.FUNCTION_STARTS: quay_linkedit_data_command, quay_LOAD_COMMAND.DYLD_ENVIRONMENT: quay_dylinker_command, quay_LOAD_COMMAND.DATA_IN_CODE: quay_linkedit_data_command, quay_LOAD_COMMAND.BUILD_VERSION: quay_build_version_command, quay_LOAD_COMMAND.MAIN: quay_entry_point_command, quay_LOAD_COMMAND.RPATH: quay_rpath_command, quay_LOAD_COMMAND.ENCRYPTION_INFO: quay_encryption_info_command, quay_LOAD_COMMAND.ENCRYPTION_INFO_64: quay_encryption_info_command_64, quay_LOAD_COMMAND.VERSION_MIN_MACOSX: quay_version_min_command, quay_LOAD_COMMAND.VERSION_MIN_IPHONEOS: quay_version_min_command, quay_LOAD_COMMAND.VERSION_MIN_TVOS: quay_version_min_command, quay_LOAD_COMMAND.VERSION_MIN_WATCHOS: quay_version_min_command, quay_LOAD_COMMAND.LC_DYLD_EXPORTS_TRIE: quay_linkedit_data_command, quay_LOAD_COMMAND.LC_DYLD_CHAINED_FIXUPS: quay_linkedit_data_command}

@_name_boundary.class_contract('S_FLAGS_MASKS', {})
class quay_S_FLAGS_MASKS(quay_IntEnum):
    SECTION_TYPE = 255
    SECTION_ATTRIBUTES = 4294967040
    SECTION_ATTRIBUTES_USR = 4278190080
    SECTION_ATTRIBUTES_SYS = 16776960

@_name_boundary.class_contract('SectionType', {})
class quay_SectionType(quay_IntEnum):
    S_REGULAR = 0
    S_ZEROFILL = 1
    S_CSTRING_LITERALS = 2
    S_4BYTE_LITERALS = 3
    S_8BYTE_LITERALS = 4
    S_LITERAL_POINTERS = 5
    S_NON_LAZY_SYMBOL_POINTERS = 6
    S_LAZY_SYMBOL_POINTERS = 7
    S_SYMBOL_STUBS = 8
    S_MOD_INIT_FUNC_POINTERS = 9
    S_MOD_TERM_FUNC_POINTERS = 10
    S_COALESCED = 11
    S_GB_ZEROFILL = 12
    S_INTERPOSING = 13
    S_16BYTE_LITERALS = 14
    S_DTRACE_DOF = 15
    S_LAZY_DYLIB_SYMBOL_POINTERS = 16
    S_THREAD_LOCAL_REGULAR = 17
    S_THREAD_LOCAL_ZEROFILL = 18
    S_THREAD_LOCAL_VARIABLES = 19
    S_THREAD_LOCAL_VARIABLE_POINTERS = 20
    S_THREAD_LOCAL_INIT_FUNCTION_POINTERS = 21

@_name_boundary.class_contract('SectionAttributesUser', {})
class quay_SectionAttributesUser(quay_IntEnum):
    S_ATTR_PURE_INSTRUCTIONS = 2147483648
    S_ATTR_NO_TOC = 1073741824
    S_ATTR_STRIP_STATIC_SYMS = 536870912
    S_ATTR_NO_DEAD_STRIP = 268435456
    S_ATTR_LIVE_SUPPORT = 134217728
    S_ATTR_SELF_MODIFYING_CODE = 67108864
    S_ATTR_DEBUG = 33554432

@_name_boundary.class_contract('SectionAttributesSys', {})
class quay_SectionAttributesSys(quay_IntEnum):
    S_ATTR_SOME_INSTRUCTIONS = 1024
    S_ATTR_EXT_RELOC = 512
    S_ATTR_LOC_RELOC = 256
quay_CPU_ARCH_MASK = 4278190080
quay_CPU_ARCH_ABI64 = 16777216
quay_CPU_ARCH_ABI6432 = 33554432

@_name_boundary.class_contract('CPUType', {})
class quay_CPUType(quay_IntEnum):
    ANY = -1
    X86 = 7
    X86_64 = X86 | quay_CPU_ARCH_ABI64
    MC98000 = 10
    ARM = 12
    ARM64 = ARM | quay_CPU_ARCH_ABI64
    SPARC = 14
    POWERPC = 18
    POWERPC64 = POWERPC | quay_CPU_ARCH_ABI64
    ARM6432 = ARM | quay_CPU_ARCH_ABI6432

@_name_boundary.class_contract('CPUSubTypeX86', {})
class quay_CPUSubTypeX86(quay_IntEnum):
    ALL = 3
    ARCH1 = 4

@_name_boundary.class_contract('CPUSubTypeX86_64', {})
class quay_CPUSubTypeX86_64(quay_IntEnum):
    ALL = 3
    H = 8

@_name_boundary.class_contract('CPUSubTypeARM', {})
class quay_CPUSubTypeARM(quay_IntEnum):
    ALL = 0
    V4T = 5
    V6 = 6
    V5 = 7
    V5TEJ = 7
    XSCALE = 8
    V7 = 9
    ARM_V7F = 10
    V7S = 11
    V7K = 12
    V6M = 14
    V7M = 15
    V7EM = 16

@_name_boundary.class_contract('CPUSubTypeARM64', {})
class quay_CPUSubTypeARM64(quay_IntEnum):
    ALL = 0
    ARM64E = 2

@_name_boundary.class_contract('CPUSubTypeSPARC', {})
class quay_CPUSubTypeSPARC(quay_IntEnum):
    ALL = 0

@_name_boundary.class_contract('CPUSubTypePowerPC', {})
class quay_CPUSubTypePowerPC(quay_IntEnum):
    ALL = 0
    _601 = 1
    _602 = 2
    _603 = 3
    _603e = 4
    _603ev = 5
    _604 = 6
    _604e = 7
    _620 = 8
    _750 = 9
    _7400 = 10
    _7450 = 11
    _970 = 100

@_name_boundary.class_contract('CPUSubTypeARM6432', {})
class quay_CPUSubTypeARM6432(quay_IntEnum):
    ALL = 0
    V8 = 1
quay_CPU_SUBTYPES = {quay_CPUType.X86: quay_CPUSubTypeX86, quay_CPUType.X86_64: quay_CPUSubTypeX86_64, quay_CPUType.POWERPC: quay_CPUSubTypePowerPC, quay_CPUType.ARM: quay_CPUSubTypeARM, quay_CPUType.ARM64: quay_CPUSubTypeARM64, quay_CPUType.ARM6432: quay_CPUSubTypeARM6432, quay_CPUType.SPARC: quay_CPUSubTypeSPARC}
_name_boundary.module_contract(globals(), {'CPUSubTypeARM': 'quay_CPUSubTypeARM', 'MH_CIGAM_64': 'quay_MH_CIGAM_64', 'MH_MAGIC_64': 'quay_MH_MAGIC_64', 'CPUType': 'quay_CPUType', 'CPUSubTypeX86_64': 'quay_CPUSubTypeX86_64', 'SectionAttributesUser': 'quay_SectionAttributesUser', 'CPU_SUBTYPES': 'quay_CPU_SUBTYPES', 'CPUSubTypePowerPC': 'quay_CPUSubTypePowerPC', 'FAT_CIGAM': 'quay_FAT_CIGAM', 'MH_FLAGS': 'quay_MH_FLAGS', 'S_FLAGS_MASKS': 'quay_S_FLAGS_MASKS', 'CPUSubTypeARM6432': 'quay_CPUSubTypeARM6432', 'LC_REQ_DYLD': 'quay_LC_REQ_DYLD', 'CPUSubTypeX86': 'quay_CPUSubTypeX86', 'LOAD_COMMAND': 'quay_LOAD_COMMAND', 'CPUSubTypeSPARC': 'quay_CPUSubTypeSPARC', 'SectionAttributesSys': 'quay_SectionAttributesSys', 'SectionType': 'quay_SectionType', 'MH_CIGAM': 'quay_MH_CIGAM', 'CPU_ARCH_ABI64': 'quay_CPU_ARCH_ABI64', 'CPU_ARCH_MASK': 'quay_CPU_ARCH_MASK', 'CPU_ARCH_ABI6432': 'quay_CPU_ARCH_ABI6432', 'LOAD_COMMAND_MAP': 'quay_LOAD_COMMAND_MAP', 'CPUSubTypeARM64': 'quay_CPUSubTypeARM64', 'IntEnum': 'quay_IntEnum', 'MH_FILETYPE': 'quay_MH_FILETYPE', 'MH_MAGIC': 'quay_MH_MAGIC', 'FAT_MAGIC': 'quay_FAT_MAGIC'})
