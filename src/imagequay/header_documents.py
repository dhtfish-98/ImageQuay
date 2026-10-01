# Derived from src/ktool/headers.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  headers.py
#
#  This file contains the utilities used to create ObjC Header File dumps
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary
from typing import List as quay_List, Dict as quay_Dict
from imagequay.metadata_reader import quay_SymbolType as quay_SymbolType, quay_Image as quay_Image
from imagequay.objc_model import quay_ObjCImage as quay_ObjCImage, quay_Class as quay_Class, quay_Category as quay_Category, quay_Protocol as quay_Protocol, quay_Property as quay_Property, quay_Method as quay_Method, quay_Ivar as quay_Ivar
from imagequay.formatting import quay_IMAGEQUAY_VERSION as quay_IMAGEQUAY_VERSION
from pygments import highlight as quay_highlight
from pygments.formatters.terminal import TerminalFormatter as quay_TerminalFormatter
try:
    from pygments.lexers.objective import ObjectiveCLexer as quay_ObjectiveCLexer
except ImportError:
    quay_ObjectiveCLexer = None

@_name_boundary.class_contract('HeaderUtils', {'header_head_html': 'quay_header_head_html', 'header_head': 'quay_header_head'})
class quay_HeaderUtils:

    @staticmethod
    @_name_boundary.callable_contract({'image': 'quay_image_38d0a48'}, 'header_head_html')
    def quay_header_head_html(quay_image_38d0a48: quay_Image) -> str:
        """
        This is the prefix comments at the very top of the headers generated

        :param image: MachO Image
        :return: Newline delimited string to be placed at the top of the header.
        """
        try:
            quay_prefix_f1775a9 = '\n<div class="highlight"><pre><span></span><span class="c1">// Headers generated with imagequay v{}</span>\n<span class="c1">// <a href="https://github.com/0cyn/imagequay">https://github.com/0cyn/imagequay</a> | pip3 install k2l</span>\n<span class="c1">// Platform: {} | Minimum OS: {} | SDK: {}</span>'.format(quay_IMAGEQUAY_VERSION, _name_boundary.attributes(_name_boundary.attributes(quay_image_38d0a48)['platform'])['name'], f"{_name_boundary.attributes(_name_boundary.attributes(quay_image_38d0a48)['minos'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_image_38d0a48)['minos'])['y']}.{_name_boundary.attributes(quay_image_38d0a48)['minos'].z}", f"{_name_boundary.attributes(_name_boundary.attributes(quay_image_38d0a48)['sdk_version'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_image_38d0a48)['sdk_version'])['y']}.{_name_boundary.attributes(quay_image_38d0a48)['sdk_version'].z}")
        except AttributeError:
            quay_prefix_f1775a9 = '\n<div class="highlight"><pre><span></span><span class="c1">// Headers generated with imagequay v{}</span>\n<span class="c1">// https://github.com/0cyn/imagequay | pip3 install k2l</span>\n<span class="c1">// Issue loading image metadata'.format(quay_IMAGEQUAY_VERSION)
        return quay_prefix_f1775a9

    @staticmethod
    @_name_boundary.callable_contract({'image': 'quay_image_bab6c82'}, 'header_head')
    def quay_header_head(quay_image_bab6c82: quay_Image) -> str:
        """
        This is the prefix comments at the very top of the headers generated

        :param image: MachO Image
        :return: Newline delimited string to be placed at the top of the header.
        """
        try:
            quay_prefix_0d55e4b = '// Headers generated with imagequay v' + quay_IMAGEQUAY_VERSION + '\n'
            quay_prefix_0d55e4b += '// https://github.com/cxnder/imagequay | pip3 install k2l\n'
            quay_prefix_0d55e4b += f"// Platform: {_name_boundary.attributes(_name_boundary.attributes(quay_image_bab6c82)['platform'])['name']} | "
            quay_prefix_0d55e4b += f"Minimum OS: {_name_boundary.attributes(_name_boundary.attributes(quay_image_bab6c82)['minos'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_image_bab6c82)['minos'])['y']}.{_name_boundary.attributes(quay_image_bab6c82)['minos'].z} | "
            quay_prefix_0d55e4b += f"SDK: {_name_boundary.attributes(_name_boundary.attributes(quay_image_bab6c82)['sdk_version'])['x']}.{_name_boundary.attributes(_name_boundary.attributes(quay_image_bab6c82)['sdk_version'])['y']}.{_name_boundary.attributes(quay_image_bab6c82)['sdk_version'].z}\n\n"
            return quay_prefix_0d55e4b
        except AttributeError:
            quay_prefix_0d55e4b = '// Headers generated with imagequay v' + quay_IMAGEQUAY_VERSION + '\n'
            quay_prefix_0d55e4b += '// https://github.com/cxnder/imagequay | pip3 install k2l\n'
            quay_prefix_0d55e4b += '// Issue loading image metadata\n\n'
            return quay_prefix_0d55e4b

@_name_boundary.class_contract('TypeResolver', {'find_linked': 'quay_find_linked', 'objc_image': 'quay_objc_image', 'classmap': 'quay_classmap', 'classes': 'quay_classes', 'local_classes': 'quay_local_classes', 'local_protos': 'quay_local_protos', '_linked_cache': 'quay__linked_cache'})
class quay_TypeResolver:
    """
    the Type Resolver is just in charge of figuring out where imports came from.

    Initialize it with an objc image, then pass it a type name, and it'll try to figure out which
        framework that class should be imported from (utilizing the image's imports)
    """

    @_name_boundary.callable_contract({'self': 'quay_self_e0e88b9', 'objc_image': 'quay_objc_image_dbd38bb'}, '__init__')
    def __init__(quay_self_e0e88b9, quay_objc_image_dbd38bb: quay_ObjCImage):
        _name_boundary.attributes(quay_self_e0e88b9)['objc_image'] = quay_objc_image_dbd38bb
        quay_classes_883a154 = []
        _name_boundary.attributes(quay_self_e0e88b9)['classmap'] = {}
        try:
            for quay_sym_14f7d2a in _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_dbd38bb)['image'])['imports']:
                if _name_boundary.attributes(quay_sym_14f7d2a)['dec_type'] == quay_SymbolType.CLASS:
                    _name_boundary.attributes(quay_self_e0e88b9)['classmap'][_name_boundary.attributes(quay_sym_14f7d2a)['name'][1:]] = quay_sym_14f7d2a
                    quay_classes_883a154.append(quay_sym_14f7d2a)
        except AttributeError:
            pass
        _name_boundary.attributes(quay_self_e0e88b9)['classes'] = quay_classes_883a154
        _name_boundary.attributes(quay_self_e0e88b9)['local_classes'] = _name_boundary.attributes(quay_objc_image_dbd38bb)['classlist']
        _name_boundary.attributes(quay_self_e0e88b9)['local_protos'] = _name_boundary.attributes(quay_objc_image_dbd38bb)['protolist']
        _name_boundary.attributes(quay_self_e0e88b9)['_linked_cache'] = {'NSObject': '/System/Library/Frameworks/Foundation'}

    @_name_boundary.callable_contract({'self': 'quay_self_11e44d2', 'classname': 'quay_classname_a6695d5'}, 'find_linked')
    def quay_find_linked(quay_self_11e44d2, quay_classname_a6695d5: str):
        """
        given a classname, return install name of a framework if that class was imported from it.

        :param classname:
        :return:
        """
        if quay_classname_a6695d5 in _name_boundary.attributes(quay_self_11e44d2)['_linked_cache']:
            return _name_boundary.attributes(quay_self_11e44d2)['_linked_cache'][quay_classname_a6695d5]
        for quay_local_dbc5fc9 in _name_boundary.attributes(quay_self_11e44d2)['local_classes']:
            if _name_boundary.attributes(quay_local_dbc5fc9)['name'] == quay_classname_a6695d5:
                _name_boundary.attributes(quay_self_11e44d2)['_linked_cache'][quay_classname_a6695d5] = ''
                return ''
        for quay_local_dbc5fc9 in _name_boundary.attributes(quay_self_11e44d2)['local_protos']:
            if _name_boundary.attributes(quay_local_dbc5fc9)['name'] == quay_classname_a6695d5[1:-1]:
                _name_boundary.attributes(quay_self_11e44d2)['_linked_cache'][quay_classname_a6695d5] = '-Protocol'
                return '-Protocol'
        if quay_classname_a6695d5 in _name_boundary.attributes(quay_self_11e44d2)['classmap']:
            try:
                quay_name_226d047 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_11e44d2)['objc_image'])['image'])['linked_images'][int(_name_boundary.attributes(_name_boundary.attributes(quay_self_11e44d2)['classmap'][quay_classname_a6695d5])['ordinal']) - 1])['install_name']
                if '.dylib' in quay_name_226d047:
                    _name_boundary.attributes(quay_self_11e44d2)['_linked_cache'][quay_classname_a6695d5] = None
                    return None
                _name_boundary.attributes(quay_self_11e44d2)['_linked_cache'][quay_classname_a6695d5] = quay_name_226d047
                return quay_name_226d047
            except IndexError:
                pass
        _name_boundary.attributes(quay_self_11e44d2)['_linked_cache'][quay_classname_a6695d5] = None
        return None

