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
from imagequay.byte_region import ByteRegion
from imagequay.failure_types import quay_MalformedMachOException
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
    def quay__parse_load_commands(cls, image, load_symtab=True, load_imports=True, load_exports=True):
        """Register address/library facts before interpreting dependent metadata."""
        deferred = []
        for cmd in image.macho_header.load_commands:
            try:
                kind = quay_LOAD_COMMAND(cmd.cmd)
            except ValueError:
                continue
            if kind in (quay_LOAD_COMMAND.SEGMENT, quay_LOAD_COMMAND.SEGMENT_64):
                segment = quay_Segment(image, cmd)
                if segment.name in image.segments:
                    raise quay_MalformedMachOException('duplicate segment names make metadata addressing ambiguous')
                try:
                    image.vm.add_segment(segment)
                except quay_MachOAlignmentError:
                    image.vm = image.vm.fallback
                    image.vm.add_segment(segment)
                image.segments[segment.name] = segment
            elif isinstance(cmd, quay_dylib_command):
                linked = quay_LinkedImage(image, cmd)
                if kind == quay_LOAD_COMMAND.ID_DYLIB:
                    image.dylib = linked
                else:
                    image.linked_images.append(linked)
            elif kind == quay_LOAD_COMMAND.UUID:
                image.uuid = cmd.uuid
            elif kind == quay_LOAD_COMMAND.MAIN:
                image._entry_off = cmd.entryoff
            elif kind in (quay_LOAD_COMMAND.SUB_CLIENT, quay_LOAD_COMMAND.RPATH):
                relative = cmd.offset if kind == quay_LOAD_COMMAND.SUB_CLIENT else cmd.path
                if relative < 12 or relative >= cmd.cmdsize:
                    raise quay_MalformedMachOException('load-command string lies outside its command')
                text = image.read_cstr(cmd.off+relative, limit=cmd.cmdsize-relative)
                if kind == quay_LOAD_COMMAND.SUB_CLIENT:
                    image.allowed_clients.append(text)
                else:
                    image.rpath = text
            elif kind == quay_LOAD_COMMAND.BUILD_VERSION:
                if cmd.ntools > (cmd.cmdsize-quay_build_version_command.size())//8:
                    raise quay_MalformedMachOException('build tool count exceeds its load command')
                try:
                    image.platform = quay_PlatformType(cmd.platform)
                except ValueError:
                    image.platform = quay_PlatformType.UNK
                image.platform_id = cmd.platform
                image.minos = quay_os_version(x=(cmd.minos >> 16) & 0xffff, y=(cmd.minos >> 8) & 255, z=cmd.minos & 255)
                image.sdk_version = quay_os_version(x=(cmd.sdk >> 16) & 0xffff, y=(cmd.sdk >> 8) & 255, z=cmd.sdk & 255)
            elif isinstance(cmd, quay_version_min_command):
                platforms = {quay_LOAD_COMMAND.VERSION_MIN_MACOSX: quay_PlatformType.MACOS,
                    quay_LOAD_COMMAND.VERSION_MIN_IPHONEOS: quay_PlatformType.IOS,
                    quay_LOAD_COMMAND.VERSION_MIN_TVOS: quay_PlatformType.TVOS,
                    quay_LOAD_COMMAND.VERSION_MIN_WATCHOS: quay_PlatformType.WATCHOS}
                if image.platform == quay_PlatformType.UNK:
                    image.platform = platforms.get(kind, quay_PlatformType.UNK)
                    version = cmd.version
                    image.minos = quay_os_version(x=(version >> 16) & 0xffff, y=(version >> 8) & 255, z=version & 255)
            elif kind in (quay_LOAD_COMMAND.THREAD, quay_LOAD_COMMAND.UNIXTHREAD):
                # Preserve the first register flavor; validate every declared flavor.
                cursor, endpoint, first = cmd.off+8, cmd.off+cmd.cmdsize, True
                while cursor < endpoint:
                    if endpoint-cursor < 8:
                        raise quay_MalformedMachOException('thread-state flavor header is truncated')
                    count = image.read_uint(cursor+4, 4)
                    cursor += 8
                    if count > (1 << 20):
                        raise quay_MalformedMachOException('thread-state count exceeds its 1048576-word budget')
                    if count > (endpoint-cursor)//4:
                        raise quay_MalformedMachOException('thread-state count exceeds its load command')
                    if first:
                        image.thread_state = [image.read_uint(cursor+4*i, 4) for i in range(count)]
                        first = False
                    cursor += count*4
            else:
                deferred.append((kind, cmd))
        # All local VM mappings and library ordinals now exist, regardless of LC order.
        for kind, cmd in deferred:
            if kind == quay_LOAD_COMMAND.CODE_SIGNATURE:
                image._codesign_cmd = cmd
                image.codesign_info = quay_CodesignInfo.from_image(image, cmd)
            elif kind in (quay_LOAD_COMMAND.DYLD_INFO, quay_LOAD_COMMAND.DYLD_INFO_ONLY):
                image.info = cmd
                if load_imports:
                    image.binding_table = quay_BindingTable(image, cmd.bind_off, cmd.bind_size)
                    image.weak_binding_table = quay_BindingTable(image, cmd.weak_bind_off, cmd.weak_bind_size, kind='weak')
                    image.lazy_binding_table = quay_BindingTable(image, cmd.lazy_bind_off, cmd.lazy_bind_size, kind='lazy')
                if load_exports:
                    image.export_trie = quay_ExportTrie.from_image(image, cmd.export_off, cmd.export_size)
            elif kind == quay_LOAD_COMMAND.LC_DYLD_CHAINED_FIXUPS and load_imports:
                image.chained_fixups = quay_ChainedFixups.from_image(image, cmd)
            elif kind == quay_LOAD_COMMAND.LC_DYLD_EXPORTS_TRIE and load_exports:
                image.export_trie = quay_ExportTrie.from_image(image, cmd.dataoff, cmd.datasize)
            elif kind == quay_LOAD_COMMAND.SYMTAB and load_symtab:
                image.symbol_table = _name_boundary.read_attribute(cls, 'SYMTAB_LOADER')(image, cmd)
            elif kind == quay_LOAD_COMMAND.FUNCTION_STARTS:
                region = ByteRegion(image, cmd.dataoff, cmd.datasize)
                cursor, address = region.start, image.vm.vm_base_addr
                if address is None:
                    raise quay_MalformedMachOException('function starts require a local VM base')
                while cursor < region.end:
                    region.use()
                    delta, cursor = region.leb(cursor)
                    if not delta:
                        if any(region.bytes(cursor, region.end-cursor)):
                            raise quay_MalformedMachOException('nonzero data follows the function-starts terminator')
                        break
                    if delta > (1 << 64)-1-address:
                        raise quay_MalformedMachOException('function-start address exceeds 64 bits')
                    address += delta
                    image.function_starts.append(address)

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
            minimum = 4 if quay_image_466e9b4.macho_header.is64 else 2
            if len(quay_image_466e9b4.thread_state) < minimum:
                raise quay_MalformedMachOException('thread state is too short for the inherited entry-point interpretation')
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
    def quay_from_image(cls, image, cmd, entry):
        strings = ByteRegion(image, cmd.stroff, cmd.strsize)
        if entry.str_index >= cmd.strsize:
            raise quay_MalformedMachOException('symbol string index leaves its string table')
        try:
            fullname, _ = strings.cstring(strings.start+entry.str_index)
        except UnicodeError as error:
            raise quay_MalformedMachOException('symbol name is not UTF-8') from error
        symbol = cls.from_values(fullname, entry.value, external=bool(entry.type & 1))
        symbol.entry = entry
        symbol.debug, symbol.private_external = bool(entry.type & 0xe0), bool(entry.type & 0x10)
        symbol.library_ordinal = (entry.desc >> 8) & 255
        symbol.types = [{0: 'N_UNDF', 2: 'N_ABS', 0xe: 'N_SECT', 0xc: 'N_PBUD', 0xa: 'N_INDR'}.get(entry.type & 0xe, 'N_UNKNOWN')]
        if (entry.type & 0xe) == 0xa:
            if entry.value >= cmd.strsize:
                raise quay_MalformedMachOException('indirect symbol name leaves its string table')
            symbol.indirect_name, _ = strings.cstring(strings.start+entry.value)
        return symbol

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

