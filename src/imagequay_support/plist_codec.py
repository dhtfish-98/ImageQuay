# Derived from src/lib0cyn/kplistlib.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  kplistlib.py
#
#  Modified stdlib package 'plistlib' to fix some crashes.
#
#  This uses the 3.7 version (since the new API is busted) and
#       modifies the integer reading stuff to properly support empty values and hex strings.
#
"""plistlib.py -- a tool to generate and parse MacOSX .plist files.
The property list (.plist) file format is a simple XML pickle supporting
basic object types, like dictionaries, lists, numbers and strings.
Usually the top level object is a dictionary.
To write out a plist file, use the dump(value, file)
function. 'value' is the top level object, 'file' is
a (writable) file object.
To parse a plist from a file, use the load(file) function,
with a (readable) file object as the only argument. It
returns the top level object (again, usually a dictionary).
To work with plist data in bytes objects, you can use loads()
and dumps().
Values can be strings, integers, floats, booleans, tuples, lists,
dictionaries (but only with string keys), Data, bytes, bytearray, or
datetime.datetime objects.
Generate Plist example:
    pl = dict(
        aString = "Doodah",
        aList = ["A", "B", 12, 32.1, [1, 2, 3]],
        aFloat = 0.1,
        anInt = 728,
        aDict = dict(
            anotherString = "<hello & hi there!>",
            aUnicodeValue = "M\\xe4ssig, Ma\\xdf",
            aTrueValue = True,
            aFalseValue = False,
        ),
        someData = b"<binary gunk>",
        someMoreData = b"<lots of binary gunk>" * 10,
        aDate = datetime.datetime.fromtimestamp(time.mktime(time.gmtime())),
    )
    with open(fileName, 'wb') as fp:
        dump(pl, fp)
Parse Plist example:
    with open(fileName, 'rb') as fp:
        pl = load(fp)
    print(pl["aKey"])
"""
import imagequay_boundary as _name_boundary
__all__ = ['InvalidFileException', 'FMT_XML', 'FMT_BINARY', 'load', 'dump', 'loads', 'dumps', 'UID']
'plistlib.py -- a tool to generate and parse MacOSX .plist files.\nThe property list (.plist) file format is a simple XML pickle supporting\nbasic object types, like dictionaries, lists, numbers and strings.\nUsually the top level object is a dictionary.\nTo write out a plist file, use the dump(value, file)\nfunction. \'value\' is the top level object, \'file\' is\na (writable) file object.\nTo parse a plist from a file, use the load(file) function,\nwith a (readable) file object as the only argument. It\nreturns the top level object (again, usually a dictionary).\nTo work with plist data in bytes objects, you can use loads()\nand dumps().\nValues can be strings, integers, floats, booleans, tuples, lists,\ndictionaries (but only with string keys), Data, bytes, bytearray, or\ndatetime.datetime objects.\nGenerate Plist example:\n    pl = dict(\n        aString = "Doodah",\n        aList = ["A", "B", 12, 32.1, [1, 2, 3]],\n        aFloat = 0.1,\n        anInt = 728,\n        aDict = dict(\n            anotherString = "<hello & hi there!>",\n            aUnicodeValue = "M\\xe4ssig, Ma\\xdf",\n            aTrueValue = True,\n            aFalseValue = False,\n        ),\n        someData = b"<binary gunk>",\n        someMoreData = b"<lots of binary gunk>" * 10,\n        aDate = datetime.datetime.fromtimestamp(time.mktime(time.gmtime())),\n    )\n    with open(fileName, \'wb\') as fp:\n        dump(pl, fp)\nParse Plist example:\n    with open(fileName, \'rb\') as fp:\n        pl = load(fp)\n    print(pl["aKey"])\n'
__all__ = ['readPlist', 'writePlist', 'readPlistFromBytes', 'writePlistToBytes', 'Data', 'InvalidFileException', 'FMT_XML', 'FMT_BINARY', 'load', 'dump', 'loads', 'dumps']
import binascii as quay_binascii
import codecs as quay_codecs
import contextlib as quay_contextlib
import datetime as quay_datetime
import enum as quay_enum
from io import BytesIO as quay_BytesIO
import itertools as quay_itertools
import os as quay_os
import re as quay_re
import struct as quay_struct
from warnings import warn as quay_warn
from xml.parsers.expat import ParserCreate as quay_ParserCreate
quay_PlistFormat = quay_enum.Enum('PlistFormat', 'FMT_XML FMT_BINARY', module=__name__)
globals().update(quay_PlistFormat.__members__)

@quay_contextlib.contextmanager
@_name_boundary.callable_contract({'pathOrFile': 'quay_pathOrFile_9c0b050', 'mode': 'quay_mode_9c03543'}, '_maybe_open')
def quay__maybe_open(quay_pathOrFile_9c0b050, quay_mode_9c03543):
    if isinstance(quay_pathOrFile_9c0b050, str):
        with open(quay_pathOrFile_9c0b050, quay_mode_9c03543) as quay_fp_f08ddc3:
            yield quay_fp_f08ddc3
    else:
        yield quay_pathOrFile_9c0b050

@_name_boundary.callable_contract({'pathOrFile': 'quay_pathOrFile_576b052'}, 'readPlist')
def quay_readPlist(quay_pathOrFile_576b052):
    """
    Read a .plist from a path or file. pathOrFile should either
    be a file name, or a readable binary file object.
    This function is deprecated, use load instead.
    """
    with quay__maybe_open(quay_pathOrFile_576b052, 'rb') as quay_fp_2a85033:
        return quay_load(quay_fp_2a85033, fmt=None, use_builtin_types=False)

@_name_boundary.callable_contract({'value': 'quay_value_50221ba', 'pathOrFile': 'quay_pathOrFile_10389f6'}, 'writePlist')
def quay_writePlist(quay_value_50221ba, quay_pathOrFile_10389f6):
    """
    Write 'value' to a .plist file. 'pathOrFile' may either be a
    file name or a (writable) file object.
    This function is deprecated, use dump instead.
    """
    with quay__maybe_open(quay_pathOrFile_10389f6, 'wb') as quay_fp_4447088:
        quay_dump(quay_value_50221ba, quay_fp_4447088, fmt=FMT_XML, sort_keys=True, skipkeys=False)

@_name_boundary.callable_contract({'data': 'quay_data_87d5321'}, 'readPlistFromBytes')
def quay_readPlistFromBytes(quay_data_87d5321):
    """
    Read a plist data from a bytes object. Return the root object.
    This function is deprecated, use loads instead.
    """
    return quay_load(quay_BytesIO(quay_data_87d5321), fmt=None, use_builtin_types=False)

@_name_boundary.callable_contract({'value': 'quay_value_8f8b924'}, 'writePlistToBytes')
def quay_writePlistToBytes(quay_value_8f8b924):
    """
    Return 'value' as a plist-formatted bytes object.
    This function is deprecated, use dumps instead.
    """
    quay_f_af13be4 = quay_BytesIO()
    quay_dump(quay_value_8f8b924, quay_f_af13be4, fmt=FMT_XML, sort_keys=True, skipkeys=False)
    return quay_f_af13be4.getvalue()

@_name_boundary.class_contract('Data', {'fromBase64': 'quay_fromBase64', 'asBase64': 'quay_asBase64', 'data': 'quay_data'})
class quay_Data:
    """
    Wrapper for binary data.
    This class is deprecated, use a bytes object instead.
    """

    @_name_boundary.callable_contract({'self': 'quay_self_3eb8bfd', 'data': 'quay_data_0ff1357'}, '__init__')
    def __init__(quay_self_3eb8bfd, quay_data_0ff1357):
        if not isinstance(quay_data_0ff1357, bytes):
            raise TypeError('data must be as bytes')
        _name_boundary.attributes(quay_self_3eb8bfd)['data'] = quay_data_0ff1357

    @classmethod
    @_name_boundary.callable_contract({'cls': 'quay_cls_ed82081', 'data': 'quay_data_a3189e5'}, 'fromBase64')
    def quay_fromBase64(quay_cls_ed82081, quay_data_a3189e5):
        return quay_cls_ed82081(quay__decode_base64(quay_data_a3189e5))

    @_name_boundary.callable_contract({'self': 'quay_self_5828b5b', 'maxlinelength': 'quay_maxlinelength_db9ce8a'}, 'asBase64')
    def quay_asBase64(quay_self_5828b5b, quay_maxlinelength_db9ce8a=76):
        return quay__encode_base64(_name_boundary.attributes(quay_self_5828b5b)['data'], quay_maxlinelength_db9ce8a)

    @_name_boundary.callable_contract({'self': 'quay_self_c125a30', 'other': 'quay_other_0c58276'}, '__eq__')
    def __eq__(quay_self_c125a30, quay_other_0c58276):
        if isinstance(quay_other_0c58276, quay_self_c125a30.__class__):
            return _name_boundary.attributes(quay_self_c125a30)['data'] == _name_boundary.attributes(quay_other_0c58276)['data']
        elif isinstance(quay_other_0c58276, bytes):
            return _name_boundary.attributes(quay_self_c125a30)['data'] == quay_other_0c58276
        else:
            return NotImplemented

    @_name_boundary.callable_contract({'self': 'quay_self_62c27c8'}, '__repr__')
    def __repr__(quay_self_62c27c8):
        return '%s(%s)' % (_name_boundary.attributes(quay_self_62c27c8.__class__)['__name__'], repr(_name_boundary.attributes(quay_self_62c27c8)['data']))