@_name_boundary.class_contract('HeaderGenerator', {'type_resolver': 'quay_type_resolver', 'objc_image': 'quay_objc_image', 'headers': 'quay_headers'})
class quay_HeaderGenerator:

    @_name_boundary.callable_contract({'self': 'quay_self_1686152', 'objc_image': 'quay_objc_image_11c45c0', 'forward_declare_private_includes': 'quay_forward_declare_private_includes_b70be1d'}, '__init__')
    def __init__(quay_self_1686152, quay_objc_image_11c45c0: quay_ObjCImage, quay_forward_declare_private_includes_b70be1d=False):
        _name_boundary.attributes(quay_self_1686152)['type_resolver']: quay_TypeResolver = quay_TypeResolver(quay_objc_image_11c45c0)
        _name_boundary.attributes(quay_self_1686152)['objc_image']: quay_ObjCImage = quay_objc_image_11c45c0
        _name_boundary.attributes(quay_self_1686152)['headers'] = {}
        for quay_objc_class_dbe618e in _name_boundary.attributes(quay_objc_image_11c45c0)['classlist']:
            _name_boundary.attributes(quay_self_1686152)['headers'][_name_boundary.attributes(quay_objc_class_dbe618e)['name'] + '.h'] = quay_Header(_name_boundary.attributes(quay_self_1686152)['objc_image'], _name_boundary.attributes(quay_self_1686152)['type_resolver'], quay_objc_class_dbe618e, quay_forward_declare_private_includes_b70be1d)
        for quay_objc_cat_148d992 in _name_boundary.attributes(quay_objc_image_11c45c0)['catlist']:
            if _name_boundary.attributes(quay_objc_cat_148d992)['classname'] != '':
                _name_boundary.attributes(quay_self_1686152)['headers'][f"{_name_boundary.attributes(quay_objc_cat_148d992)['classname']}+{_name_boundary.attributes(quay_objc_cat_148d992)['name']}.h"] = quay_CategoryHeader(_name_boundary.attributes(quay_self_1686152)['objc_image'], quay_objc_cat_148d992)
        for quay_objc_proto_f5771ef in _name_boundary.attributes(quay_objc_image_11c45c0)['protolist']:
            _name_boundary.attributes(quay_self_1686152)['headers'][_name_boundary.attributes(quay_objc_proto_f5771ef)['name'] + '-Protocol.h'] = quay_ProtocolHeader(_name_boundary.attributes(quay_self_1686152)['objc_image'], quay_objc_proto_f5771ef)
        if _name_boundary.attributes(_name_boundary.attributes(quay_self_1686152)['objc_image'])['name'] == '':
            quay_image_name_04a6458 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_1686152)['objc_image'])['image'])['slice'])['macho_file'])['filename']
        else:
            quay_image_name_04a6458 = _name_boundary.attributes(_name_boundary.attributes(quay_self_1686152)['objc_image'])['name']
        if quay_image_name_04a6458 + '.h' in _name_boundary.attributes(quay_self_1686152)['headers']:
            _name_boundary.attributes(quay_self_1686152)['headers'][quay_image_name_04a6458 + '-Umbrella.h'] = quay_UmbrellaHeader(_name_boundary.attributes(quay_self_1686152)['headers'])
        else:
            _name_boundary.attributes(quay_self_1686152)['headers'][quay_image_name_04a6458 + '.h'] = quay_UmbrellaHeader(_name_boundary.attributes(quay_self_1686152)['headers'])
        _name_boundary.attributes(quay_self_1686152)['headers'][quay_image_name_04a6458 + '-Structs.h'] = quay_StructHeader(quay_objc_image_11c45c0)

@_name_boundary.class_contract('StructHeader', {'text': 'quay_text'})
class quay_StructHeader:

    @_name_boundary.callable_contract({'self': 'quay_self_fc1e195', 'objc_image': 'quay_objc_image_82af1b3'}, '__init__')
    def __init__(quay_self_fc1e195, quay_objc_image_82af1b3: quay_ObjCImage):
        """
        Scans through structs cached in the ObjCLib's type processor and writes them to a header

        :param objc_image: image containing structs
        """
        quay_text_eb815f9 = ''
        for quay_struct_1564961 in _name_boundary.attributes(_name_boundary.attributes(quay_objc_image_82af1b3)['tp'])['structs'].values():
            quay_text_eb815f9 += str(quay_struct_1564961) + '\n\n'
        _name_boundary.attributes(quay_self_fc1e195)['text'] = quay_text_eb815f9

    @_name_boundary.callable_contract({'self': 'quay_self_68635e8'}, '__str__')
    def __str__(quay_self_68635e8):
        return _name_boundary.attributes(quay_self_68635e8)['text']

