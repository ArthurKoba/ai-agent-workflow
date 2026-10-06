# Best Practices Registry

## B-001 — Externalize state
Current state must live outside chat memory.

## B-002 — One authority per layer
Separate current source/state, heavy evidence, mutable reverse knowledge and local environment context.

## B-003 — Adaptive granularity
Stop at real decision boundaries; group proven routine steps.

## B-004 — Searchable corpus
Prepare evidence once and query it repeatedly.

## B-005 — Capture once, analyze offline

## B-006 — Known-good baseline + delta isolation

## B-007 — Validation ontology
Do not collapse source/build/hardware/product acceptance.

## B-008 — Natural repository ownership

## B-009 — Parallel specialists with explicit scopes

## B-010 — Implementer / Reviewer separation

## B-011 — MCP-first for deterministic operations

## B-012 — Same-iteration authority synchronization

## B-013 — Local context outside universal prompts

## B-014 — Completion audit

## B-015 — Fail closed on unknown capability
Unknown ABI/feature/tool behavior must be explicit, not silent success.

## B-016 — Fail closed on insufficient evidence
When evidence cannot support the required conclusion, maximize grounded progress, state the unknown explicitly and change evidence path rather than inventing certainty.

## B-017 — Contradiction ledger with severity
Contradictions are tracked deliberately. Material planning/acceptance contradictions block progress; implementation-time contradictions may be deferred only when they are non-blocking and recorded for closure.

## B-018 — Autonomous execution with scoped progress
Continue independently as far as tools/evidence/permissions allow. Report progress by milestone and remaining scope; percentages are approximate and must name their denominator.


## B-019 — Observable bootstrap
A workflow map/skill is considered loaded only when actually retrieved or injected. Substantial work has a startup gate before implementation/mutation/operator commands.

## B-020 — Durable Task Context
Long-running work externalizes objective, acceptance, active ref, known-good state, active patch/delta identity, latest result, blockers and next decision boundary. Patch continuity must not depend on chat memory.


## B-021 — Local contract beats generic default
Universal skills define the class of operation; project/local context defines concrete transport, flags and operational classification. When a local contract exists, it wins. Missing local context is a blocker, not a reason to fall back to a familiar default.


## B-022 — Pre-send hard-constraint compliance
Reading a rule is not enough. Before sending output governed by an active skill/project contract, validate the draft against its hard constraints. Explicit STOP/MUST/decision-boundary rules outrank secondary response objectives.


## B-023 — Isolate build-lane environment
WSL/container/native Linux builds must use the environment contract of that lane. Do not let host Windows PATH/toolchain state leak into Buildroot or other Linux-native builds. Reuse a known clean environment instead of rediscovering it after failure.

## B-024 — Observable safety-block incident loop
During reverse/behavior analysis, every provider/safety/pre-tool block becomes a durable, sanitized incident evidence point. Re-read the active behavior-analysis terminology before the next analysis call, consolidate repeated occurrences into the same infrastructure issue when they share a failure class, and distinguish the block from target evidence.

## B-025 — Persist research exhaustion and stay reverse-first
For legacy/obscure silicon, once bounded public research has failed to produce authoritative material, record that boundary and make target reverse the default in later sessions. Reopen web/source research only for a new concrete lead or explicit user request; do not restart family-wide searching merely because a new agent/chat began.


## B-026 — Delta-first progress reporting
Ordinary report requests show only changes since the previous report checkpoint: changed progress as a scalar `before -> after`, unique new findings, current goal status and the immediate next path. Full/detailed reports intentionally reconstruct the complete current state. Long-running tasks persist enough report-checkpoint state to make the delta recoverable after context changes.

## B-027 — Sticky progress metrics
Once an active workstream is reported with a scoped percentage, preserve that percentage basis across later reports so progress remains comparable. This includes an established overall-goal percentage. Exact counters and evidence states may supplement the percentage; if the prior numeric value is temporarily unrecoverable, keep the current approximate percentage and mark the old baseline unavailable rather than silently switching metrics.


## B-028 — Parser-aware Coolify Compose
Treat Coolify's Compose parser as an explicit deployment API. Encode required external topology with empty `:?` expressions in owning service environments, keep secrets behind scoped shared references, keep internal traffic on Docker DNS, use one generated-domain owner per service, use inline `content:` for managed file templates, and validate parser-generated UI state on a fresh resource before runtime acceptance.

## B-029 — Evidence-state semantic lifecycle
Persistent behavior-analysis metadata is confidence-aware. Unknown objects stay structural; likely conclusions may use conservative provisional names; confirmed behavior is promoted to canonical semantic names and synchronized comments/types/boundaries/links; contradictions demote misleading metadata; withdrawn interpretations are retired. One semantic object keeps one canonical name across references, and stale strong names are treated as defects rather than harmless history.
