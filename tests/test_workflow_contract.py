from __future__ import annotations

import re
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
REVERIFY = ROOT / ".github" / "workflows" / "evoguard-reverify.yml"
SEAL = ROOT / ".github" / "workflows" / "evoguard-seal.yml"
RUNTIME_URL = (
    "https://github.com/EvoRiseKsa/EvoOM-Guard-m/"
    "releases/download/v4.0.2/evo-guard.pyz"
)
PACK_SHA256 = "aa97da0bdff54432f0371e531c6d71a955a0de732a81bbf006bec60bf348ebf4"


class WorkflowContractTests(unittest.TestCase):
    def test_policy_pins_the_v4_pack_identity(self) -> None:
        policy = (ROOT / ".evoguard.json").read_text(encoding="utf-8")
        self.assertIn(f'"expect_verifier_pack_sha256": "{PACK_SHA256}"', policy)

    def test_runtime_url_is_exact_and_present_once_per_workflow(self) -> None:
        for path in (REVERIFY, SEAL):
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count(RUNTIME_URL), 1, path)
            urls = re.findall(
                r"https://github\.com/EvoRiseKsa/EvoOM-Guard-m/"
                r"releases/download/v[^/]+/evo-guard\.pyz",
                text,
            )
            self.assertEqual(urls, [RUNTIME_URL], path)

    def test_unprivileged_workflow_has_no_key_or_secret(self) -> None:
        text = REVERIFY.read_text(encoding="utf-8")
        self.assertNotIn("secrets.", text)
        self.assertNotIn("EVOGUARD_FINALIZER_KEY", text)
        self.assertIn("derive-finalizer-bindings", text)
        self.assertIn("verify-finalizer-bindings", text)

    def test_key_is_confined_to_protected_seal_job(self) -> None:
        text = SEAL.read_text(encoding="utf-8")
        self.assertIn("environment: evoguard-finalizer", text)
        self.assertIn("secrets.EVOGUARD_FINALIZER_KEY", text)
        self.assertIn("actions/checkout", REVERIFY.read_text(encoding="utf-8"))
        self.assertNotIn("actions/checkout", text)

    def test_all_github_actions_are_full_sha_pinned(self) -> None:
        combined = REVERIFY.read_text(encoding="utf-8") + SEAL.read_text(encoding="utf-8")
        refs = re.findall(r"uses:\s*actions/[A-Za-z0-9_.-]+@([^\s#]+)", combined)
        self.assertTrue(refs)
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{40}", ref) for ref in refs))


if __name__ == "__main__":
    unittest.main()
