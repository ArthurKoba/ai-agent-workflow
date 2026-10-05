# AGENTS.md

Mandatory workspace map for agents working in this repository.

## Important

Do **not** reread `prompts/ACCOUNT_PROMPT.md` or a project prompt as a runtime prerequisite.

Those are source templates for account/project configuration and are assumed to be injected by the harness already.

Read them only when the task is to design, audit or update prompts.

## Hard startup gate

For substantial technical work, follow `docs/BOOTSTRAP_PROTOCOL.md` before the first implementation/mutation/human-operated command block. Do not claim a map/skill was read unless it was actually retrieved or injected into the current context.

## Start

1. Read `README.md`.
2. Identify your role from `roles/README.md`.
3. Select the task module from `skills/README.md`.
4. If changing the agent system itself, also read `audit/README.md`, `audit/CONTEXT_MAINTENANCE.md` and `docs/SYSTEM_ARCHITECTURE.md`.
5. If creating/restructuring skills, also read `docs/SKILL_AUTHORING.md`.
6. If touching tooling/MCP/infrastructure strategy, read `docs/MCP_STRATEGY.md`.

## Routing

- implementation/refactoring/backend/Python/PostgreSQL → `skills/software-engineering/README.md`
- frontend/Vue/TypeScript/FSD/UI/tables → `skills/frontend-engineering/README.md`
- Git commit/message work → `skills/git-workflow/README.md`
- persistent knowledge-base/wiki/Obsidian work → `skills/knowledge-base/README.md`
- independent review → `skills/code-review/README.md`
- shell/SSH/UART/PowerShell/WSL/remote execution → `skills/terminal-operations/README.md`
- any task that emits human-operated commands → `skills/terminal-operations/README.md` (mandatory)
- service/deployment/infrastructure operations → `skills/service-engineering/README.md`
- embedded reverse/bring-up → `skills/hardware-reverse/README.md`
- OpenIPC migration/porting/contribution → `skills/openipc-porting/README.md`
- context-efficient documentation/bootstrap/multi-agent workflow design → `skills/context-engineering/README.md`
- chat/workflow/prompt audit → `skills/workflow-audit/README.md`

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
