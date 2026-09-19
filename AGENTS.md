# AGENTS.md

This repository is the authority for reusable AI engineering workflow rules.

## Startup

Before changing workflow rules, read:

1. `README.md`
2. `prompts/BASE_PROMPT.md`
3. `context/LOCAL_CONTEXT_CONTRACT.md`
4. `roles/ROLE_MODEL.md`
5. the relevant file under `workflows/`

## Scope

Keep this repository project-neutral.

Do not add:
- project-specific IPs, hostnames, absolute local paths or temporary target state;
- credentials/tokens/private keys;
- hardware-specific facts that only apply to one product;
- active state/tasks from another repository.

Generalize a lesson before adding it here.

## Change discipline

- Prefer editing the existing rule over adding a duplicate.
- Keep account-level rules short.
- Put domain-specific behavior in a workflow module, not in the account prompt.
- Do not turn one incident into a universal rule without a clear reusable rationale.
- If a rule depends on local machine state, put the contract in `context/` and the actual value outside tracked Git.
- Significant changes require an independent Reviewer pass according to `roles/ROLE_MODEL.md`.

## Validation

A workflow change is complete only when:
- the affected documents agree with each other;
- the rule has a clear layer: account / base / role / context / module;
- no project-specific secrets or transient values leaked into the universal layer;
- Reviewer findings are resolved or explicitly documented.
