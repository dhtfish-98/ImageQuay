# Derived from src/ktool_macho/base.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool_macho
#  base.py
#
#
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary
from abc import ABC as quay_ABC, abstractmethod as quay_abstractmethod

@_name_boundary.class_contract('Constructable', {'from_image': 'quay_from_image', 'from_values': 'quay_from_values', 'raw_bytes': 'quay_raw_bytes'})
class quay_Constructable(quay_ABC):
    """
    This is an attempt to define a standardized API for objects we load and may want to create.

    The idea is that all objects should be loadable and serializable in both directions, to allow patching, creation,
        and standard loading, with hopefully not too much overhead being shared between the three.

    """

    @classmethod
    @quay_abstractmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_3df48de', 'args': 'quay_args_4167ca4', 'kwargs': 'quay_kwargs_5c15bae'}, 'from_image')
    def quay_from_image(quay_cls_3df48de, *quay_args_4167ca4, **quay_kwargs_5c15bae):
        """
        Base method for serializing an instance of the subclass based on raw bytes

        Implementation/Args left up to implementations, but should usually follow `from_bytes(raw: bytes)`

        :return:
        """

    @classmethod
    @quay_abstractmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_dc681b1', 'args': 'quay_args_162e552', 'kwargs': 'quay_kwargs_07cbdd4'}, 'from_values')
    def quay_from_values(quay_cls_dc681b1, *quay_args_162e552, **quay_kwargs_07cbdd4):
        """
        Base method for serializing an instance of the subclass based on the required set of values to create it.

        Implementation and argument structure of this is definitely left up to subclasses.

        :return:
        """

    @quay_abstractmethod
    @_name_boundary.callable_contract({'self': 'quay_self_5d39a08'}, 'raw_bytes')
    def quay_raw_bytes(quay_self_5d39a08):
        """
        Built or stored raw byte representation of this item

        :return:
        """
_name_boundary.module_contract(globals(), {'Constructable': 'quay_Constructable', 'abstractmethod': 'quay_abstractmethod', 'ABC': 'quay_ABC'})
