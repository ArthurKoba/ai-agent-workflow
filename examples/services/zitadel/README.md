# ZITADEL infrastructure presets

Two variants expose **one Coolify-managed HTTPS domain** through an embedded Caddy gateway. No custom Traefik labels, label-escaping switch, second Login V2 domain, or hardcoded hostname is required.

| Variant | Compose services | Dependency ownership |
| --- | --- | --- |
| `standalone/` | `postgres`, `valkey`, `zitadel-core`, `zitadel-login`, `zitadel-api` (Caddy) | Private PostgreSQL and Valkey in the same stack |
| `shared/` | `zitadel-core`, `zitadel-login`, `zitadel-api` (Caddy) | Existing private PostgreSQL/PgBouncer and Valkey |

## One public hostname, internal path routing

In Coolify configure one HTTPS domain for **`zitadel-api:8080`** with path `/`. The only public declaration in either Coolify Compose overlay is `SERVICE_URL_ZITADEL_API_8080: /` on that service. The service name `zitadel-api` refers to the public Caddy gateway; ZITADEL itself runs privately as `zitadel-core`.

- `/ui/v2/login` and `/ui/v2/login/*` are forwarded unchanged to `zitadel-login:3000`.
- Everything else, including `/ui/console`, OIDC discovery, API and gRPC, is forwarded to `zitadel-core:8080` via h2c.

Caddy runs on cleartext HTTP port 8080 behind Coolify's TLS termination. Its Caddyfile is created by the Compose command, not a separate mounted file or Coolify Files record. Only the gateway receives a public Coolify route; no extra Domain is needed for Core or Login. No Compose service publishes a host port.

ZITADEL Core receives the **portless** generated `${SERVICE_FQDN_ZITADEL_API:?}` as its external hostname, redirect origin and Login's forwarded Host. It must match the canonical domain assigned to the Caddy service; do not invent or manually set a second public domain. Preserve the same issuer once the database has been initialized.

The Caddy upstream uses h2c, but end-to-end native gRPC also requires HTTP/2 across the Coolify-to-Caddy hop. Verify native gRPC separately rather than treating HTTP 200 as full acceptance.

## Evidence and boundaries

The previous Koba installation on 2026-11-02 verified an **older direct-Traefik** configuration, not this universal Caddy preset. An Intens-specific Caddy installation has returned HTTP 200 for issuer discovery, Login V2 health and console, but real login/logout, authenticated gRPC and restore still require verification. The reusable variants remain **source-ready, not independently runtime-accepted**.

PostgreSQL/Valkey ownership, Redis cache connectors and DB offset, named PAT bootstrap volume, native ZITADEL master key and Login session secret retain their established contracts. Never copy real credentials or project-specific domains into these templates. Do not reset volumes or rotate the master key to troubleshoot routes.

See `standalone/README.md`, `shared/README.md` and `VALIDATION.md`.
