from __future__ import annotations

import base64
import hashlib
import io
import json
from pathlib import Path
import unittest
import zipfile


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "evidence" / "round1"
OBSERVATION = EVIDENCE / "OBSERVATION.json"
BUNDLE_B64 = EVIDENCE / "final-allow.evb.b64"

HEAD = "03868cf84825b7aaa9bdb0efd88f215eb878b943"
BUNDLE_SHA256 = "d2f0f598d6b0e08c545345d86a3f762786afd2c551a29e710d9cd53e8ea4a4b3"
BINDINGS_SHA256 = "c16b737762d8ba078c40d851d21f696e686dbf20940c5eda579497a69a2c20f3"


def strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_strict(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=strict_object)


class Round1EvidenceTests(unittest.TestCase):
    def test_observation_is_strict_and_has_expected_sequence(self) -> None:
        observation = load_strict(OBSERVATION)
        self.assertEqual(observation["format"], "EVOGUARD_V4_FINALIZER_PILOT_ROUND1_V1")
        self.assertEqual(observation["candidate"]["head_sha"], HEAD)
        sequence = observation["sequence"]
        self.assertEqual(
            [(item["phase"], item["decision"]) for item in sequence],
            [
                ("bootstrap_fail_closed", "DENY"),
                ("first_complete_allow", "ALLOW"),
                ("cancelled_fresh_attempt", "DENY"),
                ("final_complete_allow", "ALLOW"),
            ],
        )

    def test_cancelled_attempt_cannot_inherit_allow(self) -> None:
        observation = load_strict(OBSERVATION)
        cancelled = observation["sequence"][2]
        self.assertEqual(cancelled["reverify_conclusion"], "cancelled")
        self.assertEqual(cancelled["metadata_job"], "success")
        self.assertEqual(cancelled["reverify_evidence_artifact_count"], 0)
        self.assertEqual(cancelled["protected_seal_job"], "skipped")
        self.assertEqual(cancelled["check_conclusion"], "failure")
        self.assertEqual(cancelled["sealed_artifact_count"], 0)

    def test_retained_bundle_hashes_and_internal_manifest(self) -> None:
        encoded = "".join(BUNDLE_B64.read_text(encoding="ascii").split())
        bundle = base64.b64decode(encoded, validate=True)
        self.assertEqual(hashlib.sha256(bundle).hexdigest(), BUNDLE_SHA256)

        with zipfile.ZipFile(io.BytesIO(bundle), "r") as archive:
            self.assertEqual(len(archive.namelist()), len(set(archive.namelist())))
            self.assertEqual(
                set(archive.namelist()),
                {
                    "bundle.json",
                    "bundle.sig",
                    "record/verdict.json",
                    "materials/000-trusted-finalizer-git-bindings",
                    "materials/001-trusted-finalizer-handoff",
                },
            )
            manifest = json.loads(archive.read("bundle.json"))
            verdict = archive.read("record/verdict.json")
            bindings = archive.read("materials/000-trusted-finalizer-git-bindings")
            self.assertEqual(manifest["format"], "EVOGUARD_EVIDENCE_BUNDLE_V1")
            self.assertEqual(manifest["context"]["head_sha"], HEAD)
            self.assertEqual(manifest["context"]["run_id"], "29870833745")
            self.assertEqual(hashlib.sha256(verdict).hexdigest(), manifest["record"]["sha256"])
            self.assertEqual(hashlib.sha256(bindings).hexdigest(), BINDINGS_SHA256)
            self.assertEqual(manifest["materials"][0]["sha256"], BINDINGS_SHA256)

    def test_archived_expected_context_matches_observation(self) -> None:
        observation = load_strict(OBSERVATION)
        source = load_strict(EVIDENCE / "final-allow-expected-source.json")
        context = load_strict(EVIDENCE / "final-allow-expected-context.json")
        bindings = load_strict(EVIDENCE / "final-allow-derived-bindings.json")
        self.assertEqual(source["head_sha"], observation["candidate"]["head_sha"])
        self.assertEqual(source["workflow_run_id"], "29870833745")
        self.assertEqual(context["run_id"], source["workflow_run_id"])
        self.assertEqual(context["candidate_sha256"], observation["candidate"]["candidate_sha256"])
        self.assertEqual(bindings["source"], source)
        self.assertEqual(
            hashlib.sha256(
                (EVIDENCE / "final-allow-derived-bindings.json").read_bytes()
            ).hexdigest(),
            BINDINGS_SHA256,
        )

    def test_claims_remain_narrow(self) -> None:
        claims = load_strict(OBSERVATION)["claim_boundary"]
        self.assertTrue(claims["same_owner_non_independent_exercise"])
        for key in (
            "production_merge_gate",
            "hostile_code_vm_boundary",
            "artifact_build_or_release_admission",
            "independent_security_audit",
        ):
            self.assertFalse(claims[key], key)


if __name__ == "__main__":
    unittest.main()
