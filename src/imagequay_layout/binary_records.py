# Derived from src/ktool_macho/structs.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool_macho
#  structs.py
#
#  the __init__ defs here are unnecessary and only required for my IDE (pycharm) to recognize and autocomplete
#   the struct attributes
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary
import imagequay_layout as quay_imagequay_macho
from imagequay_support.record_engine import *

@_name_boundary.callable_contract({'struct': 'quay_struct_7f08eac', 'field': 'quay_field_b351b0e'}, 'os_tuple_composer')
def quay_os_tuple_composer(quay_struct_7f08eac: quay_Struct, quay_field_b351b0e: str):
    quay_value_c36466e = _name_boundary.read_attribute(quay_struct_7f08eac, quay_field_b351b0e)
    quay_x_7db56d6 = quay_value_c36466e >> 16 & 65535
    quay_y_295994f = quay_value_c36466e >> 8 & 255
    quay_z_704907f = quay_value_c36466e & 255
    quay_dot_747a374 = _name_boundary.attributes(quay_Struct)['t_token']('.')
    return f"{_name_boundary.attributes(quay_Struct)['t_base'](quay_x_7db56d6)}{quay_dot_747a374}{_name_boundary.attributes(quay_Struct)['t_base'](quay_y_295994f)}{quay_dot_747a374}{_name_boundary.attributes(quay_Struct)['t_base'](quay_z_704907f)}"

@_name_boundary.callable_contract({'struct': 'quay_struct_2583985', 'field': 'quay_field_bcfdd49'}, 'cmd_composer')
def quay_cmd_composer(quay_struct_2583985: quay_Struct, quay_field_bcfdd49: str):
    quay_value_fec5793 = _name_boundary.read_attribute(quay_struct_2583985, quay_field_bcfdd49)
    return f"{_name_boundary.attributes(quay_Struct)['t_base'](_name_boundary.attributes(_name_boundary.attributes(quay_imagequay_macho)['LOAD_COMMAND'](quay_value_fec5793))['name'])} {_name_boundary.attributes(quay_Struct)['t_token']('(')}{_name_boundary.attributes(quay_Struct)['t_base'](hex(quay_value_fec5793))}{_name_boundary.attributes(quay_Struct)['t_token'](')')}"

