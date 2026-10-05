# Standalone Table

Use this subskill when designing, refactoring or reviewing a reusable table shell, entity table wrapper, responsive/mobile rendering or table composition across FSD layers.

## Read with

- `../table-layout.md`
- `../ui-layout.md`
- `../feature-sliced-design.md` when the project uses FSD or the task changes FSD boundaries
- `../feature-sliced-design-examples.md` when placement is ambiguous
- this directory's `rules.md` and `checklist.md`

## Responsibility

The subskill owns the reusable design workflow: separate generic mechanics from entity presentation and scenario composition; design stable slots/overrides; keep server/client table state explicit; avoid duplicating shell behavior across consumers.

It does not define the project's domain DTOs, backend API, design system or package manager.

## Workflow

1. Identify whether the change belongs to generic shell, entity wrapper, feature action, widget/page composition or route state.
2. Reuse an existing table shell before creating another.
3. Place responsibilities at their natural owner; do not solve reuse by creating same-layer cross-imports.
4. Design stable extension points rather than scenario-specific shell forks.
5. Verify loading/empty/error, long content, actions, pagination and mobile behavior.
6. For non-trivial library API behavior, confirm the current framework/library contract from an authoritative source.
7. Finish with `checklist.md`.
