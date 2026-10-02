# Derived from src/ktool_swift/structs.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool_swift
#  structs.py
#
#  https://knight.sc/reverse%20engineering/2019/07/17/swift-metadata.html
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2022.
#
import imagequay_boundary as _name_boundary
import enum as quay_enum
from imagequay_support.record_engine import *

@_name_boundary.class_contract('ProtocolDescriptor', {'FIELDS': 'quay_FIELDS', 'Flags': 'quay_Flags', 'Parent': 'quay_Parent', 'Name': 'quay_Name', 'NumRequirementsInSignature': 'quay_NumRequirementsInSignature', 'NumRequirements': 'quay_NumRequirements', 'AssociatedTypeNames': 'quay_AssociatedTypeNames'})
class quay_ProtocolDescriptor(quay_Struct):
    quay_FIELDS = {'Flags': quay_uint32_t, 'Parent': quay_int32_t, 'Name': quay_int32_t, 'NumRequirementsInSignature': quay_uint32_t, 'NumRequirements': quay_uint32_t, 'AssociatedTypeNames': quay_int32_t}

@_name_boundary.class_contract('ProtocolConformanceDescriptor', {'FIELDS': 'quay_FIELDS', 'ProtocolDescriptor': 'quay_ProtocolDescriptor', 'NominalTypeDescriptor': 'quay_NominalTypeDescriptor', 'ProtocolWitnessTable': 'quay_ProtocolWitnessTable', 'ConformanceFlags': 'quay_ConformanceFlags'})
class quay_ProtocolConformanceDescriptor(quay_Struct):
    quay_FIELDS = {'ProtocolDescriptor': quay_int32_t, 'NominalTypeDescriptor': quay_int32_t, 'ProtocolWitnessTable': quay_int32_t, 'ConformanceFlags': quay_uint32_t}

@_name_boundary.class_contract('EnumDescriptor', {'FIELDS': 'quay_FIELDS', 'Flags': 'quay_Flags', 'Parent': 'quay_Parent', 'Name': 'quay_Name', 'AccessFunction': 'quay_AccessFunction', 'FieldDescriptor': 'quay_FieldDescriptor', 'NumPayloadCasesAndPayloadSizeOffset': 'quay_NumPayloadCasesAndPayloadSizeOffset', 'NumEmptyCases': 'quay_NumEmptyCases'})
class quay_EnumDescriptor(quay_Struct):
    quay_FIELDS = {'Flags': quay_uint32_t, 'Parent': quay_int32_t, 'Name': quay_int32_t, 'AccessFunction': quay_int32_t, 'FieldDescriptor': quay_int32_t, 'NumPayloadCasesAndPayloadSizeOffset': quay_uint32_t, 'NumEmptyCases': quay_uint32_t}

@_name_boundary.class_contract('StructDescriptor', {'FIELDS': 'quay_FIELDS', 'Flags': 'quay_Flags', 'Parent': 'quay_Parent', 'Name': 'quay_Name', 'AccessFunction': 'quay_AccessFunction', 'FieldDescriptor': 'quay_FieldDescriptor', 'NumFields': 'quay_NumFields', 'FieldOffsetVectorOffset': 'quay_FieldOffsetVectorOffset'})
class quay_StructDescriptor(quay_Struct):
    quay_FIELDS = {'Flags': quay_uint32_t, 'Parent': quay_int32_t, 'Name': quay_int32_t, 'AccessFunction': quay_int32_t, 'FieldDescriptor': quay_int32_t, 'NumFields': quay_uint32_t, 'FieldOffsetVectorOffset': quay_uint32_t}

@_name_boundary.class_contract('ClassDescriptor', {'FIELDS': 'quay_FIELDS', 'Flags': 'quay_Flags', 'Parent': 'quay_Parent', 'Name': 'quay_Name', 'AccessFunction': 'quay_AccessFunction', 'FieldDescriptor': 'quay_FieldDescriptor', 'SuperclassType': 'quay_SuperclassType', 'MetadataNegativeSizeInWords': 'quay_MetadataNegativeSizeInWords', 'MetadataPositiveSizeInWords': 'quay_MetadataPositiveSizeInWords', 'NumImmediateMembers': 'quay_NumImmediateMembers', 'NumFields': 'quay_NumFields', 'FieldOffsetVectorOffset': 'quay_FieldOffsetVectorOffset'})
class quay_ClassDescriptor(quay_Struct):
    quay_FIELDS = {'Flags': quay_uint32_t, 'Parent': quay_int32_t, 'Name': quay_int32_t, 'AccessFunction': quay_int32_t, 'FieldDescriptor': quay_int32_t, 'SuperclassType': quay_int32_t, 'MetadataNegativeSizeInWords': quay_uint32_t, 'MetadataPositiveSizeInWords': quay_uint32_t, 'NumImmediateMembers': quay_uint32_t, 'NumFields': quay_uint32_t, 'FieldOffsetVectorOffset': quay_uint32_t}

