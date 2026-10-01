"""Deterministic isolated observations used for upstream/derivative comparison."""
import argparse
import contextlib
import importlib
import io
import json
import logging
import os
from pathlib import Path
import random
import struct
import sys
import tempfile

case_parser=argparse.ArgumentParser()
case_parser.add_argument('project')
case_parser.add_argument('variant',choices=['original','derivative'])
case_parser.add_argument('root',type=Path)
case_parser.add_argument('--fixtures',type=Path)
case_args=case_parser.parse_args()
case_random=random.Random(812603)
case_data=[]

def case_observe(case_label,case_callable):
    try:
        case_result=case_callable()
        case_data.append([case_label,'return',case_result])
    except Exception as case_exception:
        case_data.append([case_label,'exception',type(case_exception).__name__.removeprefix('quay_').removeprefix('meadow_').removeprefix('mosaic_'),str(case_exception)])

def case_import(case_old,case_new):
    return importlib.import_module(case_old if case_args.variant=='original' else case_new)

if case_args.project=='ImageQuay':
    sys.path.insert(0,str(case_args.root/'src'))
    case_api=case_import('ktool','imagequay')
    case_structs=case_import('ktool_macho.structs','imagequay_layout.binary_records')
    case_engine=case_import('lib0cyn.structs','imagequay_support.record_engine')
    case_fixups=case_import('ktool_macho.fixups','imagequay_layout.pointer_records')
    case_plist=case_import('lib0cyn.kplistlib','imagequay_support.plist_codec')
    case_record_names=[]
    for case_name,case_type in vars(case_structs).items():
        if case_name.startswith('quay_'):continue
        if isinstance(case_type,type) and issubclass(case_type,case_engine.Struct) and case_type is not case_engine.Struct:
            case_record_names.append(case_name)
    for case_name in sorted(set(case_record_names)):
        case_type=getattr(case_structs,case_name)
        for case_index in range(12):
            case_raw=case_random.randbytes(case_type.size())
            def case_struct_output():
                case_value=case_engine.Struct.create_with_bytes(case_type,case_raw)
                return [case_value.raw.hex(),case_value.serialize(),str(case_value)]
            case_observe(['struct',case_name,case_index],case_struct_output)
    for case_word in [0,1,2,3,2**63,2**64-1]+[case_random.getrandbits(64) for _ in range(128)]:
        for case_name in ['dyld_chained_ptr_arm64e_rebase','dyld_chained_ptr_arm64e_bind','dyld_chained_ptr_64_rebase']:
            def case_fixup_output():
                case_value=case_engine.Struct.create_with_bytes(getattr(case_fixups,case_name),case_word.to_bytes(8,'little'))
                return [case_value.raw.hex(),case_value.serialize(),str(case_value)]
            case_observe(['fixup',case_name,case_word],case_fixup_output)
    for case_format in [case_plist.FMT_XML,case_plist.FMT_BINARY]:
        for case_index in range(40):
            case_value={'label':'场景'+str(case_index),'count':case_random.getrandbits(31),'entries':[True,False,b'\x00\xff',case_index]}
            case_observe(['plist',case_format.name,case_index],lambda:case_plist.dumps(case_value,fmt=case_format).hex())
    for case_name in ['testbin1','testbin1.fat','testbin1.signed','testlib1.dylib']:
        case_path=case_args.fixtures/case_name
        case_observe(['image',case_name],lambda:case_api.load_image(open(case_path,'rb')).serialize())

elif case_args.project=='TraceMeadow':
    sys.path.insert(0,str(case_args.root if case_args.variant=='original' else case_args.root/'src'))
    case_events=case_import('pykdebugparser.kevent','tracemeadow.event_records')
    case_codes=case_import('pykdebugparser.trace_codes','tracemeadow.code_index')
    case_stream=case_import('pykdebugparser.kd_buf_parser','tracemeadow.binary_stream')
    for case_size in list(range(0,70))+[128,256]:
        case_raw=case_random.randbytes(case_size)
        case_observe(['event-boundary',case_size],lambda:list(case_events.from_kd_buf(case_raw)))
    for case_index in range(1000):
        case_raw=case_random.randbytes(64)
        case_observe(['event',case_index],lambda:[case_events.from_kd_buf(case_raw)._asdict(),repr(case_events.from_kd_buf(case_raw))])
    case_observe(['trace-codes'],lambda:case_codes.default_trace_codes())
    for case_size in range(0,60):
        case_raw=case_random.randbytes(case_size)
        case_observe(['stream-boundary',case_size],lambda:list(case_stream.KdBufParser().parse(io.BytesIO(case_raw))))

