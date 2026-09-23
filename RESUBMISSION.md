# Reviewer resubmission: functional stale-claim reassessment

## Request addressed

The reviewer identified that a previously `CLEAR` claim could become stale after a newer claim for the same DAO and vendor was submitted. Version 1 could signal `NEW_RELEVANT_CLAIM_REQUIRES_REASSESSMENT`, but `assess_claim` accepted only `PENDING` claims and `retry_unresolved` reopened only `UNRESOLVED` claims. That left an unconsumed authorization without a complete reassessment path.

Version 2 removes that stranded state.

## Implemented state transition

When `submit_claim` stores a new claim, the same atomic transaction scans older claims for the same DAO and vendor. Every older claim that is both `CLEAR` and unconsumed is changed to:

- `status = PENDING`
- `reason_code = NEW_RELEVANT_CLAIM_REQUIRES_REASSESSMENT`
- `assessment_mode = REASSESSMENT`
- `revision = revision + 1`
- the new claim ID appended to `reassessment_scope`

Because the revision changes in the submission transaction, the treasury controller cannot consume the previous authorization between discovery and reopening.

`assess_claim` now accepts this reassessment state. It dynamically derives every same-DAO/same-vendor claim not already recorded in `compared_ids`, rather than trusting a caller-supplied list or only the first claim that caused reopening. A claim arriving while reassessment is pending extends the scope and increments revision again. An assessment using the older revision is rejected.

The reassessment can finish as:

- `CLEAR`: every newly relevant claim was evaluated and no material duplicate was found;
- `DUPLICATE`: overlap was found and authorization remains unavailable; or
- `UNRESOLVED`: evidence or consensus failed, and no authorization is available until a revision-aware retry succeeds.

Consumed claims are immutable and are never reopened.

## Automated proof

Run:

```text
python scripts/verify_local.py
```

The suite contains 21 tests, including the reviewer-specific cases:

1. a formerly clear claim is atomically reopened by a later relevant claim;
2. reassessment can restore it to clear and permit exact single-use consumption;
3. reassessment can revoke it as duplicate;
4. two later claims extend the scope and invalidate an in-flight stale revision;
5. unresolved reassessment preserves its scope for retry;
6. an already consumed claim is never reopened; and
7. a claim for another vendor does not trigger reassessment.

Local verification also runs GenVM lint and contract validation. The verified contract source is 12,580 bytes with SHA-256:

```text
a62ec2336f80239778ed5ab9dc29029f526faeed3fc09b393cd8d6d939b5e4ee
```

## Deployment evidence

The original version 1 deployment is historical evidence only. The matching version 2 source is deployed on Studionet at [`0xF6cF059A3bFa4e8F8B01Db976387f32324DBc477`](https://explorer-studio.genlayer.com/address/0xF6cF059A3bFa4e8F8B01Db976387f32324DBc477). Completed reviewer-path, multi-arrival and duplicate-revocation evidence is linked in [`docs/studionet-v2-evidence.md`](docs/studionet-v2-evidence.md).
