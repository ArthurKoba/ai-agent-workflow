# Prompt / Workflow Changelog

## 2026-10 — Route Briareus Analysis MCP incidents to their service owner

Changes:
- named `https://github.com/ArthurKoba/briareus/issues` as the tracker for
  Briareus Analysis MCP (`/analysis/mcp`) failures and pre-tool policy blocks;
- require deduplication against existing Briareus issues instead of
  reporting them to `ArthurKoba/infrastructure` or the analyzed project;
- require an explicit provider-owned tracker for other services, and a
  local incident checkpoint when no owner has been configured.

Reason: a reverse-analysis pre-tool block was incorrectly filed in an
unrelated infrastructure repository because the skill did not identify
the Analysis MCP service's actual issue tracker.

## 2026-10 — Terminal commands grouped by decision boundary

Changes:
- clarified that one current operator decision boundary receives one copyable block, even when collecting several related evidence points;
- made terminal clearing conditional on no longer needing the previous output, with no separate clearance block;
- recorded the operator-overhead failure in E-038 and the matching practice in B-039 (avoiding pre-existing E-029/B-029 IDs).

Reason:
The old rule could lead an agent to fragment a single routine collection into multiple blocks and inadvertently discard the information needed at the next decision.

## 2026-10 — Progress is bounded by the active recovery task

Changes:
- reverse-analysis now scores a named behavior contract against the
  target artifact and its actual in-scope code, not unknown EC internals,
  foreign firmware versions, hardware acceptance or future OS adapters;
- reporting protocol now requires explicit denominator boundaries,
  separate external unknowns and rebaselining misleading near-100 figures.

Reason: an agent held otherwise recovered target-side contracts at
unjustified near-completion percentages because unrelated downstream
firmware and product-validation tasks remained open.

## 2026-10 — Flat Reverse Analysis skill

Changes:
- renamed the general program-behavior skill to `skills/reverse-analysis.md` at the root of `skills/`;
- removed the one-file `program-analysis/README.md` folder and redirected active maps;
- set flat `skills/<skill-name>.md` as the normal standalone skill format, retaining folder/README only for genuinely multi-file skills;
- preserved the reverse-analysis method for executables, BIOS/UEFI, libraries, drivers and firmware, including semantics, tracing, script persistence and monitored jobs.

Reason:
The previous correction consolidated content but still created an unnecessary folder/README indirection. A single cohesive skill should be a single named file. Historical references below are provenance, not active router paths.

## 2026-10 — Standalone program-analysis skill

Changes:
- renamed the former hardware-reverse skill to `skills/program-analysis/README.md`, maintaining a single file and no nested analysis subskills;
- broadened analyzer tracing, semantic naming, evidence states and Java/GhidraScript lifecycle to executables, BIOS/UEFI, libraries, drivers, services and firmware;
- updated active workflow routing; historical references to the old directory remain only in chronological audit records.

Reason:
The analysis skill is about investigating program behavior, not inherently hardware reverse. A standalone cohesive skill avoids unnecessary navigation and applies to high- and low-level code equally.

## 2026-10 — Coolify watch-path input isolation

Changes:
- Coolify/Git-backed infrastructure now scopes Watch paths to actual deployment inputs instead of assuming the entire service directory should trigger redeploy;
- README/runbook/audit-only files are explicitly excluded from deployment triggers unless they are real runtime inputs;
- E-027/B-028 now include docs-only redeploy as parser/orchestrator-contract failure.

Reason:
A documentation-only update inside a watched deployment directory triggered a live service redeploy even though no runtime input changed. Directory ownership is not the same thing as deployment-input ownership.

## 2026-10 — Contract recovery after repeated correction

Changes:
- bootstrap now treats repeated explicit technical correction or escalating dissatisfaction after a mismatch as a narrow re-bootstrap trigger;
- context-engineering defines a correction-triggered recovery flow: stop patch stacking, recover the latest acceptance contract and durable state, identify the drifted assumption/owner, reload only the relevant authority, then persist the corrected contract;
- audit now distinguishes acceptance-contract drift from ordinary local defects and treats repeated user correction as workflow evidence rather than conversational noise;
- added E-029/E-030 and B-030/B-031.

