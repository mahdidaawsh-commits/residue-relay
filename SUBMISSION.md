# ResidueRelay: Consensus coded-record reconstruction

Category: **Builder → Intelligent Contracts**

## Notes / Description

ResidueRelay reconstructs public coded records from prose fragments. A deployment pins five document URLs/SHA-256 hashes for a three-symbol GF(17) record. Anyone acquires unseen positions in atomic batches. Leader and validators independently fetch complete documents, normalize final observed symbols and audit every decision, including erasures. Exact observations feed finite-field decoding with a 2*errors+erasures budget. Sealing records a unique record, outside-budget failure or ambiguity witnesses. Only unique sealed records permit source-bound repair packets; raw observations stay immutable. StudioNet proofs cover clean recovery, one corrupted symbol, two erasures and conflicting candidates. All 35 receipts finalized MAJORITY_AGREE; 35 views match an independent exhaustive oracle. The repo includes 131 direct tests and all 4,913 payload round-trips. Synthetic public fragments demonstrate conditional compatibility, not publisher honesty or external repair application.

## Evidence

- [Repository](https://github.com/mahdidaawsh-commits/residue-relay)
- [GenLayer contract source](https://github.com/mahdidaawsh-commits/residue-relay/blob/main/contracts/residue_relay.py)
- [Contract explorer — corruption recovery and repair](https://explorer-studio.genlayer.com/address/0xD11B6AFD5C50075C1b72162Cd678698bcfe88f3a)
- [Deployment transaction](https://explorer-studio.genlayer.com/tx/0xf9e835e777edaed7036fcc076d38e08cda97fb2568244e5727365d325424d7b6)
- [Consensus source acquisition](https://explorer-studio.genlayer.com/tx/0x9de1527b0d56771a4f60360300a9737faf5f43cb95e7530f6a5558b5c10dda85)
- [Unique reconstruction](https://explorer-studio.genlayer.com/tx/0xd1dc4720d2f0d4d400f22596dd4da809b8d60f35050e09b7d396babb9bce05c6)
- [Recorded correction packet](https://explorer-studio.genlayer.com/tx/0x57acb47701aac0d7135cff7ac7cc7ec96551900df8b36baa303bb237600d6c26)
- [Full proofs, all scenarios and transaction links](https://github.com/mahdidaawsh-commits/residue-relay/blob/main/proofs/README.md)

One contract mechanism, four scenario deployments. The finite-field code is classical;
the contribution is the GenLayer acquisition, exact consensus, explicit ambiguity
and immutable repair-provenance composition. This submission does not claim invention
of Reed–Solomon coding, encryption, physical-data truth or externally applied repairs.
