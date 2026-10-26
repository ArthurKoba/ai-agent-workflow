# Deployment Variable Glossary

Load **when creating operator/Shared/secret keys, checking naming collisions or proposing ENV renames**; not required for ordinary deployment of an already approved contract. This file owns the names below. OpenTelemetry-specific keys → `telemetry-variables.md`. Parser semantics → `coolify-variables.md`; whether a setting needs ENV → `environment-policy.md`; protection and scopes → `coolify-secrets.md`. The operator approves new keys and migrations before any resource change.

## Naming and scope

- Our new operator keys use upper `SNAKE_CASE`, full purpose words (`USERNAME`, `PASSWORD`, `DATABASE`), not `USER`, `PWD`, `DB`. Upstream image/SDK keys remain unchanged; translate at the Compose or application boundary. Keep one approved key per meaning and scope, without gratuitous aliases.
- Inside a single-resource/single-consumer context, use short names such as `POSTGRES_USERNAME`; the Coolify Resource already identifies the owner. With multiple consumers/identities **within a resource**, or in Shared/Secret Manager scopes spanning resources, prefix the actual owning service: `ZITADEL_POSTGRES_PASSWORD`, `BACKEND_POSTGRES_PASSWORD`. Never publish ambiguous unqualified `POSTGRES_PASSWORD` in a shared namespace.
- Prefer native Team/Project/Environment/Server scopes to encoding `DEV`/`PROD` in names. Add deployment-environment prefixes/suffixes only when the store cannot separate the values and collision would otherwise occur. A shared key's owner is the *principal or system it configures*, not always the container consuming it.
- For every candidate state purpose, owner/consumer, external input vs derived constant, scope, Required/default, secret status and upstream mapping. Use an existing approved name first. On mismatch **report a proposed mapping/rename; do not mutate live keys or rotate secrets** as part of unrelated work.

## PostgreSQL — one resource, one database context

| Operator key | Coolify contract | Upstream input | Decision |
| --- | --- | --- | --- |
| `POSTGRES_USERNAME` | `${POSTGRES_USERNAME:-postgres}` | `POSTGRES_USER` | Exposed default `postgres`, editable when useful |
| `POSTGRES_PASSWORD` | `${POSTGRES_PASSWORD:?}` | `POSTGRES_PASSWORD` | Required, empty until secret reference is set |
| `POSTGRES_DATABASE` | `${POSTGRES_DATABASE:-postgres}` | `POSTGRES_DB` | Exposed default `postgres` **by agreement**, not literal-only |

Example of mapping the approved operator keys to the image interface:

```yaml
services:
  postgres:
    environment:
      POSTGRES_USER: ${POSTGRES_USERNAME:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?}
      POSTGRES_DB: ${POSTGRES_DATABASE:-postgres}
```

`POSTGRES_USER` in the official image creates an initial superuser (not an automatically least-privileged app user). These initialization variables act on a fresh data directory, not as automatic migrations of existing users/databases. Keep the minimum viable single-role bootstrap when explicitly accepted; separate service accounts only when the architecture calls for isolation. Do not force account proliferation on a small deployment.

When the **administrator identity is explicitly separated**, `POSTGRES_SUPERUSER_PASSWORD` identifies that privilege and may map to the upstream initial `POSTGRES_PASSWORD`. Do not expose *both* names for the **same** secret without an approved reason. The administrator username may remain literal `postgres`; qualify an admin key with the owning instance if a wider Shared scope contains several PostgreSQL instances.

## PostgreSQL — multiple consumer principals or wider Shared scope

| Scoped key pattern | Purpose | Placement |
| --- | --- | --- |
| `ZITADEL_POSTGRES_USERNAME` / `ZITADEL_POSTGRES_PASSWORD` | ZITADEL database login | Shared/secret provider when used across resources; owner `ZITADEL` |
| `BACKEND_POSTGRES_USERNAME` / `BACKEND_POSTGRES_PASSWORD` | Backend database login | Separate principal if provisioned |
| `PLATFORM_POSTGRES_USERNAME` / `PLATFORM_POSTGRES_PASSWORD` | Deliberately shared platform login | Only when shared privileges were explicitly accepted |
| `<OWNER>_POSTGRES_DATABASE` | Database owned by that consumer | Default may be in Compose; create ENV only when an override is needed |

The prefix is **conditional**, not mandatory inside a single isolated Postgres resource. Keys alone do not create database roles; bootstrap owns creation, privileges and migrations.

## Other frequently encountered dependencies — not yet canonical

| Integration | Existing upstream/project input | Status |
| --- | --- | --- |
| Valkey auth | `VALKEYCLI_AUTH` / project `VALKEY_PASSWORD` | Mapping example; name not yet approved universally |
| ZITADEL first admin | `ZITADEL_FIRSTINSTANCE_ORG_HUMAN_USERNAME` | Bootstrap-specific; project name not yet canonical |
| OAuth signing | Provider-specific | No generic signing-secret key approved |

Other names need an owner/scope/Required mapping and separate approval.
