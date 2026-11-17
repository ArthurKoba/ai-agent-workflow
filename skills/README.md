# Skill Map

Each heading is an independently installable **Arthur Koba AI Agent Workflow**
package; each list item is an individual Skill inside that package.
Install only the domains relevant to the user. In particular, backend,
architecture, frontend, testing, setup and code review are **one Development
package**, not separate installations.

## Development

- backend implementation, services, APIs and persistence across languages → `backend-engineering.md`
- language-neutral software architecture, DDD and service boundaries → `software-architecture.md`
- project/environment bootstrap, Bun/uv, strict quality gates, hooks → `project-bootstrap.md`
- frontend/Vue/TypeScript/FSD/UI/tables → `frontend-engineering/README.md`
- UI/UX design review and browser acceptance → `interface-design-review.md`
- software test design, run profiles and suite audits → `software-testing/README.md`
- independent review → `code-review.md`

## DevOps & Infrastructure

- Git, Issues, branches, commits, PR/MR and publication → `git-workflow.md`
- shell/PowerShell/WSL/SSH/UART/bootloader → `terminal-operations.md`
- deployment/services/infrastructure operations → `services-deployment/README.md`

## Agent Workflows

- multi-agent coordination, PDCA and direct agent communication → `orchestration/README.md`
- context-efficient documentation/bootstrap/multi-agent workflow design → `context-engineering.md`
- skill creation, editing, splitting, merging and review → `skill-authoring.md` (mandatory)
- workflow/chat/prompt audit → `workflow-audit.md`

## Research & Porting

- program behavior analysis, reconstruction and evidence-driven analysis (EXE, BIOS/UEFI, firmware, drivers, libraries) → `reverse-analysis.md`
- OpenIPC migration/porting/contribution → `openipc-porting.md`
- scientific diagrams, vector SVG, Excel-like charts and reproducible figures → `scientific-visualization.md`

## Domain Management

- domain registration/purchase, renewal, transfer, cost and DNS continuity → `domain-acquisition.md`

## Browser Access

- operator-authorized browser sessions, tabs, DevTools and extension grants → `remote-browser-session.md`

Domain Management and Browser Access are optional, specialized packages;
they are neither prerequisites for software development nor bundled into DevOps.
Skills may reference other source documents conditionally, but no package
requires another package, an external service, Briareus or a Git clone.
