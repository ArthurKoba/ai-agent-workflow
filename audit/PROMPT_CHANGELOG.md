# Prompt / Workflow Changelog

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
