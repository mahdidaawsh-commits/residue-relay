// Merge explicit completed workflow artifacts; never infer missing receipts.
const fs=require('node:fs'),path=require('node:path');
const {root,assert,equal,sourceHash,save}=require('./transport.cjs'),{ids}=require('./scenario.cjs');
const locations=process.argv.slice(2);assert(locations.length===ids.length,'Supply four artifact directories in scenario order');
const suite=[],hashes={};
locations.forEach((dir,i)=>{
 const absolute=path.resolve(dir),load=name=>JSON.parse(fs.readFileSync(path.join(absolute,name+'.json')));
 const deployment=load('suite'),journal=load('transactions'),verification=load('verification-'+ids[i]);
 assert(deployment.length===1&&deployment[0].id===ids[i]&&journal.source_sha256===sourceHash&&verification.source_sha256===sourceHash&&verification.live_state_match,'Successful source-bound scenario artifacts');
 suite.push(deployment[0]);
 for(const [label,hash] of Object.entries(journal.hashes)){assert(!(label in hashes),'Unique artifact labels');hashes[label]=hash;}
 for(const file of fs.readdirSync(absolute)){
  if(file.startsWith(ids[i]+'-')||file==='verification-'+ids[i]+'.json')fs.copyFileSync(path.join(absolute,file),path.join(root,'proofs',file));
 }
 fs.copyFileSync(path.join(absolute,'cloud-direct-tests.xml'),path.join(root,'proofs',ids[i]+'-cloud-direct-tests.xml'));
});
assert(suite.every(d=>d.fixture_revision===suite[0].fixture_revision),'One immutable fixture revision');
save('suite',suite);save('transactions',{source_sha256:sourceHash,hashes});
console.log('Merged four complete source-bound hosted artifact sets.');