else:
    case_original=case_args.variant=='original'
    if case_original:
        sys.path.insert(0,str(case_args.root/'reverse-sandbox'))
        os.chdir(case_args.root/'reverse-sandbox')
    else:sys.path.insert(0,str(case_args.root/'src'))
    case_profiles=case_import('reverse_sandbox','policymosaic.profile_decoder')
    case_regex=case_import('regex_parser','policymosaic.regex_bytecode')
    case_strings=case_import('reverse_string','policymosaic.string_bytecode')
    case_filters=case_import('filters','policymosaic.filter_catalog')
    case_modifiers=case_import('modifiers','policymosaic.modifier_catalog')
    case_nodes=case_import('operation_node','policymosaic.rule_graph')
    logging.disable(logging.CRITICAL)
    for case_release in [17,18,26]:
        for case_index in range(128):
            case_values=[case_random.randrange(0,40) for _ in range(9)]
            case_values[0]=case_random.choice([0,0x8000])
            case_value=case_profiles.SandboxData(case_release,14,*case_values)
            case_labels=['release','header_size','type','op_nodes_count','sb_ops_count','vars_count','states_count','num_profiles','regex_count','entitlements_count','regex_table_offset','vars_offset','states_offset','entitlements_offset','profiles_offset','profiles_end_offset','operation_nodes_size','operation_nodes_offset','base_addr']
            case_observe(['profile-layout',case_release,case_index],lambda:[{n:getattr(case_value,n) for n in case_labels},repr(case_value)])
    for case_size in range(0,20):
        case_raw=case_random.randbytes(case_size)
        case_namespace=argparse.Namespace(release='17')
        with contextlib.redirect_stdout(io.StringIO()):
            case_observe(['header-boundary',case_size],lambda:repr(case_profiles.parse_profile(io.BytesIO(case_raw),case_namespace)))
    for case_opcode in [0x02,0x19,0x29,0x09,0x2f,0x0a,0x1b,0x25]:
        for case_index in range(64):
            case_payload=bytes([case_opcode])+case_random.randbytes(10)
            case_records=[]
            case_observe(['regex-opcode',case_opcode,case_index],lambda:[case_regex.parse(case_payload,0,case_records),case_records])
    for case_text in ['', 'a', '.', 'alpha', '/tmp/example', '场景', 'x'*80]:
        for case_end in [b'',b'\x0a']:
            case_wire=bytes([0x3f+len(case_text.encode())])+case_text.encode()+case_end
            case_observe(['string',case_text,case_end.hex()],lambda:case_strings.SandboxString().parse_byte_string(case_wire,[]))
    case_observe(['filters'],lambda:case_filters.Filters.filters)
    case_observe(['modifiers'],lambda:case_modifiers.Modifiers.modifiers)
    for case_allow in [0,1,2,None]:
        for case_flags in [0,1,2,255,None]:
            case_node=case_nodes.TerminalNode();case_node.type=case_allow;case_node.flags=case_flags
            case_observe(['terminal',case_allow,case_flags],lambda:str(case_node))
    case_helper=case_import('extract_sb','policymosaic.firmware_helper') if not case_original else None
    if case_original:
        sys.path.insert(0,str(case_args.root/'helpers'));case_helper=importlib.import_module('extract_sb')
    for case_text in ['Created /tmp/kernel','kernelcache already exists /tmp/kernel','hello\nCreated ./kernel','nothing']:
        case_observe(['helper-output',case_text],lambda:str(case_helper.ipsw_get_out_path(case_text)))

print(json.dumps(case_data,ensure_ascii=False,sort_keys=True,default=lambda case_v:case_v.hex() if isinstance(case_v,(bytes,bytearray)) else str(case_v)))
