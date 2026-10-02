# Derived from src/ktool/image.py; original copyright and license in ORIGIN.md and LICENSE.
import imagequay_boundary as _name_boundary
from collections import namedtuple as quay_namedtuple
from enum import Enum as quay_Enum
from typing import List as quay_List, Dict as quay_Dict, Union as quay_Union
from imagequay_layout import quay_LOAD_COMMAND as quay_LOAD_COMMAND, quay_dylib_command as quay_dylib_command, quay_dyld_info_command as quay_dyld_info_command, quay_Struct as quay_Struct, quay_CPUSubTypeARM64 as quay_CPUSubTypeARM64, quay_CPUType as quay_CPUType, quay_segment_command_64 as quay_segment_command_64
from imagequay_layout.record_contract import quay_Constructable as quay_Constructable
from imagequay.signing_reader import quay_CodesignInfo as quay_CodesignInfo
from imagequay.failure_types import quay_VMAddressingError as quay_VMAddressingError, quay_MachOAlignmentError as quay_MachOAlignmentError
from imagequay.formatting import quay_bytes_to_hex as quay_bytes_to_hex, quay_uint_to_int as quay_uint_to_int, quay_Table as quay_Table, quay_get_terminal_size as quay_get_terminal_size
from imagequay_support.diagnostics import quay_log as quay_log
from imagequay.container_io import quay_Slice as quay_Slice, quay_SlicedBackingFile as quay_SlicedBackingFile, quay_MachOImageHeader as quay_MachOImageHeader, quay_Segment as quay_Segment, quay_PlatformType as quay_PlatformType, quay_ToolType as quay_ToolType
quay_os_version = _name_boundary.named_record('os_version', ['x', 'y', 'z'])
quay__fakeseg = _name_boundary.named_record('_fakeseg', ['vm_address', 'file_address', 'size'])

class _Ranges:
    """Half-open file-backed interval mapping; allocation is O(segment count)."""
    def _normalized(self, address):
        if type(address) is not int or address < 0:
            raise quay_VMAddressingError('address must be a nonnegative integer')
        if self.detag_kern_64:
            address |= 0xffff000000000000
        if self.detag_64:
            address &= 0xfffffffff
        return address

    def quay_translate(self, address):
        address = self._normalized(address)
        for virtual, (physical, size) in self.segs.items():
            if virtual <= address < virtual + size:
                return physical + address - virtual
        raise quay_VMAddressingError(f'Address {address:#x} is outside file-backed VM ranges')

    def quay_de_translate(self, file_address):
        if type(file_address) is not int or file_address < 0:
            raise quay_VMAddressingError('file address must be a nonnegative integer')
        for virtual, (physical, size) in self.segs.items():
            if physical <= file_address < physical + size:
                return virtual + file_address - physical
        raise quay_VMAddressingError(f'Could not de_translate address {file_address}')

    def quay_vm_check(self, address):
        try:
            self.quay_translate(address)
            return True
        except quay_VMAddressingError:
            return False

    def _add_range(self, physical, virtual, size):
        if any(type(value) is not int or value < 0 for value in (physical, virtual, size)):
            raise quay_VMAddressingError('VM range coordinates must be nonnegative integers')
        if virtual + size > 1 << 64 or physical + size > 1 << 64:
            raise quay_VMAddressingError('VM range overflows 64 bits')
        if size == 0:
            return
        for previous, (_, previous_size) in self.segs.items():
            if max(previous, virtual) < min(previous + previous_size, virtual + size):
                if previous == virtual and self.segs[previous] == [physical, size]:
                    return
                raise quay_VMAddressingError('overlapping virtual mappings are ambiguous')
        self.segs[virtual] = [physical, size]
        self.cache.clear()

    def __str__(self):
        table = quay_Table(dividers=True, avoid_wrapping_titles=True)
        table.titles = ['VM Start', 'VM End', 'File Start', 'File End', 'Size']
        table.size_pinned_columns = [0, 1]
        for virtual, (physical, size) in self.segs.items():
            table.rows.append([hex(virtual), hex(virtual + size), hex(physical), hex(physical + size), hex(size)])
        return table.fetch_all(quay_get_terminal_size().columns - 5)


quay_vm_obj = _name_boundary.named_record('vm_obj', ['vmaddr', 'vmend', 'size', 'fileaddr'])


