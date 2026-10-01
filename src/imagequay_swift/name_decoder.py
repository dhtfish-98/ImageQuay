# Derived from src/ktool_swift/demangle.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool_swift
#  demangle.py
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

@_name_boundary.callable_contract({'name': 'quay_name_bdbd1d6'}, 'demangle')
def quay_demangle(quay_name_bdbd1d6):
    """
    Very basic, very sloppy bare minimum POC for swift classname demangling

    :param name:
    :return:
    """
    quay_project_15e0c1a = ''
    quay_typename_3b97718 = ''
    quay_stage_4b14df1 = 0
    quay_skip_e83c567 = False
    for quay_c_d5aba07 in quay_name_bdbd1d6:
        if quay_c_d5aba07.isdigit():
            if quay_skip_e83c567:
                continue
            else:
                quay_stage_4b14df1 += 1
                quay_skip_e83c567 = True
                continue
        else:
            quay_skip_e83c567 = False
            if quay_stage_4b14df1 == 0:
                continue
            elif quay_stage_4b14df1 == 1:
                quay_project_15e0c1a += quay_c_d5aba07
            elif quay_stage_4b14df1 == 2:
                quay_typename_3b97718 += quay_c_d5aba07
    return (quay_project_15e0c1a, quay_typename_3b97718)
_name_boundary.module_contract(globals(), {'demangle': 'quay_demangle'})
