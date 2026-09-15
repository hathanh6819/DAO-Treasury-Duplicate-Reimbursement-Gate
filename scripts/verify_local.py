from __future__ import annotations
import hashlib,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"contracts"/"dao_treasury_duplicate_reimbursement_gate.py"
def run(args):
    print("$ "+" ".join(args),flush=True)
    subprocess.run(args,cwd=ROOT,check=True)
run([sys.executable,"-m","pytest","-q","-p","no:cacheprovider"])
run([sys.executable,"-X","utf8","-m","genvm_linter.cli","check",str(SOURCE.relative_to(ROOT))])
body=SOURCE.read_bytes()
print("source_bytes="+str(len(body)))
print("source_sha256="+hashlib.sha256(body).hexdigest())