@_name_boundary.class_contract('MisalignedVM', {'vm_check':'quay_vm_check', 'translate':'quay_translate', 'de_translate':'quay_de_translate', 'add_segment':'quay_add_segment', 'detag_kern_64':'quay_detag_kern_64', 'detag_64':'quay_detag_64', 'fallback':'quay_fallback', 'segs':'quay_segs', 'map':'quay_map', 'stats':'quay_stats', 'vm_base_addr':'quay_vm_base_addr', 'sorted_map':'quay_sorted_map', 'cache':'quay_cache'})
class quay_MisalignedVM(_Ranges):
    def __init__(self):
        self.detag_kern_64 = self.detag_64 = False
        self.fallback = None
        self.segs, self.map, self.stats, self.sorted_map, self.cache = {}, {}, {}, {}, {}
        self.vm_base_addr = 0

    def quay_add_segment(self, segment):
        size = getattr(segment, 'file_size', segment.size)
        self._add_range(segment.file_address, segment.vm_address, size)
        self.map[segment.vm_address] = quay_vm_obj(segment.vm_address, segment.vm_address + size, size, segment.file_address)
        if segment.file_address == 0 and size:
            self.vm_base_addr = segment.vm_address


@_name_boundary.class_contract('VM', {'vm_check':'quay_vm_check', 'add_segment':'quay_add_segment', 'translate':'quay_translate', 'de_translate':'quay_de_translate', 'map_pages':'quay_map_pages', 'page_size':'quay_page_size', 'page_size_bits':'quay_page_size_bits', 'page_table':'quay_page_table', 'tlb':'quay_tlb', 'segs':'quay_segs', 'vm_base_addr':'quay_vm_base_addr', 'dirty':'quay_dirty', 'fallback':'quay_fallback', 'detag_kern_64':'quay_detag_kern_64', 'detag_64':'quay_detag_64'})
class quay_VM(_Ranges):
    def __init__(self, page_size):
        if type(page_size) is not int or page_size <= 0 or page_size & (page_size - 1):
            raise ValueError('page_size must be a positive power of two')
        self.page_size, self.page_size_bits = page_size, page_size.bit_length() - 1
        self.page_table, self.tlb, self.segs, self.cache = {}, {}, {}, {}
        self.vm_base_addr, self.dirty = None, False
        self.fallback = quay_MisalignedVM()
        self.detag_kern_64 = self.detag_64 = False

    def quay_add_segment(self, segment):
        if segment.name == '__PAGEZERO':
            return
        size = getattr(segment, 'file_size', segment.size)
        if self.vm_base_addr is None:
            self.vm_base_addr = segment.vm_address
        # File-backed final partial pages are valid; virtual zero-fill is excluded.
        self._add_range(segment.file_address, segment.vm_address, size)
        self.fallback.quay_add_segment(quay__fakeseg(segment.vm_address, segment.file_address, size))

    def quay_map_pages(self, physical_addr, virtual_addr, size):
        if any(type(value) is not int or value < 0 for value in (physical_addr, virtual_addr, size)):
            raise quay_MachOAlignmentError('page map coordinates must be nonnegative integers')
        if any(value % self.page_size for value in (physical_addr, virtual_addr, size)):
            raise quay_MachOAlignmentError(f'Tried to map {virtual_addr:#x}+{size:#x} to {physical_addr:#x}')
        self._add_range(physical_addr, virtual_addr, size)
        self.fallback.quay_add_segment(quay__fakeseg(virtual_addr, physical_addr, size))