@_name_boundary.class_contract('FieldDescriptor', {'FIELDS': 'quay_FIELDS', 'MangledTypeName': 'quay_MangledTypeName', 'Superclass': 'quay_Superclass', 'Kind': 'quay_Kind', 'FieldRecordSize': 'quay_FieldRecordSize', 'NumFields': 'quay_NumFields'})
class quay_FieldDescriptor(quay_Struct):
    quay_FIELDS = {'MangledTypeName': quay_int32_t, 'Superclass': quay_int32_t, 'Kind': quay_uint16_t, 'FieldRecordSize': quay_uint16_t, 'NumFields': quay_uint32_t}

@_name_boundary.class_contract('FieldRecord', {'FIELDS': 'quay_FIELDS', 'Flags': 'quay_Flags', 'MangledTypeName': 'quay_MangledTypeName', 'FieldName': 'quay_FieldName'})
class quay_FieldRecord(quay_Struct):
    quay_FIELDS = {'Flags': quay_uint32_t, 'MangledTypeName': quay_int32_t, 'FieldName': quay_int32_t}

@_name_boundary.class_contract('AssociatedTypeRecord', {'FIELDS': 'quay_FIELDS', 'Name': 'quay_Name', 'SubstitutedTypename': 'quay_SubstitutedTypename'})
class quay_AssociatedTypeRecord(quay_Struct):
    quay_FIELDS = {'Name': quay_int32_t, 'SubstitutedTypename': quay_int32_t}

@_name_boundary.class_contract('AssociatedTypeDescriptor', {'FIELDS': 'quay_FIELDS', 'ConformingTypeName': 'quay_ConformingTypeName', 'ProtocolTypeName': 'quay_ProtocolTypeName', 'NumAssociatedTypes': 'quay_NumAssociatedTypes', 'AssociatedTypeRecordSize': 'quay_AssociatedTypeRecordSize'})
class quay_AssociatedTypeDescriptor(quay_Struct):
    quay_FIELDS = {'ConformingTypeName': quay_int32_t, 'ProtocolTypeName': quay_int32_t, 'NumAssociatedTypes': quay_uint32_t, 'AssociatedTypeRecordSize': quay_uint32_t}

@_name_boundary.class_contract('BuiltinTypeDescriptor', {'FIELDS': 'quay_FIELDS', 'TypeName': 'quay_TypeName', 'Size': 'quay_Size', 'AlignmentAndFlags': 'quay_AlignmentAndFlags', 'Stride': 'quay_Stride', 'NumExtraInhabitants': 'quay_NumExtraInhabitants'})
class quay_BuiltinTypeDescriptor(quay_Struct):
    quay_FIELDS = {'TypeName': quay_int32_t, 'Size': quay_uint32_t, 'AlignmentAndFlags': quay_uint32_t, 'Stride': quay_uint32_t, 'NumExtraInhabitants': quay_uint32_t}

@_name_boundary.class_contract('CaptureTypeRecord', {'FIELDS': 'quay_FIELDS', 'MangledTypeName': 'quay_MangledTypeName'})
class quay_CaptureTypeRecord(quay_Struct):
    quay_FIELDS = {'MangledTypeName': quay_int32_t}

@_name_boundary.class_contract('MetadataSourceRecord', {'FIELDS': 'quay_FIELDS', 'MangledTypeName': 'quay_MangledTypeName', 'MangledMetadataSource': 'quay_MangledMetadataSource'})
class quay_MetadataSourceRecord(quay_Struct):
    quay_FIELDS = {'MangledTypeName': quay_int32_t, 'MangledMetadataSource': quay_int32_t}

@_name_boundary.class_contract('CaptureDescriptor', {'FIELDS': 'quay_FIELDS', 'NumCaptureTypes': 'quay_NumCaptureTypes', 'NumMetadataSources': 'quay_NumMetadataSources', 'NumBindings': 'quay_NumBindings'})
class quay_CaptureDescriptor(quay_Struct):
    quay_FIELDS = {'NumCaptureTypes': quay_uint32_t, 'NumMetadataSources': quay_uint32_t, 'NumBindings': quay_uint32_t}

