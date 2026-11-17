"""AI Agent Workflow native plugin: one package, 18 skills, no runtime Git access."""

from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build-plugin-marketplace.py"
SPEC = importlib.util.spec_from_file_location("build_marketplace", SCRIPT)
assert SPEC and SPEC.loader
MARKET = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MARKET)


class MarketplaceContracts(unittest.TestCase):
    def test_one_plugin_contains_all_scoped_skills(self) -> None:
        root = ROOT / "plugins/ai-agent-workflow"
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        self.assertEqual(len(marketplace["plugins"]), 1)
        self.assertEqual(marketplace["plugins"][0]["name"], "ai-agent-workflow")
        for name in ("plugin.json", ".codex-plugin/plugin.json"):
            manifest = json.loads((root / name).read_text())
            self.assertEqual(manifest["name"], "ai-agent-workflow")
            self.assertEqual(manifest["skills"], "./skills/")
        skills = list((root / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), len(MARKET.SOURCES))
        for slug, source, description in MARKET.SOURCES:
            skill = root / "skills" / ("aiwf-" + slug) / "SKILL.md"
            body = skill.read_text()
            self.assertLessEqual(len(body), 5000)
            self.assertIn("name: aiwf-" + slug, body)
            self.assertIn(description, body)
            self.assertTrue((skill.parent / "references" / source).is_file())

    def test_every_packaged_reference_matches_authoritative_source(self) -> None:
        base = ROOT / "plugins/ai-agent-workflow/skills"
        for ref in base.glob("*/references/**/*.md"):
            source = ROOT / Path(*ref.relative_to(base).parts[2:])
            self.assertTrue(source.is_file(), ref)
            self.assertEqual(ref.read_bytes(), source.read_bytes())

    def test_markdown_links_resolve_without_repository_checkout(self) -> None:
        pattern = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")
        base = ROOT / "plugins/ai-agent-workflow/skills"
        for file in base.glob("*/references/**/*.md"):
            for href in pattern.findall(file.read_text()):
                if href.startswith(("https:", "http:", "#", "/", "mailto:", "data:")):
                    continue
                target = file.parent / unquote(href.partition("#")[0])
                self.assertTrue(target.exists(), f"{file}: missing {href}")

    def test_generator_is_repeatable_and_detects_drift(self) -> None:
        self.assertEqual(MARKET.update(check=True), (0, 0))
        with tempfile.TemporaryDirectory() as temp, patch.multiple(
            MARKET, ROOT=Path(temp), OUT=Path(temp) / MARKET.PLUGIN,
            MANIFEST=Path(temp) / ".agents/plugins/marketplace.json"
        ):
            # Templates are read from the original source. Simulate an existing
            # package entry and verify the drift guard without touching Git.
            with patch.object(MARKET, "generated_files", return_value={
                Path("plugins/ai-agent-workflow/plugin.json"): b"{}",
                Path(".agents/plugins/marketplace.json"): b"{}",
            }):
                self.assertEqual(MARKET.update(check=False), (2, 0))
                self.assertEqual(MARKET.update(check=True), (0, 0))
                target = Path(temp) / "plugins/ai-agent-workflow/plugin.json"
                target.write_text("changed")
                with self.assertRaisesRegex(ValueError, "Marketplace drift"):
                    MARKET.update(check=True)

    def test_all_owner_map_entries_have_a_skill(self) -> None:
        routes = set(re.findall(
            re.escape(chr(96)) + r"([^\x60]+\.md)" + re.escape(chr(96)),
            (ROOT / "skills/README.md").read_text(encoding="utf-8"),
        ))
        actual = {path.replace("skills/", "", 1) for _, path, _ in MARKET.SOURCES}
        self.assertEqual(routes, actual)

    def test_non_allowlisted_paths_are_rejected(self) -> None:
        for unsafe in ("prompts/accounts/universal.md", "../.git/config", "skills/absent.md"):
            with self.assertRaises(ValueError):
                MARKET._source(unsafe)


if __name__ == "__main__":
    unittest.main()
