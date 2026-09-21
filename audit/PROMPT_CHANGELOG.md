# Prompt / Workflow Changelog

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
