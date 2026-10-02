# Derived from ktool; Copyright (c) 0cyn 2021. MIT license in LICENSE.
# ImageQuay rewrites the container/byte boundary and header editing architecture.
"""Bounded snapshots, exact range reads and lossless Mach-O header editing.

Caller data is never mapped or modified on disk. Editing works on private bytes;
all read and patch coordinates are checked before any change. `use_mmaped_io`
is accepted for API compatibility and uses the same snapshot backend.
"""
import os as quay_os
import stat
from enum import Enum as quay_Enum
from io import BytesIO as quay_BytesIO
from typing import Tuple as quay_Tuple, Dict as quay_Dict, Union as quay_Union, BinaryIO as quay_BinaryIO, List as quay_List
import imagequay_boundary as _name_boundary
from imagequay_layout import *
from imagequay_layout.binary_records import *
from imagequay_layout.record_contract import quay_Constructable
from imagequay_layout.command_models import quay_SegmentLoadCommand
from imagequay.failure_types import *
from imagequay_support.diagnostics import quay_log
from imagequay.formatting import quay_ignore

MAX_INPUT_BYTES = 1 << 30
MAX_ARCHITECTURES = 4096
quay_mmap = None


def checked_range(size, address, count, label='binary range'):
    if type(address) is not int or type(count) is not int or address < 0 or count < 0:
        raise quay_MalformedMachOException(f'{label}: coordinates must be nonnegative integers')
    if address > size or count > size - address:
        raise quay_MalformedMachOException(f'{label}: outside the {size}-byte container')
    return address, address + count


def snapshot(fp):
    """Read a finite seekable stream or regular descriptor, checking concurrent changes."""
    initial = None
    try:
        descriptor = fp.fileno()
    except (AttributeError, OSError, ValueError):
        descriptor = None
    if descriptor is not None:
        initial = quay_os.fstat(descriptor)
        if not stat.S_ISREG(initial.st_mode):
            raise quay_MalformedMachOException('input descriptor must be a regular file')
        size = initial.st_size
    else:
        if not hasattr(fp, 'seek') or not hasattr(fp, 'tell'):
            raise quay_MalformedMachOException('input must be a finite seekable binary stream')
        position = fp.tell()
        fp.seek(0, quay_os.SEEK_END)
        size = fp.tell()
        fp.seek(position)
    if size < 0 or size > MAX_INPUT_BYTES:
        raise quay_MalformedMachOException('input exceeds the 1 GiB snapshot budget')
    result = bytearray()
    fp.seek(0)
    while len(result) < size:
        chunk = fp.read(min(1 << 20, size - len(result)))
        if not isinstance(chunk, (bytes, bytearray)) or not chunk:
            raise quay_MalformedMachOException('input ended before its advertised length')
        if len(chunk) > size - len(result):
            raise quay_MalformedMachOException('binary stream returned more bytes than requested')
        result.extend(chunk)
    if fp.read(1):
        raise quay_MalformedMachOException('input grew while its snapshot was being read')
    if initial is not None:
        final = quay_os.fstat(descriptor)
        before = (initial.st_dev, initial.st_ino, initial.st_size, initial.st_mtime_ns, initial.st_ctime_ns)
        after = (final.st_dev, final.st_ino, final.st_size, final.st_mtime_ns, final.st_ctime_ns)
        if before != after:
            raise quay_MalformedMachOException('input changed while its snapshot was being read')
    return result


@_name_boundary.class_contract('MachOFileType', {})
class quay_MachOFileType(quay_Enum):
    FAT = 0
    THIN = 1


class _ByteStore:
    def quay_read_bytes(self, location, count):
        start, end = checked_range(self.size, location, count)
        return bytes(self.file[start:end])

    def quay_read_int(self, location, count, endian='big'):
        return int.from_bytes(self.quay_read_bytes(location, count), endian)

    def quay_write(self, location, data):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError('patch must contain bytes')
        data = bytes(data)
        start, end = checked_range(self.size, location, len(data), 'patch')
        self.file[start:end] = data
        self._generation += 1


