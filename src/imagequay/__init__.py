# Derived from src/ktool/__init__.py; original copyright and license in ORIGIN.md and LICENSE.
import imagequay_boundary as _name_boundary
from imagequay.toolkit_api import quay_load_image as quay_load_image, quay_load_objc_metadata as quay_load_objc_metadata, quay_generate_headers as quay_generate_headers, quay_generate_text_based_stub as quay_generate_text_based_stub, quay_load_macho_file as quay_load_macho_file, quay_macho_verify as quay_macho_verify, quay_reload_image as quay_reload_image, quay_macho_combine as quay_macho_combine
from imagequay.objc_model import quay_ObjCImage as quay_ObjCImage
from imagequay.metadata_reader import quay_MachOImageLoader as quay_MachOImageLoader
from imagequay.parsed_image import quay_Image as quay_Image
from imagequay.container_io import quay_Slice as quay_Slice, quay_MachOFile as quay_MachOFile, quay_MachOFileType as quay_MachOFileType, quay_Segment as quay_Segment, quay_Section as quay_Section, quay_MachOImageHeader as quay_MachOImageHeader
try:
    from imagequay.header_documents import quay_HeaderGenerator as quay_HeaderGenerator, quay_Header as quay_Header
except ModuleNotFoundError:
    quay_Header = None
    quay_HeaderGenerator = None
    pass
from imagequay.formatting import quay_IMAGEQUAY_VERSION as quay_IMAGEQUAY_VERSION, quay_ignore as quay_ignore, quay_Table as quay_Table, quay_detect_filetype as quay_detect_filetype, quay_FileType as quay_FileType
from imagequay_support.diagnostics import quay_LogLevel as quay_LogLevel, quay_log as quay_log
_name_boundary.module_contract(globals(), {'Table': 'quay_Table', 'Image': 'quay_Image', 'generate_headers': 'quay_generate_headers', 'macho_verify': 'quay_macho_verify', 'MachOFileType': 'quay_MachOFileType', 'reload_image': 'quay_reload_image', 'load_image': 'quay_load_image', 'load_macho_file': 'quay_load_macho_file', 'load_objc_metadata': 'quay_load_objc_metadata', 'KTOOL_VERSION': 'quay_IMAGEQUAY_VERSION', 'ignore': 'quay_ignore', 'MachOImageLoader': 'quay_MachOImageLoader', 'MachOImageHeader': 'quay_MachOImageHeader', 'Section': 'quay_Section', 'Slice': 'quay_Slice', 'generate_text_based_stub': 'quay_generate_text_based_stub', 'ObjCImage': 'quay_ObjCImage', 'LogLevel': 'quay_LogLevel', 'FileType': 'quay_FileType', 'Segment': 'quay_Segment', 'MachOFile': 'quay_MachOFile', 'macho_combine': 'quay_macho_combine', 'log': 'quay_log', 'detect_filetype': 'quay_detect_filetype'})
