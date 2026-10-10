# Context-Efficient AI Engineering

Use this skill when designing repository documentation, agent bootstrap/context loading, multi-agent engineering workflows, or staged implementation/refactoring so agents can work accurately without preloading the whole system.

## Core principle

Context is a constrained engineering resource.

The goal is not to maximize how much documentation an agent reads. The goal is to load the smallest authoritative context that lets the agent make the next correct decision, then retrieve more evidence only when the task crosses a real boundary.

A large always-on context creates three costs:

- token and context-window consumption;
- slower evidence retrieval and more irrelevant attention;
- higher risk that stale narrative documentation competes with current source code.

Prefer progressive disclosure over mandatory bulk reading.

**Progressive disclosure selects files, not fragments.** Once a map, role,
skill or contract is required for the current decision, read the **entire**
file and honor the missing-source STOP/user-approval gate in
`../docs/BOOTSTRAP_PROTOCOL.md`. A summary or truncated response cannot
substitute for the complete required authority.

## Documentation ownership

Documentation must not become a second implementation.

### Code owns implementation detail

Source code is the authority for:

- concrete functions/classes/modules;
- internal call flow;
- exact implementation structure;
- current private helpers;
- low-level algorithm details;
- line-by-line behavior that can be recovered cheaply from the source.

Do not duplicate these details into a giant current-state document merely so an agent can preload them. The agent should navigate to the relevant source and read it when the task requires it.

### Documentation owns durable contracts and navigation

Documentation is justified when it carries information that cannot be recovered safely or cheaply from one local code read, for example:

- system/product boundaries;
- cross-repository contracts;
- public API/transport/data contracts;
- domain invariants and terminology;
- architectural ownership decisions;
- operational/release/recovery contracts;
- unresolved contradictions, gates and accepted future requirements;
- a compact map from capability/domain to the code/document owner.

### One meaning, one owner

Do not maintain equivalent implementation truth in both source and narrative documentation.

If a fact changes whenever the implementation changes and can be observed directly from code, prefer a navigation pointer over a duplicated description.

If several applications need the same contract, give that contract one shared authority instead of copying it into each application repository.

## Repository documentation shape

### AGENTS.md is a router

`AGENTS.md` should answer only the startup/navigation questions:

- what repository/project is this;
- what authorities matter;
- which task skill applies;
- what minimal project map/status file should be read;
- where shared contracts live;
- which repository-specific policies can change agent decisions.

It should not contain a complete architecture manual, coding style handbook, implementation history or duplicated universal skill text.

### Project/application map is a map

A project map should optimize navigation, not describe the codebase exhaustively.

Good map entries look like:

```text
authentication -> src/domain/auth + src/application/auth + HTTP auth contract
finance -> src/domain/finance + src/application/finance + shared finance contract
subscription UI -> src/entities/subscription + relevant feature/widget entry points
deployment -> operations/deployment.md
```

The map tells the agent where to jump. The source then explains how the implementation works.

Do not turn the map into a catalog of every class, worker, DTO, repository method, event or database model.

### Shared system authority

When backend, frontend, workers or other applications must agree on the same behavior, put the shared meaning in one neutral project authority selected by the Project architecture.

Typical shared material:

- product/system capabilities and boundaries;
- backend/frontend integration contracts;
- public API semantics;
- shared domain vocabulary;
- cross-application workflows;
- common acceptance/release contracts;
- system-level decisions that neither application owns alone.

Backend/frontend repositories should link to that shared owner and keep only their local implementation map, local constraints and local state.

## Work tracking

Unfinished work, defects, acceptance gaps and follow-up tasks belong in the repository's issue/work-item tracker when one is available.

Do not maintain Markdown roadmaps, backlog files or open-question lists as a parallel planning database. Documentation may define durable acceptance criteria or product semantics; Issues/Work Items own task lifecycle, priority, assignee, discussion and closure evidence.

A documentation page may link to an issue, but it must not copy the mutable task state back into prose. Conditional future options should become issues only when they are actually activated.

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

## Implementation and refactoring are different passes

Do not force one agent/pass to optimize every quality dimension at once.

For substantial work, a high-throughput workflow may intentionally separate:

### 1. Functional implementation pass

Objective: make the required behavior real and integrate it with the existing system.

Load:

- task/product contract;
- local source around the change;
- only architectural/safety rules required for correctness.

Do not preload unrelated style/refactor checklists.

### 2. Architecture pass

Objective: verify boundaries, ownership, dependency direction, domain/application/infrastructure placement and lifecycle decisions.

Load the architecture-specific skill modules and inspect the integrated implementation.

