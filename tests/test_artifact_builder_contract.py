from __future__ import annotations

import base64
import hashlib
import re
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
BUILDER = ROOT / ".github" / "workflows" / "trusted-artifact-builder.yml"
ADMISSION_PUBLIC = ROOT / "security" / "artifact-admission-public.pem"
FINALIZER_PUBLIC = ROOT / "security" / "finalizer-public.pem"

ADMISSION_KEY_ID = "sha256:cd9db360e786c0f4c5d31881a5953152bb773a86ee9d3716721dbf01658b357b"
FINALIZER_KEY_ID = "sha256:e5ca8d43c4816900ed42b81b52cbd65a6c42105b1bdfaa00a6c100462d70faf0"


def pem_key_id(path: Path) -> str:
    lines = [line.strip() for line in path.read_text(encoding="ascii").splitlines()]
    der = base64.b64decode("".join(line for line in lines if not line.startswith("-----")), validate=True)
    return "sha256:" + hashlib.sha256(der).hexdigest()


class ArtifactBuilderContractTests(unittest.TestCase):
    def test_builder_is_reusable_only_and_has_no_secret_or_environment(self) -> None:
        text = BUILDER.read_text(encoding="utf-8")
        self.assertIn("workflow_call:", text)
        self.assertNotIn("workflow_dispatch:", text)
        self.assertNotIn("pull_request:", text)
        self.assertNotIn("environment:", text)
        self.assertNotIn("secrets.", text)
        self.assertNotIn("sign-key", text)

    def test_builder_uses_exact_full_sha_action_pins(self) -> None:
        text = BUILDER.read_text(encoding="utf-8")
        refs = re.findall(r"uses:\s*actions/[A-Za-z0-9_.-]+@([^\s#]+)", text)
        self.assertGreaterEqual(len(refs), 5)
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{40}", ref) for ref in refs))
        self.assertEqual(text.count("actions/attest@f7c74d28b9d84cb8768d0b8ca14a4bac6ef463e6"), 1)

    def test_candidate_is_read_as_fixed_bounded_git_blobs_not_executed(self) -> None:
        text = BUILDER.read_text(encoding="utf-8")
        for path in ("calc/__init__.py", "calc/__main__.py", "calc/ops.py"):
            self.assertEqual(text.count(f'"{path}"'), 1)
        self.assertIn('[*git, "cat-file", "blob", object_id]', text)
        self.assertIn("git init --bare", text)
        self.assertNotIn("actions/checkout@", text)
        self.assertIn('mode not in {"100644", "100755"}', text)
        self.assertIn("source object exceeds 256 KiB", text)
        self.assertNotIn("python -m calc", text)
        self.assertNotIn("pytest", text)

    def test_builder_cryptographically_binds_finalizer_to_current_pr(self) -> None:
        text = BUILDER.read_text(encoding="utf-8")
        for token in (
            "PR base must equal the current protected main head",
            "reverify.head_sha !== pr.base.sha",
            "finalizer control does not bind this exact PR/base/head/run",
            "artifact-ids: ${{ steps.preflight.outputs.finalizer_reverify_control_artifact_id }}",
            "artifact-ids: ${{ steps.preflight.outputs.finalizer_reverify_evidence_artifact_id }}",
            "artifact-ids: ${{ steps.preflight.outputs.finalizer_bundle_artifact_id }}",
            "derive-finalizer-bindings",
            "verify-finalizer-bindings",
            "verify-finalized",
            "--require-pass",
            "--expected-source",
            "--expected-context",
            "signed finalizer member does not equal external proof",
            '"trusted-finalizer-git-bindings", "trusted-finalizer-handoff"',
        ):
            self.assertIn(token, text)
        self.assertIn("MCowBQYDK2VwAyEA4JaVN8axu8ERZTzSXdoDe7uznDO0Tf/zltCQm6jr/5o=", text)

    def test_cross_run_artifact_downloads_select_the_validated_run_ids(self) -> None:
        text = BUILDER.read_text(encoding="utf-8")
        cases = (
            (
                "Download the exact immutable finalizer control artifact",
                "Download the exact re-verification evidence artifact",
                "run-id: ${{ steps.preflight.outputs.finalizer_reverify_run_id }}",
            ),
            (
                "Download the exact re-verification evidence artifact",
                "Download the exact signed finalizer bundle artifact",
                "run-id: ${{ steps.preflight.outputs.finalizer_reverify_run_id }}",
            ),
            (
                "Download the exact signed finalizer bundle artifact",
                "Download and verify the reviewed Guard",
                "run-id: ${{ steps.preflight.outputs.finalizer_seal_run_id }}",
            ),
        )
        for start, end, expected in cases:
            block = text[text.index(start) : text.index(end)]
            self.assertIn(expected, block)

    def test_builder_uses_reviewed_runtime_and_hash_locked_verifier(self) -> None:
        text = BUILDER.read_text(encoding="utf-8")
        self.assertIn("releases/download/v4.0.2/evo-guard.pyz", text)
        self.assertGreaterEqual(
            text.count("7813db5c99f27f780ec31bbaa124b5526405783d1f53caecc32f70aabfbc13c3"),
            2,
        )
        self.assertIn("--require-hashes", text)
        self.assertIn("cryptography==46.0.7", text)

    def test_control_binds_provider_build_and_finalizer_identifiers(self) -> None:
        text = BUILDER.read_text(encoding="utf-8")
        for token in (
            "GITHUB_RUN_ID",
            "GITHUB_RUN_ATTEMPT",
            "SUBJECT_ARTIFACT_ID",
            "SUBJECT_ARTIFACT_DIGEST",
            "SUBJECT_SHA256",
            "ATTESTATION_ID",
            "FINALIZER_REVERIFY_RUN_ID",
            "FINALIZER_SEAL_RUN_ID",
            "FINALIZER_SEAL_RUN_ATTEMPT",
            "FINALIZER_SEAL_WORKFLOW_ID",
            "FINALIZER_SEAL_HEAD_SHA",
            "FINALIZER_BUNDLE_ARTIFACT_ID",
            "FINALIZER_BUNDLE_ARTIFACT_DIGEST",
        ):
            self.assertIn(token, text)
        self.assertIn('"format": "EVOGUARD_ARTIFACT_BUILD_CONTROL_V1"', text)
        self.assertIn("invalid positive decimal action output", text)
        self.assertIn("invalid GitHub artifact API digest", text)
        self.assertIn("invalid GitHub URL action output", text)
        self.assertIn("os.O_NOFOLLOW", text)

    def test_admission_key_is_distinct_from_finalizer_key(self) -> None:
        admission = pem_key_id(ADMISSION_PUBLIC)
        finalizer = pem_key_id(FINALIZER_PUBLIC)
        self.assertEqual(admission, ADMISSION_KEY_ID)
        self.assertEqual(finalizer, FINALIZER_KEY_ID)
        self.assertNotEqual(admission, finalizer)


if __name__ == "__main__":
    unittest.main()
