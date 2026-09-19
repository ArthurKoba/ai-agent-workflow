# Prompt Sources

These files are **configuration sources for humans/harnesses**, not documents ordinary agents should reread on startup.

## Account

`ACCOUNT_PROMPT.md`

Copy/adapt into account-level instructions. It is always active and must remain project-neutral.

## Project

`PROJECT_PROMPT_TEMPLATE.md`

Use as the skeleton for a Project/workspace prompt. The resulting project prompt is injected only inside that Project.

## Task-specific behavior

Task-specific instructions are not another always-on prompt.

They live under `../skills/` and are selected through repository `AGENTS.md`.

Runtime hierarchy:

`account → project → skill`
