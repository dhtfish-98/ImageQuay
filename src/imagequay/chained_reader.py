# Derived API from ktool; Copyright (c) 0cyn 2021, MIT in LICENSE.
# Layout evidence: Apple's include/mach-o/fixup-chains.h (linked in VALIDATION.md).
"""Local, finite chained-fixup metadata and pointer interpretation.

Every header/table is confined to its declared linkedit region. Chain locations
must stay inside one page and its file-backed segment. Targets requiring another
cache's base remain explicit unresolved metadata until the caller supplies that
base; the reader does not guess an address, change a file, or perform a fixup.
"""
from dataclasses import dataclass
import imagequay_boundary as _name_boundary
from imagequay.byte_region import ByteRegion
from imagequay.failure_types import quay_MalformedMachOException as Malformed
from imagequay_layout.record_contract import quay_Constructable

MAX_SYMBOL_BYTES = 64 << 20
MAX_CHAINED_METADATA_BYTES = 128 << 20


@dataclass(frozen=True)
class _Import:
    ordinal: int
    weak: bool
    name: str
    addend: int


def _signed(value, bits):
    return value-(1 << bits) if value & (1 << (bits-1)) else value


def _word(value, pointer_format, base, segments, max_pointer, cache_bases):
    """Return stride, next count, import index, addend, target, details."""
    details = {'format': pointer_format}
    index, addend, target = None, 0, None
    if pointer_format in (1, 7, 9, 10, 12):
        stride = 4 if pointer_format in (7, 10) else 8
        delta = (value >> 51) & 0x7ff
        authenticated, bind = bool(value >> 63), bool((value >> 62) & 1)
        details['authenticated'] = authenticated
        if bind:
            index = value & ((1 << (24 if pointer_format == 12 else 16))-1)
            addend = 0 if authenticated else _signed((value >> 32) & 0x7ffff, 19)
        elif authenticated:
            target = base+(value & 0xffffffff)
        else:
            low, high = value & ((1 << 43)-1), ((value >> 43) & 255) << 56
            target = ((base+low) if pointer_format in (7, 9, 12) else low) | high
    elif pointer_format in (2, 6):
        stride, delta = 4, (value >> 51) & 0xfff
        if value >> 63:
            index, addend = value & 0xffffff, (value >> 24) & 255
        else:
            low, high = value & ((1 << 36)-1), ((value >> 36) & 255) << 56
            target = ((base+low) if pointer_format == 6 else low) | high
    elif pointer_format == 3:
        stride, delta = 4, (value >> 26) & 31
        if value >> 31:
            index, addend = value & 0xfffff, (value >> 20) & 63
        else:
            low = value & 0x3ffffff
            if max_pointer and low > max_pointer:
                details['non_pointer_value'] = low-((0x4000000+max_pointer)//2)
            else:
                target = low
    elif pointer_format in (4, 8, 11, 13):
        stride = 1 if pointer_format == 11 else (8 if pointer_format == 13 else 4)
        if pointer_format == 4:
            low, level, delta = value & 0x3fffffff, 0, value >> 30
        elif pointer_format == 13:
            low, level, delta = value & ((1 << 34)-1), 0, (value >> 52) & 0x7ff
            details['authenticated'] = bool(value >> 63)
            details['high8'] = 0 if value >> 63 else (value >> 34) & 255
        else:
            low, level, delta = value & 0x3fffffff, (value >> 30) & 3, (value >> 51) & 0xfff
            details['authenticated'] = bool(value >> 63)
        details['cache_level'], details['target_offset'] = level, low
        if level in cache_bases:
            target = cache_bases[level]+low
            if pointer_format == 13:
                target |= details['high8'] << 56
        else:
            details['unresolved_cache_base'] = True
    elif pointer_format == 5:
        stride, delta, target = 4, value >> 26, value & 0x3ffffff
    elif pointer_format == 14:
        stride, delta = 4, (value >> 51) & 0xfff
        segment_index, offset = (value >> 28) & 15, value & 0xfffffff
        if segment_index >= len(segments) or offset >= segments[segment_index].size:
            raise Malformed('segmented rebase target leaves its selected segment')
        target = segments[segment_index].vm_address+offset
        details['authenticated'] = bool(value >> 63)
    else:
        raise Malformed(f'unsupported chained pointer format {pointer_format}')
    if target is not None and not 0 <= target < 1 << 64:
        raise Malformed('chained rebase target exceeds 64 bits')
    return stride, delta, index, addend, target, details


@_name_boundary.class_contract('ChainedFixups', {name: 'quay_'+name for name in
    ('from_image', 'from_values', 'raw_bytes', 'symbols', 'rebases')})
class quay_ChainedFixups(quay_Constructable):
    def __init__(self, symbols, rebases=None):
        self.symbols, self.rebases = symbols, {} if rebases is None else rebases
        self.rebase_details, self.unresolved_rebases, self.non_pointer_values = {}, {}, {}
        self._raw = None

    @classmethod
    def quay_from_image(cls, image, chained_fixup_cmd, *, cache_bases=None):
        from imagequay.metadata_reader import quay_Symbol
        if chained_fixup_cmd.datasize > MAX_CHAINED_METADATA_BYTES:
            raise Malformed('chained metadata exceeds the 128 MiB input budget')
        region = ByteRegion(image, chained_fixup_cmd.dataoff, chained_fixup_cmd.datasize)
        base = image.vm.vm_base_addr
        if type(base) is not int or not 0 <= base < 1 << 64:
            raise Malformed('chained fixups need a known local image VM base')
        cache_bases = {} if cache_bases is None else dict(cache_bases)
        if any(type(level) is not int or not 0 <= level < 4 or type(address) is not int or not 0 <= address < 1 << 64
               for level, address in cache_bases.items()):
            raise ValueError('cache_bases must contain levels 0..3 and unsigned 64-bit addresses')
        version, starts_offset, imports_offset, symbols_offset, count, import_format, symbol_format = [
            region.uint(region.start+offset, 4) for offset in range(0, 28, 4)]
        if version != 0:
            raise Malformed(f'unsupported chained fixup version {version}')
        if symbol_format != 0:
            raise Malformed(f'unsupported chained symbol format {symbol_format}; compressed symbol tables are not implemented')
        widths = {1: 4, 2: 8, 3: 16}
        if count and import_format not in widths:
            raise Malformed(f'unsupported chained import format {import_format}')
        region.use(count)
        imports_start = region.start+imports_offset
        import_width = widths.get(import_format, 4)
        imports_end = imports_start+count*import_width
        if count and (imports_offset < 28 or imports_end > region.end):
            raise Malformed('chained import table leaves its metadata region')
        if starts_offset < 28 or starts_offset > chained_fixup_cmd.datasize-4:
            raise Malformed('chained starts table leaves its metadata region')
        starts_start = region.start+starts_offset
        segment_count = region.uint(starts_start, 4)
        segments = list(image.segments.values())
        if segment_count > len(segments):
            raise Malformed('chained starts segment count exceeds the image segments')
        region.use(segment_count)
        table_end = starts_start+4+4*segment_count
        region.bytes(starts_start, table_end-starts_start)
        if count:
            if symbols_offset < 28 or symbols_offset >= chained_fixup_cmd.datasize:
                raise Malformed('chained symbol table leaves its metadata region')
            symbols_start = region.start+symbols_offset
            symbols_end = min([region.end]+[address for address in (starts_start, imports_start) if address > symbols_start])
        else:
            symbols_start, symbols_end = region.end, region.end
        intervals = [(region.start, region.start+28), (starts_start, table_end)]
        if count:
            intervals += [(imports_start, imports_end), (symbols_start, symbols_end)]
        def add_interval(start, end):
            if start < region.start+28 or end > region.end or end <= start:
                raise Malformed('chained starts record leaves its metadata region')
            if any(max(start, old_start) < min(end, old_end) for old_start, old_end in intervals):
                raise Malformed('chained metadata tables overlap')
            intervals.append((start, end))
        # Check base tables for overlap before following any strings/pointers.
        for index, (start, end) in enumerate(intervals):
            if any(max(start, other_start) < min(end, other_end) for other_start, other_end in intervals[:index]):
                raise Malformed('chained metadata tables overlap')
        imports = []
        name_bytes = 0
        for index in range(count):
            address = imports_start+index*import_width
            first = region.uint(address, 8 if import_format == 3 else 4)
            if import_format == 3:
                ordinal, weak, name_offset = first & 0xffff, bool((first >> 16) & 1), first >> 32
                if first & (0x7fff << 17):
                    raise Malformed('chained import has nonzero reserved bits')
                ordinal = ordinal-0x10000 if ordinal >= 0xfff1 else ordinal
                addend = region.uint(address+8, 8)
            else:
                ordinal, weak, name_offset = first & 255, bool((first >> 8) & 1), first >> 9
                ordinal = ordinal-256 if ordinal >= 0xf1 else ordinal
                addend = _signed(region.uint(address+4, 4), 32) if import_format == 2 else 0
            if ordinal < -3 or ordinal > len(image.linked_images):
                raise Malformed('chained import library ordinal leaves its linked images')
            try:
                name, _ = region.cstring(symbols_start+name_offset, endpoint=symbols_end)
            except UnicodeError as error:
                raise Malformed('chained symbol name is not UTF-8') from error
            if not name:
                raise Malformed('chained import symbol name is empty')
            name_bytes += len(name.encode('utf-8'))
            if name_bytes > MAX_SYMBOL_BYTES:
                raise Malformed('chained symbol names exceed the 64 MiB aggregate budget')
            imports.append(_Import(ordinal, weak, name, addend))
        result, visited = cls([]), set()
        for segment_index in range(segment_count):
            relative = region.uint(starts_start+4+4*segment_index, 4)
            if not relative:
                continue
            record_start = starts_start+relative
            size = region.uint(record_start, 4)
            if size < 22:
                raise Malformed('chained segment record is shorter than its header')
            record_end = record_start+size
            add_interval(record_start, record_end)
            page_size, pointer_format = region.uint(record_start+4, 2), region.uint(record_start+6, 2)
            segment_offset = region.uint(record_start+8, 8)
            max_pointer, page_count = region.uint(record_start+16, 4), region.uint(record_start+20, 2)
            if page_size not in (0x1000, 0x4000) or pointer_format not in range(1, 15):
                raise Malformed('chained segment has an unsupported page or pointer format')
            segment = segments[segment_index]
            if segment.vm_address != base+segment_offset:
                raise Malformed('chained segment offset does not match its load command')
            if page_count > (segment.size+page_size-1)//page_size or 22+2*page_count > size or (size-22) % 2:
                raise Malformed('chained page count or starts table exceeds its segment record')
            region.use(page_count)
            width = 4 if pointer_format in (3, 4, 5) else 8
            starts_count = (size-22)//2
            def page_start(index):
                if not 0 <= index < starts_count:
                    raise Malformed('chained multi-start index leaves its segment record')
                return region.uint(record_start+22+2*index, 2)
            for page in range(page_count):
                start = page_start(page)
                if start == 0xffff:
                    continue
                start_list = []
                if start & 0x8000:
                    overflow = start & 0x7fff
                    if overflow < page_count:
                        raise Malformed('chained multi-start index overlaps the primary page table')
                    while True:
                        region.use()
                        extra = page_start(overflow)
                        start_list.append(extra & 0x7fff)
                        overflow += 1
                        if extra & 0x8000:
                            break
                else:
                    start_list.append(start)
                for start in start_list:
                    position = page*page_size+start
                    page_end = (page+1)*page_size
                    while True:
                        region.use()
                        if start >= page_size or position+width > page_end or position+width > segment.file_size:
                            raise Malformed('chained pointer leaves its page or file-backed segment')
                        address = segment.vm_address+position
                        if address in visited:
                            raise Malformed('chained pointer is referenced by more than one chain')
                        visited.add(address)
                        word = image.read_uint(segment.file_address+position, width)
                        stride, delta, import_index, pointer_addend, target, details = _word(word, pointer_format, base, segments, max_pointer, cache_bases)
                        if position % stride:
                            raise Malformed('chained pointer is not aligned to its format stride')
                        result.rebase_details[address] = details
                        if import_index is not None:
                            if import_index >= len(imports):
                                raise Malformed('chained pointer ordinal leaves its import table')
                            imported = imports[import_index]
                            symbol = quay_Symbol.from_values(imported.name, address, external=True, ordinal=imported.ordinal)
                            addend = imported.addend+pointer_addend
                            if not -(1 << 63) <= addend < 1 << 64:
                                raise Malformed('chained binding addend exceeds 64-bit storage')
                            symbol.addend, symbol.weak_import = addend, imported.weak
                            symbol.pointer_format = pointer_format
                            result.symbols.append(symbol)
                            result.rebases[address] = 0
                        elif target is not None:
                            result.rebases[address] = target
                        elif 'non_pointer_value' in details:
                            result.non_pointer_values[address] = details['non_pointer_value']
                        else:
                            result.unresolved_rebases[address] = details
                        if not delta:
                            break
                        position += delta*stride
        result._raw = bytes(image.read_bytearray(region.start, region.end-region.start))
        return result

    @classmethod
    def quay_from_values(cls, symbols, rebases=None):
        return cls(list(symbols), {} if rebases is None else dict(rebases))

    def quay_raw_bytes(self):
        if self._raw is None:
            raise NotImplementedError('chained fixup encoding is not implemented')
        return bytearray(self._raw)


_name_boundary.module_contract(globals(), {'ChainedFixups': 'quay_ChainedFixups'})