@_name_boundary.class_contract('Header', {'generate_highlighted_text': 'quay_generate_highlighted_text', 'generate_html': 'quay_generate_html', '_generate_text': 'quay__generate_text', '_process_import_section': 'quay__process_import_section', 'interface': 'quay_interface', 'objc_image': 'quay_objc_image', 'objc_class': 'quay_objc_class', 'type_resolver': 'quay_type_resolver', 'forward_declare_private_imports': 'quay_forward_declare_private_imports', 'forward_declaration_classes': 'quay_forward_declaration_classes', 'forward_declaration_protocols': 'quay_forward_declaration_protocols', 'imported_classes': 'quay_imported_classes', 'locally_imported_classes': 'quay_locally_imported_classes', 'locally_imported_protocols': 'quay_locally_imported_protocols', 'text': 'quay_text', 'highlighted_text': 'quay_highlighted_text'})
class quay_Header:

    @_name_boundary.callable_contract({'self': 'quay_self_2867888', 'objc_image': 'quay_objc_image_7ec0640', 'type_resolver': 'quay_type_resolver_d898732', 'objc_class': 'quay_objc_class_1e19802', 'forward_declare_private_imports': 'quay_forward_declare_private_imports_3d2cb5f'}, '__init__')
    def __init__(quay_self_2867888, quay_objc_image_7ec0640: 'ObjCImage', quay_type_resolver_d898732, quay_objc_class_1e19802: quay_Class, quay_forward_declare_private_imports_3d2cb5f):
        _name_boundary.attributes(quay_self_2867888)['interface']: quay_Interface = quay_Interface(quay_objc_class_1e19802)
        _name_boundary.attributes(quay_self_2867888)['objc_image'] = quay_objc_image_7ec0640
        _name_boundary.attributes(quay_self_2867888)['objc_class']: quay_Class = quay_objc_class_1e19802
        _name_boundary.attributes(quay_self_2867888)['type_resolver']: quay_TypeResolver = quay_type_resolver_d898732
        _name_boundary.attributes(quay_self_2867888)['forward_declare_private_imports'] = quay_forward_declare_private_imports_3d2cb5f
        _name_boundary.attributes(quay_self_2867888)['forward_declaration_classes']: quay_List[str] = []
        _name_boundary.attributes(quay_self_2867888)['forward_declaration_protocols']: quay_List[str] = []
        _name_boundary.attributes(quay_self_2867888)['imported_classes']: quay_Dict[str, str] = {}
        _name_boundary.attributes(quay_self_2867888)['locally_imported_classes']: quay_List[str] = []
        _name_boundary.attributes(quay_self_2867888)['locally_imported_protocols']: quay_List[str] = []
        _name_boundary.attributes(quay_self_2867888)['_process_import_section']()
        _name_boundary.attributes(quay_self_2867888)['text'] = _name_boundary.attributes(quay_self_2867888)['_generate_text']()
        _name_boundary.attributes(quay_self_2867888)['highlighted_text'] = None

    @_name_boundary.callable_contract({'self': 'quay_self_0ed7aab'}, '__str__')
    def __str__(quay_self_0ed7aab):
        return _name_boundary.attributes(quay_self_0ed7aab)['text']

    @_name_boundary.callable_contract({'self': 'quay_self_0a2879c'}, 'generate_highlighted_text')
    def quay_generate_highlighted_text(quay_self_0a2879c):
        if quay_ObjectiveCLexer is None:
            return _name_boundary.attributes(quay_self_0a2879c)['text']
        if _name_boundary.attributes(quay_self_0a2879c)['highlighted_text']:
            return _name_boundary.attributes(quay_self_0a2879c)['highlighted_text']
        quay_formatter_1289e48 = quay_TerminalFormatter()
        _name_boundary.attributes(quay_self_0a2879c)['highlighted_text'] = quay_highlight(_name_boundary.attributes(quay_self_0a2879c)['text'], quay_ObjectiveCLexer(), quay_formatter_1289e48)
        return _name_boundary.attributes(quay_self_0a2879c)['highlighted_text']

    @_name_boundary.callable_contract({'self': 'quay_self_eed2a6b', 'generate_address_links': 'quay_generate_address_links_181cd93'}, 'generate_html')
    def quay_generate_html(quay_self_eed2a6b, quay_generate_address_links_181cd93=False):
        quay_text_d4171ac = [_name_boundary.attributes(quay_HeaderUtils)['header_head_html'](_name_boundary.attributes(_name_boundary.attributes(quay_self_eed2a6b)['objc_image'])['image'])]
        for quay_i_e117693 in _name_boundary.attributes(_name_boundary.attributes(quay_self_eed2a6b)['objc_class'])['load_errors']:
            quay_text_d4171ac.append(f'<span class="c1">// err: {quay_i_e117693}</span>')
        if len(_name_boundary.attributes(_name_boundary.attributes(quay_self_eed2a6b)['objc_class'])['load_errors']) > 0:
            quay_text_d4171ac.append('')
        if len(_name_boundary.attributes(quay_self_eed2a6b)['forward_declaration_classes']) > 0:
            quay_text_d4171ac.append(f'<span class="k">@class</span> ' + ', '.join(_name_boundary.attributes(quay_self_eed2a6b)['forward_declaration_classes']) + ';')
        if len(_name_boundary.attributes(quay_self_eed2a6b)['forward_declaration_protocols']) > 0:
            quay_text_d4171ac.append(f'<span class="k">@protocol</span> ' + ', '.join(_name_boundary.attributes(quay_self_eed2a6b)['forward_declaration_protocols']) + ';')
        quay_text_d4171ac.append('')
        quay_imported_classes_4342261 = {}
        for quay_objc_class_2f42d91, quay_install_name_60e310b in _name_boundary.attributes(_name_boundary.attributes(quay_self_eed2a6b)['imported_classes'])['items']():
            if '/Frameworks/' in quay_install_name_60e310b:
                quay_nam_eded4c7 = quay_install_name_60e310b.split('/')[-1]
                if quay_nam_eded4c7 not in quay_imported_classes_4342261:
                    quay_imported_classes_4342261[quay_nam_eded4c7] = quay_nam_eded4c7
            elif _name_boundary.attributes(quay_self_eed2a6b)['forward_declare_private_imports']:
                quay_text_d4171ac.append(f'<span class="k">@class</span> {quay_objc_class_2f42d91};')
            else:
                quay_imported_classes_4342261[quay_objc_class_2f42d91] = quay_install_name_60e310b
        for quay_objc_class_2f42d91, quay_install_name_60e310b in _name_boundary.attributes(quay_imported_classes_4342261)['items']():
            quay_text_d4171ac.append(f"""<span class="k">#import</span> &lt;{quay_install_name_60e310b.split('/')[-1]}/{quay_objc_class_2f42d91}.h&gt;""")
        quay_text_d4171ac.append('')
        if _name_boundary.attributes(quay_self_eed2a6b)['forward_declare_private_imports']:
            for quay_objc_class_2f42d91 in _name_boundary.attributes(quay_self_eed2a6b)['locally_imported_classes']:
                quay_text_d4171ac.append(f'<span class="k">@class</span> {quay_objc_class_2f42d91};')
            for quay_objc_protocol_56728f2 in _name_boundary.attributes(quay_self_eed2a6b)['locally_imported_protocols']:
                quay_text_d4171ac.append(f'<span class="k">@protocol</span> {quay_objc_protocol_56728f2};')
        else:
            for quay_objc_class_2f42d91 in _name_boundary.attributes(quay_self_eed2a6b)['locally_imported_classes']:
                quay_objc_class_text_e03c118 = f'&quot;{quay_objc_class_2f42d91}.h&quot;'
                quay_text_d4171ac.append(f'<span class="cp">#import {quay_objc_class_text_e03c118}</span>')
            for quay_objc_protocol_56728f2 in _name_boundary.attributes(quay_self_eed2a6b)['locally_imported_protocols']:
                quay_objc_proto_text_5a72125 = f'&quot;{quay_objc_protocol_56728f2}-Protocol.h&quot;'
                quay_text_d4171ac.append(f'<span class="cp">#import {quay_objc_proto_text_5a72125}</span>')
        quay_text_d4171ac.append('')
        quay_text_d4171ac.append(_name_boundary.attributes(_name_boundary.attributes(quay_self_eed2a6b)['interface'])['generate_html'](quay_generate_address_links_181cd93))
        quay_text_d4171ac.append('')
        return '\n'.join(quay_text_d4171ac)

    @_name_boundary.callable_contract({'self': 'quay_self_eab588e'}, '_generate_text')
    def quay__generate_text(quay_self_eab588e) -> str:
        """
        Generates the header text based on the processed and configured properties

        :return: the header text
        """
        quay_text_0ecf580 = [_name_boundary.attributes(quay_HeaderUtils)['header_head'](_name_boundary.attributes(_name_boundary.attributes(quay_self_eab588e)['objc_image'])['image']), '#ifndef ' + _name_boundary.attributes(_name_boundary.attributes(quay_self_eab588e)['objc_class'])['name'].upper() + '_H', '#define ' + _name_boundary.attributes(_name_boundary.attributes(quay_self_eab588e)['objc_class'])['name'].upper() + '_H', '']
        for quay_i_4da0ca3 in _name_boundary.attributes(_name_boundary.attributes(quay_self_eab588e)['objc_class'])['load_errors']:
            quay_text_0ecf580.append(f'// {quay_i_4da0ca3}')
        if len(_name_boundary.attributes(_name_boundary.attributes(quay_self_eab588e)['objc_class'])['load_errors']) > 0:
            quay_text_0ecf580.append('')
        if len(_name_boundary.attributes(quay_self_eab588e)['forward_declaration_classes']) > 0:
            quay_text_0ecf580.append('@class ' + ', '.join(_name_boundary.attributes(quay_self_eab588e)['forward_declaration_classes']) + ';')
        if len(_name_boundary.attributes(quay_self_eab588e)['forward_declaration_protocols']) > 0:
            quay_text_0ecf580.append('@protocol ' + ', '.join(_name_boundary.attributes(quay_self_eab588e)['forward_declaration_protocols']) + ';')
        quay_text_0ecf580.append('')
        quay_imported_classes_d0685a0 = {}
        for quay_objc_class_eb48187, quay_install_name_b5fe808 in _name_boundary.attributes(_name_boundary.attributes(quay_self_eab588e)['imported_classes'])['items']():
            if '/Frameworks/' in quay_install_name_b5fe808:
                quay_nam_f3ce895 = quay_install_name_b5fe808.split('/')[-1]
                if quay_nam_f3ce895 not in quay_imported_classes_d0685a0:
                    quay_imported_classes_d0685a0[quay_nam_f3ce895] = quay_nam_f3ce895
            elif _name_boundary.attributes(quay_self_eab588e)['forward_declare_private_imports']:
                quay_text_0ecf580.append(f'@class {quay_objc_class_eb48187};')
            else:
                quay_imported_classes_d0685a0[quay_objc_class_eb48187] = quay_install_name_b5fe808
        for quay_objc_class_eb48187, quay_install_name_b5fe808 in _name_boundary.attributes(quay_imported_classes_d0685a0)['items']():
            quay_text_0ecf580.append(f"#import <{quay_install_name_b5fe808.split('/')[-1]}/{quay_objc_class_eb48187}.h>")
        quay_text_0ecf580.append('')
        if _name_boundary.attributes(quay_self_eab588e)['forward_declare_private_imports']:
            for quay_objc_class_eb48187 in _name_boundary.attributes(quay_self_eab588e)['locally_imported_classes']:
                quay_text_0ecf580.append(f'@class {quay_objc_class_eb48187};')
            for quay_objc_protocol_88f1f5d in _name_boundary.attributes(quay_self_eab588e)['locally_imported_protocols']:
                quay_text_0ecf580.append(f'@protocol {quay_objc_protocol_88f1f5d};')
        else:
            for quay_objc_class_eb48187 in _name_boundary.attributes(quay_self_eab588e)['locally_imported_classes']:
                quay_text_0ecf580.append(f'#import "{quay_objc_class_eb48187}.h"')
            for quay_objc_protocol_88f1f5d in _name_boundary.attributes(quay_self_eab588e)['locally_imported_protocols']:
                quay_text_0ecf580.append(f'#import "{quay_objc_protocol_88f1f5d}-Protocol.h"')
        quay_text_0ecf580.append('')
        quay_text_0ecf580.append(str(_name_boundary.attributes(quay_self_eab588e)['interface']))
        quay_text_0ecf580.append('')
        quay_text_0ecf580.append('')
        quay_text_0ecf580.append('#endif')
        return '\n'.join(quay_text_0ecf580)

    @_name_boundary.callable_contract({'self': 'quay_self_d3f7c07'}, '_process_import_section')
    def quay__process_import_section(quay_self_d3f7c07):
        if _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_d3f7c07)['interface'])['objc_class'])['superclass'] != '':
            quay_type_name_a67a5a9 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_d3f7c07)['interface'])['objc_class'])['superclass'].split('_')[-1]
            quay_resolved_type_df1bd2d = _name_boundary.attributes(_name_boundary.attributes(quay_self_d3f7c07)['type_resolver'])['find_linked'](quay_type_name_a67a5a9)
            if quay_resolved_type_df1bd2d is None:
                if quay_type_name_a67a5a9 != 'id':
                    if quay_type_name_a67a5a9.startswith('<'):
                        if quay_type_name_a67a5a9[1:-1] not in _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols']:
                            _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols'].append(quay_type_name_a67a5a9[1:-1])
                    elif quay_type_name_a67a5a9.startswith('NSObject<'):
                        if quay_type_name_a67a5a9[9:-1] not in _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols']:
                            _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols'].append(quay_type_name_a67a5a9[9:-1])
                    elif quay_type_name_a67a5a9 not in _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_classes']:
                        _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_classes'].append(quay_type_name_a67a5a9)
            elif quay_resolved_type_df1bd2d == '':
                if quay_type_name_a67a5a9 not in _name_boundary.attributes(quay_self_d3f7c07)['locally_imported_classes']:
                    _name_boundary.attributes(quay_self_d3f7c07)['locally_imported_classes'].append(quay_type_name_a67a5a9)
            elif quay_type_name_a67a5a9 not in _name_boundary.attributes(quay_self_d3f7c07)['imported_classes']:
                _name_boundary.attributes(quay_self_d3f7c07)['imported_classes'][quay_type_name_a67a5a9] = quay_resolved_type_df1bd2d
        for quay_protocol_3f7112b in _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_d3f7c07)['interface'])['objc_class'])['protocols']:
            quay_type_name_a67a5a9 = f"<{_name_boundary.attributes(quay_protocol_3f7112b)['name']}>"
            quay_resolved_type_df1bd2d = _name_boundary.attributes(_name_boundary.attributes(quay_self_d3f7c07)['type_resolver'])['find_linked'](quay_type_name_a67a5a9)
            if quay_resolved_type_df1bd2d == '-Protocol':
                _name_boundary.attributes(quay_self_d3f7c07)['locally_imported_protocols'].append(_name_boundary.attributes(quay_protocol_3f7112b)['name'])
            else:
                _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols'].append(_name_boundary.attributes(quay_protocol_3f7112b)['name'])
        for quay_ivar_f9af654 in _name_boundary.attributes(_name_boundary.attributes(quay_self_d3f7c07)['interface'])['ivars']:
            if _name_boundary.attributes(quay_ivar_f9af654)['is_id']:
                quay_type_name_a67a5a9 = _name_boundary.attributes(quay_ivar_f9af654)['type']
                quay_resolved_type_df1bd2d = _name_boundary.attributes(_name_boundary.attributes(quay_self_d3f7c07)['type_resolver'])['find_linked'](quay_type_name_a67a5a9)
                if quay_resolved_type_df1bd2d is None:
                    if quay_type_name_a67a5a9 != 'id':
                        if quay_type_name_a67a5a9.startswith('<'):
                            if quay_type_name_a67a5a9[1:-1] not in _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols']:
                                _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols'].append(quay_type_name_a67a5a9[1:-1])
                        elif quay_type_name_a67a5a9.startswith('NSObject<'):
                            if quay_type_name_a67a5a9[9:-1] not in _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols']:
                                _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols'].append(quay_type_name_a67a5a9[9:-1])
                        elif quay_type_name_a67a5a9 not in _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_classes']:
                            _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_classes'].append(quay_type_name_a67a5a9)
                elif quay_resolved_type_df1bd2d == '':
                    if quay_type_name_a67a5a9 not in _name_boundary.attributes(quay_self_d3f7c07)['locally_imported_classes']:
                        _name_boundary.attributes(quay_self_d3f7c07)['locally_imported_classes'].append(quay_type_name_a67a5a9)
                elif quay_resolved_type_df1bd2d == '-Protocol':
                    if quay_type_name_a67a5a9 not in _name_boundary.attributes(quay_self_d3f7c07)['locally_imported_protocols']:
                        _name_boundary.attributes(quay_self_d3f7c07)['locally_imported_protocols'].append(quay_type_name_a67a5a9[1:-1])
                elif quay_type_name_a67a5a9 not in _name_boundary.attributes(quay_self_d3f7c07)['imported_classes']:
                    _name_boundary.attributes(quay_self_d3f7c07)['imported_classes'][quay_type_name_a67a5a9] = quay_resolved_type_df1bd2d
        for quay_objc_property_dd32518 in _name_boundary.attributes(_name_boundary.attributes(quay_self_d3f7c07)['interface'])['properties']:
            if _name_boundary.attributes(quay_objc_property_dd32518)['is_id']:
                quay_type_name_a67a5a9 = _name_boundary.attributes(quay_objc_property_dd32518)['type']
                quay_resolved_type_df1bd2d = _name_boundary.attributes(_name_boundary.attributes(quay_self_d3f7c07)['type_resolver'])['find_linked'](quay_type_name_a67a5a9)
                if quay_resolved_type_df1bd2d is None:
                    if quay_type_name_a67a5a9 != 'id':
                        if quay_type_name_a67a5a9.startswith('<'):
                            if quay_type_name_a67a5a9[1:-1] not in _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols']:
                                _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols'].append(quay_type_name_a67a5a9[1:-1])
                        elif quay_type_name_a67a5a9.startswith('NSObject<'):
                            if quay_type_name_a67a5a9[9:-1] not in _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols']:
                                _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_protocols'].append(quay_type_name_a67a5a9[9:-1])
                        elif quay_type_name_a67a5a9 not in _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_classes']:
                            _name_boundary.attributes(quay_self_d3f7c07)['forward_declaration_classes'].append(quay_type_name_a67a5a9)
                elif quay_resolved_type_df1bd2d == '':
                    if quay_type_name_a67a5a9 not in _name_boundary.attributes(quay_self_d3f7c07)['locally_imported_classes']:
                        _name_boundary.attributes(quay_self_d3f7c07)['locally_imported_classes'].append(quay_type_name_a67a5a9)
                elif quay_resolved_type_df1bd2d == '-Protocol':
                    if quay_type_name_a67a5a9 not in _name_boundary.attributes(quay_self_d3f7c07)['locally_imported_protocols']:
                        _name_boundary.attributes(quay_self_d3f7c07)['locally_imported_protocols'].append(quay_type_name_a67a5a9[1:-1])
                elif quay_type_name_a67a5a9 not in _name_boundary.attributes(quay_self_d3f7c07)['imported_classes']:
                    _name_boundary.attributes(quay_self_d3f7c07)['imported_classes'][quay_type_name_a67a5a9] = quay_resolved_type_df1bd2d

