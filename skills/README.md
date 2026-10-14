# Skill Map

Load only the module matching the current task.

- software implementation/refactoring/backend/Python/PostgreSQL → `software-engineering/README.md`
- frontend/Vue/TypeScript/FSD/UI/tables → `frontend-engineering/README.md`
- project/environment bootstrap, Bun/uv, strict quality gates, hooks → `project-bootstrap.md`
- Git commits and commit-message discipline → `git-workflow.md`
- independent review → `code-review.md`
- UI/UX design review and browser acceptance → `interface-design-review.md`
- shell/PowerShell/WSL/SSH/UART/bootloader → `terminal-operations.md`
- deployment/services/infrastructure operations → `service-engineering/README.md`
- remote browser sessions / Chrome tabs / DevTools / extension permissions → `remote-browser-session.md`
- program behavior analysis, reconstruction and Ghidra/Analysis scripting (EXE, BIOS/UEFI, firmware, drivers, libraries) → `reverse-analysis.md`
- OpenIPC migration/porting/contribution → `openipc-porting.md`
- context-efficient documentation/bootstrap/multi-agent workflow design → `context-engineering.md`
- workflow/chat/prompt audit → `workflow-audit.md`
- domain purchase/transfer/renewal cost and continuity → `domain-acquisition.md`

Skills may reference another skill when a task genuinely crosses domains. Avoid loading the full library by default.


## ChatGPT skill editor mapping

These entries map repository skills to the three **separate fields** in the
ChatGPT skill editor: **Name**, **Description**, and **Instructions**. The Markdown
source named by `instructions_source` is the **entire text to paste** into the
Instructions field; do not prepend this metadata, truncate the source, or
maintain a second copy of the skill. The source file remains canonical.

Each new editor mapping belongs in this section with the same four keys:
`id` (stable repository identifier), `name` (editor title), `description`
(editor activation text), and `instructions_source` (repository-root-relative
path to the canonical Markdown). Do not add placeholder entries for skills
whose editor metadata has not been reviewed.
For ChatGPT, `name` must use lowercase ASCII letters, digits and hyphens
(no spaces or uppercase characters); e.g. `reverse-analysis`.

### Reverse Analysis

```yaml
id: reverse-analysis
name: reverse-analysis
description: >-
  Reverse engineer executable programs and firmware (EXE/PE/ELF, DLLs,
  BIOS/UEFI, ACPI/WMI, drivers, libraries and embedded binaries). Use for
  Ghidra/Analysis MCP investigations, complete decompilation, control/data-flow
  tracing, semantic and behavior recovery, evidence confidence and proof,
  persistent analysis projects, scripts and reverse-engineering reports.
instructions_source: skills/reverse-analysis.md
```

Copy the **Name** and **Description** above into the corresponding editor
fields, and paste the complete contents of
[`reverse-analysis.md`](reverse-analysis.md) into **Instructions** unchanged.
For reports, the original skill additionally routes to
[`docs/REPORTING_PROTOCOL.md`](../docs/REPORTING_PROTOCOL.md); the editor
does not automatically resolve this relative reference, so make that document
available through the existing repository connection when its rules apply.

This map does not create a native installation or automatically synchronize
the ChatGPT editor with GitHub. Updating an installed skill requires replacing
the editor's Instructions text from the current canonical file.
