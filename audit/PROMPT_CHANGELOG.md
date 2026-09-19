# Prompt / Workflow Changelog

Track why the agent system changed.

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
