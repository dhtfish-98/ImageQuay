# Derived from src/ktool/kcache.py; original copyright and license in ORIGIN.md and LICENSE.
#
#  ktool | ktool
#  kcache.py
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
from io import BytesIO as quay_BytesIO
import imagequay as quay_imagequay
from imagequay_support.record_engine import *
from imagequay import quay_MachOFile as quay_MachOFile, quay_Image as quay_Image
from imagequay_support.diagnostics import quay_log as quay_log
from imagequay.metadata_reader import quay_MachOImageHeader as quay_MachOImageHeader, quay_MachOImageLoader as quay_MachOImageLoader
import imagequay_support.plist_codec as quay_plistlib
from imagequay.failure_types import quay_UnsupportedFiletypeException as quay_UnsupportedFiletypeException

@_name_boundary.class_contract('kmod_info_64', {'_FIELDNAMES': 'quay__FIELDNAMES', '_SIZES': 'quay__SIZES', 'SIZE': 'quay_SIZE', 'next_addr': 'quay_next_addr', 'info_version': 'quay_info_version', 'id': 'quay_id', 'name': 'quay_name', 'version': 'quay_version', 'reference_count': 'quay_reference_count', 'reference_list_addr': 'quay_reference_list_addr', 'address': 'quay_address', 'size': 'quay_size', 'hdr_size': 'quay_hdr_size', 'start_addr': 'quay_start_addr', 'stop_addr': 'quay_stop_addr'})
class quay_kmod_info_64(quay_Struct):
    """
    """
    quay__FIELDNAMES = ['next_addr', 'info_version', 'id', 'name', 'version', 'reference_count', 'reference_list_addr', 'address', 'size', 'hdr_size', 'start_addr', 'stop_addr']
    quay__SIZES = [quay_uint64_t, quay_int32_t, quay_uint32_t, quay_char_t[64], quay_char_t[64], quay_int32_t, quay_uint64_t, quay_uint64_t, quay_uint64_t, quay_uint64_t, quay_uint64_t, quay_uint64_t]
    quay_SIZE = sum([65535 & quay_i_a1eeb8a for quay_i_a1eeb8a in quay__SIZES])

    @_name_boundary.callable_contract({'self': 'quay_self_39528a1', 'byte_order': 'quay_byte_order_c73cba3'}, '__init__')
    def __init__(quay_self_39528a1, quay_byte_order_c73cba3='little'):
        super().__init__(fields=_name_boundary.attributes(quay_self_39528a1)['_FIELDNAMES'], sizes=_name_boundary.attributes(quay_self_39528a1)['_SIZES'], byte_order=quay_byte_order_c73cba3)

@_name_boundary.class_contract('Kext', {'prelink_info': 'quay_prelink_info', 'name': 'quay_name', 'version': 'quay_version', 'start_addr': 'quay_start_addr', 'development_region': 'quay_development_region', 'executable_name': 'quay_executable_name', 'id': 'quay_id', 'bundle_name': 'quay_bundle_name', 'package_type': 'quay_package_type', 'info_string': 'quay_info_string', 'version_str': 'quay_version_str', 'image': 'quay_image'})
class quay_Kext:

    @_name_boundary.callable_contract({'self': 'quay_self_8487f49'}, '__init__')
    def __init__(quay_self_8487f49):
        _name_boundary.attributes(quay_self_8487f49)['prelink_info'] = {}
        _name_boundary.attributes(quay_self_8487f49)['name'] = ''
        _name_boundary.attributes(quay_self_8487f49)['version'] = ''
        _name_boundary.attributes(quay_self_8487f49)['start_addr'] = 0
        _name_boundary.attributes(quay_self_8487f49)['development_region'] = ''
        _name_boundary.attributes(quay_self_8487f49)['executable_name'] = ''
        _name_boundary.attributes(quay_self_8487f49)['id'] = ''
        _name_boundary.attributes(quay_self_8487f49)['bundle_name'] = ''
        _name_boundary.attributes(quay_self_8487f49)['package_type'] = ''
        _name_boundary.attributes(quay_self_8487f49)['info_string'] = ''
        _name_boundary.attributes(quay_self_8487f49)['version_str'] = ''
        _name_boundary.attributes(quay_self_8487f49)['image'] = None

