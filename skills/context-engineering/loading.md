# Context loading and recovery

## Minimal bootstrap

Default substantial-task startup should be intentionally small:

1. repository `AGENTS.md`;
2. one compact application/project map or task authority selected by it;
3. the task-specific skill/router;
4. the source/contracts directly relevant to the current task.

Do not require an agent to read every architecture, language, database, frontend, observability and style document before ordinary implementation.

Escalate context only when the task crosses the boundary owned by that context.

Examples:

- a small HTTP handler fix may need the handler, its use case and HTTP contract, not the full DDD/PostgreSQL/style corpus;
- a new bounded context or large architectural change should load Clean Architecture/DDD and package/API guidance;
- a transaction/concurrency change should load the PostgreSQL module;
- an FSD placement refactor should load FSD/package/UI ownership rules;
- a formatting/style cleanup should load language/style tooling after functionality is already stable.

## Just-in-time rule loading

Rules should be grouped by the decision they protect.

A task skill/router should expose conditional modules rather than forcing all modules into every task.

Load a rule when at least one is true:

- the task changes the boundary governed by the rule;
- a decision cannot be made safely without it;
- validation/review specifically targets that concern;
- the user asks for that quality dimension;
- a previous finding proves that concern is currently risky.

Do not load a rule merely because it is generally 'good practice'.

## Correction-triggered context recovery

Repeated explicit correction is a context signal.

When a user rejects the same technical direction more than once, says the implementation violates an earlier requirement, or becomes strongly dissatisfied immediately after a technical mismatch:

1. stop stacking local fixes;
2. recover the latest explicit acceptance requirements and the durable task/branch state;
3. compare the current design against those requirements rather than against the most recent failure alone;
4. identify whether the drift is in terminology, trust model, lifecycle assumptions, ownership, validation level or tool/routing rules;
5. load only the authority that owns that mismatch;
6. restate/persist the corrected contract before substantial implementation resumes.

Do not treat frustration as permission to guess what the user wants, and do not bulk-reload every document as a ritual. The purpose of the reset is to recover the decision model that produced the wrong work.

## Context escalation

Start narrow, but do not remain narrow when evidence shows the task crosses another boundary.

Escalate by the next real decision boundary:

- local source -> neighboring module;
- module -> public package/API contract;
- application -> shared system contract;
- code -> persistence/operations/security authority;
- one repository -> cross-repository authority.

Retrieve only the next required layer, inspect the result, then decide whether more is needed.