@_name_boundary.class_contract('CategoryHeader', {'_generate_text': 'quay__generate_text', 'objc_image': 'quay_objc_image', 'category': 'quay_category', 'properties': 'quay_properties', 'methods': 'quay_methods', 'protocols': 'quay_protocols', 'interface': 'quay_interface', 'text': 'quay_text'})
class quay_CategoryHeader:

    @_name_boundary.callable_contract({'self': 'quay_self_940ac17', 'objc_image': 'quay_objc_image_0aba9f7', 'objc_category': 'quay_objc_category_f3b6a4b'}, '__init__')
    def __init__(quay_self_940ac17, quay_objc_image_0aba9f7, quay_objc_category_f3b6a4b: quay_Category):
        _name_boundary.attributes(quay_self_940ac17)['objc_image'] = quay_objc_image_0aba9f7
        _name_boundary.attributes(quay_self_940ac17)['category'] = quay_objc_category_f3b6a4b
        _name_boundary.attributes(quay_self_940ac17)['properties'] = _name_boundary.attributes(quay_objc_category_f3b6a4b)['properties']
        _name_boundary.attributes(quay_self_940ac17)['methods'] = _name_boundary.attributes(quay_objc_category_f3b6a4b)['methods']
        _name_boundary.attributes(quay_self_940ac17)['protocols'] = _name_boundary.attributes(quay_objc_category_f3b6a4b)['protocols']
        _name_boundary.attributes(quay_self_940ac17)['interface'] = quay_CategoryInterface(quay_objc_category_f3b6a4b)
        _name_boundary.attributes(quay_self_940ac17)['text'] = _name_boundary.attributes(quay_self_940ac17)['_generate_text']()

    @_name_boundary.callable_contract({'self': 'quay_self_dc1fa07'}, '__str__')
    def __str__(quay_self_dc1fa07):
        return _name_boundary.attributes(quay_self_dc1fa07)['text']

    @_name_boundary.callable_contract({'self': 'quay_self_f213f6d'}, '_generate_text')
    def quay__generate_text(quay_self_f213f6d):
        """
        Generate Category text

        :return: category text
        """
        quay_text_4262cb0 = [_name_boundary.attributes(quay_HeaderUtils)['header_head'](_name_boundary.attributes(_name_boundary.attributes(quay_self_f213f6d)['objc_image'])['image']), '', str(_name_boundary.attributes(quay_self_f213f6d)['interface']), '', '']
        return '\n'.join(quay_text_4262cb0)

