# AGENTS.md

Mandatory workspace map for agents working in this repository.

## Important

Do **not** reread `prompts/accounts/universal.md` or a project prompt as a runtime prerequisite.

Those are source templates for account/project configuration and are assumed to be injected by the harness already.

Read them only when the task is to design, audit or update prompts.

## Start

Use this map and the injected Account/Project prompts. Select only the
relevant role and task skill(s) below; load further contracts when the task
requires them. `roles/README.md` and `skills/README.md` are optional
discovery maps, not additional mandatory startup steps.

Read selected mandatory sources completely through the Project's designated
authority. If a required source is unavailable or incomplete, do not perform
actions that depend on it; follow the injected Account/Project rules.
Do not reread account/project prompt templates merely to start work.

For workflow-library changes, consult the owning audit or architecture
source when relevant. For every skill creation, edit, split, merge or review,
load `skills/skill-authoring.md` first. For governed progress reports, use
`docs/REPORTING_PROTOCOL.md`. Avoid loading the whole library.

## Routing

Playbooks (decision/checklist guides, not additional runtime prompt layers):
- new service / repository setup → `playbook/new-project.md` (load when planning a new project)


Roles (read the selected role file in full):
- implementation → `roles/IMPLEMENTER.md`
- independent review → `roles/REVIEWER.md`
- multi-agent coordination → `roles/ORCHESTRATOR.md`

Task skills:
- implementation/refactoring/backend/Python/PostgreSQL → `skills/software-engineering/README.md`
- frontend/Vue/TypeScript/FSD/UI/tables → `skills/frontend-engineering/README.md`
- project bootstrap / toolchain / lint, types, hooks and CI setup → `skills/project-bootstrap.md`
- writing/editing/splitting/reviewing skills → `skills/skill-authoring.md` (mandatory)
- Git / Issues / branches / commits / PR-MR / Git-backed coordination → `skills/git-workflow.md`
- independent review → `skills/code-review.md`
- interface/UX design review and acceptance → `skills/interface-design-review.md`
- scientific flowcharts, Draw.io/SVG diagrams, measured/calculated plots and spreadsheet-backed charts → `skills/scientific-visualization.md`
- shell/SSH/UART/PowerShell/WSL/remote execution → `skills/terminal-operations.md`
- any task that emits human-operated commands → `skills/terminal-operations.md` (mandatory)
- service/deployment/infrastructure operations → `skills/service-engineering/README.md`
- remote browser sessions / Chrome tabs / DevTools / extension permissions → `skills/remote-browser-session.md`
- reusable service deployment examples/presets → `examples/services/README.md` after loading the relevant service-engineering skill
- program analysis (EXE, BIOS/UEFI, firmware, libraries, drivers), behavior tracing and Ghidra/Analysis → `skills/reverse-analysis.md`
- OpenIPC migration/porting/contribution → `skills/openipc-porting.md`
- context-efficient documentation/bootstrap/multi-agent workflow design → `skills/context-engineering.md`
- chat/workflow/prompt audit → `skills/workflow-audit.md`
- registrar/domain procurement, long-term cost, transfers and DNS continuity → `skills/domain-acquisition.md`

## Publication policy — AI Agent Workflow

**Owner decision, 2026-10-22:** publish completed and locally verified changes
**directly to this repository's `main` without mandatory pull requests or
pre-merge independent review**. Direct publication is the default for every
task in **AI Agent Workflow**, including skill and agent-rule updates.

- The Implementer/writer (for GitHub Apps: `koba-ai-agent`) checks the current
  `main` HEAD and effective permissions, validates the full change, and
  publishes with a **normal fast-forward push or one atomic GitHub commit**.
  Never force-update `main`, silently overwrite concurrent changes, or skip
  hooks, locally available checks and required GitHub protections.
- A separate worktree/branch may still be used for isolated drafting and
  testing; it is **not** a reason to open a PR before directly incorporating
  its verified commit into `main`.
- `koba-ai-reviewer` may perform requested or follow-up independent review,
  but reviewer approval and PR creation are **not publication prerequisites**
  in this repository.
- Open a PR only if **the owner explicitly requests one** or actual branch
  protection/permissions require it. If direct publication is technically
  prohibited, report the blocker and follow the permitted process; do not
  evade protections through another transport.
- These rules govern **this repository**, not other Projects with their own
  Git or reviewer policies. Account aliases are stable selectors; concrete
  App IDs, credentials and tokens are not repository documentation.

## Rules

- Keep this repository project-neutral.
- Do not store project IPs, hostnames, GPIO maps, active SHAs or machine-specific paths.
- Do not store credentials/tokens/private keys.
- Put task-specific rules in skills, not account prompt.
- Put environment values in local context, not universal prompts.
- Prefer editing an existing rule over adding a duplicate.
- Significant changes require completed local verification and a traceable commit; independent review is optional or separately requested, never a required pre-publication step in this repository.
- Generalize a lesson here only when it is reusable beyond one project.

## Depth

Preferred hierarchy:

`account → project → skill`

A skill may contain a small internal map, but avoid recursive prompt trees.