@_name_boundary.class_contract('BackingFile', {'read_bytes':'quay_read_bytes', 'read_int':'quay_read_int', 'write':'quay_write', 'close':'quay_close', 'fp':'quay_fp', 'name':'quay_name', 'file':'quay_file', 'size':'quay_size'})
class quay_BackingFile(_ByteStore):
    def __init__(self, fp, use_mmaped_io=False):
        self.fp = fp
        self.name = quay_os.path.basename(getattr(fp, 'name', '')) if isinstance(getattr(fp, 'name', ''), (str, bytes)) else ''
        self.file = snapshot(fp)
        self.size = len(self.file)
        self._generation = 0

    def quay_close(self):
        self.fp.close()


@_name_boundary.class_contract('SlicedBackingFile', {'read_bytes':'quay_read_bytes', 'read_int':'quay_read_int', 'write':'quay_write', 'file':'quay_file', 'size':'quay_size', 'name':'quay_name'})
class quay_SlicedBackingFile(_ByteStore):
    def __init__(self, backing_file, offset, size):
        self.file = bytearray(backing_file.read_bytes(offset, size))
        self.size = size
        self.name = backing_file.name
        self._generation = 0


@_name_boundary.class_contract('MachOFile', {'_load_struct':'quay__load_struct', 'file_object':'quay_file_object', 'uses_mmaped_io':'quay_uses_mmaped_io', 'file':'quay_file', 'slices':'quay_slices', 'magic':'quay_magic', 'filename':'quay_filename', 'type':'quay_type', 'header':'quay_header'})
class quay_MachOFile:
    def __init__(self, file, use_mmaped_io=True):
        self.file_object = file
        self.uses_mmaped_io = False
        self.filename = quay_os.path.basename(getattr(file, 'name', '')) if isinstance(getattr(file, 'name', ''), (str, bytes)) else ''
        self.file = quay_BackingFile(file, use_mmaped_io)
        self.slices = []
        self.magic = self.file.read_int(0, 4)
        thin_magics = (quay_MH_MAGIC, quay_MH_CIGAM, quay_MH_MAGIC_64, quay_MH_CIGAM_64)
        if self.magic in thin_magics:
            self.type = quay_MachOFileType.THIN
            self.slices.append(quay_Slice(self, self.file))
        elif self.magic in (quay_FAT_MAGIC, quay_FAT_CIGAM):
            self.type = quay_MachOFileType.FAT
            order = 'big' if self.magic == quay_FAT_MAGIC else 'little'
            self.header = self.quay__load_struct(0, quay_fat_header, order)
            count = self.header.nfat_archs
            if count == 0 or count > MAX_ARCHITECTURES:
                raise quay_MalformedMachOException('fat architecture count must be between 1 and 4096')
            table_end = quay_fat_header.size() + count * quay_fat_arch.quay_size()
            checked_range(self.file.size, 0, table_end, 'fat architecture table')
            ranges = []
            records = []
            for index in range(count):
                arch = self.quay__load_struct(quay_fat_header.size() + index * quay_fat_arch.quay_size(), quay_fat_arch, order)
                checked_range(self.file.size, arch.offset, arch.quay_size, 'fat slice')
                if arch.offset < table_end or arch.quay_size < quay_mach_header.size() or arch.align > 30 or arch.offset % (1 << arch.align):
                    raise quay_MalformedMachOException('fat slice overlaps its table, has an invalid alignment or is too short')
                if self.file.read_int(arch.offset, 4) not in thin_magics:
                    raise quay_MalformedMachOException('fat slice has unsupported Mach-O magic')
                ranges.append((arch.offset, arch.offset + arch.quay_size))
                records.append(arch)
            ordered = sorted(ranges)
            if any(left[1] > right[0] for left, right in zip(ordered, ordered[1:])):
                raise quay_MalformedMachOException('fat architecture slices overlap')
            for arch in records:
                backing = quay_SlicedBackingFile(self.file, arch.offset, arch.quay_size)
                self.slices.append(quay_Slice(self, backing, arch))
        else:
            raise quay_UnsupportedFiletypeException(f'unsupported Mach-O magic {self.magic:#x}')

    def quay__load_struct(self, address, struct_type, endian='little'):
        record = quay_Struct.create_with_bytes(struct_type, self.file.read_bytes(address, struct_type.size()), endian)
        record.off = address
        return record

    def __del__(self):
        backing = getattr(self, 'file', None)
        if backing is not None and hasattr(backing, 'close'):
            backing.close()


