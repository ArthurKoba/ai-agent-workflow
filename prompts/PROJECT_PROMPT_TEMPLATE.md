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
Whenever entering a repository, read its `AGENTS.md` **completely**.
Read every selected mandatory workflow/role/skill/contract document completely
through its authoritative connector, as required by the workflow Bootstrap
Protocol. A snippet or truncated tool response is not successful loading.

AGENTS is a router, not a replacement for this project prompt.

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

If REQUIRED context is missing, inaccessible or incompletely read, **STOP**
before substantial work. Report the missing source/connector and seek an
explicit user decision for this particular task: restore access and reread it,
or authorize a degraded start without the named context. Do not treat an
earlier general work request as permission to ignore the missing authority.

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