@_name_boundary.class_contract('EmbeddedKext', {'start_addr': 'quay_start_addr', 'size': 'quay_size', 'name': 'quay_name', 'version': 'quay_version', 'backing_file': 'quay_backing_file', 'image': 'quay_image'})
class quay_EmbeddedKext(quay_Kext):

    @_name_boundary.callable_contract({'self': 'quay_self_abc3624', 'image': 'quay_image_4a8dfb4', 'prelink_info': 'quay_prelink_info_aaeb3b2'}, '__init__')
    def __init__(quay_self_abc3624, quay_image_4a8dfb4, quay_prelink_info_aaeb3b2):
        super().__init__()
        _name_boundary.attributes(quay_self_abc3624)['start_addr'] = quay_prelink_info_aaeb3b2['_PrelinkExecutableLoadAddr']
        _name_boundary.attributes(quay_self_abc3624)['size'] = quay_prelink_info_aaeb3b2['_PrelinkExecutableSize']
        _name_boundary.attributes(quay_self_abc3624)['name'] = quay_prelink_info_aaeb3b2['CFBundleIdentifier']
        _name_boundary.attributes(quay_self_abc3624)['version'] = quay_prelink_info_aaeb3b2['CFBundleVersion']
        _name_boundary.attributes(quay_self_abc3624)['backing_file'] = quay_BytesIO()
        _name_boundary.attributes(_name_boundary.attributes(quay_self_abc3624)['backing_file'])['write'](_name_boundary.attributes(quay_image_4a8dfb4)['read_bytearray'](_name_boundary.attributes(quay_self_abc3624)['start_addr'], _name_boundary.attributes(quay_self_abc3624)['size'], vm=True))
        _name_boundary.attributes(quay_self_abc3624)['backing_file'].seek(0)
        _name_boundary.attributes(quay_self_abc3624)['image'] = _name_boundary.attributes(quay_imagequay)['load_image'](_name_boundary.attributes(quay_self_abc3624)['backing_file'])

@_name_boundary.class_contract('MergedKext', {'backing_image': 'quay_backing_image', 'backing_slice': 'quay_backing_slice', 'name': 'quay_name', 'version': 'quay_version', 'start_addr': 'quay_start_addr', 'info': 'quay_info', 'mach_header': 'quay_mach_header', 'image': 'quay_image'})
class quay_MergedKext(quay_Kext):

    @_name_boundary.callable_contract({'self': 'quay_self_d09568c', 'image': 'quay_image_1a2da93', 'kmod_info': 'quay_kmod_info_13e4f0c', 'start_addr': 'quay_start_addr_2434604'}, '__init__')
    def __init__(quay_self_d09568c, quay_image_1a2da93: quay_Image, quay_kmod_info_13e4f0c, quay_start_addr_2434604):
        super().__init__()
        _name_boundary.attributes(quay_self_d09568c)['backing_image'] = quay_image_1a2da93
        _name_boundary.attributes(quay_self_d09568c)['backing_slice'] = _name_boundary.attributes(quay_image_1a2da93)['slice']
        quay_is64_37df375 = _name_boundary.attributes(_name_boundary.attributes(quay_image_1a2da93)['macho_header'])['is64']
        _name_boundary.attributes(quay_self_d09568c)['name'] = _name_boundary.attributes(quay_image_1a2da93)['read_cstr'](_name_boundary.attributes(quay_kmod_info_13e4f0c)['off'] + (16 if quay_is64_37df375 else 8), vm=False)
        _name_boundary.attributes(quay_self_d09568c)['version'] = _name_boundary.attributes(quay_image_1a2da93)['read_cstr'](_name_boundary.attributes(quay_kmod_info_13e4f0c)['off'] + 64 + (16 if quay_is64_37df375 else 8), vm=False)
        _name_boundary.attributes(quay_self_d09568c)['start_addr'] = quay_start_addr_2434604
        _name_boundary.attributes(quay_self_d09568c)['info'] = quay_kmod_info_13e4f0c
        quay_file_base_addr_7c52893 = _name_boundary.attributes(_name_boundary.attributes(quay_image_1a2da93)['vm'])['translate'](quay_start_addr_2434604)
        _name_boundary.attributes(quay_self_d09568c)['mach_header'] = _name_boundary.attributes(quay_MachOImageHeader)['from_image'](_name_boundary.attributes(quay_self_d09568c)['backing_slice'], quay_file_base_addr_7c52893)
        _name_boundary.attributes(quay_self_d09568c)['image'] = quay_Image(_name_boundary.attributes(quay_self_d09568c)['backing_slice'])
        _name_boundary.attributes(_name_boundary.attributes(quay_self_d09568c)['image'])['macho_header'] = _name_boundary.attributes(quay_self_d09568c)['mach_header']
        _name_boundary.attributes(_name_boundary.attributes(quay_self_d09568c)['image'])['vm_realign'](yell_about_misalignment=False)
        _name_boundary.attributes(quay_MachOImageLoader)['_parse_load_commands'](_name_boundary.attributes(quay_self_d09568c)['image'])
        _name_boundary.attributes(quay_MachOImageLoader)['_process_image'](_name_boundary.attributes(quay_self_d09568c)['image'])
        for quay_segment_6b84166 in _name_boundary.attributes(quay_image_1a2da93)['segments'].values():
            _name_boundary.attributes(quay_segment_6b84166)['vm_address'] = _name_boundary.attributes(quay_segment_6b84166)['vm_address'] | 18446462598732840960

