# Standalone ZITADEL — Caddy single-domain ingress

Both API and Login V2 run as UID `0` for the root-owned Docker local named `zitadel-bootstrap` volume: the API must write a bootstrap PAT, and Login must read it. Live Coolify v4.5.3 testing showed `permission denied` with the default `zitadel` image user and partially persisted bootstrap rows after retry. This is a privilege trade-off; improve to a tested least-privilege volume-ownership init pattern before production. An already-partial initial setup may require a backed-up, scoped logical DB recovery; do not blindly delete unique constraints. No host filesystem mounts or host ports are added.

One Compose resource owns **five containers**: PostgreSQL, Valkey, ZITADEL Core, Login V2 and the Caddy public gateway (`zitadel-api`). The ZITADEL process is internal `zitadel-core:8080`, while Login V2 stays at `zitadel-login:3000`. The original `postgres-data`, `valkey-data` and shared `zitadel-bootstrap` PAT volumes are preserved. Only the gateway receives a public Coolify route; no host port is published. Core must reach PostgreSQL at the `postgres:5432` Compose service hostname, not an alias present only on another Docker network.

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

Copy both Compose files into the owning repository. In Coolify use the service directory as Base Directory, `/docker-compose.coolify.yaml` as Compose Location, and Watch Paths covering both Compose files.

Configure **one** HTTPS domain on `zitadel-api:8080` with path `/`. This is the Caddy gateway service; `SERVICE_URL_ZITADEL_API_8080: /` is its only public magic route. Do not assign domains to `zitadel-core` or `zitadel-login`, add Traefik labels, change label escaping, or configure manual path rewriting. No project hostname is hardcoded in the example.

The inline Caddyfile routes `/ui/v2/login` and all child paths unchanged to Login V2 on 3000. All other paths reach ZITADEL Core over h2c on 8080. Coolify terminates HTTPS; `SERVICE_FQDN_ZITADEL_API` must resolve to the canonical bare hostname used by Core's `ZITADEL_EXTERNALDOMAIN`, the public Login V2 URLs and forwarded Host. Confirm this before the first instance initializes.

The standalone base Compose retains its non-Coolify public-origin defaults; if deploying without Coolify, supply a suitable external TLS ingress and explicit canonical hostname. On an existing instance, preserve the current issuer, master key, database and PAT volume. Caddy uses h2c upstream but authenticated native gRPC still requires the outer proxy to preserve HTTP/2.

## Telemetry inputs

The **base Compose** supports native ZITADEL Core traces, metrics and logs. Optional `OTEL_ENDPOINT` is a receiver **host:port**; set `ZITADEL_INSTRUMENTATION_TRACE_EXPORTER_TYPE`, `ZITADEL_INSTRUMENTATION_METRIC_EXPORTER_TYPE` and/or `ZITADEL_INSTRUMENTATION_LOG_EXPORTER_TYPE` to `http` (OTLP/HTTP) or `grpc`. Their default `none` leaves remote export off until a collector is configured. Transport defaults to TLS; the matching native `*_INSECURE` inputs permit approved private cleartext transport. A protected `OTEL_EXPORTER_OTLP_HEADERS` input supports receivers requiring auth. `OTEL_RESOURCE_ATTRIBUTES` can identify the environment; do not copy real endpoint or token values into the generic source. JSON stderr logs remain available without remote export. Login V2 logs require collection from its own container.

## Acceptance / recovery

Verify all five services, the one generated public domain, both Caddy upstreams and the named volumes. Confirm OIDC discovery, JWKS, `/ui/v2/login/healthy` and `/ui/console/` on the single public hostname, then exercise actual OIDC login/logout and authenticated native gRPC. Verify Redis DBOffset behavior, restart and recovery with PostgreSQL/bootstrap PAT/master key backups. Full checklist in `../VALIDATION.md`. **Generic preset runtime acceptance remains open.**
