# Derived public Objective-C API from ktool; Copyright (c) 0cyn 2021, MIT in LICENSE.
"""Snapshot-scoped Objective-C graph inspection with visible partial results.

Static lists are checked before walking; imports remain external references.
Neither chained pointers nor the caller's bytes are patched during inspection.
"""
from enum import Enum
from itertools import islice
import imagequay_boundary as _name_boundary
from imagequay.objc_encoding import (quay_Type, quay_Struct_Representation,
    quay_TypeProcessor, quay_EncodedType, quay_type_encodings, MAX_ENCODING_CHARS)
from imagequay.objc_records import *
from imagequay.metadata_graph import MetadataGraph, MAX_GRAPH_RECORDS
from imagequay_layout.record_contract import quay_Constructable
from imagequay.formatting import quay_ignore, quay_opts
from imagequay.failure_types import quay_MalformedMachOException as Malformed

quay_RELATIVE_METHODS_SELECTORS_ARE_DIRECT_FLAG = 1 << 30
quay_RELATIVE_METHOD_FLAG = 1 << 31
quay_METHOD_LIST_FLAGS_MASK = 0xffff0003
quay_attr_encodings = {'&':'retain','N':'nonatomic','W':'weak','R':'readonly','C':'copy'}
quay_property_attr = _name_boundary.named_record('property_attr',
    ['type','attributes','ivar','is_id','typestr','getter','setter','is_dynamic'])


def _contract(label, fields=(), methods=()):
    return _name_boundary.class_contract(label, {name:'quay_'+name for name in
        ('from_image','from_values','raw_bytes','serialize')+tuple(fields)+tuple(methods)})


def _finite(items):
    values = list(islice(iter(items), MAX_GRAPH_RECORDS+1))
    if len(values) > MAX_GRAPH_RECORDS:
        raise ValueError('Objective-C values exceed the 1048576-record budget')
    return values


def _raw(model):
    if model._snapshot is None:
        raise ValueError('Objective-C metadata assembled from values has no encoded snapshot')
    return bytes(model._snapshot)


def _typename(node, *, method=False):
    if node.type == quay_EncodedType.STRUCT:
        prefix = node.value.kind+' ' if method else ''
        return prefix+node.value.name+(' '+'*'*node.pointer_count if node.pointer_count else '')
    if node.type == quay_EncodedType.NAMED:
        if str(node.value).startswith('<'):
            return 'id'+str(node.value)+(' '+'*'*node.pointer_count if node.pointer_count else '')
        return str(node.value)+(' '+'*'*(node.pointer_count+1))
    return str(node)


def _structs(types):
    return [node.value for node in types if node.type == quay_EncodedType.STRUCT]


def _symbol_class(symbol):
    name = symbol.fullname
    for prefix in ('_OBJC_CLASS_$_','_OBJC_METACLASS_$_'):
        if name.startswith(prefix):
            return name[len(prefix):]
    return symbol.name.lstrip('_')


@_contract('EncodingType')
class quay_EncodingType(Enum):
    METHOD=0
    PROPERTY=1
    IVAR=2


@_contract('ObjCImage', ('image','tp','classlist','catlist','protolist','class_map',
    'cat_map','prot_map','name'), ('vm_check','read_uint','read_ptr','read_struct',
    'read_fixed_len_str','read_cstr'))
