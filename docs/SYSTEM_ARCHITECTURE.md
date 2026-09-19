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

## Maximum depth
Prefer `account → project → skill`.

If an agent must traverse many nested policy documents before acting, simplify the map.
