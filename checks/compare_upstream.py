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
audit_differences=[{'index':i,'old':old,'new':new} for i,(old,new) in enumerate(zip(audit_old,audit_new)) if old!=new]
if audit_differences:
    print(audit_json.dumps(audit_differences[:10],ensure_ascii=False,indent=2))
    raise SystemExit(1)
print(audit_json.dumps({'project':audit_project,'observations':len(audit_old),'mismatches':0,'status':'PASS'}))
