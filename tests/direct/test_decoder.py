import itertools
import random
import pytest
from support import F,WORDS,answer,verify

@pytest.mark.parametrize('constant',range(17))
def test_every_field_payload_round_trips(constant):
    for coeff,word in WORDS:
        if coeff[0]==constant:
            out = F['decode'](word,2)
            assert out['status']=='RECOVERED' and out['complete_list']
            assert out['candidates']==[F['candidate'](coeff,word)]

@pytest.mark.parametrize('coeff',[[0,0,0],[4,3,2],[16,16,16],[0,1,0],[8,0,9],[3,12,7],[15,2,6],[9,11,13]])
def test_every_single_corruption_and_erasure_pair(coeff):
    word = [F['evaluate'](coeff,x) for x in range(1,6)]
    for position in range(5):
        for offset in range(1,17):
            damaged = word.copy(); damaged[position]=(damaged[position]+offset)%17
            out = F['decode'](damaged,2)
            assert out['status']=='RECOVERED' and out['candidates'][0]['coefficients']==coeff
            assert out['candidates'][0]['mismatches']==[position+1]
    for positions in itertools.combinations(range(5),2):
        erased = word.copy()
        for p in positions: erased[p]='UNKNOWN'
        out = F['decode'](erased,2)
        assert out['status']=='RECOVERED' and out['candidates'][0]['coefficients']==coeff

@pytest.mark.parametrize('seed',range(32))
def test_independent_exhaustive_field_oracle_at_every_budget(seed):
    rng = random.Random(seed)
    symbols = [rng.choice(list(range(17))+['UNKNOWN']*5) for _ in range(5)]
    for limit in range(5): verify(symbols,limit,F['decode'](symbols,limit))

@pytest.mark.parametrize('case',['clean','corrupt','erasures','ambiguous'])
def test_all_fixture_budget_results_against_4913_polynomials(case):
    for limit in range(5): verify(answer(case),limit,F['decode'](answer(case),limit))

@pytest.mark.parametrize('symbols',[[0,'UNKNOWN','UNKNOWN','UNKNOWN','UNKNOWN'],[0,0,'UNKNOWN','UNKNOWN','UNKNOWN'],
    [9,'UNKNOWN',14,'UNKNOWN',1],['UNKNOWN']*5,[0,0,0,0,'UNKNOWN']])
def test_sparse_agreements_never_create_false_unique_decode(symbols):
    for limit in range(5): verify(symbols,limit,F['decode'](symbols,limit))

def test_looser_budget_is_not_a_uniqueness_claim():
    symbols = answer('erasures')
    assert F['decode'](symbols,2)['status']=='RECOVERED'
    out = F['decode'](symbols,4)
    assert out['status']=='AMBIGUOUS' and not out['complete_list']
    verify(symbols,4,out)

@pytest.mark.parametrize('bad',[True,False,None,17,-1,1.0,{},[], 'one'])
def test_values_require_canonical_residues_or_explicit_unknown(bad):
    assert not F['valid_values']([bad],1)
