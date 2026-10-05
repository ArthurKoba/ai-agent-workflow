# Context Maintenance

Use this protocol when changing the reusable agent workflow library itself: prompts, skills, roles, routing maps, audit registries or system documentation.

## Goal

Keep the operating context cumulative without turning it into a duplicate rule tree. One meaning has one owner; adjacent files link to it.

## Problem classes

- `missing-rule` — a recurring failure has no owning rule;
- `unclear-rule` — the rule exists but its trigger/decision is ambiguous;
- `duplicate-rule` — the same meaning has multiple owners;
- `conflict-rule` — active rules require incompatible actions;
- `noisy-rule` — text does not change a decision or prevent a failure;
- `wrong-owner` — the rule belongs at another account/project/skill/role/tool layer;
- `missing-link` — the rule exists but routing cannot discover it.

## Procedure

1. Read root `AGENTS.md`, `README.md`, `docs/SYSTEM_ARCHITECTURE.md` and the owner candidates.
2. Classify the problem before editing.
3. Find the existing owner; create a new file only when no owner exists.
4. Make the smallest change that resolves the recurring decision/failure.
5. Add routing links only where an agent otherwise cannot discover the owner.
6. Remove or shorten duplicated text when ownership moves.
7. Re-read changed files and check for conflicts with account/project/skill boundaries.
8. For significant changes, require an independent Reviewer pass.

## Promotion

Do not promote one project incident directly into universal policy. Prefer:

`project/local fix → reusable skill rule → account rule only if broadly universal`

If the failure is deterministic execution/tooling rather than reasoning, prefer an MCP/tool capability instead of more prompt text.

## Project knowledge

Project architecture, business contracts, current state, paths, versions and operational values stay with the owning project/repository. This public workflow repository stores only generalized rules and patterns.

## Completion check

- changed scope has one clear owner;
- routing reaches that owner;
- no project secrets/paths/active state were copied in;
- no duplicate or conflicting rule remains;
- audit/error registries are updated only when a reusable lesson actually changed.
