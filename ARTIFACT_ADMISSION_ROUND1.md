# Artifact Admission Round 1

Round 1 completed one public, source-only Artifact Admission exercise. It was
an operational same-owner test, not an independent audit.

## Exact source and control-plane bindings

- PR: [`#7`](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/pull/7)
- base commit: `a602c2b007fad4d5627476187bcbc8c218c16be9`
- candidate head: `a3c71c622cc9818242ae5294bc550ee75674ab1d`
- post-admission squash merge: `f9bb56c62c98759820353154ce66ac79057b6234`
- Reverify run: [`29878266034`](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/actions/runs/29878266034), attempt 1, success
- protected Seal run: [`29878298540`](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/actions/runs/29878298540), attempt 1, success
- Artifact Build run: [`29878399911`](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/actions/runs/29878399911), attempt 1, success
- protected Admission run: [`29878420698`](https://github.com/EvoRiseKsa/evoom-guard-v4-finalizer-pilot/actions/runs/29878420698), attempt 1, success
- immutable builder workflow commit: `8083c3763e3472ff8616bd645b016ad0779da91d`
- Guard v4.0.2 SHA-256: `7813db5c99f27f780ec31bbaa124b5526405783d1f53caecc32f70aabfbc13c3`
- admitted regular-file SHA-256: `555695a5b1b6aa082495dc8b4faeb5562fcbc7e23124daf046ef4592d253eae6`
- finalizer key ID: `sha256:e5ca8d43c4816900ed42b81b52cbd65a6c42105b1bdfaa00a6c100462d70faf0`
- admission key ID: `sha256:cd9db360e786c0f4c5d31881a5953152bb773a86ee9d3716721dbf01658b357b`

The successful build emitted exactly two live artifacts:

- subject artifact ID `8513830753`, API digest
  `sha256:26573f986aeec794a0b526d21f079c95bd8ad1424671226c51756fe40d7961bc`;
- control artifact ID `8513830962`, API digest
  `sha256:168dae39d5d20fa3a1275dfb17c4f65d035b368fd9297ac79ca061b78fd65967`.

The Admission evidence artifact is ID `8513863288`, API digest
`sha256:6cd052809c9e00e8ad300bf7ffac2b0deaf6bfdf9c5aa339b9de31a79851025e`.

## What was verified

The protected Admission job revalidated the live build and finalizer selectors,
downloaded artifacts only by their exact run and artifact IDs, re-derived the
raw-Git bindings, and verified the GitHub provenance through a root-owned,
digest-bound `gh` executable running as a separate low-privilege OS user. That
same boundary was used before key materialization, during sealing, and during
post-key retained/fresh-provider checks.

The distinct admission key was materialized only after provider preflight and
was removed before retained verification. The job then verified the `.eab`,
performed a fresh provider query, rejected 13 negative cases, confirmed the
original evidence remained unchanged, and uploaded the public evidence.

After download, all 27 entries in `SHA256SUMS` were recomputed locally with
zero mismatches. The retained `.eab` also verified locally with the immutable
v4.0.2 zipapp and the separately supplied public keys, expected source, and
expected context; the result was `VERIFIED` with decision `ALLOW`.

## Fail-closed observations before success

The path was not treated as successful until the live run passed. Earlier
attempts failed without issuing an admission decision:

- build `29876087399`: cross-run downloads lacked the validated run ID;
- build `29876697930`: upload digest lacked normalization to the API form;
- Admission `29877194449`: the low-privilege user could not execute `gh` from
  the runner-private extraction path; key cleanup still succeeded;
- build `29878359169`: dispatch used `main` instead of the exact PR branch and
  was rejected before artifact construction.

These are evidence that the selectors failed closed in those observed cases;
they are not a proof that every possible failure mode is covered.

## Retained evidence and claim boundary

The downloaded public evidence is retained under
[`evidence/artifact-admission/round1`](evidence/artifact-admission/round1).
`OBSERVATION.json` is the machine-readable identity record and `SHA256SUMS`
covers the positive evidence set.

The supported claim is only that one regular-file SHA-256 was freshly verified
under the recorded GitHub attestation signer/source policy and bound to a
same-head Trusted Finalizer `ALLOW`. This does not establish reproducibility,
general code safety, release/deployment admission, OCI admission, production
readiness, or independent assurance. `EvoRiseKsa` and `MANA-awam` are
same-owner operational roles.