Reason:
A long infrastructure integration repeatedly optimized for the latest failure and, after user corrections, sometimes continued from the same incorrect task model. The productive turning point was to stop implementation, reconstruct the non-negotiable contract and resolve contradictions before coding again. The reusable lesson is not to preload more context; it is to reload the right context when feedback proves the current model is wrong.

## 2026-10 — Lifecycle-first infrastructure and parser acceptance

Changes:
- service engineering now freezes deployment-entrypoint, steady-state, privilege, persistence, manual-step and validation invariants before substantial redesign;
- Git-backed infrastructure now requires lifecycle coverage for clean install, repeat deploy, stale/partial state, restart/reboot, upgrade/migration and rollback;
- resource/service separation is no longer treated as a security boundary unless permissions, identities, credentials or deployment authority actually differ;
- Docker/Compose guidance distinguishes one deployment entrypoint from one service/container and allows narrowly scoped one-shot privileged bootstrap only when the accepted trust model requires it;
- terminal operations now require validation of the exact production invocation mode, not only shell syntax;
- Coolify guidance now covers generated-route vs application-visible URL separation, nested generated-URL fallback, fresh-resource parser-state diagnosis, narrow legacy storage migration and user-namespace ownership semantics;
- added E-031 through E-035 and B-032 through B-036.

Reason:
The same integration exposed several independent failure classes: happy-path-only bootstrap design, invented metadata invariants, syntax tests that did not match stdin/wrapper execution, a nominal resource split that added complexity without a new authority boundary, and duplicated lifecycle/security behavior implemented before upstream ownership was understood. Clean recreation plus behavioral acceptance closed the ambiguity.


## 2026-10 — Evidence-state semantic naming lifecycle

Changes:
- `skills/hardware-reverse/behavior-analysis.md` now defines an explicit semantic lifecycle for actions, states/globals, MMIO/register fields, constants, structures, protocol fields, addresses and action links;
- `UNKNOWN` stays structural, `LIKELY` may use conservative provisional naming, and `CONFIRMED` promotes the object to canonical semantic metadata;
- contradictions now require demotion/neutralization of names/types/links that assert too much, while `WITHDRAWN` is defined as a historical marker for invalidated interpretations rather than a live evidence state;
- semantic promotion/demotion must synchronize names, comments, types/prototypes, boundaries and proven relationships in one coherent materialization pass;
- repeated references reuse one canonical semantic object instead of accumulating per-action synonyms, while equal numeric values are not merged without identity proof;
- added E-028 / B-029 for semantic metadata whose apparent certainty drifts away from the actual evidence.

Reason:
Long-running firmware behavior recovery can accumulate two opposite defects: confirmed behavior remains hidden behind generic addresses/FUN names, while older speculative names survive after later evidence disproves their owner or hardware interpretation. The persistent Analysis surface is a handoff authority, so its names and relationships must communicate the current evidence strength rather than merely preserve the chronology of guesses.

## 2026-10 — Coolify Compose parser contract

Changes:
- added `skills/service-engineering/coolify-compose.md` as the focused authority for Coolify-parsed Compose;
- Coolify tasks now distinguish generic Compose validity from parser-generated environment/domain/storage state;
- required external topology uses empty `${VAR:?}` expressions and must be declared in the owning service environment so the UI materializes an empty Required value;
- shared team/project/environment/server variables are the default authority for secrets and reusable credentials;
- internal service traffic stays on Docker DNS/`expose`; host `ports` are reserved for real external consumers;
- generated domains are modeled per Compose service, with separate lightweight ingress services when independent public routes share one underlying network namespace;
- editable config files use inline `content:` managed file mounts when appropriate;
- fresh-resource parser validation is required for generated env/domain/storage behavior;
- Docker Compose location is explicitly documented as relative to Coolify Base directory, with narrow repository-relative watch paths;
- provider-specific deployment manifests use `deploy/<orchestrator>/<service>/` by default instead of an ambiguous generic stack directory;
- added E-027 / B-028 for treating valid Compose as sufficient evidence of Coolify correctness.