quay_PLISTHEADER = b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
quay__controlCharPat = quay_re.compile('[\\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\x0b\\x0c\\x0e\\x0f\\x10\\x11\\x12\\x13\\x14\\x15\\x16\\x17\\x18\\x19\\x1a\\x1b\\x1c\\x1d\\x1e\\x1f]')

@_name_boundary.callable_contract({'s': 'quay_s_87428eb', 'maxlinelength': 'quay_maxlinelength_fe4f7df'}, '_encode_base64')
def quay__encode_base64(quay_s_87428eb, quay_maxlinelength_fe4f7df=76):
    quay_maxbinsize_65898c7 = quay_maxlinelength_fe4f7df // 4 * 3
    quay_pieces_aefa338 = []
    for quay_i_b991dfe in range(0, len(quay_s_87428eb), quay_maxbinsize_65898c7):
        quay_chunk_be9869d = quay_s_87428eb[quay_i_b991dfe:quay_i_b991dfe + quay_maxbinsize_65898c7]
        quay_pieces_aefa338.append(quay_binascii.b2a_base64(quay_chunk_be9869d))
    return b''.join(quay_pieces_aefa338)

@_name_boundary.callable_contract({'s': 'quay_s_1cd86f5'}, '_decode_base64')
def quay__decode_base64(quay_s_1cd86f5):
    if isinstance(quay_s_1cd86f5, str):
        return quay_binascii.a2b_base64(quay_s_1cd86f5.encode('utf-8'))
    else:
        return quay_binascii.a2b_base64(quay_s_1cd86f5)
quay__dateParser = quay_re.compile('(?P<year>\\d\\d\\d\\d)(?:-(?P<month>\\d\\d)(?:-(?P<day>\\d\\d)(?:T(?P<hour>\\d\\d)(?::(?P<minute>\\d\\d)(?::(?P<second>\\d\\d))?)?)?)?)?Z', quay_re.ASCII)

@_name_boundary.callable_contract({'s': 'quay_s_c40337a'}, '_date_from_string')
def quay__date_from_string(quay_s_c40337a):
    quay_order_c199e2d = ('year', 'month', 'day', 'hour', 'minute', 'second')
    quay_gd_6e5b498 = quay__dateParser.match(quay_s_c40337a).groupdict()
    quay_lst_f808a50 = []
    for quay_key_22fae34 in quay_order_c199e2d:
        quay_val_9105225 = quay_gd_6e5b498[quay_key_22fae34]
        if quay_val_9105225 is None:
            break
        quay_lst_f808a50.append(int(quay_val_9105225))
    return quay_datetime.datetime(*quay_lst_f808a50)

@_name_boundary.callable_contract({'d': 'quay_d_60bdc4a'}, '_date_to_string')
def quay__date_to_string(quay_d_60bdc4a):
    return '%04d-%02d-%02dT%02d:%02d:%02dZ' % (quay_d_60bdc4a.year, quay_d_60bdc4a.month, quay_d_60bdc4a.day, quay_d_60bdc4a.hour, quay_d_60bdc4a.minute, quay_d_60bdc4a.second)

@_name_boundary.callable_contract({'text': 'quay_text_f60c033'}, '_escape')
def quay__escape(quay_text_f60c033):
    quay_m_98bfded = quay__controlCharPat.search(quay_text_f60c033)
    if quay_m_98bfded is not None:
        raise ValueError("strings can't contains control characters; use bytes instead")
    quay_text_f60c033 = quay_text_f60c033.replace('\r\n', '\n')
    quay_text_f60c033 = quay_text_f60c033.replace('\r', '\n')
    quay_text_f60c033 = quay_text_f60c033.replace('&', '&amp;')
    quay_text_f60c033 = quay_text_f60c033.replace('<', '&lt;')
    quay_text_f60c033 = quay_text_f60c033.replace('>', '&gt;')
    return quay_text_f60c033

