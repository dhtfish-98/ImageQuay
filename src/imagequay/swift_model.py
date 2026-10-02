# Derived public metadata API from ktool; Copyright (c) 0cyn 2022, MIT in LICENSE.
"""Finite static Swift descriptor inspection; no runtime metadata accessors run."""
from itertools import islice
import imagequay_boundary as _name_boundary
from imagequay_layout.record_contract import quay_Constructable
from imagequay_swift.metadata_records import (quay_FieldDescriptor, quay_FieldRecord,
    quay_ClassDescriptor, quay_StructDescriptor, quay_EnumDescriptor,
    quay_ContextDescriptorKind)
from imagequay_swift.name_decoder import quay_demangle
from imagequay.metadata_graph import MetadataGraph, MAX_GRAPH_RECORDS
from imagequay.failure_types import quay_MalformedMachOException as Malformed


def _contract(label, fields=()):
    return _name_boundary.class_contract(label, {name: 'quay_'+name for name in
        ('from_image', 'from_values', 'raw_bytes')+tuple(fields)})


def _finite(values):
    result = list(islice(iter(values), MAX_GRAPH_RECORDS+1))
    if len(result) > MAX_GRAPH_RECORDS:
        raise ValueError('Swift values exceed the 1048576-record budget')
    return result


def _raw_record(record):
    if record is None:
        raise ValueError('Swift metadata assembled from values has no encoded snapshot')
    return bytes(record.raw)


@_contract('Field', ('flags', 'type_name', 'name'))
class quay_Field:
    def __init__(self, flags, type_name, name):
        if type(flags) is not int or not 0 <= flags < 1 << 32:
            raise ValueError('Swift field flags exceed 32 bits')
        self.flags, self.type_name, self.name = flags, type_name, name
        self.type_name_bytes = type_name.encode('utf-8')
        self.symbolic_type = False

    def __str__(self):
        return f'{self.name} : {self.type_name} ({hex(self.flags)})'


@_contract('_FieldDescriptor', ('fields', 'desc'))
class quay__FieldDescriptor(quay_Constructable):
    @classmethod
    def quay_from_image(cls, objc_image, location, *, _reader=None):
        reader = _reader or MetadataGraph(objc_image.image)
        if location in reader.field_cache:
            return reader.field_cache[location]
        descriptor = reader.record(location, quay_FieldDescriptor)
        if descriptor.Kind not in range(9):
            raise Malformed('unsupported Swift field descriptor kind')
        if descriptor.FieldRecordSize != 12:
            raise Malformed('Swift field record size must be 12 bytes for this ABI')
        count = descriptor.NumFields
        reader.use(count)
        total = 16+count*12
        raw = reader.bytes(location, total)
        fields = []
        for index in range(count):
            address = location+16+index*12
            record = reader.record(address, quay_FieldRecord)
            name_location = reader.relative(address+8, record.FieldName, nullable=False)
            type_location = reader.relative(address+4, record.MangledTypeName)
            name = reader.string(name_location)
            type_raw, type_text = reader.symbolic_mangling(type_location) if type_location is not None else (b'', '')
            field = quay_Field(record.Flags, type_text, name)
            field.type_name_bytes, field.symbolic_type = type_raw, any(1 <= byte <= 31 for byte in type_raw)
            field.record, field.location = record, address
            fields.append(field)
        result = cls(fields, descriptor)
        result._snapshot, result.location = raw, location
        # Descriptor-level names are metadata as well, and may contain symbolic
        # references. Capture bytes without following or executing references.
        for attribute, delta, field in (('type_mangling', descriptor.MangledTypeName, location),
                                       ('superclass_mangling', descriptor.Superclass, location+4)):
            target = reader.relative(field, delta)
            setattr(result, attribute, reader.symbolic_mangling(target) if target is not None else (b'', ''))
        reader.field_cache[location] = result
        return result

    @classmethod
    def quay_from_values(cls, fields, desc=None):
        return cls(fields, desc)

    def quay_raw_bytes(self):
        return self._snapshot if self._snapshot is not None else _raw_record(self.desc)

    def __init__(self, fields, desc=None):
        self.fields, self.desc, self._snapshot = _finite(fields), desc, None


