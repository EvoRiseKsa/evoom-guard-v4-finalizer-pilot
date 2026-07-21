# Controlled operating protocol

This protocol is an operational same-owner exercise, not an independent audit.

1. Verify the v4.0.2 release is immutable and the downloaded zipapp SHA-256 is
   `7813db5c99f27f780ec31bbaa124b5526405783d1f53caecc32f70aabfbc13c3`.
2. Protect `main` with linear history, one current approving review, code-owner
   review, stale-approval dismissal, conversation resolution, and `pilot-ci`.
   Do not require the finalizer display name yet.
3. Create `evoguard-finalizer` with a new pilot-only Ed25519 private key,
   required `MANA-awam` reviewer, self-review prevention, and administrator
   bypass disabled. This is technical separation only because both accounts
   have the same owner.
4. Set `EVOGUARD_GUARD_ARTIFACT_SHA256` to the exact digest above. Leave
   `EVOGUARD_REVERIFY_WORKFLOW_ID` absent for the first dispatch.
5. Open and approve one public-safe source-only PR. Dispatch **EvoGuard
   Reverify** from protected `main` with that PR number. Record the bootstrap
   fail-closed result and the numeric workflow ID.
6. Set `EVOGUARD_REVERIFY_WORKFLOW_ID` to that exact numeric ID. Start a new
   full dispatch; never use a partial job rerun. Approve the Environment only
   after all preflight identities match.
7. Download the finalized bundle and public-safe expected source/context.
   Re-fetch PR/run/tree identities independently and verify the bundle offline.
8. On the unchanged PR head, create a fresh attempt and deliberately fail or
   cancel it after the attempt-bound pending check exists. Confirm it does not
   reuse the earlier success. Then run one final complete passing attempt.
9. Archive bounded public evidence and only then consider whether the finalizer
   check name can safely become required. Do not enable it if GitHub's repeated
   check-name behavior is ambiguous.

Stop on any unexpected artifact, stale head/base, workflow mismatch, missing
cleanup, key exposure, or inability to rederive source/context.
