# Software Architecture

Use for service decomposition, bounded contexts, modular monoliths, domain
models, clean architecture, contracts, dependency direction, ownership and
architecture review **independent of language**. Rust, Python, Go, JavaScript
and other implementations must be judged by the same evidence-based
architecture goals, not by one language's example.

Read [Clean Architecture and DDD](software-engineering/clean-architecture-ddd.md)
only for the architecture concerns present in the task. That document
is the single source for shared architecture methods; do not duplicate
its rules here or infer required Python, ORM or framework adoption from
an example. Discover actual project boundaries, interfaces and existing
code before recommending restructuring.

For creating a new repository, toolchain, quality gates or CI, combine
this Skill with the separately installed Project Bootstrap Skill when
available. For backend implementation use Backend Engineering; for
frontend implementation use Frontend Engineering. Do not require
other skills merely to evaluate an architecture.