@_name_boundary.class_contract('Section', {'SectionIterator':'quay_SectionIterator', 'serialize':'quay_serialize', 'cmd':'quay_cmd', 'segment':'quay_segment', 'name':'quay_name', 'vm_address':'quay_vm_address', 'file_address':'quay_file_address', 'size':'quay_size', 'ptr_size':'quay_ptr_size'})
class quay_Section:
    class quay_SectionIterator:
        def __init__(self, sect, vm=False, ptr_size=8):
            if ptr_size not in (4, 8) or sect.size % ptr_size:
                raise quay_MalformedMachOException('pointer section has a partial entry')
            self._iterator = iter(range(sect.vm_address if vm else sect.file_address,
                                        (sect.vm_address if vm else sect.file_address) + sect.size, ptr_size))
        def __iter__(self):
            return self
        def __next__(self):
            return next(self._iterator)

    def __init__(self, segment, cmd, ptr_size):
        self.cmd, self.segment, self.ptr_size = cmd, segment, ptr_size
        self.name, self.vm_address, self.file_address, self.size = cmd.sectname, cmd.addr, cmd.offset, cmd.quay_size

    def __iter__(self):
        return self.quay_SectionIterator(self, ptr_size=self.ptr_size)

    def quay_serialize(self):
        return {'command':self.cmd.serialize(), 'name':self.name, 'vm_address':self.vm_address,
                'file_address':self.file_address, 'size':self.size}


@_name_boundary.class_contract('Segment', {'serialize':'quay_serialize', '_process_sections':'quay__process_sections', 'image':'quay_image', 'is64':'quay_is64', 'cmd':'quay_cmd', 'vm_address':'quay_vm_address', 'file_address':'quay_file_address', 'size':'quay_size', 'file_size':'quay_file_size', 'name':'quay_name', 'sections':'quay_sections', 'type':'quay_type'})
class quay_Segment:
    def __init__(self, image, cmd):
        self.image, self.cmd = image, cmd
        self.is64 = isinstance(cmd, quay_segment_command_64)
        self.vm_address, self.file_address, self.size, self.file_size = cmd.vmaddr, cmd.fileoff, cmd.vmsize, cmd.filesize
        self.name = cmd.segname
        checked_range(image.slice.size, self.file_address, self.file_size, 'segment bytes')
        if self.vm_address + self.size > 1 << (64 if self.is64 else 32):
            raise quay_MalformedMachOException('segment virtual range overflows its address width')
        self.sections = self.quay__process_sections()
        self.type = quay_SectionType(quay_S_FLAGS_MASKS.SECTION_TYPE & cmd.flags)

    def quay__process_sections(self):
        section_type = quay_section_64 if self.is64 else quay_section
        base = self.cmd.off + self.cmd.size()
        if self.cmd.nsects > (self.cmd.cmdsize - self.cmd.size()) // section_type.size():
            raise quay_MalformedMachOException('section table exceeds its load command')
        result = {}
        for index in range(self.cmd.nsects):
            record = self.image.read_struct(base + index * section_type.size(), section_type, endian=self.image.slice.byte_order)
            value = quay_Section(self, record, 8 if self.is64 else 4)
            # Zero-fill declarations have no file bytes; every other section does.
            if record.flags & 0xff not in (1, 12, 18):
                checked_range(self.image.slice.size, record.offset, record.quay_size, 'section bytes')
            if record.addr + record.quay_size > 1 << (64 if self.is64 else 32):
                raise quay_MalformedMachOException('section virtual range overflows its address width')
            if value.name in result:
                raise quay_MalformedMachOException('duplicate section name in a segment')
            result[value.name] = value
        return result

    def __str__(self):
        return f'Segment {self.name} at {self.vm_address:#x}\n'

    def quay_serialize(self):
        return {'command':self.cmd.serialize(), 'name':self.name, 'vm_address':self.vm_address,
                'file_address':self.file_address, 'size':self.size, 'type':self.type.name,
                'sections':{name:section.serialize() for name,section in self.sections.items()}}


