# Derived from src/ktool/structs.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  structs.py
#
#  This file contains objc2 structs conforming to the ktool_macho struct system.
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary
from imagequay_support.record_engine import *

@_name_boundary.class_contract('objc2_class', {'FIELDS': 'quay_FIELDS', 'isa': 'quay_isa', 'superclass': 'quay_superclass', 'cache': 'quay_cache', 'vtable': 'quay_vtable', 'info': 'quay_info'})
class quay_objc2_class(quay_Struct):
    quay_FIELDS = {'isa': quay_uintptr_t, 'superclass': quay_uintptr_t, 'cache': quay_uintptr_t, 'vtable': quay_uintptr_t, 'info': quay_uintptr_t}

    @_name_boundary.callable_contract({'self': 'quay_self_8942e5f', 'byte_order': 'quay_byte_order_c3e9cfe'}, '__init__')
    def __init__(quay_self_8942e5f, quay_byte_order_c3e9cfe='little'):
        super().__init__(byte_order=quay_byte_order_c3e9cfe)
        _name_boundary.attributes(quay_self_8942e5f)['isa'] = 0
        _name_boundary.attributes(quay_self_8942e5f)['superclass'] = 0
        _name_boundary.attributes(quay_self_8942e5f)['cache'] = 0
        _name_boundary.attributes(quay_self_8942e5f)['vtable'] = 0
        _name_boundary.attributes(quay_self_8942e5f)['info'] = 0

@_name_boundary.class_contract('objc2_class_ro', {'FIELDS': 'quay_FIELDS', 'flags': 'quay_flags', 'ivar_base_start': 'quay_ivar_base_start', 'ivar_base_size': 'quay_ivar_base_size', 'reserved': 'quay_reserved', 'ivar_lyt': 'quay_ivar_lyt', 'name': 'quay_name', 'base_meths': 'quay_base_meths', 'base_prots': 'quay_base_prots', 'ivars': 'quay_ivars', 'weak_ivar_lyt': 'quay_weak_ivar_lyt', 'base_props': 'quay_base_props'})
class quay_objc2_class_ro(quay_Struct):
    quay_FIELDS = {'flags': quay_uint32_t, 'ivar_base_start': quay_uint32_t, 'ivar_base_size': quay_uint32_t, 'reserved': quay_pad_for_64_bit_only(4), 'ivar_lyt': quay_uintptr_t, 'name': quay_uintptr_t, 'base_meths': quay_uintptr_t, 'base_prots': quay_uintptr_t, 'ivars': quay_uintptr_t, 'weak_ivar_lyt': quay_uintptr_t, 'base_props': quay_uintptr_t}

    @_name_boundary.callable_contract({'self': 'quay_self_a0c513d', 'byte_order': 'quay_byte_order_0e9db5a'}, '__init__')
    def __init__(quay_self_a0c513d, quay_byte_order_0e9db5a='little'):
        super().__init__(byte_order=quay_byte_order_0e9db5a)
        _name_boundary.attributes(quay_self_a0c513d)['flags'] = 0
        _name_boundary.attributes(quay_self_a0c513d)['ivar_base_start'] = 0
        _name_boundary.attributes(quay_self_a0c513d)['ivar_base_size'] = 0
        _name_boundary.attributes(quay_self_a0c513d)['reserved'] = 0
        _name_boundary.attributes(quay_self_a0c513d)['ivar_lyt'] = 0
        _name_boundary.attributes(quay_self_a0c513d)['name'] = 0
        _name_boundary.attributes(quay_self_a0c513d)['base_meths'] = 0
        _name_boundary.attributes(quay_self_a0c513d)['base_prots'] = 0
        _name_boundary.attributes(quay_self_a0c513d)['ivars'] = 0
        _name_boundary.attributes(quay_self_a0c513d)['weak_ivar_lyt'] = 0
        _name_boundary.attributes(quay_self_a0c513d)['base_props'] = 0

@_name_boundary.class_contract('objc2_meth', {'FIELDS': 'quay_FIELDS', 'selector': 'quay_selector', 'types': 'quay_types', 'imp': 'quay_imp'})
class quay_objc2_meth(quay_Struct):
    quay_FIELDS = {'selector': quay_uintptr_t, 'types': quay_uintptr_t, 'imp': quay_uintptr_t}

    @_name_boundary.callable_contract({'self': 'quay_self_4abbe90', 'byte_order': 'quay_byte_order_42f386d'}, '__init__')
    def __init__(quay_self_4abbe90, quay_byte_order_42f386d='little'):
        super().__init__(byte_order=quay_byte_order_42f386d)
        _name_boundary.attributes(quay_self_4abbe90)['selector'] = 0
        _name_boundary.attributes(quay_self_4abbe90)['types'] = 0
        _name_boundary.attributes(quay_self_4abbe90)['imp'] = 0

