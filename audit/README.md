# Workflow Audit

Purpose: learn from real agent work and improve the hierarchy without stuffing every incident into prompts.

## Sources
May include exported chats, handoffs, issue/review history, failed builds/tests, user corrections and incident notes.

Raw material stays with its source project/archive. This repository stores generalized conclusions.

## Cycle
1. collect a bounded source batch;
2. assign neutral source IDs;
3. extract agent errors, user corrections, useful workflow changes, tooling gaps and authority/role failures;
4. deduplicate by root cause;
5. update `ERROR_REGISTRY.md`, `BEST_PRACTICES.md` and `../history/EVOLUTION.md` when the operating model changed;
6. decide whether the correct fix belongs in account, project, skill, role or MCP/tooling;
7. record system changes in `PROMPT_CHANGELOG.md`;
8. independent Reviewer checks that the fix is at the correct layer.

## Cadence
Run after major phases, repeated corrections, serious incidents, before major prompt rewrites, or when enough new evidence accumulates.

Detailed project chronology is optional and belongs to the source project when useful.

## Promotion rule
One incident does not automatically become an account-level rule.

Prefer:
- project fix first;
- skill rule when domain-reusable;
- account rule only when broadly universal;
- MCP/tooling change when the core problem is deterministic execution rather than reasoning.


## Cross-project registry

Use `SOURCE_REGISTRY.md` to record which projects/history batches have already been aggregated and where their detailed chronology remains.
