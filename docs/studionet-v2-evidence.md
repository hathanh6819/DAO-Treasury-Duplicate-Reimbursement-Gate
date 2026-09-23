# Studionet version 2 live evidence

Verified on 2026-09-22 and 2026-09-23 against [`0xF6cF059A3bFa4e8F8B01Db976387f32324DBc477`](https://explorer-studio.genlayer.com/address/0xF6cF059A3bFa4e8F8B01Db976387f32324DBc477).

## Deployment readback

- Network: Studionet, chain ID `61999`
- Protocol version: `2`
- Source SHA-256: `a62ec2336f80239778ed5ab9dc29029f526faeed3fc09b393cd8d6d939b5e4ee`
- DAO authority: `0x1D283b45974B0be9630DFD1deC6A62a9B72B2760`
- Treasury controller: `0xf96Cf822F9f4e76956AB9fAAa22B3BdCD7b10aD6`
- Custody: `false`
- Initial claim count: `0`

## Reviewer path: stale authorization is reassessed

| Check | Finalized transaction | Authoritative readback |
|---|---|---|
| Authority submits claim A | [`0xc74e38...487b1`](https://explorer-studio.genlayer.com/tx/0xc74e38dfc9a78fdb4909435a60edf6547984e377efa81f75987fa4e6e38487b1) | Claim 1 is `PENDING`, revision 1 |
| Validators assess A | [`0x0cb137...1fb18`](https://explorer-studio.genlayer.com/tx/0x0cb137db34ecb13e3dffde626aad4a61e52eabd9772835f04d5bb75efa01fb18) | A becomes `CLEAR`, revision 2, unconsumed |
| Authority submits unrelated-work claim B for the same DAO/vendor | [`0x20f097...79e6b`](https://explorer-studio.genlayer.com/tx/0x20f0973fc82f4b89db70d74f416bd203414ab9d9c5a6ee3f72a47386e3079e6b) | In the same finalized state A becomes `PENDING`, reason `NEW_RELEVANT_CLAIM_REQUIRES_REASSESSMENT`, mode `REASSESSMENT`, revision 3, scope `[2]` |
| Controller attempts stale revision-2 consume | [`0xf6bc51...064f8`](https://explorer-studio.genlayer.com/tx/0xf6bc51ac0bea46d24abdcbe72172dd954a702cc925b5ce7177339e9bb0b064f8) | A remains unchanged and `consumed=false` |
| Validators reassess A against B | [`0x2c9474...ef35f`](https://explorer-studio.genlayer.com/tx/0x2c9474e9da80a1ba60426223df4d5c185986a6b32d5b650660b3549ff67ef35f) | A returns to `CLEAR`, revision 4, `compared_ids=[2]`, scope cleared |
| Controller consumes current exact authorization | [`0x41c6cf...6a5c3`](https://explorer-studio.genlayer.com/tx/0x41c6cf783065547f42f1f159db646727eb3b1bc5080d4b6f699cf8b6e4b6a5c3) | `consumed=true` at revision 4 |
| Controller replays consume | [`0x2bb626...19f55`](https://explorer-studio.genlayer.com/tx/0x2bb626c033b3f4639f65edd04ba0ce338b1388ce526a7d44b1d915f612619f55) | Validator return `AUTHORIZATION_ALREADY_CONSUMED`; state unchanged |

## Every newly relevant claim is included

| Check | Finalized transaction | Authoritative readback |
|---|---|---|
| Submit and initially clear claim C | [`submit C`](https://explorer-studio.genlayer.com/tx/0xc1b6b0da5ace5afe2f60829fef813885de85225edd52468e1293e7b0c4017e5e), [`assess C`](https://explorer-studio.genlayer.com/tx/0x299d27fa3c2e94e87080fa782c81e573e3087f5c0d45c2424cd0ab92ee53c75d) | Claim 3 is `CLEAR`, revision 2 |
| Submit newer claim D | [`0x699ecc...bf482`](https://explorer-studio.genlayer.com/tx/0x699ecc0d7bfccd12d458034bda9866ce8a76ae94117d7b59002832d7ebdbf482) | C reopens, revision 3, scope `[4]` |
| Submit another claim E before reassessment | [`0x43bb87...a83bb`](https://explorer-studio.genlayer.com/tx/0x43bb8738452ebaff2248203e849fa30b68dc479c02542aa921f7d765203a83bb) | C remains pending, revision 4, scope `[4,5]` |
| Attempt reassessment with stale revision 3 | [`0xde179c...7f004`](https://explorer-studio.genlayer.com/tx/0xde179ca16bed700b7d1df00bc8110c24c3231e265d65f76d5c314b90b9e7f004) | C remains unchanged at revision 4 |
| Reassess using current revision | [`0x0e1f82...bd2f0`](https://explorer-studio.genlayer.com/tx/0x0e1f821c95d0eba8be3e0fbe493aafedcd73b027007a7908501e35af752bd2f0) | C becomes `CLEAR`, revision 5, `compared_ids=[4,5]`, scope cleared |
| Consume only after complete coverage | [`0x752443...c5136`](https://explorer-studio.genlayer.com/tx/0x752443d40595d2f6aa6c63cc52ef6d22a90b8e903b148502662d99e47c9c5136) | C consumes only after both later claims were recorded |

## Reassessment can revoke authorization

Claim 6 was initially assessed `CLEAR` by [`0xfc8457...d2e57`](https://explorer-studio.genlayer.com/tx/0xfc8457d0f0f7b25f706b2c4d85ce44a7d304210e60f3e815cc1f99cd6f2d2e57). After a semantically overlapping rebill was registered as claim 7, validators reassessed claim 6 to `DUPLICATE`, revision 4, reason `MATERIAL_DUPLICATE`, `compared_ids=[7]`, `consumed=false`. This state is publicly readable from the [contract](https://explorer-studio.genlayer.com/address/0xF6cF059A3bFa4e8F8B01Db976387f32324DBc477).

The controller then attempted exact consumption at the current revision in [`0x022fb2...01b3e`](https://explorer-studio.genlayer.com/tx/0x022fb2b74f952045d4e662b2ec24cb915f0e4f336e31fd95593441f7e4501b3e). It finalized with consensus but claim 6 remained byte-for-byte unchanged and `consumed=false`.

All fixtures are synthetic. The contract records authorization only and neither holds nor transfers funds.

