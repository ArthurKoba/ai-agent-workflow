# Project Prompt Template

Template for configuring a Project/workspace. The actual project prompt is injected by the harness.

Repository AGENTS files must not require agents to reread this template.

## Project
Project: <name>
Purpose: <short purpose>

## Authorities
Primary repositories:
- <repo>

Coordination/state authority:
- <repo/path>

Evidence/artifact authority:
- <system/repo>

## Workspace map
On entering a repository, read its `AGENTS.md` completely; if absent, use
`CLAUDE.md`, then `README.md` and relevant contribution/review rules.
Follow its minimal task routing without preloading unrelated roles or skills.
For selected mandatory authorities, follow the Account/Project rules on
complete reading and unavailable sources. Prompt source templates are not
additional runtime prerequisites.

## Primary tool surfaces
Git/repository mutations:
- <primary MCP/connector>

Reverse-analysis:
- <primary tool>

Artifacts/files:
- <primary tool>

HTTP/browser-like requests:
- <primary tool>

Do not switch to alternate mutation surfaces as a workaround unless explicitly allowed.

## Local context
local_context: <REQUIRED | OPTIONAL | NOT_USED>

Source:
- <source>

If REQUIRED local context is unavailable or incomplete, stop actions
that depend on its machine-specific values (local execution, target access,
build/deployment, transport, etc.). Report the missing source once; do not
invent paths, tools or addresses. Independent authorized source reading and
analysis may continue. If this Project imposes a stricter gate, state it
explicitly here. Degraded environment-dependent action requires the
explicit task-specific exception allowed by governing rules, not assumed
permission from a general work request.

## Roles
Default implementation role:
- Implementer

Independent review required for:
- architecture/ownership changes;
- multi-repository changes;
- hardware/boot/storage critical changes;
- destructive/recovery-sensitive work;
- infrastructure/security/permission changes;
- release/upstream-ready changes.

## Validation ownership
Authoritative local build surface:
- <owner/CI/runner>

Hardware acceptance surface:
- <owner/device/lab>

Do not claim these gates without actual evidence.
