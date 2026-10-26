// Independent exhaustive coefficient enumeration: no interpolation or triple decoder.
const crypto=require('node:crypto'),assert=require('node:assert/strict');
const equal=(a,b)=>assert.deepEqual(a,b);
const words=[];
for(let a=0;a<17;a++)for(let b=0;b<17;b++)for(let c=0;c<17;c++)words.push({coefficients:[a,b,c],codeword:[1,2,3,4,5].map(x=>(a+b*x+c*x*x)%17)});
function candidates(symbols,limit){
 const erasures=symbols.flatMap((y,i)=>y==='UNKNOWN'?[i+1]:[]);
 return words.flatMap(w=>{const mismatches=symbols.flatMap((y,i)=>y!=='UNKNOWN'&&y!==w.codeword[i]?[i+1]:[]),fault_weight=erasures.length+2*mismatches.length;
  return fault_weight<=limit?[{...w,erasures,mismatches,support:symbols.flatMap((y,i)=>y!=='UNKNOWN'&&y===w.codeword[i]?[i+1]:[]),fault_weight}]:[];});
}
function checkDecode(symbols,limit,result){
 equal(Object.keys(result).sort(),['limit','erasures','unique_bound','status','complete_list','candidates'].sort());
 const expected=candidates(symbols,limit),erasures=symbols.filter(y=>y==='UNKNOWN').length;
 equal(result.limit,limit);equal(result.erasures,erasures);equal(result.unique_bound,limit<=2);
 equal(result.status,expected.length===0?'OUTSIDE_BUDGET':expected.length===1?'RECOVERED':'AMBIGUOUS');
 const required=5-erasures-Math.floor((limit-erasures)/2),complete=erasures>limit||required>=3;
 equal(result.complete_list,complete);
 if(complete)equal(result.candidates,expected);
 else {
  equal(result.candidates.length,2);assert(expected.length>1);
  const keys=result.candidates.map(c=>JSON.stringify(c.coefficients));assert(new Set(keys).size===2);
  for(const c of result.candidates){const original=expected.find(e=>JSON.stringify(e.coefficients)===JSON.stringify(c.coefficients));assert(original);equal(c,original);}
  const sorted=result.candidates.slice().sort((a,b)=>a.coefficients[0]-b.coefficients[0]||a.coefficients[1]-b.coefficients[1]||a.coefficients[2]-b.coefficients[2]);equal(result.candidates,sorted);
 }
 return expected;
}
function packet(config,symbols,reconstruction,position){
 const coefficients=reconstruction.candidates[0].coefficients,[a,b,c]=coefficients,recovered=(a+b*position+c*position*position)%17,observed=symbols[position-1];
 return {cohort:config.cohort,position,source_sha256:config.hashes[position-1],observed,recovered,required:observed!==recovered,coefficients,
  polynomial_commitment:crypto.createHash('sha256').update('ResidueRelay-v1:'+config.cohort+':'+JSON.stringify(coefficients)).digest('hex')};
}
module.exports={candidates,checkDecode,packet};
