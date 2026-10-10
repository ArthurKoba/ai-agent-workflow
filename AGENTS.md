# AGENTS.md

Mandatory workspace map for agents working in this repository.

## Important

Do **not** reread `prompts/ACCOUNT_PROMPT.md` or a project prompt as a runtime prerequisite.

Those are source templates for account/project configuration and are assumed to be injected by the harness already.

Read them only when the task is to design, audit or update prompts.

## Hard startup gate

For substantial technical work, follow `docs/BOOTSTRAP_PROTOCOL.md` before the first implementation/mutation/human-operated command block. Every **selected mandatory document** (the project map, this workflow's bootstrap/role/skills and any task-triggered authority) must be retrieved and **read completely**, not merely opened, summarized or partially displayed. A truncated or unavailable source is **not loaded**. Use the configured GitHub MCP for this library; if required context remains incomplete, **STOP and request explicit task-scoped user approval** before proceeding without it. Never assume approval from the original task request. The detailed single owner of this gate is `docs/BOOTSTRAP_PROTOCOL.md`.

## Start

1. Read `README.md`.
2. Identify your role from `roles/README.md`.
3. Select the task module from `skills/README.md`.
4. If changing the agent system itself, also read `audit/README.md`, `audit/CONTEXT_MAINTENANCE.md` and `docs/SYSTEM_ARCHITECTURE.md`.
5. If creating/restructuring skills, also read `docs/SKILL_AUTHORING.md`.
6. If touching tooling/MCP/infrastructure strategy, read `docs/MCP_STRATEGY.md`.
7. For long-running work or any user-facing progress/report request, read `docs/REPORTING_PROTOCOL.md`.

## Routing

- implementation/refactoring/backend/Python/PostgreSQL → `skills/software-engineering/README.md`
- frontend/Vue/TypeScript/FSD/UI/tables → `skills/frontend-engineering/README.md`
- project bootstrap / toolchain / lint, types, hooks and CI setup → `skills/project-bootstrap.md`
- Git commit/message work → `skills/git-workflow.md`
- independent review → `skills/code-review.md`
- shell/SSH/UART/PowerShell/WSL/remote execution → `skills/terminal-operations.md`
- any task that emits human-operated commands → `skills/terminal-operations.md` (mandatory)
- service/deployment/infrastructure operations → `skills/service-engineering/README.md`
- remote browser sessions / Chrome tabs / DevTools / extension permissions → `skills/remote-browser-session.md`
- reusable service deployment examples/presets → `examples/services/README.md` after loading the relevant service-engineering skill
- program analysis (EXE, BIOS/UEFI, firmware, libraries, drivers), behavior tracing and Ghidra/Analysis → `skills/reverse-analysis.md`
- OpenIPC migration/porting/contribution → `skills/openipc-porting.md`
- context-efficient documentation/bootstrap/multi-agent workflow design → `skills/context-engineering.md`
- chat/workflow/prompt audit → `skills/workflow-audit.md`

## GitHub writer/reviewer identity contract

When both GitHub App identities are available:
- `koba-ai-agent` is the writer/Implementer identity. It may create working branches, commits, issues and pull requests, update its PR branch, and respond to review findings.
- `koba-ai-reviewer` is the independent Reviewer identity. It reads the proposed diff and current authority, submits review state, and is the only identity that merges pull requests into reserved/default branches.
- The writer must not merge its own pull request. The reviewer must not edit the implementation under review; requested changes return to the writer for a new revision.
- Reserved/default branches such as `main`/`master` are not direct-mutation targets for the writer. Use `writer branch -> PR -> reviewer review -> reviewer merge` unless a repository explicitly has no review surface or the tool authority says otherwise.
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
