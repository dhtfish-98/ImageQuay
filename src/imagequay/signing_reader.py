# Derived from ktool; Copyright (c) 0cyn 2022. MIT license in LICENSE.
"""Read signature metadata with every slot confined to its declared SuperBlob.

This is structural metadata analysis. It does not validate signing trust,
revocation, executable integrity, identity, or platform acceptance.
"""
import struct
from typing import List as quay_List
import imagequay_boundary as _name_boundary
from imagequay_layout.record_contract import quay_Constructable
from imagequay_layout.binary_records import quay_linkedit_data_command
from imagequay_layout.signing_records import *
from imagequay_support.diagnostics import quay_log
from imagequay.failure_types import quay_MalformedMachOException
from imagequay.container_io import checked_range


def quay_swap_32(value):
    if type(value) is not int or not 0 <= value <= 0xffffffff:
        raise ValueError('swap_32 requires an unsigned 32-bit integer')
    return int.from_bytes(value.to_bytes(4, 'little'), 'big')


@_name_boundary.class_contract('CodesignInfo', {'from_image':'quay_from_image', 'from_values':'quay_from_values', 'raw_bytes':'quay_raw_bytes', 'superblob':'quay_superblob', 'slots':'quay_slots', 'entitlements':'quay_entitlements', 'req_dat':'quay_req_dat'})
class quay_CodesignInfo(quay_Constructable):
    @classmethod
    def quay_from_image(cls, image, codesign_cmd):
        start, size = codesign_cmd.dataoff, codesign_cmd.datasize
        checked_range(image.slice.size, start, size, 'code signature region')
        if size < 12:
            raise quay_MalformedMachOException('code signature is shorter than a SuperBlob header')
        prefix = image.read_bytearray(start, 12)
        magic, length, count = struct.unpack('>III', prefix)
        if magic not in (quay_CSMAGIC_EMBEDDED_SIGNATURE, quay_CSMAGIC_DETACHED_SIGNATURE):
            raise quay_MalformedMachOException('signature is not a supported SuperBlob')
        if length < 12 or length > size or count > (length - 12) // 8:
            raise quay_MalformedMachOException('signature length or index count exceeds its region')
        table_end = 12 + count * 8
        # Keep the inherited raw SuperBlob public record representation.
        superblob = image.read_struct(start, quay_SuperBlob, endian='little')
        slots, intervals, types = [], [], set()
        entitlements, requirements = '', None
        for index in range(count):
            index_start = start + 12 + index * 8
            kind, relative = struct.unpack('>II', image.read_bytearray(index_start, 8))
            if kind in types:
                raise quay_MalformedMachOException('signature contains a duplicate slot type')
            types.add(kind)
            if relative < table_end:
                raise quay_MalformedMachOException('signature slot overlaps the index table')
            checked_range(length, relative, 8, 'signature slot header')
            blob_magic, blob_length = struct.unpack('>II', image.read_bytearray(start + relative, 8))
            if blob_length < 8:
                raise quay_MalformedMachOException('signature slot is shorter than its blob header')
            checked_range(length, relative, blob_length, 'signature slot body')
            intervals.append((relative, relative + blob_length))
            slot = image.read_struct(index_start, quay_BlobIndex, endian='little')
            slot.type, slot.offset = kind, relative
            slots.append(slot)
            payload_start, payload_length = start + relative + 8, blob_length - 8
            if kind == quay_CSSLOT_ENTITLEMENTS:
                if blob_magic != quay_CSMAGIC_EMBEDDED_ENTITLEMENTS:
                    raise quay_MalformedMachOException('entitlement slot has the wrong blob magic')
                entitlements = image.read_fixed_len_str(payload_start, payload_length)
            elif kind == quay_CSSLOT_REQUIREMENTS:
                if blob_magic != quay_CSMAGIC_REQUIREMENTS:
                    raise quay_MalformedMachOException('requirement slot has the wrong blob magic')
                requirements = image.read_bytearray(payload_start, payload_length)
        ordered = sorted(intervals)
        if any(left[1] > right[0] for left, right in zip(ordered, ordered[1:])):
            raise quay_MalformedMachOException('signature slot bodies overlap')
        result = cls(superblob, slots, entitlements=entitlements, req_dat=requirements)
        result._raw = image.read_bytearray(start, length)
        return result

    @classmethod
    def quay_from_values(cls, *args, **kwargs):
        raise NotImplementedError('signature construction and signing are not implemented')

    def quay_raw_bytes(self):
        if self._raw is None:
            raise ValueError('no stored signature bytes are available')
        return self._raw

    def __init__(self, superblob, slots, entitlements=None, req_dat=None):
        self.superblob, self.slots = superblob, slots
        self.entitlements, self.req_dat = entitlements, req_dat
        self._raw = None

_name_boundary.module_contract(globals(), {'swap_32': 'quay_swap_32', 'Constructable': 'quay_Constructable', 'linkedit_data_command': 'quay_linkedit_data_command', 'CodesignInfo': 'quay_CodesignInfo', 'log': 'quay_log', 'List': 'quay_List'})