def _context(reader, location):
    """Walk file-backed parent descriptors with explicit cycle/depth limits."""
    visited, names, current = set(), [], location
    for _ in range(64):
        if current in visited:
            raise Malformed('Swift parent descriptors form a cycle')
        visited.add(current)
        flags = reader.uint(current, 4)
        kind = flags & 31
        version = (flags >> 8) & 255
        if version:
            raise Malformed('unsupported Swift context descriptor version')
        if kind in (0, 16, 17, 18):
            target = reader.relative(current+8, reader.uint(current+8, 4, signed=True), nullable=False)
            names.append(reader.string(target))
        elif kind == 1:
            target = reader.relative(current+8, reader.uint(current+8, 4, signed=True), nullable=False)
            names.append(reader.symbolic_mangling(target)[1])
        elif kind not in (2, 3, 4):
            raise Malformed('unsupported Swift context descriptor kind')
        parent = reader.relative(current+4, reader.uint(current+4, 4, signed=True), indirectable=True)
        if parent is None:
            return tuple(reversed(names))
        current = parent
    raise Malformed('Swift parent descriptors exceed 64 levels')


def _load_descriptor(objc_image, location, record_type, kind, reader):
    descriptor = reader.record(location, record_type)
    if descriptor.Flags & 31 != kind:
        raise Malformed('Swift nominal descriptor kind does not match its record')
    name = reader.string(reader.relative(location+8, descriptor.Name, nullable=False))
    target = reader.relative(location+16, descriptor.FieldDescriptor)
    fields = quay__FieldDescriptor.from_image(objc_image, target, _reader=reader) if target is not None else None
    path = _context(reader, location)
    return descriptor, name, fields, path


@_contract('SwiftStruct', ('name', 'field_desc', 'fields'))
class quay_SwiftStruct(quay_Constructable):
    @classmethod
    def quay_from_image(cls, objc_image, type_location, *, _reader=None):
        reader = _reader or MetadataGraph(objc_image.image)
        desc, name, fields, path = _load_descriptor(objc_image, type_location, quay_StructDescriptor, 17, reader)
        result = cls(name, fields)
        result.typedesc, result.context_path, result.location = desc, path, type_location
        return result

    @classmethod
    def quay_from_values(cls, name, field_desc=None):
        return cls(name, field_desc)

    def quay_raw_bytes(self):
        return _raw_record(self.typedesc)

    def __init__(self, name, field_desc=None):
        self.name, self.field_desc = name, field_desc
        self.fields = field_desc.fields if field_desc is not None else []
        self.typedesc, self.context_path = None, ()


@_contract('SwiftClass', ('name', 'fields', 'class_desc', 'field_desc', 'ivars'))
class quay_SwiftClass(quay_Constructable):
    @classmethod
    def quay_from_image(cls, image, objc_image, type_location, *, _reader=None):
        if image is not objc_image.image:
            raise ValueError('Swift and Objective-C views must refer to the same image')
        reader = _reader or MetadataGraph(image)
        desc, name, fields, path = _load_descriptor(objc_image, type_location, quay_ClassDescriptor, 16, reader)
        ivars, rendered_name = [], name
        for item in objc_image.classlist:
            reader.use()
            module, nominal = quay_demangle(item.name)
            if nominal == name and (not path or len(path) < 2 or module == path[0]):
                ivars, rendered_name = item.ivars, module+'.'+name
                break
        result = cls(rendered_name, fields.fields if fields is not None else [], desc, fields, ivars)
        result.context_path, result.location = path, type_location
        return result

    @classmethod
    def quay_from_values(cls, name, fields, class_descriptor=None, field_descriptor=None, ivars=None):
        return cls(name, fields, class_descriptor, field_descriptor, ivars)

    def quay_raw_bytes(self):
        return _raw_record(self.class_desc)

    def __init__(self, name, fields, class_descriptor=None, field_descriptor=None, ivars=None):
        self.name, self.fields = name, _finite(fields)
        self.class_desc, self.field_desc = class_descriptor, field_descriptor
        self.ivars, self.context_path = _finite(ivars or []), ()


