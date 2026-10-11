#!/usr/bin/env python3
"""Deterministically package the complete canonical reverse-analysis skill."""
from __future__ import annotations

import argparse
import hashlib
import io
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = "reverse-analysis"
SOURCE = ROOT / "skills" / "reverse-analysis.md"
REPORTING = ROOT / "docs" / "REPORTING_PROTOCOL.md"
LICENSE = ROOT / "LICENSE"
DEFAULT_OUTPUT = ROOT / "dist" / "agent-skills" / (NAME + ".zip")

DESCRIPTION = (
    "Reverse engineer and reconstruct behavior of executable programs, PE/EXE/"
    "DLL/ELF binaries, BIOS/UEFI firmware, drivers, embedded images, and ACPI/WMI. "
    "Use for Ghidra and Analysis MCP workflows: exhaustive decompilation, control/"
    "data-flow tracing, semantic naming, evidence confidence, proofs, persistent "
    "Ghidra projects and scripts, and reverse-engineering progress reports."
)

PRELUDE = """# Native skill activation and continuity

This package is a versioned, self-contained snapshot of the canonical
ArthurKoba/ai-agent-workflow repository file skills/reverse-analysis.md.
The full, unabridged canonical methodology follows below.

- Activation: Apply the entire methodology to reverse-analysis work. A
  remembered excerpt or partial read does not substitute for the source.
  Project-owned target scope, permitted tools and acceptance remain authoritative.
- Before analyzer mutation: Establish the canonical project/program, known-good
  state, evidence and relevant decision gates. Respect the source's mutation rules.
- Continuity: Preserve this skill's name, packaged source SHA-256 from metadata,
  canonical project/program, evidence level, contradictions, validation and next
  decision boundary in the existing durable task checkpoint when needed.
  Do not create a parallel task database.
- Context recovery: After context loss, handoff or material contradiction,
  re-read this complete SKILL.md before any further operation governed by it.
  Context retention is not guaranteed by packaging alone.
- Tools: This package provides instructions only. Ghidra, Analysis MCP, storage,
  GitHub access and permissions must exist independently. Do not invent them.
- Reference mapping: The original source's ../docs/REPORTING_PROTOCOL.md is
  included here as references/REPORTING_PROTOCOL.md. Read that complete file
  for reports, issue checkpoints and publication as required.
- Updates: This ZIP is a snapshot, not a live GitHub link. Rebuild it whenever
  the canonical source changes.

---

"""

ZIP_DATETIME = (1980, 1, 1, 0, 0, 0)


def build() -> tuple[bytes, str, int]:
    source = SOURCE.read_bytes()
    reporting = REPORTING.read_bytes()
    license_text = LICENSE.read_bytes()
    source.decode("utf-8")
    reporting.decode("utf-8")
    source_sha = hashlib.sha256(source).hexdigest()
    header = (
        "---\n"
        "name: reverse-analysis\n"
        'description: "' + DESCRIPTION.replace('"', r'\"') + '"\n'
        "license: MIT\n"
        'compatibility: "Instructions only; Ghidra/Analysis MCP needed for live analyzer actions."\n'
        "metadata:\n"
        '  source-repository: "ArthurKoba/ai-agent-workflow"\n'
        '  source-path: "skills/reverse-analysis.md"\n'
        '  source-sha256: "' + source_sha + '"\n'
        '  packaging-version: "1"\n'
        "---\n\n"
    )
    entries = {
        "reverse-analysis/SKILL.md": header.encode() + PRELUDE.encode() + source,
        "reverse-analysis/references/REPORTING_PROTOCOL.md": reporting,
        "reverse-analysis/LICENSE": license_text,
    }
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(entries.items()):
            info = zipfile.ZipInfo(name, date_time=ZIP_DATETIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return out.getvalue(), source_sha, len(source)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    data, source_sha, source_size = build()
    if args.check:
        if not output.is_file() or output.read_bytes() != data:
            print("Missing or stale installable skill archive: " + str(output), file=sys.stderr)
            return 1
        result = "verified"
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
        result = "built"
    print(result + ": " + str(output) + " (source bytes: " + str(source_size)
          + "; source SHA-256: " + source_sha
          + "; archive SHA-256: " + hashlib.sha256(data).hexdigest() + ")")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
