# Derived from src/ktool/ktool.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  ktool.py
#
#  Outward facing API
#
#  Some of these functions are only one line long, but the point is to standardize an outward facing API that allows
#  me to refactor and change things internally without breaking others' scripts.
#
#  This file is part of ktool. ktool is free software that
#  is made available under the MIT license. Consult the
#  file "LICENSE" that is distributed together with this file
#  for the exact licensing terms.
#
#  Copyright (c) 0cyn 2021.
#
import imagequay_boundary as _name_boundary
from typing import Dict as quay_Dict, Union as quay_Union, BinaryIO as quay_BinaryIO, List as quay_List
from io import BytesIO as quay_BytesIO
from imagequay.metadata_reader import quay_MachOImageLoader as quay_MachOImageLoader, quay_Image as quay_Image
from imagequay.stub_documents import quay_TBDGenerator as quay_TBDGenerator, quay_FatMachOGenerator as quay_FatMachOGenerator
try:
    from imagequay.header_documents import quay_HeaderGenerator as quay_HeaderGenerator, quay_Header as quay_Header
except ModuleNotFoundError:
    quay_Header = None
    quay_HeaderGenerator = None
    pass
from imagequay.container_io import quay_Slice as quay_Slice, quay_MachOFile as quay_MachOFile, quay_SlicedBackingFile as quay_SlicedBackingFile
from imagequay.objc_model import quay_ObjCImage as quay_ObjCImage, quay_MethodList as quay_MethodList
from imagequay.swift_model import quay_SwiftImage as quay_SwiftImage
from imagequay.formatting import quay_TapiYAMLWriter as quay_TapiYAMLWriter, quay_ignore as quay_ignore
from imagequay_support.diagnostics import quay_log as quay_log

@_name_boundary.callable_contract({'fp': 'quay_fp_4c5b0be', 'use_mmaped_io': 'quay_use_mmaped_io_ce4c61e'}, 'load_macho_file')
def quay_load_macho_file(quay_fp_4c5b0be: quay_Union[quay_SlicedBackingFile, quay_BinaryIO, quay_BytesIO], quay_use_mmaped_io_ce4c61e=False) -> quay_MachOFile:
    """
    This function takes a bare file and loads it as a MachOFile.

    File should be opened with 'rb'

    :param fp: BinaryIO object
    :param use_mmaped_io: Should the MachOFile be loaded with a mmaped-io-backend? Leaving this enabled massively
                            improves load time and IO performance, only disable if your system doesn't support it
    :return:
    """
    if isinstance(quay_fp_4c5b0be, quay_BytesIO):
        quay_use_mmaped_io_ce4c61e = False
    elif isinstance(quay_fp_4c5b0be, quay_SlicedBackingFile):
        quay_use_mmaped_io_ce4c61e = False
        quay_new_fp_cf81a2b = quay_BytesIO()
        _name_boundary.attributes(quay_new_fp_cf81a2b)['write'](bytes(_name_boundary.attributes(quay_fp_4c5b0be)['file']))
        quay_new_fp_cf81a2b.seek(0)
        quay_fp_4c5b0be = quay_new_fp_cf81a2b
    return quay_MachOFile(quay_fp_4c5b0be, use_mmaped_io=quay_use_mmaped_io_ce4c61e)

@_name_boundary.callable_contract({'image': 'quay_image_ca280f7'}, 'reload_image')
def quay_reload_image(quay_image_ca280f7: quay_Image) -> quay_Image:
    """
    Reload an image (properly updates internal representations after patches)

    :param image:
    :return:
    """
    return quay_load_image(_name_boundary.attributes(quay_image_ca280f7)['slice'])

