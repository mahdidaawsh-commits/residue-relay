"""Export actual mocked GenVM execution for a separate exhaustive JS oracle."""
import json
import os
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests/direct'))
from support import CASES,deploy,acquire

def main():
    # Use pytest's proven loader fixture through the dedicated export test.
    import subprocess
    subprocess.run([sys.executable,'-m','pytest','tests/direct/test_export.py','-q'],cwd=ROOT,check=True,
                   env={**os.environ,'RESIDUE_EXPORT':'1'})
if __name__=='__main__': main()