### 3. Module/package/import pass

Objective: verify public APIs, encapsulation, file/module ownership, imports, dependency edges and package layout.

Load package/module rules, not unrelated database/UI material.

### 4. Consistency/duplication pass

Objective: identify repeated behavior, parallel contracts, redundant adapters/helpers and inconsistent naming/ownership.

Focus on the relevant code slice plus cross-references.

### 5. API/contract pass

Objective: verify public HTTP/event/provider/data contracts, compatibility and backend/frontend agreement.

Load only contract authorities and the affected adapters/consumers.

### 6. Persistence/concurrency/performance pass

Objective: verify database invariants, transaction boundaries, query shape, locks, indexes and measured performance risks.

Load database-specific modules only when persistence is in scope.

### 7. Code-quality/style/tooling pass

Objective: run targeted linters/type checks/static diagnostics and clean style/typing/import issues after behavior and architecture have stabilized.

This is the right pass for detailed language/style rules that would otherwise consume implementation context without changing the main design decision.

Additional passes such as security, observability, accessibility, deployment or hardware acceptance should be added when the product risk requires them.

## Multi-agent orchestration

Different passes may use different agents/workspaces when independence or context isolation improves quality.

Each slice should receive:

- one explicit objective;
- a bounded source/diff scope;
- the one or few authorities needed for that objective;
- the relevant skill module(s);
- the current patch/commit identity;
- the validation expected from that pass.

Do not give every specialist the full project corpus by default.

An architecture reviewer does not need every style rule. A style agent does not need the complete issue backlog/product-planning context. A database reviewer does not need the entire frontend architecture unless the contract crosses that boundary.

Fan-in must operate on one known integrated revision so findings from separate passes refer to the same implementation.

## Documentation synchronization after changes

Update documentation when the change modifies durable meaning, not whenever source lines change.

Usually update docs when changing:

- public/system contracts;
- domain invariants;
- ownership/boundaries;
- project/application maps;
- operational/release procedures;
- architectural decisions;
- known blockers/acceptance gates.

Usually do not update narrative docs for:

- private helper refactors;
- implementation-only class/function movement already discoverable from the map/source;
- formatting/type cleanup;
- internal call-flow changes that do not alter a durable contract.

## Backend/frontend synchronization

Backend and frontend should not synchronize by maintaining two large prose descriptions of each other.

Prefer:

```text
shared contract authority
        ↓
backend local implementation map
        ↓
backend source

shared contract authority
        ↓
frontend local implementation map
        ↓
frontend source
```

The shared contract defines what must agree. Each application map says where its side is implemented. The code supplies the implementation detail.

## Context escalation

Start narrow, but do not remain narrow when evidence shows the task crosses another boundary.

Escalate by the next real decision boundary:

- local source -> neighboring module;
- module -> public package/API contract;
- application -> shared system contract;
- code -> persistence/operations/security authority;
- one repository -> cross-repository authority.

Retrieve only the next required layer, inspect the result, then decide whether more is needed.

## Anti-patterns

Avoid:

- mandatory reading lists that load most of the project before every task;
- giant `current-state.md` files that mirror implementation details;
- architecture documents that enumerate every class/method/model;
- duplicating backend behavior inside frontend docs or vice versa;
- universal style/linter rules in the startup path for every implementation task;
- one mega-agent expected to implement, architecturally refactor, style-clean, performance-tune and review everything in one context;
- multiple documents that claim authority over the same current behavior;
- documentation that must be updated line-for-line with ordinary refactors.

## Audit questions

When refactoring an existing project's documentation/context system, ask:

1. What must every agent know before any substantial task?
2. What can be discovered from code on demand?
3. Which contracts are shared across applications and need one neutral owner?
4. Which current documents duplicate implementation detail?
5. Which mandatory files can become conditional modules?
6. Can the project map route from capability/domain to source in a few lines?
7. Are backend/frontend synchronized through shared contracts rather than duplicated prose?
8. Can implementation and later quality/refactor passes use separate context sets?
9. Is every rule loaded because it protects a decision in the current pass?
10. Does any documentation owner compete with the source code for implementation truth?

## Completion criteria

A context/documentation refactor is successful when:

- startup context is small and stable;
- shared contracts have one owner;
- application maps are compact navigation surfaces;
- source code remains the implementation authority;
- task rules are loaded just in time;
- specialized passes can work from isolated context without rediscovering the whole system;
- documentation still preserves durable product/architecture/operational knowledge;
- removing duplicated narrative detail does not remove any contract, invariant, decision or acceptance gate that cannot be recovered from code alone.
