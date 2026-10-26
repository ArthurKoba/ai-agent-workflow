# Coolify / Docker Compose Contract

**Mandatory when Coolify parses, owns or deploys Docker Compose.** This is a parser/runtime contract, not generic Docker Compose documentation: valid Compose YAML can still generate incorrect ENV, routes, storage or managed files in Coolify.

Load additional modules **when their condition applies**:
- Creating/changing resource ENV, Required/default flags or names → `coolify-variables.md`; deciding whether ENV belongs at deployment time → `environment-policy.md`.
- Shared or secret-manager references, secret permissions → `coolify-secrets.md`.
- Cross-resource networks, ingress routes or managed domains → `coolify-networking.md`.
- Managed configuration files, storage and telemetry collector → `coolify-files.md`.
- Existing resource migration, stale parser state or persistent-volume changes → `coolify-migrations.md`.
- Fresh parser/deploy/acceptance checks → `coolify-validation.md`.
- Git folders and Watch Paths → `deployment-layout.md` and `git-backed-infrastructure.md`.

The standard produces a generic `docker-compose.yaml` and a `docker-compose.coolify.yaml` entrypoint, both with four-letter `.yaml`. Do not assume Coolify merges them. `extends`, `include` and multi-file merging are separate Compose mechanisms; verify the exact deployed Coolify parser and full resolved topology before adopting one. If parser materialization cannot be demonstrated, record the blocker; do not silently duplicate or abandon the base Compose contract.

## Authority

Keep these layers distinct:

1. **Git Compose** — desired topology, non-secret defaults, parser directives, shared-variable references and managed-file templates.
2. **Coolify** — resolved runtime variables, shared-variable values, domains/certificates, parsed persistent storage and deployment lifecycle.
3. **Container runtime** — actual containers, networks, volumes and mounted files.
4. **Acceptance** — real service behavior.

When parser behavior matters, inspect the deployed Coolify version's parser/source instead of assuming generic Compose behavior.

## Mandatory deployment contract

- **Unrequested changes require prior approval.** Do not edit, rename, add, remove, migrate, deploy or otherwise change anything beyond the user's explicit request. If an extra change seems necessary or beneficial, first state the exact proposed change and wait for explicit authorization. Neither conventions, best practices, nor a broad request to proceed imply consent.
- **Get explicit user approval of the complete operator-variable contract** before adding, renaming, aliasing or removing keys: exact names, purpose, Required/Default semantics, owner and secret scope. Never infer approval from a general implementation request.
- Prefer existing approved or upstream names. Do not invent prefixes, duplicate credentials, intermediary aliases or new privileged identities for convenience.
- Keep a single canonical Compose owner and only justified orchestrator overrides. Ensure every effective deployment input is tracked by Watch Paths; verify inheritance in the actual parser.
- Treat generated domains, Shared references and parser-managed variables as runtime state. Verify the resulting application configuration and reconcile stale entries before declaring changes complete.
- Preserve data, privilege boundaries and existing deployments. Distinguish source validation from parser, deployment and real-consumer acceptance; never use a speculative redeploy to settle an unresolved contract.