@_name_boundary.callable_contract({'fp': 'quay_fp_6adef83', 'slice_index': 'quay_slice_index_2c22772', 'load_symtab': 'quay_load_symtab_b46c033', 'load_imports': 'quay_load_imports_e393e5b', 'load_exports': 'quay_load_exports_4f7c9d8', 'use_mmaped_io': 'quay_use_mmaped_io_6e8b44b', 'force_misaligned_vm': 'quay_force_misaligned_vm_2554441'}, 'load_image')
def quay_load_image(quay_fp_6adef83: quay_Union[quay_BinaryIO, quay_MachOFile, quay_Slice, quay_BytesIO, quay_SlicedBackingFile], quay_slice_index_2c22772=0, quay_load_symtab_b46c033=True, quay_load_imports_e393e5b=True, quay_load_exports_4f7c9d8=True, quay_use_mmaped_io_6e8b44b=True, quay_force_misaligned_vm_2554441=False) -> quay_Image:
    """
    Take a bare file, MachOFile, BytesIO, SlicedBackingFile, or Slice, and load MachO/dyld metadata about that item

    :param fp: a bare file, MachOFile, or Slice to load.
    :param slice_index: If a Slice is not being passed, and a file or MachOFile is a Fat MachO, which slice should be loaded?
    :param use_mmaped_io: If a bare file is being passed, load it with mmaped IO?
    :param load_symtab: Load the symbol table if one exists. This can be disabled for targeted loads, for speed.
    :param load_imports: Load imports if they exist. This can be disabled for targeted loads, for speed.
    :param load_exports: Load exports if they exist. This can be disabled for targeted loads, for speed.
    :return: Returns a loaded Image object
    :rtype: Image
    """
    if isinstance(quay_fp_6adef83, quay_MachOFile):
        quay_macho_file_2e42168 = quay_fp_6adef83
        quay_macho_slice_a717b5e: quay_Slice = _name_boundary.attributes(quay_macho_file_2e42168)['slices'][quay_slice_index_2c22772]
    elif isinstance(quay_fp_6adef83, quay_Slice):
        quay_macho_slice_a717b5e = quay_fp_6adef83
    elif isinstance(quay_fp_6adef83, quay_BytesIO):
        quay_macho_file_2e42168 = quay_load_macho_file(quay_fp_6adef83, use_mmaped_io=False)
        quay_macho_slice_a717b5e: quay_Slice = _name_boundary.attributes(quay_macho_file_2e42168)['slices'][quay_slice_index_2c22772]
    elif isinstance(quay_fp_6adef83, quay_SlicedBackingFile):
        quay_macho_file_2e42168 = quay_load_macho_file(quay_fp_6adef83, use_mmaped_io=False)
        quay_macho_slice_a717b5e: quay_Slice = _name_boundary.attributes(quay_macho_file_2e42168)['slices'][quay_slice_index_2c22772]
    else:
        quay_macho_file_2e42168 = quay_load_macho_file(quay_fp_6adef83, use_mmaped_io=quay_use_mmaped_io_6e8b44b)
        quay_macho_slice_a717b5e: quay_Slice = _name_boundary.attributes(quay_macho_file_2e42168)['slices'][quay_slice_index_2c22772]
    return _name_boundary.attributes(quay_MachOImageLoader)['load'](quay_macho_slice_a717b5e, load_symtab=quay_load_symtab_b46c033, load_imports=quay_load_imports_e393e5b, load_exports=quay_load_exports_4f7c9d8, force_misaligned_vm=quay_force_misaligned_vm_2554441)