@_name_boundary.class_contract('_PlistParser', {'parse': 'quay_parse', 'handle_entity_decl': 'quay_handle_entity_decl', 'handle_begin_element': 'quay_handle_begin_element', 'handle_end_element': 'quay_handle_end_element', 'handle_data': 'quay_handle_data', 'add_object': 'quay_add_object', 'get_data': 'quay_get_data', 'stack': 'quay_stack', 'current_key': 'quay_current_key', 'root': 'quay_root', '_use_builtin_types': 'quay__use_builtin_types', '_dict_type': 'quay__dict_type', 'parser': 'quay_parser', 'data': 'quay_data'})
class quay__PlistParser:

    @_name_boundary.callable_contract({'self': 'quay_self_30c0504', 'use_builtin_types': 'quay_use_builtin_types_71736c5', 'dict_type': 'quay_dict_type_d28f928'}, '__init__')
    def __init__(quay_self_30c0504, quay_use_builtin_types_71736c5, quay_dict_type_d28f928):
        _name_boundary.attributes(quay_self_30c0504)['stack'] = []
        _name_boundary.attributes(quay_self_30c0504)['current_key'] = None
        _name_boundary.attributes(quay_self_30c0504)['root'] = None
        _name_boundary.attributes(quay_self_30c0504)['_use_builtin_types'] = quay_use_builtin_types_71736c5
        _name_boundary.attributes(quay_self_30c0504)['_dict_type'] = quay_dict_type_d28f928

    @_name_boundary.callable_contract({'self': 'quay_self_60e8ac4', 'fileobj': 'quay_fileobj_1f1e79b'}, 'parse')
    def quay_parse(quay_self_60e8ac4, quay_fileobj_1f1e79b):
        _name_boundary.attributes(quay_self_60e8ac4)['parser'] = quay_ParserCreate()
        _name_boundary.attributes(quay_self_60e8ac4)['parser'].StartElementHandler = _name_boundary.attributes(quay_self_60e8ac4)['handle_begin_element']
        _name_boundary.attributes(quay_self_60e8ac4)['parser'].EndElementHandler = _name_boundary.attributes(quay_self_60e8ac4)['handle_end_element']
        _name_boundary.attributes(quay_self_60e8ac4)['parser'].CharacterDataHandler = _name_boundary.attributes(quay_self_60e8ac4)['handle_data']
        _name_boundary.attributes(quay_self_60e8ac4)['parser'].EntityDeclHandler = _name_boundary.attributes(quay_self_60e8ac4)['handle_entity_decl']
        _name_boundary.attributes(quay_self_60e8ac4)['parser'].ParseFile(quay_fileobj_1f1e79b)
        return _name_boundary.attributes(quay_self_60e8ac4)['root']

    @_name_boundary.callable_contract({'self': 'quay_self_91e97b6', 'entity_name': 'quay_entity_name_f4e94bb', 'is_parameter_entity': 'quay_is_parameter_entity_9bc3ffc', 'value': 'quay_value_78912c7', 'base': 'quay_base_3687144', 'system_id': 'quay_system_id_aa2897d', 'public_id': 'quay_public_id_c2f769f', 'notation_name': 'quay_notation_name_6338def'}, 'handle_entity_decl')
    def quay_handle_entity_decl(quay_self_91e97b6, quay_entity_name_f4e94bb, quay_is_parameter_entity_9bc3ffc, quay_value_78912c7, quay_base_3687144, quay_system_id_aa2897d, quay_public_id_c2f769f, quay_notation_name_6338def):
        raise quay_InvalidFileException('XML entity declarations are not supported in plist files')

    @_name_boundary.callable_contract({'self': 'quay_self_6008112', 'element': 'quay_element_f7a9b9c', 'attrs': 'quay_attrs_173b8b4'}, 'handle_begin_element')
    def quay_handle_begin_element(quay_self_6008112, quay_element_f7a9b9c, quay_attrs_173b8b4):
        _name_boundary.attributes(quay_self_6008112)['data'] = []
        quay_handler_f1e2f9d = _name_boundary.read_attribute(quay_self_6008112, 'begin_' + quay_element_f7a9b9c, None)
        if quay_handler_f1e2f9d is not None:
            quay_handler_f1e2f9d(quay_attrs_173b8b4)

    @_name_boundary.callable_contract({'self': 'quay_self_e02bfd8', 'element': 'quay_element_9a5443f'}, 'handle_end_element')
    def quay_handle_end_element(quay_self_e02bfd8, quay_element_9a5443f):
        quay_handler_4163f8c = _name_boundary.read_attribute(quay_self_e02bfd8, 'end_' + quay_element_9a5443f, None)
        if quay_handler_4163f8c is not None:
            quay_handler_4163f8c()

    @_name_boundary.callable_contract({'self': 'quay_self_64e5ed6', 'data': 'quay_data_07660e8'}, 'handle_data')
    def quay_handle_data(quay_self_64e5ed6, quay_data_07660e8):
        _name_boundary.attributes(quay_self_64e5ed6)['data'].append(quay_data_07660e8)

    @_name_boundary.callable_contract({'self': 'quay_self_84d8aa0', 'value': 'quay_value_13d79f0'}, 'add_object')
    def quay_add_object(quay_self_84d8aa0, quay_value_13d79f0):
        if _name_boundary.attributes(quay_self_84d8aa0)['current_key'] is not None:
            if not isinstance(_name_boundary.attributes(quay_self_84d8aa0)['stack'][-1], type({})):
                raise ValueError('unexpected element at line %d' % _name_boundary.attributes(quay_self_84d8aa0)['parser'].CurrentLineNumber)
            _name_boundary.attributes(quay_self_84d8aa0)['stack'][-1][_name_boundary.attributes(quay_self_84d8aa0)['current_key']] = quay_value_13d79f0
            _name_boundary.attributes(quay_self_84d8aa0)['current_key'] = None
        elif not _name_boundary.attributes(quay_self_84d8aa0)['stack']:
            _name_boundary.attributes(quay_self_84d8aa0)['root'] = quay_value_13d79f0
        else:
            if not isinstance(_name_boundary.attributes(quay_self_84d8aa0)['stack'][-1], type([])):
                raise ValueError('unexpected element at line %d' % _name_boundary.attributes(quay_self_84d8aa0)['parser'].CurrentLineNumber)
            _name_boundary.attributes(quay_self_84d8aa0)['stack'][-1].append(quay_value_13d79f0)

    @_name_boundary.callable_contract({'self': 'quay_self_c47b860'}, 'get_data')
    def quay_get_data(quay_self_c47b860):
        quay_data_d8cbe57 = ''.join(_name_boundary.attributes(quay_self_c47b860)['data'])
        _name_boundary.attributes(quay_self_c47b860)['data'] = []
        return quay_data_d8cbe57

    @_name_boundary.callable_contract({'self': 'quay_self_eeb4b71', 'attrs': 'quay_attrs_72d89d2'}, 'begin_dict')
    def begin_dict(quay_self_eeb4b71, quay_attrs_72d89d2):
        quay_d_64293b9 = _name_boundary.attributes(quay_self_eeb4b71)['_dict_type']()
        _name_boundary.attributes(quay_self_eeb4b71)['add_object'](quay_d_64293b9)
        _name_boundary.attributes(quay_self_eeb4b71)['stack'].append(quay_d_64293b9)

    @_name_boundary.callable_contract({'self': 'quay_self_856690a'}, 'end_dict')
    def end_dict(quay_self_856690a):
        if _name_boundary.attributes(quay_self_856690a)['current_key']:
            raise ValueError("missing value for key '%s' at line %d" % (_name_boundary.attributes(quay_self_856690a)['current_key'], _name_boundary.attributes(quay_self_856690a)['parser'].CurrentLineNumber))
        _name_boundary.attributes(quay_self_856690a)['stack'].pop()

    @_name_boundary.callable_contract({'self': 'quay_self_ce0790a'}, 'end_key')
    def end_key(quay_self_ce0790a):
        if _name_boundary.attributes(quay_self_ce0790a)['current_key'] or not isinstance(_name_boundary.attributes(quay_self_ce0790a)['stack'][-1], type({})):
            raise ValueError('unexpected key at line %d' % _name_boundary.attributes(quay_self_ce0790a)['parser'].CurrentLineNumber)
        _name_boundary.attributes(quay_self_ce0790a)['current_key'] = _name_boundary.attributes(quay_self_ce0790a)['get_data']()

    @_name_boundary.callable_contract({'self': 'quay_self_eaf8905', 'attrs': 'quay_attrs_40d1124'}, 'begin_array')
    def begin_array(quay_self_eaf8905, quay_attrs_40d1124):
        quay_a_2f46d81 = []
        _name_boundary.attributes(quay_self_eaf8905)['add_object'](quay_a_2f46d81)
        _name_boundary.attributes(quay_self_eaf8905)['stack'].append(quay_a_2f46d81)

    @_name_boundary.callable_contract({'self': 'quay_self_3371603'}, 'end_array')
    def end_array(quay_self_3371603):
        _name_boundary.attributes(quay_self_3371603)['stack'].pop()

    @_name_boundary.callable_contract({'self': 'quay_self_aa8831f'}, 'end_true')
    def end_true(quay_self_aa8831f):
        _name_boundary.attributes(quay_self_aa8831f)['add_object'](True)

    @_name_boundary.callable_contract({'self': 'quay_self_ac66bb3'}, 'end_false')
    def end_false(quay_self_ac66bb3):
        _name_boundary.attributes(quay_self_ac66bb3)['add_object'](False)

    @_name_boundary.callable_contract({'self': 'quay_self_b35c2a5'}, 'end_integer')
    def end_integer(quay_self_b35c2a5):
        quay_val_d389b0b = _name_boundary.attributes(quay_self_b35c2a5)['get_data']()
        if quay_val_d389b0b == '':
            _name_boundary.attributes(quay_self_b35c2a5)['add_object'](0)
        elif quay_val_d389b0b.lower().startswith('0x'):
            _name_boundary.attributes(quay_self_b35c2a5)['add_object'](int(quay_val_d389b0b.lower(), 16))
        else:
            _name_boundary.attributes(quay_self_b35c2a5)['add_object'](int(quay_val_d389b0b))

    @_name_boundary.callable_contract({'self': 'quay_self_7081a15'}, 'end_real')
    def end_real(quay_self_7081a15):
        _name_boundary.attributes(quay_self_7081a15)['add_object'](float(_name_boundary.attributes(quay_self_7081a15)['get_data']()))

    @_name_boundary.callable_contract({'self': 'quay_self_9436a0f'}, 'end_string')
    def end_string(quay_self_9436a0f):
        _name_boundary.attributes(quay_self_9436a0f)['add_object'](_name_boundary.attributes(quay_self_9436a0f)['get_data']())

    @_name_boundary.callable_contract({'self': 'quay_self_da04c19'}, 'end_data')
    def end_data(quay_self_da04c19):
        if _name_boundary.attributes(quay_self_da04c19)['_use_builtin_types']:
            _name_boundary.attributes(quay_self_da04c19)['add_object'](quay__decode_base64(_name_boundary.attributes(quay_self_da04c19)['get_data']()))
        else:
            _name_boundary.attributes(quay_self_da04c19)['add_object'](_name_boundary.attributes(quay_Data)['fromBase64'](_name_boundary.attributes(quay_self_da04c19)['get_data']()))

    @_name_boundary.callable_contract({'self': 'quay_self_66cdf8b'}, 'end_date')
    def end_date(quay_self_66cdf8b):
        _name_boundary.attributes(quay_self_66cdf8b)['add_object'](quay__date_from_string(_name_boundary.attributes(quay_self_66cdf8b)['get_data']()))

@_name_boundary.class_contract('_DumbXMLWriter', {'begin_element': 'quay_begin_element', 'end_element': 'quay_end_element', 'simple_element': 'quay_simple_element', 'writeln': 'quay_writeln', 'file': 'quay_file', 'stack': 'quay_stack', '_indent_level': 'quay__indent_level', 'indent': 'quay_indent'})
class quay__DumbXMLWriter:

    @_name_boundary.callable_contract({'self': 'quay_self_ca9ec32', 'file': 'quay_file_55b0bf7', 'indent_level': 'quay_indent_level_84636cf', 'indent': 'quay_indent_09018e7'}, '__init__')
    def __init__(quay_self_ca9ec32, quay_file_55b0bf7, quay_indent_level_84636cf=0, quay_indent_09018e7='\t'):
        _name_boundary.attributes(quay_self_ca9ec32)['file'] = quay_file_55b0bf7
        _name_boundary.attributes(quay_self_ca9ec32)['stack'] = []
        _name_boundary.attributes(quay_self_ca9ec32)['_indent_level'] = quay_indent_level_84636cf
        _name_boundary.attributes(quay_self_ca9ec32)['indent'] = quay_indent_09018e7

    @_name_boundary.callable_contract({'self': 'quay_self_1980061', 'element': 'quay_element_46a9241'}, 'begin_element')
    def quay_begin_element(quay_self_1980061, quay_element_46a9241):
        _name_boundary.attributes(quay_self_1980061)['stack'].append(quay_element_46a9241)
        _name_boundary.attributes(quay_self_1980061)['writeln']('<%s>' % quay_element_46a9241)
        _name_boundary.attributes(quay_self_1980061)['_indent_level'] += 1

    @_name_boundary.callable_contract({'self': 'quay_self_5ed2fb4', 'element': 'quay_element_48351d6'}, 'end_element')
    def quay_end_element(quay_self_5ed2fb4, quay_element_48351d6):
        assert _name_boundary.attributes(quay_self_5ed2fb4)['_indent_level'] > 0
        assert _name_boundary.attributes(quay_self_5ed2fb4)['stack'].pop() == quay_element_48351d6
        _name_boundary.attributes(quay_self_5ed2fb4)['_indent_level'] -= 1
        _name_boundary.attributes(quay_self_5ed2fb4)['writeln']('</%s>' % quay_element_48351d6)

    @_name_boundary.callable_contract({'self': 'quay_self_900b567', 'element': 'quay_element_22483d0', 'value': 'quay_value_95844bb'}, 'simple_element')
    def quay_simple_element(quay_self_900b567, quay_element_22483d0, quay_value_95844bb=None):
        if quay_value_95844bb is not None:
            quay_value_95844bb = quay__escape(quay_value_95844bb)
            _name_boundary.attributes(quay_self_900b567)['writeln']('<%s>%s</%s>' % (quay_element_22483d0, quay_value_95844bb, quay_element_22483d0))
        else:
            _name_boundary.attributes(quay_self_900b567)['writeln']('<%s/>' % quay_element_22483d0)

    @_name_boundary.callable_contract({'self': 'quay_self_f011b18', 'line': 'quay_line_d966d5a'}, 'writeln')
    def quay_writeln(quay_self_f011b18, quay_line_d966d5a):
        if quay_line_d966d5a:
            if isinstance(quay_line_d966d5a, str):
                quay_line_d966d5a = quay_line_d966d5a.encode('utf-8')
            _name_boundary.attributes(_name_boundary.attributes(quay_self_f011b18)['file'])['write'](_name_boundary.attributes(quay_self_f011b18)['_indent_level'] * _name_boundary.attributes(quay_self_f011b18)['indent'])
            _name_boundary.attributes(_name_boundary.attributes(quay_self_f011b18)['file'])['write'](quay_line_d966d5a)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_f011b18)['file'])['write'](b'\n')

