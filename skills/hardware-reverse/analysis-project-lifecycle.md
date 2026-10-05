# Persistent Analysis Project Lifecycle

Use this module when the analysis backend stores persistent projects/programs but exposes session-local worker/program handles.

## Distinguish project, session and open program

- The persistent **project** owns saved analysis state on durable storage.
- A **project/session handle** is a live backend attachment to that project.
- An **open program** is a session-local handle to one saved program/artifact.

Loss of a session or open-program handle is not evidence that the persistent project or program analysis was deleted.

## Recovery order

When a previously available program disappears or an operation reports that the program is not open:

1. Check project/session status and persistent project contents.
2. If the project exists, reacquire/open the project session.
3. Reopen only the required saved program by its project path.
4. Reuse the saved program; do not re-import the original binary unless the durable project artifact is genuinely absent or unusable.
5. Treat the program as missing/corrupt only after the persistent file is absent or opening it produces a concrete storage/backend diagnostic.

Do not abandon the active behavior route merely because a live handle was released.

## Worker pools

Worker capacity/assignment is infrastructure state, not project identity.

- A project may remain sticky to one worker while its session is active.
- After idle release/restart, the same project may reopen on another eligible worker.
- Never encode worker index as part of durable project identity or evidence.

## Mapping and index state

Persistent bytes, program mapping and analysis/index state are different surfaces.

- A missing action/index entry does not prove the bytes are absent.
- A mapping/base mismatch can make valid bytes appear unavailable at the expected address.
- Before broad re-analysis, inspect the smallest known region and verify the expected mapping/load address.
- When a mapping/index repair is proven, save the corrected program state before relying on it across sessions.

## Known-good state

Before semantic mutation or repair:

- identify the canonical project/program;
- verify the current mapping/load assumptions;
- avoid creating competing mutable copies of the same binary without an explicit experiment boundary;
- preserve recoverable checkpoints when a mutation could invalidate existing references or analysis state.

## Backend defects

Keep session/transport/index defects separate from target-behavior findings. A project-open failure, dropped handle or stale index is tooling evidence, not firmware behavior. Record and fix the owning infrastructure layer when possible without rewriting target conclusions around a transient backend defect.
