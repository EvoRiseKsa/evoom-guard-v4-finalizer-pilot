from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "evidence" / "artifact-admission" / "round1"
BASE_SHA = "a602c2b007fad4d5627476187bcbc8c218c16be9"
HEAD_SHA = "a3c71c622cc9818242ae5294bc550ee75674ab1d"
ARTIFACT_SHA256 = "555695a5b1b6aa082495dc8b4faeb5562fcbc7e23124daf046ef4592d253eae6"


class ArtifactAdmissionRound1Tests(unittest.TestCase):
    def test_positive_evidence_manifest_is_complete_and_unchanged(self) -> None:
        lines = (EVIDENCE / "SHA256SUMS").read_text(encoding="ascii").splitlines()
        self.assertEqual(len(lines), 27)
        observed: set[str] = set()
        for line in lines:
            match = re.fullmatch(r"([0-9a-f]{64})  ([^\\]+)", line)
            self.assertIsNotNone(match, line)
            assert match is not None
            digest, relative = match.groups()
            self.assertNotIn(relative, observed)
            observed.add(relative)
            target = EVIDENCE / Path(relative)
            self.assertTrue(target.is_file(), relative)
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), digest)

    def test_observation_binds_the_exact_successful_round(self) -> None:
        observation = json.loads((EVIDENCE / "OBSERVATION.json").read_bytes())
        self.assertEqual(observation["format"], "EVOGUARD_ARTIFACT_ADMISSION_OBSERVATION_V1")
        self.assertEqual(observation["base_sha"], BASE_SHA)
        self.assertEqual(observation["head_sha"], HEAD_SHA)
        self.assertEqual(observation["pr_number"], 7)
        self.assertEqual(observation["finalizer_reverify_run_id"], "29878266034")
        self.assertEqual(observation["finalizer_seal_run_id"], "29878298540")
        self.assertEqual(observation["build_run_id"], "29878399911")

    def test_retained_reports_are_allow_and_negative_controls_reject(self) -> None:
        retained = json.loads((EVIDENCE / "retained-verify-report.json").read_bytes())
        self.assertTrue(retained["ok"])
        self.assertTrue(retained["verified"])
        self.assertEqual(retained["status"], "VERIFIED")
        self.assertEqual(retained["decision"], "ALLOW")
        self.assertEqual(retained["artifact"]["sha256"], ARTIFACT_SHA256)
        self.assertEqual(retained["finalizer"]["context"]["base_sha"], BASE_SHA)
        self.assertEqual(retained["finalizer"]["context"]["head_sha"], HEAD_SHA)

        negatives = json.loads((EVIDENCE / "negative-controls.json").read_bytes())
        self.assertTrue(negatives["original_evidence_unchanged"])
        self.assertEqual(len(negatives["rejected_cases"]), 13)
        self.assertTrue(all(code != 0 for code in negatives["rejected_cases"].values()))

    def test_archive_contains_no_private_key_material(self) -> None:
        for target in EVIDENCE.rglob("*"):
            if target.is_file():
                self.assertNotIn(b"BEGIN PRIVATE KEY", target.read_bytes(), str(target))


if __name__ == "__main__":
    unittest.main()
