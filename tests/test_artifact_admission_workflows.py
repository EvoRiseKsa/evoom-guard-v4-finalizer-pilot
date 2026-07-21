from __future__ import annotations

import re
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
DISPATCH = ROOT / ".github" / "workflows" / "artifact-build-dispatch.yml"
ADMISSION = ROOT / ".github" / "workflows" / "artifact-admission.yml"
BUILDER_MERGE = "c6de26095c84e654c2cc5adcb00885ac9b6a2362"


class ArtifactAdmissionWorkflowTests(unittest.TestCase):
    def test_dispatcher_pins_the_reviewed_reusable_builder(self) -> None:
        text = DISPATCH.read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", text)
        self.assertIn(
            "uses: EvoRiseKsa/evoom-guard-v4-finalizer-pilot/"
            f".github/workflows/trusted-artifact-builder.yml@{BUILDER_MERGE}",
            text,
        )
        self.assertNotIn("@main", text)
        self.assertNotIn("secrets: inherit", text)
        for permission in ("attestations: write", "id-token: write", "contents: read"):
            self.assertIn(permission, text)

    def test_all_third_party_actions_are_full_sha_pinned(self) -> None:
        texts = [DISPATCH.read_text(encoding="utf-8")]
        if ADMISSION.exists():
            texts.append(ADMISSION.read_text(encoding="utf-8"))
        for text in texts:
            refs = re.findall(r"uses:\s*actions/[A-Za-z0-9_.-]+@([^\s#]+)", text)
            self.assertTrue(all(re.fullmatch(r"[0-9a-f]{40}", ref) for ref in refs))

    def test_admission_is_protected_and_has_no_candidate_execution_surface(self) -> None:
        text = ADMISSION.read_text(encoding="utf-8")
        self.assertIn('workflows: ["EvoGuard Artifact Build"]', text)
        self.assertNotIn("workflow_dispatch:", text)
        self.assertIn("environment: evoguard-artifact-admission", text)
        self.assertNotIn("actions/checkout@", text)
        self.assertNotIn("id-token: write", text)
        self.assertNotIn("contents: write", text)
        self.assertNotIn("attestations: write", text)
        self.assertEqual(text.count("secrets.EVOGUARD_ARTIFACT_ADMISSION_KEY"), 1)
        self.assertLess(
            text.index("Make a fresh provider check before any admission key is materialized"),
            text.index("secrets.EVOGUARD_ARTIFACT_ADMISSION_KEY"),
        )
        seal = text[text.index("- id: seal") : text.index("Remove the admission private key")]
        self.assertNotIn("secrets.", seal)
        self.assertNotIn("EVOGUARD_ARTIFACT_ADMISSION_KEY", seal)

    def test_admission_revalidates_exact_artifacts_and_finalizer(self) -> None:
        text = ADMISSION.read_text(encoding="utf-8")
        for token in (
            "EVOGUARD_ARTIFACT_BUILD_WORKFLOW_ID",
            "artifact-ids: ${{ needs.preflight.outputs.subject_artifact_id }}",
            "artifact-ids: ${{ needs.preflight.outputs.control_artifact_id }}",
            "artifact-ids: ${{ needs.preflight.outputs.finalizer_control_artifact_id }}",
            "artifact-ids: ${{ needs.preflight.outputs.finalizer_evidence_artifact_id }}",
            "artifact-ids: ${{ needs.preflight.outputs.finalizer_bundle_artifact_id }}",
            "derive-finalizer-bindings",
            "verify-finalizer-bindings",
            "verify-finalized",
            "--require-pass",
        ):
            self.assertIn(token, text)

    def test_admission_pins_provider_policy_and_runtimes(self) -> None:
        text = ADMISSION.read_text(encoding="utf-8")
        for token in (
            "7813db5c99f27f780ec31bbaa124b5526405783d1f53caecc32f70aabfbc13c3",
            "b2aef7b23ec6899bf27f37a32c57a7935d0a178568ac33dc9bb03842f724195a",
            "gh_2.90.0_linux_amd64.tar.gz",
            "EvoRiseKsa/evoom-guard-v4-finalizer-pilot/.github/workflows/trusted-artifact-builder.yml",
            BUILDER_MERGE,
            "https://token.actions.githubusercontent.com",
            "runinvocationuri",
            "buildsignerdigest",
            "sourcerepositorydigest",
            "runnerenvironment",
            "github-hosted",
        ):
            self.assertIn(token, text)

    def test_certificate_binding_receives_every_dynamic_policy_input(self) -> None:
        text = ADMISSION.read_text(encoding="utf-8")
        block = text[
            text.index("- name: Bind the provider certificate") :
            text.index("- name: Prepare a lower-privilege provider process wrapper")
        ]
        for token in (
            "BUILD_RUN_ID: ${{ needs.preflight.outputs.build_run_id }}",
            "BUILD_RUN_ATTEMPT: ${{ needs.preflight.outputs.build_run_attempt }}",
            "EXPECTED_HEAD_SHA: ${{ needs.preflight.outputs.head_sha }}",
            "EXPECTED_SOURCE_REF: ${{ needs.preflight.outputs.source_ref }}",
            "GITHUB_REPOSITORY_ID: ${{ github.event.repository.id }}",
        ):
            self.assertIn(token, block)

    def test_lower_privilege_provider_has_an_explicit_config_directory(self) -> None:
        text = ADMISSION.read_text(encoding="utf-8")
        wrapper = text[
            text.index("- name: Prepare a lower-privilege provider process wrapper") :
            text.index("- name: Materialize the distinct admission key")
        ]
        self.assertIn('GH_CONFIG_DIR=%s\\n', wrapper)
        self.assertIn('${GH_CONFIG_DIR:?GH_CONFIG_DIR must be set}', wrapper)
        self.assertIn("-u evoguard-gh", wrapper)

    def test_public_checksum_manifest_covers_pinned_tool_hashes(self) -> None:
        text = ADMISSION.read_text(encoding="utf-8")
        manifest = text[text.index('names = [') : text.index('(root / "SHA256SUMS")')]
        self.assertIn('"guard.sha256"', manifest)
        self.assertIn('"gh.sha256"', manifest)

    def test_admission_seals_verifies_freshly_rechecks_and_has_negatives(self) -> None:
        text = ADMISSION.read_text(encoding="utf-8")
        for token in (
            "seal-github-attestation-admission",
            "verify-github-attestation-admission",
            "reverify-github-attestation-receipt",
            "negative-mutated-subject.json",
            "negative-wrong-source.json",
            "negative-wrong-build-run.json",
            "original_evidence_unchanged",
            "negative unexpectedly passed",
            "retention-days: 90",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