@_name_boundary.class_contract('LinkedImage', {'serialize': 'quay_serialize', '_get_name': 'quay__get_name', 'cmd': 'quay_cmd', 'source_image': 'quay_source_image', 'install_name': 'quay_install_name', 'weak': 'quay_weak', 'local': 'quay_local'})
class quay_LinkedImage:

    @_name_boundary.callable_contract({'self': 'quay_self_2eef63d', 'source_image': 'quay_source_image_cf91a8b', 'cmd': 'quay_cmd_31d7e86'}, '__init__')
    def __init__(quay_self_2eef63d, quay_source_image_cf91a8b: 'Image', quay_cmd_31d7e86):
        _name_boundary.attributes(quay_self_2eef63d)['cmd'] = quay_cmd_31d7e86
        _name_boundary.attributes(quay_self_2eef63d)['source_image'] = quay_source_image_cf91a8b
        _name_boundary.attributes(quay_self_2eef63d)['install_name'] = _name_boundary.attributes(quay_self_2eef63d)['_get_name'](quay_cmd_31d7e86)
        _name_boundary.attributes(quay_self_2eef63d)['weak'] = _name_boundary.attributes(quay_cmd_31d7e86)['cmd'] == _name_boundary.attributes(quay_LOAD_COMMAND.LOAD_WEAK_DYLIB)['value']
        _name_boundary.attributes(quay_self_2eef63d)['local'] = _name_boundary.attributes(quay_cmd_31d7e86)['cmd'] == _name_boundary.attributes(quay_LOAD_COMMAND.ID_DYLIB)['value']

    @_name_boundary.callable_contract({'self': 'quay_self_5e279c3'}, 'serialize')
    def quay_serialize(quay_self_5e279c3):
        return {'install_name': _name_boundary.attributes(quay_self_5e279c3)['install_name'], 'load_command': _name_boundary.attributes(quay_LOAD_COMMAND(_name_boundary.attributes(_name_boundary.attributes(quay_self_5e279c3)['cmd'])['cmd']))['name']}

    def quay__get_name(self, cmd):
        relative = cmd.dylib.name
        if relative < quay_dylib_command.size() or relative >= cmd.cmdsize:
            from imagequay.failure_types import quay_MalformedMachOException
            raise quay_MalformedMachOException('dylib name is outside its load command')
        return self.source_image.read_cstr(cmd.off + relative, limit=cmd.cmdsize - relative)

