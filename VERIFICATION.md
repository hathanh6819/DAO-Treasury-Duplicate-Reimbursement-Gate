# Verification record

Local release gate on 2026-09-15:

- Direct Mode: `16 passed`.
- GenVM lint: `3 checks passed`.
- GenVM validation: `7 methods` (`3 view`, `4 write`).
- Exact source: `10,654 bytes`.
- SHA-256: `5b7177db86d74d5f8f2336d3fa8486dfe35efc3137199b6289262c2dd1ead781`.
- Studionet deployment `0x8B1c24CA1340aCdC37008A665b9B332E74cD0183` completed the two-wallet safe/consume/replay and semantic duplicate/block lifecycles. See `docs/studionet-evidence.md`.

Tests execute contract logic and mock only validator model output. They prove bounded semantic duplicate results, the first-obligation path, independent-claim consume, exact invoice replay, malformed/incomplete/identity-swapped model output, recovery, actor/revision/action binding, new-claim race, expiry, comparator limit and prompt-injection rejection.

Important limitation: the invoice digest is committed by the DAO authority but invoice bytes are not fetched or authenticated by the contract. The gate's claim concerns duplicate **registered obligations**, not objective invoice authenticity or actual payment prevention absent treasury integration.
