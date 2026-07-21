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
  for the same repository/PR/base/head/run/attempt. It also requires the signed
  verdict, handoff, and Git-binding bytes inside the bundle to equal the exact
  downloaded/re-derived external proofs.
- [x] It reads three fixed blobs from a bare Git object store with
  `git cat-file`, creates one bounded canonical regular file, and never checks
  out, imports, or executes candidate code.
- [x] It generates one GitHub provenance attestation with a full-SHA-pinned
  `actions/attest` action.
- [x] It emits separate subject and audit-control artifacts binding run/attempt,
  source, finalizer, artifact ID/API digest/file digest, and attestation ID.
  The B/Seal run attempt, workflow ID, and protected-main head are bound at
  this builder/attestation layer; v4.0.2 itself cryptographically binds the
  A/Reverify run and does not claim a B-attempt field inside its signed format.
- [x] A separate artifact-admission public key exists. Its key ID is
  `sha256:cd9db360e786c0f4c5d31881a5953152bb773a86ee9d3716721dbf01658b357b`.

Phase A was initially merged at immutable commit
`c6de26095c84e654c2cc5adcb00885ac9b6a2362`. Live build run `29876087399`
then failed closed before attestation because cross-run artifact downloads did
not pass their validated `run-id`. The correction was merged at immutable
commit `27a233f41b9914aa67fdf70edefd45fe3dfc05ee`. A second live build,
`29876697930`, then completed finalizer verification, canonical construction,
GitHub attestation, and subject upload before failing closed because the upload
action's bare digest had not been normalized to the API's `sha256:` form. That
normalization was merged at immutable commit
`8083c3763e3472ff8616bd645b016ad0779da91d`; the dispatcher below pins this
latest reviewed correction rather than `main`.

## Phase B — protected admission enablement

- [x] Pin a dispatcher to the immutable Phase A merge commit.
- [x] Add a split preflight/protected-admission workflow and pin GitHub CLI
  `v2.90.0` by
  archive SHA-256
  `b2aef7b23ec6899bf27f37a32c57a7935d0a178568ac33dc9bb03842f724195a`.
- [x] Keep the admission key out of job/seal environments, materialize it only
  after a fresh provider check, execute the second provider check under a
  lower-privilege OS identity, and destroy the key before retained checks.
- [x] Configure numeric workflow IDs as repository variables.
- [x] Configure `evoguard-artifact-admission` with the distinct private key,
  required reviewer, self-review prevention, protected branches only, and no
  administrator bypass.
- [ ] Open a new source-only PR, obtain a fresh finalizer `ALLOW`, build and
  attest the exact regular file, seal one `.eab`, and verify it offline and
  through a fresh GitHub attestation query.
- [ ] Run live negative controls and retain exact evidence.

The workflows, variables, and protected Environment are enabled. Static tests
and the recorded fail-closed probe are not positive live provider evidence;
the live checkboxes remain open until one new PR completes the full sequence.

## Claim boundary

The completed pilot may claim only that one exact regular-file SHA-256 was
bound to a GitHub attestation verified under the recorded provider policy and
to a Trusted Finalizer `ALLOW` for the same source head. It must not claim
reproducibility, code safety, publication, release, deployment, OCI admission,
production readiness, or independent review. `EvoRiseKsa` and `MANA-awam`
remain same-owner technical roles.