@_name_boundary.class_contract('Image', {'serialize': 'quay_serialize', 'vm_realign': 'quay_vm_realign', 'vm_check': 'quay_vm_check', 'read_uint': 'quay_read_uint', 'read_ptr': 'quay_read_ptr', 'read_int': 'quay_read_int', 'read_bytearray': 'quay_read_bytearray', 'read_struct': 'quay_read_struct', 'read_fixed_len_str': 'quay_read_fixed_len_str', 'read_cstr': 'quay_read_cstr', 'read_uleb128': 'quay_read_uleb128', 'slice': 'quay_slice', 'vm': 'quay_vm', 'base_name': 'quay_base_name', 'install_name': 'quay_install_name', 'linked_images': 'quay_linked_images', 'segments': 'quay_segments', 'info': 'quay_info', 'dylib': 'quay_dylib', 'uuid': 'quay_uuid', 'codesign_info': 'quay_codesign_info', '_codesign_cmd': 'quay__codesign_cmd', 'platform': 'quay_platform', 'allowed_clients': 'quay_allowed_clients', 'rpath': 'quay_rpath', 'minos': 'quay_minos', 'sdk_version': 'quay_sdk_version', 'imports': 'quay_imports', 'exports': 'quay_exports', 'symbols': 'quay_symbols', 'import_table': 'quay_import_table', 'export_table': 'quay_export_table', 'entry_point': 'quay_entry_point', 'function_starts': 'quay_function_starts', 'thread_state': 'quay_thread_state', '_entry_off': 'quay__entry_off', 'binding_table': 'quay_binding_table', 'weak_binding_table': 'quay_weak_binding_table', 'lazy_binding_table': 'quay_lazy_binding_table', 'export_trie': 'quay_export_trie', 'chained_fixups': 'quay_chained_fixups', 'symbol_table': 'quay_symbol_table', 'struct_cache': 'quay_struct_cache', 'macho_header': 'quay_macho_header', 'ptr_size': 'quay_ptr_size'})
class quay_Image:
    """
    This class represents the Mach-O Binary as a whole.

    It's the root object in the massive tree of information we're going to build up about the binary.

    This class on its own does not handle populating its fields.
    The Dyld class set is fittingly responsible for loading in and processing the raw values to it.

    :ivar Slice slice: Mach-O underlying Slice. This sits inbetween the Image and the underlying file.
    :ivar Union[VM, MisalignedVM] vm: VM mapping information describing how this file is loaded into memory.
        If this can't be aligned to 16kb or 4kb segments, it will contain a 'MisalignedVM', which uses
        slightly slower map lookups.
    :ivar MachOImageHeader macho_header: Mach-O Header representation for this image.
    :ivar str install_name: "Install name" of the image. Only shared libraries will have this.
    :ivar str base_name: Basename of the image, if it has one. This'll be the "filename" part of the installname
        (e.g. /usr/lib/libSystem.dylib -> libSystem.dylib)
    :ivar List[LinkedImage] linked_images: List of linked images
    :ivar Dict[str, Segment] segments: map of segment names to their respective segments
    :ivar Union[dyld_info_command, None] info: Raw content of the dyld_info_command if this image contains one
    :ivar Union[LinkedImage, None] dylib: "Identity" info of this image. This contains the info that would be used to link it within another image.
    :ivar bytearray uuid: UUID of this image.
    :ivar Union[CodesignInfo, None] codesign_info: Codesigning information for this binary.
    :ivar PlatformType platform: Platform type for the image.
    :ivar List[str] allowed_clients: List of the allowed clients for this image.
        Allowed clients are a list of executables dyld will allow to load this image.
    :ivar str rpath: rpath of the library.
    :ivar os_version minos: x.y.z Minimum OS for the library
    :ivar os_version sdk_version: x.y.z SDK version this library was linked against
    :ivar List[Symbol] imports: List of imported symbols
    :ivar List[Symbol] exports: List of exported symbols
    :ivar Dict[int, 'Symbol'] symbols: Table mapping locations to symbols in the library
    :ivar Dict[int, 'Symbol'] import_table: Table mapping locations to linked symbols in the library
    :ivar Dict[int, 'Symbol'] export_table: Table mapping locations to exported symbols in the library
    :ivar int entry_point: Extrapolated entry point for the image, pulled from either thread starts or an entry point cmd
    :ivar List[int] function_starts: List of function starts for this image
    :ivar List[int] thread_state: Initial values for registers when launching this binary.
    """

    @_name_boundary.callable_contract({'self': 'quay_self_8d86c1d', 'macho_slice': 'quay_macho_slice_a3c7e87', 'force_misaligned_vm': 'quay_force_misaligned_vm_202cfdb'}, '__init__')
    def __init__(quay_self_8d86c1d, quay_macho_slice_a3c7e87: quay_Slice, quay_force_misaligned_vm_202cfdb=False):
        """
        Create a MachO image

        :param macho_slice: MachO Slice being processed
        :type macho_slice: MachO Slice
        """
        _name_boundary.attributes(quay_self_8d86c1d)['slice']: quay_Slice = quay_macho_slice_a3c7e87
        _name_boundary.attributes(quay_self_8d86c1d)['vm'] = None
        if _name_boundary.attributes(quay_self_8d86c1d)['slice']:
            _name_boundary.attributes(quay_self_8d86c1d)['macho_header']: quay_MachOImageHeader = _name_boundary.attributes(quay_MachOImageHeader)['from_image'](macho_slice=quay_macho_slice_a3c7e87)
            if quay_force_misaligned_vm_202cfdb:
                _name_boundary.attributes(quay_self_8d86c1d)['vm'] = quay_MisalignedVM()
            else:
                _name_boundary.attributes(quay_self_8d86c1d)['vm_realign']()
            _name_boundary.attributes(quay_self_8d86c1d)['ptr_size'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_8d86c1d)['slice'])['ptr_size']
        _name_boundary.attributes(quay_self_8d86c1d)['base_name'] = ''
        _name_boundary.attributes(quay_self_8d86c1d)['install_name'] = ''
        _name_boundary.attributes(quay_self_8d86c1d)['linked_images']: quay_List[quay_LinkedImage] = []
        _name_boundary.attributes(quay_self_8d86c1d)['segments']: quay_Dict[str, quay_Segment] = {}
        _name_boundary.attributes(quay_self_8d86c1d)['info']: quay_Union[quay_dyld_info_command, None] = None
        _name_boundary.attributes(quay_self_8d86c1d)['dylib']: quay_Union[quay_LinkedImage, None] = None
        _name_boundary.attributes(quay_self_8d86c1d)['uuid'] = None
        _name_boundary.attributes(quay_self_8d86c1d)['codesign_info']: quay_Union[quay_CodesignInfo, None] = None
        _name_boundary.attributes(quay_self_8d86c1d)['_codesign_cmd'] = None
        _name_boundary.attributes(quay_self_8d86c1d)['platform']: quay_PlatformType = quay_PlatformType.UNK
        _name_boundary.attributes(quay_self_8d86c1d)['allowed_clients']: quay_List[str] = []
        _name_boundary.attributes(quay_self_8d86c1d)['rpath']: quay_Union[str, None] = None
        _name_boundary.attributes(quay_self_8d86c1d)['minos'] = quay_os_version(0, 0, 0)
        _name_boundary.attributes(quay_self_8d86c1d)['sdk_version'] = quay_os_version(0, 0, 0)
        _name_boundary.attributes(quay_self_8d86c1d)['imports']: quay_List['Symbol'] = []
        _name_boundary.attributes(quay_self_8d86c1d)['exports']: quay_List['Symbol'] = []
        _name_boundary.attributes(quay_self_8d86c1d)['symbols']: quay_Dict[int, 'Symbol'] = {}
        _name_boundary.attributes(quay_self_8d86c1d)['import_table']: quay_Dict[int, 'Symbol'] = {}
        _name_boundary.attributes(quay_self_8d86c1d)['export_table']: quay_Dict[int, 'Symbol'] = {}
        _name_boundary.attributes(quay_self_8d86c1d)['entry_point'] = 0
        _name_boundary.attributes(quay_self_8d86c1d)['function_starts']: quay_List[int] = []
        _name_boundary.attributes(quay_self_8d86c1d)['thread_state']: quay_List[int] = []
        _name_boundary.attributes(quay_self_8d86c1d)['_entry_off'] = 0
        _name_boundary.attributes(quay_self_8d86c1d)['binding_table'] = None
        _name_boundary.attributes(quay_self_8d86c1d)['weak_binding_table'] = None
        _name_boundary.attributes(quay_self_8d86c1d)['lazy_binding_table'] = None
        _name_boundary.attributes(quay_self_8d86c1d)['export_trie'] = None
        _name_boundary.attributes(quay_self_8d86c1d)['chained_fixups'] = None
        _name_boundary.attributes(quay_self_8d86c1d)['symbol_table'] = None
        _name_boundary.attributes(quay_self_8d86c1d)['struct_cache']: quay_Dict[int, quay_Struct] = {}

    @_name_boundary.callable_contract({'self': 'quay_self_5a47171'}, 'serialize')
    def quay_serialize(quay_self_5a47171):
        quay_image_dict_7e54097 = {'macho_header': _name_boundary.attributes(_name_boundary.attributes(quay_self_5a47171)['macho_header'])['serialize']()}
        if _name_boundary.attributes(quay_self_5a47171)['install_name'] != '':
            quay_image_dict_7e54097['install_name'] = _name_boundary.attributes(quay_self_5a47171)['install_name']
        quay_linked_6a01c14 = []
        for quay_ext_dylib_14fd564 in _name_boundary.attributes(quay_self_5a47171)['linked_images']:
            quay_linked_6a01c14.append(_name_boundary.attributes(quay_ext_dylib_14fd564)['serialize']())
        quay_image_dict_7e54097['linked'] = quay_linked_6a01c14
        quay_segments_e2e393c = {}
        for quay_seg_name_0a2dfc0, quay_seg_f3c3ea4 in _name_boundary.attributes(_name_boundary.attributes(quay_self_5a47171)['segments'])['items']():
            quay_segments_e2e393c[quay_seg_name_0a2dfc0] = _name_boundary.attributes(quay_seg_f3c3ea4)['serialize']()
        quay_image_dict_7e54097['segments'] = quay_segments_e2e393c
        if _name_boundary.attributes(quay_self_5a47171)['uuid']:
            quay_image_dict_7e54097['uuid'] = quay_bytes_to_hex(_name_boundary.attributes(quay_self_5a47171)['uuid'])
        quay_image_dict_7e54097['platform'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_5a47171)['platform'])['name']
        quay_image_dict_7e54097['allowed-clients'] = _name_boundary.attributes(quay_self_5a47171)['allowed_clients']
        if _name_boundary.attributes(quay_self_5a47171)['rpath']:
            quay_image_dict_7e54097['rpath'] = _name_boundary.attributes(quay_self_5a47171)['rpath']
        quay_image_dict_7e54097['imports'] = [_name_boundary.attributes(quay_sym_276afc9)['serialize']() for quay_sym_276afc9 in _name_boundary.attributes(quay_self_5a47171)['imports']]
        quay_image_dict_7e54097['exports'] = [_name_boundary.attributes(quay_sym_3faa973)['serialize']() for quay_sym_3faa973 in _name_boundary.attributes(quay_self_5a47171)['exports']]
        quay_image_dict_7e54097['symbols'] = [_name_boundary.attributes(quay_sym_4abc826)['serialize']() for quay_sym_4abc826 in _name_boundary.attributes(quay_self_5a47171)['symbols'].values()]
        quay_image_dict_7e54097['entry_point'] = _name_boundary.attributes(quay_self_5a47171)['entry_point']
        quay_image_dict_7e54097['function_starts'] = _name_boundary.attributes(quay_self_5a47171)['function_starts']
        quay_image_dict_7e54097['thread_state'] = _name_boundary.attributes(quay_self_5a47171)['thread_state']
        quay_image_dict_7e54097['minos'] = f"{_name_boundary.attributes(_name_boundary.attributes(quay_self_5a47171)['minos'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_self_5a47171)['minos'])['y']}{_name_boundary.attributes(quay_self_5a47171)['minos'].z}"
        quay_image_dict_7e54097['sdk_version'] = f"{_name_boundary.attributes(_name_boundary.attributes(quay_self_5a47171)['sdk_version'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_self_5a47171)['sdk_version'])['y']}.{_name_boundary.attributes(quay_self_5a47171)['sdk_version'].z}"
        return quay_image_dict_7e54097

    @_name_boundary.callable_contract({'self': 'quay_self_e6f41a7', 'yell_about_misalignment': 'quay_yell_about_misalignment_5c0a5ee'}, 'vm_realign')
    def quay_vm_realign(quay_self_e6f41a7, quay_yell_about_misalignment_5c0a5ee=True):
        quay_align_by_12519f7 = 16384
        quay_aligned_2b1d7fd = False
        quay_detag_64_7bef3c2 = False
        quay_segs_a94ba7d = []
        for quay_cmd_d2b6228 in _name_boundary.attributes(_name_boundary.attributes(quay_self_e6f41a7)['macho_header'])['load_commands']:
            if _name_boundary.attributes(quay_cmd_d2b6228)['cmd'] in [_name_boundary.attributes(quay_LOAD_COMMAND.SEGMENT)['value'], _name_boundary.attributes(quay_LOAD_COMMAND.SEGMENT_64)['value']]:
                quay_segs_a94ba7d.append(quay_cmd_d2b6228)
            if _name_boundary.attributes(quay_cmd_d2b6228)['cmd'] == quay_LOAD_COMMAND.LC_DYLD_CHAINED_FIXUPS:
                quay_detag_64_7bef3c2 = True
        if _name_boundary.attributes(_name_boundary.attributes(quay_self_e6f41a7)['slice'])['type'] == quay_CPUType.ARM64 and _name_boundary.attributes(_name_boundary.attributes(quay_self_e6f41a7)['slice'])['subtype'] == quay_CPUSubTypeARM64.ARM64E:
            quay_detag_64_7bef3c2 = True
        while not quay_aligned_2b1d7fd:
            quay_aligned_2b1d7fd = True
            for quay_cmd_d2b6228 in quay_segs_a94ba7d:
                quay_cmd_d2b6228: quay_segment_command_64 = quay_cmd_d2b6228
                if _name_boundary.attributes(quay_cmd_d2b6228)['vmaddr'] % quay_align_by_12519f7 != 0:
                    if quay_align_by_12519f7 == 16384:
                        quay_align_by_12519f7 = 4096
                        quay_aligned_2b1d7fd = False
                        break
                    else:
                        quay_align_by_12519f7 = 0
                        quay_aligned_2b1d7fd = True
                        break
        if quay_align_by_12519f7 != 0:
            _name_boundary.attributes(quay_log)['info'](f'Aligned to {hex(quay_align_by_12519f7)} pages')
            _name_boundary.attributes(quay_self_e6f41a7)['vm']: quay_VM = quay_VM(page_size=quay_align_by_12519f7)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_e6f41a7)['vm'])['detag_64'] = quay_detag_64_7bef3c2
        else:
            if quay_yell_about_misalignment_5c0a5ee:
                _name_boundary.attributes(quay_log)['info']('MachO cannot be aligned to 16k or 4k pages. Swapping to fallback mapping.')
            _name_boundary.attributes(quay_self_e6f41a7)['vm']: quay_MisalignedVM = quay_MisalignedVM()
            _name_boundary.attributes(_name_boundary.attributes(quay_self_e6f41a7)['vm'])['detag_64'] = quay_detag_64_7bef3c2

    @_name_boundary.callable_contract({'self': 'quay_self_256b29f', 'address': 'quay_address_3aa2588'}, 'vm_check')
    def quay_vm_check(quay_self_256b29f, quay_address_3aa2588):
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_256b29f)['vm'])['vm_check'](quay_address_3aa2588)

    @_name_boundary.callable_contract({'self': 'quay_self_530a811', 'offset': 'quay_offset_7cf468a', 'length': 'quay_length_287c888', 'vm': 'quay_vm_f26fb2d'}, 'read_uint')
    def quay_read_uint(quay_self_530a811, quay_offset_7cf468a: int, quay_length_287c888: int, quay_vm_f26fb2d=False):
        """
        Get a sequence of bytes (as an int) from a location

        :param offset: Offset within the image
        :param length: Amount of bytes to get
        :param vm: Is `offset` a VM address
        :param section_name: Section Name if vm==True (improves translation time slightly)
        :return: `length` Bytes at `offset`
        """
        if quay_vm_f26fb2d:
            quay_offset_7cf468a = _name_boundary.attributes(_name_boundary.attributes(quay_self_530a811)['vm'])['translate'](quay_offset_7cf468a)
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_530a811)['slice'])['read_uint'](quay_offset_7cf468a, quay_length_287c888)

    @_name_boundary.callable_contract({'self': 'quay_self_03f17d9', 'offset': 'quay_offset_1df7120', 'vm': 'quay_vm_bb07aed'}, 'read_ptr')
    def quay_read_ptr(quay_self_03f17d9, quay_offset_1df7120: int, quay_vm_bb07aed=False):
        """ Read a ptr (uint of size self.ptr_size)

        :param offset:
        :param vm:
        """
        return _name_boundary.attributes(quay_self_03f17d9)['read_uint'](quay_offset_1df7120, _name_boundary.attributes(quay_self_03f17d9)['ptr_size'], vm=quay_vm_bb07aed)

    @_name_boundary.callable_contract({'self': 'quay_self_f65d0e4', 'offset': 'quay_offset_dde5bb4', 'length': 'quay_length_128e486', 'vm': 'quay_vm_c39153e'}, 'read_int')
    def quay_read_int(quay_self_f65d0e4, quay_offset_dde5bb4: int, quay_length_128e486: int, quay_vm_c39153e=False):
        return quay_uint_to_int(_name_boundary.attributes(quay_self_f65d0e4)['read_uint'](quay_offset_dde5bb4, quay_length_128e486, quay_vm_c39153e), quay_length_128e486 * 8)

    @_name_boundary.callable_contract({'self': 'quay_self_d3cf1be', 'offset': 'quay_offset_fe692ef', 'length': 'quay_length_01b57fa', 'vm': 'quay_vm_eebc4a8'}, 'read_bytearray')
    def quay_read_bytearray(quay_self_d3cf1be, quay_offset_fe692ef: int, quay_length_01b57fa: int, quay_vm_eebc4a8=False) -> bytearray:
        """
        Get a sequence of bytes from a location

        :param offset: Offset within the image
        :param length: Amount of bytes to get
        :param vm: Is `offset` a VM address
        :param section_name: Section Name if vm==True (improves translation time slightly)
        :return: `length` Bytes at `offset`
        """
        if quay_vm_eebc4a8:
            quay_offset_fe692ef = _name_boundary.attributes(_name_boundary.attributes(quay_self_d3cf1be)['vm'])['translate'](quay_offset_fe692ef)
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_d3cf1be)['slice'])['read_bytearray'](quay_offset_fe692ef, quay_length_01b57fa)

    def quay_read_struct(self, address, struct_type, vm=False, endian=None, force_reload=False):
        physical = self.vm.translate(address) if vm else address
        order = endian or self.slice.byte_order
        key = (physical, struct_type, order, self.ptr_size, self.slice.file._generation)
        if force_reload or key not in self.struct_cache:
            self.struct_cache[key] = self.slice.read_struct(physical, struct_type, order)
        return self.struct_cache[key]

    @_name_boundary.callable_contract({'self': 'quay_self_bf4acac', 'address': 'quay_address_4c02936', 'count': 'quay_count_286e367', 'vm': 'quay_vm_085f2ed', 'force': 'quay_force_9517485'}, 'read_fixed_len_str')
    def quay_read_fixed_len_str(quay_self_bf4acac, quay_address_4c02936: int, quay_count_286e367: int, quay_vm_085f2ed=False, quay_force_9517485=False):
        """
        Get string with set length from location (to be used essentially only for loading segment names)

        :param address: Address of string start
        :param count: Length of string
        :param vm: Is `address` a VM address?
        :param force: Force reading non-ascii data into the str. Failed decodes will be rendered as `?`.
            This is slightly slower than ascii reads due to python jank.
        :return: The loaded string.
        """
        if quay_vm_085f2ed:
            quay_address_4c02936 = _name_boundary.attributes(_name_boundary.attributes(quay_self_bf4acac)['vm'])['translate'](quay_address_4c02936)
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_bf4acac)['slice'])['read_fixed_len_str'](quay_address_4c02936, quay_count_286e367, force=quay_force_9517485)

    @_name_boundary.callable_contract({'self': 'quay_self_6de66b4', 'address': 'quay_address_4d97322', 'limit': 'quay_limit_0268a81', 'vm': 'quay_vm_c98d2ab'}, 'read_cstr')
    def quay_read_cstr(quay_self_6de66b4, quay_address_4d97322: int, quay_limit_0268a81: int=0, quay_vm_c98d2ab=False):
        """
        Load a C style string from a location, stopping once a null byte is encountered.

        :param address: Address to load string from
        :param limit: Limit of the length of bytes, 0 = unlimited
        :param vm: Is `address` a VM address?
        :return: The loaded C string
        """
        if quay_vm_c98d2ab:
            quay_address_4d97322 = _name_boundary.attributes(_name_boundary.attributes(quay_self_6de66b4)['vm'])['translate'](quay_address_4d97322)
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_6de66b4)['slice'])['read_cstr'](quay_address_4d97322, quay_limit_0268a81)

    @_name_boundary.callable_contract({'self': 'quay_self_87ebfad', 'read_head': 'quay_read_head_30db81b'}, 'read_uleb128')
    def quay_read_uleb128(quay_self_87ebfad, quay_read_head_30db81b: int):
        """
        Decode a uleb128 integer from a location

        :param read_head: Start location
        :return: (end location, value)
        """
        return _name_boundary.attributes(_name_boundary.attributes(quay_self_87ebfad)['slice'])['read_uleb128'](quay_read_head_30db81b)
