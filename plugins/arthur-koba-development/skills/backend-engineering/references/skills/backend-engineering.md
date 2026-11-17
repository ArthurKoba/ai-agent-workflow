# Backend Engineering

Use for backend applications, services, runtime boundaries, persistence,
APIs, observability, refactoring and implementation **in any language**,
including Rust, Python, Go and others. Do not assume Python is the
language or that framework/database-specific techniques apply.

Read the [canonical implementation workflow](software-engineering/README.md)
first. Use its language-independent development, validation and recovery
requirements. Load only its conditional modules when the target actually
uses the relevant language, database or framework: Python, PostgreSQL,
aiogram-dialog, etc. Do not load Python modules for Rust work merely because
they exist in the library.

For architecture-heavy tasks, use [Software Architecture](software-architecture.md).
Repository-owned rules, real code/toolchain, and tests take precedence
over examples from another language. No runtime, compiler or provider
is a prerequisite for this Skill.