@_name_boundary.class_contract('ProtocolHeader', {'_generate_text': 'quay__generate_text', 'objc_image': 'quay_objc_image', 'protocol': 'quay_protocol', 'interface': 'quay_interface', 'text': 'quay_text'})
class quay_ProtocolHeader:

    @_name_boundary.callable_contract({'self': 'quay_self_9703fb8', 'objc_image': 'quay_objc_image_e68fce4', 'objc_protocol': 'quay_objc_protocol_f656dd0'}, '__init__')
    def __init__(quay_self_9703fb8, quay_objc_image_e68fce4, quay_objc_protocol_f656dd0: quay_Protocol):
        _name_boundary.attributes(quay_self_9703fb8)['objc_image'] = quay_objc_image_e68fce4
        _name_boundary.attributes(quay_self_9703fb8)['protocol']: quay_Protocol = quay_objc_protocol_f656dd0
        _name_boundary.attributes(quay_self_9703fb8)['interface'] = quay_ProtocolInterface(quay_objc_protocol_f656dd0)
        _name_boundary.attributes(quay_self_9703fb8)['text'] = _name_boundary.attributes(quay_self_9703fb8)['_generate_text']()

    @_name_boundary.callable_contract({'self': 'quay_self_3b67558'}, '__str__')
    def __str__(quay_self_3b67558):
        return _name_boundary.attributes(quay_self_3b67558)['text']

    @_name_boundary.callable_contract({'self': 'quay_self_de00df6'}, '_generate_text')
    def quay__generate_text(quay_self_de00df6):
        """
        Generate Protocol Header text

        :return:
        """
        quay_text_be4a3c3 = [_name_boundary.attributes(quay_HeaderUtils)['header_head'](_name_boundary.attributes(_name_boundary.attributes(quay_self_de00df6)['objc_image'])['image']), '', str(_name_boundary.attributes(quay_self_de00df6)['interface']), '', '']
        return '\n'.join(quay_text_be4a3c3)

