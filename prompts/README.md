# Prompt Sources

Account and Project prompts are configuration sources for humans/harnesses.
They are injected into the relevant account/Project; ordinary agents must
not reread these files as a startup prerequisite.

## Accounts

- [universal](accounts/universal.md) — current project-neutral Account Prompt.

Additional named account variants belong under `accounts/`, not in the root.

## Projects

- [cobra-infrastructure](projects/cobra-infrastructure.md) — проектный промпт личной инфраструктуры.
- [reverse-analysis](projects/reverse-analysis.md) — Analyzer-focused Project Prompt.

Add each new Project with its own name under `projects/`, not under
a second top-level `projects/` directory. A source file does not prove
its prompt is installed in a ChatGPT Project.

## Skills

Task-specific instructions remain in `../skills/`; no additional prompt layer
is introduced.

Runtime hierarchy: `account → project → skill`.
