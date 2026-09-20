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
4. If changing the agent system itself, also read `audit/README.md` and `docs/SYSTEM_ARCHITECTURE.md`.
5. If touching tooling/MCP/infrastructure strategy, read `docs/MCP_STRATEGY.md`.

## Routing

- implementation/refactoring → `skills/software-engineering/README.md`
- independent review → `skills/code-review/README.md`
- shell/SSH/UART/PowerShell/WSL/remote execution → `skills/terminal-operations/README.md`
- any task that emits human-operated commands → `skills/terminal-operations/README.md` (mandatory)
- service/deployment/infrastructure operations → `skills/service-engineering/README.md`
- embedded reverse/bring-up → `skills/hardware-reverse/README.md`
- OpenIPC migration/porting/contribution → `skills/openipc-porting/README.md`
- chat/workflow/prompt audit → `skills/workflow-audit/README.md`

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
