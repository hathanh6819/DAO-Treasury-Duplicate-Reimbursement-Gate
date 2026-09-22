# Scope and adversarial audit specification

## Version 2 reassessment invariant

For every unconsumed claim `C` with status `CLEAR`, submission of a later claim with the same normalized DAO and vendor identity atomically makes `C` non-consumable, increments `C.revision`, and adds the later claim to `C.reassessment_scope`. `C` may return to `CLEAR` only after validator comparison covers every same-identity claim absent from `C.compared_ids`. Claims submitted during an open reassessment extend the scope and invalidate the earlier expected revision. Consumed claims and claims for other vendors are never reopened.

## Claim

`CLEAR` means no material overlap was found against the complete bounded set of previously DAO-sealed obligations for the same DAO/vendor. `DUPLICATE` means at least one per-prior finding reports material overlap or same work in the same period. `UNRESOLVED` means the semantic judgment cannot be safely established.

## Trust boundaries

- DAO authority authenticates submission to this contract, not invoice truth.
- Invoice digest is a commitment supplied by that authority. The contract does not fetch invoice bytes, so it does not claim fetched-content integrity or external invoice provenance.
- Work summaries are immutable on-chain inputs to validators and are treated as inert evidence, not instructions.
- The model cannot grant payment authority. Only deterministic state and the registered controller can consume authorization.
- This contract is a gate, not a Safe module. No external transfer is prevented without mandatory integration into the treasury execution path.

## Negative sequences

1. Exact invoice digest repeated for same DAO → rejected with count unchanged.
2. Same work reworded, split amount or changed token/period → compared and duplicate-blocked.
3. Model omits a prior ID, adds an ID, duplicates one, returns a string boolean or says coverage incomplete → `UNRESOLVED`.
4. Authority or outsider tries controller consume → unchanged state.
5. Controller supplies wrong digest, expired revision or repeats a consumed authorization → unchanged state.
6. A new same-vendor claim appears after `CLEAR` but before consume → old authorization is atomically reopened and cannot be consumed until every new relevant claim is assessed.
7. More than eight same-vendor claims → new submission fails closed; no silent comparison truncation.

## Live evidence requirement

For every Studionet transaction record hash, finality, execution result, consensus result, returned code, and complete relevant before/after `get_claim`/`get_count` readbacks. A finalized transaction with `ERROR` is not a successful test unless rollback and unchanged state are proven. Separate synthetic fixtures from real-world claims.