@_name_boundary.class_contract('Interface', {'generate_html': 'quay_generate_html', '_process_properties': 'quay__process_properties', '_process_ivars': 'quay__process_ivars', '_process_methods': 'quay__process_methods', 'objc_class': 'quay_objc_class', 'properties': 'quay_properties', 'methods': 'quay_methods', 'ivars': 'quay_ivars', 'structs': 'quay_structs', 'getters': 'quay_getters', 'setters': 'quay_setters'})
class quay_Interface:
    """
    The Interface class represents the "main body" of the header (not including the import section)

    """

    @_name_boundary.callable_contract({'self': 'quay_self_12f3b1c', 'objc_class': 'quay_objc_class_67f35a7'}, '__init__')
    def __init__(quay_self_12f3b1c, quay_objc_class_67f35a7: quay_Class):
        _name_boundary.attributes(quay_self_12f3b1c)['objc_class'] = quay_objc_class_67f35a7
        _name_boundary.attributes(quay_self_12f3b1c)['properties']: quay_List[quay_Property] = []
        _name_boundary.attributes(quay_self_12f3b1c)['methods']: quay_List[quay_Method] = []
        _name_boundary.attributes(quay_self_12f3b1c)['ivars']: quay_List[quay_Ivar] = []
        _name_boundary.attributes(quay_self_12f3b1c)['structs'] = []
        _name_boundary.attributes(quay_self_12f3b1c)['getters']: quay_List[str] = []
        _name_boundary.attributes(quay_self_12f3b1c)['setters']: quay_List[str] = []
        _name_boundary.attributes(quay_self_12f3b1c)['_process_properties']()
        _name_boundary.attributes(quay_self_12f3b1c)['_process_methods']()
        _name_boundary.attributes(quay_self_12f3b1c)['_process_ivars']()

    @_name_boundary.callable_contract({'self': 'quay_self_cc51158', 'generate_address_links': 'quay_generate_address_links_a838094'}, 'generate_html')
    def quay_generate_html(quay_self_cc51158, quay_generate_address_links_a838094=False):
        if quay_generate_address_links_a838094:
            quay_head_f1410ff = f"""<span class="k">@interface</span> <span class="k"><a href="addr/{_name_boundary.attributes(_name_boundary.attributes(quay_self_cc51158)['objc_class'])['loc']}">{_name_boundary.attributes(_name_boundary.attributes(quay_self_cc51158)['objc_class'])['name']}</a></span>"""
        else:
            quay_head_f1410ff = f"""<span class="k">@interface</span> <span class="k">{_name_boundary.attributes(_name_boundary.attributes(quay_self_cc51158)['objc_class'])['name']}</span>"""
        quay_superclass_9357ae1 = 'NSObject'
        if _name_boundary.attributes(_name_boundary.attributes(quay_self_cc51158)['objc_class'])['superclass'] != '':
            quay_superclass_9357ae1 = _name_boundary.attributes(_name_boundary.attributes(quay_self_cc51158)['objc_class'])['superclass'].split('_')[-1]
        quay_head_f1410ff += f' : <span class="bp">{quay_superclass_9357ae1}</span>'
        if len(_name_boundary.attributes(_name_boundary.attributes(quay_self_cc51158)['objc_class'])['protocols']) > 0:
            quay_head_f1410ff += '<span class="o">&lt;</span>'
            for quay_protocol_cd53cae in _name_boundary.attributes(_name_boundary.attributes(quay_self_cc51158)['objc_class'])['protocols']:
                quay_head_f1410ff += f'<span class="n">{quay_protocol_cd53cae}</span><span class="p">,</span> '
            quay_head_f1410ff = quay_head_f1410ff[:-len('<span class="p">,</span> ')]
            quay_head_f1410ff += '<span class="o">&gt;</span>'
        quay_ivars_36b04ce = ''
        if len(_name_boundary.attributes(quay_self_cc51158)['ivars']) > 0:
            quay_ivars_36b04ce = "<span class='o'>{</span>\n"
            for quay_ivar_2105d9c in _name_boundary.attributes(quay_self_cc51158)['ivars']:
                quay_ptr_count_15e458a = _name_boundary.attributes(_name_boundary.attributes(quay_ivar_2105d9c)['type'])['count']('*')
                quay_type_text_42bb28a = _name_boundary.attributes(quay_ivar_2105d9c)['type'].replace('*', '')
                if quay_generate_address_links_a838094:
                    quay_type_text_42bb28a = f'<a href="type/{quay_type_text_42bb28a}">{quay_type_text_42bb28a}</a>'
                quay_ivars_36b04ce += f'\t<span class="bp">{quay_type_text_42bb28a}</span>'
                for quay_i_b598fd5 in range(quay_ptr_count_15e458a):
                    quay_ivars_36b04ce += '<span class="o">*</span>'
                quay_ivar_name_fd7259a = _name_boundary.attributes(quay_ivar_2105d9c)['name']
                if quay_generate_address_links_a838094:
                    quay_ivar_name_fd7259a = f"""<a href="ivar/{_name_boundary.attributes(_name_boundary.attributes(quay_self_cc51158)['objc_class'])['name']}/{quay_ivar_name_fd7259a}">{quay_ivar_name_fd7259a}</a>"""
                quay_ivars_36b04ce += f' <span class="n">{quay_ivar_name_fd7259a}</span><span class="p">;</span>\n'
            quay_ivars_36b04ce += '<span class="o">}</span>'
        quay_props_02d002c = ''
        for quay_prop_98f3a88 in _name_boundary.attributes(quay_self_cc51158)['properties']:
            quay_props_02d002c += f'<span class="k">@property</span> '
            if len(_name_boundary.attributes(quay_prop_98f3a88)['attributes']):
                quay_props_02d002c += '<span class="p">(</span>'
                for quay_attr_459e9a0 in _name_boundary.attributes(quay_prop_98f3a88)['attributes']:
                    quay_props_02d002c += f'<span class="p">{quay_attr_459e9a0}</span>, '
                quay_props_02d002c = quay_props_02d002c[:-2]
                quay_props_02d002c += '<span class="k">)</span> '
            quay_prop_type_a825b51 = _name_boundary.attributes(quay_prop_98f3a88)['type']
            if quay_generate_address_links_a838094:
                quay_prop_type_a825b51 = f'<a href="type/{quay_prop_type_a825b51}">{quay_prop_type_a825b51}</a>'
            quay_props_02d002c += f'<span class="bp">{quay_prop_type_a825b51}</span> '
            for quay_i_b598fd5 in range(_name_boundary.attributes(_name_boundary.attributes(quay_prop_98f3a88)['type'])['count']('*')):
                quay_props_02d002c += '<span class="o">*</span>'
            if _name_boundary.attributes(quay_prop_98f3a88)['is_id']:
                quay_props_02d002c += '<span class="o">*</span>'
            quay_props_02d002c += f"""<span class="n">{_name_boundary.attributes(quay_prop_98f3a88)['name']}</span><span class="p">;</span>"""
            if quay_generate_address_links_a838094 or _name_boundary.attributes(quay_prop_98f3a88)['ivarname'] != '':
                quay_props_02d002c += '<span class="c1"> // '
            if quay_generate_address_links_a838094:
                quay_getter_5aaeb88 = _name_boundary.attributes(_name_boundary.attributes(quay_prop_98f3a88)['attr'])['getter']
                if quay_getter_5aaeb88 == '' or quay_getter_5aaeb88 is None:
                    quay_getter_5aaeb88 = _name_boundary.attributes(quay_prop_98f3a88)['name']
                quay_setter_61347d9 = _name_boundary.attributes(_name_boundary.attributes(quay_prop_98f3a88)['attr'])['setter']
                if quay_setter_61347d9 == '' or quay_setter_61347d9 is None:
                    quay_setter_61347d9 = f"set{_name_boundary.attributes(quay_prop_98f3a88)['name'][0].upper()}{_name_boundary.attributes(quay_prop_98f3a88)['name'][1:]}:"
                quay_getter_5aaeb88 = f"""<a href="meth/{_name_boundary.attributes(_name_boundary.attributes(quay_self_cc51158)['objc_class'])['name']}/{quay_getter_5aaeb88}">Getter</a>"""
                quay_setter_61347d9 = f"""<a href="meth/{_name_boundary.attributes(_name_boundary.attributes(quay_self_cc51158)['objc_class'])['name']}/{quay_setter_61347d9}">Setter</a>"""
                quay_props_02d002c += f'{quay_getter_5aaeb88} | '
                if 'readonly' not in _name_boundary.attributes(quay_prop_98f3a88)['attributes']:
                    quay_props_02d002c += f'{quay_setter_61347d9} | '
            if _name_boundary.attributes(quay_prop_98f3a88)['ivarname'] != '':
                quay_ivarname_1350908 = _name_boundary.attributes(quay_prop_98f3a88)['ivarname']
                if quay_generate_address_links_a838094:
                    quay_ivarname_1350908 = f"""<a href="ivar/{_name_boundary.attributes(_name_boundary.attributes(quay_self_cc51158)['objc_class'])['name']}/{quay_ivarname_1350908}">{quay_ivarname_1350908}</a>"""
                quay_props_02d002c += f' ivar: {quay_ivarname_1350908}'
            else:
                quay_props_02d002c = quay_props_02d002c[:-3]
            if quay_generate_address_links_a838094 or _name_boundary.attributes(quay_prop_98f3a88)['ivarname'] != '':
                quay_props_02d002c += '</span>'
            quay_props_02d002c += '\n'
        quay_meths_f1cd4cb = ''
        for quay_meth_19937ad in _name_boundary.attributes(quay_self_cc51158)['methods']:
            if _name_boundary.attributes(quay_meth_19937ad)['sel'].strip() != '':
                quay_meths_f1cd4cb += f"""<span class="p">{('+' if _name_boundary.attributes(quay_meth_19937ad)['meta'] else '-')}</span> """
                quay_meths_f1cd4cb += f'<span class="p">(</span>'
                quay_meths_f1cd4cb += f"""<span class="p">{_name_boundary.attributes(quay_meth_19937ad)['return_string']}</span>"""
                quay_meths_f1cd4cb += f'<span class="p">)</span> '
                if quay_generate_address_links_a838094:
                    quay_meths_f1cd4cb += f"""<a href="addr/{_name_boundary.attributes(quay_meth_19937ad)['imp']}">"""
                if len(_name_boundary.attributes(quay_meth_19937ad)['arguments']) == 0:
                    quay_meths_f1cd4cb += f"""<span class="nf">{_name_boundary.attributes(quay_meth_19937ad)['sel']}</span> """
                else:
                    quay_segments_7ea8c12 = []
                    for quay_i_b598fd5, quay_item_7b91c05 in enumerate(_name_boundary.attributes(quay_meth_19937ad)['sel'].split(':')):
                        if quay_item_7b91c05 == '':
                            continue
                        try:
                            quay_segments_7ea8c12.append(f'<span class="nf">{quay_item_7b91c05}:</span>' + '<span class="p">(</span>' + f"""<span class="nv">{_name_boundary.attributes(quay_meth_19937ad)['arguments'][quay_i_b598fd5 + 2]}</span>""" + '<span class="p">)</span>' + 'arg' + str(quay_i_b598fd5) + ' ')
                        except IndexError:
                            quay_segments_7ea8c12.append(quay_item_7b91c05)
                    quay_sig_e06ff0c = ''.join(quay_segments_7ea8c12)
                    quay_meths_f1cd4cb += quay_sig_e06ff0c
                quay_meths_f1cd4cb += f'<span class="p">;</span>\n'
                if quay_generate_address_links_a838094:
                    quay_meths_f1cd4cb += '</a>'
        quay_foot_8b573cc = "<span class='k'>@end</span>"
        return '\n'.join([quay_head_f1410ff, quay_ivars_36b04ce, quay_props_02d002c, quay_meths_f1cd4cb, quay_foot_8b573cc])

    @_name_boundary.callable_contract({'self': 'quay_self_6e89398'}, '__str__')
    def __str__(quay_self_6e89398):
        quay_head_50b5c95 = '@interface ' + _name_boundary.attributes(_name_boundary.attributes(quay_self_6e89398)['objc_class'])['name'] + ' : '
        quay_superclass_6fb53d7 = 'NSObject'
        if _name_boundary.attributes(_name_boundary.attributes(quay_self_6e89398)['objc_class'])['superclass'] != '':
            quay_superclass_6fb53d7 = _name_boundary.attributes(_name_boundary.attributes(quay_self_6e89398)['objc_class'])['superclass'].split('_')[-1]
        quay_head_50b5c95 += quay_superclass_6fb53d7
        if len(_name_boundary.attributes(_name_boundary.attributes(quay_self_6e89398)['objc_class'])['protocols']) > 0:
            quay_head_50b5c95 += ' <'
            for quay_protocol_a9a1670 in _name_boundary.attributes(_name_boundary.attributes(quay_self_6e89398)['objc_class'])['protocols']:
                quay_head_50b5c95 += str(quay_protocol_a9a1670) + ', '
            quay_head_50b5c95 = quay_head_50b5c95[:-2]
            quay_head_50b5c95 += '>\n\n'
        quay_ivars_8b3de63 = ''
        if len(_name_boundary.attributes(quay_self_6e89398)['ivars']) > 0:
            quay_ivars_8b3de63 = ' {\n'
            for quay_ivar_9f7eeac in _name_boundary.attributes(quay_self_6e89398)['ivars']:
                quay_ivars_8b3de63 += '    ' + str(quay_ivar_9f7eeac) + ';\n'
            quay_ivars_8b3de63 += '}\n'
        quay_props_fd0ccc9 = '\n\n'
        for quay_prop_498ce70 in _name_boundary.attributes(quay_self_6e89398)['properties']:
            quay_props_fd0ccc9 += str(quay_prop_498ce70) + ';'
            if _name_boundary.attributes(quay_prop_498ce70)['ivarname'] != '':
                quay_props_fd0ccc9 += ' // ivar: ' + _name_boundary.attributes(quay_prop_498ce70)['ivarname'] + '\n'
            else:
                quay_props_fd0ccc9 += '\n'
        quay_meths_01c9110 = '\n\n'
        for quay_i_cd5cb31 in _name_boundary.attributes(quay_self_6e89398)['methods']:
            if _name_boundary.attributes(quay_i_cd5cb31)['sel'].strip() != '':
                if '(unk)' in str(quay_i_cd5cb31):
                    quay_meths_01c9110 += f'// {str(quay_i_cd5cb31)} ;\n'
                elif '.cxx_' not in str(quay_i_cd5cb31):
                    quay_meths_01c9110 += str(quay_i_cd5cb31) + ';\n'
        quay_foot_3e87a20 = '\n\n@end'
        return quay_head_50b5c95 + quay_ivars_8b3de63 + quay_props_fd0ccc9 + quay_meths_01c9110 + quay_foot_3e87a20

    @_name_boundary.callable_contract({'self': 'quay_self_932ed44'}, '_process_properties')
    def quay__process_properties(quay_self_932ed44):
        for quay_objc_property_8eef248 in _name_boundary.attributes(_name_boundary.attributes(quay_self_932ed44)['objc_class'])['properties']:
            if not _name_boundary.has_attribute(quay_objc_property_8eef248, 'type'):
                continue
            _name_boundary.attributes(quay_self_932ed44)['getters'].append(_name_boundary.attributes(quay_objc_property_8eef248)['getter'])
            _name_boundary.attributes(quay_self_932ed44)['setters'].append(_name_boundary.attributes(quay_objc_property_8eef248)['setter'])
            _name_boundary.attributes(quay_self_932ed44)['properties'].append(quay_objc_property_8eef248)

    @_name_boundary.callable_contract({'self': 'quay_self_c772fd9'}, '_process_ivars')
    def quay__process_ivars(quay_self_c772fd9):
        for quay_ivar_f2f38ca in _name_boundary.attributes(_name_boundary.attributes(quay_self_c772fd9)['objc_class'])['ivars']:
            quay_bad_a959590 = False
            for quay_prop_a0e8894 in _name_boundary.attributes(quay_self_c772fd9)['properties']:
                if _name_boundary.attributes(quay_ivar_f2f38ca)['name'] == _name_boundary.attributes(quay_prop_a0e8894)['ivarname']:
                    quay_bad_a959590 = True
                    break
            if quay_bad_a959590:
                continue
            _name_boundary.attributes(quay_self_c772fd9)['ivars'].append(quay_ivar_f2f38ca)

    @_name_boundary.callable_contract({'self': 'quay_self_cbd3e17'}, '_process_methods')
    def quay__process_methods(quay_self_cbd3e17):
        for quay_method_703a3f2 in _name_boundary.attributes(_name_boundary.attributes(quay_self_cbd3e17)['objc_class'])['methods']:
            quay_bad_10fcbdf = False
            for quay_name_18264ab in _name_boundary.attributes(quay_self_cbd3e17)['getters']:
                if quay_name_18264ab in _name_boundary.attributes(quay_method_703a3f2)['sel'] and ':' not in _name_boundary.attributes(quay_method_703a3f2)['sel']:
                    quay_bad_10fcbdf = True
                    break
            for quay_name_18264ab in _name_boundary.attributes(quay_self_cbd3e17)['setters']:
                if quay_name_18264ab in _name_boundary.attributes(quay_method_703a3f2)['sel'] and 'set' in _name_boundary.attributes(quay_method_703a3f2)['sel']:
                    quay_bad_10fcbdf = True
                    break
            if quay_bad_10fcbdf:
                continue
            _name_boundary.attributes(quay_self_cbd3e17)['methods'].append(quay_method_703a3f2)

