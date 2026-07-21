# Round 1 results

Round 1 exercised the immutable EvoOM Guard `v4.0.2` Trusted Finalizer
reference against source-only pull request
[`#3`](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/pull/3).
The PR remained open and its head remained
`03868cf84825b7aaa9bdb0efd88f215eb878b943` throughout the sequence.

## Observed sequence

| Observation | Reverify run | Seal run | Final check | Sealed artifacts |
| --- | ---: | ---: | --- | ---: |
| Bootstrap without the trusted workflow-ID variable | [29869975583](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/actions/runs/29869975583) | [29870012646](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/actions/runs/29870012646) | `DENY` / failure | 0 |
| First complete attempt | [29870072197](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/actions/runs/29870072197) | [29870118470](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/actions/runs/29870118470) | `ALLOW` / success | 1 |
| Fresh attempt cancelled after metadata | [29870611929](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/actions/runs/29870611929) | [29870628369](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/actions/runs/29870628369) | `DENY` / failure | 0 |
| Final complete attempt | [29870833745](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/actions/runs/29870833745) | [29870873532](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/actions/runs/29870873532) | `ALLOW` / success | 1 |

The cancellation occurred after the metadata job had succeeded and while the
reverify job was queued/running. The dependent Seal workflow reconciled the
attempt to `DENY`, skipped its protected seal job, and uploaded no artifact.
It did not inherit either earlier `ALLOW` or its evidence.

## Independently rederived final bundle

The final bundle was downloaded from artifact `8511087135`, decoded from the
retained Base64 copy, and checked with the published `v4.0.2` zipapp whose
SHA-256 is
`7813db5c99f27f780ec31bbaa124b5526405783d1f53caecc32f70aabfbc13c3`.
Source and context were rederived from a separately fetched bare Git object
store plus GitHub API identities.

- bundle SHA-256:
  `d2f0f598d6b0e08c545345d86a3f762786afd2c551a29e710d9cd53e8ea4a4b3`
- rederived and bundled binding SHA-256:
  `c16b737762d8ba078c40d851d21f696e686dbf20940c5eda579497a69a2c20f3`
- public-key ID:
  `sha256:e5ca8d43c4816900ed42b81b52cbd65a6c42105b1bdfaa00a6c100462d70faf0`
- offline result: `VERIFIED`, decision `ALLOW`

Pilot CI reconstructs the archived `.evb`, verifies its signature and exact
expected source/context with the pinned runtime, and requires an `ALLOW`.
[`OBSERVATION.json`](evidence/round1/OBSERVATION.json) contains the exact
machine-readable run, check, artifact, governance, and claim-boundary facts.

## Claim boundary

This is a same-owner, non-production operational exercise. It proves only
that the recorded workflow version produced attempt-bound signed evidence for
the recorded PR/base/head/policy/pack/runtime context and failed closed for
the recorded bootstrap and cancellation controls. It is not an independent
security audit, a hostile-code VM claim, a production merge gate, or proof
about any built, released, or deployed artifact.