@_name_boundary.class_contract('objc2_meth_list_entry', {'FIELDS': 'quay_FIELDS', 'selector': 'quay_selector', 'types': 'quay_types', 'imp': 'quay_imp'})
class quay_objc2_meth_list_entry(quay_Struct):
    quay_FIELDS = {'selector': quay_uint32_t, 'types': quay_uint32_t, 'imp': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_3ee9e61', 'byte_order': 'quay_byte_order_a4415eb'}, '__init__')
    def __init__(quay_self_3ee9e61, quay_byte_order_a4415eb='little'):
        super().__init__(byte_order=quay_byte_order_a4415eb)
        _name_boundary.attributes(quay_self_3ee9e61)['selector'] = 0
        _name_boundary.attributes(quay_self_3ee9e61)['types'] = 0
        _name_boundary.attributes(quay_self_3ee9e61)['imp'] = 0

@_name_boundary.class_contract('objc2_meth_list', {'FIELDS': 'quay_FIELDS', 'entrysize': 'quay_entrysize', 'count': 'quay_count'})
class quay_objc2_meth_list(quay_Struct):
    quay_FIELDS = {'entrysize': quay_uint32_t, 'count': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_b0e6784', 'byte_order': 'quay_byte_order_04f6f60'}, '__init__')
    def __init__(quay_self_b0e6784, quay_byte_order_04f6f60='little'):
        super().__init__(byte_order=quay_byte_order_04f6f60)
        _name_boundary.attributes(quay_self_b0e6784)['entrysize'] = 0
        _name_boundary.attributes(quay_self_b0e6784)['count'] = 0

@_name_boundary.class_contract('objc2_prop_list', {'FIELDS': 'quay_FIELDS', 'entrysize': 'quay_entrysize', 'count': 'quay_count'})
class quay_objc2_prop_list(quay_Struct):
    quay_FIELDS = {'entrysize': quay_uint32_t, 'count': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_63077f9', 'byte_order': 'quay_byte_order_1facaa7'}, '__init__')
    def __init__(quay_self_63077f9, quay_byte_order_1facaa7='little'):
        super().__init__(byte_order=quay_byte_order_1facaa7)
        _name_boundary.attributes(quay_self_63077f9)['entrysize'] = 0
        _name_boundary.attributes(quay_self_63077f9)['count'] = 0

@_name_boundary.class_contract('objc2_prop', {'FIELDS': 'quay_FIELDS', 'name': 'quay_name', 'attr': 'quay_attr'})
class quay_objc2_prop(quay_Struct):
    quay_FIELDS = {'name': quay_uintptr_t, 'attr': quay_uintptr_t}

    @_name_boundary.callable_contract({'self': 'quay_self_19d1c1e', 'byte_order': 'quay_byte_order_4ce904c'}, '__init__')
    def __init__(quay_self_19d1c1e, quay_byte_order_4ce904c='little'):
        super().__init__(byte_order=quay_byte_order_4ce904c)
        _name_boundary.attributes(quay_self_19d1c1e)['name'] = 0
        _name_boundary.attributes(quay_self_19d1c1e)['attr'] = 0

@_name_boundary.class_contract('objc2_prot_list', {'FIELDS': 'quay_FIELDS', 'cnt': 'quay_cnt'})
class quay_objc2_prot_list(quay_Struct):
    quay_FIELDS = {'cnt': quay_uintptr_t}

    @_name_boundary.callable_contract({'self': 'quay_self_a3d4952', 'byte_order': 'quay_byte_order_4aeaf94'}, '__init__')
    def __init__(quay_self_a3d4952, quay_byte_order_4aeaf94='little'):
        super().__init__(byte_order=quay_byte_order_4aeaf94)
        _name_boundary.attributes(quay_self_a3d4952)['cnt'] = 0

@_name_boundary.class_contract('objc2_prot', {'FIELDS': 'quay_FIELDS', 'isa': 'quay_isa', 'name': 'quay_name', 'prots': 'quay_prots', 'inst_meths': 'quay_inst_meths', 'class_meths': 'quay_class_meths', 'opt_inst_meths': 'quay_opt_inst_meths', 'opt_class_meths': 'quay_opt_class_meths', 'inst_props': 'quay_inst_props', 'cb': 'quay_cb', 'flags': 'quay_flags'})
class quay_objc2_prot(quay_Struct):
    quay_FIELDS = {'isa': quay_uintptr_t, 'name': quay_uintptr_t, 'prots': quay_uintptr_t, 'inst_meths': quay_uintptr_t, 'class_meths': quay_uintptr_t, 'opt_inst_meths': quay_uintptr_t, 'opt_class_meths': quay_uintptr_t, 'inst_props': quay_uintptr_t, 'cb': quay_uint32_t, 'flags': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_376da70', 'byte_order': 'quay_byte_order_abc5f3e'}, '__init__')
    def __init__(quay_self_376da70, quay_byte_order_abc5f3e='little'):
        super().__init__(byte_order=quay_byte_order_abc5f3e)
        _name_boundary.attributes(quay_self_376da70)['isa'] = 0
        _name_boundary.attributes(quay_self_376da70)['name'] = 0
        _name_boundary.attributes(quay_self_376da70)['prots'] = 0
        _name_boundary.attributes(quay_self_376da70)['inst_meths'] = 0
        _name_boundary.attributes(quay_self_376da70)['class_meths'] = 0
        _name_boundary.attributes(quay_self_376da70)['opt_inst_meths'] = 0
        _name_boundary.attributes(quay_self_376da70)['opt_class_meths'] = 0
        _name_boundary.attributes(quay_self_376da70)['inst_props'] = 0
        _name_boundary.attributes(quay_self_376da70)['cb'] = 0
        _name_boundary.attributes(quay_self_376da70)['flags'] = 0

@_name_boundary.class_contract('objc2_ivar_list', {'FIELDS': 'quay_FIELDS', 'entrysize': 'quay_entrysize', 'cnt': 'quay_cnt'})
class quay_objc2_ivar_list(quay_Struct):
    quay_FIELDS = {'entrysize': quay_uint32_t, 'cnt': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_fc6d06c', 'byte_order': 'quay_byte_order_de822c9'}, '__init__')
    def __init__(quay_self_fc6d06c, quay_byte_order_de822c9='little'):
        super().__init__(byte_order=quay_byte_order_de822c9)
        _name_boundary.attributes(quay_self_fc6d06c)['entrysize'] = 0
        _name_boundary.attributes(quay_self_fc6d06c)['cnt'] = 0

@_name_boundary.class_contract('objc2_ivar', {'FIELDS': 'quay_FIELDS', 'offs': 'quay_offs', 'name': 'quay_name', 'type': 'quay_type', 'align': 'quay_align', 'size': 'quay_size'})
class quay_objc2_ivar(quay_Struct):
    quay_FIELDS = {'offs': quay_uintptr_t, 'name': quay_uintptr_t, 'type': quay_uintptr_t, 'align': quay_uint32_t, 'size': quay_uint32_t}

    @_name_boundary.callable_contract({'self': 'quay_self_7a5412e', 'byte_order': 'quay_byte_order_ecd5475'}, '__init__')
    def __init__(quay_self_7a5412e, quay_byte_order_ecd5475='little'):
        super().__init__(byte_order=quay_byte_order_ecd5475)
        _name_boundary.attributes(quay_self_7a5412e)['offs'] = 0
        _name_boundary.attributes(quay_self_7a5412e)['name'] = 0

@_name_boundary.class_contract('objc2_category', {'FIELDS': 'quay_FIELDS', 'name': 'quay_name', 's_class': 'quay_s_class', 'inst_meths': 'quay_inst_meths', 'class_meths': 'quay_class_meths', 'prots': 'quay_prots', 'props': 'quay_props'})
class quay_objc2_category(quay_Struct):
    quay_FIELDS = {'name': quay_uintptr_t, 's_class': quay_uintptr_t, 'inst_meths': quay_uintptr_t, 'class_meths': quay_uintptr_t, 'prots': quay_uintptr_t, 'props': quay_uintptr_t}

    @_name_boundary.callable_contract({'self': 'quay_self_bf59704', 'byte_order': 'quay_byte_order_e46b232'}, '__init__')
    def __init__(quay_self_bf59704, quay_byte_order_e46b232='little'):
        super().__init__(byte_order=quay_byte_order_e46b232)
        _name_boundary.attributes(quay_self_bf59704)['name'] = 0
        _name_boundary.attributes(quay_self_bf59704)['s_class'] = 0
        _name_boundary.attributes(quay_self_bf59704)['inst_meths'] = 0
        _name_boundary.attributes(quay_self_bf59704)['class_meths'] = 0
        _name_boundary.attributes(quay_self_bf59704)['prots'] = 0
        _name_boundary.attributes(quay_self_bf59704)['props'] = 0
_name_boundary.module_contract(globals(), {'objc2_category': 'quay_objc2_category', 'objc2_prop': 'quay_objc2_prop', 'objc2_prop_list': 'quay_objc2_prop_list', 'objc2_class': 'quay_objc2_class', 'objc2_meth': 'quay_objc2_meth', 'objc2_meth_list': 'quay_objc2_meth_list', 'objc2_ivar_list': 'quay_objc2_ivar_list', 'objc2_meth_list_entry': 'quay_objc2_meth_list_entry', 'objc2_prot_list': 'quay_objc2_prot_list', 'objc2_prot': 'quay_objc2_prot', 'objc2_ivar': 'quay_objc2_ivar', 'objc2_class_ro': 'quay_objc2_class_ro'})