@_name_boundary.class_contract('_PlistWriter', {'write': 'quay_write', 'write_value': 'quay_write_value', 'write_data': 'quay_write_data', 'write_bytes': 'quay_write_bytes', 'write_dict': 'quay_write_dict', 'write_array': 'quay_write_array', '_sort_keys': 'quay__sort_keys', '_skipkeys': 'quay__skipkeys', '_indent_level': 'quay__indent_level', 'writeln': 'quay_writeln', 'begin_element': 'quay_begin_element', 'end_element': 'quay_end_element', 'simple_element': 'quay_simple_element', 'indent': 'quay_indent'})
class quay__PlistWriter(quay__DumbXMLWriter):

    @_name_boundary.callable_contract({'self': 'quay_self_0176574', 'file': 'quay_file_941f0fe', 'indent_level': 'quay_indent_level_9c808d1', 'indent': 'quay_indent_564a15c', 'writeHeader': 'quay_writeHeader_a7b2b94', 'sort_keys': 'quay_sort_keys_968c6a6', 'skipkeys': 'quay_skipkeys_0148475'}, '__init__')
    def __init__(quay_self_0176574, quay_file_941f0fe, quay_indent_level_9c808d1=0, quay_indent_564a15c=b'\t', quay_writeHeader_a7b2b94=1, quay_sort_keys_968c6a6=True, quay_skipkeys_0148475=False):
        if quay_writeHeader_a7b2b94:
            _name_boundary.attributes(quay_file_941f0fe)['write'](quay_PLISTHEADER)
        quay__DumbXMLWriter.__init__(quay_self_0176574, quay_file_941f0fe, quay_indent_level_9c808d1, quay_indent_564a15c)
        _name_boundary.attributes(quay_self_0176574)['_sort_keys'] = quay_sort_keys_968c6a6
        _name_boundary.attributes(quay_self_0176574)['_skipkeys'] = quay_skipkeys_0148475

    @_name_boundary.callable_contract({'self': 'quay_self_3ac7987', 'value': 'quay_value_551d248'}, 'write')
    def quay_write(quay_self_3ac7987, quay_value_551d248):
        _name_boundary.attributes(quay_self_3ac7987)['writeln']('<plist version="1.0">')
        _name_boundary.attributes(quay_self_3ac7987)['write_value'](quay_value_551d248)
        _name_boundary.attributes(quay_self_3ac7987)['writeln']('</plist>')

    @_name_boundary.callable_contract({'self': 'quay_self_c578ec5', 'value': 'quay_value_36f1009'}, 'write_value')
    def quay_write_value(quay_self_c578ec5, quay_value_36f1009):
        if isinstance(quay_value_36f1009, str):
            _name_boundary.attributes(quay_self_c578ec5)['simple_element']('string', quay_value_36f1009)
        elif quay_value_36f1009 is True:
            _name_boundary.attributes(quay_self_c578ec5)['simple_element']('true')
        elif quay_value_36f1009 is False:
            _name_boundary.attributes(quay_self_c578ec5)['simple_element']('false')
        elif isinstance(quay_value_36f1009, int):
            if -1 << 63 <= quay_value_36f1009 < 1 << 64:
                _name_boundary.attributes(quay_self_c578ec5)['simple_element']('integer', '%d' % quay_value_36f1009)
            else:
                raise OverflowError(quay_value_36f1009)
        elif isinstance(quay_value_36f1009, float):
            _name_boundary.attributes(quay_self_c578ec5)['simple_element']('real', repr(quay_value_36f1009))
        elif isinstance(quay_value_36f1009, dict):
            _name_boundary.attributes(quay_self_c578ec5)['write_dict'](quay_value_36f1009)
        elif isinstance(quay_value_36f1009, quay_Data):
            _name_boundary.attributes(quay_self_c578ec5)['write_data'](quay_value_36f1009)
        elif isinstance(quay_value_36f1009, (bytes, bytearray)):
            _name_boundary.attributes(quay_self_c578ec5)['write_bytes'](quay_value_36f1009)
        elif isinstance(quay_value_36f1009, quay_datetime.datetime):
            _name_boundary.attributes(quay_self_c578ec5)['simple_element']('date', quay__date_to_string(quay_value_36f1009))
        elif isinstance(quay_value_36f1009, (tuple, list)):
            _name_boundary.attributes(quay_self_c578ec5)['write_array'](quay_value_36f1009)
        else:
            raise TypeError('unsupported type: %s' % type(quay_value_36f1009))

    @_name_boundary.callable_contract({'self': 'quay_self_5d42061', 'data': 'quay_data_95da546'}, 'write_data')
    def quay_write_data(quay_self_5d42061, quay_data_95da546):
        _name_boundary.attributes(quay_self_5d42061)['write_bytes'](_name_boundary.attributes(quay_data_95da546)['data'])

    @_name_boundary.callable_contract({'self': 'quay_self_7b18ae8', 'data': 'quay_data_9833129'}, 'write_bytes')
    def quay_write_bytes(quay_self_7b18ae8, quay_data_9833129):
        _name_boundary.attributes(quay_self_7b18ae8)['begin_element']('data')
        _name_boundary.attributes(quay_self_7b18ae8)['_indent_level'] -= 1
        quay_maxlinelength_5001892 = max(16, 76 - len(_name_boundary.attributes(quay_self_7b18ae8)['indent'].replace(b'\t', b' ' * 8) * _name_boundary.attributes(quay_self_7b18ae8)['_indent_level']))
        for quay_line_7582d9b in quay__encode_base64(quay_data_9833129, quay_maxlinelength_5001892).split(b'\n'):
            if quay_line_7582d9b:
                _name_boundary.attributes(quay_self_7b18ae8)['writeln'](quay_line_7582d9b)
        _name_boundary.attributes(quay_self_7b18ae8)['_indent_level'] += 1
        _name_boundary.attributes(quay_self_7b18ae8)['end_element']('data')

    @_name_boundary.callable_contract({'self': 'quay_self_f589b4c', 'd': 'quay_d_54638d5'}, 'write_dict')
    def quay_write_dict(quay_self_f589b4c, quay_d_54638d5):
        if quay_d_54638d5:
            _name_boundary.attributes(quay_self_f589b4c)['begin_element']('dict')
            if _name_boundary.attributes(quay_self_f589b4c)['_sort_keys']:
                quay_items_fb41740 = sorted(_name_boundary.attributes(quay_d_54638d5)['items']())
            else:
                quay_items_fb41740 = _name_boundary.attributes(quay_d_54638d5)['items']()
            for quay_key_82706e6, quay_value_9e590f6 in quay_items_fb41740:
                if not isinstance(quay_key_82706e6, str):
                    if _name_boundary.attributes(quay_self_f589b4c)['_skipkeys']:
                        continue
                    raise TypeError('keys must be strings')
                _name_boundary.attributes(quay_self_f589b4c)['simple_element']('key', quay_key_82706e6)
                _name_boundary.attributes(quay_self_f589b4c)['write_value'](quay_value_9e590f6)
            _name_boundary.attributes(quay_self_f589b4c)['end_element']('dict')
        else:
            _name_boundary.attributes(quay_self_f589b4c)['simple_element']('dict')

    @_name_boundary.callable_contract({'self': 'quay_self_cd30741', 'array': 'quay_array_cc6a5d4'}, 'write_array')
    def quay_write_array(quay_self_cd30741, quay_array_cc6a5d4):
        if quay_array_cc6a5d4:
            _name_boundary.attributes(quay_self_cd30741)['begin_element']('array')
            for quay_value_a644b64 in quay_array_cc6a5d4:
                _name_boundary.attributes(quay_self_cd30741)['write_value'](quay_value_a644b64)
            _name_boundary.attributes(quay_self_cd30741)['end_element']('array')
        else:
            _name_boundary.attributes(quay_self_cd30741)['simple_element']('array')