Reason:
Repeated infrastructure work exposed the same parser-specific failures: descriptive `:?` text became a variable value, variables referenced only from ports/commands did not appear as Required in the UI, multiple generated domains on one service collapsed into one route, and managed file generation depended on Coolify-specific `content:` semantics. These are reusable deployment-contract issues rather than one project's topology.

## 2026-10 — Sticky percentage progress in reports

Changes:
- strengthened `docs/REPORTING_PROTOCOL.md` so every changed report direction has an explicit progress indicator;
- percentage reporting is now sticky once established for an active direction/workstream, including an established overall-goal percentage;
- exact counters/state transitions may supplement an established percentage but no longer silently replace it;
- when no prior percentage exists but progress is meaningfully estimable, compact reports provide a scoped scalar percentage;
- losing the previous numeric checkpoint no longer permits dropping percentages: report the current approximate percentage and mark the prior baseline unavailable;
- the same sticky percentage rule now applies to both compact and full/detailed reports;
- percentage omission is allowed only when percentage progress is materially misleading or undefined, with a brief reason;
- multi-direction reports include a scoped overall-goal percentage when a defensible aggregate exists;
- report checkpoints now preserve the percentage denominator/estimation basis;
- added E-026 / B-027 for disappearing progress percentages.

Reason:
A compact report followed the delta-report rule but omitted progress percentages because exact counters and qualitative transitions were available. The previous wording allowed that interpretation even though the active workstream expected percentage continuity. Counters are evidence; they must not erase an established progress metric.

## 2026-10 — Delta-based progress reporting contract

Changes:
- added `docs/REPORTING_PROTOCOL.md` as the single reusable authority for progress-report semantics;
- plain/compact report requests now mean delta reports against the previous report checkpoint;
- compact reports show only changed directions, scalar `before -> after` progress, unique new results, goal status and the immediate next path;
- full/detailed report requests remain comprehensive current-state snapshots and may repeat stable context;
- percentage ranges are prohibited in reports; use one stable scalar estimate, exact counters, or an evidence/state transition instead;
- long-running tasks persist enough report-checkpoint state to recover the comparison baseline without relying only on chat memory;
- added E-025 / B-026 for repetitive non-delta reporting.

Reason:
Long-running technical sessions accumulated noisy reports that repeated unchanged findings and baselines. The user had to mentally diff reports to discover what actually changed, and progress ranges made successive reports difficult to compare. The new contract makes ordinary reports delta-first while preserving a separate explicit full-report mode.

## 2026-10 — Stop repeated public research for exhausted legacy silicon

Changes:
- hardware-reverse now treats generic web/source/datasheet/SDK research as a bounded evidence path rather than a per-session startup step;
- once a project records that public research for a legacy/obscure processor or companion chip is exhausted, later agents default to target reverse instead of rerunning family-wide searches;
- external research reopens only for a new concrete artifact/identifier lead or an explicit user request;
- added E-024 / B-025 for cross-session public-research loops that displace firmware/Analysis evidence work.

Reason:
Long-running reverse projects repeatedly lost time because each fresh agent independently retried the same broad searches for old processor documentation, SDK/source code and secondary-controller material. The searches produced no authoritative target corpus, while preserved firmware and Analysis already offered the productive evidence path.

## 2026-10 — Reverse-analysis safety-block incident loop

Changes:
- behavior-analysis now treats provider/policy/safety/pre-tool blocks as infrastructure evidence rather than target evidence;
- every such block requires a narrow re-read of the current behavior-analysis terminology before the next reverse-analysis invocation;
- blocked invocations are recorded with sanitized request shape, purpose, block text, backend-reached state and alternate-path result;
- agents must reuse an analogous infrastructure issue when one exists and append each occurrence, otherwise create a new issue;
- added E-023 / B-024 so recurring safety false positives build a durable diagnostic corpus instead of disappearing in chat history.

