# Studionet evidence

Synthetic lifecycle verified on 2026-09-15 against [`0x8B1c24CA1340aCdC37008A665b9B332E74cD0183`](https://explorer-studio.genlayer.com/address/0x8B1c24CA1340aCdC37008A665b9B332E74cD0183). Initial readback bound wallet A as DAO authority, wallet B as treasury controller, custody false, version 1 and count 0.

| Check | Transaction | Final return and authoritative readback |
|---|---|---|
| Wallet A submits first sealed obligation | [`0xc66fd4...9a807`](https://explorer-studio.genlayer.com/tx/0xc66fd4e51814f89d11077da3b192d1f6822d23b4a5d60993bf0b4ef561b9a807) | Claim 1, revision 1, `PENDING` |
| Wallet A assesses first obligation | [`0xa07f78...53796`](https://explorer-studio.genlayer.com/tx/0xa07f78249824218e98176914c65d2ed6d7eb677e642938d903b6d08d3fa53796) | `CLEAR`, revision 2, evidence digest `sha256:e93013e2c4220f5338a09764c92be8b2de50ba5c7e997764be567bf9cc94b840` |
| Wallet A attempts treasury consume | [`0x13f93b...69b0b`](https://explorer-studio.genlayer.com/tx/0x13f93b0faa29ee06e4f35ddaaa88cf8d3b8cde401ab6c9dcf4512100b9d69b0b) | `ONLY_TREASURY_CONTROLLER`; complete claim unchanged |
| Wallet B uses wrong action digest | [`0x00a4ca...e7d88`](https://explorer-studio.genlayer.com/tx/0x00a4cac2ce2db4319853f1379b6634e9c70caf5b3efe375f5d9b17374cde7d88) | `ACTION_DIGEST_MISMATCH` |
| Wallet B consumes exact authorization | [`0xc5ba68...a2e83`](https://explorer-studio.genlayer.com/tx/0xc5ba680833c43336d324f323580d017ef637deea1ad11c8bba7aba814bba2e83) | `AUTHORIZATION_CONSUMED`; consumed true |
| Wallet B repeats the same authorization | [`0xb18351...e538e`](https://explorer-studio.genlayer.com/tx/0xb18351a382c5281826181f9a7a305b108209f27b72233787a939939e751e538e) | `AUTHORIZATION_ALREADY_CONSUMED` |
| Wallet A submits adversarial re-bill | [`0xbea1bd...620b5`](https://explorer-studio.genlayer.com/tx/0xbea1bd8d8a306e0ddac728b05ea8316d4c8083c9b236d3792b3c42e17a9620b5) | Claim 2 changes invoice, beneficiary, token and amount while describing the same July audit |
| Validators assess semantic overlap | [`0x07f430...12235`](https://explorer-studio.genlayer.com/tx/0x07f430b3558499d8ccd47d0d438cc61e4234366af68af00e9d6a3e2903112235) | `DUPLICATE`, comparator `[1]`, evidence digest `sha256:b55c0bad745ba5549453aeb815de2a630bb01c9b3d735695c3892419fee7d969` |
| Wallet B attempts exact duplicate consume | [`0x5937d3...ca159`](https://explorer-studio.genlayer.com/tx/0x5937d38725ee525e9c43316387691cb6ccd5e1871d26eac4f432188b075ca159) | `NOT_AUTHORIZED`; complete claim unchanged; count remains 2 |

This lifecycle proves behavior for synthetic on-chain obligations, not invoice authenticity or external Safe execution. No funds were transferred or held.