@_name_boundary.class_contract('StructDef', {'struct_definition': 'quay_struct_definition'})
class quay_StructDef:

    @_name_boundary.callable_contract({'self': 'quay_self_b0cd4e1', 'struct_definition': 'quay_struct_definition_4e5cef7'}, '__init__')
    def __init__(quay_self_b0cd4e1, quay_struct_definition_4e5cef7):
        _name_boundary.attributes(quay_self_b0cd4e1)['struct_definition'] = quay_struct_definition_4e5cef7

@_name_boundary.class_contract('CategoryInterface', {'_generate_text': 'quay__generate_text', 'category': 'quay_category', 'properties': 'quay_properties', 'methods': 'quay_methods', 'protocols': 'quay_protocols', 'text': 'quay_text'})
class quay_CategoryInterface:

    @_name_boundary.callable_contract({'self': 'quay_self_7bef6ff', 'objc_category': 'quay_objc_category_e888e33'}, '__init__')
    def __init__(quay_self_7bef6ff, quay_objc_category_e888e33: quay_Category):
        _name_boundary.attributes(quay_self_7bef6ff)['category'] = quay_objc_category_e888e33
        _name_boundary.attributes(quay_self_7bef6ff)['properties'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_7bef6ff)['category'])['properties']
        _name_boundary.attributes(quay_self_7bef6ff)['methods'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_7bef6ff)['category'])['methods']
        _name_boundary.attributes(quay_self_7bef6ff)['protocols'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_7bef6ff)['category'])['protocols']
        _name_boundary.attributes(quay_self_7bef6ff)['text'] = _name_boundary.attributes(quay_self_7bef6ff)['_generate_text']()

    @_name_boundary.callable_contract({'self': 'quay_self_d1fb0ba'}, '__str__')
    def __str__(quay_self_d1fb0ba):
        return _name_boundary.attributes(quay_self_d1fb0ba)['text']

    @_name_boundary.callable_contract({'self': 'quay_self_6d28528'}, '_generate_text')
    def quay__generate_text(quay_self_6d28528):
        quay_head_6f80b3f = '@interface '
        quay_head_6f80b3f += _name_boundary.attributes(_name_boundary.attributes(quay_self_6d28528)['category'])['classname'] + ' (' + _name_boundary.attributes(_name_boundary.attributes(quay_self_6d28528)['category'])['name'] + ')'
        if len(_name_boundary.attributes(_name_boundary.attributes(quay_self_6d28528)['category'])['protocols']) > 0:
            quay_head_6f80b3f += ' <'
            for quay_protocol_e75986c in _name_boundary.attributes(_name_boundary.attributes(quay_self_6d28528)['category'])['protocols']:
                quay_head_6f80b3f += str(quay_protocol_e75986c) + ', '
            quay_head_6f80b3f = quay_head_6f80b3f[:-2]
            quay_head_6f80b3f += '>\n'
        quay_props_47a869b = '\n\n'
        for quay_prop_a92479e in _name_boundary.attributes(quay_self_6d28528)['properties']:
            quay_props_47a869b += str(quay_prop_a92479e) + ';'
            if _name_boundary.attributes(quay_prop_a92479e)['ivarname'] != '':
                quay_props_47a869b += ' // ivar: ' + _name_boundary.attributes(quay_prop_a92479e)['ivarname'] + '\n'
            else:
                quay_props_47a869b += '\n'
        quay_meths_2a4b2e4 = '\n\n'
        for quay_i_844707d in _name_boundary.attributes(quay_self_6d28528)['methods']:
            quay_meths_2a4b2e4 += str(quay_i_844707d) + ';\n'
        quay_foot_4523abb = '@end\n'
        return quay_head_6f80b3f + quay_props_47a869b + quay_meths_2a4b2e4 + quay_foot_4523abb

