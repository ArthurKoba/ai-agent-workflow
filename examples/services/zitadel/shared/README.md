# ZITADEL with shared PostgreSQL/PgBouncer and Valkey

One Coolify Compose resource holds `zitadel-api`, `zitadel-login`, `gateway` only. PostgreSQL/PgBouncer and **Valkey must already exist** in the same environment's private network; this variant **does not disable cache** or start duplicate database/cache containers. Prefer `database:5432` for the chosen PostgreSQL/pooler endpoint and `valkey:6379` for the cache. The dependency owner must explicitly provision resources before starting ZITADEL.

## Dependency contract

| Target | Required pre-existing state |
| --- | --- |
| PostgreSQL or PgBouncer | Dedicated logical `zitadel` database and restricted application role, not the credentials/database of Infisical or VPN Core |
| `database:5432` | Direct PostgreSQL or PgBouncer with a stable alias; do not assign alias to both |
| `valkey:6379` | Working Valkey standalone endpoint, authenticated `zitadel` ACL principal, allocated **non-overlapping cache DB indexes** |
| Cache DBOffset | Default `10`, configurable by `VALKEY_DATABASE_OFFSET`; reserve the indexes actually used by ZITADEL and verify they are supported by the server's `databases` setting |

ZITADEL's `Instance`, `Milestones` and `Organization` caches all use `redis`. Its Redis URL may end in `/0`, but ZITADEL selects logical DB indexes from **DBOffset + cache purpose** and may invoke `FLUSHDB`. Protect other applications by reserving a distinct index set and, where supported, limiting its ACL user to those indexes. Sharing only different key prefixes in one Redis database is unsafe. <https://zitadel.com/docs/self-hosting/deploy/kubernetes/caching>

## Operator inputs

| Key | Default / requirement |
| --- | --- |
| `POSTGRES_USERNAME`, `POSTGRES_DATABASE` | Defaults `zitadel`, mapping to an already provisioned user and database |
| `POSTGRES_PASSWORD` | Required protected application credential; not PostgreSQL superuser |
| `VALKEY_USERNAME` | Default `zitadel`, matching a provisioned ACL principal |
| `VALKEY_PASSWORD` | Required protected ACL secret |
| `VALKEY_DATABASE_OFFSET` | Optional default `10`, must be unique for that shared Valkey |
| `ZITADEL_MASTERKEY`, `ZITADEL_ADMIN_PASSWORD`, `ZITADEL_SESSION_COOKIE_SECRET` | Required independent root-of-trust/bootstrap secrets |

In a wider Shared/Infisical namespace, secret keys must identify ZITADEL as owner (e.g. `ZITADEL_POSTGRES_PASSWORD`, `ZITADEL_VALKEY_PASSWORD`). Resource-local Compose can use short `POSTGRES_*`/`VALKEY_*` names. Use URL-safe credentials when embedding them into connection URIs; do not duplicate editable DSN/password operator inputs.

Attach this Coolify resource to the **actual predefined environment network**, with `Connect To Predefined Network` when required; verify container membership and DNS, not merely the displayed Destination. The gateway alone receives Coolify's generated HTTPS domain. Ensure its `ZITADEL_EXTERNALDOMAIN`, issuer/login routes and Login request headers resolve to the generated public origin before starting real user registration. Keep database, Valkey and bootstrap volumes under their respective owners.

Copy the variant's contents into the private infrastructure repository (`deploy/zitadel/` is an example); use `/docker-compose.coolify.yaml` and `deploy/zitadel/**` Watch Paths. See [`../VALIDATION.md`](../VALIDATION.md). A shared Valkey cache is beta in ZITADEL and demands real isolation/compatibility acceptance before production use.
