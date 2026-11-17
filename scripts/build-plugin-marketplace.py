#!/usr/bin/env python3
"""Package selectable, self-contained Arthur Koba AI Agent Workflow plugin groups."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
from collections import deque
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = Path("plugins")
MANIFEST = ROOT / ".agents/plugins/marketplace.json"
LEGACY_PLUGIN = "ai-agent-workflow"
RETIRED_PLUGINS = (
    "arthur-koba-backend",
    "arthur-koba-architecture",
    "arthur-koba-frontend",
    "arthur-koba-quality",
    "arthur-koba-browser",
    "arthur-koba-domains",
)
MARKETPLACE_TITLE = "Arthur Koba AI Agent Workflow"

# Each category is an independent installable plugin. Skills are assigned by
# section in skills/README.md: there must be exactly one owner per Skill.
# The marketing title retains Arthur Koba's name, while the machine IDs are
# stable, unique and not inferred from display text.
GROUPS = {
    "Development": {
        "id": "arthur-koba-development",
        "title": "Development",
        "short": "Backend, frontend, architecture, testing and code review",
        "description": "Complete language-neutral software development, including Rust/Python backends, UI, testing and review.",
    },
    "DevOps & Infrastructure": {
        "id": "arthur-koba-devops",
        "title": "DevOps",
        "short": "Git, terminal, services and deployments",
        "description": "Git workflows, shell operations, infrastructure and service deployment.",
    },
    "Agent Workflows": {
        "id": "arthur-koba-agents",
        "title": "Agent Workflows",
        "short": "Agent orchestration, context and reusable Skills",
        "description": "Coordination, context engineering, Skill authoring and workflow audits.",
    },
    "Software Research": {
        "id": "arthur-koba-research",
        "title": "Software Research",
        "short": "Software reverse analysis and firmware porting",
        "description": "Evidence-based analysis of programs, firmware and OpenIPC porting.",
    },
    "Science": {
        "id": "arthur-koba-science",
        "title": "Science",
        "short": "Research methods, novelty, papers, experiments and scientific figures",
        "description": "Evidence-based scientific research, novelty and literature review, reproducible experiments, writing, mathematical notation, implementation, peer review and visualizations.",
    },
    "Other": {
        "id": "arthur-koba-other",
        "title": "Other",
        "short": "Domain ownership and AI Agent Workflow updates",
        "description": "Optional domain acquisition and on-demand Skill marketplace discovery and contributions.",
    },
}

ALLOWED = frozenset({"skills", "docs", "audit", "context", "playbook", "examples"})
CURATED_DESCRIPTIONS = {
    "backend-engineering": "Backend services and APIs across Rust, Python, Go and other languages",
    "software-architecture": "Language-neutral software architecture, DDD and ownership",
    "frontend-engineering": "Frontend architecture, Vue, TypeScript, layouts and accessible UI",
    "software-testing": "Design, select and verify tests across product boundaries",
    "project-bootstrap": "Project setup, toolchains, quality gates, hooks and CI",
    "skill-authoring": "Create, review, refactor and validate reusable agent skills",
    "git-workflow": "Git, branches, commits, review, publication and issues",
    "orchestration": "Multi-agent coordination, PDCA, delegation and handoffs",
    "code-review": "Independent technical reviews, evidence and acceptance",
    "interface-design-review": "Interface design review, accessibility and user journeys",
    "scientific-research-design": "Scientific question, objectives, models and testable research design",
    "scientific-novelty": "Evidence-based scientific novelty and personal contribution assessment",
    "scientific-literature": "Scientific literature verification, citations and critical synthesis",
    "scientific-experiments": "Research experiments, reproducibility, fair baselines and statistics",
    "scientific-implementation": "Scientific method implementation, validation and practical adoption",
    "scientific-writing": "Scientific articles, manuscript writing, editing and venue formatting",
    "scientific-formatting-ru": "Russian venue-specific scientific formatting and style requirements",
    "scientific-mathematics": "Complete scientific formulas, notation, units and faithful export",
    "scientific-review": "Independent scientific content review and revision acceptance",
    "scientific-visualization": "Technical diagrams, scientific figures and measured plots",
    "terminal-operations": "Shell, PowerShell, SSH, serial and terminal operations",
    "services-deployment": "Services, Docker Compose, Coolify, environments and deployments",
    "reverse-analysis": "Reverse engineering, firmware, binaries, tracing and evidence",
    "openipc-porting": "OpenIPC firmware porting and contribution workflows",
    "context-engineering": "Agent context management, source maps and progressive disclosure",
    "workflow-audit": "Agent workflow and prompt audits",
    "domain-acquisition": "Domain registration, transfers, pricing and continuity",
    "workflow-marketplace": "Discover Arthur Koba AI Agent Workflow updates and contribute reusable skills",
}


LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")
CODE_PATH = re.compile(r"`([^`\s]+\.md(?:#[^`\s]*)?)`")



def _discover_sources() -> tuple[tuple[str, str, str, str], ...]:
    """The source task map owns both Skill discovery and plugin membership."""
    found: list[tuple[str, str, str, str]] = []
    group: str | None = None
    for line in (ROOT / "skills/README.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            group = line[3:].strip()
            if group not in GROUPS:
                raise ValueError(f"Unknown selectable marketplace section: {group}")
            continue
        if not line.startswith("- ") or "→" not in line:
            continue
        if group is None:
            raise ValueError(f"Skill entry without marketplace section: {line}")
        heading, route = line.split("→", 1)
        match = re.search(r"`([^`]+\.md)`", route)
        if match is None:
            raise ValueError(f"Unroutable Skill map entry: {line}")
        path = "skills/" + match.group(1)
        entry = Path(path)
        slug = entry.parent.name if entry.name == "README.md" else entry.stem
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError(f"Invalid Skill identifier: {slug}")
        description = CURATED_DESCRIPTIONS.get(slug, heading[2:].strip())
        found.append((GROUPS[group]["id"], slug, path, description))
    if not found or len({slug for _, slug, _, _ in found}) != len(found):
        raise ValueError("Empty or ambiguous Skill map")
    if len({path for _, _, path, _ in found}) != len(found):
        raise ValueError("Duplicate Skill source in map")
    for meta in GROUPS.values():
        if not any(group_id == meta["id"] for group_id, _, _, _ in found):
            raise ValueError(f"Empty selectable plugin: {meta['id']}")
    return tuple(found)


SOURCES = _discover_sources()

def _json(data: object) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _source(path: str) -> Path:
    if not path.startswith(tuple(prefix + "/" for prefix in ALLOWED)):
        raise ValueError(f"Unsupported source owner: {path}")
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to(ROOT) or not resolved.is_file():
        raise ValueError(f"Missing/unsafe source: {path}")
    if (ROOT / path).is_symlink():
        raise ValueError(f"Symlink source forbidden: {path}")
    return resolved


def _linked_documents(path: str, text: str) -> set[str]:
    found: set[str] = set()
    for token in [*LINK.findall(text), *CODE_PATH.findall(text)]:
        if token.startswith(("http:", "https:", "#", "/", "mailto:", "data:")):
            continue
        target = token.split("#", 1)[0]
        if not target or any(c in target for c in "{}*<>"):
            continue
        local = posixpath.normpath(posixpath.join(posixpath.dirname(path), unquote(target)))
        if local.startswith("../") or local == "..":
            continue
        if (ROOT / local).is_dir():
            local = posixpath.join(local, "README.md")
        if local.startswith(tuple(prefix + "/" for prefix in ALLOWED)):
            if (ROOT / local).is_file():
                found.add(local)
    return found


def _roots(source: str) -> set[str]:
    root = Path(source)
    result = {source}
    folder = root.parent if root.name == "README.md" else root.parent / root.stem
    if (ROOT / folder).is_dir():
        result.update(
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / folder).rglob("*.md")
            if path.is_file()
        )
    return result


def _closure(source: str) -> dict[str, bytes]:
    queue = deque(sorted(_roots(source)))
    included: dict[str, bytes] = {}
    while queue:
        path = queue.popleft()
        if path in included:
            continue
        raw = _source(path).read_bytes()
        raw.decode("utf-8")
        if len(raw) > 256 * 1024:
            raise ValueError(f"Reference too large: {path}")
        included[path] = raw
        if len(included) > 150:
            raise ValueError(f"Reference closure too large for {source}")
        queue.extend(sorted(_linked_documents(path, raw.decode("utf-8")) - included.keys()))
    return included


def _skill_file(slug: str, source: str, description: str) -> bytes:
    title = slug.replace("-", " ").title()
    content = (
        "---\n"
        f"name: {slug}\n"
        f"description: {json.dumps(description, ensure_ascii=False)}\n"
        "---\n\n"
        f"# {title}\n\n"
        f"Use this skill for: {description.lower()}.\n\n"
        f"Read [the authoritative workflow](references/{source}) completely when "
        "the task requires this domain. That entrypoint routes to conditional "
        "modules under the references directory; read only the modules relevant "
        "to the task and fully read any module it marks mandatory.\n\n"
        "This package includes versioned reference documents locally. "
        "Do not require access to the AI Agent Workflow Git repository just to "
        "use these instructions. Project-specific rules, real permissions, "
        "and tool contracts remain authoritative. Do not assume this skill "
        "grants tool permissions or overrides a user's explicit restrictions.\n"
    )
    if len(content) > 5000:
        raise ValueError(f"Skill too long: {slug}")
    return content.encode("utf-8")


def _plugin_directory(name: str) -> Path:
    return PLUGIN_ROOT / name


def generated_files() -> dict[Path, bytes]:
    files: dict[Path, bytes] = {}
    marketplace = {
        "name": LEGACY_PLUGIN,
        "interface": {"displayName": MARKETPLACE_TITLE},
        "plugins": [],
    }
    for section, info in GROUPS.items():
        plugin_id = info["id"]
        sources = [(slug, path, desc) for gid, slug, path, desc in SOURCES if gid == plugin_id]
        package = _plugin_directory(plugin_id)
        marketplace["plugins"].append({
            "name": plugin_id,
            "source": {"source": "local", "path": "./" + package.as_posix()},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        })
        interface = {
            "displayName": MARKETPLACE_TITLE + " · " + info["title"],
            "shortDescription": info["short"],
            "longDescription": info["description"] + f" Includes {len(sources)} independent Skills.",
            "developerName": "Arthur Koba",
            "category": "Productivity",
            "capabilities": ["Read"],
        }
        manifest = {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": plugin_id,
            "version": "1.0.0",
            "description": info["description"],
            "author": {"name": "Arthur Koba"},
            "repository": "https://github.com/ArthurKoba/ai-agent-workflow",
            "skills": "./skills/",
            "extensions": {"com.openai": {"interface": interface}},
        }
        files[package / "plugin.json"] = _json(manifest)
        files[package / ".codex-plugin/plugin.json"] = _json({
            "name": plugin_id,
            "version": "1.0.0",
            "description": manifest["description"],
            "skills": "./skills/",
            "interface": interface,
        })
        for slug, source, description in sources:
            folder = package / "skills" / slug
            files[folder / "SKILL.md"] = _skill_file(slug, source, description)
            for name, raw in _closure(source).items():
                files[folder / "references" / name] = raw
    files[Path(".agents/plugins/marketplace.json")] = _json(marketplace)
    return files


def _managed_plugin_names() -> tuple[str, ...]:
    return (LEGACY_PLUGIN, *RETIRED_PLUGINS, *(meta["id"] for meta in GROUPS.values()))


def _current_files() -> set[Path]:
    result: set[Path] = set()
    for name in _managed_plugin_names():
        output = ROOT / _plugin_directory(name)
        if output.is_symlink():
            raise ValueError(f"Symlink managed plugin directory: {output}")
        if not output.is_dir():
            continue
        for file in output.rglob("*"):
            if file.is_symlink():
                raise ValueError(f"Symlink in managed plugin: {file}")
            if file.is_file():
                result.add(file.relative_to(ROOT))
    if MANIFEST.is_file():
        result.add(MANIFEST.relative_to(ROOT))
    return result


def update(*, check: bool) -> tuple[int, int]:
    expected = generated_files()
    current = _current_files()
    missing = sorted(
        path for path, content in expected.items()
        if not (ROOT / path).is_file() or (ROOT / path).read_bytes() != content
    )
    stale = sorted(current - expected.keys())
    if check and (missing or stale):
        raise ValueError(f"Marketplace drift: {len(missing)} changed, {len(stale)} stale")
    if not check:
        for path in stale:
            (ROOT / path).unlink()
        # Retire only empty directories within managed packages. In
        # particular, do not clean unrelated plugins or source documents.
        for name in _managed_plugin_names():
            output = ROOT / _plugin_directory(name)
            if output.is_dir():
                directories = sorted(
                    (item for item in output.rglob("*") if item.is_dir()),
                    key=lambda item: len(item.parts),
                    reverse=True,
                )
                for folder in (*directories, output):
                    if not any(folder.iterdir()):
                        folder.rmdir()
        for path in missing:
            file = ROOT / path
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(expected[path])
    return len(missing), len(stale)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed, stale = update(check=args.check)
    print(json.dumps({"plugins": len(GROUPS), "skills": len(SOURCES), "changed": changed,
                      "stale": stale, "check": args.check}))


if __name__ == "__main__":
    main()