@_name_boundary.class_contract('Replacement', {'FIELDS': 'quay_FIELDS', 'ReplacedFunctionKey': 'quay_ReplacedFunctionKey', 'NewFunction': 'quay_NewFunction', 'Replacement': 'quay_Replacement', 'Flags': 'quay_Flags'})
class quay_Replacement(quay_Struct):
    quay_FIELDS = {'ReplacedFunctionKey': quay_int32_t, 'NewFunction': quay_int32_t, 'Replacement': quay_int32_t, 'Flags': quay_uint32_t}

@_name_boundary.class_contract('ReplacementScope', {'FIELDS': 'quay_FIELDS', 'Flags': 'quay_Flags', 'NumReplacements': 'quay_NumReplacements'})
class quay_ReplacementScope(quay_Struct):
    quay_FIELDS = {'Flags': quay_uint32_t, 'NumReplacements': quay_uint32_t}

@_name_boundary.class_contract('AutomaticReplacements', {'FIELDS': 'quay_FIELDS', 'Flags': 'quay_Flags', 'NumReplacements': 'quay_NumReplacements', 'Replacements': 'quay_Replacements'})
class quay_AutomaticReplacements(quay_Struct):
    quay_FIELDS = {'Flags': quay_uint32_t, 'NumReplacements': quay_uint32_t, 'Replacements': quay_int32_t}

@_name_boundary.class_contract('OpaqueReplacement', {'FIELDS': 'quay_FIELDS', 'Original': 'quay_Original', 'Replacement': 'quay_Replacement'})
class quay_OpaqueReplacement(quay_Struct):
    quay_FIELDS = {'Original': quay_int32_t, 'Replacement': quay_int32_t}

@_name_boundary.class_contract('OpaqueAutomaticReplacement', {'FIELDS': 'quay_FIELDS', 'Flags': 'quay_Flags', 'NumReplacements': 'quay_NumReplacements'})
class quay_OpaqueAutomaticReplacement(quay_Struct):
    quay_FIELDS = {'Flags': quay_uint32_t, 'NumReplacements': quay_uint32_t}

@_name_boundary.class_contract('ClassMethodListTable', {'FIELDS': 'quay_FIELDS', 'VTableOffset': 'quay_VTableOffset', 'VTableSize': 'quay_VTableSize'})
class quay_ClassMethodListTable(quay_Struct):
    quay_FIELDS = {'VTableOffset': quay_uint32_t, 'VTableSize': quay_uint32_t}

@_name_boundary.class_contract('TargetMethodDescriptor', {'FIELDS': 'quay_FIELDS', 'Flags': 'quay_Flags', 'Impl': 'quay_Impl'})
class quay_TargetMethodDescriptor(quay_Struct):
    quay_FIELDS = {'Flags': quay_uint32_t, 'Impl': quay_int32_t}

@_name_boundary.class_contract('ContextDescriptorKind', {})
class quay_ContextDescriptorKind(quay_enum.Enum):
    Module = 0
    Extension = 1
    Anonymous = 2
    SwiftProtocol = 3
    OpaqueType = 4
    Class = 16
    Struct = 17
    Enum = 18
    Type_Last = 31
_name_boundary.module_contract(globals(), {'AssociatedTypeRecord': 'quay_AssociatedTypeRecord', 'TargetMethodDescriptor': 'quay_TargetMethodDescriptor', 'ClassMethodListTable': 'quay_ClassMethodListTable', 'BuiltinTypeDescriptor': 'quay_BuiltinTypeDescriptor', 'CaptureTypeRecord': 'quay_CaptureTypeRecord', 'EnumDescriptor': 'quay_EnumDescriptor', 'Replacement': 'quay_Replacement', 'ClassDescriptor': 'quay_ClassDescriptor', 'FieldRecord': 'quay_FieldRecord', 'FieldDescriptor': 'quay_FieldDescriptor', 'OpaqueAutomaticReplacement': 'quay_OpaqueAutomaticReplacement', 'ContextDescriptorKind': 'quay_ContextDescriptorKind', 'AssociatedTypeDescriptor': 'quay_AssociatedTypeDescriptor', 'MetadataSourceRecord': 'quay_MetadataSourceRecord', 'ProtocolConformanceDescriptor': 'quay_ProtocolConformanceDescriptor', 'AutomaticReplacements': 'quay_AutomaticReplacements', 'ReplacementScope': 'quay_ReplacementScope', 'ProtocolDescriptor': 'quay_ProtocolDescriptor', 'CaptureDescriptor': 'quay_CaptureDescriptor', 'StructDescriptor': 'quay_StructDescriptor', 'enum': 'quay_enum', 'OpaqueReplacement': 'quay_OpaqueReplacement'})
