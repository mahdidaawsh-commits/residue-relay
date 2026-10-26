const fs=require('node:fs'),path=require('node:path');
const {root,assert,equal,sourceHash,invoke,read,rpc,receipt,save}=require('./transport.cjs');
const {ids,args,plan,validateState,queryPlan,validateQuery,cliArgs}=require('./scenario.cjs');
async function main(){
 const id=process.env.RESIDUE_SCENARIO;assert(ids.includes(id),'Select a complete coded-record scenario');
 const accounts=JSON.parse(process.env.RESIDUE_ACCOUNTS||'[]');assert(accounts.length===1,'One disposable CLI caller');
 const account=accounts[0];process.env.RESIDUE_ACCOUNT=account.name;
 assert(await rpc('eth_chainId',[])==='0xf22f','StudioNet only');
 const revision=fs.readFileSync(path.join(root,'config/fixture-revision.txt'),'utf8').trim();
 const hash=await invoke(id+'-deployment',['deploy','--contract','contracts/residue_relay.py','--args',...cliArgs(args(id,revision))]);
 const deployed=await receipt(id+'-deployment',hash,true),contract=deployed.to_address||deployed.recipient;assert(/^0x[a-fA-F0-9]{40}$/.test(contract),'Actual deployed address');
 save('suite',[{id,network:'studionet',chain_id:61999,contract,deployment:hash,caller:account.address,args:args(id,revision),fixture_revision:revision,source_sha256:sourceHash}]);
 let before=await read(id+'-initial',['call',contract,'get_state']);const recorded=[],trace=[];
 validateState(before,id,revision,recorded);save(id+'-initial-state',before);
 for(const item of plan(id)){
  const h=await invoke(item.label,['write',contract,item.method,...(item.args.length?['--args',...cliArgs(item.args)]:[])]);
  await receipt(item.label,h,!item.error);
  const state=await read(item.label+'-state',['call',contract,'get_state']);
  if(item.error)assert(equal(before,state),'Full rejected-call rollback');else recorded.push(item.name);
  validateState(state,id,revision,recorded);trace.push({...item,transaction:h,state_before:before,state});save(id+'-trace',trace);before=state;
 }
 save(id+'-final-state',before);const queries=[];
 for(const q of queryPlan(id)){
  const result=await read(id+'-query-'+queries.length,['call',contract,q.method,'--args',...cliArgs(q.args)]);
  validateQuery(result,q,before);queries.push({...q,result});save(id+'-queries',queries);
 }
 console.log('PASSED '+id+': '+(trace.length+1)+' finalized receipts and '+queries.length+' exhaustive-oracle views');
}
main().catch(e=>{console.error(e.stack);process.exitCode=1;});