@_name_boundary.class_contract('SymbolTable', {name: 'quay_'+name for name in ('image', 'cmd', 'ext', 'table', '_load_symbol_table')})
class quay_SymbolTable:
    """Bounded nlist records and strings from their separate declared regions."""
    def __init__(self, image, cmd):
        self.image, self.cmd, self.ext = image, cmd, []
        self.table = self._load_symbol_table()

    def quay__load_symbol_table(self):
        entry_type = quay_symtab_entry if self.image.macho_header.is64 else quay_symtab_entry_32
        width = entry_type.size()
        entries = ByteRegion(self.image, self.cmd.symoff, self.cmd.nsyms*width)
        strings = ByteRegion(self.image, self.cmd.stroff, self.cmd.strsize)
        entries.use(self.cmd.nsyms)
        table = []
        for index in range(self.cmd.nsyms):
            entry = self.image.read_struct(entries.start+index*width, entry_type)
            symbol = quay_Symbol.from_image(self.image, self.cmd, entry)
            table.append(symbol)
            if symbol.external:
                self.ext.append(symbol)
        return table

from imagequay.chained_reader import quay_ChainedFixups
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

@_name_boundary.class_contract('ExportTrie', {'from_values':'quay_from_values', 'raw_bytes':'quay_raw_bytes', 'from_image':'quay_from_image', '_read_node_tree_iter':'quay__read_node_tree_iter', 'print_tree':'quay_print_tree', 'raw':'quay_raw', 'nodes':'quay_nodes', 'symbols':'quay_symbols', 'root':'quay_root'})
class quay_ExportTrie(quay_Constructable):
    def __init__(self):
        self.raw, self.nodes, self.symbols, self.root = bytearray(), [], [], None

    @classmethod
    def quay_from_values(cls, *args, **kwargs):
        raise NotImplementedError('export trie construction is not implemented')

    def quay_raw_bytes(self):
        return self.raw

    @classmethod
    def quay_from_image(cls, image, export_start, export_size):
        from imagequay.byte_region import ByteRegion
        result = cls()
        if not export_size:
            return result
        region = ByteRegion(image, export_start, export_size)
        result.root = cls._decode(region)
        stack = [result.root]
        while stack:
            node = stack.pop()
            if node.offset is not None:
                result.nodes.append(quay_export_node(node.name, node.offset, node.flags))
                symbol = quay_Symbol.from_values(node.name, node.offset, False)
                symbol.reexport_ordinal = getattr(node, 'reexport_ordinal', None)
                symbol.reexport_name = getattr(node, 'reexport_name', None)
                symbol.resolver_offset = getattr(node, 'resolver_offset', None)
                result.symbols.append(symbol)
            stack.extend(node.children[::-1])
        result.raw = image.read_bytearray(export_start, export_size)
        return result

    @classmethod
    def _decode(cls, region):
        from imagequay.failure_types import quay_MalformedMachOException
        root = quay_ExportNode('', None, None)
        stack = [(root, region.start, False)]
        active = set()
        names_budget = 64 << 20
        while stack:
            node, cursor, closing = stack.pop()
            if closing:
                active.remove(cursor)
                continue
            region.use()
            if cursor in active:
                raise quay_MalformedMachOException('export trie contains a cycle')
            if len(active) >= 4096:
                raise quay_MalformedMachOException('export trie exceeds the 4096-node path depth budget')
            if not region.start <= cursor < region.end:
                raise quay_MalformedMachOException('export trie child lies outside its region')
            active.add(cursor)
            stack.append((node, cursor, True))
            terminal_size, terminal = region.leb(cursor)
            if terminal_size > region.end - terminal:
                raise quay_MalformedMachOException('export terminal exceeds its region')
            child_start = terminal + terminal_size
            if terminal_size:
                flags, terminal_cursor = region.leb(terminal, endpoint=child_start)
                node.flags = flags
                if flags & 8:  # EXPORT_SYMBOL_FLAGS_REEXPORT
                    node.reexport_ordinal, terminal_cursor = region.leb(terminal_cursor, endpoint=child_start)
                    node.reexport_name, terminal_cursor = region.cstring(terminal_cursor, endpoint=child_start)
                    node.offset = 0  # Reexports carry an ordinal/name, not a local address.
                else:
                    node.offset, terminal_cursor = region.leb(terminal_cursor, endpoint=child_start)
                    if flags & 16:  # EXPORT_SYMBOL_FLAGS_STUB_AND_RESOLVER
                        node.resolver_offset, terminal_cursor = region.leb(terminal_cursor, endpoint=child_start)
                if terminal_cursor != child_start:
                    raise quay_MalformedMachOException('export terminal fields and length disagree')
            branches = region.uint(child_start, 1)
            cursor = child_start + 1
            edges = []
            for _ in range(branches):
                text, cursor = region.cstring(cursor)
                relative, cursor = region.leb(cursor)
                if not relative or relative >= region.end - region.start:
                    raise quay_MalformedMachOException('export child offset is outside its region')
                if not text or len((node.name + text).encode('utf-8')) > 1 << 20:
                    raise quay_MalformedMachOException('export path is empty or exceeds the 1 MiB name budget')
                edges.append((text, relative))
            # Preserve inherited traversal ordering while each path has a cycle guard.
            for text, relative in reversed(edges):
                child_name = node.name + text
                names_budget -= len(child_name.encode('utf-8'))
                if names_budget < 0:
                    raise quay_MalformedMachOException('export trie names exceed the 64 MiB aggregate budget')
                child = quay_ExportNode(child_name, None, None)
                node.children.append(child)
                stack.append((child, region.start + relative, False))
        return root

    @classmethod
    def quay__read_node_tree_iter(cls, image, trie_start, endpoint):
        from imagequay.byte_region import ByteRegion
        return cls._decode(ByteRegion(image, trie_start, endpoint - trie_start))

    def quay_print_tree(self):
        if not self.root:
            print('<empty export trie>')
            return
        stack = [(self.root, '', True)]
        while stack:
            node, prefix, last = stack.pop()
            label = repr(node.name) if node.name else '<root>'
            if node.offset is not None:
                label += f' (offset=0x{node.offset:x}, flags=0x{node.flags:x})'
            print(prefix + ('└── ' if last else '├── ') + label)
            child_prefix = prefix + ('    ' if last else '│   ')
            for index, child in enumerate(reversed(node.children)):
                stack.append((child, child_prefix, index == 0))