class quay_ObjCImage(quay_Constructable):
    def __init__(self, image, type_processor=None):
        self.image, self.tp = image, type_processor or quay_TypeProcessor()
        self.name = getattr(image,'base_name','')
        self.classlist, self.catlist, self.protolist = [], [], []
        self.class_map, self.cat_map, self.prot_map = {}, {}, {}
        self.errors, self.complete, self._snapshots = [], True, []
        self._graph = MetadataGraph(image) if image is not None else None
        self._active, self._class_variants = set(), {}
        self._error_chars = 0

    def attempt(self, label, callback, errors=None):
        try:
            return callback()
        except (Malformed, ValueError, UnicodeError, IndexError) as error:
            if (not quay_ignore.OBJC_ERRORS or (self._graph is not None and
                (self._graph.remaining <= 0 or self.image.slice.file._generation != self._graph.generation))):
                raise
            self.complete = False
            text = label+': '+type(error).__name__+': '+str(error)
            # Diagnostics have their own finite memory budget. Count omissions
            # explicitly instead of allowing errors to allocate without limit.
            if self._error_chars+len(text) <= 4 << 20:
                self.errors.append(text)
                self._error_chars += len(text)
                if errors is not None:
                    errors.append(text)
            else:
                self.omitted_error_count = getattr(self,'omitted_error_count',0)+1
            return None

    @classmethod
    def quay_from_image(cls, image):
        result = cls(image)
        sections = {'__objc_classlist':('classlist',quay_Class),
                    '__objc_catlist':('catlist',quay_Category),
                    '__objc_protolist':('protolist',quay_Protocol)}
        for segment in image.segments.values():
            for section in segment.sections.values():
                if section.name not in sections:
                    continue
                if section.size % image.ptr_size:
                    raise Malformed('Objective-C section has a partial pointer')
                result._graph.use(section.size//image.ptr_size)
                result._snapshots.append(result._graph.bytes(section.vm_address,section.size) if section.size else b'')
                destination, model = sections[section.name]
                for offset in range(0,section.size,image.ptr_size):
                    field = section.vm_address+offset
                    if model is quay_Protocol:
                        def load(field=field):
                            location=result.read_ptr(field,vm=True)
                            if not location:return None
                            record=result.read_struct(location,quay_objc2_prot,vm=True)
                            return quay_Protocol.from_image(result,record,location)
                    else:
                        def load(field=field,model=model):return model.from_image(result,field)
                    item = result.attempt(section.name+f' at {field:#x}',load)
                    if item is not None and item not in getattr(result,destination):
                        getattr(result,destination).append(item)
        return result

    @classmethod
    def quay_from_values(cls, image, name, classlist, catlist, protolist, type_processor=None):
        result=cls(image,type_processor)
        result.name=name
        result.classlist,result.catlist,result.protolist = map(_finite,(classlist,catlist,protolist))
        result.class_map={item.loc:item for item in result.classlist}
        result.cat_map={item.loc:item for item in result.catlist}
        result.prot_map={item.loc:item for item in result.protolist}
        result.complete=not any(item.load_errors for item in result.classlist+result.catlist+result.protolist)
        return result

    def quay_raw_bytes(self):return b''.join(self._snapshots)
    def quay_serialize(self):
        result={'classes':[item.serialize() for item in self.classlist],
                'categories':[item.serialize() for item in self.catlist],
                'protocols':[item.serialize() for item in self.protolist]}
        if not self.complete:
            result['metadata-status']={'complete':False,'errors':list(self.errors),
                'omitted_error_count':getattr(self,'omitted_error_count',0)}
        return result

    def quay_vm_check(self,address):
        try:self._graph.span(address,1);return True
        except Malformed:return False

    def quay_read_uint(self,offset,length,vm=False):
        return self._graph.uint(offset,length) if vm else self.image.read_uint(offset,length)
    def quay_read_ptr(self,offset,vm=False):
        return self._graph.pointer(offset) if vm else self.image.read_ptr(offset)
    def quay_read_struct(self,addr,struct_type,vm=True,endian=None):
        endian = endian or self.image.slice.byte_order
        if vm:
            if endian != self.image.slice.byte_order:
                raise ValueError('Objective-C record byte order must match its image')
            return self._graph.record(addr,struct_type,relocate_pointers=True)
        return self.image.read_struct(addr,struct_type,vm=False,endian=endian)
    def quay_read_fixed_len_str(self,addr,count,vm=True):
        raw=self._graph.bytes(addr,count) if vm else bytes(self.image.read_bytearray(addr,count))
        return raw.decode('utf-8').rstrip('\0')
    def quay_read_cstr(self,addr,limit=0,vm=True):
        value=self._graph.string(addr) if vm else self.image.read_cstr(addr,limit,vm=False)
        if limit and len(value.encode('utf-8')) > limit:
            raise Malformed('Objective-C string exceeds the explicit limit')
        return value

    def enter(self,kind,location):
        key=kind,location
        if key in self._active:
            raise Malformed('Objective-C metadata graph has an inheritance cycle')
        if len(self._active)>=64:
            raise Malformed('Objective-C metadata graph exceeds 64 levels')
        self._active.add(key)
        self._graph.use()
        return key


def _list_entries(objc,location,record_type,count_name='count'):
    if not location:return ()
    head=objc.read_struct(location,record_type)
    count=getattr(head,count_name)
    stride=head.entrysize
    expected = 2*objc.image.ptr_size if record_type is quay_objc2_prop_list else 3*objc.image.ptr_size+8
    if stride < expected or stride > 4096:
        raise Malformed('Objective-C list entry size is smaller than its record or exceeds 4096')
    objc._graph.use(count)
    objc._graph.span(location,8+count*stride)
    return (location+8+index*stride for index in range(count))


def _properties(objc,location,errors):
    values=[]
    for address in _list_entries(objc,location,quay_objc2_prop_list):
        item=objc.attempt(f'property at {address:#x}',
            lambda address=address:quay_Property.from_image(objc,objc.read_struct(address,quay_objc2_prop)),errors)
        if item is not None:values.append(item)
    return values


def _protocols(objc,location,errors):
    if not location:return []
    count=objc._graph.uint(location,objc.image.ptr_size)
    objc._graph.use(count)
    objc._graph.span(location,(count+1)*objc.image.ptr_size)
    result=[]
    for index in range(count):
        address=objc.read_ptr(location+(index+1)*objc.image.ptr_size,vm=True)
        if not address:continue
        item=objc.attempt(f'protocol at {address:#x}',
            lambda address=address:quay_Protocol.from_image(objc,objc.read_struct(address,quay_objc2_prot),address),errors)
        if item is not None:result.append(item)
    return result


@_contract('Ivar', ('name','typestr','is_id','offset','type'), ('_renderable_type',))
class quay_Ivar(quay_Constructable):
    @classmethod
    def quay_from_image(cls,objc_image,ivar):
        result=cls(objc_image.read_cstr(ivar.name),objc_image.read_cstr(ivar.type),objc_image.tp,
                   offset=objc_image._graph.uint(ivar.offs,4) if ivar.offs else 0)
        result.offset_location=ivar.offs
        result._snapshot=getattr(ivar,'disk_raw',None)
        return result
    @classmethod
    def quay_from_values(cls,name,type_encoding,type_processor=None,offset=0):
        return cls(name,type_encoding,type_processor or quay_TypeProcessor(),offset)
    def quay_raw_bytes(self):return _raw(self)
    def __init__(self,name,type_encoding,type_processor,offset=0):
        values=type_processor.process(type_encoding)
        if len(values)!=1:raise ValueError('Objective-C ivar requires one type')
        self.name,self.typestr,self.offset=name,type_encoding,offset
        self.encoded_type=values[0]
        self.is_id=self.encoded_type.object_type
        self.type=_typename(self.encoded_type)
        self._snapshot=None
    def quay_serialize(self):
        return {'name':self.name,'type':self.type,'type_is_id':self.is_id,'typestring':self.typestr,'rendered':str(self)}
    def __str__(self):return self.encoded_type.declaration(self.name)
    @staticmethod
    def quay__renderable_type(ivar_type):return _typename(ivar_type)


@_contract('Method', ('meta','sel','type_string','types','imp','return_string','arguments','signature'),
    ('_renderable_type','_build_method_signature'))
class quay_Method(quay_Constructable):
    @classmethod
    def quay_from_image(cls,objc_image,sel_addr,types_addr,imp,is_meta,vm_addr,rms,rms_are_direct,rms_base=None):
        if rms:
            # Every signed displacement is relative to its own storage field.
            # The IMP field is a nonnullable relative pointer. A zero encoded
            # displacement points at that field, rather than denoting null.
            imp = vm_addr+8+imp
            objc_image._graph.span(imp,1)
            type_location=objc_image._graph.relative(vm_addr+4,types_addr,nullable=False)
            if rms_are_direct:
                selector_location=(rms_base+sel_addr if rms_base is not None else
                    objc_image._graph.relative(vm_addr,sel_addr,nullable=False))
            else:
                slot=objc_image._graph.relative(vm_addr,sel_addr,nullable=False)
                selector_location=objc_image.read_ptr(slot,vm=True)
        else:
            selector_location,type_location=sel_addr,types_addr
        symbol=objc_image.image.symbols.get(imp) if quay_opts.USE_SYMTAB_INSTEAD_OF_SELECTORS else None
        if symbol is not None:
            matched=symbol.fullname.rsplit(' ',1)[-1]
            selector=matched[:-1] if matched.endswith(']') else matched
        else:
            selector=objc_image.read_cstr(selector_location)
        result=cls(is_meta,selector,objc_image.read_cstr(type_location),objc_image.tp,imp)
        return result
    @classmethod
    def quay_from_values(cls,sel,type_string,is_meta=False,type_processor=None,imp=None):
        return cls(is_meta,sel,type_string,type_processor or quay_TypeProcessor(),imp)
    def quay_raw_bytes(self):return _raw(self)
    def __init__(self,meta,sel,type_string,type_processor,imp):
        self.meta,self.sel,self.type_string,self.imp=meta,sel,type_string,imp
        self.types=type_processor.process(type_string)
        self.return_string=_typename(self.types[0],method=True)
        self.arguments=[_typename(value,method=True) for value in self.types[1:]]
        self.signature=self._build_method_signature()
        self._snapshot=None
    def quay_serialize(self):
        return {'selector':self.sel,'arguments':self.arguments,'return_type':self.return_string,
                'signature':self.signature,'typestring':self.type_string}
    def __str__(self):return self.signature
    @staticmethod
    def quay__renderable_type(method_type):return _typename(method_type,method=True)
    def quay__build_method_signature(self):
        prefix=('+' if self.meta else '-')+'('+self.return_string+')'
        count=self.sel.count(':')
        if len(self.arguments)!=count+2 or (count and not self.sel.endswith(':')):
            raise ValueError('Objective-C selector argument count does not match its encoding')
        if count==0:return prefix+self.sel
        parts=self.sel.split(':')[:-1]
        return prefix+''.join(part+':('+self.arguments[index+2]+')arg'+str(index)+' ' for index,part in enumerate(parts))


@_contract('MethodList', ('objc_image','methlist_head','meta','name','load_errors','methods','struct_list','CUSTOM_RMS_BASE'), ('_process_methlist',))
class quay_MethodList:
    quay_CUSTOM_RMS_BASE=None
    def __init__(self,image,methlist_head,base_meths,class_meta,class_name):
        self.objc_image,self.methlist_head,self.meta,self.name=image,methlist_head,class_meta,class_name
        self.load_errors,self.methods,self.struct_list=[],[],[]
        if base_meths:
            self.methods=self._process_methlist(base_meths)
    def quay__process_methlist(self,base_meths):
        image,head=self.objc_image,self.methlist_head
        if head is None:raise Malformed('Objective-C method list has no header')
        relative=bool(head.entrysize & quay_RELATIVE_METHOD_FLAG)
        direct=bool(head.entrysize & quay_RELATIVE_METHODS_SELECTORS_ARE_DIRECT_FLAG)
        stride=head.entrysize & ~quay_METHOD_LIST_FLAGS_MASK
        required=12 if relative else image.image.ptr_size*3
        if stride != required:
            raise Malformed('Objective-C method list entry size does not match its format')
        image._graph.use(head.count)
        image._graph.span(base_meths,8+head.count*stride)
        methods=[]
        for index in range(head.count):
            address=base_meths+8+index*stride
            width=4 if relative else image.image.ptr_size
            if relative:
                args=[image._graph.uint(address+offset*width,width,signed=True) for offset in range(3)]
            else:
                args=[image.read_ptr(address+offset*width,vm=True) for offset in range(3)]
            def load(address=address,args=args):
                value=quay_Method.from_image(image,*args,self.meta,address,relative,direct,
                    _name_boundary.read_attribute(type(self),'CUSTOM_RMS_BASE'))
                value._snapshot=image._graph.bytes(address,stride)
                return value
            item=image.attempt(f'method at {address:#x}',load,self.load_errors)
            if item is not None:
                methods.append(item)
                self.struct_list.extend(_structs(item.types))
        return methods


@_contract('LinkedClass', ('classname','libname'))
class quay_LinkedClass:
    def __init__(self,classname,libname):self.classname,self.libname=classname,libname


def _methods(objc,location,meta,name,errors,structs):
    if not location:return []
    result=quay_MethodList(objc,objc.read_struct(location,quay_objc2_meth_list),location,meta,name)
    errors.extend(result.load_errors)
    structs.extend(result.struct_list)
    return result.methods


def _load_optional(objc,label,callback,errors,default):
    value=objc.attempt(label,callback,errors)
    return default if value is None else value


@_contract('Class', ('name','meta','superclass','loc','load_errors','struct_list','linkedlibs',
    'linked_classes','fdec_classes','fdec_prots','methods','properties','protocols','ivars'))
class quay_Class(quay_Constructable):
    @classmethod
    def quay_from_image(cls,objc_image,class_ptr,meta=False,class_ptr_is_direct=False):
        objc=objc_image
        location=class_ptr if class_ptr_is_direct else objc.read_ptr(class_ptr,vm=True)
        if not location:return None
        cache_key=location,meta
        if cache_key in objc._class_variants:return objc._class_variants[cache_key]
        active=objc.enter('class',location)
        try:
            item=objc.read_struct(location,quay_objc2_class)
            # Low ABI flags differ between 32-bit and LP64; never erase upper
            # address bits or guess a process address from authentication bits.
            ro=objc.read_struct(item.info & (~7 if objc.image.ptr_size==8 else ~3),quay_objc2_class_ro)
            name=objc.read_cstr(ro.name)
            errors,structs=[],[]
            superclass=''
            if not meta:
                external=objc.image.import_table.get(location+objc.image.ptr_size)
                if external is not None:superclass=_symbol_class(external)
                elif item.superclass:
                    parent=_load_optional(objc,'superclass',lambda:cls.from_image(objc,item.superclass,class_ptr_is_direct=True),errors,None)
                    superclass=parent.name if parent is not None else ''
            methods=_load_optional(objc,'instance methods',lambda:_methods(objc,ro.base_meths,meta,name,errors,structs),errors,[])
            properties=_load_optional(objc,'properties',lambda:_properties(objc,ro.base_props,errors),errors,[])
            protocols=_load_optional(objc,'protocols',lambda:_protocols(objc,ro.base_prots,errors),errors,[])
            ivars=[]
            def load_ivars():
                for address in _list_entries(objc,ro.ivars,quay_objc2_ivar_list,'cnt'):
                    value=objc.attempt(f'ivar at {address:#x}',lambda address=address:quay_Ivar.from_image(objc,objc.read_struct(address,quay_objc2_ivar)),errors)
                    if value is not None:ivars.append(value)
            _load_optional(objc,'ivars',load_ivars,errors,None)
            if not meta and item.isa:
                metaclass=_load_optional(objc,'metaclass',lambda:cls.from_image(objc,item.isa,meta=True,class_ptr_is_direct=True),errors,None)
                if metaclass is not None:
                    methods.extend(metaclass.methods)
                    properties.extend(metaclass.properties)
                    errors.extend(metaclass.load_errors)
                    structs.extend(metaclass.struct_list)
            for prop in properties:structs.extend(_structs([prop.attr.type]))
            for ivar in ivars:structs.extend(_structs([ivar.encoded_type]))
            result=cls(name,meta,superclass,methods,properties,ivars,protocols,errors,structs,location)
            result._snapshot=item.disk_raw
            objc._class_variants[cache_key]=result
            objc.class_map[location]=result
            if not class_ptr_is_direct:objc.class_map[class_ptr]=result
            return result
        finally:objc._active.remove(active)
    @classmethod
    def quay_from_values(cls,name,superclass_name,methods,properties,ivars,protocols,load_errors=None,structs=None):
        return cls(name,False,superclass_name,methods,properties,ivars,protocols,load_errors,structs)
    def quay_raw_bytes(self):return _raw(self)
    def __init__(self,name,is_meta,superclass_name,methods,properties,ivars,protocols,load_errors=None,structs=None,loc=0):
        self.name,self.meta,self.superclass,self.loc=name,is_meta,superclass_name,loc
        self.methods,self.properties,self.ivars,self.protocols=map(_finite,(methods,properties,ivars,protocols))
        self.load_errors,self.struct_list=_finite(load_errors or []),_finite(structs or [])
        self.linkedlibs,self.linked_classes,self.fdec_classes,self.fdec_prots=[],[],[],[]
        self._snapshot=None
    def quay_serialize(self):
        return {'name':self.name,'superclass':self.superclass,'methods':[item.serialize() for item in self.methods],
                'properties':[item.serialize() for item in self.properties],
                'protocols':[item.name for item in self.protocols],'ivars':[item.serialize() for item in self.ivars]}
    def __str__(self):return self.name


def _property_parts(text):
    if not isinstance(text,str) or not text or len(text)>MAX_ENCODING_CHARS:
        raise ValueError('Objective-C property attributes are empty or exceed 16384 characters')
    parts,start,depth,quoted=[],0,0,False
    for index,char in enumerate(text):
        if char=='"':quoted=not quoted
        elif not quoted:
            if char in '{([':depth+=1
            elif char in '})]':depth-=1
            elif char==',' and depth==0:
                parts.append(text[start:index]);start=index+1
        if depth<0 or depth>64:raise ValueError('Objective-C property aggregate depth is invalid')
    if quoted or depth:raise ValueError('Objective-C property type is unterminated')
    parts.append(text[start:])
    if any(not part for part in parts):raise ValueError('Objective-C property attribute is empty')
    return parts


@_contract('Property', ('name','attr','attr_string','type','is_id','attributes','ivarname','getter','setter'),
    ('_renderable_type','decode_property_attributes'))
class quay_Property(quay_Constructable):
    @classmethod
    def quay_from_image(cls,objc_image,property):
        result=cls(objc_image.read_cstr(property.name),objc_image.read_cstr(property.attr),objc_image.tp)
        result._snapshot=getattr(property,'disk_raw',None)
        return result
    @classmethod
    def quay_from_values(cls,name,attr_string,type_processor=None):return cls(name,attr_string,type_processor or quay_TypeProcessor())
    def quay_raw_bytes(self):return _raw(self)
    def __init__(self,name,attr_string,type_processor):
        if not name:raise ValueError('Objective-C property name is empty')
        self.name,self.attr_string=name,attr_string
        self.attr=self.decode_property_attributes(type_processor,attr_string)
        self.type,self.is_id=_typename(self.attr.type),self.attr.is_id
        self.attributes,self.ivarname=self.attr.attributes,self.attr.ivar
        self.unknown_attributes=tuple(part for part in _property_parts(attr_string)
            if part[0] not in quay_attr_encodings and part[0] not in ('T','V','G','S','D'))
        self.getter=self.attr.getter or name
        self.setter=self.attr.setter or ('' if 'readonly' in self.attributes else 'set'+name[0].upper()+name[1:]+':')
        self._snapshot=None
    def quay_serialize(self):
        return {'name':self.name,'type':self.type,'is_id':self.is_id,'ivar_name':self.ivarname,
                'attributes':self.attributes,'attr_string':self.attr_string,'getter':self.getter,
                'setter':self.setter,'rendered':str(self)}
    def __str__(self):
        attrs='('+', '.join(self.attributes)+') ' if self.attributes else ''
        return '@property '+attrs+self.type+' '+self.name
    @staticmethod
    def quay__renderable_type(_type):return _typename(_type)
    @staticmethod
    def quay_decode_property_attributes(type_processor,type_str):
        parts=_property_parts(type_str)
        fields,attrs,unknown={},[],[]
        for part in parts:
            indicator=part[0]
            if indicator in ('T','V','G','S','D'):
                if indicator in fields:raise ValueError('Objective-C property attribute is duplicated')
                fields[indicator]=part[1:]
            elif indicator in quay_attr_encodings:
                if len(part)!=1:raise ValueError('Objective-C property flag has a payload')
                attrs.append(quay_attr_encodings[indicator])
            else:unknown.append(part)
        if 'T' not in fields:raise ValueError('Objective-C property has no type encoding')
        types=type_processor.process(fields['T'])
        if len(types)!=1:raise ValueError('Objective-C property requires exactly one type')
        for flag in ('G','S'):
            if flag in fields and not fields[flag]:raise ValueError('Objective-C property accessor is empty')
        if fields.get('G'):attrs.append('getter='+fields['G'])
        if fields.get('S'):attrs.append('setter='+fields['S'])
        return quay_property_attr(types[0],attrs,fields.get('V',''),types[0].object_type,
            type_str,fields.get('G'),fields.get('S'),'D' in fields)


@_contract('Category', ('name','classname','loc','load_errors','struct_list','methods','properties','protocols'))
class quay_Category(quay_Constructable):
    @classmethod
    def quay_from_image(cls,objc_image,category_ptr):
        objc=objc_image
        location=objc.read_ptr(category_ptr,vm=True)
        if not location:return None
        if location in objc.cat_map:return objc.cat_map[location]
        record=objc.read_struct(location,quay_objc2_category)
        name=objc.read_cstr(record.name)
        external=objc.image.import_table.get(location+objc.image.ptr_size)
        errors,structs=[],[]
        if external is not None:classname=_symbol_class(external)
        else:
            owner=_load_optional(objc,'category class',lambda:quay_Class.from_image(objc,record.s_class,class_ptr_is_direct=True),errors,None) if record.s_class else None
            classname=owner.name if owner is not None else ''
        methods=[]
        for meta,loc in ((False,record.inst_meths),(True,record.class_meths)):
            methods.extend(_load_optional(objc,'category methods',lambda meta=meta,loc=loc:_methods(objc,loc,meta,name,errors,structs),errors,[]))
        props=_load_optional(objc,'category properties',lambda:_properties(objc,record.props,errors),errors,[])
        protocols=_load_optional(objc,'category protocols',lambda:_protocols(objc,record.prots,errors),errors,[])
        result=cls(classname,name,methods,props,errors,structs,location)
        result.protocols=protocols
        result._snapshot=record.disk_raw
        objc.cat_map[location]=result
        return result
    @classmethod
    def quay_from_values(cls,classname,name,methods,properties,load_errors=None,struct_list=None):return cls(classname,name,methods,properties,load_errors,struct_list)
    def quay_raw_bytes(self):return _raw(self)
    def __init__(self,classname,name,methods,properties,load_errors=None,struct_list=None,loc=0):
        self.classname,self.name,self.loc=classname,name,loc
        self.methods,self.properties=map(_finite,(methods,properties))
        self.protocols,self.load_errors,self.struct_list=[],_finite(load_errors or []),_finite(struct_list or [])
        self._snapshot=None
    def quay_serialize(self):
        return {'name':self.name,'classname':self.classname,'methods':[item.serialize() for item in self.methods],
                'properties':[item.serialize() for item in self.properties],'protocols':[item.name for item in self.protocols]}


@_contract('Protocol', ('name','loc','load_errors','struct_list','methods','opt_methods','properties'), ('load_methods',))
class quay_Protocol(quay_Constructable):
    @classmethod
    def quay_from_image(cls,objc_image,protocol,loc):
        objc=objc_image
        if loc in objc.prot_map:return objc.prot_map[loc]
        active=objc.enter('protocol',loc)
        try:
            minimum=8*objc.image.ptr_size+8
            if protocol.cb<minimum:raise Malformed('Objective-C protocol declared size is shorter than its header')
            objc._graph.span(loc,protocol.cb)
            name=objc.read_cstr(protocol.name)
            methods,optional,errors,structs=[],[],[],[]
            for dest,meta,location in ((methods,False,protocol.inst_meths),(methods,True,protocol.class_meths),
                    (optional,False,protocol.opt_inst_meths),(optional,True,protocol.opt_class_meths)):
                dest.extend(_load_optional(objc,'protocol methods',lambda location=location,meta=meta:_methods(objc,location,meta,name,errors,structs),errors,[]))
            props=_load_optional(objc,'protocol properties',lambda:_properties(objc,protocol.inst_props,errors),errors,[])
            result=cls(name,methods,optional,props,errors,structs,loc)
            result.protocols=_load_optional(objc,'adopted protocols',lambda:_protocols(objc,protocol.prots,errors),errors,[])
            if protocol.cb >= minimum+3*objc.image.ptr_size:
                class_props=objc.read_ptr(loc+minimum+2*objc.image.ptr_size,vm=True)
                result.class_properties=_load_optional(objc,'protocol class properties',lambda:_properties(objc,class_props,errors),errors,[])
            for prop in props+result.class_properties:structs.extend(_structs([prop.attr.type]))
            result.load_errors,result.struct_list=list(errors),list(structs)
            result._snapshot=objc._graph.bytes(loc,protocol.cb)
            objc.prot_map[loc]=result
            return result
        finally:objc._active.remove(active)
    @classmethod
    def quay_load_methods(cls,objc_image,name,loc,meta=False):
        return quay_MethodList(objc_image,objc_image.read_struct(loc,quay_objc2_meth_list) if loc else None,loc,meta,name)
    @classmethod
    def quay_from_values(cls,name,methods,opt_methods,properties,load_errors=None,struct_list=None):return cls(name,methods,opt_methods,properties,load_errors,struct_list)
    def quay_raw_bytes(self):return _raw(self)
    def __init__(self,name,methods,opt_methods,properties,load_errors=None,struct_list=None,loc=0):
        self.name,self.loc=name,loc
        self.methods,self.opt_methods,self.properties=map(_finite,(methods,opt_methods,properties))
        self.load_errors,self.struct_list=_finite(load_errors or []),_finite(struct_list or [])
        self.protocols,self.class_properties,self._snapshot=[],[],None
    def quay_serialize(self):
        return {'name':self.name,'methods':[item.serialize() for item in self.methods],
                'optional-methods':[item.serialize() for item in self.opt_methods],
                'properties':[item.serialize() for item in self.properties]}
    def __str__(self):return self.name


_name_boundary.module_contract(globals(), {name:'quay_'+name for name in
    ('LinkedClass','Protocol','Type','METHOD_LIST_FLAGS_MASK','attr_encodings',
    'type_encodings','EncodedType','RELATIVE_METHOD_FLAG','EncodingType','Method',
    'MethodList','ignore','opts','Struct_Representation','Property','ObjCImage','Ivar',
    'Class','TypeProcessor','property_attr','Category','RELATIVE_METHODS_SELECTORS_ARE_DIRECT_FLAG')})
