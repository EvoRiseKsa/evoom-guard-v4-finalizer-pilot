# Pilot status

## Baseline

- [x] Public-safe calculator and judge-owned verifier pack.
- [x] Base-owned `.evoguard.json` policy.
- [x] Current implementation-ready reverify and seal workflows targeting the
  immutable v4.0.2 zipapp.
- [x] Static workflow-contract and fixture tests.
- [x] Protected `main` branch and required `pilot-ci` check verified live.
- [x] `evoguard-finalizer` Environment configured with a new pilot-only key,
  required reviewer, self-review prevention, and administrator bypass disabled.
- [x] Numeric reverify workflow ID recorded as a protected repository variable.

## Required live observations

- [x] Bootstrap attempt with the workflow-ID variable absent fails closed.
- [x] One source-only PR obtains a fresh raw-Git `ALLOW` after the variable is
  recorded and the Environment is approved.
- [x] The final `.evb` verifies offline with a separately supplied public key
  and GitHub/API-derived expected source and context.
- [x] A deliberately failed or cancelled fresh attempt does not inherit the
  prior success.
- [x] A final fresh full attempt on the unchanged PR head succeeds.

No box may be checked from a unit test alone. Each live observation requires
exact run/attempt IDs, commit/tree identities, artifact hashes, and the
same-owner/non-independent disclosure.

The pilot public key ID is
`sha256:e5ca8d43c4816900ed42b81b52cbd65a6c42105b1bdfaa00a6c100462d70faf0`.
The matching private key exists only as the protected Environment secret
`EVOGUARD_FINALIZER_KEY`; the local generation file was zeroed after upload.

Exact live observations and the retained final bundle are recorded in
[`ROUND1_RESULTS.md`](ROUND1_RESULTS.md) and
[`evidence/round1/OBSERVATION.json`](evidence/round1/OBSERVATION.json).