quay_action = _name_boundary.named_record('action', ['vmaddr', 'libname', 'item'])
quay_record = _name_boundary.named_record('record', ['off', 'seg_index', 'seg_offset', 'lib_ordinal', 'type', 'flags', 'name', 'addend', 'special_dylib'])

from imagequay.binding_reader import quay_BindingTable, quay_action, quay_record
_name_boundary.module_contract(globals(), {'action': 'quay_action', 'MH_MAGIC_64': 'quay_MH_MAGIC_64', 'macho_is_malformed': 'quay_macho_is_malformed', 'ExportTrie': 'quay_ExportTrie', 'CPUType': 'quay_CPUType', 'CodesignInfo': 'quay_CodesignInfo', 'Image': 'quay_Image', 'Tuple': 'quay_Tuple', 'ExportNode': 'quay_ExportNode', 'MH_FLAGS': 'quay_MH_FLAGS', 'Union': 'quay_Union', 'ignore': 'quay_ignore', 'MachOImageLoader': 'quay_MachOImageLoader', 'MachOImageHeader': 'quay_MachOImageHeader', 'ChainedFixups': 'quay_ChainedFixups', 'namedtuple': 'quay_namedtuple', 'PlatformType': 'quay_PlatformType', 'BIND_SUBOPCODE_THREADED_SET_BIND_ORDINAL_TABLE_SIZE_ULEB': 'quay_BIND_SUBOPCODE_THREADED_SET_BIND_ORDINAL_TABLE_SIZE_ULEB', 'MisalignedVM': 'quay_MisalignedVM', 'BindingTable': 'quay_BindingTable', 'export_node': 'quay_export_node', 'LOAD_COMMAND': 'quay_LOAD_COMMAND', 'BINDING_OPCODE': 'quay_BINDING_OPCODE', 'BIND_SUBOPCODE_THREADED_APPLY': 'quay_BIND_SUBOPCODE_THREADED_APPLY', 'Constructable': 'quay_Constructable', 'ktool': 'quay_imagequay', 'SymbolTable': 'quay_SymbolTable', 'Slice': 'quay_Slice', 'record': 'quay_record', 'SymbolType': 'quay_SymbolType', 'Optional': 'quay_Optional', 'LOAD_COMMAND_MAP': 'quay_LOAD_COMMAND_MAP', 'List': 'quay_List', 'LinkedImage': 'quay_LinkedImage', 'CPUSubTypeARM64': 'quay_CPUSubTypeARM64', 'Dict': 'quay_Dict', 'Segment': 'quay_Segment', 'MachOAlignmentError': 'quay_MachOAlignmentError', 'Symbol': 'quay_Symbol', 'MH_FILETYPE': 'quay_MH_FILETYPE', 'os_version': 'quay_os_version', 'bytes_to_hex': 'quay_bytes_to_hex', 'MH_MAGIC': 'quay_MH_MAGIC', 'log': 'quay_log'})
