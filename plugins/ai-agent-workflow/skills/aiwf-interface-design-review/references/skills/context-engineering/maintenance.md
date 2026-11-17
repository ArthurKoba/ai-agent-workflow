# Documentation synchronization and acceptance

## Documentation synchronization after changes

Update documentation when the change modifies durable meaning, not whenever source lines change.

Usually update docs when changing:

- public/system contracts;
- domain invariants;
- ownership/boundaries;
- project/application maps;
- operational/release procedures;
- architectural decisions;
- known blockers/acceptance gates.

Usually do not update narrative docs for:

- private helper refactors;
- implementation-only class/function movement already discoverable from the map/source;
- formatting/type cleanup;
- internal call-flow changes that do not alter a durable contract.

## Backend/frontend synchronization

Backend and frontend should not synchronize by maintaining two large prose descriptions of each other.

Prefer:

```text
shared contract authority
        ↓
backend local implementation map
        ↓
backend source

shared contract authority
        ↓
frontend local implementation map
        ↓
frontend source
```

The shared contract defines what must agree. Each application map says where its side is implemented. The code supplies the implementation detail.

## Anti-patterns

Avoid:

- mandatory reading lists that load most of the project before every task;
- giant `current-state.md` files that mirror implementation details;
- architecture documents that enumerate every class/method/model;
- duplicating backend behavior inside frontend docs or vice versa;
- universal style/linter rules in the startup path for every implementation task;
- one mega-agent expected to implement, architecturally refactor, style-clean, performance-tune and review everything in one context;
- multiple documents that claim authority over the same current behavior;
- documentation that must be updated line-for-line with ordinary refactors.

## Audit questions

When refactoring an existing project's documentation/context system, ask:

1. What must every agent know before any substantial task?
2. What can be discovered from code on demand?
3. Which contracts are shared across applications and need one neutral owner?
4. Which current documents duplicate implementation detail?
5. Which mandatory files can become conditional modules?
6. Can the project map route from capability/domain to source in a few lines?
7. Are backend/frontend synchronized through shared contracts rather than duplicated prose?
8. Can implementation and later quality/refactor passes use separate context sets?
9. Is every rule loaded because it protects a decision in the current pass?
10. Does any documentation owner compete with the source code for implementation truth?

## Completion criteria

A context/documentation refactor is successful when:

- startup context is small and stable;
- shared contracts have one owner;
- application maps are compact navigation surfaces;
- source code remains the implementation authority;
- task rules are loaded just in time;
- specialized passes can work from isolated context without rediscovering the whole system;
- documentation still preserves durable product/architecture/operational knowledge;
- removing duplicated narrative detail does not remove any contract, invariant, decision or acceptance gate that cannot be recovered from code alone.