@_name_boundary.class_contract('fat_header', {'FIELDS': 'quay_FIELDS', 'magic': 'quay_magic', 'nfat_archs': 'quay_nfat_archs'})
class quay_fat_header(quay_Struct):
    """
    First 8 Bytes of a FAT MachO File

    Attributes:
        self.magic: FAT MachO Magic

        self.nfat_archs: Number of Fat Arch entries after these bytes
    """
    quay_FIELDS = {'magic': quay_uint32_t, 'nfat_archs': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_833be6a', 'byte_order': 'quay_byte_order_64f709c'}, '__init__')
    def __init__(quay_self_833be6a, quay_byte_order_64f709c='little'):
        super().__init__(byte_order=quay_byte_order_64f709c)
        _name_boundary.attributes(quay_self_833be6a)['magic'] = 0
        _name_boundary.attributes(quay_self_833be6a)['nfat_archs'] = 0

@_name_boundary.class_contract('fat_arch', {'FIELDS': 'quay_FIELDS', 'cpu_type': 'quay_cpu_type', 'cpu_subtype': 'quay_cpu_subtype', 'offset': 'quay_offset', 'size': 'quay_size', 'align': 'quay_align'})
class quay_fat_arch(quay_Struct):
    """
    Struct representing a slice in a FAT MachO

    Attribs:
        cpu_type:
    """
    quay_FIELDS = {'cpu_type': quay_uint32_t, 'cpu_subtype': quay_uint32_t, 'offset': quay_uint32_t, 'size': quay_uint32_t, 'align': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_0914460', 'byte_order': 'quay_byte_order_3d67d92'}, '__init__')
    def __init__(quay_self_0914460, quay_byte_order_3d67d92='little'):
        super().__init__(byte_order=quay_byte_order_3d67d92)
        _name_boundary.attributes(quay_self_0914460)['cpu_type'] = 0
        _name_boundary.attributes(quay_self_0914460)['cpu_subtype'] = 0
        _name_boundary.attributes(quay_self_0914460)['offset'] = 0
        _name_boundary.attributes(quay_self_0914460)['size'] = 0
        _name_boundary.attributes(quay_self_0914460)['align'] = 0

@_name_boundary.class_contract('mach_header', {'FIELDS': 'quay_FIELDS', 'magic': 'quay_magic', 'cpu_type': 'quay_cpu_type', 'cpu_subtype': 'quay_cpu_subtype', 'filetype': 'quay_filetype', 'loadcnt': 'quay_loadcnt', 'loadsize': 'quay_loadsize', 'flags': 'quay_flags'})
class quay_mach_header(quay_Struct):
    quay_FIELDS = {'magic': quay_uint32_t, 'cpu_type': quay_uint32_t, 'cpu_subtype': quay_uint32_t, 'filetype': quay_uint32_t, 'loadcnt': quay_uint32_t, 'loadsize': quay_uint32_t, 'flags': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_b286bdb', 'byte_order': 'quay_byte_order_13c19d2'}, '__init__')
    def __init__(quay_self_b286bdb, quay_byte_order_13c19d2='little'):
        super().__init__(byte_order=quay_byte_order_13c19d2)
        _name_boundary.attributes(quay_self_b286bdb)['magic'] = 0
        _name_boundary.attributes(quay_self_b286bdb)['cpu_type'] = 0
        _name_boundary.attributes(quay_self_b286bdb)['cpu_subtype'] = 0
        _name_boundary.attributes(quay_self_b286bdb)['filetype'] = 0
        _name_boundary.attributes(quay_self_b286bdb)['loadcnt'] = 0
        _name_boundary.attributes(quay_self_b286bdb)['loadsize'] = 0
        _name_boundary.attributes(quay_self_b286bdb)['flags'] = 0

@_name_boundary.class_contract('mach_header_64', {'FIELDS': 'quay_FIELDS', 'magic': 'quay_magic', 'cpu_type': 'quay_cpu_type', 'cpu_subtype': 'quay_cpu_subtype', 'filetype': 'quay_filetype', 'loadcnt': 'quay_loadcnt', 'loadsize': 'quay_loadsize', 'flags': 'quay_flags', 'reserved': 'quay_reserved'})
class quay_mach_header_64(quay_Struct):
    quay_FIELDS = {'magic': quay_uint32_t, 'cpu_type': quay_uint32_t, 'cpu_subtype': quay_uint32_t, 'filetype': quay_uint32_t, 'loadcnt': quay_uint32_t, 'loadsize': quay_uint32_t, 'flags': quay_uint32_t, 'reserved': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_4f8714d', 'byte_order': 'quay_byte_order_c10f65d'}, '__init__')
    def __init__(quay_self_4f8714d, quay_byte_order_c10f65d='little'):
        super().__init__(byte_order=quay_byte_order_c10f65d)
        _name_boundary.attributes(quay_self_4f8714d)['magic'] = 0
        _name_boundary.attributes(quay_self_4f8714d)['cpu_type'] = 0
        _name_boundary.attributes(quay_self_4f8714d)['cpu_subtype'] = 0
        _name_boundary.attributes(quay_self_4f8714d)['filetype'] = 0
        _name_boundary.attributes(quay_self_4f8714d)['loadcnt'] = 0
        _name_boundary.attributes(quay_self_4f8714d)['loadsize'] = 0
        _name_boundary.attributes(quay_self_4f8714d)['flags'] = 0
        _name_boundary.attributes(quay_self_4f8714d)['reserved'] = 0

@_name_boundary.class_contract('unk_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'add_field_composer': 'quay_add_field_composer'})
class quay_unk_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_b08fe93', 'byte_order': 'quay_byte_order_db96283'}, '__init__')
    def __init__(quay_self_b08fe93, quay_byte_order_db96283='little'):
        super().__init__(byte_order=quay_byte_order_db96283)
        _name_boundary.attributes(quay_self_b08fe93)['cmd'] = 0
        _name_boundary.attributes(quay_self_b08fe93)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_b08fe93)['cmdsize'] = 0

@_name_boundary.class_contract('segment_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'segname': 'quay_segname', 'vmaddr': 'quay_vmaddr', 'vmsize': 'quay_vmsize', 'fileoff': 'quay_fileoff', 'filesize': 'quay_filesize', 'maxprot': 'quay_maxprot', 'initprot': 'quay_initprot', 'nsects': 'quay_nsects', 'flags': 'quay_flags', 'add_field_composer': 'quay_add_field_composer'})
class quay_segment_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'segname': quay_char_t[16], 'vmaddr': quay_uint32_t, 'vmsize': quay_uint32_t, 'fileoff': quay_uint32_t, 'filesize': quay_uint32_t, 'maxprot': quay_uint32_t, 'initprot': quay_uint32_t, 'nsects': quay_uint32_t, 'flags': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_5b5df6e', 'byte_order': 'quay_byte_order_1b8a154'}, '__init__')
    def __init__(quay_self_5b5df6e, quay_byte_order_1b8a154='little'):
        super().__init__(byte_order=quay_byte_order_1b8a154)
        _name_boundary.attributes(quay_self_5b5df6e)['cmd'] = 0
        _name_boundary.attributes(quay_self_5b5df6e)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_5b5df6e)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_5b5df6e)['segname'] = 0
        _name_boundary.attributes(quay_self_5b5df6e)['vmaddr'] = 0
        _name_boundary.attributes(quay_self_5b5df6e)['vmsize'] = 0
        _name_boundary.attributes(quay_self_5b5df6e)['fileoff'] = 0
        _name_boundary.attributes(quay_self_5b5df6e)['filesize'] = 0
        _name_boundary.attributes(quay_self_5b5df6e)['maxprot'] = 0
        _name_boundary.attributes(quay_self_5b5df6e)['initprot'] = 0
        _name_boundary.attributes(quay_self_5b5df6e)['nsects'] = 0
        _name_boundary.attributes(quay_self_5b5df6e)['flags'] = 0

@_name_boundary.class_contract('segment_command_64', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'segname': 'quay_segname', 'vmaddr': 'quay_vmaddr', 'vmsize': 'quay_vmsize', 'fileoff': 'quay_fileoff', 'filesize': 'quay_filesize', 'maxprot': 'quay_maxprot', 'initprot': 'quay_initprot', 'nsects': 'quay_nsects', 'flags': 'quay_flags', 'add_field_composer': 'quay_add_field_composer'})
class quay_segment_command_64(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'segname': quay_char_t[16], 'vmaddr': quay_uint64_t, 'vmsize': quay_uint64_t, 'fileoff': quay_uint64_t, 'filesize': quay_uint64_t, 'maxprot': quay_uint32_t, 'initprot': quay_uint32_t, 'nsects': quay_uint32_t, 'flags': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_4c16e75', 'byte_order': 'quay_byte_order_7fbaab8'}, '__init__')
    def __init__(quay_self_4c16e75, quay_byte_order_7fbaab8='little'):
        super().__init__(byte_order=quay_byte_order_7fbaab8)
        _name_boundary.attributes(quay_self_4c16e75)['cmd'] = 0
        _name_boundary.attributes(quay_self_4c16e75)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_4c16e75)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_4c16e75)['segname'] = 0
        _name_boundary.attributes(quay_self_4c16e75)['vmaddr'] = 0
        _name_boundary.attributes(quay_self_4c16e75)['vmsize'] = 0
        _name_boundary.attributes(quay_self_4c16e75)['fileoff'] = 0
        _name_boundary.attributes(quay_self_4c16e75)['filesize'] = 0
        _name_boundary.attributes(quay_self_4c16e75)['maxprot'] = 0
        _name_boundary.attributes(quay_self_4c16e75)['initprot'] = 0
        _name_boundary.attributes(quay_self_4c16e75)['nsects'] = 0
        _name_boundary.attributes(quay_self_4c16e75)['flags'] = 0

@_name_boundary.class_contract('section', {'FIELDS': 'quay_FIELDS', 'sectname': 'quay_sectname', 'segname': 'quay_segname', 'addr': 'quay_addr', 'size': 'quay_size', 'offset': 'quay_offset', 'align': 'quay_align', 'reloff': 'quay_reloff', 'nreloc': 'quay_nreloc', 'flags': 'quay_flags', 'reserved1': 'quay_reserved1', 'reserved2': 'quay_reserved2'})
class quay_section(quay_Struct):
    quay_FIELDS = {'sectname': quay_char_t[16], 'segname': quay_char_t[16], 'addr': quay_uint32_t, 'size': quay_uint32_t, 'offset': quay_uint32_t, 'align': quay_uint32_t, 'reloff': quay_uint32_t, 'nreloc': quay_uint32_t, 'flags': quay_uint32_t, 'reserved1': quay_uint32_t, 'reserved2': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_064807a', 'byte_order': 'quay_byte_order_9c2c556'}, '__init__')
    def __init__(quay_self_064807a, quay_byte_order_9c2c556='little'):
        super().__init__(byte_order=quay_byte_order_9c2c556)
        _name_boundary.attributes(quay_self_064807a)['sectname'] = 0
        _name_boundary.attributes(quay_self_064807a)['segname'] = 0
        _name_boundary.attributes(quay_self_064807a)['addr'] = 0
        _name_boundary.attributes(quay_self_064807a)['size'] = 0
        _name_boundary.attributes(quay_self_064807a)['offset'] = 0
        _name_boundary.attributes(quay_self_064807a)['align'] = 0
        _name_boundary.attributes(quay_self_064807a)['reloff'] = 0
        _name_boundary.attributes(quay_self_064807a)['nreloc'] = 0
        _name_boundary.attributes(quay_self_064807a)['flags'] = 0
        _name_boundary.attributes(quay_self_064807a)['reserved1'] = 0
        _name_boundary.attributes(quay_self_064807a)['reserved2'] = 0

@_name_boundary.class_contract('section_64', {'FIELDS': 'quay_FIELDS', 'sectname': 'quay_sectname', 'segname': 'quay_segname', 'addr': 'quay_addr', 'size': 'quay_size', 'offset': 'quay_offset', 'align': 'quay_align', 'reloff': 'quay_reloff', 'nreloc': 'quay_nreloc', 'flags': 'quay_flags', 'reserved1': 'quay_reserved1', 'reserved2': 'quay_reserved2', 'reserved3': 'quay_reserved3'})
class quay_section_64(quay_Struct):
    quay_FIELDS = {'sectname': quay_char_t[16], 'segname': quay_char_t[16], 'addr': quay_uint64_t, 'size': quay_uint64_t, 'offset': quay_uint32_t, 'align': quay_uint32_t, 'reloff': quay_uint32_t, 'nreloc': quay_uint32_t, 'flags': quay_uint32_t, 'reserved1': quay_uint32_t, 'reserved2': quay_uint32_t, 'reserved3': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_215b3c7', 'byte_order': 'quay_byte_order_67a0715'}, '__init__')
    def __init__(quay_self_215b3c7, quay_byte_order_67a0715='little'):
        super().__init__(byte_order=quay_byte_order_67a0715)
        _name_boundary.attributes(quay_self_215b3c7)['sectname'] = 0
        _name_boundary.attributes(quay_self_215b3c7)['segname'] = 0
        _name_boundary.attributes(quay_self_215b3c7)['addr'] = 0
        _name_boundary.attributes(quay_self_215b3c7)['size'] = 0
        _name_boundary.attributes(quay_self_215b3c7)['offset'] = 0
        _name_boundary.attributes(quay_self_215b3c7)['align'] = 0
        _name_boundary.attributes(quay_self_215b3c7)['reloff'] = 0
        _name_boundary.attributes(quay_self_215b3c7)['nreloc'] = 0
        _name_boundary.attributes(quay_self_215b3c7)['flags'] = 0
        _name_boundary.attributes(quay_self_215b3c7)['reserved1'] = 0
        _name_boundary.attributes(quay_self_215b3c7)['reserved2'] = 0
        _name_boundary.attributes(quay_self_215b3c7)['reserved3'] = 0

@_name_boundary.class_contract('symtab_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'symoff': 'quay_symoff', 'nsyms': 'quay_nsyms', 'stroff': 'quay_stroff', 'strsize': 'quay_strsize', 'add_field_composer': 'quay_add_field_composer'})
class quay_symtab_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'symoff': quay_uint32_t, 'nsyms': quay_uint32_t, 'stroff': quay_uint32_t, 'strsize': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_4e1d3a4', 'byte_order': 'quay_byte_order_83c7ee7'}, '__init__')
    def __init__(quay_self_4e1d3a4, quay_byte_order_83c7ee7='little'):
        super().__init__(byte_order=quay_byte_order_83c7ee7)
        _name_boundary.attributes(quay_self_4e1d3a4)['cmd'] = 0
        _name_boundary.attributes(quay_self_4e1d3a4)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_4e1d3a4)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_4e1d3a4)['symoff'] = 0
        _name_boundary.attributes(quay_self_4e1d3a4)['nsyms'] = 0
        _name_boundary.attributes(quay_self_4e1d3a4)['stroff'] = 0
        _name_boundary.attributes(quay_self_4e1d3a4)['strsize'] = 0

@_name_boundary.class_contract('dysymtab_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'ilocalsym': 'quay_ilocalsym', 'nlocalsym': 'quay_nlocalsym', 'iextdefsym': 'quay_iextdefsym', 'nextdefsym': 'quay_nextdefsym', 'iundefsym': 'quay_iundefsym', 'nundefsym': 'quay_nundefsym', 'tocoff': 'quay_tocoff', 'ntoc': 'quay_ntoc', 'modtaboff': 'quay_modtaboff', 'nmodtab': 'quay_nmodtab', 'extrefsymoff': 'quay_extrefsymoff', 'nextrefsyms': 'quay_nextrefsyms', 'indirectsymoff': 'quay_indirectsymoff', 'nindirectsyms': 'quay_nindirectsyms', 'extreloff': 'quay_extreloff', 'nextrel': 'quay_nextrel', 'locreloff': 'quay_locreloff', 'nlocrel': 'quay_nlocrel', 'add_field_composer': 'quay_add_field_composer'})
class quay_dysymtab_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'ilocalsym': quay_uint32_t, 'nlocalsym': quay_uint32_t, 'iextdefsym': quay_uint32_t, 'nextdefsym': quay_uint32_t, 'iundefsym': quay_uint32_t, 'nundefsym': quay_uint32_t, 'tocoff': quay_uint32_t, 'ntoc': quay_uint32_t, 'modtaboff': quay_uint32_t, 'nmodtab': quay_uint32_t, 'extrefsymoff': quay_uint32_t, 'nextrefsyms': quay_uint32_t, 'indirectsymoff': quay_uint32_t, 'nindirectsyms': quay_uint32_t, 'extreloff': quay_uint32_t, 'nextrel': quay_uint32_t, 'locreloff': quay_uint32_t, 'nlocrel': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_17bb7fa', 'byte_order': 'quay_byte_order_a15572e'}, '__init__')
    def __init__(quay_self_17bb7fa, quay_byte_order_a15572e='little'):
        super().__init__(byte_order=quay_byte_order_a15572e)
        _name_boundary.attributes(quay_self_17bb7fa)['cmd'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_17bb7fa)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['ilocalsym'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['nlocalsym'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['iextdefsym'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['nextdefsym'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['iundefsym'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['nundefsym'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['tocoff'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['ntoc'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['modtaboff'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['nmodtab'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['extrefsymoff'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['nextrefsyms'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['indirectsymoff'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['nindirectsyms'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['extreloff'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['nextrel'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['locreloff'] = 0
        _name_boundary.attributes(quay_self_17bb7fa)['nlocrel'] = 0

@_name_boundary.class_contract('dylib', {'FIELDS': 'quay_FIELDS', 'name': 'quay_name', 'timestamp': 'quay_timestamp', 'current_version': 'quay_current_version', 'compatibility_version': 'quay_compatibility_version', 'add_field_composer': 'quay_add_field_composer'})
class quay_dylib(quay_Struct):
    quay_FIELDS = {'name': quay_uint32_t, 'timestamp': quay_uint32_t, 'current_version': quay_uint32_t, 'compatibility_version': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_c35e14b', 'byte_order': 'quay_byte_order_e26656f'}, '__init__')
    def __init__(quay_self_c35e14b, quay_byte_order_e26656f='little'):
        super().__init__(byte_order=quay_byte_order_e26656f)
        _name_boundary.attributes(quay_self_c35e14b)['name'] = 0
        _name_boundary.attributes(quay_self_c35e14b)['timestamp'] = 0
        _name_boundary.attributes(quay_self_c35e14b)['current_version'] = 0
        _name_boundary.attributes(quay_self_c35e14b)['compatibility_version'] = 0
        _name_boundary.attributes(quay_self_c35e14b)['add_field_composer']('current_version', quay_os_tuple_composer)
        _name_boundary.attributes(quay_self_c35e14b)['add_field_composer']('compatibility_version', quay_os_tuple_composer)

@_name_boundary.class_contract('dylib_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'dylib': 'quay_dylib', 'add_field_composer': 'quay_add_field_composer'})
class quay_dylib_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'dylib': quay_dylib}

    @_name_boundary.callable_contract({'self': 'quay_self_2dbe009', 'byte_order': 'quay_byte_order_2b0c4b2'}, '__init__')
    def __init__(quay_self_2dbe009, quay_byte_order_2b0c4b2='little'):
        super().__init__(byte_order=quay_byte_order_2b0c4b2)
        _name_boundary.attributes(quay_self_2dbe009)['cmd'] = 0
        _name_boundary.attributes(quay_self_2dbe009)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_2dbe009)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_2dbe009)['dylib'] = 0

@_name_boundary.class_contract('dylinker_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'name': 'quay_name', 'add_field_composer': 'quay_add_field_composer'})
class quay_dylinker_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'name': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_249446c', 'byte_order': 'quay_byte_order_dbd1e20'}, '__init__')
    def __init__(quay_self_249446c, quay_byte_order_dbd1e20='little'):
        super().__init__(byte_order=quay_byte_order_dbd1e20)
        _name_boundary.attributes(quay_self_249446c)['cmd'] = 0
        _name_boundary.attributes(quay_self_249446c)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_249446c)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_249446c)['name'] = 0

@_name_boundary.class_contract('sub_client_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'offset': 'quay_offset', 'add_field_composer': 'quay_add_field_composer'})
class quay_sub_client_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'offset': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_3325d0d', 'byte_order': 'quay_byte_order_a17718b'}, '__init__')
    def __init__(quay_self_3325d0d, quay_byte_order_a17718b='little'):
        super().__init__(byte_order=quay_byte_order_a17718b)
        _name_boundary.attributes(quay_self_3325d0d)['cmd'] = 0
        _name_boundary.attributes(quay_self_3325d0d)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_3325d0d)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_3325d0d)['offset'] = 0

@_name_boundary.class_contract('uuid_command', {'FIELDS': 'quay_FIELDS', 'uuid_field_composer': 'quay_uuid_field_composer', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'uuid': 'quay_uuid', 'add_field_composer': 'quay_add_field_composer'})
class quay_uuid_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'uuid': quay_bytes_t[16]}

    @_name_boundary.callable_contract({'self': 'quay_self_e0010a0', 'byte_order': 'quay_byte_order_d8f9227'}, '__init__')
    def __init__(quay_self_e0010a0, quay_byte_order_d8f9227='little'):
        super().__init__(byte_order=quay_byte_order_d8f9227)
        _name_boundary.attributes(quay_self_e0010a0)['cmd'] = 0
        _name_boundary.attributes(quay_self_e0010a0)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_e0010a0)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_e0010a0)['uuid'] = 0
        _name_boundary.attributes(quay_self_e0010a0)['add_field_composer']('uuid', _name_boundary.attributes(quay_uuid_command)['uuid_field_composer'])

    @staticmethod
    @_name_boundary.callable_contract({'struct': 'quay_struct_2539e36', 'field': 'quay_field_372dc2d'}, 'uuid_field_composer')
    def quay_uuid_field_composer(quay_struct_2539e36, quay_field_372dc2d):
        assert quay_field_372dc2d == 'uuid'
        quay_byte_array_f33ddea = _name_boundary.attributes(quay_struct_2539e36)['uuid']
        return _name_boundary.attributes(quay_Struct)['t_base'](f'"{quay_byte_array_f33ddea[0]:02x}{quay_byte_array_f33ddea[1]:02x}{quay_byte_array_f33ddea[2]:02x}{quay_byte_array_f33ddea[3]:02x}-{quay_byte_array_f33ddea[4]:02x}{quay_byte_array_f33ddea[5]:02x}-{quay_byte_array_f33ddea[6]:02x}{quay_byte_array_f33ddea[7]:02x}-{quay_byte_array_f33ddea[8]:02x}{quay_byte_array_f33ddea[9]:02x}-{quay_byte_array_f33ddea[10]:02x}{quay_byte_array_f33ddea[11]:02x}{quay_byte_array_f33ddea[12]:02x}{quay_byte_array_f33ddea[13]:02x}{quay_byte_array_f33ddea[14]:02x}{quay_byte_array_f33ddea[15]:02x}"')

@_name_boundary.class_contract('build_version_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'platform': 'quay_platform', 'minos': 'quay_minos', 'sdk': 'quay_sdk', 'ntools': 'quay_ntools', 'add_field_composer': 'quay_add_field_composer'})
class quay_build_version_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'platform': quay_uint32_t, 'minos': quay_uint32_t, 'sdk': quay_uint32_t, 'ntools': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_f0b2194', 'byte_order': 'quay_byte_order_812e757'}, '__init__')
    def __init__(quay_self_f0b2194, quay_byte_order_812e757='little'):
        super().__init__(byte_order=quay_byte_order_812e757)
        _name_boundary.attributes(quay_self_f0b2194)['cmd'] = 0
        _name_boundary.attributes(quay_self_f0b2194)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_f0b2194)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_f0b2194)['platform'] = 0
        _name_boundary.attributes(quay_self_f0b2194)['minos'] = 0
        _name_boundary.attributes(quay_self_f0b2194)['sdk'] = 0
        _name_boundary.attributes(quay_self_f0b2194)['ntools'] = 0
        _name_boundary.attributes(quay_self_f0b2194)['add_field_composer']('minos', quay_os_tuple_composer)
        _name_boundary.attributes(quay_self_f0b2194)['add_field_composer']('sdk', quay_os_tuple_composer)

@_name_boundary.class_contract('entry_point_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'entryoff': 'quay_entryoff', 'stacksize': 'quay_stacksize', 'add_field_composer': 'quay_add_field_composer'})
class quay_entry_point_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'entryoff': quay_uint64_t, 'stacksize': quay_uint64_t}

    @_name_boundary.callable_contract({'self': 'quay_self_c5edfd4', 'byte_order': 'quay_byte_order_1361b91'}, '__init__')
    def __init__(quay_self_c5edfd4, quay_byte_order_1361b91='little'):
        super().__init__(byte_order=quay_byte_order_1361b91)
        _name_boundary.attributes(quay_self_c5edfd4)['cmd'] = 0
        _name_boundary.attributes(quay_self_c5edfd4)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_c5edfd4)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_c5edfd4)['entryoff'] = 0
        _name_boundary.attributes(quay_self_c5edfd4)['stacksize'] = 0

@_name_boundary.class_contract('rpath_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'path': 'quay_path', 'add_field_composer': 'quay_add_field_composer'})
class quay_rpath_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'path': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_4383c44', 'byte_order': 'quay_byte_order_9573b49'}, '__init__')
    def __init__(quay_self_4383c44, quay_byte_order_9573b49='little'):
        super().__init__(byte_order=quay_byte_order_9573b49)
        _name_boundary.attributes(quay_self_4383c44)['cmd'] = 0
        _name_boundary.attributes(quay_self_4383c44)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_4383c44)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_4383c44)['path'] = 0

@_name_boundary.class_contract('source_version_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'version': 'quay_version', 'add_field_composer': 'quay_add_field_composer'})
class quay_source_version_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'version': quay_uint64_t}

    @_name_boundary.callable_contract({'self': 'quay_self_e3fe565', 'byte_order': 'quay_byte_order_5fea9ee'}, '__init__')
    def __init__(quay_self_e3fe565, quay_byte_order_5fea9ee='little'):
        super().__init__(byte_order=quay_byte_order_5fea9ee)
        _name_boundary.attributes(quay_self_e3fe565)['cmd'] = 0
        _name_boundary.attributes(quay_self_e3fe565)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_e3fe565)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_e3fe565)['version'] = 0
        _name_boundary.attributes(quay_self_e3fe565)['add_field_composer']('version', quay_os_tuple_composer)

@_name_boundary.class_contract('linkedit_data_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'dataoff': 'quay_dataoff', 'datasize': 'quay_datasize', 'add_field_composer': 'quay_add_field_composer'})
class quay_linkedit_data_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'dataoff': quay_uint32_t, 'datasize': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_d0c1be9', 'byte_order': 'quay_byte_order_c0f7530'}, '__init__')
    def __init__(quay_self_d0c1be9, quay_byte_order_c0f7530='little'):
        super().__init__(byte_order=quay_byte_order_c0f7530)
        _name_boundary.attributes(quay_self_d0c1be9)['cmd'] = 0
        _name_boundary.attributes(quay_self_d0c1be9)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_d0c1be9)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_d0c1be9)['dataoff'] = 0
        _name_boundary.attributes(quay_self_d0c1be9)['datasize'] = 0

@_name_boundary.class_contract('dyld_info_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdisze': 'quay_cmdisze', 'rebase_off': 'quay_rebase_off', 'rebase_size': 'quay_rebase_size', 'bind_off': 'quay_bind_off', 'bind_size': 'quay_bind_size', 'weak_bind_off': 'quay_weak_bind_off', 'weak_bind_size': 'quay_weak_bind_size', 'lazy_bind_off': 'quay_lazy_bind_off', 'lazy_bind_size': 'quay_lazy_bind_size', 'export_off': 'quay_export_off', 'export_size': 'quay_export_size', 'add_field_composer': 'quay_add_field_composer', 'cmdsize': 'quay_cmdsize'})
class quay_dyld_info_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'rebase_off': quay_uint32_t, 'rebase_size': quay_uint32_t, 'bind_off': quay_uint32_t, 'bind_size': quay_uint32_t, 'weak_bind_off': quay_uint32_t, 'weak_bind_size': quay_uint32_t, 'lazy_bind_off': quay_uint32_t, 'lazy_bind_size': quay_uint32_t, 'export_off': quay_uint32_t, 'export_size': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_8dad836', 'byte_order': 'quay_byte_order_b297e55'}, '__init__')
    def __init__(quay_self_8dad836, quay_byte_order_b297e55='little'):
        super().__init__(byte_order=quay_byte_order_b297e55)
        _name_boundary.attributes(quay_self_8dad836)['cmd'] = 0
        _name_boundary.attributes(quay_self_8dad836)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_8dad836)['cmdisze'] = 0
        _name_boundary.attributes(quay_self_8dad836)['rebase_off'] = 0
        _name_boundary.attributes(quay_self_8dad836)['rebase_size'] = 0
        _name_boundary.attributes(quay_self_8dad836)['bind_off'] = 0
        _name_boundary.attributes(quay_self_8dad836)['bind_size'] = 0
        _name_boundary.attributes(quay_self_8dad836)['weak_bind_off'] = 0
        _name_boundary.attributes(quay_self_8dad836)['weak_bind_size'] = 0
        _name_boundary.attributes(quay_self_8dad836)['lazy_bind_off'] = 0
        _name_boundary.attributes(quay_self_8dad836)['lazy_bind_size'] = 0
        _name_boundary.attributes(quay_self_8dad836)['export_off'] = 0
        _name_boundary.attributes(quay_self_8dad836)['export_size'] = 0

@_name_boundary.class_contract('symtab_entry_32', {'FIELDS': 'quay_FIELDS', 'str_index': 'quay_str_index', 'type': 'quay_type', 'sect_index': 'quay_sect_index', 'desc': 'quay_desc', 'value': 'quay_value'})
class quay_symtab_entry_32(quay_Struct):
    quay_FIELDS = {'str_index': quay_uint32_t, 'type': quay_uint8_t, 'sect_index': quay_uint8_t, 'desc': quay_uint16_t, 'value': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_c0e9a80', 'byte_order': 'quay_byte_order_1fe52e3'}, '__init__')
    def __init__(quay_self_c0e9a80, quay_byte_order_1fe52e3='little'):
        super().__init__(byte_order=quay_byte_order_1fe52e3)
        _name_boundary.attributes(quay_self_c0e9a80)['str_index'] = 0
        _name_boundary.attributes(quay_self_c0e9a80)['type'] = 0
        _name_boundary.attributes(quay_self_c0e9a80)['sect_index'] = 0
        _name_boundary.attributes(quay_self_c0e9a80)['desc'] = 0
        _name_boundary.attributes(quay_self_c0e9a80)['value'] = 0

@_name_boundary.class_contract('symtab_entry', {'FIELDS': 'quay_FIELDS', 'str_index': 'quay_str_index', 'type': 'quay_type', 'sect_index': 'quay_sect_index', 'desc': 'quay_desc', 'value': 'quay_value'})
class quay_symtab_entry(quay_Struct):
    quay_FIELDS = {'str_index': quay_uint32_t, 'type': quay_uint8_t, 'sect_index': quay_uint8_t, 'desc': quay_uint16_t, 'value': quay_uint64_t}

    @_name_boundary.callable_contract({'self': 'quay_self_eba5acd', 'byte_order': 'quay_byte_order_9a79eb4'}, '__init__')
    def __init__(quay_self_eba5acd, quay_byte_order_9a79eb4='little'):
        super().__init__(byte_order=quay_byte_order_9a79eb4)
        _name_boundary.attributes(quay_self_eba5acd)['str_index'] = 0
        _name_boundary.attributes(quay_self_eba5acd)['type'] = 0
        _name_boundary.attributes(quay_self_eba5acd)['sect_index'] = 0
        _name_boundary.attributes(quay_self_eba5acd)['desc'] = 0
        _name_boundary.attributes(quay_self_eba5acd)['value'] = 0

@_name_boundary.class_contract('version_min_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'version': 'quay_version', 'reserved': 'quay_reserved', 'add_field_composer': 'quay_add_field_composer'})
class quay_version_min_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'version': quay_uint32_t, 'reserved': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_0dcfa34', 'byte_order': 'quay_byte_order_ce4b0a7'}, '__init__')
    def __init__(quay_self_0dcfa34, quay_byte_order_ce4b0a7='little'):
        super().__init__(byte_order=quay_byte_order_ce4b0a7)
        _name_boundary.attributes(quay_self_0dcfa34)['cmd'] = 0
        _name_boundary.attributes(quay_self_0dcfa34)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_0dcfa34)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_0dcfa34)['version'] = 0
        _name_boundary.attributes(quay_self_0dcfa34)['reserved'] = 0
        _name_boundary.attributes(quay_self_0dcfa34)['add_field_composer']('version', quay_os_tuple_composer)

@_name_boundary.class_contract('encryption_info_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'cryptoff': 'quay_cryptoff', 'cryptsize': 'quay_cryptsize', 'cryptid': 'quay_cryptid', 'add_field_composer': 'quay_add_field_composer'})
class quay_encryption_info_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'cryptoff': quay_uint32_t, 'cryptsize': quay_uint32_t, 'cryptid': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_c4e1499', 'byte_order': 'quay_byte_order_0f304e2'}, '__init__')
    def __init__(quay_self_c4e1499, quay_byte_order_0f304e2='little'):
        super().__init__(byte_order=quay_byte_order_0f304e2)
        _name_boundary.attributes(quay_self_c4e1499)['cmd'] = 0
        _name_boundary.attributes(quay_self_c4e1499)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_c4e1499)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_c4e1499)['cryptoff'] = 0
        _name_boundary.attributes(quay_self_c4e1499)['cryptsize'] = 0
        _name_boundary.attributes(quay_self_c4e1499)['cryptid'] = 0

@_name_boundary.class_contract('encryption_info_command_64', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'cryptoff': 'quay_cryptoff', 'cryptsize': 'quay_cryptsize', 'cryptid': 'quay_cryptid', 'pad': 'quay_pad', 'add_field_composer': 'quay_add_field_composer'})
class quay_encryption_info_command_64(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'cryptoff': quay_uint32_t, 'cryptsize': quay_uint32_t, 'cryptid': quay_uint32_t, 'pad': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_14b2c44', 'byte_order': 'quay_byte_order_20f4cd0'}, '__init__')
    def __init__(quay_self_14b2c44, quay_byte_order_20f4cd0='little'):
        super().__init__(byte_order=quay_byte_order_20f4cd0)
        _name_boundary.attributes(quay_self_14b2c44)['cmd'] = 0
        _name_boundary.attributes(quay_self_14b2c44)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_14b2c44)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_14b2c44)['cryptoff'] = 0
        _name_boundary.attributes(quay_self_14b2c44)['cryptsize'] = 0
        _name_boundary.attributes(quay_self_14b2c44)['cryptid'] = 0
        _name_boundary.attributes(quay_self_14b2c44)['pad'] = 0

@_name_boundary.class_contract('thread_command', {'FIELDS': 'quay_FIELDS', 'cmd': 'quay_cmd', 'cmdsize': 'quay_cmdsize', 'flavor': 'quay_flavor', 'count': 'quay_count', 'add_field_composer': 'quay_add_field_composer'})
class quay_thread_command(quay_Struct):
    quay_FIELDS = {'cmd': quay_uint32_t, 'cmdsize': quay_uint32_t, 'flavor': quay_uint32_t, 'count': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_b82fb4d', 'byte_order': 'quay_byte_order_2712fbf'}, '__init__')
    def __init__(quay_self_b82fb4d, quay_byte_order_2712fbf='little'):
        super().__init__(byte_order=quay_byte_order_2712fbf)
        _name_boundary.attributes(quay_self_b82fb4d)['cmd'] = 0
        _name_boundary.attributes(quay_self_b82fb4d)['add_field_composer']('cmd', quay_cmd_composer)
        _name_boundary.attributes(quay_self_b82fb4d)['cmdsize'] = 0
        _name_boundary.attributes(quay_self_b82fb4d)['flavor'] = 0
        _name_boundary.attributes(quay_self_b82fb4d)['count'] = 0
_name_boundary.module_contract(globals(), {'dysymtab_command': 'quay_dysymtab_command', 'build_version_command': 'quay_build_version_command', 'ktool_macho': 'quay_imagequay_macho', 'rpath_command': 'quay_rpath_command', 'version_min_command': 'quay_version_min_command', 'section': 'quay_section', 'entry_point_command': 'quay_entry_point_command', 'segment_command': 'quay_segment_command', 'unk_command': 'quay_unk_command', 'symtab_command': 'quay_symtab_command', 'linkedit_data_command': 'quay_linkedit_data_command', 'dylinker_command': 'quay_dylinker_command', 'thread_command': 'quay_thread_command', 'segment_command_64': 'quay_segment_command_64', 'fat_header': 'quay_fat_header', 'uuid_command': 'quay_uuid_command', 'encryption_info_command_64': 'quay_encryption_info_command_64', 'cmd_composer': 'quay_cmd_composer', 'mach_header': 'quay_mach_header', 'symtab_entry': 'quay_symtab_entry', 'os_tuple_composer': 'quay_os_tuple_composer', 'sub_client_command': 'quay_sub_client_command', 'symtab_entry_32': 'quay_symtab_entry_32', 'mach_header_64': 'quay_mach_header_64', 'source_version_command': 'quay_source_version_command', 'encryption_info_command': 'quay_encryption_info_command', 'dylib_command': 'quay_dylib_command', 'fat_arch': 'quay_fat_arch', 'dyld_info_command': 'quay_dyld_info_command', 'section_64': 'quay_section_64', 'dylib': 'quay_dylib'})