@_name_boundary.class_contract('Slice', {'patch':'quay_patch', 'full_bytes_for_slice':'quay_full_bytes_for_slice', 'find':'quay_find', 'read_struct':'quay_read_struct', 'read_uint':'quay_read_uint', 'read_bytearray':'quay_read_bytearray', 'read_fixed_len_str':'quay_read_fixed_len_str', 'read_cstr':'quay_read_cstr', 'read_uleb128':'quay_read_uleb128', '_load_type':'quay__load_type', '_load_subtype':'quay__load_subtype', 'file':'quay_file', 'macho_file':'quay_macho_file', 'arch_struct':'quay_arch_struct', 'offset':'quay_offset', 'type':'quay_type', 'subtype':'quay_subtype', 'ptr_size':'quay_ptr_size', 'size':'quay_size', 'byte_order':'quay_byte_order', '_cstring_cache':'quay__cstring_cache'})
class quay_Slice:
    def __init__(self, macho_file, sliced_backing_file, arch_struct=None, offset=0):
        self.file, self.macho_file = sliced_backing_file, macho_file
        self.size = sliced_backing_file.size
        self.offset = arch_struct.offset if arch_struct else offset
        little_magic = self.file.read_int(0, 4, 'little')
        self.byte_order = 'little' if little_magic in (quay_MH_MAGIC, quay_MH_MAGIC_64) else 'big'
        header = quay_Struct.create_with_bytes(quay_mach_header, self.file.read_bytes(0, 28), self.byte_order)
        self.arch_struct = arch_struct or quay_Struct.create_with_values(quay_fat_arch, [header.cpu_type, header.cpu_subtype, 0, 0, 0])
        if arch_struct and (header.cpu_type != arch_struct.cpu_type or header.cpu_subtype != arch_struct.cpu_subtype):
            raise quay_MalformedMachOException('fat architecture and slice CPU identities disagree')
        self.type = self.quay__load_type()
        self.subtype = self.quay__load_subtype(self.type)
        self.ptr_size = 4 if self.type in (quay_CPUType.ARM, quay_CPUType.X86, quay_CPUType.POWERPC, quay_CPUType.ARM6432) else 8
        self._cstring_cache = {}

    def quay_patch(self, address, raw):
        self.file.write(address, raw)
        self._cstring_cache.clear()

    def quay_full_bytes_for_slice(self):
        return self.file.read_bytes(0, self.size)

    def quay_find(self, pattern):
        return self.file.file.find(pattern.encode('utf-8') if isinstance(pattern, str) else pattern)

    def quay_read_struct(self, addr, struct_type, endian=None):
        record = quay_Struct.create_with_bytes(struct_type, self.file.read_bytes(addr, struct_type.size(self.ptr_size)),
                                              endian or self.byte_order, ptr_size=self.ptr_size)
        record.off = addr
        return record

    def quay_read_uint(self, addr, count, endian=None):
        return self.file.read_int(addr, count, endian or self.byte_order)

    def quay_read_bytearray(self, addr, count):
        return self.file.read_bytes(addr, count)

    def quay_read_fixed_len_str(self, addr, count, force=False):
        data = self.file.read_bytes(addr, count)
        return data.decode('utf-8', errors='replace' if force else 'strict').rstrip('\x00')

    def quay_read_cstr(self, addr, limit=0):
        checked_range(self.size, addr, 0, 'C string')
        if type(limit) is not int or limit < 0:
            raise quay_MalformedMachOException('C string limit must be a nonnegative integer')
        end = min(self.size, addr + limit) if limit else self.size
        key = (addr, end, self.file._generation)
        if key not in self._cstring_cache:
            terminal = self.file.file.find(b'\x00', addr, end)
            if terminal < 0:
                raise quay_MalformedMachOException('C string has no terminator inside its declared range')
            self._cstring_cache[key] = self.file.read_bytes(addr, terminal - addr).decode('utf-8')
        return self._cstring_cache[key]

    def quay_read_uleb128(self, read_head):
        value = 0
        for index in range(10):
            byte = self.quay_read_uint(read_head + index, 1)
            if index == 9 and byte & 0xfe:
                raise quay_MalformedMachOException('ULEB128 exceeds 64 bits')
            value |= (byte & 0x7f) << (index * 7)
            if not byte & 0x80:
                return value, read_head + index + 1
        raise quay_MalformedMachOException('unterminated ULEB128')

    def quay__load_type(self):
        return quay_CPUType(self.arch_struct.cpu_type)

    def quay__load_subtype(self, cputype):
        subtype = self.arch_struct.cpu_subtype & 0xffff
        if cputype not in quay_CPU_SUBTYPES:
            quay_log.error(f'Unknown CPU SubType ({subtype:#x})')
            return quay_CPUSubTypeARM64.ALL
        return quay_CPU_SUBTYPES[cputype](subtype)


