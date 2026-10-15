# Prompt Sources

Account and Project prompts are configuration sources for humans/harnesses.
They are injected into the relevant account/Project; ordinary agents must
not reread these files as a startup prerequisite.

## Accounts

- [account](accounts/account.md) — current project-neutral Account Prompt.

Additional named account variants belong under `accounts/`, not in the root.

## Projects

- [infrastructure](projects/infrastructure.md) — personal AI/development infrastructure.
- [reverse-engineering](projects/reverse-engineering.md) — broad firmware, embedded and program analysis.
- [reverse-analysis](projects/reverse-analysis.md) — standalone Analyzer-focused Project Prompt.
- [_template](projects/_template.md) — skeleton for new Project prompts; not an active Project.

Add each new Project with its own name under `projects/`, not under
a second top-level `projects/` directory. A source file does not prove
its prompt is installed in a ChatGPT Project.

## Skills

Task-specific instructions remain in `../skills/`; no additional prompt layer
is introduced.

Runtime hierarchy: `account → project → skill`.
