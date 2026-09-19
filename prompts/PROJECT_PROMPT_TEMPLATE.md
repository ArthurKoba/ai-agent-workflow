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
Whenever entering a repository, read its `AGENTS.md`.

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

If REQUIRED context is missing, report degraded-start once and do not guess environment-specific values.

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