@_name_boundary.callable_contract({'header': 'quay_header_d32a04f'}, '_is_fmt_xml')
def quay__is_fmt_xml(quay_header_d32a04f):
    quay_prefixes_297a0af = (b'<?xml', b'<plist')
    for quay_pfx_8922ebd in quay_prefixes_297a0af:
        if quay_header_d32a04f.startswith(quay_pfx_8922ebd):
            return True
    for quay_bom_5b27cf5, quay_encoding_d1abaa0 in ((quay_codecs.BOM_UTF8, 'utf-8'), (quay_codecs.BOM_UTF16_BE, 'utf-16-be'), (quay_codecs.BOM_UTF16_LE, 'utf-16-le')):
        if not quay_header_d32a04f.startswith(quay_bom_5b27cf5):
            continue
        for quay_start_cc207af in quay_prefixes_297a0af:
            quay_prefix_05e2b92 = quay_bom_5b27cf5 + quay_start_cc207af.decode('ascii').encode(quay_encoding_d1abaa0)
            if quay_header_d32a04f[:len(quay_prefix_05e2b92)] == quay_prefix_05e2b92:
                return True
    return False

@_name_boundary.class_contract('InvalidFileException', {})
class quay_InvalidFileException(ValueError):

    @_name_boundary.callable_contract({'self': 'quay_self_e179c7d', 'message': 'quay_message_993edd4'}, '__init__')
    def __init__(quay_self_e179c7d, quay_message_993edd4='Invalid file'):
        ValueError.__init__(quay_self_e179c7d, quay_message_993edd4)
quay__BINARY_FORMAT = {1: 'B', 2: 'H', 4: 'L', 8: 'Q'}
quay__undefined = object()

@_name_boundary.class_contract('_BinaryPlistParser', {'parse': 'quay_parse', '_get_size': 'quay__get_size', '_read_ints': 'quay__read_ints', '_read_refs': 'quay__read_refs', '_read_object': 'quay__read_object', '_use_builtin_types': 'quay__use_builtin_types', '_dict_type': 'quay__dict_type', '_fp': 'quay__fp', '_object_offsets': 'quay__object_offsets', '_objects': 'quay__objects', '_ref_size': 'quay__ref_size'})
class quay__BinaryPlistParser:
    """
    Read or write a binary plist file, following the description of the binary
    format.  Raise InvalidFileException in case of error, otherwise return the
    root object.
    see also: http://opensource.apple.com/source/CF/CF-744.18/CFBinaryPList.c
    """

    @_name_boundary.callable_contract({'self': 'quay_self_839f7e9', 'use_builtin_types': 'quay_use_builtin_types_b898df5', 'dict_type': 'quay_dict_type_a254387'}, '__init__')
    def __init__(quay_self_839f7e9, quay_use_builtin_types_b898df5, quay_dict_type_a254387):
        _name_boundary.attributes(quay_self_839f7e9)['_use_builtin_types'] = quay_use_builtin_types_b898df5
        _name_boundary.attributes(quay_self_839f7e9)['_dict_type'] = quay_dict_type_a254387

    @_name_boundary.callable_contract({'self': 'quay_self_a50edca', 'fp': 'quay_fp_c926c59'}, 'parse')
    def quay_parse(quay_self_a50edca, quay_fp_c926c59):
        try:
            _name_boundary.attributes(quay_self_a50edca)['_fp'] = quay_fp_c926c59
            _name_boundary.attributes(quay_self_a50edca)['_fp'].seek(-32, quay_os.SEEK_END)
            quay_trailer_01a183c = _name_boundary.attributes(_name_boundary.attributes(quay_self_a50edca)['_fp'])['read'](32)
            if len(quay_trailer_01a183c) != 32:
                raise quay_InvalidFileException()
            quay_offset_size_2ca7e1b, _name_boundary.attributes(quay_self_a50edca)['_ref_size'], quay_num_objects_579b7b6, quay_top_object_732f176, quay_offset_table_offset_a7ce551 = quay_struct.unpack('>6xBBQQQ', quay_trailer_01a183c)
            _name_boundary.attributes(quay_self_a50edca)['_fp'].seek(quay_offset_table_offset_a7ce551)
            _name_boundary.attributes(quay_self_a50edca)['_object_offsets'] = _name_boundary.attributes(quay_self_a50edca)['_read_ints'](quay_num_objects_579b7b6, quay_offset_size_2ca7e1b)
            _name_boundary.attributes(quay_self_a50edca)['_objects'] = [quay__undefined] * quay_num_objects_579b7b6
            return _name_boundary.attributes(quay_self_a50edca)['_read_object'](quay_top_object_732f176)
        except (OSError, IndexError, _name_boundary.attributes(quay_struct)['error'], OverflowError, ValueError):
            raise quay_InvalidFileException()

    @_name_boundary.callable_contract({'self': 'quay_self_e9e5b75', 'tokenL': 'quay_tokenL_f6df830'}, '_get_size')
    def quay__get_size(quay_self_e9e5b75, quay_tokenL_f6df830):
        """ return the size of the next object."""
        if quay_tokenL_f6df830 == 15:
            quay_m_aa77b0c = _name_boundary.attributes(_name_boundary.attributes(quay_self_e9e5b75)['_fp'])['read'](1)[0] & 3
            quay_s_f8edea0 = 1 << quay_m_aa77b0c
            quay_f_3f92e80 = '>' + quay__BINARY_FORMAT[quay_s_f8edea0]
            return quay_struct.unpack(quay_f_3f92e80, _name_boundary.attributes(_name_boundary.attributes(quay_self_e9e5b75)['_fp'])['read'](quay_s_f8edea0))[0]
        return quay_tokenL_f6df830

    @_name_boundary.callable_contract({'self': 'quay_self_2caab7e', 'n': 'quay_n_c70f4ff', 'size': 'quay_size_f9b47d0'}, '_read_ints')
    def quay__read_ints(quay_self_2caab7e, quay_n_c70f4ff, quay_size_f9b47d0):
        quay_data_e5af6a6 = _name_boundary.attributes(_name_boundary.attributes(quay_self_2caab7e)['_fp'])['read'](quay_size_f9b47d0 * quay_n_c70f4ff)
        if quay_size_f9b47d0 in quay__BINARY_FORMAT:
            return quay_struct.unpack(f'>{quay_n_c70f4ff}{quay__BINARY_FORMAT[quay_size_f9b47d0]}', quay_data_e5af6a6)
        else:
            if not quay_size_f9b47d0 or len(quay_data_e5af6a6) != quay_size_f9b47d0 * quay_n_c70f4ff:
                raise quay_InvalidFileException()
            return tuple((int.from_bytes(quay_data_e5af6a6[quay_i_c4be9a2:quay_i_c4be9a2 + quay_size_f9b47d0], 'big') for quay_i_c4be9a2 in range(0, quay_size_f9b47d0 * quay_n_c70f4ff, quay_size_f9b47d0)))

    @_name_boundary.callable_contract({'self': 'quay_self_82d3660', 'n': 'quay_n_1958454'}, '_read_refs')
    def quay__read_refs(quay_self_82d3660, quay_n_1958454):
        return _name_boundary.attributes(quay_self_82d3660)['_read_ints'](quay_n_1958454, _name_boundary.attributes(quay_self_82d3660)['_ref_size'])

    @_name_boundary.callable_contract({'self': 'quay_self_1d57978', 'ref': 'quay_ref_643df8b'}, '_read_object')
    def quay__read_object(quay_self_1d57978, quay_ref_643df8b):
        """
        read the object by reference.
        May recursively read sub-objects (content of an array/dict/set)
        """
        quay_result_8082304 = _name_boundary.attributes(quay_self_1d57978)['_objects'][quay_ref_643df8b]
        if quay_result_8082304 is not quay__undefined:
            return quay_result_8082304
        quay_offset_26ff770 = _name_boundary.attributes(quay_self_1d57978)['_object_offsets'][quay_ref_643df8b]
        _name_boundary.attributes(quay_self_1d57978)['_fp'].seek(quay_offset_26ff770)
        quay_token_bafd2cd = _name_boundary.attributes(_name_boundary.attributes(quay_self_1d57978)['_fp'])['read'](1)[0]
        quay_tokenH_5c36372, quay_tokenL_f0217a8 = (quay_token_bafd2cd & 240, quay_token_bafd2cd & 15)
        if quay_token_bafd2cd == 0:
            quay_result_8082304 = None
        elif quay_token_bafd2cd == 8:
            quay_result_8082304 = False
        elif quay_token_bafd2cd == 9:
            quay_result_8082304 = True
        elif quay_token_bafd2cd == 15:
            quay_result_8082304 = b''
        elif quay_tokenH_5c36372 == 16:
            quay_result_8082304 = int.from_bytes(_name_boundary.attributes(_name_boundary.attributes(quay_self_1d57978)['_fp'])['read'](1 << quay_tokenL_f0217a8), 'big', signed=quay_tokenL_f0217a8 >= 3)
        elif quay_token_bafd2cd == 34:
            quay_result_8082304 = quay_struct.unpack('>f', _name_boundary.attributes(_name_boundary.attributes(quay_self_1d57978)['_fp'])['read'](4))[0]
        elif quay_token_bafd2cd == 35:
            quay_result_8082304 = quay_struct.unpack('>d', _name_boundary.attributes(_name_boundary.attributes(quay_self_1d57978)['_fp'])['read'](8))[0]
        elif quay_token_bafd2cd == 51:
            quay_f_5814d77 = quay_struct.unpack('>d', _name_boundary.attributes(_name_boundary.attributes(quay_self_1d57978)['_fp'])['read'](8))[0]
            quay_result_8082304 = quay_datetime.datetime(2001, 1, 1) + quay_datetime.timedelta(seconds=quay_f_5814d77)
        elif quay_tokenH_5c36372 == 64:
            quay_s_1f13791 = _name_boundary.attributes(quay_self_1d57978)['_get_size'](quay_tokenL_f0217a8)
            quay_result_8082304 = _name_boundary.attributes(_name_boundary.attributes(quay_self_1d57978)['_fp'])['read'](quay_s_1f13791)
            if len(quay_result_8082304) != quay_s_1f13791:
                raise quay_InvalidFileException()
            if not _name_boundary.attributes(quay_self_1d57978)['_use_builtin_types']:
                quay_result_8082304 = quay_Data(quay_result_8082304)
        elif quay_tokenH_5c36372 == 80:
            quay_s_1f13791 = _name_boundary.attributes(quay_self_1d57978)['_get_size'](quay_tokenL_f0217a8)
            quay_data_071e2c3 = _name_boundary.attributes(_name_boundary.attributes(quay_self_1d57978)['_fp'])['read'](quay_s_1f13791)
            if len(quay_data_071e2c3) != quay_s_1f13791:
                raise quay_InvalidFileException()
            quay_result_8082304 = quay_data_071e2c3.decode('ascii')
        elif quay_tokenH_5c36372 == 96:
            quay_s_1f13791 = _name_boundary.attributes(quay_self_1d57978)['_get_size'](quay_tokenL_f0217a8) * 2
            quay_data_071e2c3 = _name_boundary.attributes(_name_boundary.attributes(quay_self_1d57978)['_fp'])['read'](quay_s_1f13791)
            if len(quay_data_071e2c3) != quay_s_1f13791:
                raise quay_InvalidFileException()
            quay_result_8082304 = quay_data_071e2c3.decode('utf-16be')
        elif quay_tokenH_5c36372 == 160:
            quay_s_1f13791 = _name_boundary.attributes(quay_self_1d57978)['_get_size'](quay_tokenL_f0217a8)
            quay_obj_refs_4416828 = _name_boundary.attributes(quay_self_1d57978)['_read_refs'](quay_s_1f13791)
            quay_result_8082304 = []
            _name_boundary.attributes(quay_self_1d57978)['_objects'][quay_ref_643df8b] = quay_result_8082304
            quay_result_8082304.extend((_name_boundary.attributes(quay_self_1d57978)['_read_object'](quay_x_2a6c65a) for quay_x_2a6c65a in quay_obj_refs_4416828))
        elif quay_tokenH_5c36372 == 208:
            quay_s_1f13791 = _name_boundary.attributes(quay_self_1d57978)['_get_size'](quay_tokenL_f0217a8)
            quay_key_refs_8a4fad5 = _name_boundary.attributes(quay_self_1d57978)['_read_refs'](quay_s_1f13791)
            quay_obj_refs_4416828 = _name_boundary.attributes(quay_self_1d57978)['_read_refs'](quay_s_1f13791)
            quay_result_8082304 = _name_boundary.attributes(quay_self_1d57978)['_dict_type']()
            _name_boundary.attributes(quay_self_1d57978)['_objects'][quay_ref_643df8b] = quay_result_8082304
            try:
                for quay_k_f266f88, quay_o_f6fcb84 in zip(quay_key_refs_8a4fad5, quay_obj_refs_4416828):
                    quay_result_8082304[_name_boundary.attributes(quay_self_1d57978)['_read_object'](quay_k_f266f88)] = _name_boundary.attributes(quay_self_1d57978)['_read_object'](quay_o_f6fcb84)
            except TypeError:
                raise quay_InvalidFileException()
        else:
            raise quay_InvalidFileException()
        _name_boundary.attributes(quay_self_1d57978)['_objects'][quay_ref_643df8b] = quay_result_8082304
        return quay_result_8082304

