"""Regression tests for the native reverse-analysis skill snapshot."""
import hashlib
import importlib.util
import io
from pathlib import Path
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("agent_skill", ROOT / "scripts/build-agent-skill.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BuildTests(unittest.TestCase):
    def test_source_is_unabridged(self):
        data, sha, count = MODULE.build()
        original = (ROOT / "skills/reverse-analysis.md").read_bytes()
        self.assertEqual(sha, hashlib.sha256(original).hexdigest())
        self.assertEqual(count, len(original))
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            self.assertEqual(sorted(archive.namelist()), [
                "reverse-analysis/LICENSE",
                "reverse-analysis/SKILL.md",
                "reverse-analysis/references/REPORTING_PROTOCOL.md",
            ])
            skill = archive.read("reverse-analysis/SKILL.md")
            self.assertTrue(skill.startswith(b"---\nname: reverse-analysis\n"))
            self.assertTrue(skill.endswith(original))
            self.assertIn(sha.encode(), skill)
            self.assertEqual(archive.read("reverse-analysis/references/REPORTING_PROTOCOL.md"),
                             (ROOT / "docs/REPORTING_PROTOCOL.md").read_bytes())
            self.assertEqual(archive.read("reverse-analysis/LICENSE"),
                             (ROOT / "LICENSE").read_bytes())
            self.assertIsNone(archive.testzip())

    def test_deterministic_and_compliant_metadata(self):
        data, sha, _ = MODULE.build()
        self.assertEqual(data, MODULE.build()[0])
        self.assertLessEqual(len(MODULE.DESCRIPTION), 1024)
        self.assertRegex(sha, r"^[a-f0-9]{64}$")
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            skill = archive.read("reverse-analysis/SKILL.md").decode()
            self.assertIn("description:", skill.split("---", 2)[1])
            self.assertIn("license: MIT", skill.split("---", 2)[1])


if __name__ == "__main__":
    unittest.main()
