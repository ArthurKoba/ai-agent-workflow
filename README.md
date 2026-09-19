# AI Agent Workflow

Universal operating system for AI engineering agents.

This repository stores reusable agent hierarchy, skills, roles, audit rules and system-evolution knowledge. It is not a project repository and not an infrastructure inventory.

## Runtime hierarchy

There are only three instruction layers.

### Level 0 — Account prompt
Injected by the account/harness for every conversation.

Source template: `prompts/ACCOUNT_PROMPT.md`.

Contains only universal behavior. No project names, MCP products, IPs, paths, GPIO, branch SHAs or task-specific methods.

### Level 1 — Project prompt
Injected by the selected Project/workspace.

Template: `prompts/PROJECT_PROMPT_TEMPLATE.md`.

Defines project authorities, primary tools/MCP, local-context policy and validation ownership.

### Level 2 — Task / skill
Loaded only for the current task.

Map: `skills/README.md`.

Do not create deeper instruction chains unless there is a real need. Three meaningful layers are the intended maximum.

## AGENTS.md is a map, not another prompt

`AGENTS.md` is always read when entering this repository.

It routes the agent to the relevant role, skill, audit or architecture document. It must not require rereading account/project prompts; those are assumed already injected by the harness.

## Repository map

- `prompts/` — account-level and generic Project prompt source templates.
- `projects/` — ready Project prompt sources for major workspaces.
- `skills/` — task-specific modules.
- `roles/` — Implementer / Reviewer / Orchestrator.
- `context/` — local-context contract/templates.
- `docs/` — system architecture and MCP strategy.
- `audit/` — recurring error/best-practice aggregation.
- `history/` — evolution of the agent system.

## Placement rule

A rule belongs at the highest layer that is truly universal, but no higher.

Examples:
- do not guess current state → account;
- use a specific MCP in one project → project;
- shell/UART formatting → terminal skill;
- Ghidra reverse methodology → hardware-reverse skill;
- independent review behavior → role model.

## Infrastructure

Concrete MCP servers, GitHub Apps, HTTP presets, runners, artifact stores, network topology and operational runbooks belong in a separate infrastructure authority.

This repository stores the strategy for using such infrastructure, not its live inventory.

See `docs/MCP_STRATEGY.md`.

## Continuous improvement

See:
- `history/EVOLUTION.md`
- `audit/README.md`
- `audit/ERROR_REGISTRY.md`
- `audit/BEST_PRACTICES.md`
- `audit/PROMPT_CHANGELOG.md`
