"""Snapshot-scoped file-backed VM reads for declarative language metadata."""
from imagequay.failure_types import quay_MalformedMachOException as Malformed
from imagequay_support.record_engine import quay_Struct, quay_uintptr_t

MAX_GRAPH_RECORDS = 1 << 20
MAX_GRAPH_STRING = 1 << 20
MAX_GRAPH_STRINGS = 16 << 20


class MetadataGraph:
    def __init__(self, image):
        if image.ptr_size not in (4, 8):
            raise Malformed('language metadata requires 4-byte or 8-byte pointers')
        self.image = image
        self.generation = image.slice.file._generation
        self.remaining, self.string_remaining = MAX_GRAPH_RECORDS, MAX_GRAPH_STRINGS
        self.ranges = sorted((segment.vm_address, segment.vm_address+segment.file_size,
                              segment.file_address) for segment in image.segments.values()
                             if segment.file_size)
        self.field_cache, self.type_cache = {}, {}

    def use(self, count=1):
        if type(count) is not int or count < 0 or count > self.remaining:
            raise Malformed('language metadata exceeds the 1048576-record work budget')
        self.remaining -= count
        if self.image.slice.file._generation != self.generation:
            raise Malformed('image changed during language metadata inspection')

    def span(self, address, count):
        self.use()
        if type(address) is not int or type(count) is not int or min(address, count) < 0:
            raise Malformed('language metadata coordinates must be nonnegative integers')
        if address+count > 1 << (8*self.image.ptr_size):
            raise Malformed('language metadata range exceeds pointer width')
        for start, end, physical in self.ranges:
            if start <= address < end and count <= end-address:
                return physical+address-start, end-address
        raise Malformed('language metadata range leaves its file-backed segment')

    def bytes(self, address, count):
        physical, _ = self.span(address, count)
        return bytes(self.image.slice.read_bytearray(physical, count))

    def uint(self, address, width, *, signed=False):
        return int.from_bytes(self.bytes(address, width), self.image.slice.byte_order, signed=signed)

    def pointer(self, address):
        self.span(address, self.image.ptr_size)
        fixups = getattr(self.image, 'chained_fixups', None)
        if fixups is not None:
            if address in getattr(self.image, 'import_table', {}):
                return 0  # unresolved external reference remains in import_table
            if address in fixups.unresolved_rebases:
                raise Malformed('language pointer needs an unavailable external cache base')
            if address in fixups.rebases:
                return fixups.rebases[address]
        return self.uint(address, self.image.ptr_size)

    def record(self, address, record_type, *, relocate_pointers=False):
        width = record_type.size(ptr_size=self.image.ptr_size)
        raw = self.bytes(address, width)
        result = quay_Struct.create_with_bytes(record_type, raw,
            self.image.slice.byte_order, ptr_size=self.image.ptr_size)
        result.off = self.span(address, width)[0]
        result.disk_raw = raw
        if relocate_pointers:
            for name, specification in result._field_sizes.items():
                if isinstance(specification, type) and issubclass(specification, quay_uintptr_t):
                    setattr(result, name, self.pointer(address+result._field_offsets[name]))
        return result

    def relative(self, field, displacement, *, nullable=True, indirectable=False):
        if type(displacement) is not int or not -(1 << 31) <= displacement < (1 << 31):
            raise Malformed('language relative displacement exceeds signed 32 bits')
        if displacement == 0:
            if nullable:
                return None
            raise Malformed('required language relative pointer is null')
        indirect = indirectable and bool(displacement & 1)
        target = field+(displacement & ~1 if indirectable else displacement)
        self.span(target, self.image.ptr_size if indirect else 1)
        if indirect:
            target = self.pointer(target)
            if not target and nullable:
                return None
            self.span(target, 1)
        return target

    def string(self, address):
        physical, available = self.span(address, 1)
        bound = min(available, MAX_GRAPH_STRING+1, self.string_remaining+1)
        raw = self.image.slice.file.file
        terminal = raw.find(b'\0', physical, physical+bound)
        if terminal < 0:
            raise Malformed('language string has no terminator within its region or budget')
        size = terminal-physical
        if size > self.string_remaining:
            raise Malformed('language strings exceed the 16 MiB budget')
        self.string_remaining -= size
        try:
            return self.bytes(address, size).decode('utf-8')
        except UnicodeError as error:
            raise Malformed('language metadata name is not UTF-8') from error

    def symbolic_mangling(self, address):
        """Capture symbolic bytes; never follow them or invoke a Swift accessor."""
        physical, available = self.span(address, 1)
        raw = self.image.slice.file.file
        cursor, end = physical, physical+min(available, MAX_GRAPH_STRING+1, self.string_remaining+1)
        pieces, literal = [], bytearray()
        while cursor < end:
            self.use()
            value = raw[cursor]
            if value == 0:
                size = cursor-physical
                if size > self.string_remaining:
                    raise Malformed('language strings exceed the 16 MiB budget')
                self.string_remaining -= size
                if literal:
                    pieces.append(literal.decode('utf-8', errors='backslashreplace'))
                return bytes(raw[physical:cursor]), ''.join(pieces)
            if 1 <= value <= 31:
                if literal:
                    pieces.append(literal.decode('utf-8', errors='backslashreplace'))
                    literal.clear()
                width = 4 if value < 24 else self.image.ptr_size
                if cursor+1+width > end:
                    raise Malformed('Swift symbolic reference leaves its string region')
                payload = raw[cursor+1:cursor+1+width]
                pieces.append(f'<symbolic:0x{value:02x}:{bytes(payload).hex()}>')
                cursor += 1+width
            elif value == 255:
                pieces.append('<padding:ff>')
                cursor += 1
            else:
                literal.append(value)
                cursor += 1
        raise Malformed('Swift mangling has no terminator within its region or budget')