@_name_boundary.class_contract('MachOImageHeader', {'MachOLoadCommandIterator':'quay_MachOLoadCommandIterator', 'from_image':'quay_from_image', 'from_values':'quay_from_values', 'serialize':'quay_serialize', 'raw_bytes':'quay_raw_bytes', 'insert_load_command':'quay_insert_load_command', 'remove_load_command':'quay_remove_load_command', 'replace_load_command':'quay_replace_load_command', 'is64':'quay_is64', 'dyld_header':'quay_dyld_header', 'filetype':'quay_filetype', 'flags':'quay_flags', 'load_commands':'quay_load_commands', 'raw':'quay_raw'})
class quay_MachOImageHeader(quay_Constructable):
    class quay_MachOLoadCommandIterator:
        def __init__(self, hdr):
            self._iterator = iter(hdr.load_commands)
        def __iter__(self):
            return self
        def __next__(self):
            return next(self._iterator)

    def __init__(self):
        self.is64, self.dyld_header, self.filetype = False, None, quay_MH_FILETYPE(0)
        self.flags, self.load_commands, self.raw = [], [], bytearray()
        self._file_offset = 0
        self._byte_order = 'little'

    @classmethod
    def quay_from_image(cls, macho_slice, offset=0):
        header = macho_slice.read_struct(offset, quay_mach_header)
        if header.magic not in (quay_MH_MAGIC, quay_MH_MAGIC_64):
            raise quay_MalformedMachOException('invalid Mach-O header magic')
        is64 = header.magic == quay_MH_MAGIC_64
        if is64:
            header = macho_slice.read_struct(offset, quay_mach_header_64)
        start = offset + header.size()
        _, end = checked_range(macho_slice.size, start, header.loadsize, 'load-command region')
        if header.loadcnt > header.loadsize // 8:
            raise quay_MalformedMachOException('load-command count exceeds its region')
        result = cls()
        result._file_offset, result._byte_order = offset, macho_slice.byte_order
        result.is64, result.dyld_header = is64, header
        result.filetype = quay_MH_FILETYPE(header.filetype)
        result.flags = [flag for flag in quay_MH_FLAGS if header.flags & flag.value]
        cursor = start
        for index in range(header.loadcnt):
            checked_range(end, cursor, 8, 'load-command prefix')
            code = macho_slice.read_uint(cursor, 4)
            size = macho_slice.read_uint(cursor + 4, 4)
            if size < 8 or size % (8 if is64 else 4):
                raise quay_MalformedMachOException('load command has an invalid size or alignment')
            checked_range(end, cursor, size, 'load-command body')
            try:
                command_type = quay_LOAD_COMMAND_MAP[quay_LOAD_COMMAND(code)]
            except (ValueError, KeyError):
                if not quay_ignore.MALFORMED:
                    quay_log.error(f'Bad Load Command at {cursor:#x} index {index}: {code:#x} - {size:#x}')
                command_type = quay_unk_command
            if size < command_type.size():
                raise quay_MalformedMachOException('load command is shorter than its required record')
            command = quay_Struct.create_with_bytes(command_type, macho_slice.read_bytearray(cursor, command_type.size()), result._byte_order)
            command.off = cursor
            result.load_commands.append(command)
            cursor += size
        if cursor != end:
            raise quay_MalformedMachOException('load-command count and declared length disagree')
        result.raw = bytearray(macho_slice.read_bytearray(offset, end - offset))
        return result

    @classmethod
    def quay_from_values(cls, is_64, cpu_type, cpu_subtype, filetype, flags, load_commands):
        def integer(value):
            return value.value if isinstance(value, quay_Enum) else int(value)
        payload, count = bytearray(), 0
        for command in load_commands:
            if isinstance(command, (bytes, bytearray)):
                payload.extend(command)
            elif isinstance(command, (quay_Segment, quay_SegmentLoadCommand)):
                payload.extend(command.cmd.raw)
                for section in command.sections.values():
                    payload.extend(section.cmd.raw)
                count += 1
            elif isinstance(command, quay_Struct) and hasattr(command, 'cmdsize'):
                payload.extend(command.raw)
                count += 1
            else:
                raise TypeError('unsupported load-command representation')
        if len(payload) > MAX_INPUT_BYTES:
            raise quay_MalformedMachOException('edited header exceeds the snapshot budget')
        flag_bits = 0
        for flag in flags:
            flag_bits |= integer(flag)
        values = [quay_MH_MAGIC_64 if is_64 else quay_MH_MAGIC, integer(cpu_type), integer(cpu_subtype), integer(filetype), count, len(payload), flag_bits]
        if is_64:
            values.append(0)
        record = quay_Struct.create_with_values(quay_mach_header_64 if is_64 else quay_mach_header, values)
        backing = quay_BackingFile(quay_BytesIO(bytes(record.raw) + payload))
        view = quay_Slice(None, backing)
        return cls.quay_from_image(view)

    def __iter__(self):
        return self.quay_MachOLoadCommandIterator(self)

    def __str__(self):
        return f'MachO Header - 64 bit VM: {self.is64} | File Type: {self.filetype} | Flags: {self.flags} | Load Cmd Count: {len(self.load_commands)}'

    def quay_serialize(self):
        return {'filetype':self.filetype.name, 'flags':[flag.name for flag in self.flags], 'is_64_bit':self.is64,
                'dyld_header':self.dyld_header.serialize(), 'load_commands':[cmd.serialize() for cmd in self.load_commands]}

    def quay_raw_bytes(self):
        return self.raw

    def _chunks(self):
        chunks = []
        for command in self.load_commands:
            relative = command.off - self._file_offset
            start, end = checked_range(len(self.raw), relative, command.cmdsize, 'stored command')
            chunks.append(bytes(self.raw[start:end]))
        return chunks

    def _encode_command(self, command, suffix):
        if isinstance(command, (quay_Segment, quay_SegmentLoadCommand)):
            data = bytes(command.cmd.raw) + b''.join(bytes(item.cmd.raw) for item in command.sections.values())
        elif isinstance(command, quay_Struct) and hasattr(command, 'cmdsize'):
            data = bytes(command.raw)
            if suffix is not None:
                if isinstance(suffix, str):
                    if '\x00' in suffix:
                        raise ValueError('command string contains a NUL')
                    tail = suffix.encode('utf-8') + b'\x00'
                    alignment = 8 if self.is64 else 4
                    tail += b'\x00' * (-(len(data) + len(tail)) % alignment)
                elif isinstance(suffix, (bytes, bytearray)):
                    tail = bytes(suffix)
                else:
                    raise TypeError('command suffix must be text or bytes')
                data += tail
                data = data[:4] + len(data).to_bytes(4, self._byte_order) + data[8:]
            if len(data) != int.from_bytes(data[4:8], self._byte_order):
                raise ValueError('load-command bytes do not match cmdsize; provide its complete suffix')
        else:
            raise TypeError('unsupported load command')
        return data

    def _rebuild(self, chunks):
        count = len(chunks)
        payload = b''.join(chunks)
        header = bytearray(self.dyld_header.raw)
        header[16:20] = count.to_bytes(4, self._byte_order)
        header[20:24] = len(payload).to_bytes(4, self._byte_order)
        view = quay_Slice(None, quay_BackingFile(quay_BytesIO(bytes(header) + payload)))
        return self.__class__.quay_from_image(view)

    def quay_insert_load_command(self, load_command, index=-1, suffix=None):
        chunks = self._chunks()
        index = len(chunks) if index == -1 else index
        if type(index) is not int or not 0 <= index <= len(chunks):
            raise IndexError('insert index is outside the command list')
        chunks.insert(index, self._encode_command(load_command, suffix))
        return self._rebuild(chunks)

    def quay_remove_load_command(self, index):
        chunks = self._chunks()
        if type(index) is not int or not 0 <= index < len(chunks):
            raise IndexError('remove index is outside the command list')
        del chunks[index]
        return self._rebuild(chunks)

    def quay_replace_load_command(self, load_command, index=-1, suffix=None):
        if index == -1:
            return self.quay_insert_load_command(load_command, suffix=suffix)
        chunks = self._chunks()
        if type(index) is not int or not 0 <= index < len(chunks):
            raise IndexError('replace index is outside the command list')
        chunks[index] = self._encode_command(load_command, suffix)
        return self._rebuild(chunks)


