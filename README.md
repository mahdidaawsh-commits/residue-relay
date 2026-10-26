# ResidueRelay

**Consensus interpretation of public coded fragments, followed by exact bounded-error reconstruction.**

A reusable small GenLayer primitive for reading prose archive fragments whose final
observations may differ from drafts or proposed repairs. Five independently committed
reports represent evaluations of a degree-at-most-two polynomial over GF(17). The
three coefficients are a public record. This is not encryption or secret sharing.

## What makes the result consequential

Anyone acquires previously unseen fragments in atomic batches. Leader and validators
fetch the complete commit-pinned documents themselves, check SHA-256 and identity,
and independently interpret each final observed symbol. Exact normalized observations
must agree. Validators also audit every decision against the full text, including
explicit missing values. They never infer observations by fitting a codeword.

The agreed observations feed an exact finite-field decoder. A unique compatible
record enables source-bound repair packets; ambiguous records block repairs. A wrong
AI extraction can therefore change the reconstructed payload, exclusions and repair
authorization. Consensus is material to the state transition.

## Public workflow

1. Deploy with a fixed repository, cohort, five distinct commit-pinned fragment URLs,
   five SHA-256 hashes and fault-weight limit 0–4.
2. `collect(positions)` fetches and interprets unseen positions. An unacquired slot
   stays `UNSEEN`; a fetched but unavailable observation is `UNKNOWN`.
3. After all five acquisitions, `probe(limit)` examines a counterfactual budget.
4. `seal()` freezes reconstruction under the configured budget once.
5. `repair_packet(position)` returns a reproducible polynomial commitment and recovered
   symbol only for a unique sealed result. `record_repair(position)` records a needed
   repair once without changing the raw observation or external document.

There is no owner role, proposal graph, service certificate, transfer of money or
claim that a publisher actually applied a repair.

## Decoder and ambiguity

For a candidate polynomial, `fault_weight = 2*mismatches + erasures`. Five evaluations
and three coefficients give the standard uniqueness guarantee through weight two.
The decoder reports `RECOVERED`, `OUTSIDE_BUDGET` or `AMBIGUOUS` relative to the chosen
budget. A result does not establish that the real original record obeys that budget.

When every compatible candidate must agree with at least three known positions,
all known triples are interpolated and filtered, yielding the complete candidate
list. If fewer than three agreements are required, triple search is incomplete:
the contract instead exhibits two distinct compatible polynomials and explicitly
sets `complete_list=false`. It never calls that family a unique decode.

The familiar [Reed–Solomon error/erasure bound](https://web.mit.edu/6.02/www/f2009/handouts/lectures/L8.pdf)
and finite-field interpolation are existing mathematics. The contribution is the
source-acquisition, exact consensus, partial-observation lifecycle and repair-gating
composition. See [architecture and trust model](docs/architecture.md).

## Scenarios and reproducibility

The synthetic payload `[4,3,2]` evaluates to `[9,1,14,14,1]`:

| Cohort | Observed symbols | Configured limit | Expected result |
|---|---|---:|---|
| clean | 9,1,14,14,1 | 2 | unique; no repair |
| corrupt | 9,8,14,14,1 | 2 | unique; repair position 2 to 1 |
| erasures | 9,UNKNOWN,14,UNKNOWN,1 | 2 | unique; repair positions 2 and 4 |
| ambiguous | 9,8,14,7,1 | 4 | ten compatible records; repair blocked |

The erasure case becomes ambiguous at counterfactual limit four. This checks the
important sparse-agreement boundary rather than assuming more tolerance is safe.

```sh
python -m pip install -r requirements-dev.txt
genvm-lint download --version v0.2.16
genvm-lint check contracts/residue_relay.py --json
python -m pytest tests/direct -q
node --test tests/rpc-preflight.test.cjs
python scripts/export-direct.py
node scripts/check-direct.cjs
```

Tests include all 4,913 payloads, 640 single-symbol corruptions, 80 two-erasure
patterns, random full-field exhaustive oracle comparisons, actual GenVM storage
execution, independent validator replay, source failures, and rollback checks.
The separate JS oracle enumerates all coefficient triples without interpolation.
Direct tests mock web and LLM responses; live workflows exercise actual consensus.

The pinned runner is declared in the source. Node 24 and Python 3.13 are used in CI.
Generic CLI transport is reused under MIT; the algebraic decoder, scenarios,
validator criteria and oracle are specific to this primitive.

[Contract source](contracts/residue_relay.py) · [Live proof journal](proofs/README.md)

## Limits

The corpus and field are deliberately small, bounded and public. Hashes establish
committed bytes, not publisher honesty. LLM agreement cannot prove external truth.
Prose can be adversarial; exact independent extraction and a second audit reduce,
but do not eliminate, interpretation failures. Missing fetches fail the whole batch;
they do not silently become erasures. A wrong fault assumption can yield a unique
compatible record that differs from the original. Repair packets are public records,
not evidence of external application. StudioNet deployment is a test-network result.