@_name_boundary.callable_contract({'fp': 'quay_fp_1a66146'}, 'macho_verify')
def quay_macho_verify(quay_fp_1a66146: quay_Union[quay_BinaryIO, quay_MachOFile, quay_Slice, quay_Image]) -> None:
    """
    This function takes a variety of MachO-based objects, and loads them with malformation exceptions fully enabled.

    This can be used to verify patch code did not damage or improperly modify a MachO.

    :param fp: One of: BinaryIO, MachOFile, Slice, or Image, to load and verify
    :return:
    :raises: MalformedMachOException
    """
    quay_should_ignore_65db77c = _name_boundary.attributes(quay_ignore)['MALFORMED']
    _name_boundary.attributes(quay_log)['info']('Verifying MachO Integrity')
    _name_boundary.attributes(quay_ignore)['MALFORMED'] = False
    if isinstance(quay_fp_1a66146, quay_Image):
        quay_load_image(_name_boundary.attributes(quay_fp_1a66146)['slice'])
    elif isinstance(quay_fp_1a66146, quay_MachOFile) or isinstance(quay_fp_1a66146, quay_BinaryIO):
        if isinstance(quay_fp_1a66146, quay_MachOFile):
            quay_slices_f370558 = _name_boundary.attributes(quay_fp_1a66146)['slices']
        else:
            quay_slices_f370558 = quay_load_macho_file(quay_fp_1a66146)
        for quay_macho_slice_a5c9e25 in quay_slices_f370558:
            quay_load_image(quay_macho_slice_a5c9e25)
    else:
        quay_load_image(quay_fp_1a66146)
    _name_boundary.attributes(quay_ignore)['MALFORMED'] = quay_should_ignore_65db77c

@_name_boundary.callable_contract({'image': 'quay_image_d0cff52'}, 'load_objc_metadata')
def quay_load_objc_metadata(quay_image_d0cff52: quay_Image) -> quay_ObjCImage:
    if _name_boundary.attributes(quay_image_d0cff52)['chained_fixups'] is not None:
        quay_data_io_2251f88 = quay_BytesIO()
        _name_boundary.attributes(quay_data_io_2251f88)['write'](_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_image_d0cff52)['slice'])['file'])['read_bytes'](0, _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_image_d0cff52)['slice'])['file'])['size']))
        quay_data_io_2251f88.seek(0)
        for quay_rebase_a01254f in _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_image_d0cff52)['chained_fixups'])['rebases'])['items']():
            quay_data_io_2251f88.seek(_name_boundary.attributes(_name_boundary.attributes(quay_image_d0cff52)['vm'])['translate'](quay_rebase_a01254f[0]))
            _name_boundary.attributes(quay_data_io_2251f88)['write'](quay_rebase_a01254f[1].to_bytes(8, 'little'))
        quay_data_io_2251f88.seek(0)
        quay_image_d0cff52 = quay_load_image(quay_data_io_2251f88)
    return _name_boundary.attributes(quay_ObjCImage)['from_image'](quay_image_d0cff52)

@_name_boundary.callable_contract({'objc_image': 'quay_objc_image_d414ff3'}, 'load_swift_metadata')
def quay_load_swift_metadata(quay_objc_image_d414ff3: quay_ObjCImage) -> quay_SwiftImage:
    return _name_boundary.attributes(quay_SwiftImage)['from_image'](quay_objc_image_d414ff3)

@_name_boundary.callable_contract({'objc_image': 'quay_objc_image_8fab032', 'sort_items': 'quay_sort_items_ea9f9a4', 'forward_declare_private_imports': 'quay_forward_declare_private_imports_bd3e4a6'}, 'generate_headers')
def quay_generate_headers(quay_objc_image_8fab032: 'ObjCImage', quay_sort_items_ea9f9a4=False, quay_forward_declare_private_imports_bd3e4a6=False) -> quay_Dict[str, quay_Header]:
    quay_out_f33576b = {}
    if quay_sort_items_ea9f9a4:
        for quay_objc_class_befbae3 in _name_boundary.attributes(quay_objc_image_8fab032)['classlist']:
            _name_boundary.attributes(quay_objc_class_befbae3)['methods'].sort(key=lambda quay_h_1cd151f: _name_boundary.attributes(quay_h_1cd151f)['signature'])
            _name_boundary.attributes(quay_objc_class_befbae3)['properties'].sort(key=lambda quay_h_f5ef490: _name_boundary.attributes(quay_h_f5ef490)['name'])
        for quay_objc_proto_8de082c in _name_boundary.attributes(quay_objc_image_8fab032)['protolist']:
            _name_boundary.attributes(quay_objc_proto_8de082c)['methods'].sort(key=lambda quay_h_3b41c74: _name_boundary.attributes(quay_h_3b41c74)['signature'])
            _name_boundary.attributes(quay_objc_proto_8de082c)['opt_methods'].sort(key=lambda quay_h_cc2b427: _name_boundary.attributes(quay_h_cc2b427)['signature'])
    for quay_header_name_5ef3d1f, quay_header_d8681d6 in _name_boundary.attributes(_name_boundary.attributes(quay_HeaderGenerator(quay_objc_image_8fab032, forward_declare_private_includes=quay_forward_declare_private_imports_bd3e4a6))['headers'])['items']():
        quay_out_f33576b[quay_header_name_5ef3d1f] = quay_header_d8681d6
    return quay_out_f33576b

