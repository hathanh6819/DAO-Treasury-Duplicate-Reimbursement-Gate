# DAO Treasury Duplicate Reimbursement Gate

A contract-only GenLayer gate for one narrow treasury problem: the same DAO vendor billing substantially the same work twice under changed invoice numbers, wording, payment token, beneficiary, amount or service period.

Verified Studionet deployment: [`0x8B1c24CA1340aCdC37008A665b9B332E74cD0183`](https://explorer-studio.genlayer.com/address/0x8B1c24CA1340aCdC37008A665b9B332E74cD0183). See [live evidence](docs/studionet-evidence.md).

## Proof obligation

The contract can establish whether a **new DAO-authorized, sealed reimbursement claim** materially overlaps other claims registered for the same DAO/vendor. It cannot establish whether the off-chain invoice is genuine, whether a vendor has concealed work under another vendor identity, or whether an external Safe actually executed payment. The registered DAO authority is accountable for invoice and vendor identity; the controller must independently verify the exact external payment action before using the returned authorization. A Safe/module/treasury adapter must call this gate on its actual execution path if blocking payment is required. This contract never transfers or custodies assets.

## Mechanism

- Constructor binds a DAO authority (test wallet A) and a separate treasury controller (test wallet B). The deployer has no subsequent lifecycle role.
- Authority seals DAO/vendor, beneficiary, token, amount, period, invoice SHA-256 commitment, work summary, payment action SHA-256 commitment and deadline in one immutable claim digest. Exact invoice-digest replay is rejected before state creation.
- Assessment compares the candidate with **all** previously registered claims for the same DAO/vendor, including different tokens and periods. More than eight comparators fails closed rather than silently truncating coverage.
- GenLayer validators reach strict consensus on bounded per-prior-claim findings. Deterministic code checks exact identity, every prior ID exactly once, boolean types, full coverage and derives `CLEAR`, `DUPLICATE` or `UNRESOLVED`.
- Only `CLEAR` can be consumed by the exact controller/revision/action digest before expiry. Consumption is single-use. A later relevant claim appearing before consumption blocks the earlier authorization.
- Missing or malformed model output becomes `UNRESOLVED` with no authorization; revision-aware retry is available.

The first registered vendor obligation is `CLEAR` deterministically because there is no prior registered obligation to compare. This is **not** a statement that the invoice itself is authentic.

## Verification

Run `python scripts/verify_local.py`. The local gate currently passes 16 tests plus GenVM lint and validation; see [VERIFICATION.md](VERIFICATION.md). Tests cover legitimate clear/consume, semantic duplicate, changed token/period, invalid inputs, duplicate invoice, model identity/coverage/schema failure, unresolved recovery, actor/revision failure, new-claim race, expiry, comparator bound, prompt injection and replay. Direct Mode mocks only the nondeterministic model boundary and executes the real contract logic.

## Deployment

Deploy `contracts/dao_treasury_duplicate_reimbursement_gate.py` on Studionet with exactly two constructor arguments:

1. `dao_authority`: test wallet A (`0x1D283b45974B0be9630DFD1deC6A62a9B72B2760`)
2. `treasury_controller`: test wallet B (`0xf96Cf822F9f4e76956AB9fAAa22B3BdCD7b10aD6`)

Do not use a live DAO, real invoices, or real payments for the synthetic lifecycle. The two supplied test keys must not be committed. The deployment wallet signs only deployment; wallet A submits synthetic claims, and wallet B attempts/consumes authorizations. Send the deployed contract address before live testing.
