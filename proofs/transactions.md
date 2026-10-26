# All ResidueRelay StudioNet transactions

One source, four independent scenario deployments. Every row finalized with a strict
`MAJORITY_AGREE`; ERROR rows are intended public-method rejections with unchanged state.

| Call | Transaction | Execution | Agree / disagree / idle |
|---|---|---|---|
| clean-deployment | [0x3f8e7929bdc0710e3486598bffcc6b1312a6ca6cda5f96a86bc844f4569976b4](https://explorer-studio.genlayer.com/tx/0x3f8e7929bdc0710e3486598bffcc6b1312a6ca6cda5f96a86bc844f4569976b4) | SUCCESS | 5 / 0 / 0 |
| clean-first | [0x1d54afa0372a83c2fbd42f0671c7d108a2b1d879f3efac2060294fe5ea417a1e](https://explorer-studio.genlayer.com/tx/0x1d54afa0372a83c2fbd42f0671c7d108a2b1d879f3efac2060294fe5ea417a1e) | SUCCESS | 3 / 0 / 2 |
| clean-early | [0x79c53c775104b483369435c046b2bafc466fba82c82fd10570a7966137459a62](https://explorer-studio.genlayer.com/tx/0x79c53c775104b483369435c046b2bafc466fba82c82fd10570a7966137459a62) | ERROR | 3 / 0 / 2 |
| clean-second | [0xce70207753702ec23a061325993e39a4aa1d3139e0e5362f069e1a71e96c4ee5](https://explorer-studio.genlayer.com/tx/0xce70207753702ec23a061325993e39a4aa1d3139e0e5362f069e1a71e96c4ee5) | SUCCESS | 3 / 0 / 2 |
| clean-duplicate | [0x80d3ed364ff9d46a7be9e2bda18623a6e19c76b53a5dbee7a7d2a49ce45950df](https://explorer-studio.genlayer.com/tx/0x80d3ed364ff9d46a7be9e2bda18623a6e19c76b53a5dbee7a7d2a49ce45950df) | ERROR | 3 / 0 / 2 |
| clean-seal | [0x721da34ef168b5f89a5d61e16c708e7ec263bcce490de0507ec15ec56fb0f7c6](https://explorer-studio.genlayer.com/tx/0x721da34ef168b5f89a5d61e16c708e7ec263bcce490de0507ec15ec56fb0f7c6) | SUCCESS | 3 / 0 / 2 |
| clean-reseal | [0xc9431ecf420e0642d4ff26fd291049c5ddc34fd010b2c9fb7f918dccedb67c3e](https://explorer-studio.genlayer.com/tx/0xc9431ecf420e0642d4ff26fd291049c5ddc34fd010b2c9fb7f918dccedb67c3e) | ERROR | 3 / 0 / 2 |
| clean-unneeded | [0x87516b0a8dd5952616b4f243a65fbef0c753a61f2085acfca11e7496aabda42c](https://explorer-studio.genlayer.com/tx/0x87516b0a8dd5952616b4f243a65fbef0c753a61f2085acfca11e7496aabda42c) | ERROR | 5 / 0 / 0 |
| corrupt-deployment | [0xf9e835e777edaed7036fcc076d38e08cda97fb2568244e5727365d325424d7b6](https://explorer-studio.genlayer.com/tx/0xf9e835e777edaed7036fcc076d38e08cda97fb2568244e5727365d325424d7b6) | SUCCESS | 5 / 0 / 0 |
| corrupt-first | [0x9de1527b0d56771a4f60360300a9737faf5f43cb95e7530f6a5558b5c10dda85](https://explorer-studio.genlayer.com/tx/0x9de1527b0d56771a4f60360300a9737faf5f43cb95e7530f6a5558b5c10dda85) | SUCCESS | 3 / 0 / 2 |
| corrupt-early | [0xd12cd0ffdda3f0b00d46b6c6caa011feaa8ed7c01366e661f5be5ab9a2e8e1d9](https://explorer-studio.genlayer.com/tx/0xd12cd0ffdda3f0b00d46b6c6caa011feaa8ed7c01366e661f5be5ab9a2e8e1d9) | ERROR | 3 / 0 / 2 |
| corrupt-second | [0x478f7eee1911bd93443750989a1911834d847f0283dc7e5debe678d0b13e2858](https://explorer-studio.genlayer.com/tx/0x478f7eee1911bd93443750989a1911834d847f0283dc7e5debe678d0b13e2858) | SUCCESS | 3 / 0 / 2 |
| corrupt-duplicate | [0x15dbe7bb1e9d8f1910c3efa9da2956698ce91d7f7bcc4f1dbfb3acb0f04e2f6a](https://explorer-studio.genlayer.com/tx/0x15dbe7bb1e9d8f1910c3efa9da2956698ce91d7f7bcc4f1dbfb3acb0f04e2f6a) | ERROR | 3 / 0 / 2 |
| corrupt-seal | [0xd1dc4720d2f0d4d400f22596dd4da809b8d60f35050e09b7d396babb9bce05c6](https://explorer-studio.genlayer.com/tx/0xd1dc4720d2f0d4d400f22596dd4da809b8d60f35050e09b7d396babb9bce05c6) | SUCCESS | 3 / 0 / 2 |
| corrupt-reseal | [0x43c1d23582c3a372b3df383c0ee5771e4e85573b8b02aa132ae782429ff06275](https://explorer-studio.genlayer.com/tx/0x43c1d23582c3a372b3df383c0ee5771e4e85573b8b02aa132ae782429ff06275) | ERROR | 5 / 0 / 0 |
| corrupt-repair-two | [0x57acb47701aac0d7135cff7ac7cc7ec96551900df8b36baa303bb237600d6c26](https://explorer-studio.genlayer.com/tx/0x57acb47701aac0d7135cff7ac7cc7ec96551900df8b36baa303bb237600d6c26) | SUCCESS | 3 / 0 / 2 |
| corrupt-duplicate-repair | [0x2a5ccd38c1b0c4dae0068b881a408dfa77cafb3eee1f2ac57f0c7c523e4255a0](https://explorer-studio.genlayer.com/tx/0x2a5ccd38c1b0c4dae0068b881a408dfa77cafb3eee1f2ac57f0c7c523e4255a0) | ERROR | 3 / 0 / 2 |
| erasures-deployment | [0xb028ce6052d8d1b12130ba16084b2155e94948e13b1487589a3be4857df7e168](https://explorer-studio.genlayer.com/tx/0xb028ce6052d8d1b12130ba16084b2155e94948e13b1487589a3be4857df7e168) | SUCCESS | 3 / 0 / 2 |
| erasures-first | [0xf2804045cf8025e9f0c4856bce3bd441dae042fa40bc9192195b747634ba9282](https://explorer-studio.genlayer.com/tx/0xf2804045cf8025e9f0c4856bce3bd441dae042fa40bc9192195b747634ba9282) | SUCCESS | 3 / 0 / 2 |
| erasures-early | [0x23ea50969cc5b26bc6ea417362a19320c70fd7cacf0c4f0fe71d5b57705e99cc](https://explorer-studio.genlayer.com/tx/0x23ea50969cc5b26bc6ea417362a19320c70fd7cacf0c4f0fe71d5b57705e99cc) | ERROR | 5 / 0 / 0 |
| erasures-second | [0x3f4942c9513e05921129f6d79601ae12fb0cc5240534576db47d686e2e1be83d](https://explorer-studio.genlayer.com/tx/0x3f4942c9513e05921129f6d79601ae12fb0cc5240534576db47d686e2e1be83d) | SUCCESS | 3 / 0 / 2 |
| erasures-duplicate | [0xc29ba2bc54287af7af37fed4f4229cc0b32044cf33bf981835ed7c3228b42f70](https://explorer-studio.genlayer.com/tx/0xc29ba2bc54287af7af37fed4f4229cc0b32044cf33bf981835ed7c3228b42f70) | ERROR | 3 / 0 / 2 |
| erasures-seal | [0xee32b57a8dcd8aefeffd4335e01dcc072f9008570ce4852ec24f6c4e4ae21170](https://explorer-studio.genlayer.com/tx/0xee32b57a8dcd8aefeffd4335e01dcc072f9008570ce4852ec24f6c4e4ae21170) | SUCCESS | 5 / 0 / 0 |
| erasures-reseal | [0x237f0e4ec0275dcf731f9917a100488ec75fb466cd0ae2f54d0084c5fddceb6e](https://explorer-studio.genlayer.com/tx/0x237f0e4ec0275dcf731f9917a100488ec75fb466cd0ae2f54d0084c5fddceb6e) | ERROR | 5 / 0 / 0 |
| erasures-repair-two | [0x23014997b7f544b2bf27c517cb1331b0828ace26940eff302b9b0903c3d8ebfd](https://explorer-studio.genlayer.com/tx/0x23014997b7f544b2bf27c517cb1331b0828ace26940eff302b9b0903c3d8ebfd) | SUCCESS | 4 / 0 / 1 |
| erasures-repair-four | [0xd152b2508aac6e6bb73d1ec7cff4023ed3921fea422344436d0939feb059220b](https://explorer-studio.genlayer.com/tx/0xd152b2508aac6e6bb73d1ec7cff4023ed3921fea422344436d0939feb059220b) | SUCCESS | 3 / 0 / 2 |
| erasures-duplicate-repair | [0x091a5661ecbf2def53fbf1d0632ead32491ee61dc346e92aa24c9562a262370e](https://explorer-studio.genlayer.com/tx/0x091a5661ecbf2def53fbf1d0632ead32491ee61dc346e92aa24c9562a262370e) | ERROR | 3 / 0 / 2 |
| ambiguous-deployment | [0x4db40c2e29e2b28d11c56330a93ebf000f0d5742feb82128bc01bb43e6cfd362](https://explorer-studio.genlayer.com/tx/0x4db40c2e29e2b28d11c56330a93ebf000f0d5742feb82128bc01bb43e6cfd362) | SUCCESS | 3 / 0 / 2 |
| ambiguous-first | [0x66bf14ac8e66cde057b54ba25a8f6ccb21510cbf5a5f021cd977bb3b5ce8af11](https://explorer-studio.genlayer.com/tx/0x66bf14ac8e66cde057b54ba25a8f6ccb21510cbf5a5f021cd977bb3b5ce8af11) | SUCCESS | 3 / 0 / 2 |
| ambiguous-early | [0x2efe9cbddb5054947118361aaddcfb8d334a8c90e1cf2033270fa24e319122a0](https://explorer-studio.genlayer.com/tx/0x2efe9cbddb5054947118361aaddcfb8d334a8c90e1cf2033270fa24e319122a0) | ERROR | 3 / 0 / 2 |
| ambiguous-second | [0x5f363796e45bbb607c40d97d49afaf427170e27a11dffe37813910f587c0cbda](https://explorer-studio.genlayer.com/tx/0x5f363796e45bbb607c40d97d49afaf427170e27a11dffe37813910f587c0cbda) | SUCCESS | 3 / 0 / 2 |
| ambiguous-duplicate | [0x6ae5976730c10de79439b158834080280fc986c20d20ae083265e0e5008bf19f](https://explorer-studio.genlayer.com/tx/0x6ae5976730c10de79439b158834080280fc986c20d20ae083265e0e5008bf19f) | ERROR | 3 / 0 / 2 |
| ambiguous-seal | [0x64c175b488b7924bc278a9a7c170dd089c777c2f8589535f4e5454da5f2f2a3e](https://explorer-studio.genlayer.com/tx/0x64c175b488b7924bc278a9a7c170dd089c777c2f8589535f4e5454da5f2f2a3e) | SUCCESS | 3 / 0 / 2 |
| ambiguous-reseal | [0x3056c58a0d822e0859127163634e3b42721cda84b9aa9bfba7111986c2275eb9](https://explorer-studio.genlayer.com/tx/0x3056c58a0d822e0859127163634e3b42721cda84b9aa9bfba7111986c2275eb9) | ERROR | 3 / 0 / 2 |
| ambiguous-blocked-repair | [0xed900eae03d61aae808cebcc034c20ceeb664d122f1dd25d30e5a355090140c0](https://explorer-studio.genlayer.com/tx/0xed900eae03d61aae808cebcc034c20ceeb664d122f1dd25d30e5a355090140c0) | ERROR | 3 / 0 / 2 |

[Full verification](verification.json) · [Source-bound suite](suite.json) · [Proof explanation](README.md)
