# Standalone ZITADEL — direct Coolify Traefik

Both API and Login V2 run as UID `0` for the root-owned Docker local named `zitadel-bootstrap` volume: the API must write a bootstrap PAT, and Login must read it. Live Coolify v4.5.3 testing showed `permission denied` with the default `zitadel` image user and partially persisted bootstrap rows after retry. This is a privilege trade-off; improve to a tested least-privilege volume-ownership init pattern before production. An already-partial initial setup may require a backed-up, scoped logical DB recovery; do not blindly delete unique constraints. No host filesystem mounts or host ports are added.

One Compose resource owns **four containers**: PostgreSQL, Valkey, ZITADEL API and Login V2. There is no gateway container and no Caddyfile. PostgreSQL/Valkey have persistent `postgres-data` and `valkey-data` volumes; Login client PAT is in `zitadel-bootstrap` shared between API and Login. Neither PostgreSQL nor Valkey nor the API/Login publishes host ports. The ZITADEL API must use the **`postgres:5432` Compose service hostname**, not a custom `database` alias attached to only one network; this was confirmed in Coolify v4.5.3 when API and PostgreSQL were on a generated resource network that did not carry the custom alias.

## Secrets and defaults

| Required secret | Role |
| --- | --- |
| `POSTGRES_PASSWORD` | Own PostgreSQL initial user (URL-safe) |
| `VALKEY_PASSWORD` | Own default Valkey ACL user (URL-safe) |
| `ZITADEL_MASTERKEY` | Exactly 32 ASCII characters, stable across upgrades and DB restores |
| `ZITADEL_ADMIN_PASSWORD` | First administrator password |
| `ZITADEL_SESSION_COOKIE_SECRET` | Login V2 cookie-signing secret (at least 32 characters) |

Standalone fixes PostgreSQL role `postgres` and database `zitadel` as Compose literals; `POSTGRES_USERNAME` and `POSTGRES_DATABASE` are **not** operator variables. The ZITADEL admin username defaults to `zitadel-admin`. PostgreSQL initial `POSTGRES_PASSWORD` applies only to an empty data volume; changing it later does not rotate credentials or migrate roles. Shared-dependency ZITADEL retains independent PostgreSQL user/database configuration.

Generate secrets on a trusted operator host and store them in appropriately protected Shared Variables or an independently backed up secret manager. Do not commit real `.env` values. Avoid bootstrap cyclic dependency on ZITADEL or Infisical.

## Coolify setup

Assign **one** canonical HTTPS domain to `zitadel-api:8080` in Coolify Domains; do not assign a separate Login domain. The Coolify entrypoint declares `SERVICE_FQDN_ZITADEL_API_8080: /` as the route, but derives the ZITADEL issuer, public login URLs, forwarded Host and both Traefik Host rules from the **portless** `${SERVICE_FQDN_ZITADEL_API:?}`. No separate `ZITADEL_PUBLIC_DOMAIN` Resource ENV or hardcoded hostname is needed when the portless value resolves. Check the actual Deployable Compose before first boot: `SERVICE_FQDN_ZITADEL_API_8080` may contain `host:8080`, which is not a valid ZITADEL external domain. A previous Coolify 4.5.3 deployment needed an explicit domain because its parser did not supply the generated host; do not treat this updated generic example as validated on that version.

Copy the directory into the actual infrastructure repository. Use Base Directory equal to that directory, Compose Location `/docker-compose.coolify.yaml`, and Watch Paths `deploy/coolify/zitadel/**` in a deployment located at that path (including future service inputs). Connect to the actual Coolify proxy / per-resource network. Choose a single public HTTPS domain for **`zitadel-api:8080`**, via `SERVICE_FQDN_ZITADEL_API_8080: /`; set no Login domain. Login's custom router shares the API hostname and routes `/ui/v2/login` to port 3000. The API custom router speaks h2c to 8080. Both routers use the target proxy's `https` entrypoint and its configured `letsencrypt` resolver; validate the actual proxy naming and TLS configuration before use.

Coolify may generate an additional HTTPS/HTTP route for the domain; the custom routers' priorities must win. Verify that Login is reachable on the proxy's Docker network despite having no separately generated public domain. Validate `ZITADEL_EXTERNALDOMAIN`, Login `CUSTOM_REQUEST_HEADERS`, the discovery issuer and all OIDC/SAML login redirects against the **same** canonical generated hostname.

Custom router names are static in this source example: multiple deployments sharing a Traefik Docker provider require unique names or an isolated proxy to avoid collisions. A generic Compose invocation without Coolify needs an external ingress that does the same path and h2c routing. The public API has no root redirect and no diagnostics filtering by default; evaluate the exposed endpoints before production.

## Acceptance / recovery

Check generic Compose structure, Coolify actual parser-generated ENV, labels, services and volumes; no stale `SERVICE_FQDN_GATEWAY_8080` or inherited Caddy mounts; TLS, OIDC discovery/JWKS, Login V2, gRPC API, real login/logout, repeat deploy, backup/restore of PostgreSQL/bootstrap PAT/master key. Verify `DBOffset=10` caching behavior, cold restart and Valkey cache failure. Full test matrix in `../VALIDATION.md`. **Not runtime validated.**
