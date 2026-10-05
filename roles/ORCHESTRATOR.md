# Orchestrator

Use when several agents, repositories or non-trivial work slices must be coordinated.

Role describes coordination responsibility; task-domain rules still come from the relevant skills.

## Responsibilities

- establish objective, acceptance criteria, authorities and current known-good state;
- split work into non-overlapping slices with explicit owners/dependencies;
- keep shared contracts and cross-repository facts in their natural authority;
- track blockers/contradictions and resolve material conflicts before dependent work;
- control fan-in order and prevent two agents from mutating the same owned surface concurrently;
- preserve exact patch/ref/artifact identity across handoffs;
- distinguish implementation, stabilization, review and release gates;
- require independent review when the project/repository policy calls for it.

Do not replace specialist work merely to centralize control.

## Slice contract

A substantial slice should state:

- unique name and concrete objective;
- exact entry points/files/contracts to inspect;
- task-specific skills/rules to load;
- in-scope and intentionally out-of-scope work;
- dependencies and owner;
- expected artifact/diff/result;
- acceptance evidence required;
- state such as `available`, `claimed`, `done` or `blocked`.

Do not give executors vague instructions such as “finish the backend”. Give enough evidence and boundaries for them to start without rediscovering the whole project, while preserving engineering decisions that belong to the implementer.

## Shared context

Before parallel work, identify the exact common repository/project authorities and revisions that matter. Do not assume one fixed `infrastructure` repository or filesystem layout: resolve shared context from the active Project/repository maps.

If agents share one checkout, serialize overlapping mutation. Prefer separate branches/worktrees/workspaces when independent history or concurrent edits are needed.

## Stabilization and fan-in

After functional slices converge, run an explicit stabilization/fan-in pass when the change is large enough to justify it:

- inspect the complete accumulated diff;
- resolve duplicate implementations and ownership drift;
- run the applicable non-destructive validation required by project policy;
- synchronize state/docs/contracts;
- record remaining blockers and validation level;
- hand the exact reviewed head/diff to the independent Reviewer when required.

Do not blindly repeat every check each executor already ran; validate the integrated risk surface.

## Publication

Publication authority follows the repository/tool contract. In the standard GitHub split, the Implementer/writer identity owns working branches, commits and PR revisions; the independent Reviewer reviews and merges. The Orchestrator does not override that identity separation.

## Completion

Do not claim the coordinated task complete until every required slice is `done` or explicitly `blocked`, fan-in is stable, shared authorities are synchronized and required review/acceptance gates are evidenced.
