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

A **standalone skill is a single named Markdown file**:

```text
skills/<skill-name>.md
```

Do not require a directory or `README.md` for a self-contained skill.
The file itself describes triggers, terminology, process, tool workflows,
validation and completion.

Only group a genuinely multi-file skill when it contains distinct,
independently useful documents or assets. In that case use:

```text
skills/<skill-name>/
  README.md
  <optional-module>.md
```

The folder's `README.md` then routes to its independent modules. Do not
split one coherent analysis/recovery process into subordinate documents,
and do not create a folder merely to hold a single README. The central
`skills/README.md` map must link directly to whichever entrypoint exists.

## Migration and structure gate

- A folder containing only `README.md` is a standalone skill in the wrong
  shape: move it to `skills/<name>.md`, not another nested folder.
- A subdirectory within a modular skill is justified only when it contains
  multiple independently useful modules. A router, repetitive rules and a
  checklist for **one** workflow should normally be one adjacent file.
- On any move, update all inbound routes (root and domain maps, role/project
  templates and neighboring skills), and fix relative paths **inside** the
  moved file. Search for the old path before requesting review.
- Keep the migrated content and proof; do not resurrect superseded modules
  merely to preserve old commit history. If behavior already exists under a
  newer canonical owner, record the overlap and omit the duplicate.

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
