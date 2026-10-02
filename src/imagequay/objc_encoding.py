# Derived public type API from ktool; Copyright (c) 0cyn 2021, MIT in LICENSE.
"""Finite Objective-C encoding grammar with independent, mutable public views.

No type string is evaluated. Layout offsets are retained as metadata; aggregate
fields, pointer depth, arrays, unions, qualifiers and object names are parsed as
syntax rather than filtered out of the input.
"""
from collections import OrderedDict
from copy import deepcopy
from enum import Enum
import imagequay_boundary as _name_boundary

MAX_ENCODING_CHARS = 16384
MAX_ENCODING_NODES = 4096
MAX_ENCODING_DEPTH = 64
MAX_CACHE_ENTRIES = 1024
MAX_CACHE_CHARS = 1 << 20
MAX_CACHE_NODES = 65536

quay_type_encodings = {'c': 'char', 'i': 'int', 's': 'short', 'l': 'long',
    'q': 'NSInteger', 'C': 'unsigned char', 'I': 'unsigned int',
    'S': 'unsigned short', 'L': 'unsigned long',
    'Q': 'NSUInteger', 'f': 'float', 'd': 'CGFloat', 'D': 'long double',
    'b': 'BOOL', '@': 'id', 'B': 'BOOL', 'v': 'void', '*': 'char *',
    '#': 'Class', ':': 'SEL', '?': 'unk', 'T': 'unk'}
QUALIFIERS = {'r': 'const', 'n': 'in', 'N': 'inout', 'o': 'out',
              'O': 'bycopy', 'R': 'byref', 'V': 'oneway'}


@_name_boundary.class_contract('EncodedType', {})
class quay_EncodedType(Enum):
    STRUCT = 0
    NAMED = 1
    ID = 2
    NORMAL = 3


@_name_boundary.class_contract('Type', {name: 'quay_'+name for name in
    ('child', 'pointer_count', 'type', 'value')})
class quay_Type:
    def __init__(self, processor, type_string, pc=0):
        if not isinstance(pc, int) or isinstance(pc, bool) or not 0 <= pc <= MAX_ENCODING_DEPTH:
            raise ValueError('encoding pointer count exceeds 64')
        parser = _Parser(processor, type_string)
        node = parser.type(0)
        if parser.position != len(type_string):
            raise ValueError('Type requires exactly one complete encoding')
        self.__dict__.update(node.__dict__)
        if node.pointer_count+pc > MAX_ENCODING_DEPTH:
            raise ValueError('encoding pointer count exceeds 64')
        self.pointer_count += pc

    def __str__(self):
        # Preserve the historical public display convention. C declarations use
        # declaration() so pointer/array placement is syntactically accurate.
        return '*'*self.pointer_count + str(self.value)

    def declaration(self, name):
        if self.array_count is not None:
            decorated = '('+'*'*self.pointer_count+name+')' if self.pointer_count else name
            return self.child.declaration(decorated+f'[{self.array_count}]')
        if self.bit_width is not None:
            return f'unsigned int {name} : {self.bit_width}'
        if self.type == quay_EncodedType.NAMED:
            # @"<P>" is id<P>; a named class already implies one object pointer.
            base = 'id'+str(self.value) if str(self.value).startswith('<') else str(self.value)
            stars = self.pointer_count+(not str(self.value).startswith('<'))
        else:
            base = (self.value.kind+' '+self.value.name) if self.type == quay_EncodedType.STRUCT else str(self.value)
            stars = self.pointer_count
        qualifier = 'const ' if 'r' in self.qualifiers else ''
        return qualifier+base+' '+'*'*stars+name


def _node(value, encoded_type=quay_EncodedType.NORMAL, **metadata):
    node = object.__new__(quay_Type)
    node.child, node.pointer_count, node.type, node.value = None, 0, encoded_type, value
    node.qualifiers, node.encoding, node.offset = (), '', None
    node.array_count, node.bit_width, node.object_type, node.block = None, None, False, False
    for name, item in metadata.items():
        setattr(node, name, item)
    return node


@_name_boundary.class_contract('Struct_Representation', {name: 'quay_'+name for name in
    ('name', 'fields', 'field_names')})