@_name_boundary.class_contract('KernelCache', {'_process_kexts_from_prelink_info': 'quay__process_kexts_from_prelink_info', '_process_kexts': 'quay__process_kexts', '_process_prelink_info': 'quay__process_prelink_info', '_process_merged_kexts': 'quay__process_merged_kexts', 'mach_kernel_file': 'quay_mach_kernel_file', 'mach_kernel': 'quay_mach_kernel', 'kexts': 'quay_kexts', 'prelink_info': 'quay_prelink_info', 'version': 'quay_version', 'version_str': 'quay_version_str', 'release_type': 'quay_release_type', 'arch': 'quay_arch', 'soc': 'quay_soc'})
class quay_KernelCache:

    @_name_boundary.callable_contract({'self': 'quay_self_7ab307c', 'macho_file': 'quay_macho_file_222a9fd'}, '__init__')
    def __init__(quay_self_7ab307c, quay_macho_file_222a9fd: quay_MachOFile):
        _name_boundary.attributes(quay_self_7ab307c)['mach_kernel_file'] = quay_macho_file_222a9fd
        _name_boundary.attributes(quay_self_7ab307c)['mach_kernel'] = _name_boundary.attributes(quay_imagequay)['load_image'](quay_macho_file_222a9fd)
        if _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_7ab307c)['mach_kernel'])['macho_header'])['is64']:
            _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_7ab307c)['mach_kernel'])['vm'])['detag_kern_64'] = True
        _name_boundary.attributes(quay_self_7ab307c)['kexts'] = []
        _name_boundary.attributes(quay_self_7ab307c)['prelink_info'] = {}
        if '__info' in _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_7ab307c)['mach_kernel'])['segments']['__PRELINK_INFO'])['sections']:
            _name_boundary.attributes(quay_self_7ab307c)['_process_prelink_info']()
        _name_boundary.attributes(quay_self_7ab307c)['version'] = _name_boundary.attributes(quay_self_7ab307c)['prelink_info']['com.apple.kpi.mach']['CFBundleVersion']
        _name_boundary.attributes(quay_self_7ab307c)['version_str'] = ''
        quay_vloc_1f8c4ac = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_7ab307c)['mach_kernel'])['slice'])['find']('@(#)VERSION:')
        _name_boundary.attributes(quay_self_7ab307c)['version_str'] = _name_boundary.attributes(_name_boundary.attributes(quay_self_7ab307c)['mach_kernel'])['read_cstr'](quay_vloc_1f8c4ac)
        quay_dat_9f0e2b0 = _name_boundary.attributes(quay_self_7ab307c)['version_str'].split('xnu_')[-1].split('/')[-1].lower()
        _name_boundary.attributes(quay_self_7ab307c)['release_type'] = quay_dat_9f0e2b0.split('_')[0]
        _name_boundary.attributes(quay_self_7ab307c)['arch'] = quay_dat_9f0e2b0.split('_')[1]
        _name_boundary.attributes(quay_self_7ab307c)['soc'] = quay_dat_9f0e2b0.split('_')[2]
        if '__kmod_info' in _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_7ab307c)['mach_kernel'])['segments']['__PRELINK_INFO'])['sections']:
            _name_boundary.attributes(quay_self_7ab307c)['_process_merged_kexts']()
        if len(_name_boundary.attributes(quay_self_7ab307c)['kexts']) == 0:
            if '_PrelinkExecutableLoadAddr' in _name_boundary.attributes(quay_self_7ab307c)['prelink_info']['com.apple.kpi.mach']:
                _name_boundary.attributes(quay_self_7ab307c)['_process_kexts_from_prelink_info']()
        _name_boundary.attributes(quay_self_7ab307c)['_process_kexts']()

    @_name_boundary.callable_contract({'self': 'quay_self_ec40b0a'}, '_process_kexts_from_prelink_info')
    def quay__process_kexts_from_prelink_info(quay_self_ec40b0a):
        for quay_kext_name_66710c5, quay_kext_b3e432b in _name_boundary.attributes(_name_boundary.attributes(quay_self_ec40b0a)['prelink_info'])['items']():
            try:
                _name_boundary.attributes(quay_self_ec40b0a)['kexts'].append(quay_EmbeddedKext(_name_boundary.attributes(quay_self_ec40b0a)['mach_kernel'], quay_kext_b3e432b))
            except quay_UnsupportedFiletypeException:
                _name_boundary.attributes(quay_log)['debug'](f'Bad Header(?) at {quay_kext_name_66710c5}')
            except KeyError:
                pass

    @_name_boundary.callable_contract({'self': 'quay_self_bb148c1'}, '_process_kexts')
    def quay__process_kexts(quay_self_bb148c1):
        for quay_kext_0969447 in _name_boundary.attributes(quay_self_bb148c1)['kexts']:
            if _name_boundary.attributes(quay_kext_0969447)['name'] in _name_boundary.attributes(quay_self_bb148c1)['prelink_info'].keys():
                _name_boundary.attributes(quay_kext_0969447)['executable_name'] = _name_boundary.attributes(quay_self_bb148c1)['prelink_info'][_name_boundary.attributes(quay_kext_0969447)['name']]['CFBundleExecutable']
                _name_boundary.attributes(quay_kext_0969447)['id'] = _name_boundary.attributes(quay_self_bb148c1)['prelink_info'][_name_boundary.attributes(quay_kext_0969447)['name']]['CFBundleIdentifier']
                _name_boundary.attributes(quay_kext_0969447)['bundle_name'] = _name_boundary.attributes(quay_self_bb148c1)['prelink_info'][_name_boundary.attributes(quay_kext_0969447)['name']]['CFBundleName']
                _name_boundary.attributes(quay_kext_0969447)['package_type'] = _name_boundary.attributes(quay_self_bb148c1)['prelink_info'][_name_boundary.attributes(quay_kext_0969447)['name']]['CFBundlePackageType']
                _name_boundary.attributes(quay_kext_0969447)['info_string'] = _name_boundary.attributes(quay_self_bb148c1)['prelink_info'][_name_boundary.attributes(quay_kext_0969447)['name']]['CFBundleGetInfoString'] if 'CFBundleGetInfoString' in _name_boundary.attributes(quay_self_bb148c1)['prelink_info'][_name_boundary.attributes(quay_kext_0969447)['name']] else ''
                _name_boundary.attributes(quay_kext_0969447)['version_str'] = _name_boundary.attributes(quay_self_bb148c1)['prelink_info'][_name_boundary.attributes(quay_kext_0969447)['name']]['CFBundleVersion']
                _name_boundary.attributes(quay_kext_0969447)['prelink_info'] = _name_boundary.attributes(quay_self_bb148c1)['prelink_info'][_name_boundary.attributes(quay_kext_0969447)['name']]

    @_name_boundary.callable_contract({'self': 'quay_self_cd6294b'}, '_process_prelink_info')
    def quay__process_prelink_info(quay_self_cd6294b):
        quay_address_77703d6 = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_cd6294b)['mach_kernel'])['segments']['__PRELINK_INFO'])['sections']['__info'])['vm_address']
        quay_prelink_info_str_ee997df = f"""<plist version="1.0">{_name_boundary.attributes(_name_boundary.attributes(quay_self_cd6294b)['mach_kernel'])['read_cstr'](quay_address_77703d6, vm=True)}</plist>"""
        quay_prelink_info_dat_efb7527 = quay_prelink_info_str_ee997df.encode('utf-8')
        quay_prelink_info_624c04c = quay_plistlib.readPlistFromBytes(quay_prelink_info_dat_efb7527)
        quay_items_9fe9baf = quay_prelink_info_624c04c['_PrelinkInfoDictionary']
        for quay_bundle_dict_eabab42 in quay_items_9fe9baf:
            _name_boundary.attributes(quay_self_cd6294b)['prelink_info'][quay_bundle_dict_eabab42['CFBundleIdentifier']] = quay_bundle_dict_eabab42

    @_name_boundary.callable_contract({'self': 'quay_self_58b5d7d'}, '_process_merged_kexts')
    def quay__process_merged_kexts(quay_self_58b5d7d):
        quay_kext_starts_0d35804 = []
        quay_kmod_start_sect_a2ab25e = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_58b5d7d)['mach_kernel'])['segments']['__PRELINK_INFO'])['sections']['__kmod_start']
        quay_ptr_size_6360105 = 8 if _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_58b5d7d)['mach_kernel'])['macho_header'])['is64'] else 4
        for quay_i_a3f47c6 in range(_name_boundary.attributes(quay_kmod_start_sect_a2ab25e)['file_address'], _name_boundary.attributes(quay_kmod_start_sect_a2ab25e)['file_address'] + _name_boundary.attributes(quay_kmod_start_sect_a2ab25e)['size'], quay_ptr_size_6360105):
            quay_kext_starts_0d35804.append(_name_boundary.attributes(_name_boundary.attributes(quay_self_58b5d7d)['mach_kernel'])['read_uint'](quay_i_a3f47c6, quay_ptr_size_6360105, vm=False))
        quay_kmod_info_locations_e27d997 = []
        quay_kmod_info_sect_bbb83dd = _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(quay_self_58b5d7d)['mach_kernel'])['segments']['__PRELINK_INFO'])['sections']['__kmod_info']
        for quay_i_a3f47c6 in range(_name_boundary.attributes(quay_kmod_info_sect_bbb83dd)['file_address'], _name_boundary.attributes(quay_kmod_info_sect_bbb83dd)['file_address'] + _name_boundary.attributes(quay_kmod_info_sect_bbb83dd)['size'], quay_ptr_size_6360105):
            quay_kmod_info_locations_e27d997.append(_name_boundary.attributes(_name_boundary.attributes(quay_self_58b5d7d)['mach_kernel'])['read_uint'](quay_i_a3f47c6, quay_ptr_size_6360105, vm=False))
        for quay_i_a3f47c6, quay_info_loc_a672041 in enumerate(quay_kmod_info_locations_e27d997):
            quay_info_5be8755 = _name_boundary.attributes(_name_boundary.attributes(quay_self_58b5d7d)['mach_kernel'])['read_struct'](quay_info_loc_a672041, quay_kmod_info_64, vm=True)
            quay_start_addr_f171727 = quay_kext_starts_0d35804[quay_i_a3f47c6]
            quay_kext_156dd3c = quay_MergedKext(_name_boundary.attributes(quay_self_58b5d7d)['mach_kernel'], quay_info_5be8755, quay_start_addr_f171727)
            _name_boundary.attributes(quay_self_58b5d7d)['kexts'].append(quay_kext_156dd3c)
_name_boundary.module_contract(globals(), {'plistlib': 'quay_plistlib', 'MachOFile': 'quay_MachOFile', 'ktool': 'quay_imagequay', 'kmod_info_64': 'quay_kmod_info_64', 'MergedKext': 'quay_MergedKext', 'Image': 'quay_Image', 'Kext': 'quay_Kext', 'KernelCache': 'quay_KernelCache', 'EmbeddedKext': 'quay_EmbeddedKext', 'MachOImageLoader': 'quay_MachOImageLoader', 'MachOImageHeader': 'quay_MachOImageHeader', 'UnsupportedFiletypeException': 'quay_UnsupportedFiletypeException', 'BytesIO': 'quay_BytesIO', 'log': 'quay_log'})
