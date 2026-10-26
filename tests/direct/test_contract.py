import hashlib
import json
import re
import pytest
from support import F,CASES,answer,record,deploy,mocks,acquire,verify

@pytest.mark.parametrize('case',CASES)
def test_atomic_slots_full_sources_seal_all_budget_views_and_repairs(direct_vm,direct_deploy,case):
    c = deploy(direct_deploy,case)
    acquire(c,direct_vm,case,[2,1])
    before = c.get_state()
    assert [r['status'] for r in before['observations']]==['OBSERVED','OBSERVED','UNSEEN','UNSEEN','UNSEEN']
    with direct_vm.expect_revert('Five observations required'): c.seal()
    assert c.get_state()==before
    acquire(c,direct_vm,case,[5,3,4])
    before = c.get_state()
    for p,row in enumerate(before['observations'],1):
        assert row['source']==json.loads(record(case,p)[2]) and row['value']==answer(case)[p-1]
    for limit in range(5): verify(answer(case),limit,c.probe(limit))
    with direct_vm.expect_revert('Position already observed'): c.collect([1])
    assert c.get_state()==before
    c.seal()
    state = c.get_state()
    verify(answer(case),state['configuration']['fault_limit'],state['reconstruction'])
    with direct_vm.expect_revert('Cohort sealed'): c.seal()
    with direct_vm.expect_revert('Cohort sealed'): c.collect([3])
    assert c.get_state()==state
    if case=='ambiguous':
        with direct_vm.expect_revert('Unique sealed reconstruction required'): c.record_repair(1)
    else:
        for p in range(1,6):
            packet = c.repair_packet(p)
            assert packet['coefficients']==[4,3,2] and packet['observed']==answer(case)[p-1]
            assert packet['source_sha256']==record(case,p)[1]
            assert packet['polynomial_commitment']==hashlib.sha256(('ResidueRelay-v1:'+case+':[4,3,2]').encode()).hexdigest()
            if packet['required']:
                c.record_repair(p)
                with direct_vm.expect_revert('Repair already recorded'): c.record_repair(p)
            else:
                with direct_vm.expect_revert('No repair required'): c.record_repair(p)
        assert c.get_state()['observations']==before['observations']

def test_permissionless_acquisition_and_recording(direct_vm,direct_deploy,direct_accounts):
    c = deploy(direct_deploy,'corrupt')
    direct_vm.sender = direct_accounts[1]; acquire(c,direct_vm,'corrupt',[1,2])
    direct_vm.sender = direct_accounts[2]; acquire(c,direct_vm,'corrupt',[3,4,5])
    c.seal(); c.record_repair(2)
    assert c.get_state()['repairs'][0]['recovered']==1

@pytest.mark.parametrize('p',range(5))
def test_every_independent_symbol_disagreement_rejected(direct_vm,direct_deploy,p):
    c = deploy(direct_deploy); acquire(c,direct_vm)
    values = answer(); values[p]=(values[p]+1)%17
    mocks(direct_vm,values={'values':values})
    assert direct_vm.run_validator() is False

@pytest.mark.parametrize('p',range(5))
def test_every_faithfulness_audit_flag_required(direct_vm,direct_deploy,p):
    c = deploy(direct_deploy); acquire(c,direct_vm)
    flags = [True]*5; flags[p]=False
    mocks(direct_vm,audit={'supported':flags})
    assert direct_vm.run_validator() is False

def test_unknown_is_supported_but_imputation_and_erasing_known_value_rejected(direct_vm,direct_deploy):
    c = deploy(direct_deploy,'erasures'); acquire(c,direct_vm,'erasures')
    source = [r['source'] for r in c.get_state()['observations']]
    for p,value in [(1,1),(0,'UNKNOWN')]:
        values = answer('erasures'); values[p]=value
        assert direct_vm.run_validator(leader_result={'sources':source,'values':values}) is False

def test_corrupted_observation_is_preserved_instead_of_model_repair(direct_vm,direct_deploy):
    c = deploy(direct_deploy,'corrupt'); acquire(c,direct_vm,'corrupt')
    values = answer('corrupt'); values[1]=1
    source = [r['source'] for r in c.get_state()['observations']]
    assert direct_vm.run_validator(leader_result={'sources':source,'values':values}) is False

