# EvoOM Guard v4 Trusted Finalizer pilot

This is a public, disposable, non-production consumer of the EvoOM Guard
Trusted Finalizer reference. It exists to exercise the current immutable
`v4.0.2` runtime without changing the frozen v3.7.0 pilot or its evidence.

The target is intentionally a tiny calculator. All source, policy, verifier
pack, workflow logs, and retained evidence must be safe for public disclosure.
Never add credentials, customer code, private incidents, or production data.

## Exact runtime root

- release: `v4.0.2`
- release commit: `3374164c65ad692049929fdc903eafb47c843a8e`
- `evo-guard.pyz` SHA-256:
  `7813db5c99f27f780ec31bbaa124b5526405783d1f53caecc32f70aabfbc13c3`
- `EVOGUARD_PACK_V2` verifier-pack SHA-256:
  `aa97da0bdff54432f0371e531c6d71a955a0de732a81bbf006bec60bf348ebf4`
- pilot finalizer public-key ID:
  `sha256:e5ca8d43c4816900ed42b81b52cbd65a6c42105b1bdfaa00a6c100462d70faf0`

The repository variable `EVOGUARD_GUARD_ARTIFACT_SHA256` must contain that
exact digest. The workflow downloads the immutable release asset and verifies
the protected variable before executing it. Pilot CI recomputes the pack
identity from Git-index-stable LF bytes and requires the policy pin to match.

## Claim boundary

A completed exercise can show that the reference workflow produced an
attempt-bound result for one public-safe PR under the recorded repository,
workflow, policy, pack, runtime, and Environment configuration. It cannot show
that:

- the implementation is free from other defects;
- Docker is equivalent to a hostile-code VM boundary;
- the same-owner `EvoRiseKsa` / `MANA-awam` roles are independent review;
- the workflow is a production merge gate; or
- a built/released/deployed artifact is the source that was admitted.

See [PILOT_STATUS.md](PILOT_STATUS.md) for current state and
[OPERATING_PROTOCOL.md](OPERATING_PROTOCOL.md) for the controlled sequence.
The completed Round 1 sequence and machine-readable retained evidence are in
[ROUND1_RESULTS.md](ROUND1_RESULTS.md).

The separately keyed Artifact Admission pilot is staged in bounded phases;
see [ARTIFACT_ADMISSION_STATUS.md](ARTIFACT_ADMISSION_STATUS.md). Its trusted
builder first verifies that a signed finalizer `ALLOW` belongs to the exact
current PR/base/head, then creates and attests a canonical regular file from a
bare Git object store without checking out or executing candidate code. No
artifact-admission decision is enabled merely by installing that reusable
workflow.

The Phase B dispatcher is pinned to the exact Phase A merge commit. Its
separate `workflow_run` admission path performs an unprivileged provider
preflight before a protected Environment can materialize the distinct
admission key. See the status document for the still-required live run; the
presence of workflow files alone is not evidence of an admitted artifact.

This repository is source-available under [LICENSE](LICENSE).
