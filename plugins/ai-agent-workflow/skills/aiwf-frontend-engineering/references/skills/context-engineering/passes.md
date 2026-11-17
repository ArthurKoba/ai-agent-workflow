# Focused engineering passes

## Implementation and refactoring are different passes

Do not force one agent/pass to optimize every quality dimension at once.

For substantial work, a high-throughput workflow may intentionally separate:

### 1. Functional implementation pass

Objective: make the required behavior real and integrate it with the existing system.

Load:

- task/product contract;
- local source around the change;
- only architectural/safety rules required for correctness.

Do not preload unrelated style/refactor checklists.

### 2. Architecture pass

Objective: verify boundaries, ownership, dependency direction, domain/application/infrastructure placement and lifecycle decisions.

Load the architecture-specific skill modules and inspect the integrated implementation.

### 3. Module/package/import pass

Objective: verify public APIs, encapsulation, file/module ownership, imports, dependency edges and package layout.

Load package/module rules, not unrelated database/UI material.

### 4. Consistency/duplication pass

Objective: identify repeated behavior, parallel contracts, redundant adapters/helpers and inconsistent naming/ownership.

Focus on the relevant code slice plus cross-references.

### 5. API/contract pass

Objective: verify public HTTP/event/provider/data contracts, compatibility and backend/frontend agreement.

Load only contract authorities and the affected adapters/consumers.

### 6. Persistence/concurrency/performance pass

Objective: verify database invariants, transaction boundaries, query shape, locks, indexes and measured performance risks.

Load database-specific modules only when persistence is in scope.

### 7. Code-quality/style/tooling pass

Objective: run targeted linters/type checks/static diagnostics and clean style/typing/import issues after behavior and architecture have stabilized.

This is the right pass for detailed language/style rules that would otherwise consume implementation context without changing the main design decision.

Additional passes such as security, observability, accessibility, deployment or hardware acceptance should be added when the product risk requires them.

## Координация проходов

Назначения, совмещение функций, передача версий и приёмка определяются [скиллом оркестрации](../orchestration/README.md). Каждый проход получает одну цель, ограниченный scope, нужные источники/скиллы, точную версию и ожидаемые свидетельства. Не загружай специалисту весь корпус проекта. Общая приёмка относится к одной интегрированной версии.
