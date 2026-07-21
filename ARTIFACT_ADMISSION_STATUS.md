# Artifact Admission pilot status

This repository is being extended in bounded phases after the completed
Trusted Finalizer Round 1. The first phase installs a reusable trusted builder;
it does **not** enable an artifact-admission decision by itself.

## Phase A — trusted builder infrastructure

- [x] A reusable workflow accepts only an open same-repository PR at its exact
  current branch/SHA.
- [x] It requires the PR base to equal current protected `main`, downloads the
  exact Reverify control/evidence and Seal bundle artifact IDs, re-derives the
  raw-Git bindings, and cryptographically verifies a signed finalizer `ALLOW`
  for the same repository/PR/base/head/run/attempt.
- [x] It reads three fixed blobs from a bare Git object store with
  `git cat-file`, creates one bounded canonical regular file, and never checks
  out, imports, or executes candidate code.
- [x] It generates one GitHub provenance attestation with a full-SHA-pinned
  `actions/attest` action.
- [x] It emits separate subject and audit-control artifacts binding run/attempt,
  source, finalizer, artifact ID/API digest/file digest, and attestation ID.
- [x] A separate artifact-admission public key exists. Its key ID is
  `sha256:cd9db360e786c0f4c5d31881a5953152bb773a86ee9d3716721dbf01658b357b`.

## Phase B — pending after Phase A is merged

- [ ] Pin a dispatcher to the immutable Phase A merge commit.
- [ ] Add the protected admission workflow and pin GitHub CLI `v2.90.0` by
  archive SHA-256
  `b2aef7b23ec6899bf27f37a32c57a7935d0a178568ac33dc9bb03842f724195a`.
- [ ] Configure numeric workflow IDs as repository variables.
- [ ] Configure `evoguard-artifact-admission` with the distinct private key,
  required reviewer, self-review prevention, protected branches only, and no
  administrator bypass.
- [ ] Open a new source-only PR, obtain a fresh finalizer `ALLOW`, build and
  attest the exact regular file, seal one `.eab`, and verify it offline and
  through a fresh GitHub attestation query.
- [ ] Run live negative controls and retain exact evidence.

## Claim boundary

The completed pilot may claim only that one exact regular-file SHA-256 was
bound to a GitHub attestation verified under the recorded provider policy and
to a Trusted Finalizer `ALLOW` for the same source head. It must not claim
reproducibility, code safety, publication, release, deployment, OCI admission,
production readiness, or independent review. `EvoRiseKsa` and `MANA-awam`
remain same-owner technical roles.