@_name_boundary.class_contract('PlatformType', {})
class quay_PlatformType(quay_Enum):
    MACOS=1
    IOS=2
    TVOS=3
    WATCHOS=4
    BRIDGE_OS=5
    MAC_CATALYST=6
    IOS_SIMULATOR=7
    TVOS_SIMULATOR=8
    WATCHOS_SIMULATOR=9
    DRIVER_KIT=10
    UNK=64


@_name_boundary.class_contract('ToolType', {})
class quay_ToolType(quay_Enum):
    CLANG=1
    SWIFT=2
    LD=3

_name_boundary.module_contract(globals(), {'os': 'quay_os', 'ToolType': 'quay_ToolType', 'Tuple': 'quay_Tuple', 'MachOFileType': 'quay_MachOFileType', 'mmap': 'quay_mmap', 'Union': 'quay_Union', 'ignore': 'quay_ignore', 'BackingFile': 'quay_BackingFile', 'MachOImageHeader': 'quay_MachOImageHeader', 'BytesIO': 'quay_BytesIO', 'PlatformType': 'quay_PlatformType', 'Section': 'quay_Section', 'Constructable': 'quay_Constructable', 'BinaryIO': 'quay_BinaryIO', 'Slice': 'quay_Slice', 'SlicedBackingFile': 'quay_SlicedBackingFile', 'Enum': 'quay_Enum', 'List': 'quay_List', 'SegmentLoadCommand': 'quay_SegmentLoadCommand', 'Dict': 'quay_Dict', 'Segment': 'quay_Segment', 'MachOFile': 'quay_MachOFile', 'log': 'quay_log'})
