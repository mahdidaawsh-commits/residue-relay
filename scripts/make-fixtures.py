"""Reproduce the public synthetic corpus; never overwrite an existing fixture."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = {'clean':[9,1,14,14,1], 'corrupt':[9,8,14,14,1],
         'erasures':[9,'UNKNOWN',14,'UNKNOWN',1], 'ambiguous':[9,8,14,7,1]}
for cohort, values in CASES.items():
    for position, value in enumerate(values,1):
        prefix = f'Public synthetic GF(17) coded-record fragment. Cohort {cohort}; evaluation position {position}. '
        if value == 'UNKNOWN':
            text = prefix + 'An earlier draft proposed symbol six. That draft was withdrawn. The current final observation is erased: no final observed symbol is available. A downstream repair suggestion of one is not an observation and must not fill this erasure.'
        elif value == 1:
            text = prefix + 'An early draft said six, but that draft was cancelled. The signed final observed symbol is minus sixteen, equivalent to residue one modulo seventeen. A future repair proposal is not part of the observation.'
        else:
            words = {7:'seven',8:'eight',9:'nine',14:'fourteen'}
            text = prefix + f'A provisional note proposed six; it was superseded. The current final observed symbol is {words[value]} ({value}). Preserve this reported symbol even if a decoder later finds it inconsistent. A proposed repair must not replace this observation.'
        target = ROOT/'fragments'/f'{cohort}-{position}.json'
        raw = (json.dumps({'cohort':cohort,'position':position,'text':text},indent=2)+'\n').encode()
        if target.exists():
            assert target.read_bytes() == raw, 'Refusing to change pinned fixture'
        else: target.write_bytes(raw)
    target = ROOT/'tests'/f'{cohort}-expected.json'
    raw = (json.dumps(values)+'\n').encode()
    if target.exists(): assert target.read_bytes() == raw
    else: target.write_bytes(raw)
