# AI Agent Workflow

Personal engineering workflow for AI agents.

This repository stores **project-neutral** rules and reusable workflow contracts. It is intentionally separate from individual hardware/software projects.

## Start here

1. [AGENTS.md](AGENTS.md)
2. [Base prompt](prompts/BASE_PROMPT.md)
3. [Account-level prompt](prompts/ACCOUNT_PROMPT.md)
4. [Local context contract](context/LOCAL_CONTEXT_CONTRACT.md)
5. [Role model](roles/ROLE_MODEL.md)
6. Relevant workflow modules under `workflows/`

## What belongs here

- universal agent behavior;
- engineering state/validation rules;
- Implementer / Reviewer / Orchestrator responsibilities;
- reusable workflow modules;
- local-context templates;
- generalized lessons that apply across projects.

## What does not belong here

- project-specific IP addresses or paths;
- credentials/secrets;
- camera/board GPIO maps;
- temporary branch SHAs;
- one project’s current state/tasks;
- generated binaries or evidence blobs;
- project-specific chronology.

Those belong in the relevant project repository, local context, or dedicated infrastructure/evidence storage.

## Status

The repository is being bootstrapped from a long-running hardware reverse/porting workflow audit. The imported rules are **working canonical**, not frozen forever. Changes should remain small, reviewable and justified by concrete engineering failures or improvements.
