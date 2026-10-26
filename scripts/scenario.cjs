const fs=require('node:fs'),path=require('node:path');
const {root,assert,equal,digest}=require('./transport.cjs'),{checkDecode,packet}=require('./oracle.cjs');
const ids=['clean','corrupt','erasures','ambiguous'],repo='mahdidaawsh-commits/residue-relay';
const values=id=>JSON.parse(fs.readFileSync(path.join(root,'tests',id+'-expected.json')));
function fixture(id,p,revision){const raw=fs.readFileSync(path.join(root,'fragments',id+'-'+p+'.json'));return {url:`https://raw.githubusercontent.com/${repo}/${revision}/fragments/${id}-${p}.json`,hash:digest(raw),source:JSON.parse(raw)};}
function args(id,revision){return [repo,id,[1,2,3,4,5].map(p=>fixture(id,p,revision).url),[1,2,3,4,5].map(p=>fixture(id,p,revision).hash),id==='ambiguous'?4:2];}
function plan(id){
 const step=(name,method,args=[],error)=>({name,label:id+'-'+name,method,args,...(error?{error:'[EXPECTED] '+error}:{})});
 const p=[step('first','collect',[[1,2]]),step('early','seal',[],'Five observations required'),step('second','collect',[[3,4,5]]),step('duplicate','collect',[[1]],'Position already observed'),step('seal','seal'),step('reseal','seal',[],'Cohort sealed')];
 if(id==='clean')p.push(step('unneeded','record_repair',[1],'No repair required'));
 if(id==='corrupt')p.push(step('repair-two','record_repair',[2]),step('duplicate-repair','record_repair',[2],'Repair already recorded'));
 if(id==='erasures')p.push(step('repair-two','record_repair',[2]),step('repair-four','record_repair',[4]),step('duplicate-repair','record_repair',[2],'Repair already recorded'));
 if(id==='ambiguous')p.push(step('blocked-repair','record_repair',[1],'Unique sealed reconstruction required'));
 return p;
}
function validateState(state,id,revision,recorded){
 const a=args(id,revision),config={repository:a[0],cohort:id,urls:a[2],hashes:a[3],fault_limit:a[4],prime:17};
 assert(equal(Object.keys(state).sort(),['configuration','observations','reconstruction','repairs'].sort()),'Exact state schema');
 assert(equal(state.configuration,config),'Immutable five-fragment configuration');
 const seen=new Set(recorded.flatMap(x=>x==='first'?[1,2]:x==='second'?[3,4,5]:[])),symbols=values(id);
 assert(equal(state.observations,[1,2,3,4,5].map(p=>seen.has(p)?{position:p,status:'OBSERVED',source:fixture(id,p,revision).source,value:symbols[p-1]}:{position:p,status:'UNSEEN'})),'Full source-linked raw observations and unseen slots');
 if(recorded.includes('seal'))checkDecode(symbols,config.fault_limit,state.reconstruction);
 else assert(equal(state.reconstruction,{status:'COLLECTING'}),'Unsealed analysis cannot replace persistent result');
 const positions=recorded.flatMap(x=>x==='repair-two'?[2]:x==='repair-four'?[4]:[]);
 assert(equal(state.repairs,positions.map(p=>packet(config,symbols,state.reconstruction,p))),'Exact append-only repair packets');
}
function queryPlan(id){return [...[0,1,2,3,4].map(limit=>({method:'probe',args:[limit]})),...(id==='ambiguous'?[]:[1,2,3,4,5].map(p=>({method:'repair_packet',args:[p]})))];}
function validateQuery(result,q,state){
 const symbols=state.observations.map(r=>r.value);
 if(q.method==='probe')checkDecode(symbols,q.args[0],result);
 else assert(equal(result,packet(state.configuration,symbols,state.reconstruction,q.args[0])),'Source-bound finite-field repair packet');
}
const cliArgs=args=>args.map(x=>Array.isArray(x)?JSON.stringify(x):String(x));
module.exports={ids,args,plan,validateState,queryPlan,validateQuery,cliArgs};
