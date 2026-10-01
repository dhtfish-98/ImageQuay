# Derived from src/ktool_macho/codesign.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool_macho
#  codesign.py
#
#
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2022.
#
import imagequay_boundary as _name_boundary
from imagequay_layout.binary_records import quay_Struct as quay_Struct, quay_uint32_t as quay_uint32_t
quay_CSMAGIC_REQUIREMENT = 4208856064
quay_CSMAGIC_REQUIREMENTS = 4208856065
quay_CSMAGIC_CODEDIRECTORY = 4208856066
quay_CSMAGIC_EMBEDDED_SIGNATURE = 4208856256
quay_CSMAGIC_EMBEDDED_SIGNATURE_OLD = 4208855810
quay_CSMAGIC_EMBEDDED_ENTITLEMENTS = 4208882033
quay_CSMAGIC_EMBEDDED_DERFORMAT = 4208882034
quay_CSMAGIC_DETACHED_SIGNATURE = 4208856257
quay_CSMAGIC_BLOBWRAPPER = 4208855809
quay_CSSLOT_CODEDIRECTORY = 0
quay_CSSLOT_INFOSLOT = 1
quay_CSSLOT_REQUIREMENTS = 2
quay_CSSLOT_RESOURCEDIR = 3
quay_CSSLOT_APPLICATION = 4
quay_CSSLOT_ENTITLEMENTS = 5
quay_CSSLOT_REPSPECIFIC = 6
quay_CSSLOT_DERFORMAT = 7
quay_CSSLOT_ALTERNATE = 4096

@_name_boundary.class_contract('BlobIndex', {'_FIELDNAMES': 'quay__FIELDNAMES', '_SIZES': 'quay__SIZES', 'SIZE': 'quay_SIZE', 'type': 'quay_type', 'offset': 'quay_offset'})
class quay_BlobIndex(quay_Struct):
    quay__FIELDNAMES = ['type', 'offset']
    quay__SIZES = [quay_uint32_t, quay_uint32_t]
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_06fde75', 'byte_order': 'quay_byte_order_945bab7'}, '__init__')
    def __init__(quay_self_06fde75, quay_byte_order_945bab7='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_06fde75)['_FIELDNAMES'], sizes=_name_boundary.attributes(quay_self_06fde75)['_SIZES'], byte_order=quay_byte_order_945bab7)
        _name_boundary.attributes(quay_self_06fde75)['type'] = 0
        _name_boundary.attributes(quay_self_06fde75)['offset'] = 0

@_name_boundary.class_contract('Blob', {'_FIELDNAMES': 'quay__FIELDNAMES', '_SIZES': 'quay__SIZES', 'SIZE': 'quay_SIZE', 'magic': 'quay_magic', 'length': 'quay_length'})
class quay_Blob(quay_Struct):
    quay__FIELDNAMES = ['magic', 'length']
    quay__SIZES = [quay_uint32_t, quay_uint32_t]
    quay_SIZE = 8

    @_name_boundary.callable_contract({'self': 'quay_self_3f1f12a', 'byte_order': 'quay_byte_order_a512d49'}, '__init__')
    def __init__(quay_self_3f1f12a, quay_byte_order_a512d49='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_3f1f12a)['_FIELDNAMES'], sizes=_name_boundary.attributes(quay_self_3f1f12a)['_SIZES'], byte_order=quay_byte_order_a512d49)
        _name_boundary.attributes(quay_self_3f1f12a)['magic'] = 0
        _name_boundary.attributes(quay_self_3f1f12a)['length'] = 0

@_name_boundary.class_contract('SuperBlob', {'_FIELDNAMES': 'quay__FIELDNAMES', '_SIZES': 'quay__SIZES', 'SIZE': 'quay_SIZE', 'blob': 'quay_blob', 'count': 'quay_count'})
class quay_SuperBlob(quay_Struct):
    quay__FIELDNAMES = ['blob', 'count']
    quay__SIZES = [quay_Blob, quay_uint32_t]
    quay_SIZE = 12

    @_name_boundary.callable_contract({'self': 'quay_self_8f5b3c2', 'byte_order': 'quay_byte_order_4d34cbb'}, '__init__')
    def __init__(quay_self_8f5b3c2, quay_byte_order_4d34cbb='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_8f5b3c2)['_FIELDNAMES'], sizes=_name_boundary.attributes(quay_self_8f5b3c2)['_SIZES'], byte_order=quay_byte_order_4d34cbb)
        _name_boundary.attributes(quay_self_8f5b3c2)['blob'] = 0
        _name_boundary.attributes(quay_self_8f5b3c2)['count'] = 0
_name_boundary.module_contract(globals(), {'CSSLOT_DERFORMAT': 'quay_CSSLOT_DERFORMAT', 'CSMAGIC_EMBEDDED_SIGNATURE': 'quay_CSMAGIC_EMBEDDED_SIGNATURE', 'CSSLOT_RESOURCEDIR': 'quay_CSSLOT_RESOURCEDIR', 'CSMAGIC_EMBEDDED_ENTITLEMENTS': 'quay_CSMAGIC_EMBEDDED_ENTITLEMENTS', 'CSSLOT_ENTITLEMENTS': 'quay_CSSLOT_ENTITLEMENTS', 'BlobIndex': 'quay_BlobIndex', 'CSMAGIC_REQUIREMENT': 'quay_CSMAGIC_REQUIREMENT', 'CSSLOT_CODEDIRECTORY': 'quay_CSSLOT_CODEDIRECTORY', 'CSMAGIC_EMBEDDED_DERFORMAT': 'quay_CSMAGIC_EMBEDDED_DERFORMAT', 'Blob': 'quay_Blob', 'CSSLOT_REPSPECIFIC': 'quay_CSSLOT_REPSPECIFIC', 'CSSLOT_REQUIREMENTS': 'quay_CSSLOT_REQUIREMENTS', 'CSMAGIC_EMBEDDED_SIGNATURE_OLD': 'quay_CSMAGIC_EMBEDDED_SIGNATURE_OLD', 'CSSLOT_ALTERNATE': 'quay_CSSLOT_ALTERNATE', 'SuperBlob': 'quay_SuperBlob', 'CSSLOT_APPLICATION': 'quay_CSSLOT_APPLICATION', 'uint32_t': 'quay_uint32_t', 'Struct': 'quay_Struct', 'CSMAGIC_REQUIREMENTS': 'quay_CSMAGIC_REQUIREMENTS', 'CSMAGIC_DETACHED_SIGNATURE': 'quay_CSMAGIC_DETACHED_SIGNATURE', 'CSMAGIC_BLOBWRAPPER': 'quay_CSMAGIC_BLOBWRAPPER', 'CSMAGIC_CODEDIRECTORY': 'quay_CSMAGIC_CODEDIRECTORY', 'CSSLOT_INFOSLOT': 'quay_CSSLOT_INFOSLOT'})
