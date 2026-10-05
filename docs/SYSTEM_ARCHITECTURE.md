# System Architecture

## Three instruction layers

### 0. Account
Always active. Universal behavior only.

### 1. Project
Always active inside one project. Authorities, primary tools, local-context policy and validation ownership.

### 2. Skill
Loaded only when required. Terminal, software, service, reverse, review, audit, etc.

## AGENTS
AGENTS is a workspace navigation map. It answers:
- where am I;
- what is authoritative;
- what role/skill applies;
- where state/tasks live;
- where findings must be written.

It does not duplicate account/project prompts.

## Roles are orthogonal
Role = responsibility. Skill = task domain.

Implementer and Reviewer can use the same project + skill while having different permissions and obligations.

## State is not prompt
Dynamic facts such as active SHA, PID, IP, boot mode and current artifact belong in state/local context.

## Infrastructure is not prompt
MCP servers, Apps, runners, artifact stores, presets and credentials belong in infrastructure authority. Project prompt only selects which infrastructure to use.

## Skill internals
A skill may route to conditional modules or a focused subskill when the task domain is large. Those modules are not extra global instruction layers: they are loaded only through the selected task skill.

Examples:
- `software-engineering` routes to Python, DDD, PostgreSQL and observability only when relevant;
- `frontend-engineering` routes to Vue/TypeScript, FSD, UI and table modules;
- `knowledge-base` may route to optional Obsidian graph maintenance.

Avoid mandatory chains where an agent must load unrelated modules before acting.

## Progressive context disclosure

Context size is an architectural constraint. Repository maps and skill routers should minimize mandatory startup context and route the agent to additional authorities only when the current task crosses their boundary.

Documentation should preserve durable contracts, ownership and navigation; source code remains the authority for ordinary implementation detail. Avoid giant mandatory current-state documents that mirror the codebase.

For the full operating model, use `../skills/context-engineering/README.md`.

## Maximum depth
Prefer `account → project → skill`.

If an agent must traverse many nested policy documents before acting, simplify the map.
