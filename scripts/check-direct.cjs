const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {root}=require('./transport.cjs'),{checkDecode,packet}=require('./oracle.cjs');
const output=JSON.parse(fs.readFileSync(path.join(root,'proofs/direct-vm-export.json')));
assert.deepEqual(output.map(x=>x.case),['clean','corrupt','erasures','ambiguous']);
for(const x of output){
 const symbols=JSON.parse(fs.readFileSync(path.join(root,'tests',x.case+'-expected.json'))),state=x.state;
 assert.deepEqual(state.observations.map(r=>r.value),symbols);
 assert.equal(x.probes.length,5);x.probes.forEach((p,i)=>checkDecode(symbols,i,p));
 checkDecode(symbols,state.configuration.fault_limit,state.reconstruction);
 assert.equal(x.packets.length,x.case==='ambiguous'?0:5);
 x.packets.forEach((p,i)=>assert.deepEqual(p,packet(state.configuration,symbols,state.reconstruction,i+1)));
}
console.log('Actual GenVM exports match independent enumeration of all 4913 polynomials at every budget.');
