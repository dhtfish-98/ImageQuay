# Derived binding API from ktool; Copyright (c) 0cyn 2021, MIT in LICENSE.
"""Confined dyld binding opcode interpreter with explicit pointer-chain state."""
import imagequay_boundary as _name_boundary
from imagequay.byte_region import ByteRegion
from imagequay.failure_types import quay_MalformedMachOException as Malformed

quay_action = _name_boundary.named_record('action', ['vmaddr', 'libname', 'item'])
quay_record = _name_boundary.named_record('record', ['off', 'seg_index', 'seg_offset', 'lib_ordinal', 'type', 'flags', 'name', 'addend', 'special_dylib'])


def _signed(value, bits):
    return value-(1 << bits) if value & (1 << (bits-1)) else value


@_name_boundary.class_contract('BindingTable', {name: 'quay_'+name for name in
    ('image', 'import_stack', 'actions', 'lookup_table', 'link_table', 'symbol_table',
     '_load_symbol_table', '_create_action_list', '_load_binding_info')})
class quay_BindingTable:
    def __init__(self, image, table_start, table_size, *, kind='bind'):
        if kind not in ('bind', 'weak', 'lazy'):
            raise ValueError('binding table kind must be bind, weak, or lazy')
        self.kind, self.strong_definitions = kind, []
        self.image = image
        self.import_stack = self._load_binding_info(table_start, table_size)
        self.actions = self._create_action_list()
        self.lookup_table, self.link_table = {}, {}
        self.symbol_table = self._load_symbol_table()

    def _segment(self, index, offset, width=0):
        segments = list(self.image.segments.values())
        if not 0 <= index < len(segments):
            raise Malformed('binding segment index is outside the image')
        segment = segments[index]
        if offset < 0 or offset > segment.file_size or width > segment.file_size-offset:
            raise Malformed('binding location is outside the file-backed segment')
        address = segment.vm_address+offset
        if address+width > 1 << (self.image.ptr_size*8):
            raise Malformed('binding address exceeds the image pointer width')
        return segment, address

    def _library(self, ordinal):
        if ordinal > 0:
            if ordinal > len(self.image.linked_images):
                raise Malformed('binding library ordinal is outside the linked images')
            return self.image.linked_images[ordinal-1].install_name
        if ordinal < -3:
            raise Malformed('binding special library ordinal is unsupported')
        return str(ordinal)

    def quay__create_action_list(self):
        actions = []
        for item in self.import_stack:
            width = self.image.ptr_size if item.type == 1 else 4
            _, address = self._segment(item.seg_index, item.seg_offset, width)
            actions.append(quay_action(address, self._library(item.lib_ordinal), item.name))
        return actions

    def quay__load_symbol_table(self):
        from imagequay.metadata_reader import quay_Symbol
        result = []
        for item, action in zip(self.import_stack, self.actions):
            symbol = quay_Symbol.from_values(item.name, action.vmaddr, external=True, ordinal=action.libname)
            symbol.binding_ordinal, symbol.binding_type = item.lib_ordinal, item.type
            symbol.addend, symbol.weak_import = item.addend, bool(item.flags & 1)
            result.append(symbol)
            self.lookup_table[action.vmaddr] = symbol
        return result

    def quay__load_binding_info(self, table_start, table_size):
        region = ByteRegion(self.image, table_start, table_size)
        if self.image.ptr_size not in (4, 8):
            raise Malformed('binding image pointer width must be 4 or 8 bytes')
        cursor, result = region.start, []
        state = {'segment': 0, 'offset': 0, 'ordinal': -3 if self.kind == 'weak' else 0, 'type': 1 if self.kind == 'lazy' else 0, 'flags': 0, 'name': '', 'addend': 0, 'special': 0}
        segment_set, ordinal_set = False, self.kind == 'weak'
        ordinal_table, ordinal_count = [], None
        def snapshot(op_start, offset=None, segment=None, addend=None):
            if not ordinal_set or not state['name'] or state['type'] not in (1, 2, 3):
                raise Malformed('binding action has no symbol or a valid binding type')
            self._library(state['ordinal'])
            return quay_record(op_start, state['segment'] if segment is None else segment,
                state['offset'] if offset is None else offset, state['ordinal'], state['type'],
                state['flags'], state['name'], state['addend'] if addend is None else addend, state['special'])
        def emit(item):
            region.use()
            if not segment_set:
                raise Malformed('binding action has no selected segment')
            self._segment(item.seg_index, item.seg_offset, self.image.ptr_size if item.type == 1 else 4)
            result.append(item)
        def advance(amount):
            # dyld stores this cursor in uint64_t; older ARM64_32 files
            # encode backward moves as a large ULEB. Reproduce that arithmetic
            # and still require the resulting cursor inside a declared segment.
            state['offset'] = (state['offset']+amount) & ((1 << 64)-1)
        while cursor < region.end:
            region.use()
            op_start = cursor
            byte = region.uint(cursor, 1)
            cursor += 1
            opcode, immediate = byte & 0xf0, byte & 15
            if opcode == 0:
                # DONE ends regular/weak input, and separates lazy sequences.
                # It never creates a binding or discards existing lazy state.
                if self.kind != 'lazy':
                    if any(region.bytes(cursor, region.end-cursor)):
                        raise Malformed('nonzero bytes follow the binding DONE terminator')
                    break
            elif opcode == 0x10:
                state['ordinal'], state['special'] = immediate, 0
                ordinal_set = True
            elif opcode == 0x20:
                state['ordinal'], cursor = region.leb(cursor)
                state['special'] = 0
                ordinal_set = True
            elif opcode == 0x30:
                state['ordinal'] = _signed(immediate | 0xf0, 8) if immediate else 0
                state['special'] = 1
                ordinal_set = True
            elif opcode == 0x40:
                state['flags'] = immediate
                try:
                    state['name'], cursor = region.cstring(cursor)
                except UnicodeError as error:
                    raise Malformed('binding symbol name is not UTF-8') from error
                if not state['name']:
                    raise Malformed('binding symbol name is empty')
                if immediate & 8:
                    self.strong_definitions.append(state['name'])
            elif opcode == 0x50:
                if immediate not in (1, 2, 3):
                    raise Malformed('unsupported binding type')
                state['type'] = immediate
            elif opcode == 0x60:
                state['addend'], cursor = region.leb(cursor, signed=True)
            elif opcode == 0x70:
                state['segment'] = immediate
                segment_set = True
                state['offset'], cursor = region.leb(cursor)
                self._segment(immediate, state['offset'])
            elif opcode == 0x80:
                amount, cursor = region.leb(cursor)
                advance(amount)
            elif opcode in (0x90, 0xa0, 0xb0):
                item = snapshot(op_start)
                if opcode == 0x90 and ordinal_count is not None:
                    if len(ordinal_table) >= ordinal_count:
                        raise Malformed('threaded binding ordinal table has too many entries')
                    region.use()
                    ordinal_table.append(item)
                    continue
                emit(item)
                if opcode == 0xa0:
                    amount, cursor = region.leb(cursor)
                else:
                    amount = immediate*self.image.ptr_size if opcode == 0xb0 else 0
                advance(self.image.ptr_size+amount)
            elif opcode == 0xc0:
                count, cursor = region.leb(cursor)
                skip, cursor = region.leb(cursor)
                region.use(count)
                for _ in range(count):
                    emit(snapshot(op_start))
                    advance(self.image.ptr_size+skip)
            elif opcode == 0xd0 and immediate == 0:
                if ordinal_count is not None:
                    raise Malformed('threaded binding ordinal table is declared twice')
                ordinal_count, cursor = region.leb(cursor)
                if ordinal_count > 65536:
                    raise Malformed('threaded binding ordinal table exceeds 65536 entries')
            elif opcode == 0xd0 and immediate == 1:
                if self.image.ptr_size != 8 or ordinal_count is None or len(ordinal_table) != ordinal_count:
                    raise Malformed('threaded binding apply needs a complete 64-bit ordinal table')
                segment_index, offset = state['segment'], state['offset']
                while True:
                    region.use()
                    segment, _ = self._segment(segment_index, offset, 8)
                    word = self.image.read_uint(segment.file_address+offset, 8)
                    delta = (word >> 51) & 0x7ff
                    if word & (1 << 62):
                        index = word & 0xffff
                        if index >= len(ordinal_table):
                            raise Malformed('threaded pointer ordinal leaves its binding table')
                        target = ordinal_table[index]
                        pointer_addend = 0 if word & (1 << 63) else _signed((word >> 32) & 0x7ffff, 19)
                        addend = target.addend+pointer_addend
                        if not -(1 << 63) <= addend < 1 << 63:
                            raise Malformed('threaded binding addend exceeds 64 bits')
                        emit(target._replace(off=op_start, seg_index=segment_index, seg_offset=offset, addend=addend))
                    if not delta:
                        break
                    offset += delta*8
                state['offset'] = offset
            else:
                raise Malformed(f'unsupported binding opcode 0x{byte:02x}')
        if ordinal_count is not None and len(ordinal_table) != ordinal_count:
            raise Malformed('threaded binding ordinal table is incomplete')
        return result


_name_boundary.module_contract(globals(), {'BindingTable': 'quay_BindingTable', 'action': 'quay_action', 'record': 'quay_record'})