Reason:
A read-only reverse-analysis batch request was blocked before reaching the Analysis backend while narrower individual requests remained legitimate. The immediate workaround preserved progress, but without a durable incident loop the exact blocked request would be lost and repeated provider/safety false positives would remain hard to diagnose.

## 2026-09 — Browser-first web routing with cURL fallback

Changes:
- removed explicit cURL preset selection from Reverse and Infrastructure Project prompts;
- ordinary web research now uses the built-in browser/search path first;
- Koba MCP cURL is the required fallback when browser/search is insufficient or direct HTTP/download/stream access is needed;
- preset selection is omitted unless a non-default request profile is explicitly required.

Reason:
Koba cURL now has a safe production default, so Project prompts should describe when to use cURL, not duplicate transport defaults that are already enforced by the tool.


## 2026-09 — WSL / Buildroot environment isolation

Changes:
- terminal skill now treats inherited Windows environment as a possible WSL lane contamination;
- OpenIPC porting skill now requires a Buildroot/WSL preflight using the project-defined Linux-only PATH and `hash -r`;
- added E-022 / B-023 for host environment leakage into Linux-native build lanes.

Reason:
A real OpenIPC Builder run failed before build/archive because WSL inherited Windows PATH entries including `/mnt/c/Program Files/...`; Buildroot correctly rejected PATH containing spaces. The failure was environment-boundary loss, not source failure.


## 2026-09 — Pre-send hard-constraint compliance

Changes:
- terminal skill now requires a final compliance pass before any human-operated command response;
- bootstrap protocol distinguishes “skill loaded” from “draft complies with skill”;
- account prompt now states that active hard Project/repository/skill constraints outrank response-completeness and end-to-end planning goals;
- added E-021 / B-022 for loaded-rule displacement during answer generation.

Reason:
A real failure occurred even though the terminal skill was correctly loaded and understood. While composing the answer, the agent optimized for “give the full path to finished firmware” and displaced the explicit decision-boundary rule. The missing layer was final output compliance, not context loading.


## 2026-09 — Local-contract precedence

Changes:
- terminal skill now explicitly distinguishes “not universal” from “optional”;
- project/local transport contracts override generic command defaults;
- expected-but-unavailable local contracts now block command emission instead of falling back to familiar defaults;
- generic safety wording must not reclassify a project-defined routine operation without project evidence.

Reason:
A real failure occurred after the terminal skill was correctly read: the agent saw that `scp -O` was project/local-specific, but incorrectly resolved that as permission to use generic `scp`. The failure was instruction application/precedence, not missing file loading.


## 2026-09 — Hard bootstrap and durable task context

Changes:
- added `docs/BOOTSTRAP_PROTOCOL.md` as a hard startup gate for substantial technical work;
- added `templates/TASK_CONTEXT.md` for recoverable long-running state;
- made terminal skill mandatory before any human-operated command block;
- prohibited claiming AGENTS/skill files were read without actual retrieval/injection evidence;
- added patch/delta continuity requirements so unfinished work is not stored only in chat memory;
- opened Koba MCP Bridge issue #60 for a typed `workflow_bootstrap` / workflow-context capability.

Reason:
Agents continued to violate command and context rules despite those rules existing in prompts/docs. The missing layer was observability/enforcement: “read and follow” remained a soft conversational request, and active patch state remained vulnerable to context loss.


## 2026-09 — Self-discovering bootstrap and concrete project maps

Changes:
- account prompt now links the universal workflow library and requires reading its AGENTS/README routing map for substantial technical work;
- account fallback order added for repositories without AGENTS: CLAUDE → README/contribution docs;
- Reverse Project prompt expanded from a template-like policy into a concrete map of current reverse/OpenIPC/infrastructure/reference repositories;
- Reverse Project prompt now includes representative Koba GitHub Agent/Reviewer, Ghidra, artifact and cURL operations;
- Infrastructure Project prompt now points to the real Koba MCP Bridge and Ghidra MCP repositories and their authority boundaries.

