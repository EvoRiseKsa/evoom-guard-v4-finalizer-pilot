from __future__ import annotations

import subprocess
import sys
import unittest

from calc.ops import add


class CalculatorTests(unittest.TestCase):
    def test_add_returns_integer_sum(self) -> None:
        self.assertEqual(add(2, 3), 5)

    def test_cli_uses_public_protocol(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-m", "calc", "add", "10", "20"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "30")


if __name__ == "__main__":
    unittest.main()
