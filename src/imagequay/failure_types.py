# Derived from src/ktool/exceptions.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  exceptions.py
#
#  Custom Exceptions for internal (and occasionally external) usage
#
#  This does not include the exceptions used in the interrupt model in the GUI.
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary

@_name_boundary.class_contract('MalformedMachOException', {})
class quay_MalformedMachOException(Exception):
    """
    """

@_name_boundary.class_contract('MachOAlignmentError', {})
class quay_MachOAlignmentError(Exception):
    """
    """

@_name_boundary.class_contract('VMAddressingError', {})
class quay_VMAddressingError(ValueError):
    """
    """

@_name_boundary.class_contract('UnsupportedFiletypeException', {})
class quay_UnsupportedFiletypeException(Exception):
    """
    """

@_name_boundary.class_contract('NoObjCMetadataException', {})
class quay_NoObjCMetadataException(Exception):
    """
    """
_name_boundary.module_contract(globals(), {'MalformedMachOException': 'quay_MalformedMachOException', 'VMAddressingError': 'quay_VMAddressingError', 'MachOAlignmentError': 'quay_MachOAlignmentError', 'NoObjCMetadataException': 'quay_NoObjCMetadataException', 'UnsupportedFiletypeException': 'quay_UnsupportedFiletypeException'})
