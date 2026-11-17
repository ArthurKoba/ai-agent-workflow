"""Selectable native plugins: distinct domain packages and no runtime Git access."""

from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build-plugin-marketplace.py"
SPEC = importlib.util.spec_from_file_location("build_marketplace", SCRIPT)
assert SPEC and SPEC.loader
MARKET = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MARKET)


def plugin_skill_paths() -> list[Path]:
    return [
        skill
        for info in MARKET.GROUPS.values()
        for skill in (ROOT / "plugins" / info["id"] / "skills").glob("*/SKILL.md")
    ]


class MarketplaceContracts(unittest.TestCase):
    def test_six_independently_installable_plugins_contain_each_skill_once(self) -> None:
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        self.assertEqual(marketplace["name"], "ai-agent-workflow")
        self.assertEqual(
            marketplace["interface"]["displayName"],
            "Arthur Koba AI Agent Workflow",
        )
        entries = marketplace["plugins"]
        self.assertEqual(len(entries), 6)
        self.assertEqual(
            [entry["name"] for entry in entries],
            [info["id"] for info in MARKET.GROUPS.values()],
        )
        self.assertFalse((ROOT / "plugins/ai-agent-workflow").exists())
        for retired in MARKET.RETIRED_PLUGINS:
            self.assertFalse((ROOT / "plugins" / retired).exists())
        counts: Counter[str] = Counter()
        for entry in entries:
            self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
            self.assertEqual(entry["source"]["source"], "local")
            root = ROOT / entry["source"]["path"]
            self.assertTrue(root.is_dir())
            self.assertFalse(list(root.rglob("aiwf-*/SKILL.md")))
            for manifest_path in ("plugin.json", ".codex-plugin/plugin.json"):
                manifest = json.loads((root / manifest_path).read_text(encoding="utf-8"))
                self.assertEqual(manifest["name"], entry["name"])
                self.assertEqual(manifest["skills"], "./skills/")
                if manifest_path == "plugin.json":
                    self.assertEqual(manifest["author"]["name"], "Arthur Koba")
                    interface = manifest["extensions"]["com.openai"]["interface"]
                else:
                    interface = manifest["interface"]
                self.assertEqual(interface["developerName"], "Arthur Koba")
                self.assertTrue(
                    interface["displayName"].startswith("Arthur Koba AI Agent Workflow")
                )
                self.assertNotIn("logo", interface)
            for skill in (root / "skills").glob("*/SKILL.md"):
                slug = skill.parent.name
                counts[slug] += 1
                body = skill.read_text(encoding="utf-8")
                self.assertLessEqual(len(body), 5000)
                self.assertIn("name: " + slug, body)
                self.assertIn("references/skills/", body)
        self.assertEqual(len(counts), len(MARKET.SOURCES))
        self.assertEqual(sum(counts.values()), 28)
        self.assertTrue(all(count == 1 for count in counts.values()))
        self.assertEqual(set(counts), {slug for _, slug, _, _ in MARKET.SOURCES})

    def test_plugin_membership_is_exactly_task_map_sections(self) -> None:
        for group_id, slug, source, description in MARKET.SOURCES:
            skill = ROOT / "plugins" / group_id / "skills" / slug / "SKILL.md"
            self.assertTrue(skill.is_file(), skill)
            self.assertIn(description, skill.read_text(encoding="utf-8"))
            self.assertTrue((skill.parent / "references" / source).is_file(), skill)
        sections = {
            info["id"]: {slug for grp, slug, _, _ in MARKET.SOURCES if grp == info["id"]}
            for info in MARKET.GROUPS.values()
        }
        expected = {
            "arthur-koba-development": {
                "backend-engineering",
                "software-architecture",
                "project-bootstrap",
                "frontend-engineering",
                "interface-design-review",
                "software-testing",
                "code-review",
            },
            "arthur-koba-devops": {
                "git-workflow",
                "terminal-operations",
                "services-deployment",
            },
            "arthur-koba-agents": {
                "orchestration",
                "context-engineering",
                "skill-authoring",
                "workflow-audit",
            },
            "arthur-koba-research": {
                "reverse-analysis",
                "openipc-porting",
            },
            "arthur-koba-science": {
                "scientific-research-design",
                "scientific-novelty",
                "scientific-literature",
                "scientific-experiments",
                "scientific-implementation",
                "scientific-formatting-ru",
                "scientific-writing",
                "scientific-mathematics",
                "scientific-review",
                "scientific-visualization",
            },
            "arthur-koba-other": {"domain-acquisition", "workflow-marketplace"},
        }
        self.assertEqual(sections, expected)

    def test_packaged_references_match_single_authoritative_sources(self) -> None:
        for skill in plugin_skill_paths():
            folder = skill.parent / "references"
            for file in folder.rglob("*.md"):
                path = file.relative_to(folder)
                original = ROOT / path
                self.assertTrue(original.is_file(), file)
                self.assertEqual(file.read_bytes(), original.read_bytes(), file)

    def test_links_resolve_independently_inside_each_installable_plugin(self) -> None:
        pattern = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")
        for skill in plugin_skill_paths():
            root = skill.parent
            for file in (root / "references").rglob("*.md"):
                for href in pattern.findall(file.read_text(encoding="utf-8")):
                    if href.startswith(("https:", "http:", "#", "/", "mailto:", "data:")):
                        continue
                    target = file.parent / unquote(href.partition("#")[0])
                    self.assertTrue(target.exists(), f"{file}: missing {href}")

    def test_generator_is_repeatable_and_retires_legacy_package(self) -> None:
        self.assertEqual(MARKET.update(check=True), (0, 0))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with (
                patch.object(MARKET, "ROOT", root),
                patch.object(MARKET, "MANIFEST", root / ".agents/plugins/marketplace.json"),
                patch.object(
                    MARKET,
                    "generated_files",
                    return_value={
                        Path("plugins/arthur-koba-backend/plugin.json"): b"{}",
                        Path(".agents/plugins/marketplace.json"): b"{}",
                    },
                ),
            ):
                old = root / "plugins/ai-agent-workflow/skills/old/SKILL.md"
                old.parent.mkdir(parents=True)
                old.write_bytes(b"obsolete")
                retired_browser = (
                    root / "plugins/arthur-koba-browser/skills/"
                    "remote-browser-session/SKILL.md"
                )
                retired_browser.parent.mkdir(parents=True)
                retired_browser.write_bytes(b"retired browser")
                self.assertEqual(MARKET.update(check=False), (2, 2))
                self.assertFalse(old.exists())
                self.assertFalse((root / "plugins/ai-agent-workflow").exists())
                self.assertFalse(retired_browser.exists())
                self.assertFalse((root / "plugins/arthur-koba-browser").exists())
                self.assertEqual(MARKET.update(check=True), (0, 0))
                target = root / "plugins/arthur-koba-backend/plugin.json"
                target.write_text("changed")
                with self.assertRaisesRegex(ValueError, "Marketplace drift"):
                    MARKET.update(check=True)

    def test_all_owner_map_entries_have_one_mapped_skill(self) -> None:
        routes = set(
            re.findall(
                re.escape(chr(96)) + r"([^\x60]+\.md)" + re.escape(chr(96)),
                (ROOT / "skills/README.md").read_text(encoding="utf-8"),
            )
        )
        actual = {path.replace("skills/", "", 1) for _, _, path, _ in MARKET.SOURCES}
        self.assertEqual(routes, actual)

    def test_new_task_map_skill_discovers_group_but_unknown_group_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "skills").mkdir()
            task_map = root / "skills/README.md"
            task_map.write_text(
                "## Operations\n\n- operational verification → "
                + chr(96)
                + "ops-validation.md"
                + chr(96)
                + "\n",
                encoding="utf-8",
            )
            with (
                patch.object(MARKET, "ROOT", root),
                patch.object(MARKET, "GROUPS", {"Operations": {"id": "test-ops"}}),
            ):
                self.assertEqual(
                    MARKET._discover_sources(),
                    (("test-ops", "ops-validation", "skills/ops-validation.md", "operational verification"),),
                )
                task_map.write_text("## Unknown group\n\n- x → " + chr(96) + "x.md" + chr(96))
                with self.assertRaisesRegex(ValueError, "Unknown selectable"):
                    MARKET._discover_sources()

    def test_architecture_is_language_neutral_and_independent_of_backend(self) -> None:
        architecture = (ROOT / "skills/software-architecture.md").read_text()
        backend = (ROOT / "skills/backend-engineering.md").read_text()
        implementation = (ROOT / "skills/software-engineering/README.md").read_text()
        self.assertIn("independent of language", architecture)
        self.assertIn("Rust", architecture)
        self.assertIn("Rust", backend)
        self.assertIn("Rust", implementation)
        self.assertIn("conditional", implementation)
        self.assertFalse(
            list((ROOT / "plugins").glob("*/skills/software-engineering/SKILL.md"))
        )
        self.assertTrue(
            (ROOT / "plugins/arthur-koba-development/skills/software-architecture/SKILL.md").is_file()
        )
        self.assertTrue(
            (ROOT / "plugins/arthur-koba-development/skills/backend-engineering/SKILL.md").is_file()
        )

    def test_retired_browser_skill_and_plugin_do_not_return(self) -> None:
        self.assertFalse((ROOT / "skills/remote-browser-session.md").exists())
        self.assertFalse((ROOT / "skills/remote-browser-session").exists())
        self.assertFalse((ROOT / "plugins/arthur-koba-browser").exists())
        self.assertIn("arthur-koba-browser", MARKET.RETIRED_PLUGINS)
        self.assertFalse((ROOT / "plugins/arthur-koba-domains").exists())
        self.assertIn("arthur-koba-domains", MARKET.RETIRED_PLUGINS)
        self.assertNotIn("remote-browser-session", {
            slug for _, slug, _, _ in MARKET.SOURCES
        })
        self.assertNotIn("arthur-koba-browser", {
            info["id"] for info in MARKET.GROUPS.values()
        })
        self.assertNotIn(
            "remote-browser-session",
            (ROOT / "skills/README.md").read_text(encoding="utf-8"),
        )

    def test_science_owns_ten_independent_evidence_scoped_skills(self) -> None:
        slugs = {
            "scientific-research-design",
            "scientific-novelty",
            "scientific-literature",
            "scientific-experiments",
            "scientific-implementation",
            "scientific-formatting-ru",
            "scientific-writing",
            "scientific-mathematics",
            "scientific-review",
            "scientific-visualization",
        }
        package = ROOT / "plugins/arthur-koba-science/skills"
        self.assertEqual(
            {path.parent.name for path in package.glob("*/SKILL.md")}, slugs
        )
        for slug in slugs:
            with self.subTest(slug=slug):
                source = ROOT / "skills" / (slug + ".md")
                packaged = package / slug / "references/skills" / source.name
                self.assertEqual(packaged.read_bytes(), source.read_bytes())
                self.assertLessEqual(len(source.read_text(encoding="utf-8")), 5000)
                body = (package / slug / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("name: " + slug, body)
                for forbidden in (
                    "AI-Science",
                    "Barelief",
                    "BDSP",
                    "2.3.1",
                    "SUP-",
                    "vestcyber",
                    "github.com/ArthurKoba/AI-Science",
                ):
                    self.assertNotIn(forbidden.lower(), source.read_text(encoding="utf-8").lower())
                self.assertFalse(
                    (ROOT / "plugins/arthur-koba-research/skills" / slug).exists()
                )

    def test_science_localization_is_opt_in_and_publications_are_consolidated(self) -> None:
        science = ROOT / "plugins/arthur-koba-science/skills"
        self.assertFalse((science / "scientific-publications").exists())
        self.assertFalse((ROOT / "skills/scientific-publications.md").exists())
        writing = (ROOT / "skills/scientific-writing.md").read_text(encoding="utf-8")
        self.assertIn("Manuscript structure and publication formatting", writing)
        locale = (ROOT / "skills/scientific-formatting-ru.md").read_text(encoding="utf-8")
        self.assertIn("regional supplement", locale)
        self.assertIn("GOST", locale)
        chart = (ROOT / "skills/scientific-visualization/charts.md").read_text(encoding="utf-8")
        self.assertNotIn("short Russian labels", chart)
        self.assertNotIn("Cyrillic** letters", chart)
        authoring = (ROOT / "skills/scientific-visualization/authoring.md").read_text(encoding="utf-8")
        self.assertIn(".drawio", authoring)
        self.assertIn("SVG", authoring)
        self.assertIn(".xlsx", (ROOT / "skills/scientific-visualization/charts.md").read_text(encoding="utf-8"))

    def test_science_preserves_editable_figures_and_project_specific_join_markers(self) -> None:
        source = ROOT / "skills/scientific-visualization.md"
        base = ROOT / "skills/scientific-visualization"
        packaged = (
            ROOT / "plugins/arthur-koba-science/skills/"
            "scientific-visualization/references/skills"
        )
        files = {path.name for path in base.glob("*.md")}
        self.assertEqual(
            files,
            {"authoring.md", "diagrams.md", "charts.md", "verification.md"},
        )
        self.assertEqual(
            source.read_bytes(),
            (packaged / source.relative_to(ROOT / "skills")).read_bytes(),
        )
        for file in base.glob("*.md"):
            self.assertLessEqual(len(file.read_text(encoding="utf-8")), 5000)
            self.assertEqual(
                file.read_bytes(),
                (packaged / file.relative_to(ROOT / "skills")).read_bytes(),
            )
        diagrams = (base / "diagrams.md").read_text(encoding="utf-8")
        self.assertIn("junction dot at a real merge", diagrams)
        self.assertIn("when required", diagrams)
        self.assertIn("notation forbids it", diagrams)
        self.assertIn("crossing", diagrams.lower())
        charts = (base / "charts.md").read_text(encoding="utf-8")
        self.assertIn("Reproducible spreadsheet-first workflow", charts)
        self.assertIn("MODEL EXAMPLE", charts)
        self.assertIn("SVG", charts)
        self.assertIn("Draw.io", (base / "authoring.md").read_text(encoding="utf-8"))

    def test_other_owns_domain_acquisition_and_on_demand_contributions(self) -> None:
        other = ROOT / "plugins/arthur-koba-other/skills"
        self.assertTrue((other / "domain-acquisition/SKILL.md").is_file())
        marketplace = other / "workflow-marketplace"
        self.assertTrue((marketplace / "SKILL.md").is_file())
        source = ROOT / "skills/workflow-marketplace.md"
        content = source.read_text(encoding="utf-8")
        self.assertLessEqual(len(content), 5000)
        self.assertEqual(
            source.read_bytes(),
            (marketplace / "references/skills/workflow-marketplace.md").read_bytes(),
        )
        self.assertIn("https://github.com/ArthurKoba/ai-agent-workflow", content)
        self.assertIn(".agents/plugins/marketplace.json", content)
        self.assertIn("on-demand", content)
        self.assertIn("contribute", content.lower())
        self.assertIn("not\nauthorization to schedule ongoing monitoring", content)
        self.assertFalse(
            (ROOT / "plugins/arthur-koba-devops/skills/domain-acquisition").exists()
        )

    def test_reverse_analysis_is_independent_of_engines_and_mcp(self) -> None:
        router = ROOT / "skills/reverse-analysis.md"
        files = [router, *sorted((ROOT / "skills/reverse-analysis").glob("*.md"))]
        self.assertEqual(len(files), 11)
        compiled = []
        for file in files:
            text = file.read_text(encoding="utf-8")
            self.assertLessEqual(len(text), 5000, file.name)
            for forbidden in (
                "ghidra",
                "radare2",
                "mcp__",
                "run_analysis_script",
                "GHIDRA_MCP",
                "job_start(",
                "get_storage_info(",
            ):
                self.assertNotIn(forbidden.lower(), text.lower(), str(file))
            compiled.append(text)
        contents = "\n".join(compiled)
        for essential in ("CONFIRMED", "LIKELY", "UNKNOWN", "CONTRADICTION", "WITHDRAWN"):
            self.assertIn(essential, contents)
        packaged = ROOT / "plugins/arthur-koba-research/skills/reverse-analysis/references"
        for file in files:
            self.assertEqual(file.read_bytes(), (packaged / file.relative_to(ROOT)).read_bytes())

    def test_publisher_stages_all_packages_and_the_retired_one(self) -> None:
        root = ROOT / ".github/workflows"
        publisher = (root / "publish-plugin-marketplace.yml").read_text()
        self.assertIn("workflow_dispatch:", publisher)
        self.assertIn("branches: [main]", publisher)
        self.assertIn("python3 scripts/build-plugin-marketplace.py", publisher)
        self.assertIn("git add -A -- .agents/plugins/marketplace.json plugins/", publisher)
        self.assertIn("git push origin HEAD:main", publisher)
        self.assertNotIn("BRIAREUS_DISPATCH_TOKEN", publisher)
        self.assertNotIn("KobaProduction/Briareus", publisher)
        self.assertFalse((root / "notify-briareus.yml").exists())

    def test_non_allowlisted_paths_are_rejected(self) -> None:
        for unsafe in ("prompts/accounts/universal.md", "../.git/config", "skills/absent.md"):
            with self.assertRaises(ValueError):
                MARKET._source(unsafe)


if __name__ == "__main__":
    unittest.main()
