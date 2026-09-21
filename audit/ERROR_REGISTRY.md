# Error Registry

Generalized recurring failure classes.

## E-001 — Current-state loss
Agent forgets/assumes environment, target or repository state.
Mitigation: external state authority + live inventory after context changes.

## E-002 — Wrong step granularity
Agent runs too far past decision boundaries or produces excessive microsteps.
Mitigation: adaptive granularity.

## E-003 — Execution-lane confusion
Host/WSL/SSH/UART/bootloader contexts are mixed.
Mitigation: terminal skill + explicit lane.

## E-004 — Protocol/rule drift
Agent acknowledges a rule and later ignores it.
Mitigation: encode stable rules in prompt/skill/tool instead of chat memory.

## E-005 — User becomes technical router
User must interpret outputs, move files/context or repeat agent-accessible work.
Mitigation: agent-owned branching + shared authority + MCP access.

## E-006 — Premature completion
Central mechanism solved but acceptance surface still open.
Mitigation: requirement audit + validation levels.

## E-007 — Documentation/source drift
Docs and actual source/state disagree.
Mitigation: same-iteration synchronization + reread actual source before claims.

## E-008 — Validation inheritance
Different bytes/state inherit a previous PASS.
Mitigation: bind validation to exact artifact/commit identity.

## E-009 — Diagnostic changes the system
Observation destabilizes the investigated state.
Mitigation: safety/resource model + state-machine experiment.

## E-010 — Competing authorities
Multiple active trees/projects/branches/handoffs claim to be current.
Mitigation: one canonical authority per layer; archive old states.

## E-011 — Ownership mixing
Kernel/device/runtime/coordination/infrastructure logic accumulates in the wrong repository.
Mitigation: natural-owner architecture.

## E-012 — Cleanup removes dependency before replacement
Legacy dependency removed before a new owner/provider exists.
Mitigation: dependency-closure audit + transitional pinned provider.

## E-013 — Broad work instead of targeted evidence
Agent scans/reverses/builds more than needed for the next decision.
Mitigation: evidence contract scoped to next boundary.

## E-014 — Self-review presented as independent review
Implementer claims independent assurance without a separate pass.
Mitigation: Reviewer role/identity.

## E-015 — Tool bypass
Agent installs/reimplements workflows instead of using the project’s specialized MCP/tool.
Mitigation: primary-tool policy + capability-gap reporting.

## E-016 — Fabricated certainty under insufficient evidence
Agent lacks enough information to support a required conclusion but continues by inventing an answer, contract, path or causal explanation.
Mitigation: bounded evidence work → explicit unknown → alternate evidence path or stop boundary. Never convert missing information into confident prose.

## E-017 — Unresolved contradiction is ignored
Conflicting user requirements, documentation, source facts or acceptance criteria are left unresolved while implementation proceeds as if they were compatible.
Mitigation: resolve material contradictions before planning/acceptance; during implementation track non-blocking contradictions explicitly and stop only when they threaten correctness, safety or acceptance validity.

## E-018 — Claimed context load without evidence
Agent says AGENTS/skill/prompt was read or accounted for, but there is no actual retrieval/injected context and behavior immediately violates that file.
Mitigation: hard bootstrap gate; a document counts as loaded only when actually retrieved or injected. Never use conversational acknowledgement as proof of loading.

## E-019 — Volatile patch/delta exists only in chat memory
An unfinished patch, diff, generated file set or validation state is not persisted to repository/artifact/task state and is lost after context growth, handoff or restart.
Mitigation: durable Task Context with exact repo/ref/files + diff/patch/artifact locator + applied/validation state before long continuation or handoff.

## E-020 — Generic default overrides a known local contract
Agent reads the universal rule correctly but resolves “project/local-specific” as permission to use a generic default instead of restoring the actual local contract.
Example: using modern `scp` after reading that the required legacy `scp -O` belongs to project/local context.
Mitigation: explicit local-contract precedence; expected-but-unavailable local contract blocks command emission rather than triggering fallback to generic defaults.

## E-021 — Hard constraint displaced by a competing response objective
Agent correctly reads and understands an active rule, but while composing the answer optimizes for another goal (for example “give the full end-to-end path”) and violates the loaded hard constraint (for example “stop at the first real decision boundary”).
Mitigation: explicit pre-send compliance gate. Hard Project/skill constraints outrank completeness, compactness, convenience and end-to-end planning goals.

## E-022 — Host environment leaks into an isolated build lane
A WSL/container/Linux-native build inherits host environment entries that are invalid or unsafe for the build system. Example: Windows `PATH` entries under `/mnt/c/Program Files/...` reach Buildroot, which rejects PATH values containing spaces.
Mitigation: explicit build-lane environment isolation; restore the known Linux-only PATH, reset shell command hashing, and keep Linux-native builds on the intended Linux workspace/toolchain surface.

Add a new class only when root cause or mitigation is materially different.
