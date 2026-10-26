# Standalone ZITADEL + PostgreSQL + Valkey

One Compose/Coolify resource owns **five services**: `postgres`, `valkey`, `zitadel-api`, `zitadel-login`, `gateway`. The database and cache have separate persistent Docker volumes; the Login API token is shared only between API and Login through `zitadel-bootstrap`. No database, cache or private API port is exposed on the host. Caddy routes `/ui/v2/login/*` to Login and the remaining OIDC/API requests to the h2c API backend.

## Required operator secrets

| Key | Purpose |
| --- | --- |
| `POSTGRES_PASSWORD` | PostgreSQL initial database credential, URL-safe; keep stored away from Git |
| `VALKEY_PASSWORD` | Valkey ACL password for local `default` account, URL-safe |
| `ZITADEL_MASTERKEY` | 32-character ZITADEL encryption master key, stable across upgrades |
| `ZITADEL_ADMIN_PASSWORD` | Initial ZITADEL administrator password, used during first setup |
| `ZITADEL_SESSION_COOKIE_SECRET` | Login UI session signature secret (at least 32 characters) |

`POSTGRES_USERNAME=postgres`, `POSTGRES_DATABASE=zitadel` and `ZITADEL_ADMIN_USERNAME=zitadel-admin` have Compose defaults. PostgreSQL initializes only on an empty volume; changing its ENV does not update existing roles/databases. Valkey uses its ACL file to require authentication and reserves its own cache indexes from `DBOffset=10`. The server is configured for 32 logical databases; the API is configured with all three Redis connectors enabled.

Keep master/admin/session secrets in a protected independent bootstrap authority. Generate cryptographic values on a trusted operator host; never commit them. The service itself must not depend on ZITADEL or Infisical for retrieval of secrets necessary for its own first start.

## Coolify configuration

Copy this folder to `deploy/zitadel/` of an owned infrastructure repository; set Base Directory `/deploy/zitadel`, Compose Location `/docker-compose.coolify.yaml`, Watch Paths `deploy/zitadel/**`. The public route is generated via `SERVICE_FQDN_GATEWAY_8080`, **one** gateway domain on port `8080`. The API has `ExternalSecure=true`, `ExternalPort=443` and `--tlsMode external` when Coolify terminates HTTPS. Do not invent manually populated `SITE_URL` or `ZITADEL_DOMAIN` operator keys.

The generic `docker-compose.yaml` can run under Compose with an externally supplied ingress URL and no Coolify extensions. The Coolify entrypoint uses `extends`: verify inheritance of healthchecks, mounts, service dependencies and the top-level `postgres-data`, `valkey-data`, `zitadel-bootstrap` volumes. The tracked `Caddyfile` requires support for repository files (`Preserve repository` on releases that need it); a parser treating it as a directory must be fixed before deployment.

See [`../VALIDATION.md`](../VALIDATION.md) before production use. ZITADEL cache acceleration remains beta; confirm that Valkey is actually used, not merely running alongside the API. Do not deploy over an existing identity database without a separately approved migration.
