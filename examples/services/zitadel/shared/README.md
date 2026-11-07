# Shared-dependency ZITADEL — Caddy single-domain ingress

The API and Login V2 run as UID `0` for the root-owned `zitadel-bootstrap` volume so the API can write and Login can read the Login client PAT. This is a pragmatic bootstrap compatibility trade-off for Coolify local volumes, not a production least-privilege claim. For stronger isolation implement and test a volume ownership init step; no host mounts are required.

One Compose resource owns **three containers**: ZITADEL Core, Login V2 and the Caddy public gateway (`zitadel-api`). There is no embedded PostgreSQL or Valkey; existing private dependencies must be reachable at `database:5432` and `valkey:6379`. Provision the restricted `zitadel` PostgreSQL database/user and dedicated Valkey ACL, with non-overlapping cache DBOffset indexes, before first launch. The named `zitadel-bootstrap` PAT volume belongs to Core and Login; Caddy needs no protected secret or persistent storage.

## Operator inputs

| Key | Contract |
| --- | --- |
| `POSTGRES_USERNAME`, `POSTGRES_DATABASE` | Defaults `zitadel`, provisioned by database owner |
| `POSTGRES_PASSWORD` | Required ZITADEL app credential, not superuser |
| `VALKEY_USERNAME` | Default `zitadel`, provisioned ACL principal |
| `VALKEY_PASSWORD` | Required protected Valkey credential |
| `VALKEY_DATABASE_OFFSET` | Defaults `10`; reserve all actual cache purpose indexes |
| `ZITADEL_MASTERKEY` | Exactly 32 ASCII characters; back up independently |
| `ZITADEL_ADMIN_PASSWORD` | Initial administrator secret |
| `ZITADEL_SESSION_COOKIE_SECRET` | Stable Login V2 cookie secret |

Keep wide Shared secret names qualified by their actual service owner (`ZITADEL_POSTGRES_PASSWORD`, `ZITADEL_VALKEY_PASSWORD`). Never reuse another product's live identity/database or Valkey index. ZITADEL may call `FLUSHDB` on selected cache indexes, and the Redis URL `/0` is not DB selection. Cache connector remains beta.

## Coolify routing

Configure **one** HTTPS domain on `zitadel-api:8080` with path `/`. The gateway is Caddy, with exactly one magic route `SERVICE_URL_ZITADEL_API_8080: /`. Core and Login are internal services, with no separate Domains or hand-written Traefik labels and no label-escaping or path-preservation toggle.

The embedded Caddyfile forwards `/ui/v2/login` and descendants unchanged to Login V2 on 3000 and all remaining requests over h2c to Core on 8080. `SERVICE_FQDN_ZITADEL_API` without scheme/port must resolve to the domain configured on the gateway; Core uses this as its issuer hostname and Login uses it as forwarded Host. There are no hardcoded public domains in the example.

Set Base Directory to the service folder, Compose Location to `/docker-compose.coolify.yaml`, and Watch Paths to both source Compose files. Verify Coolify's parsed URL, generated FQDN, services and volumes. Although Caddy uses h2c to Core, authenticated native gRPC must also be checked through Coolify's external HTTP/2 ingress. This variant has **not** been runtime deployed.

Use **Connect To Predefined Network** only when needed to reach the actual dependency network; verify membership and DNS from running containers. Do not infer reachability from a Coolify Destination name. The shared volume `zitadel-bootstrap` stores the first Login PAT and must be backed up with DB and master key.

This is a source-only, unvalidated integration pattern. Before production, pass all gates in `../VALIDATION.md`, including real issuer/JWKS, OIDC login/logout, gRPC API routes, caching, persistence/restore and rollback. The upstream preset does not provision shared DB/ACL roles.
