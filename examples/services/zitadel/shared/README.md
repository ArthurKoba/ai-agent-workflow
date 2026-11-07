# Shared-dependency ZITADEL — direct Coolify Traefik

The API and Login V2 run as UID `0` for the root-owned `zitadel-bootstrap` volume so the API can write and Login can read the Login client PAT. This is a pragmatic bootstrap compatibility trade-off for Coolify local volumes, not a production least-privilege claim. For stronger isolation implement and test a volume ownership init step; no host mounts are required.

One Compose resource owns **two containers**: ZITADEL API and Login V2. **No separate gateway, Caddy, PostgreSQL or Valkey containers.** This variant requires existing PostgreSQL/PgBouncer at `database:5432` and Valkey at `valkey:6379` on the correct private Docker network. Explicitly provision the `zitadel` database and restricted user and a dedicated `zitadel` Valkey ACL credential plus non-overlapping cache DB indexes before starting.

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

Assign **one** canonical HTTPS domain to `zitadel-api:8080` in Coolify Domains; do not assign a separate Login domain. The Coolify entrypoint declares `SERVICE_URL_ZITADEL_API_8080: /` as the route, but derives the ZITADEL issuer, public login URLs, forwarded Host and both Traefik Host rules from the **portless** `${SERVICE_FQDN_ZITADEL_API:?}`. No separate `ZITADEL_PUBLIC_DOMAIN` Resource ENV or hardcoded hostname is needed when the portless value resolves. Check the actual Deployable Compose before first boot: `SERVICE_URL_ZITADEL_API_8080` declares the route and internal port, not a ZITADEL external domain. A previous Coolify 4.5.3 deployment needed an explicit domain because its parser did not supply the generated host; do not treat this updated generic example as validated on that version.

Copy into the owning infrastructure repository. Base Directory is the service folder, Compose Location `/docker-compose.coolify.yaml`; use a service-directory Watch Paths glob such as `deploy/coolify/zitadel/**` for the matching deployment location. The **only** Coolify-generated public hostname belongs to `zitadel-api:8080` via `SERVICE_URL_ZITADEL_API_8080: /`. Two direct Traefik custom routers share `${SERVICE_FQDN_ZITADEL_API:?}`: Login V2 path `/ui/v2/login` goes to port 3000 at priority 200, other API paths go to 8080 over h2c at priority 100. No public domain is generated for Login.

Verify the actual Coolify Traefik parser, labels, proxy network membership, canonical issuer redirects and certificate resolver. Coolify can generate overlapping default routes, so inspect effective priority and route selection. Multiple instances on one proxy need unique custom Traefik router/service names; these static sample names cannot be reused unchanged. No root redirect or public diagnostic filtering is included; evaluate public endpoint exposure before production.

Use **Connect To Predefined Network** only when needed to reach the actual dependency network; verify membership and DNS from running containers. Do not infer reachability from a Coolify Destination name. The shared volume `zitadel-bootstrap` stores the first Login PAT and must be backed up with DB and master key.

This is a source-only, unvalidated integration pattern. Before production, pass all gates in `../VALIDATION.md`, including real issuer/JWKS, OIDC login/logout, gRPC API routes, caching, persistence/restore and rollback. The upstream preset does not provision shared DB/ACL roles.
