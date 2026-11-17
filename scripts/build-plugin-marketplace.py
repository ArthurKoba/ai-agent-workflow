#!/usr/bin/env python3
"""Produce self-contained AI Agent Workflow plugin Skills from the authoritative library."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
from collections import deque
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = Path("plugins/ai-agent-workflow")
OUT = ROOT / PLUGIN
MANIFEST = ROOT / ".agents/plugins/marketplace.json"
ALLOWED = frozenset({"skills", "docs", "audit", "context", "playbook", "examples"})
CURATED_DESCRIPTIONS = {
    'software-engineering': 'Implementation, backend, Python, architecture, persistence and observability',
    'frontend-engineering': 'Frontend architecture, Vue, TypeScript, layouts, and accessible UI',
    'software-testing': 'Design, select, and verify tests across product boundaries',
    'project-bootstrap': 'Project setup, toolchains, quality gates, hooks and CI',
    'skill-authoring': 'Create, review, refactor and validate reusable agent skills',
    'git-workflow': 'Git, branches, commits, review, publication and issues',
    'orchestration': 'Multi-agent coordination, PDCA, delegation and handoffs',
    'code-review': 'Independent technical reviews, evidence and acceptance',
    'interface-design-review': 'Interface design review, accessibility and user journeys',
    'scientific-visualization': 'Technical diagrams, scientific figures and measured plots',
    'terminal-operations': 'Shell, PowerShell, SSH, serial and terminal operations',
    'services-deployment': 'Services, Docker Compose, Coolify, environments and deployments',
    'remote-browser-session': 'Browser sessions, Chromium debugging and remote automation',
    'reverse-analysis': 'Reverse engineering, firmware, binaries, tracing and native analysis',
    'openipc-porting': 'OpenIPC firmware porting and contribution workflows',
    'context-engineering': 'Agent context management, source maps and progressive disclosure',
    'workflow-audit': 'Agent workflow and prompt audits',
    'domain-acquisition': 'Domain registration, transfers, pricing and continuity',
}

LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")
CODE_PATH = re.compile(r"`([^`\s]+\.md(?:#[^`\s]*)?)`")



def _discover_sources() -> tuple[tuple[str, str, str], ...]:
    """Make the authoritative task map determine each installable Skill."""
    found: list[tuple[str, str, str]] = []
    for line in (ROOT / "skills/README.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith("- ") or "→" not in line:
            continue
        heading, route = line.split("→", 1)
        pattern = chr(96) + r"([^" + chr(96) + r"]+\.md)" + chr(96)
        match = re.search(pattern, route)
        if match is None:
            raise ValueError(f"Unroutable Skill map entry: {line}")
        path = "skills/" + match.group(1)
        entry = Path(path)
        slug = entry.parent.name if entry.name == "README.md" else entry.stem
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError(f"Invalid Skill identifier: {slug}")
        description = CURATED_DESCRIPTIONS.get(slug, heading[2:].strip())
        found.append((slug, path, description))
    if not found or len({slug for slug, _, _ in found}) != len(found):
        raise ValueError("Empty or ambiguous Skill map")
    if len({path for _, path, _ in found}) != len(found):
        raise ValueError("Duplicate Skill source in map")
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
        f"name: aiwf-{slug}\n"
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


def generated_files() -> dict[Path, bytes]:
    files: dict[Path, bytes] = {}
    marketplace = {
        "name": "ai-agent-workflow",
        "interface": {"displayName": "AI Agent Workflow"},
        "plugins": [{
            "name": "ai-agent-workflow",
            "source": {"source": "local", "path": "./plugins/ai-agent-workflow"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        }],
    }
    interface = {
        "displayName": "AI Agent Workflow",
        "shortDescription": "Reusable agent workflows for engineering tasks",
        "longDescription": "A self-contained collection of 18 scoped Skills with locally bundled reference modules.",
        "developerName": "AI Agent Workflow",
        "category": "Productivity",
        "capabilities": ["Read"],
    }
    manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": "ai-agent-workflow",
        "version": "1.0.0",
        "description": "Task-specific engineering, development, testing, Git, and operations skills",
        "author": {"name": "AI Agent Workflow"},
        "repository": "https://github.com/ArthurKoba/ai-agent-workflow",
        "skills": "./skills/",
        "extensions": {"com.openai": {"interface": interface}},
    }
    files[Path(".agents/plugins/marketplace.json")] = _json(marketplace)
    files[PLUGIN / "plugin.json"] = _json(manifest)
    files[PLUGIN / ".codex-plugin/plugin.json"] = _json({
        "name": "ai-agent-workflow",
        "version": "1.0.0",
        "description": manifest["description"],
        "skills": "./skills/",
        "interface": interface,
    })
    for slug, source, description in SOURCES:
        folder = PLUGIN / "skills" / ("aiwf-" + slug)
        files[folder / "SKILL.md"] = _skill_file(slug, source, description)
        for name, raw in _closure(source).items():
            files[folder / "references" / name] = raw
    return files


def _current_files() -> set[Path]:
    if OUT.is_symlink():
        raise ValueError("Symlink plugin directory is forbidden")
    result: set[Path] = set()
    if OUT.is_dir():
        for file in OUT.rglob("*"):
            if file.is_symlink():
                raise ValueError(f"Symlink in generated plugin: {file}")
            if file.is_file():
                result.add(file.relative_to(ROOT))
    if MANIFEST.is_file():
        result.add(MANIFEST.relative_to(ROOT))
    return result


def update(*, check: bool) -> tuple[int, int]:
    expected = generated_files()
    current = _current_files()
    missing = sorted(path for path, content in expected.items()
                     if not (ROOT / path).is_file() or (ROOT / path).read_bytes() != content)
    stale = sorted(current - expected.keys())
    if check and (missing or stale):
        raise ValueError(f"Marketplace drift: {len(missing)} changed, {len(stale)} stale")
    if not check:
        for path in stale:
            (ROOT / path).unlink()
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
    print(json.dumps({"skills": len(SOURCES), "changed": changed,
                      "stale": stale, "check": args.check}))


if __name__ == "__main__":
    main()