Reason:
A correct hierarchy is insufficient if a new agent does not know where the workflow library, repository map and tool surfaces actually live. Bootstrap must be discoverable from the injected account/Project prompts without relying on conversational memory.


## 2026-09 — Reverse/Infrastructure Project prompts and OpenIPC porting skill

Changes:
- added a broad Reverse Engineering Project prompt that treats ANJIA/FH8626 as the main current OpenIPC case, not the entire Reverse scope;
- added an Infrastructure Project prompt with MCP-first, service-state, permission and independent-review rules;
- added a dedicated OpenIPC porting/migration/contribution skill;
- moved OpenIPC-specific repository ownership, recovery, Builder/Firmware/Linux/streamer/U-Boot contribution discipline below the account layer;
- extended the account prompt only with universal hierarchy/AGENTS routing and primary-tool-surface behavior.

Reason:
Reverse, infrastructure and OpenIPC porting need different project/task context, while the account prompt must remain universal and portable.


Track why the agent system changed.

## 2026-09 — Account prompt: uncertainty, contradictions and autonomous progress

Changes:
- added explicit fail-closed behavior when evidence is insufficient for a required answer;
- prohibited invented certainty as a substitute for missing information;
- added contradiction handling with different behavior for planning/acceptance vs implementation;
- made autonomous continuation the default when safe/correct work can proceed;
- required milestone progress to include completed/current/remaining scope;
- constrained percentage reporting to approximate, explicitly scoped denominators;
- required recorded contradictions to be checked before DONE/COMPLETE.

Reason:
Agents sometimes continue past missing evidence by inventing a plausible solution, silently carry contradictory requirements, or interrupt autonomous work unnecessarily. The account layer now defines a clearer stop/continue boundary.

## 2026-09 — Initial consolidation

Source: multi-week hardware reverse/porting workflow audit.

Changes:
- separated account/project/task instruction layers;
- converted AGENTS into a workspace map instead of another prompt;
- separated roles from task domains;
- extracted terminal, service, software, reverse and audit skills;
- created local-context contract;
- formalized independent Reviewer;
- formalized MCP-first strategy;
- created recurring workflow-audit loop;
- moved recurring error/best-practice knowledge out of a camera-specific project.

Reason:
Dominant failures were state loss, execution-lane confusion, protocol drift, premature completion and competing authorities rather than insufficient technical reasoning.

## 2026-10 — Project-neutral engineering skill consolidation

Changes:
- expanded the software-engineering skill into conditional DDD/Python/package/PostgreSQL/observability/aiogram modules;
- added frontend-engineering with Vue/TypeScript, FSD, UI and reusable-table modules;
- added Git workflow and reusable documentation/context ownership guidance;
- added skill-authoring and context-maintenance contracts;
- expanded the Orchestrator role for multi-slice/multi-repository fan-in without overriding writer/reviewer identity separation;
- removed project-specific paths, commands, versions and temporary test policies from the generalized copies.

Reason:
A mature product workspace had accumulated reusable engineering knowledge inside a legacy shared-context tree. Keeping that knowledge there created duplicate global authority and made it unavailable to unrelated projects. The reusable parts now live in the universal workflow library; project-specific facts remain with their project owners.


## 2026-10 — Issue-state ownership and defensible coverage

Changes:
- reporting protocol now owns the distinction between editable task checkpoints,
  conversation reports and private execution/recovery artifacts;
- reverse-analysis now distinguishes discovered objects, register windows and
  semantic completion, and requires explicit aggregate scope and deduplication;
- no account prompt or project-specific runtime values were added.

Reason: repeated issue-log duplication and proxy-based percentages obscured
current tasks and made progress appear more complete than the evidence allowed.
