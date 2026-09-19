# Software Engineering

## Startup
- Read repository AGENTS, current state/tasks and contribution rules.
- Confirm real active branch/ref before mutation.
- Identify the natural repository owner for the change.

## Work
- Prefer small logical commits.
- Do not mix unrelated cleanup with functional changes.
- Reuse existing implementations/contracts.
- Keep generated binaries out of source Git unless policy says otherwise.
- Synchronize coordination/state in the same iteration when topology/ownership/gates change.

## Validation
Track the highest demonstrated level:
`SOURCE_CONFIRMED → BUILD_PASS → HARDWARE_PASS → PRODUCT/UPSTREAM_READY`

## Completion
Before DONE:
- reread original requirements;
- check unresolved blockers;
- verify actual source contains the claimed change;
- request independent review when required.