class quay_Struct_Representation:
    def __init__(self, processor, type_str):
        parser = _Parser(processor, type_str)
        node = parser.type(0)
        if parser.position != len(type_str) or node.type != quay_EncodedType.STRUCT:
            raise ValueError('aggregate requires a complete struct or union encoding')
        self.__dict__.update(node.value.__dict__)

    def __str__(self):
        lines = [f'typedef {self.kind} {self.name} {{']
        if not self.fields:
            return lines[0]+'\n} // Error Processing Struct Fields'
        for index, item in enumerate(self.fields):
            name = self.field_names[index] if index < len(self.field_names) and self.field_names[index] else f'field{index}'
            lines.append('    '+item.declaration(name)+';')
        lines.append('} '+self.name+';')
        return '\n'.join(lines)


class _Parser:
    def __init__(self, processor, text):
        if not isinstance(text, str):
            raise TypeError('Objective-C type encoding must be text')
        if not text or len(text) > MAX_ENCODING_CHARS:
            raise ValueError('Objective-C type encoding is empty or exceeds 16384 characters')
        self.processor, self.text, self.position, self.nodes = processor, text, 0, 0
        self.aggregates = []

    def peek(self):
        return self.text[self.position:self.position+1]

    def take(self):
        if self.position == len(self.text):
            raise ValueError('Objective-C type encoding ends inside a type')
        result = self.text[self.position]
        self.position += 1
        return result

    def number(self, required=True):
        start = self.position
        while self.peek() and self.peek() in '0123456789':
            self.position += 1
        if self.position == start:
            if required:
                raise ValueError('encoding numeric field is missing')
            return None
        if self.position-start > 10:
            raise ValueError('encoding numeric field exceeds 32 bits')
        value = int(self.text[start:self.position])
        if value >= 1 << 32:
            raise ValueError('encoding numeric field exceeds 32 bits')
        return value

    def quoted(self):
        assert self.take() == '"'
        start = self.position
        while self.peek() and self.peek() != '"':
            if ord(self.peek()) < 32 or self.peek() == '\\':
                raise ValueError('encoding quoted name contains a control or escape')
            self.position += 1
        if not self.peek():
            raise ValueError('encoding quoted name is not terminated')
        result = self.text[start:self.position]
        self.position += 1
        return result

    def type(self, depth):
        self.nodes += 1
        if depth > MAX_ENCODING_DEPTH or self.nodes > MAX_ENCODING_NODES:
            raise ValueError('encoding exceeds its depth or 4096-node work budget')
        start, qualifiers, pointers = self.position, [], 0
        while self.peek() in QUALIFIERS:
            qualifiers.append(self.take())
        while self.peek() == '^':
            pointers += 1
            self.position += 1
            if depth+pointers > MAX_ENCODING_DEPTH:
                raise ValueError('encoding pointer count exceeds 64')
            while self.peek() in QUALIFIERS:
                qualifiers.append(self.take())
        code = self.take()
        if code in '{(':
            closing, kind = ('}', 'struct') if code == '{' else (')', 'union')
            first = self.position
            while self.peek() and self.peek() not in ('=', closing):
                if self.peek() in '{}()[]"' or ord(self.peek()) < 32:
                    raise ValueError('encoding aggregate tag is malformed')
                self.position += 1
            name = self.text[first:self.position]
            if not name or not self.peek():
                raise ValueError('encoding aggregate tag or terminator is missing')
            aggregate = object.__new__(quay_Struct_Representation)
            aggregate.name, aggregate.kind, aggregate.fields, aggregate.field_names = name, kind, [], []
            aggregate.encoding = self.text[start:]
            if self.take() == '=':
                while self.peek() and self.peek() != closing:
                    field_name = self.quoted() if self.peek() == '"' else ''
                    aggregate.field_names.append(field_name)
                    aggregate.fields.append(self.type(depth+1))
                if self.take() != closing:
                    raise ValueError('encoding aggregate has a mismatched terminator')
            aggregate.encoding = self.text[start:self.position]
            self.aggregates.append(aggregate)
            node = _node(aggregate, quay_EncodedType.STRUCT)
        elif code in ('j','A'):
            child = self.type(depth+1)
            arithmetic = {'c':'char','C':'unsigned char','s':'short','S':'unsigned short',
                'i':'int','I':'unsigned int','l':'long','L':'unsigned long',
                'q':'long long','Q':'unsigned long long','f':'float','d':'double','D':'long double'}
            if code == 'j' and child.encoding not in arithmetic:
                raise ValueError('Objective-C complex encoding requires an arithmetic type')
            node = _node(('_Complex '+arithmetic[child.encoding])
                         if code == 'j' else '_Atomic('+child.declaration('').strip()+')',
                         child=child)
        elif code == '[':
            count = self.number()
            element = self.type(depth+1)
            if self.take() != ']':
                raise ValueError('encoding array has a mismatched terminator')
            node = _node(str(element)+f' [{count}]', child=element, array_count=count)
        elif code == '"':
            self.position -= 1
            node = _node(self.quoted(), quay_EncodedType.NAMED, object_type=True)
        elif code == '@' and self.peek() == '"':
            node = _node(self.quoted(), quay_EncodedType.NAMED, object_type=True)
        elif code == '@' and self.peek() == '?':
            self.position += 1
            node = _node('id', object_type=True, block=True)
        elif code in quay_type_encodings:
            node = _node(quay_type_encodings[code], object_type=code == '@')
            if code == 'b' and self.peek() in '0123456789' and self.peek():
                node.bit_width = self.number()
                node.value = 'unsigned int'
        else:
            raise ValueError(f'unsupported Objective-C type code {code!r}')
        node.pointer_count, node.qualifiers = pointers, tuple(qualifiers)
        node.encoding = self.text[start:self.position]
        return node

    def sequence(self):
        values = []
        while self.position < len(self.text):
            node = self.type(0)
            sign = 1
            if self.peek() in ('+', '-'):
                sign = -1 if self.take() == '-' else 1
                node.offset = sign*self.number()
            else:
                number = self.number(required=False)
                if number is not None:
                    node.offset = number
            values.append(node)
        return values