@_name_boundary.class_contract('ProtocolInterface', {'_generate_text': 'quay__generate_text', 'protocol': 'quay_protocol', 'text': 'quay_text'})
class quay_ProtocolInterface:

    @_name_boundary.callable_contract({'self': 'quay_self_b039c8b', 'protocol': 'quay_protocol_fc0a1e7'}, '__init__')
    def __init__(quay_self_b039c8b, quay_protocol_fc0a1e7: quay_Protocol):
        _name_boundary.attributes(quay_self_b039c8b)['protocol']: quay_Protocol = quay_protocol_fc0a1e7
        _name_boundary.attributes(quay_self_b039c8b)['text'] = _name_boundary.attributes(quay_self_b039c8b)['_generate_text']()

    @_name_boundary.callable_contract({'self': 'quay_self_d562d10'}, '__str__')
    def __str__(quay_self_d562d10):
        return _name_boundary.attributes(quay_self_d562d10)['text']

    @_name_boundary.callable_contract({'self': 'quay_self_79852f3'}, '_generate_text')
    def quay__generate_text(quay_self_79852f3):
        quay_text_cbf22a1 = ['@protocol ' + _name_boundary.attributes(_name_boundary.attributes(quay_self_79852f3)['protocol'])['name'], '']
        for quay_prop_e9f6016 in _name_boundary.attributes(_name_boundary.attributes(quay_self_79852f3)['protocol'])['properties']:
            quay_pro_0395d53 = ''
            quay_pro_0395d53 += str(quay_prop_e9f6016) + ';'
            if _name_boundary.has_attribute(quay_prop_e9f6016, 'ivarname'):
                if _name_boundary.attributes(quay_prop_e9f6016)['ivarname'] != '':
                    quay_pro_0395d53 += ' // ivar: ' + _name_boundary.attributes(quay_prop_e9f6016)['ivarname'] + ''
                else:
                    quay_pro_0395d53 += ''
            quay_text_cbf22a1.append(quay_pro_0395d53)
        quay_text_cbf22a1.append('')
        for quay_meth_49a8af5 in _name_boundary.attributes(_name_boundary.attributes(quay_self_79852f3)['protocol'])['methods']:
            quay_text_cbf22a1.append(str(quay_meth_49a8af5) + ';')
        quay_text_cbf22a1.append('')
        if len(_name_boundary.attributes(_name_boundary.attributes(quay_self_79852f3)['protocol'])['opt_methods']) > 0:
            quay_text_cbf22a1.append('@optional')
            for quay_meth_49a8af5 in _name_boundary.attributes(_name_boundary.attributes(quay_self_79852f3)['protocol'])['opt_methods']:
                quay_text_cbf22a1.append(str(quay_meth_49a8af5) + ';')
        quay_text_cbf22a1.append('@end')
        return '\n'.join(quay_text_cbf22a1)

@_name_boundary.class_contract('UmbrellaHeader', {'text': 'quay_text'})
class quay_UmbrellaHeader:

    @_name_boundary.callable_contract({'self': 'quay_self_015bb02', 'header_list': 'quay_header_list_b5d4aa0'}, '__init__')
    def __init__(quay_self_015bb02, quay_header_list_b5d4aa0: dict):
        """
        Generates a header that solely imports other headers

        :param header_list: Dict of headers to be imported
        """
        _name_boundary.attributes(quay_self_015bb02)['text'] = '\n\n'
        for quay_header_8495d3f in quay_header_list_b5d4aa0.keys():
            _name_boundary.attributes(quay_self_015bb02)['text'] += '#include "' + quay_header_8495d3f + '"\n'

    @_name_boundary.callable_contract({'self': 'quay_self_6c0cb66'}, '__str__')
    def __str__(quay_self_6c0cb66):
        return _name_boundary.attributes(quay_self_6c0cb66)['text']
_name_boundary.module_contract(globals(), {'Protocol': 'quay_Protocol', 'TypeResolver': 'quay_TypeResolver', 'HeaderGenerator': 'quay_HeaderGenerator', 'Image': 'quay_Image', 'ProtocolHeader': 'quay_ProtocolHeader', 'HeaderUtils': 'quay_HeaderUtils', 'KTOOL_VERSION': 'quay_IMAGEQUAY_VERSION', 'Method': 'quay_Method', 'highlight': 'quay_highlight', 'ProtocolInterface': 'quay_ProtocolInterface', 'Ivar': 'quay_Ivar', 'Property': 'quay_Property', 'Header': 'quay_Header', 'Interface': 'quay_Interface', 'CategoryInterface': 'quay_CategoryInterface', 'SymbolType': 'quay_SymbolType', 'ObjCImage': 'quay_ObjCImage', 'List': 'quay_List', 'UmbrellaHeader': 'quay_UmbrellaHeader', 'TerminalFormatter': 'quay_TerminalFormatter', 'Class': 'quay_Class', 'Dict': 'quay_Dict', 'CategoryHeader': 'quay_CategoryHeader', 'StructHeader': 'quay_StructHeader', 'StructDef': 'quay_StructDef', 'Category': 'quay_Category'})
