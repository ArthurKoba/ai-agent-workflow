# AGENTS.md

Mandatory workspace map for agents working in this repository.

## Important

Do **not** reread `prompts/ACCOUNT_PROMPT.md` or a project prompt as a runtime prerequisite.

Those are source templates for account/project configuration and are assumed to be injected by the harness already.

Read them only when the task is to design, audit or update prompts.

## Startup routing

For substantial technical work, read and apply `docs/BOOTSTRAP_PROTOCOL.md`.
It alone defines mandatory-source selection, model-visible completeness,
bounded recovery and the dependent-work STOP gate. Do not duplicate that
procedure here or treat a successful tool call as proof of complete reading.

Start with this map. Select the role (`roles/README.md` when unclear), the
relevant skill from the routes below, and task-specific authorities. Read each
selected mandatory file fully. `skills/README.md` is a discovery index when
the routes below are insufficient or the skill map itself is being changed;
it does not add a compulsory extra hop for every task. Read the root
`README.md` for repository overview or when changing this workflow library,
not as a second always-on prompt.

For changes to the agent system, read `audit/README.md`,
`audit/CONTEXT_MAINTENANCE.md` and `docs/SYSTEM_ARCHITECTURE.md`. Add
`docs/SKILL_AUTHORING.md` when creating/restructuring skills,
`docs/MCP_STRATEGY.md` when changing MCP/tool strategy, and
`docs/REPORTING_PROTOCOL.md` when preparing governed progress reports.
The account/project prompt *templates* are not runtime prerequisites;
read them only when auditing or changing those templates.

## Routing

Roles (read the selected role file in full):
- implementation → `roles/IMPLEMENTER.md`
- independent review → `roles/REVIEWER.md`
- multi-agent coordination → `roles/ORCHESTRATOR.md`

Task skills:
- implementation/refactoring/backend/Python/PostgreSQL → `skills/software-engineering/README.md`
- frontend/Vue/TypeScript/FSD/UI/tables → `skills/frontend-engineering/README.md`
- project bootstrap / toolchain / lint, types, hooks and CI setup → `skills/project-bootstrap.md`
- Git / Issues / branches / commits / PR-MR / Git-backed coordination → `skills/git-workflow.md`
- independent review → `skills/code-review.md`
- interface/UX design review and acceptance → `skills/interface-design-review.md`
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

## GitHub writer/reviewer identity contract

When both GitHub App identities are available:
- `koba-ai-agent` is the writer/Implementer identity. It may create working branches, commits, issues and pull requests, update its PR branch, and respond to review findings.
- `koba-ai-reviewer` is the independent Reviewer identity. It reads the proposed diff and current authority, submits review state, and is the only identity that merges pull requests into reserved/default branches.
- For PR-governed changes the writer never merges its own PR; the reviewer does not edit its implementation, and requested changes return to the writer.
- Direct push to an unprotected default branch is permitted only when Project policy and actual tool permissions allow it. Tool-reserved branches, required reviews and protected branches use `writer branch -> PR -> reviewer review -> reviewer merge`. Do not bypass tool restrictions through another transport.
- Account aliases are stable selectors; concrete App IDs, installation IDs and credentials remain infrastructure state and do not belong in this repository.

## Rules

- Keep this repository project-neutral.
- Do not store project IPs, hostnames, GPIO maps, active SHAs or machine-specific paths.
- Do not store credentials/tokens/private keys.
- Put task-specific rules in skills, not account prompt.
- Put environment values in local context, not universal prompts.
- Prefer editing an existing rule over adding a duplicate.
- Significant changes require an independent Reviewer pass.
- Generalize a lesson here only when it is reusable beyond one project.

## Depth

Preferred hierarchy:

`account → project → skill`

A skill may contain a small internal map, but avoid recursive prompt trees.
