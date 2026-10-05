"""Verify retained local edit/combine/extract functionality from an installed wheel."""
from pathlib import Path
import tempfile,subprocess,json,hashlib,os,sys
import imagequay
root=Path(__file__).resolve().parents[1];work=Path(tempfile.mkdtemp(prefix='imagequay-installed-cli-'));executable=str(Path(sys.executable).parent/'imagequay')
assert 'site-packages' in Path(imagequay.__file__).parts
with (root/'Build/fixtures/testbin1.fat').open('rb') as stream:owner=imagequay.load_macho_file(stream)
inputs=[]
for view in owner.slices[:2]:
 path=work/view.type.name.lower();path.write_bytes(view.full_bytes_for_slice());inputs.append(path)
source=work/'owned.dylib';source.write_bytes((root/'Build/fixtures/testlib1.dylib').read_bytes());sourcehash=hashlib.sha256(source.read_bytes()).hexdigest()
def run(args,expected=0):
 result=subprocess.run([executable,'-v','-1',*map(str,args)],cwd=work,capture_output=True,text=True,timeout=15)
 assert result.returncode==expected,(args,result.returncode,result.stdout,result.stderr)
 return result
combined=work/'combined';run(['lipo','--create','--out',combined,*inputs])
with combined.open('rb') as stream:new=imagequay.load_macho_file(stream)
assert len(new.slices)==2 and [v.full_bytes_for_slice() for v in new.slices]==[p.read_bytes() for p in inputs]
extracted=work/'extracted';run(['lipo','--extract',owner.slices[1].type.name.lower(),'--out',extracted,combined]);assert extracted.read_bytes()==inputs[1].read_bytes()
edited=work/'edited';run(['edit','--iname','/Owned/Local.dylib','--out',edited,source])
with edited.open('rb') as stream:assert imagequay.load_image(stream).dylib.install_name=='/Owned/Local.dylib'
inserted=work/'inserted';run(['insert','--lc','load','--payload','/Owned/Reviewed.dylib','--out',inserted,source])
with inserted.open('rb') as stream:assert any(item.install_name=='/Owned/Reviewed.dylib' for item in imagequay.load_image(stream).linked_images)
old=edited.read_bytes();run(['edit','--iname','/Owned/New.dylib','--out',edited,source],4);assert edited.read_bytes()==old
run(['--overwrite','edit','--iname','/Owned/New.dylib','--out',edited,source])
with edited.open('rb') as stream:assert imagequay.load_image(stream).dylib.install_name=='/Owned/New.dylib'
assert hashlib.sha256(source.read_bytes()).hexdigest()==sourcehash
assert all(p.stat().st_mode&0o777==0o600 for p in [combined,extracted,edited,inserted])
proof={'status':'PASS','installed_cli_workflows':6,'workdir':str(work),'input_preserved':True,'private_output_modes':True,'combine_extract_byte_identity':True}
print(json.dumps(proof))
import shutil
shutil.rmtree(work)
