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
    if audit_project=='ImageQuay':audit_command.extend(['--fixtures',str(audit_root/'checks/bins')])
    audit_result=audit_subprocess.run(audit_command,text=True,capture_output=True,check=True)
    audit_observations.append(audit_json.loads(audit_result.stdout))
audit_old,audit_new=audit_observations
assert len(audit_old)==len(audit_new),(len(audit_old),len(audit_new))
audit_intentional=[]
# Address fixtures are cross-checked with Apple nm in test_quay_defensive_io.py.
audit_export_addresses=audit_json.loads((audit_root/'checks/export_nm_expected.json').read_text())
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
    assert audit_previous==audit_current,'Unexpected differences beyond export addresses'
    audit_intentional.append(audit_label[1])
audit_differences=[{'index':i,'old':old,'new':new} for i,(old,new) in enumerate(zip(audit_old,audit_new)) if old!=new]
if audit_differences:
    print(audit_json.dumps(audit_differences[:10],ensure_ascii=False,indent=2))
    raise SystemExit(1)
print(audit_json.dumps({'project':audit_project,'observations':len(audit_old),'unexplained_mismatches':0,'intentional_export_address_fixes':audit_intentional,'status':'PASS'}))