@_name_boundary.class_contract('TypeProcessor', {name: 'quay_'+name for name in
    ('save_struct', 'process', 'tokenize', 'structs', 'type_cache')})
class quay_TypeProcessor:
    def __init__(self):
        self.structs, self.type_cache = {}, OrderedDict()
        self._cache_chars, self._cache_nodes = 0, 0
        self._cache_counts = {}
        self._registry_chars = 0

    def quay_save_struct(self, struct_to_save):
        prior = self.structs.get(struct_to_save.name)
        if prior is None or not prior.fields or (any(struct_to_save.field_names) and not any(prior.field_names)):
            if prior is None and len(self.structs) >= MAX_ENCODING_NODES:
                raise ValueError('encoding struct registry exceeds 4096 records')
            size = len(struct_to_save.encoding) - (len(prior.encoding) if prior else 0)
            if self._registry_chars+size > MAX_CACHE_CHARS:
                raise ValueError('encoding struct registry exceeds 1 MiB')
            self.structs[struct_to_save.name] = deepcopy(struct_to_save)
            self._registry_chars += size

    def quay_process(self, type_to_process):
        if not isinstance(type_to_process, str):
            raise TypeError('Objective-C type encoding must be text')
        if type_to_process in self.type_cache:
            values = self.type_cache.pop(type_to_process)
            self.type_cache[type_to_process] = values
            return deepcopy(values)
        parser = _Parser(self, type_to_process)
        values = parser.sequence()
        for aggregate in parser.aggregates:
            self.save_struct(aggregate)
        while self.type_cache and (len(self.type_cache) >= MAX_CACHE_ENTRIES or
              self._cache_chars+len(type_to_process) > MAX_CACHE_CHARS or
              self._cache_nodes+parser.nodes > MAX_CACHE_NODES):
            key, _ = self.type_cache.popitem(last=False)
            self._cache_chars -= len(key)
            self._cache_nodes -= self._cache_counts.pop(key)
        self.type_cache[type_to_process] = deepcopy(values)
        self._cache_counts[type_to_process] = parser.nodes
        self._cache_chars += len(type_to_process)
        self._cache_nodes += parser.nodes
        return values

    @staticmethod
    def quay_tokenize(type_to_tokenize):
        parser = _Parser(None, type_to_tokenize)
        values = parser.sequence()
        result = []
        for node in values:
            encoded = node.encoding
            # Keep the legacy pointer tokens for consumers that inspect syntax.
            prefix = 0
            while prefix < len(encoded) and encoded[prefix] == '^':
                result.append('^')
                prefix += 1
            body = encoded[prefix:]
            result.append(body[1:] if body.startswith('@"') else body)
        return result


_name_boundary.module_contract(globals(), {'Type': 'quay_Type',
    'Struct_Representation': 'quay_Struct_Representation', 'TypeProcessor': 'quay_TypeProcessor',
    'EncodedType': 'quay_EncodedType', 'type_encodings': 'quay_type_encodings'})
