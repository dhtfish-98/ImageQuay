"""A byte cursor confined to a declared metadata region and finite work budget."""
from imagequay.container_io import checked_range
from imagequay.failure_types import quay_MalformedMachOException

MAX_METADATA_RECORDS = 1 << 20


class ByteRegion:
    def __init__(self, image, start, size):
        checked_range(image.slice.size, start, size, 'metadata region')
        self.image, self.start, self.end = image, start, start + size
        self.remaining = MAX_METADATA_RECORDS

    def use(self, count=1):
        if count < 0 or count > self.remaining:
            raise quay_MalformedMachOException('metadata exceeds the 1048576-record work budget')
        self.remaining -= count

    def bytes(self, address, count):
        if address < self.start:
            raise quay_MalformedMachOException('metadata cursor precedes its region')
        checked_range(self.end, address, count, 'metadata read')
        return self.image.read_bytearray(address, count)

    def uint(self, address, count, endian='little'):
        return int.from_bytes(self.bytes(address, count), endian)

    def leb(self, address, signed=False, endpoint=None):
        end = self.end if endpoint is None else min(endpoint, self.end)
        value = 0
        for index in range(10):
            if address + index >= end:
                raise quay_MalformedMachOException('LEB128 has no terminator inside its metadata region')
            byte = self.uint(address + index, 1)
            if index == 9 and (byte & 0x7f) not in ((0, 0x7f) if signed else (0, 1)):
                raise quay_MalformedMachOException('LEB128 exceeds its 64-bit width')
            value |= (byte & 0x7f) << (index * 7)
            if not byte & 0x80:
                width = (index + 1) * 7
                if signed and byte & 0x40:
                    value -= 1 << width
                if signed and not -(1 << 63) <= value < 1 << 63:
                    raise quay_MalformedMachOException('SLEB128 exceeds its 64-bit width')
                return value, address + index + 1
        raise quay_MalformedMachOException('LEB128 exceeds its 64-bit width')

    def cstring(self, address, endpoint=None):
        end = self.end if endpoint is None else min(endpoint, self.end)
        if not self.start <= address < end:
            raise quay_MalformedMachOException('string cursor is outside its metadata region')
        raw = self.image.slice.file.file
        terminal = raw.find(b'\x00', address, end)
        if terminal < 0:
            raise quay_MalformedMachOException('string is not terminated inside its metadata region')
        return self.bytes(address, terminal - address).decode('utf-8'), terminal + 1