def test_validator_refetch_error_equivalence_and_no_model_error_consensus(direct_vm,direct_deploy):
    c = deploy(direct_deploy); acquire(c,direct_vm)
    mocks(direct_vm,raws={2:b'changed'})
    assert direct_vm.run_validator() is False
    assert direct_vm.run_validator(leader_error=Exception('[EXTERNAL] Fragment commitment mismatch')) is True
    mocks(direct_vm,status=503)
    assert direct_vm.run_validator(leader_error=Exception('[TRANSIENT] Fragment unavailable')) is True
    mocks(direct_vm,values={})
    assert direct_vm.run_validator(leader_error=Exception('[LLM_ERROR] Invalid complete observations')) is False

@pytest.mark.parametrize('bad',[{}, {'values':[]},{'values':[None]*5},{'values':[True]*5},{'values':[17]*5}])
def test_bad_model_never_partially_acquires(direct_vm,direct_deploy,bad):
    c = deploy(direct_deploy); before = c.get_state(); mocks(direct_vm,values=bad)
    with direct_vm.expect_revert('Invalid complete observations'): c.collect([1,2,3,4,5])
    assert c.get_state()==before

@pytest.mark.parametrize('mutation',['identity','position','duplicate','oversize','json','text'])
def test_invalid_second_source_rolls_back_whole_batch(direct_vm,direct_deploy,mutation):
    source = json.loads(record('clean',2)[2])
    if mutation=='identity': source['cohort']='other'
    if mutation=='position': source['position']=3
    if mutation=='text': source['text']=''
    raw = json.dumps(source).encode()
    if mutation=='duplicate': raw=b'{"cohort":"clean","cohort":"clean"}'
    if mutation=='oversize': raw=b'x'*6001
    if mutation=='json': raw=b'not json'
    hashes=[record('clean',p)[1] for p in range(1,6)]; hashes[1]=hashlib.sha256(raw).hexdigest()
    c=deploy(direct_deploy,hashes=hashes); before=c.get_state()
    mocks(direct_vm,positions=[1,2],raws={2:raw})
    with direct_vm.expect_revert('EXTERNAL'): c.collect([1,2])
    assert c.get_state()==before

def test_schema_repair_keeps_explicit_erasures(direct_vm,direct_deploy):
    c=deploy(direct_deploy,'erasures')
    mocks(direct_vm,'erasures')
    direct_vm.clear_mocks()
    for p in range(1,6): direct_vm.mock_web(re.escape(record('erasures',p)[0]),{'status':200,'body':record('erasures',p)[2]})
    direct_vm.mock_llm(r'(?s)^(?!.*Previous invalid response:).*RESIDUERELAY-EXTRACT.*','{"values":[null]}')
    direct_vm.mock_llm(r'(?s).*RESIDUERELAY-EXTRACT.*Previous invalid response:.*',json.dumps({'values':answer('erasures')}))
    direct_vm.mock_llm(r'.*RESIDUERELAY-AUDIT.*','{"supported":[true,true,true,true,true]}')
    c.collect([1,2,3,4,5]); assert direct_vm.run_validator() is True
    assert c.get_state()['observations'][1]['value']=='UNKNOWN'

@pytest.mark.parametrize('positions',[[],[0],[6],[1,1],[True]])
def test_invalid_collection_positions(direct_vm,direct_deploy,positions):
    c=deploy(direct_deploy)
    with direct_vm.expect_revert('Distinct bounded positions required'): c.collect(positions)

@pytest.mark.parametrize('override',[{'fault_limit':-1},{'fault_limit':5},{'repository':'../bad'},
    {'urls':['https://example.com/x']*5},{'hashes':['0'*64]*5}])
def test_invalid_scope_and_commitments(direct_vm,direct_deploy,override):
    with direct_vm.expect_revert('EXPECTED'): deploy(direct_deploy,**override)

@pytest.mark.parametrize('limit',[-1,5,True])
def test_probe_rejects_unbounded_or_boolean_budget(direct_vm,direct_deploy,limit):
    c=deploy(direct_deploy)
    with direct_vm.expect_revert('Invalid fault limit'): c.probe(limit)

@pytest.mark.parametrize('position',[-1,0,6,True])
def test_repair_rejects_invalid_position(direct_vm,direct_deploy,position):
    c=deploy(direct_deploy)
    with direct_vm.expect_revert('Invalid repair position'): c.repair_packet(position)

@pytest.mark.parametrize('flag',['true',1,None,False])
def test_audit_requires_actual_true_not_truthiness(direct_vm,direct_deploy,flag):
    c=deploy(direct_deploy); acquire(c,direct_vm)
    mocks(direct_vm,audit={'supported':[flag,True,True,True,True]})
    assert direct_vm.run_validator() is False
