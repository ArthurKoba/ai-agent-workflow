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

Add a new class only when root cause or mitigation is materially different.