_name_boundary.module_contract(globals(), {'ToolType': 'quay_ToolType', 'Table': 'quay_Table', 'CPUType': 'quay_CPUType', 'VM': 'quay_VM', 'Image': 'quay_Image', 'get_terminal_size': 'quay_get_terminal_size', 'Union': 'quay_Union', 'MachOImageHeader': 'quay_MachOImageHeader', 'namedtuple': 'quay_namedtuple', 'PlatformType': 'quay_PlatformType', 'segment_command_64': 'quay_segment_command_64', 'MisalignedVM': 'quay_MisalignedVM', 'LOAD_COMMAND': 'quay_LOAD_COMMAND', 'Constructable': 'quay_Constructable', '_fakeseg': 'quay__fakeseg', 'Slice': 'quay_Slice', 'Struct': 'quay_Struct', 'SlicedBackingFile': 'quay_SlicedBackingFile', 'Enum': 'quay_Enum', 'List': 'quay_List', 'VMAddressingError': 'quay_VMAddressingError', 'vm_obj': 'quay_vm_obj', 'CPUSubTypeARM64': 'quay_CPUSubTypeARM64', 'Dict': 'quay_Dict', 'dylib_command': 'quay_dylib_command', 'MachOAlignmentError': 'quay_MachOAlignmentError', 'Segment': 'quay_Segment', 'LinkedImage': 'quay_LinkedImage', 'os_version': 'quay_os_version', 'dyld_info_command': 'quay_dyld_info_command', 'bytes_to_hex': 'quay_bytes_to_hex', 'CodesignInfo': 'quay_CodesignInfo', 'uint_to_int': 'quay_uint_to_int', 'log': 'quay_log'})
