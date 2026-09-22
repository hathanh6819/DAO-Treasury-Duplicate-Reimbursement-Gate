# Studio Next version 2 evidence

Status: **awaiting deployment and live lifecycle**.

This page is intentionally not presented as completed evidence. It defines the exact live matrix required to prove that the deployed bytecode matches the reviewer fix. Replace each `PENDING` value only after the corresponding finalized Studio Next transaction and authoritative readback exist.

## Deployment

- Network: Studio Next, chain ID `61997`
- Contract address: `PENDING`
- Explorer: `PENDING`
- Source SHA-256: `a62ec2336f80239778ed5ab9dc29029f526faeed3fc09b393cd8d6d939b5e4ee`
- Protocol version readback: expected `2`
- DAO authority: `0x1D283b45974B0be9630DFD1deC6A62a9B72B2760`
- Treasury controller: `0xf96Cf822F9f4e76956AB9fAAa22B3BdCD7b10aD6`

## Required reviewer lifecycle

| Check | Transaction | Required authoritative readback |
|---|---|---|
| Submit claim A | `PENDING` | Claim A is `PENDING`, revision 1 |
| Assess claim A | `PENDING` | Claim A is `CLEAR`, revision 2, unconsumed |
| Submit newer related claim B | `PENDING` | In the same finalized state, claim A is reopened to `PENDING`, reason `NEW_RELEVANT_CLAIM_REQUIRES_REASSESSMENT`, mode `REASSESSMENT`, revision 3, scope includes B |
| Attempt stale consume of A | `PENDING` | Rejected because revision 2 is stale; A remains unconsumed |
| Reassess A against B | `PENDING` | A reaches the validator-derived result and its `compared_ids` includes B |
| If A is restored `CLEAR`, consume with current revision | `PENDING` | Exact controller/action digest succeeds once; replay fails |
| Separate duplicate scenario | `PENDING` | A previously clear, unconsumed claim is reopened and reassessed to `DUPLICATE`, so consume is rejected |
| Multi-arrival scenario | `PENDING` | A second newer claim extends scope and increments revision; assessment with the earlier revision fails |

All links must point directly to Studio Next explorer transactions or the deployed contract. Synthetic claims only; this contract does not hold or transfer funds.