@_name_boundary.callable_contract({'count': 'quay_count_1cbbdc7'}, '_count_to_size')
def quay__count_to_size(quay_count_1cbbdc7):
    if quay_count_1cbbdc7 < 1 << 8:
        return 1
    elif quay_count_1cbbdc7 < 1 << 16:
        return 2
    elif quay_count_1cbbdc7 << 1 << 32:
        return 4
    else:
        return 8
quay__scalars = (str, int, float, quay_datetime.datetime, bytes)

@_name_boundary.class_contract('_BinaryPlistWriter', {'write': 'quay_write', '_flatten': 'quay__flatten', '_getrefnum': 'quay__getrefnum', '_write_size': 'quay__write_size', '_write_object': 'quay__write_object', '_fp': 'quay__fp', '_sort_keys': 'quay__sort_keys', '_skipkeys': 'quay__skipkeys', '_objlist': 'quay__objlist', '_objtable': 'quay__objtable', '_objidtable': 'quay__objidtable', '_object_offsets': 'quay__object_offsets', '_ref_size': 'quay__ref_size', '_ref_format': 'quay__ref_format'})
class quay__BinaryPlistWriter(object):

    @_name_boundary.callable_contract({'self': 'quay_self_ad3bdc5', 'fp': 'quay_fp_96afa79', 'sort_keys': 'quay_sort_keys_31e5731', 'skipkeys': 'quay_skipkeys_6e5639b'}, '__init__')
    def __init__(quay_self_ad3bdc5, quay_fp_96afa79, quay_sort_keys_31e5731, quay_skipkeys_6e5639b):
        _name_boundary.attributes(quay_self_ad3bdc5)['_fp'] = quay_fp_96afa79
        _name_boundary.attributes(quay_self_ad3bdc5)['_sort_keys'] = quay_sort_keys_31e5731
        _name_boundary.attributes(quay_self_ad3bdc5)['_skipkeys'] = quay_skipkeys_6e5639b

    @_name_boundary.callable_contract({'self': 'quay_self_c184776', 'value': 'quay_value_f8b5890'}, 'write')
    def quay_write(quay_self_c184776, quay_value_f8b5890):
        _name_boundary.attributes(quay_self_c184776)['_objlist'] = []
        _name_boundary.attributes(quay_self_c184776)['_objtable'] = {}
        _name_boundary.attributes(quay_self_c184776)['_objidtable'] = {}
        _name_boundary.attributes(quay_self_c184776)['_flatten'](quay_value_f8b5890)
        quay_num_objects_faea34a = len(_name_boundary.attributes(quay_self_c184776)['_objlist'])
        _name_boundary.attributes(quay_self_c184776)['_object_offsets'] = [0] * quay_num_objects_faea34a
        _name_boundary.attributes(quay_self_c184776)['_ref_size'] = quay__count_to_size(quay_num_objects_faea34a)
        _name_boundary.attributes(quay_self_c184776)['_ref_format'] = quay__BINARY_FORMAT[_name_boundary.attributes(quay_self_c184776)['_ref_size']]
        _name_boundary.attributes(_name_boundary.attributes(quay_self_c184776)['_fp'])['write'](b'bplist00')
        for quay_obj_e8ae645 in _name_boundary.attributes(quay_self_c184776)['_objlist']:
            _name_boundary.attributes(quay_self_c184776)['_write_object'](quay_obj_e8ae645)
        quay_top_object_a20e070 = _name_boundary.attributes(quay_self_c184776)['_getrefnum'](quay_value_f8b5890)
        quay_offset_table_offset_1211c63 = _name_boundary.attributes(quay_self_c184776)['_fp'].tell()
        quay_offset_size_991cf11 = quay__count_to_size(quay_offset_table_offset_1211c63)
        quay_offset_format_dfed28e = '>' + quay__BINARY_FORMAT[quay_offset_size_991cf11] * quay_num_objects_faea34a
        _name_boundary.attributes(_name_boundary.attributes(quay_self_c184776)['_fp'])['write'](quay_struct.pack(quay_offset_format_dfed28e, *_name_boundary.attributes(quay_self_c184776)['_object_offsets']))
        quay_sort_version_c50bcc9 = 0
        quay_trailer_1cfe834 = (quay_sort_version_c50bcc9, quay_offset_size_991cf11, _name_boundary.attributes(quay_self_c184776)['_ref_size'], quay_num_objects_faea34a, quay_top_object_a20e070, quay_offset_table_offset_1211c63)
        _name_boundary.attributes(_name_boundary.attributes(quay_self_c184776)['_fp'])['write'](quay_struct.pack('>5xBBBQQQ', *quay_trailer_1cfe834))

    @_name_boundary.callable_contract({'self': 'quay_self_2776da7', 'value': 'quay_value_a957645'}, '_flatten')
    def quay__flatten(quay_self_2776da7, quay_value_a957645):
        if isinstance(quay_value_a957645, quay__scalars):
            if (type(quay_value_a957645), quay_value_a957645) in _name_boundary.attributes(quay_self_2776da7)['_objtable']:
                return
        elif isinstance(quay_value_a957645, quay_Data):
            if (type(_name_boundary.attributes(quay_value_a957645)['data']), _name_boundary.attributes(quay_value_a957645)['data']) in _name_boundary.attributes(quay_self_2776da7)['_objtable']:
                return
        elif id(quay_value_a957645) in _name_boundary.attributes(quay_self_2776da7)['_objidtable']:
            return
        quay_refnum_7f28c7e = len(_name_boundary.attributes(quay_self_2776da7)['_objlist'])
        _name_boundary.attributes(quay_self_2776da7)['_objlist'].append(quay_value_a957645)
        if isinstance(quay_value_a957645, quay__scalars):
            _name_boundary.attributes(quay_self_2776da7)['_objtable'][type(quay_value_a957645), quay_value_a957645] = quay_refnum_7f28c7e
        elif isinstance(quay_value_a957645, quay_Data):
            _name_boundary.attributes(quay_self_2776da7)['_objtable'][type(_name_boundary.attributes(quay_value_a957645)['data']), _name_boundary.attributes(quay_value_a957645)['data']] = quay_refnum_7f28c7e
        else:
            _name_boundary.attributes(quay_self_2776da7)['_objidtable'][id(quay_value_a957645)] = quay_refnum_7f28c7e
        if isinstance(quay_value_a957645, dict):
            quay_keys_8cab536 = []
            quay_values_9071b45 = []
            quay_items_2ef7450 = _name_boundary.attributes(quay_value_a957645)['items']()
            if _name_boundary.attributes(quay_self_2776da7)['_sort_keys']:
                quay_items_2ef7450 = sorted(quay_items_2ef7450)
            for quay_k_c19140b, quay_v_e14792f in quay_items_2ef7450:
                if not isinstance(quay_k_c19140b, str):
                    if _name_boundary.attributes(quay_self_2776da7)['_skipkeys']:
                        continue
                    raise TypeError('keys must be strings')
                quay_keys_8cab536.append(quay_k_c19140b)
                quay_values_9071b45.append(quay_v_e14792f)
            for quay_o_c28e0ab in quay_itertools.chain(quay_keys_8cab536, quay_values_9071b45):
                _name_boundary.attributes(quay_self_2776da7)['_flatten'](quay_o_c28e0ab)
        elif isinstance(quay_value_a957645, (list, tuple)):
            for quay_o_c28e0ab in quay_value_a957645:
                _name_boundary.attributes(quay_self_2776da7)['_flatten'](quay_o_c28e0ab)

    @_name_boundary.callable_contract({'self': 'quay_self_4972934', 'value': 'quay_value_142aa1a'}, '_getrefnum')
    def quay__getrefnum(quay_self_4972934, quay_value_142aa1a):
        if isinstance(quay_value_142aa1a, quay__scalars):
            return _name_boundary.attributes(quay_self_4972934)['_objtable'][type(quay_value_142aa1a), quay_value_142aa1a]
        elif isinstance(quay_value_142aa1a, quay_Data):
            return _name_boundary.attributes(quay_self_4972934)['_objtable'][type(_name_boundary.attributes(quay_value_142aa1a)['data']), _name_boundary.attributes(quay_value_142aa1a)['data']]
        else:
            return _name_boundary.attributes(quay_self_4972934)['_objidtable'][id(quay_value_142aa1a)]

    @_name_boundary.callable_contract({'self': 'quay_self_18fbf49', 'token': 'quay_token_5959dd1', 'size': 'quay_size_d88e1d8'}, '_write_size')
    def quay__write_size(quay_self_18fbf49, quay_token_5959dd1, quay_size_d88e1d8):
        if quay_size_d88e1d8 < 15:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_18fbf49)['_fp'])['write'](quay_struct.pack('>B', quay_token_5959dd1 | quay_size_d88e1d8))
        elif quay_size_d88e1d8 < 1 << 8:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_18fbf49)['_fp'])['write'](quay_struct.pack('>BBB', quay_token_5959dd1 | 15, 16, quay_size_d88e1d8))
        elif quay_size_d88e1d8 < 1 << 16:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_18fbf49)['_fp'])['write'](quay_struct.pack('>BBH', quay_token_5959dd1 | 15, 17, quay_size_d88e1d8))
        elif quay_size_d88e1d8 < 1 << 32:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_18fbf49)['_fp'])['write'](quay_struct.pack('>BBL', quay_token_5959dd1 | 15, 18, quay_size_d88e1d8))
        else:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_18fbf49)['_fp'])['write'](quay_struct.pack('>BBQ', quay_token_5959dd1 | 15, 19, quay_size_d88e1d8))

    @_name_boundary.callable_contract({'self': 'quay_self_5623850', 'value': 'quay_value_bee5c4a'}, '_write_object')
    def quay__write_object(quay_self_5623850, quay_value_bee5c4a):
        quay_ref_694fb39 = _name_boundary.attributes(quay_self_5623850)['_getrefnum'](quay_value_bee5c4a)
        _name_boundary.attributes(quay_self_5623850)['_object_offsets'][quay_ref_694fb39] = _name_boundary.attributes(quay_self_5623850)['_fp'].tell()
        if quay_value_bee5c4a is None:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](b'\x00')
        elif quay_value_bee5c4a is False:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](b'\x08')
        elif quay_value_bee5c4a is True:
            _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](b'\t')
        elif isinstance(quay_value_bee5c4a, int):
            if quay_value_bee5c4a < 0:
                try:
                    _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](quay_struct.pack('>Bq', 19, quay_value_bee5c4a))
                except _name_boundary.attributes(quay_struct)['error']:
                    raise OverflowError(quay_value_bee5c4a) from None
            elif quay_value_bee5c4a < 1 << 8:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](quay_struct.pack('>BB', 16, quay_value_bee5c4a))
            elif quay_value_bee5c4a < 1 << 16:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](quay_struct.pack('>BH', 17, quay_value_bee5c4a))
            elif quay_value_bee5c4a < 1 << 32:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](quay_struct.pack('>BL', 18, quay_value_bee5c4a))
            elif quay_value_bee5c4a < 1 << 63:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](quay_struct.pack('>BQ', 19, quay_value_bee5c4a))
            elif quay_value_bee5c4a < 1 << 64:
                _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](b'\x14' + quay_value_bee5c4a.to_bytes(16, 'big', signed=True))
            else:
                raise OverflowError(quay_value_bee5c4a)
        elif isinstance(quay_value_bee5c4a, float):
            _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](quay_struct.pack('>Bd', 35, quay_value_bee5c4a))
        elif isinstance(quay_value_bee5c4a, quay_datetime.datetime):
            quay_f_a31fb8b = (quay_value_bee5c4a - quay_datetime.datetime(2001, 1, 1)).total_seconds()
            _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](quay_struct.pack('>Bd', 51, quay_f_a31fb8b))
        elif isinstance(quay_value_bee5c4a, quay_Data):
            _name_boundary.attributes(quay_self_5623850)['_write_size'](64, len(_name_boundary.attributes(quay_value_bee5c4a)['data']))
            _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](_name_boundary.attributes(quay_value_bee5c4a)['data'])
        elif isinstance(quay_value_bee5c4a, (bytes, bytearray)):
            _name_boundary.attributes(quay_self_5623850)['_write_size'](64, len(quay_value_bee5c4a))
            _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](quay_value_bee5c4a)
        elif isinstance(quay_value_bee5c4a, str):
            try:
                quay_t_4658194 = quay_value_bee5c4a.encode('ascii')
                _name_boundary.attributes(quay_self_5623850)['_write_size'](80, len(quay_value_bee5c4a))
            except UnicodeEncodeError:
                quay_t_4658194 = quay_value_bee5c4a.encode('utf-16be')
                _name_boundary.attributes(quay_self_5623850)['_write_size'](96, len(quay_t_4658194) // 2)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](quay_t_4658194)
        elif isinstance(quay_value_bee5c4a, (list, tuple)):
            quay_refs_2543868 = [_name_boundary.attributes(quay_self_5623850)['_getrefnum'](quay_o_d8c87e6) for quay_o_d8c87e6 in quay_value_bee5c4a]
            quay_s_d8b7d03 = len(quay_refs_2543868)
            _name_boundary.attributes(quay_self_5623850)['_write_size'](160, quay_s_d8b7d03)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](quay_struct.pack('>' + _name_boundary.attributes(quay_self_5623850)['_ref_format'] * quay_s_d8b7d03, *quay_refs_2543868))
        elif isinstance(quay_value_bee5c4a, dict):
            quay_keyRefs_9512aee, quay_valRefs_1fda0ce = ([], [])
            if _name_boundary.attributes(quay_self_5623850)['_sort_keys']:
                quay_rootItems_c54fe73 = sorted(_name_boundary.attributes(quay_value_bee5c4a)['items']())
            else:
                quay_rootItems_c54fe73 = _name_boundary.attributes(quay_value_bee5c4a)['items']()
            for quay_k_f1bccc6, quay_v_9532ff3 in quay_rootItems_c54fe73:
                if not isinstance(quay_k_f1bccc6, str):
                    if _name_boundary.attributes(quay_self_5623850)['_skipkeys']:
                        continue
                    raise TypeError('keys must be strings')
                quay_keyRefs_9512aee.append(_name_boundary.attributes(quay_self_5623850)['_getrefnum'](quay_k_f1bccc6))
                quay_valRefs_1fda0ce.append(_name_boundary.attributes(quay_self_5623850)['_getrefnum'](quay_v_9532ff3))
            quay_s_d8b7d03 = len(quay_keyRefs_9512aee)
            _name_boundary.attributes(quay_self_5623850)['_write_size'](208, quay_s_d8b7d03)
            _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](quay_struct.pack('>' + _name_boundary.attributes(quay_self_5623850)['_ref_format'] * quay_s_d8b7d03, *quay_keyRefs_9512aee))
            _name_boundary.attributes(_name_boundary.attributes(quay_self_5623850)['_fp'])['write'](quay_struct.pack('>' + _name_boundary.attributes(quay_self_5623850)['_ref_format'] * quay_s_d8b7d03, *quay_valRefs_1fda0ce))
        else:
            raise TypeError(quay_value_bee5c4a)

