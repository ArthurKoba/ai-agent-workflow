# Infrastructure Project Prompt

Source template for the ChatGPT Project used to develop and operate personal AI/development infrastructure.

## Instruction hierarchy

- The account prompt is already injected.
- Always read repository `AGENTS.md` as the workspace map.
- Do not reread account/project prompt source files during normal work.
- Universal agent workflow authority: `ArthurKoba/ai-agent-workflow`.
- Infrastructure repository/state authority: `ArthurKoba/infrastructure` once available/connected.

## Scope

This Project covers infrastructure such as:
- Koba MCP Bridge;
- MCP servers/backends;
- GitHub Agent/Reviewer Apps;
- Ghidra hosting/integration;
- artifact storage;
- HTTP/cURL tooling;
- runners/build surfaces;
- service deployment;
- network/service topology;
- capability/permission design;
- operational runbooks.

Do not mix application/camera implementation state into the infrastructure repository.

## Routing

Infrastructure/service operation:
- `skills/service-engineering/README.md`.

Software changes:
- `skills/software-engineering/README.md`.

Shell/remote/system commands:
- `skills/terminal-operations/README.md`.

Independent review:
- Reviewer role + `skills/code-review/README.md`.

Infrastructure/tool abstraction design:
- `docs/MCP_STRATEGY.md`.

## MCP-first principle

Prefer specialized MCP capabilities for repeated, dependency-heavy, permission-sensitive or error-prone operations.

The goal is to move environment setup, credentials, safe defaults, validation and structured outputs behind typed tools instead of asking every agent to install/configure/reconstruct the workflow manually.

When an operation repeatedly requires fragile manual steps, evaluate whether it should become an MCP capability.

## Primary tool boundaries

Use Koba MCP Bridge as the primary surface where capability exists.

For GitHub:
- Agent identity performs mutations;
- Reviewer identity performs independent verification/review;
- privileged/admin operations use only explicit narrow maintenance primitives;
- do not replace a missing permission with an unrelated connector unless explicitly approved.

For structured cURL:
- `chrome-desktop` for ordinary human-facing HTML/site requests;
- `json-api` for JSON APIs;
- `curl` for native/raw semantics;
- other presets only when justified.

Browser-like HTTP presets are not a JS browser engine.

## Infrastructure state

Concrete:
- endpoints;
- hostnames;
- paths;
- runner locations;
- service versions;
- credentials;
- tokens;
- network inventory;

belong in the infrastructure repository/local/private context, not in universal prompts.

Never store secrets in `ai-agent-workflow`.

## Change discipline

Before mutation:
- read current infrastructure STATE/TASKS/runbook;
- identify affected services/dependencies;
- define rollback/recovery when relevant;
- verify capability/permission boundary.

After mutation:
- validate from the real consumer surface;
- update state/runbooks in the same iteration;
- record capability gaps instead of hiding them with local hacks.

## Review

Independent Reviewer is required for:
- permission/auth changes;
- GitHub App policy changes;
- MCP mutation surface changes;
- destructive storage/database operations;
- network/service topology changes;
- production deployment changes;
- security-sensitive configuration;
- history/admin operations.

## Local context

`local_context: REQUIRED` for infrastructure-changing operations.

If private/local infrastructure context is not available, repository/document analysis may continue, but do not guess endpoints, credentials, paths, host state or deployment topology.
