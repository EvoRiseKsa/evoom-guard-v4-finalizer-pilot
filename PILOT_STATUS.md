# Pilot status

## Baseline

- [x] Public-safe calculator and judge-owned verifier pack.
- [x] Base-owned `.evoguard.json` policy.
- [x] Current implementation-ready reverify and seal workflows targeting the
  immutable v4.0.2 zipapp.
- [x] Static workflow-contract and fixture tests.
- [ ] Protected `main` branch and required `pilot-ci` check verified live.
- [ ] `evoguard-finalizer` Environment configured with a new pilot-only key,
  required reviewer, self-review prevention, and administrator bypass disabled.
- [ ] Numeric reverify workflow ID recorded as a protected repository variable.

## Required live observations

- [ ] Bootstrap attempt with the workflow-ID variable absent fails closed.
- [ ] One source-only PR obtains a fresh raw-Git `ALLOW` after the variable is
  recorded and the Environment is approved.
- [ ] The final `.evb` verifies offline with a separately supplied public key
  and GitHub/API-derived expected source and context.
- [ ] A deliberately failed or cancelled fresh attempt does not inherit the
  prior success.
- [ ] A final fresh full attempt on the unchanged PR head succeeds.

No box may be checked from a unit test alone. Each live observation requires
exact run/attempt IDs, commit/tree identities, artifact hashes, and the
same-owner/non-independent disclosure.
