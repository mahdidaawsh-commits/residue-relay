# ResidueRelay proof journal

**Four completed gasless CLI StudioNet suites: 35 finalized MAJORITY_AGREE receipts,
19 successful executions, 16 intended rejections, and 35 independently checked views.**
Every receipt has a strict majority. Recorded votes total 120 agree, zero disagree,
and 55 idle; idle votes are retained and are not counted as agreement.

Primary demonstration: [one-corruption recovery contract](https://explorer-studio.genlayer.com/address/0xD11B6AFD5C50075C1b72162Cd678698bcfe88f3a).
All instances run the same source; they are scenario proofs of one primitive.

| Case | Contract | Sealed result | Recorded repairs | Receipts / views |
|---|---|---|---|---|
| Clean | [0x2DD23AfEE03a9aEC3b1508962d7FFc0293a974CA](https://explorer-studio.genlayer.com/address/0x2DD23AfEE03a9aEC3b1508962d7FFc0293a974CA) | RECOVERED, coefficients 4/3/2 | none | 8 / 10 |
| One corrupted symbol | [0xD11B6AFD5C50075C1b72162Cd678698bcfe88f3a](https://explorer-studio.genlayer.com/address/0xD11B6AFD5C50075C1b72162Cd678698bcfe88f3a) | RECOVERED, position 2 differs | position 2 → 1 | 9 / 10 |
| Two erasures | [0x9f2A4CACFa3dF80FfA7f86EE61c8312a42CCE1b3](https://explorer-studio.genlayer.com/address/0x9f2A4CACFa3dF80FfA7f86EE61c8312a42CCE1b3) | RECOVERED, weight 2 | positions 2 → 1, 4 → 14 | 10 / 10 |
| Conflicting candidates | [0x3E4cD7092C72A2DDa8590317602c9fc9fF7b9697](https://explorer-studio.genlayer.com/address/0x3E4cD7092C72A2DDa8590317602c9fc9fF7b9697) | AMBIGUOUS, all ten compatible records | blocked | 8 / 5 |

The two-erasure counterfactual at weight limit four returns two ambiguity witnesses
with `complete_list=false`; the independent oracle confirms additional compatible
records exist. The conflicting-candidates case is OUTSIDE_BUDGET at limit two.

Source SHA-256: `7bda9b6ac4606cc2fc9a3afe58ebc11f978ca6de8ef087b5c2e7b39089f5e7d3`.
Fixture revision: `2e2eb5085356a542432b3a7743a05a58f79ad48e`.
Workflow revision: `58a5a0ea4b6d78583488d84cc231ae218fa31946`.
Synthetic fragment bytes are pinned by `config/fixture-revision.txt` and checked
against every deployment's actual decoded constructor arguments.

[All transaction links](transactions.md) · [aggregate verification](verification.json) ·
[local offline replay](offline-verification.json) · [workflow/artifact provenance](provenance.json).

Fresh receipt, deployed-code, final-state and view RPC checks were performed by each
hosted workflow at the timestamps in its verification report. Local offline replay
then checked the downloaded receipts, signed calldata, full state transitions, exact
rejection bytes and finite-field witnesses. The aggregate merges those checks; it
does not claim a separate later local fresh-RPC query.

Hosted workflows: [clean](https://github.com/mahdidaawsh-commits/residue-relay/actions/runs/40279795989),
[corrupt](https://github.com/mahdidaawsh-commits/residue-relay/actions/runs/40279802124),
[erasures](https://github.com/mahdidaawsh-commits/residue-relay/actions/runs/40279807916),
[ambiguous](https://github.com/mahdidaawsh-commits/residue-relay/actions/runs/40279815612).
Each also passed GenVM lint, 131 direct tests, seven transport tests and the separate
JavaScript exhaustive-field check against actual mocked GenVM exports.

Every completed scenario must include deployment, two real nondeterministic
acquisitions, early sealing rejection, duplicate acquisition rejection, final seal,
reseal rejection, and its repair recording or blocked-repair calls. Receipts must
match exact signed calldata, source bytes, execution outcomes, full vote maps and
state after each call. A second read-only pass re-fetches code, receipts, final state
and all five fault-budget views, plus all repair packets where unique.

To replay the published proof set locally with Node 24:

```sh
npm ci --ignore-scripts --no-audit --no-fund
GENLAYER_CLI_PATH="$PWD/node_modules/genlayer/dist/index.js" node scripts/verify-proofs.cjs --offline
node scripts/summarize-hosted.cjs
```

The source/fixture pin predates these live runs. No rejected or superseded live
attempt is omitted: these four are the complete live scenario set for this source.
All data are synthetic public fragments. A unique compatible codeword is conditional
on the fault assumption and does not establish publisher honesty or external repair.