@_name_boundary.callable_contract({'header': 'quay_header_34a6f65'}, '_is_fmt_binary')
def quay__is_fmt_binary(quay_header_34a6f65):
    return quay_header_34a6f65[:8] == b'bplist00'
quay__FORMATS = {FMT_XML: dict(detect=quay__is_fmt_xml, parser=quay__PlistParser, writer=quay__PlistWriter), FMT_BINARY: dict(detect=quay__is_fmt_binary, parser=quay__BinaryPlistParser, writer=quay__BinaryPlistWriter)}

@_name_boundary.callable_contract({'fp': 'quay_fp_1f4730e', 'fmt': 'quay_fmt_4933a55', 'use_builtin_types': 'quay_use_builtin_types_4115a46', 'dict_type': 'quay_dict_type_77a4e88'}, 'load')
def quay_load(quay_fp_1f4730e, *, quay_fmt_4933a55=None, quay_use_builtin_types_4115a46=True, quay_dict_type_77a4e88=dict):
    """Read a .plist file. 'fp' should be a readable and binary file object.
    Return the unpacked root object (which usually is a dictionary).
    """
    if quay_fmt_4933a55 is None:
        quay_header_921cbc3 = _name_boundary.attributes(quay_fp_1f4730e)['read'](32)
        quay_fp_1f4730e.seek(0)
        for quay_info_17fb245 in quay__FORMATS.values():
            if quay_info_17fb245['detect'](quay_header_921cbc3):
                quay_P_b884487 = quay_info_17fb245['parser']
                break
        else:
            raise quay_InvalidFileException()
    else:
        quay_P_b884487 = quay__FORMATS[quay_fmt_4933a55]['parser']
    quay_p_6c4b45c = quay_P_b884487(use_builtin_types=quay_use_builtin_types_4115a46, dict_type=quay_dict_type_77a4e88)
    return _name_boundary.attributes(quay_p_6c4b45c)['parse'](quay_fp_1f4730e)

