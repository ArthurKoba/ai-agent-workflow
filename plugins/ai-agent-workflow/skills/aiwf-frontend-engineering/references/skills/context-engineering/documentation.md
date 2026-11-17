# Documentation ownership and maps

## Documentation ownership

Documentation must not become a second implementation.

### Code owns implementation detail

Source code is the authority for:

- concrete functions/classes/modules;
- internal call flow;
- exact implementation structure;
- current private helpers;
- low-level algorithm details;
- line-by-line behavior that can be recovered cheaply from the source.

Do not duplicate these details into a giant current-state document merely so an agent can preload them. The agent should navigate to the relevant source and read it when the task requires it.

### Documentation owns durable contracts and navigation

Documentation is justified when it carries information that cannot be recovered safely or cheaply from one local code read, for example:

- system/product boundaries;
- cross-repository contracts;
- public API/transport/data contracts;
- domain invariants and terminology;
- architectural ownership decisions;
- operational/release/recovery contracts;
- unresolved contradictions, gates and accepted future requirements;
- a compact map from capability/domain to the code/document owner.

### One meaning, one owner

Do not maintain equivalent implementation truth in both source and narrative documentation.

If a fact changes whenever the implementation changes and can be observed directly from code, prefer a navigation pointer over a duplicated description.

If several applications need the same contract, give that contract one shared authority instead of copying it into each application repository.

## Repository documentation shape

### AGENTS.md is a router

`AGENTS.md` should answer only the startup/navigation questions:

- what repository/project is this;
- what authorities matter;
- which task skill applies;
- what minimal project map/status file should be read;
- where shared contracts live;
- which repository-specific policies can change agent decisions.

It should not contain a complete architecture manual, coding style handbook, implementation history or duplicated universal skill text.

### Project/application map is a map

A project map should optimize navigation, not describe the codebase exhaustively.

Good map entries look like:

```text
authentication -> src/domain/auth + src/application/auth + HTTP auth contract
finance -> src/domain/finance + src/application/finance + shared finance contract
subscription UI -> src/entities/subscription + relevant feature/widget entry points
deployment -> operations/deployment.md
```

The map tells the agent where to jump. The source then explains how the implementation works.

Do not turn the map into a catalog of every class, worker, DTO, repository method, event or database model.

### Shared system authority

When backend, frontend, workers or other applications must agree on the same behavior, put the shared meaning in one neutral project authority selected by the Project architecture.

Typical shared material:

- product/system capabilities and boundaries;
- backend/frontend integration contracts;
- public API semantics;
- shared domain vocabulary;
- cross-application workflows;
- common acceptance/release contracts;
- system-level decisions that neither application owns alone.

Backend/frontend repositories should link to that shared owner and keep only their local implementation map, local constraints and local state.

## Work tracking

Unfinished work, defects, acceptance gaps and follow-up tasks belong in the repository's issue/work-item tracker when one is available.

Do not maintain Markdown roadmaps, backlog files or open-question lists as a parallel planning database. Documentation may define durable acceptance criteria or product semantics; Issues/Work Items own task lifecycle, priority, assignee, discussion and closure evidence.

A documentation page may link to an issue, but it must not copy the mutable task state back into prose. Conditional future options should become issues only when they are actually activated.
