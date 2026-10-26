// Generate a new transaction index from verified receipts, not manually typed hashes.
const fs=require('node:fs'),path=require('node:path');
const {root,assert}=require('./transport.cjs');
const report=JSON.parse(fs.readFileSync(path.join(root,'proofs/verification.json')));
assert(report.local_offline_replay_checked&&report.transactions.length===35,'Complete verified receipt set required');
const lines=['# All ResidueRelay StudioNet transactions','','One source, four independent scenario deployments. Every row finalized with a strict','`MAJORITY_AGREE`; ERROR rows are intended public-method rejections with unchanged state.','',
 '| Call | Transaction | Execution | Agree / disagree / idle |','|---|---|---|---|'];
for(const t of report.transactions)lines.push(`| ${t.label} | [${t.hash}](https://explorer-studio.genlayer.com/tx/${t.hash}) | ${t.execution} | ${t.agree} / ${t.disagree} / ${t.idle} |`);
lines.push('','[Full verification](verification.json) · [Source-bound suite](suite.json) · [Proof explanation](README.md)','');
const target=path.join(root,'proofs/transactions.md'),text=lines.join('\n');
if(fs.existsSync(target))assert(fs.readFileSync(target,'utf8')===text,'Transaction index already exists and differs');
else fs.writeFileSync(target,text);