@_name_boundary.callable_contract({'value': 'quay_value_ba095d2', 'fmt': 'quay_fmt_509da07', 'use_builtin_types': 'quay_use_builtin_types_e5ee2a1', 'dict_type': 'quay_dict_type_11331e6'}, 'loads')
def quay_loads(quay_value_ba095d2, *, quay_fmt_509da07=None, quay_use_builtin_types_e5ee2a1=True, quay_dict_type_11331e6=dict):
    """Read a .plist file from a bytes object.
    Return the unpacked root object (which usually is a dictionary).
    """
    quay_fp_157aaa0 = quay_BytesIO(quay_value_ba095d2)
    return quay_load(quay_fp_157aaa0, fmt=quay_fmt_509da07, use_builtin_types=quay_use_builtin_types_e5ee2a1, dict_type=quay_dict_type_11331e6)

@_name_boundary.callable_contract({'value': 'quay_value_dd1be43', 'fp': 'quay_fp_d1c1989', 'fmt': 'quay_fmt_ff34a46', 'sort_keys': 'quay_sort_keys_f647f27', 'skipkeys': 'quay_skipkeys_e260cca'}, 'dump')
def quay_dump(quay_value_dd1be43, quay_fp_d1c1989, *, quay_fmt_ff34a46=FMT_XML, quay_sort_keys_f647f27=True, quay_skipkeys_e260cca=False):
    """Write 'value' to a .plist file. 'fp' should be a writable,
    binary file object.
    """
    if quay_fmt_ff34a46 not in quay__FORMATS:
        raise ValueError('Unsupported format: %r' % (quay_fmt_ff34a46,))
    quay_writer_75c7ac7 = quay__FORMATS[quay_fmt_ff34a46]['writer'](quay_fp_d1c1989, sort_keys=quay_sort_keys_f647f27, skipkeys=quay_skipkeys_e260cca)
    _name_boundary.attributes(quay_writer_75c7ac7)['write'](quay_value_dd1be43)

@_name_boundary.callable_contract({'value': 'quay_value_a5cdaf7', 'fmt': 'quay_fmt_647fc7a', 'skipkeys': 'quay_skipkeys_4502cde', 'sort_keys': 'quay_sort_keys_8b4cd0b'}, 'dumps')
def quay_dumps(quay_value_a5cdaf7, *, quay_fmt_647fc7a=FMT_XML, quay_skipkeys_4502cde=False, quay_sort_keys_8b4cd0b=True):
    """Return a bytes object with the contents for a .plist file.
    """
    quay_fp_8d8eba3 = quay_BytesIO()
    quay_dump(quay_value_a5cdaf7, quay_fp_8d8eba3, fmt=quay_fmt_647fc7a, skipkeys=quay_skipkeys_4502cde, sort_keys=quay_sort_keys_8b4cd0b)
    return quay_fp_8d8eba3.getvalue()
_name_boundary.module_contract(globals(), {'ParserCreate': 'quay_ParserCreate', 'writePlistToBytes': 'quay_writePlistToBytes', '_PlistParser': 'quay__PlistParser', 'os': 'quay_os', '_is_fmt_binary': 'quay__is_fmt_binary', '_date_to_string': 'quay__date_to_string', '_date_from_string': 'quay__date_from_string', 'readPlist': 'quay_readPlist', '_undefined': 'quay__undefined', '_maybe_open': 'quay__maybe_open', '_count_to_size': 'quay__count_to_size', 'dump': 'quay_dump', 'codecs': 'quay_codecs', '_is_fmt_xml': 'quay__is_fmt_xml', '_scalars': 'quay__scalars', 'warn': 'quay_warn', '_DumbXMLWriter': 'quay__DumbXMLWriter', '_controlCharPat': 'quay__controlCharPat', 'PlistFormat': 'quay_PlistFormat', '_decode_base64': 'quay__decode_base64', '_BinaryPlistParser': 'quay__BinaryPlistParser', '_BINARY_FORMAT': 'quay__BINARY_FORMAT', 'load': 'quay_load', 'binascii': 'quay_binascii', 'writePlist': 'quay_writePlist', 'dumps': 'quay_dumps', '_PlistWriter': 'quay__PlistWriter', 'InvalidFileException': 'quay_InvalidFileException', '_BinaryPlistWriter': 'quay__BinaryPlistWriter', 'BytesIO': 'quay_BytesIO', 'loads': 'quay_loads', 'Data': 'quay_Data', 'struct': 'quay_struct', '_encode_base64': 'quay__encode_base64', '_escape': 'quay__escape', 'PLISTHEADER': 'quay_PLISTHEADER', '_FORMATS': 'quay__FORMATS', 'itertools': 'quay_itertools', '_dateParser': 'quay__dateParser', 'contextlib': 'quay_contextlib', 're': 'quay_re', 'readPlistFromBytes': 'quay_readPlistFromBytes', 'enum': 'quay_enum', 'datetime': 'quay_datetime'})
