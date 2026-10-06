# Agent System Evolution

## Provenance

The first large evidence base for this evolution was the ANJIA AJL33PQ0866 / FH8626V100 reverse-and-porting project:

`ArthurKoba/anjia-ajl33pq0866-fh8626v100-reverse`

Its detailed technical chronology remains in that project. This file keeps only the generalized operating-model evolution, strengths, weaknesses and automation/quality effects.


## 1 — Chat-centric manual workflow
Model: agent proposes; user runs commands, transfers files/context, remembers state.

Pros: simple, almost no infrastructure.
Cons: state loss, repeated extraction, user as router, poor continuity.
Automation/quality: low automation; quality depends heavily on one chat retaining context.

## 2 — Workspace + checkpoints
Added canonical unpacked workspace, checkpoints/handoffs and persistent runtime owners.

Pros: better recovery, less repeated setup.
Cons: archives/copies can become competing truth.
Automation/quality: better reproducibility, still transfer-heavy.

## 3 — Parallel specialists
Separate reverse/implementation/evidence/product roles.

Pros: throughput and specialist depth.
Cons: fan-in and duplicated research; user still routes context.
Automation/quality: more work in parallel, coordination quality becomes limiting factor.

## 4 — Structured evidence corpus + orchestrator
Searchable corpus, maps/indexes, frozen base + delta fan-in, milestone progress.

Pros: less blind reverse, better precision and handoff.
Cons: workspace/orchestrator complexity.
Automation/quality: large accuracy gain because evidence is reused instead of recreated.

## 5 — Durable external storage
Heavy evidence/checkpoints survive chat/session loss.

Pros: persistence.
Cons: source/current state and evidence can drift if authority is unclear.

## 6 — Git + semantic reverse authority
Current source/state/contracts in Git; mutable reverse knowledge in semantic projects; heavy evidence separately stored.

Pros: reproducible history, explicit ownership, less manual file routing.
Cons: branch/project sprawl without discipline.

## 7 — MCP-native engineering
Typed repository, reverse, artifact and HTTP operations.

Pros: fewer dependency/setup mistakes, faster autonomous work, safe defaults, provenance.
Cons: MCP gaps/permissions become infrastructure blockers; tool quality matters.

## 8 — Independent review + shared contracts
Separate Implementer/Reviewer identities and parallel implementation lanes sharing neutral contracts.

Pros: less self-confirmation, better regression detection, less user routing.
Cons: requires clear ownership and review policy.

## Current model
`account prompt → project prompt → task skill`

with AGENTS as router, external state authority, local context outside prompts, MCP-first deterministic operations and periodic audit aggregation.

## Future direction
Improve task routing, MCP coverage, automated evidence ingestion, review quality and audit aggregation.

Avoid adding prompt depth unless the three-layer hierarchy genuinely cannot express the need.

## 9 — Reusable engineering skill library

Mature project-level engineering rules were generalized into reusable, project-neutral skill modules instead of remaining duplicated inside one product/infrastructure repository.

Added conditional software/backend modules for Clean Architecture/DDD, Python, package APIs, PostgreSQL, observability and aiogram-dialog; frontend modules for Vue/TypeScript, FSD, UI and table architecture; a Git commit workflow, skill-authoring/context-maintenance contracts and a richer Orchestrator role.

Project-specific commands, versions, product names, runtime values and temporary testing policies remain below the universal layer. Large specialist documents are conditional modules routed by a small skill entry point rather than mandatory startup context.

Automation/quality effect: reusable engineering knowledge is available across projects without turning one project's infrastructure repository into a second global prompt authority.

## 10 — Shared behavior-analysis vocabulary and project lifecycle

Audio Rush had accumulated reusable reverse-analysis terminology, evidence states, proof-level semantics and persistent Analysis project/session recovery rules inside its repository-local `AGENTS.md`.

Those concepts now live under `skills/hardware-reverse/` as conditional modules. Device-specific firmware/board contracts remain in the Audio Rush repository, while the universal skill owns behavior-analysis vocabulary, evidence/proof semantics and persistent project/session/program lifecycle.

Automation/quality effect: reverse-analysis agents across projects can use one terminology/evidence model without project-local copies, and session/worker failures are less likely to be misread as lost analysis state.

## 11 — Context-efficient engineering and staged specialist passes

Large project maps and mandatory current-state/rule bundles were identified as a quality problem: they consume context before the agent knows which subsystem or quality dimension matters, and they encourage documentation to mirror implementation details already available in source.

The workflow now treats context budget as an explicit engineering constraint. `context-engineering` defines compact repository maps, shared-contract ownership, code-as-implementation-authority, just-in-time rule loading and staged specialist passes for implementation, architecture, package/import boundaries, consistency, API/contracts, persistence/performance and code-quality/style.

Automation/quality effect: agents spend more context on the current decision, backend/frontend can synchronize through one shared contract authority, and later refactoring/review agents can load only the concern-specific rules needed for their pass.

## 12 — Observable provider/safety incident feedback

Reverse-analysis work now treats provider/policy/safety/pre-tool blocks as first-class infrastructure evidence. Each occurrence triggers a narrow reload of the active behavior-analysis terminology, a sanitized capture of the blocked invocation, deduplication into the configured incident tracker, and continuation through a legitimate alternate evidence path when available.

Repeated instances of the same failure class are accumulated in one issue rather than scattered across chats. This separates tool/provider failures from target evidence while building enough invocation-level history to diagnose false-positive safety checks and improve the MCP/provider layer.

Automation/quality effect: analysis can continue without blind retries, while safety/provider regressions become measurable and repairable instead of ephemeral.

## 13 — Research-exhaustion persistence for legacy silicon

Legacy-chip reverse work now persists a stop condition for generic public research. Once bounded datasheet/SDK/source/family searches have failed to produce authoritative material, a new chat or agent does not reset that evidence path to unknown. Target firmware, saved Analysis state, runtime traces and board evidence become the default continuation.

External research resumes only when a new concrete identifier/artifact materially changes the search space or the user explicitly requests another research pass.

Automation/quality effect: long-running reverse projects stop paying the same public-research tax on every handoff and spend more cycles on evidence that can actually close target behavior contracts.


## 14 — Delta-first report checkpoints

Long-running work now distinguishes ordinary progress reports from full state snapshots. An ordinary report is a delta against the previous user-facing report checkpoint: only changed directions, new findings, scalar progress transitions, goal status and the next decision boundary are shown. A full/detailed report intentionally reconstructs the complete current state.

Report comparison state can be persisted alongside existing Task Context/status authorities so a context change does not force the agent to repeat the entire project or lose the `before -> after` baseline. Progress ranges are replaced by one stable scalar estimate, exact counters or explicit state transitions.

Automation/quality effect: users can see real incremental progress without manually diffing repetitive reports, while comprehensive reports remain available on explicit request.
