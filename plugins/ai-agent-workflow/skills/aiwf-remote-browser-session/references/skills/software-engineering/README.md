# Software Engineering

Use this skill for implementation, refactoring, backend/application architecture, Python, persistence, observability and framework-specific engineering.

## Startup

- Read repository `AGENTS.md`, current state/tasks and contribution rules.
- Confirm the real active branch/ref before mutation.
- Identify the natural repository owner for the change.
- Load only the modules required by the task.

## Modules

- Clean Architecture / DDD boundaries → `clean-architecture-ddd.md`
- Python engineering → `python.md`
- Python package/public API design → `package-api.md`
- PostgreSQL queries, locking, queues and performance → `postgresql.md`
- observability, tracing, logging and metrics → `observability.md`
- aiogram-dialog design and navigation → `aiogram-dialog.md`
- recurring software-engineering execution failures → `errors.md`

Framework-, language- and database-specific modules are conditional. Do not load them for unrelated work.

## Work

- Prefer small logical changes.
- Do not mix unrelated cleanup with functional changes.
- Reuse existing implementations and contracts.
- Keep generated binaries out of source Git unless repository policy says otherwise.
- Synchronize current-state/coordination documentation in the same iteration when architecture, ownership or gates change.
- Preserve the repository's established language/runtime/package-manager/test policy unless the task explicitly changes it.

## Validation

Track the highest demonstrated level rather than inheriting a prior result:

`SOURCE_CONFIRMED → BUILD_PASS → RUNTIME/HARDWARE_PASS → PRODUCT/UPSTREAM_READY`

Choose the narrowest validation that proves the changed risk. Repository-local acceptance rules override generic defaults.

## Completion

Before claiming completion:

- reread the original requirements;
- check unresolved blockers and contradictions;
- verify the actual source contains the claimed change;
- verify documentation/state was synchronized when required;
- request independent review when the change meets the repository/project review threshold.
