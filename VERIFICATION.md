# Verification record

Local v2 release gate on 2026-09-22:

- Direct Mode: `21 passed`.
- GenVM lint: `3 checks passed`.
- GenVM validation: `7 methods` (`3 view`, `4 write`).
- Exact source: `12,580 bytes`.
- SHA-256: `a62ec2336f80239778ed5ab9dc29029f526faeed3fc09b393cd8d6d939b5e4ee`.
- The v1 Studionet deployment remains historical evidence only. The v2 fix requires a fresh Studio Next deployment and reassessment lifecycle before resubmission.

Tests execute contract logic and mock only validator model output. They additionally prove atomic reopening of stale `CLEAR` claims, comparison against every later relevant claim, revision invalidation during multi-arrival races, both restoration and revocation after reassessment, unresolved reassessment retry, consumed-claim immutability and unrelated-vendor isolation.

Important limitation: the invoice digest is committed by the DAO authority but invoice bytes are not fetched or authenticated by the contract. The gate's claim concerns duplicate **registered obligations**, not objective invoice authenticity or actual payment prevention absent treasury integration.
