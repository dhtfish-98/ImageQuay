"""Compare deterministic observations with a pinned upstream checkout."""
import argparse as audit_argparse
import json as audit_json
from pathlib import Path as AuditPath
import subprocess as audit_subprocess
import sys as audit_sys

audit_parser=audit_argparse.ArgumentParser()
audit_parser.add_argument('--upstream-root',type=AuditPath,required=True)
audit_options=audit_parser.parse_args()
audit_project='ImageQuay'
audit_root=AuditPath(__file__).resolve().parents[1]
audit_observer=audit_root/'checks/differential_observer.py'
audit_observations=[]
for audit_variant,audit_location in [('original',audit_options.upstream_root.resolve()),('derivative',audit_root)]:
    audit_command=[audit_sys.executable,str(audit_observer),audit_project,audit_variant,str(audit_location)]
    if audit_project=='ImageQuay':audit_command.extend(['--fixtures',str(audit_root/'Build/fixtures')])
    audit_result=audit_subprocess.run(audit_command,text=True,capture_output=True,check=True)
    audit_observations.append(audit_json.loads(audit_result.stdout))
audit_old,audit_new=audit_observations
assert len(audit_old)==len(audit_new),(len(audit_old),len(audit_new))
audit_intentional=[]
audit_bitfield_repairs=[]
# Address fixtures are cross-checked with Apple nm in test_quay_defensive_io.py.
audit_export_addresses=audit_json.loads((audit_root/'checks/export_nm_expected.json').read_text())
audit_function_starts=audit_json.loads((audit_root/'checks/function_starts_expected.json').read_text())
for audit_index,(audit_previous,audit_current) in enumerate(zip(audit_old,audit_new)):
    if audit_previous==audit_current:continue
    audit_label=audit_current[0]
    if audit_label[0]!='image' or audit_label[1] not in audit_export_addresses:continue
    assert audit_previous[1]==audit_current[1]=='return'
    audit_original_exports=audit_previous[2]['exports']
    audit_current_exports=audit_current[2]['exports']
    assert len(audit_original_exports)==len(audit_current_exports)
    audit_expected=audit_export_addresses[audit_label[1]]['exports']
    assert {entry['name']:entry['address'] for entry in audit_current_exports}==audit_expected
    for previous,current in zip(audit_original_exports,audit_current_exports):
        assert previous['name']==current['name']
        previous['address']=current['address']
    previous_starts,current_starts=audit_previous[2]['function_starts'],audit_current[2]['function_starts']
    assert current_starts==audit_function_starts[audit_label[1]]['function_starts']
    assert previous_starts[:len(current_starts)]==current_starts
    assert current_starts and all(value==current_starts[-1] for value in previous_starts[len(current_starts):])
    audit_previous[2]['function_starts']=current_starts
    assert audit_previous==audit_current,'Unexpected differences beyond export addresses and zero terminators'
    audit_intentional.append(audit_label[1])

# These previously failed before returning any field representation. Match the
# exact old failure and independently derive every current bit from the word;
# no other fixup record, serializer shape or rendering difference is accepted.
audit_layouts = {
    'dyld_chained_ptr_arm64e_rebase': ('target', [('target',43),('high8',8),('next',11),('bind',1),('auth',1)], 'TypeError', "'Bitfield' object cannot be interpreted as an integer"),
    'dyld_chained_ptr_arm64e_bind': ('ordinal', [('ordinal',16),('zero',16),('addend',19),('next',11),('bind',1),('auth',1)], 'TypeError', "'Bitfield' object cannot be interpreted as an integer"),
    'dyld_chained_ptr_64_rebase': ('value', [('target',36),('high8',8),('reserved',7),('next',12),('bind',1)], 'AttributeError', "'dyld_chained_ptr_64_rebase' object has no attribute 'value'"),
}
for audit_previous,audit_current in zip(audit_old,audit_new):
    if audit_previous==audit_current or audit_current[0][0]!='fixup':continue
    label,name,word = audit_current[0]
    assert name in audit_layouts
    primary,layout,error_type,error_text = audit_layouts[name]
    assert audit_previous == [[label,name,word],'exception',error_type,error_text]
    fields,position = {},0
    for field,bits in layout:
        fields[field] = (word >> position) & ((1 << bits)-1)
        position += bits
    text = name+' { '+primary+'='+''.join(f'{field}={value}, ' for field,value in fields.items())+' }'
    expected = [[label,name,word],'return',[word.to_bytes(8,'little').hex(), {'type':name,primary:fields}, text]]
    assert audit_current == expected, 'Unexpected bitfield codec or representation difference'
    audit_previous[:] = audit_current
    audit_bitfield_repairs.append([name,word])

audit_differences=[{'index':i,'old':old,'new':new} for i,(old,new) in enumerate(zip(audit_old,audit_new)) if old!=new]
if audit_differences:
    print(audit_json.dumps(audit_differences[:10],ensure_ascii=False,indent=2))
    raise SystemExit(1)
print(audit_json.dumps({'project':audit_project,'observations':len(audit_old),'unexplained_mismatches':0,'intentional_export_address_fixes':audit_intentional,'intentional_function_terminator_fixes':audit_intentional,'intentional_bitfield_codec_repairs':len(audit_bitfield_repairs),'unchanged_observations':len(audit_old)-len(audit_intentional)-len(audit_bitfield_repairs),'status':'PASS'}))
