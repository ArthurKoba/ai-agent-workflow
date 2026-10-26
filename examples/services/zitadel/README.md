# ZITADEL infrastructure presets

Two **alternative** Git-backed Compose patterns with **Valkey caching enabled**. Both use a dedicated ZITADEL API, Login UI, private Caddy h2c/path router, and one Coolify-managed public domain. These are source-level presets, **not yet runtime-validated** on the target Coolify release.

| Variant | Services in the deployment | Dependencies |
| --- | --- | --- |
| [`standalone/`](standalone/README.md) | ZITADEL API + Login + Caddy, **own PostgreSQL and Valkey** | Isolated volumes and private network |
| [`shared/`](shared/README.md) | ZITADEL API + Login + Caddy | Existing private PostgreSQL/PgBouncer **and Valkey**, with distinct ZITADEL credentials and cache DB indexes |

Valkey is not decorative: `ZITADEL_CACHES_CONNECTORS_REDIS_ENABLED=true` and the `Instance`, `Milestones`, `Organization` cache connectors all point to the configured Redis-compatible Valkey. The setting `DBOffset` isolates cache database indices. ZITADEL ignores the database number in the `/0` URL path; it may issue `FLUSHDB`, so never share those indexes with Infisical, VPN Core or other consumers. Dedicated ACL credentials alone do **not** isolate indexes. The Redis/Valkey cache connector is currently **beta** and must be tested under load, restart and cache failure. <https://zitadel.com/docs/self-hosting/manage/cache>

## Domain and routing

Coolify owns the public HTTPS route to the **gateway**, not the private API/Login services. The gateway uses Caddy with HTTP/2 cleartext (`h2c`) upstream to the API, and normal HTTP to Login V2. The Coolify entrypoint uses a generated `SERVICE_FQDN_GATEWAY_8080` as the external hostname and derives its HTTPS login/issuer URLs from that hostname. No manually configured public domain key should be introduced just to duplicate Coolify.

**Parser gate:** some Coolify releases may expand `${SERVICE_FQDN_*}` before its managed value exists. Verify the effective `ZITADEL_EXTERNALDOMAIN`, Login `CUSTOM_REQUEST_HEADERS`, and issuer/login URLs **inside the actual resource**. Stop if blank or mismatched; don't silently fall back to a hardcoded Git hostname. The generic Compose requires explicitly supplied URLs for any real public deployment, with localhost-only defaults for local tests.

## Trust and upgrades

Infisical and ZITADEL are separate root-of-trust services. Keep ZITADEL master key, initial admin password, login session cookie secret and database/Valkey credentials in an **independent bootstrap/recovery authority**, never in Infisical if that creates a startup dependency cycle. Copy the chosen variant's contents into the *owning infrastructure repository*, pin its revision, then configure Coolify to watch that copy—not this public repository's moving HEAD.

Shared PostgreSQL is **one server**, not one logical application database: ZITADEL needs its own role/database. Shared Valkey is one server with separately assigned indexes and ACLs. Production and dev ZITADEL instances must not share signing keys, identity databases or live user identities merely because they use the same Compose preset.

For implementation, read the variant README and [`VALIDATION.md`](VALIDATION.md). This repository does not contain a running ZITADEL resource or private server topology.
