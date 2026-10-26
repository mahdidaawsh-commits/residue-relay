import json
import os
import pytest
from support import ROOT,CASES,deploy,acquire

@pytest.mark.parametrize('case',CASES)
def test_actual_vm_export(direct_vm,direct_deploy,case):
    c=deploy(direct_deploy,case)
    acquire(c,direct_vm,case,[1,2]); acquire(c,direct_vm,case,[3,4,5]); c.seal()
    result={'case':case,'state':c.get_state(),'probes':[c.probe(i) for i in range(5)],
            'packets':[] if case=='ambiguous' else [c.repair_packet(i) for i in range(1,6)]}
    if os.environ.get('RESIDUE_EXPORT')=='1':
        target=ROOT/'proofs/direct-vm-export.json'
        output=[] if case==CASES[0] else json.loads(target.read_text())
        output.append(result)
        target.write_text(json.dumps(output,indent=2)+'\n')
