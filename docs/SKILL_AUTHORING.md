# Skill Authoring

Use this document when creating, splitting, merging or reviewing task skills in this repository.

## Purpose

A skill is a reusable module for a class of tasks. It describes when to load specialized context, what decision process to follow, which adjacent modules are required and how to validate the result.

A skill must not duplicate account-level behavior, Project authority, repository-local state or another skill's owned rules.

## Placement

- Universal behavior belongs in the account prompt only when it applies across essentially all work.
- Project authorities/tool selection belong in the Project prompt.
- Repository-specific state, contracts and exceptions belong in that repository.
- Reusable task-domain behavior belongs under `skills/`.
- Responsibility/permissions belong under `roles/`.
- Recurring workflow failures and generalized lessons belong under `audit/`.

## Structure

Every top-level skill has a directory with `README.md` as its entry point:

```text
skills/<skill-name>/
  README.md
  <optional-module>.md
  <optional-subskill>/README.md
```

`README.md` is a router: purpose, triggers, boundaries, required reading and completion contract. Large rules/examples belong in conditional modules so agents do not load unrelated context.

Use subskills only when a topic has its own trigger and workflow. Prefer a small internal map over another hierarchy of global prompts.

## Rule ownership

One meaning should have one owner. A skill may link to another owner but should not copy its rule text.

Examples:
- commit-message format → `skills/git-workflow/`;
- Python/package/PostgreSQL engineering → `skills/software-engineering/`;
- FSD/UI/table engineering → `skills/frontend-engineering/`;
- independent review responsibilities → `roles/REVIEWER.md`;
- workflow-error aggregation → `audit/`.

## Quality rules

- Every instruction should change an agent decision or prevent a concrete failure.
- Prefer conditional wording when a rule depends on language/framework/tooling.
- Do not freeze project-specific versions, paths, commands or providers into a universal skill.
- Preserve local/repository authority: a universal module supplies a reusable pattern, not an excuse to override a project's explicit contract.
- Avoid vague advice and duplicated checklists.
- Examples should clarify a decision boundary, not become a tutorial.

## Updating the map

After adding/removing/renaming a top-level skill, update `skills/README.md` and root `AGENTS.md` when routing changes.

Before completion, verify links, ownership, project-neutrality and that the skill can be loaded without requiring unrelated modules.
