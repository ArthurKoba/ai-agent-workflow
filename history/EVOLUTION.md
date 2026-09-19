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
