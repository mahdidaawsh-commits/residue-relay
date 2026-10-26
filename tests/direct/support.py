import ast
import hashlib
import itertools
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT/'contracts/residue_relay.py'
REPO = 'mahdidaawsh-commits/residue-relay'
CASES = ['clean','corrupt','erasures','ambiguous']

def pure():
    names = {'integer','valid_values','evaluate','interpolate','candidate','decode'}
    tree = ast.parse(SOURCE.read_text())
    ns = {'PRIME':17}
    exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(SOURCE),'exec'),ns)
    return ns

F = pure()
WORDS = [(list(c),[(c[0]+c[1]*x+c[2]*x*x)%17 for x in range(1,6)]) for c in itertools.product(range(17),repeat=3)]

def answer(case='clean'):
    return json.loads((ROOT/'tests'/(case+'-expected.json')).read_text())

def record(case,position):
    raw = (ROOT/'fragments'/f'{case}-{position}.json').read_bytes()
    return f'https://raw.githubusercontent.com/{REPO}/'+ 'a'*40+f'/fragments/{case}-{position}.json',hashlib.sha256(raw).hexdigest(),raw

def deploy(factory,case='clean',**kwargs):
    params = {'repository':REPO,'cohort':case,'urls':[record(case,p)[0] for p in range(1,6)],
              'hashes':[record(case,p)[1] for p in range(1,6)],'fault_limit':4 if case=='ambiguous' else 2}
    params.update(kwargs)
    return factory(str(SOURCE),**params)

def mocks(vm,case='clean',positions=None,values=None,audit=None,raws=None,status=200):
    positions = list(range(1,6)) if positions is None else positions
    vm.clear_mocks()
    for p in range(1,6):
        vm.mock_web(re.escape(record(case,p)[0]),{'status':status,'body':(raws or {}).get(p,record(case,p)[2])})
    vm.mock_llm(r'.*RESIDUERELAY-EXTRACT.*',json.dumps({'values':[answer(case)[p-1] for p in positions]} if values is None else values))
    vm.mock_llm(r'.*RESIDUERELAY-AUDIT.*',json.dumps({'supported':[True]*len(positions)} if audit is None else audit))

def acquire(c,vm,case='clean',positions=None):
    positions = list(range(1,6)) if positions is None else positions
    mocks(vm,case,positions)
    c.collect(positions)
    assert vm.run_validator() is True

def oracle(symbols,limit):
    erased = [i+1 for i,y in enumerate(symbols) if y=='UNKNOWN']
    results = []
    for coeff,word in WORDS:
        mismatch = [i+1 for i,y in enumerate(symbols) if y!='UNKNOWN' and y!=word[i]]
        weight = len(erased)+2*len(mismatch)
        if weight<=limit:
            results.append({'coefficients':coeff,'codeword':word,'erasures':erased,'mismatches':mismatch,
                            'support':[i+1 for i,y in enumerate(symbols) if y!='UNKNOWN' and y==word[i]],'fault_weight':weight})
    return results

def verify(symbols,limit,result):
    expected = oracle(symbols,limit)
    assert result['limit']==limit and result['erasures']==symbols.count('UNKNOWN')
    assert result['unique_bound']==(limit<=2)
    assert result['status']==('OUTSIDE_BUDGET' if not expected else 'RECOVERED' if len(expected)==1 else 'AMBIGUOUS')
    if result['complete_list']:
        assert result['candidates']==expected
    else:
        assert len(expected)>1 and len(result['candidates'])==2
        assert result['candidates'][0]['coefficients']<result['candidates'][1]['coefficients']
        assert all(c in expected for c in result['candidates'])
