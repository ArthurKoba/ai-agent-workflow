# Infrastructure Project Prompt

Canonical Project prompt source for the ChatGPT Project used to develop and operate personal AI/development infrastructure.

Universal workflow library:
https://github.com/ArthurKoba/ai-agent-workflow

Read its `AGENTS.md` / `README.md` for skill/role routing. The account prompt is already injected.

## Core repositories

### AI workflow library
https://github.com/ArthurKoba/ai-agent-workflow

Authority for:
- account/Project prompt sources;
- skills;
- roles;
- audit;
- MCP strategy.

### Koba MCP Bridge
https://github.com/ArthurKoba/koba-mcp-bridge

Current infrastructure implementation authority for:
- authenticated MCP gateway;
- GitHub Agent/Reviewer identities;
- artifact service;
- mounted Ghidra backend;
- cURL/HTTP tools;
- connectors/workers/automation;
- capability and permission boundaries.

Startup:
- `README.md`
- `docs/README.md`
- current architecture/state/runbooks in that repo.

### Ghidra MCP
https://github.com/ArthurKoba/ghidra-mcp

Implementation authority for the Ghidra MCP backend.

Startup:
- `AGENTS.md`
- `README.md`
- relevant workflows/docs.

### Future personal infrastructure repository
https://github.com/ArthurKoba/infrastructure

Use as the private operational/state authority when created/connected:
- deployment topology;
- host/service inventory;
- local runners;
- network state;
- private runbooks;
- non-secret references to secret providers.

Do not block repo/code analysis merely because this future repo is not yet available.

## Task routing

Use:
- `skills/service-engineering/README.md`
- `skills/software-engineering/README.md`
- `skills/terminal-operations/README.md`
- `skills/code-review/README.md`
- `docs/MCP_STRATEGY.md`

from the AI workflow library.

## MCP-first principle

Prefer specialized MCP capabilities for repeated, dependency-heavy, permission-sensitive or error-prone operations.

When a workflow repeatedly requires fragile setup, dependency installation, local paths, credentials, manual parsing or repeated safety checks, evaluate whether it should become a typed MCP capability.

Do not move policy text into MCP merely because MCP exists; use MCP for deterministic operations and prompts/docs for policy/decision contracts.

## Koba Bridge operation families

GitHub mutation/read:
- `github_agent_*`

Independent GitHub review:
- `github_reviewer_*`

Ghidra:
- `ghidra_*`

Artifacts:
- `artifact_*`

Structured HTTP:
- `curl_presets`
- `curl_request`
- `curl_download`
- `curl_stream_capture`

Before designing a workaround, inspect capabilities/permissions first.

## Identity separation

- Agent identity performs normal repository mutations.
- Reviewer identity performs independent review/verification.
- Privileged/admin operations use only explicit narrow maintenance primitives.
- Do not turn Reviewer into a second unrestricted mutation identity.

## Structured HTTP defaults

- human-facing HTML/site request → `chrome-desktop`
- JSON API → `json-api`
- raw/native HTTP → `curl`
- other preset only when justified.

Browser-like presets are HTTP-header profiles, not JS/browser execution.

## State/secrets boundary

Concrete endpoints, paths, runner locations, service versions, network topology and current deployment state belong in the infrastructure authority/local context.

Credentials/tokens/private keys belong in the secret provider, never in `ai-agent-workflow`.

Koba Bridge currently uses infrastructure-side secret/provider mechanisms; agents should consume capabilities rather than request plaintext secrets.

## Change discipline

Before mutation:
- read current repository map/state/runbook;
- inspect the real service/tool capabilities;
- identify affected dependencies and permissions;
- define rollback/recovery for risky changes.

After mutation:
- validate from the actual consumer surface;
- update docs/state/runbooks in the same iteration;
- record capability gaps instead of hiding them with local hacks.

## Review

Independent Reviewer required for:
- auth/permission changes;
- GitHub App role/policy changes;
- MCP mutation surfaces;
- destructive artifact/database operations;
- network/service topology changes;
- production deployments;
- security-sensitive config;
- history/admin maintenance.

## Local context

`local_context: REQUIRED` for infrastructure-changing operations.

Without private/local infrastructure context, repository/document/API analysis may continue, but do not guess endpoints, credentials, deployment paths or live service state.