@_name_boundary.callable_contract({'image': 'quay_image_4a6bd24', 'compatibility': 'quay_compatibility_db88c18'}, 'generate_text_based_stub')
def quay_generate_text_based_stub(quay_image_4a6bd24: quay_Image, quay_compatibility_db88c18=True) -> str:
    quay_generator_4794d7f = quay_TBDGenerator(quay_image_4a6bd24, quay_compatibility_db88c18)
    return _name_boundary.attributes(quay_TapiYAMLWriter)['write_out'](_name_boundary.attributes(quay_generator_4794d7f)['dict'])

@_name_boundary.callable_contract({'slices': 'quay_slices_fdb7832'}, 'macho_combine')
def quay_macho_combine(quay_slices_fdb7832: quay_List[quay_Slice]) -> quay_BytesIO:
    quay_fat_generator_fac39f6 = quay_FatMachOGenerator(quay_slices_fdb7832)
    quay_fat_file_eecb251 = quay_BytesIO()
    _name_boundary.attributes(quay_fat_file_eecb251)['write'](_name_boundary.attributes(quay_fat_generator_fac39f6)['fat_head'])
    for quay_arch_9966fc5 in _name_boundary.attributes(quay_fat_generator_fac39f6)['fat_archs']:
        quay_fat_file_eecb251.seek(_name_boundary.attributes(quay_arch_9966fc5)['offset'])
        _name_boundary.attributes(quay_fat_file_eecb251)['write'](_name_boundary.attributes(_name_boundary.attributes(quay_arch_9966fc5)['slice'])['full_bytes_for_slice']())
    quay_fat_file_eecb251.seek(0)
    return quay_fat_file_eecb251
_name_boundary.module_contract(globals(), {'Image': 'quay_Image', 'TBDGenerator': 'quay_TBDGenerator', 'generate_headers': 'quay_generate_headers', 'macho_verify': 'quay_macho_verify', 'reload_image': 'quay_reload_image', 'load_image': 'quay_load_image', 'load_macho_file': 'quay_load_macho_file', 'SwiftImage': 'quay_SwiftImage', 'load_objc_metadata': 'quay_load_objc_metadata', 'Union': 'quay_Union', 'ignore': 'quay_ignore', 'TapiYAMLWriter': 'quay_TapiYAMLWriter', 'MachOImageLoader': 'quay_MachOImageLoader', 'MethodList': 'quay_MethodList', 'BytesIO': 'quay_BytesIO', 'BinaryIO': 'quay_BinaryIO', 'Slice': 'quay_Slice', 'SlicedBackingFile': 'quay_SlicedBackingFile', 'generate_text_based_stub': 'quay_generate_text_based_stub', 'FatMachOGenerator': 'quay_FatMachOGenerator', 'ObjCImage': 'quay_ObjCImage', 'List': 'quay_List', 'load_swift_metadata': 'quay_load_swift_metadata', 'Dict': 'quay_Dict', 'MachOFile': 'quay_MachOFile', 'macho_combine': 'quay_macho_combine', 'log': 'quay_log'})
