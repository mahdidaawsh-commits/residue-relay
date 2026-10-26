# ResidueRelay proof journal

Live scenario workflows are being prepared. No deployment or live-consensus result
is claimed by this placeholder. Synthetic fragment bytes are pinned by the revision
in `config/fixture-revision.txt` and checked against deployment commitments.

Every completed scenario must include deployment, two real nondeterministic
acquisitions, early sealing rejection, duplicate acquisition rejection, final seal,
reseal rejection, and its repair recording or blocked-repair calls. Receipts must
match exact signed calldata, source bytes, execution outcomes, full vote maps and
state after each call. A second read-only pass re-fetches code, receipts, final state
and all five fault-budget views, plus all repair packets where unique.
