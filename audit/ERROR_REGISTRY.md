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


## E-023 — Tool safety/provider block disappears from the evidence trail
A provider, policy, safety or pre-tool block is treated as a transient inconvenience: the agent switches paths, but the exact blocked invocation is never recorded, so repeated false positives cannot be correlated or fixed.
Mitigation: on every block, re-read the active domain terminology/rules, record a sanitized invocation evidence point, deduplicate against the configured infrastructure incident tracker, append to an existing analogous issue or create one, then continue through a legitimate alternate evidence path.

## E-024 — Exhausted public research is restarted every session
A reverse-analysis agent repeats generic web/source/datasheet/SDK searches for the same legacy or obscure processor/controller even though prior project evidence already established that the public path is exhausted. This consumes time, duplicates weak family-level material and displaces target reverse.
Mitigation: persist the research-exhausted boundary. Do not reopen generic external research without a new concrete artifact/identifier lead or an explicit user request; continue from target firmware, Analysis and runtime/board evidence instead.

## E-025 — Compact progress reports repeat unchanged state
A long-running agent answers every ordinary report request by restating the same baseline, completed areas and old findings instead of reporting the delta since the previous report. This hides real progress, increases noise and makes progress numbers hard to compare.
Mitigation: use the reporting protocol. Plain reports are delta reports against the previous report checkpoint, changed directions use scalar `before -> after` progress, unchanged material is omitted, and the next decision boundary is always stated. Full/detailed reports remain comprehensive snapshots.

## E-026 — Progress percentage disappears from a report
A report replaces an established or meaningfully estimable percentage with counters, qualitative states or prose, so the user loses continuity of progress even though the underlying work can still be compared.
Mitigation: percentage reporting is sticky per active direction/workstream, including an established overall-goal percentage. Preserve the same scoped denominator across reports; if the previous numeric value is temporarily unrecoverable, report the current approximate percentage and mark the prior baseline unavailable rather than downgrading to counters/status.

## E-027 — Generic Compose validity is mistaken for Coolify parser correctness
Agent writes syntactically valid Compose but ignores the orchestrator parser contract, causing required variables to receive placeholder values, variables used only in ports/commands to disappear from the UI, multiple domains to collapse onto one service, managed files to fail to materialize, internal ports to be published unnecessarily, secrets to be copied into Git/resource envs, or broad watch paths to redeploy production on docs-only commits.
Mitigation: load the Coolify Compose contract; classify each value as secret/shared, required external topology, safe default, internal literal or generated parser state; validate the result on a freshly parsed Coolify resource before deployment; scope Watch paths to actual deployment inputs rather than directory ownership alone.

## E-028 — Semantic metadata claims stronger certainty than the evidence
A behavior-analysis project leaves generic names after semantics are closed, keeps provisional/candidate names after confirmation, or preserves strong semantic names/types/links after evidence weakens or contradicts them. Future agents then inherit either lost knowledge or false certainty from the persistent analysis surface.
Mitigation: use the evidence-state semantic lifecycle. Keep names/comments/types/boundaries/links synchronized with `UNKNOWN`/`LIKELY`/`CONFIRMED`/`CONTRADICTION`, retire withdrawn interpretations, reuse canonical semantic objects across references, and save after each coherent materialization pass.

## E-029 — Local failure silently rewrites the acceptance contract
An agent reacts to the latest deployment/test failure by changing topology, trust model, user flow or ownership without checking whether the new design still satisfies the already accepted requirements. A local fix becomes an accidental product/architecture decision.
Mitigation: freeze the acceptance contract before implementation. Failures may change implementation details; changing an invariant requires an explicit contradiction/contract decision first.

## E-030 — Repeated user correction is treated as conversational noise
The user explicitly rejects the same technical direction or signals escalating dissatisfaction after a mismatch, but the agent treats it only as tone and continues from the same task model.
Mitigation: trigger a narrow re-bootstrap/self-audit. Recover the latest explicit requirements and durable state, identify the drifted assumption/owner, reload only the relevant authority, and persist the corrected contract before continuing.

## E-031 — Deployment lifecycle is designed only for the happy path
A deployment is designed around first startup while repeat deploy, partial prior state, stale parser/runtime artifacts, reboot, upgrade, rollback or migration are not modeled. The first pass works, then ordinary lifecycle transitions fail.
Mitigation: define a lifecycle matrix before rollout and add regression/acceptance coverage for every materially different state transition.

## E-032 — Incidental metadata is promoted to a functional invariant
An implementation requires a representation detail (numeric owner/group equality, path shape, parser record, container count) even though the real consumer contract is behavioral and the representation can legitimately differ under namespaces/orchestrators.
Mitigation: define acceptance from the real consumer operation first; require metadata equality only when the underlying system contract explicitly guarantees it.

## E-033 — Validation path does not match the real execution path
Syntax/static checks pass, but production executes through a materially different wrapper/mode such as stdin, `bash -s`, sourcing, `set -u`, `nsenter`, generated Compose interpolation or an orchestrator helper.
Mitigation: retain fast static checks, then reproduce the exact invocation path or the closest faithful harness before rollout.

## E-034 — Nominal resource separation is mistaken for a security boundary
A privileged operation is moved to another service/template/resource under the same repository, credentials and deployment authority, and the split is described as isolation even though the same actor can still control both sides. Operational complexity increases without materially reducing authority.
Mitigation: draw the authority/credential graph. A boundary is real only when permissions, identities, approval or deployment authority differ; otherwise protect untrusted workloads from the trusted control plane without inventing a fake boundary.

## E-035 — Upstream lifecycle ownership is discovered after custom policy was built
An agent reimplements enrollment, service lifecycle, backend probing, cgroup/runtime policy or upgrade behavior before reading the third-party system's installer/source. Custom code duplicates upstream ownership and creates invented invariants.
Mitigation: inspect upstream source/installer and supported deployment modes before designing custom provisioning; implement only the uncovered integration gap and validate against upstream behavior.

Add a new class only when root cause or mitigation is materially different.
