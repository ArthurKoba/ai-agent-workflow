# Bootstrap Protocol

Purpose: make workflow loading observable and resistant to prompt/context drift.

This protocol applies to substantial technical work.

## Hard startup gate

Before the first implementation/mutation/human-operated command block:

1. identify the active Project/repository/workspace;
2. read the local repository map:
   - `AGENTS.md` if present;
   - otherwise `CLAUDE.md`;
   - otherwise `README.md` + contribution/review docs;
3. read the universal workflow library root `AGENTS.md` / `README.md` when available;
4. select and read the relevant task skill(s);
5. identify the active role;
6. read current state/tasks/authority documents required by the repository map;
7. establish the current Task Context.

Do not proceed past this gate by merely claiming that the files were read.

A document counts as loaded only if:
- it was actually retrieved/read through an available tool in the current task context; or
- its content is explicitly injected into the current context by the harness.

If the required map/skill cannot be accessed, state that once and continue only where the missing context cannot affect correctness.

## Task Context

Before substantial work, know at least:

- objective;
- acceptance criteria;
- active repository/workspace;
- active branch/ref when relevant;
- current known-good state;
- active role;
- loaded task skill(s);
- current patch/delta/artifact identity;
- latest observed result;
- next real decision boundary;
- blockers/contradictions.

This context may live in repository state, a task file, a durable artifact, or structured tool state.

Do not rely on chat memory alone for long or multi-turn technical work.

## Patch / delta continuity

An unfinished patch, generated file set, or important diff must not exist only as prose in chat.

Before a context switch, long investigation, agent handoff, or risky branch change, persist enough information to recover it:
- repository + branch/ref;
- affected files;
- diff/commit/patch artifact ID or exact locator;
- applied/not-applied state;
- validation already performed;
- remaining validation.

If the patch identity cannot be recovered, stop and reconstruct it from repository/artifact evidence before stacking new edits.

## Human-operated commands

If the task will emit commands for a human to run, `skills/terminal-operations/README.md` is mandatory.

Do not emit the first command block until the terminal skill is loaded or its rules are already injected in current context.

## Re-bootstrap triggers

Repeat only the relevant bootstrap subset when:
- repository/workspace changes;
- branch/state authority changes materially;
- a new task domain is entered;
- context/handoff/agent changes;
- a long task resumes after state uncertainty;
- the user reports that command/routing rules were violated.

Do not reread everything mechanically after every tool call.

## User-visible startup signal

For substantial work, a short startup update may state:
- repository/workspace;
- selected skill/role;
- current decision boundary.

Do not dump the whole checklist or pretend verification that did not happen.


## Pre-send compliance

Loading the correct map/skill is necessary but not sufficient.

Before emitting an action governed by an active skill, perform a final compliance check against that skill's hard constraints.

Do not let a secondary response objective such as completeness, compactness, end-to-end planning, or convenience override an explicit STOP / MUST / decision-boundary rule.

If a draft response conflicts with an active hard constraint, the hard constraint wins and the draft must be rewritten before sending.