@_contract('SwiftEnum', ('name', 'field_desc', 'fields'))
class quay_SwiftEnum(quay_SwiftStruct):
    @classmethod
    def quay_from_image(cls, objc_image, type_location, *, _reader=None):
        reader = _reader or MetadataGraph(objc_image.image)
        desc, name, fields, path = _load_descriptor(objc_image, type_location, quay_EnumDescriptor, 18, reader)
        result = cls(name, fields)
        result.typedesc, result.context_path, result.location = desc, path, type_location
        return result


@_contract('SwiftType', ('name', 'kind', 'typedesc', 'field_desc'))
class quay_SwiftType(quay_Constructable):
    @classmethod
    def quay_from_image(cls, image, objc_image, type_location, *, _reader=None):
        if image is not objc_image.image:
            raise ValueError('Swift and Objective-C views must refer to the same image')
        reader = _reader or MetadataGraph(image)
        if type_location in reader.type_cache:
            return reader.type_cache[type_location]
        kind = reader.uint(type_location, 4) & 31
        if kind == 16:
            result = quay_SwiftClass.from_image(image, objc_image, type_location, _reader=reader)
        elif kind == 17:
            result = quay_SwiftStruct.from_image(objc_image, type_location, _reader=reader)
        elif kind == 18:
            result = quay_SwiftEnum.from_image(objc_image, type_location, _reader=reader)
        else:
            # Preserve the inherited public dispatch result, with unsupported
            # section entries tracked explicitly by SwiftImage rather than lost.
            return None
        reader.type_cache[type_location] = result
        return result

    @classmethod
    def quay_from_values(cls, name, kind, typedesc=None, field_desc=None):
        return cls(name, kind, typedesc, field_desc)

    def quay_raw_bytes(self):
        return _raw_record(self.typedesc)

    def __init__(self, name, kind, typedesc=None, field_desc=None):
        self.name, self.kind, self.typedesc, self.field_desc = name, kind, typedesc, field_desc


@_contract('SwiftImage', ('types',))
class quay_SwiftImage(quay_Constructable):
    @classmethod
    def quay_from_image(cls, objc_image):
        image, reader = objc_image.image, MetadataGraph(objc_image.image)
        result = cls([])
        for segment in image.segments.values():
            for section in segment.sections.values():
                if section.name != '__swift5_types':
                    continue
                if section.size % 4:
                    raise Malformed('Swift type section has a partial relative pointer')
                reader.use(section.size//4)
                result._section_snapshots.append(reader.bytes(section.vm_address, section.size) if section.size else b'')
                for offset in range(0, section.size, 4):
                    field = section.vm_address+offset
                    relative = reader.uint(field, 4, signed=True)
                    reference_kind = relative & 3
                    if reference_kind not in (0, 1):
                        raise Malformed('Swift type section has an unsupported reference kind')
                    target = reader.relative(field, relative & ~3, nullable=False)
                    if reference_kind == 1:
                        target = reader.pointer(target)
                        reader.span(target, 1)
                    item = quay_SwiftType.from_image(image, objc_image, target, _reader=reader)
                    result.types.append(item)
                    if item is None:
                        result.unsupported_types.append({'entry': field, 'descriptor': target, 'kind': reader.uint(target, 4) & 31})
        result.complete = not result.unsupported_types
        return result

    @classmethod
    def quay_from_values(cls, types=()):
        return cls(types)

    def quay_raw_bytes(self):
        return b''.join(self._section_snapshots)

    def __init__(self, types):
        self.types, self.unsupported_types = _finite(types), []
        self.complete, self._section_snapshots = True, []
        self.scope = 'Static nominal header and field records; trailing generic/resilient/runtime metadata is not reconstructed'


_name_boundary.module_contract(globals(), {name: 'quay_'+name for name in
    ('SwiftImage', 'SwiftEnum', 'SwiftStruct', 'SwiftType', '_FieldDescriptor', 'Field', 'SwiftClass')})
