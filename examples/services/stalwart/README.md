# Stalwart Community — reusable deployment presets

**Status: source-ready illustration; runtime/parser acceptance pending.** Public examples only: copy an approved revision into the owning infrastructure repository before deploying. Never point a live Coolify resource directly at this catalogue's moving `main`.

The Stalwart v1 WebUI and management API are part of the mail-server process. There is **no separate admin-panel service**, and one generic `node/` Compose is reused for every mail node.

## Variants and ownership

| Variant | Services / intent |
| --- | --- |
| `classic/` | One Stalwart + PostgreSQL 16 + Valkey in **one** Compose resource; default for an initial standalone installation |
| `node/` | One generic Stalwart process; each Coolify resource supplies its unique `STALWART_HOSTNAME`, optional role, and host ports |
| `dependencies/` | Shared PostgreSQL + Valkey; use with `node/` only when intentionally separating lifecycles |

Each variant has a portable `docker-compose.yaml` plus `docker-compose.coolify.yaml`, which uses `extends` and repeats top-level volumes. The Coolify Base Directory is the copied variant folder, Compose Location `/docker-compose.coolify.yaml`, and Watch Paths should cover only that *owned* directory. Do not activate `classic/` and independent `dependencies/` for the same data. Separate resources require verified cross-resource Docker DNS; the default bridge does not connect hosts. Remote nodes need a separately authenticated and routed private network for shared stores and a verified cluster coordinator. Neither Swarm nor WireGuard is created here.

`classic` and `node` use a pinned Stalwart v1.0.3 image; reevaluate the pin before adoption. Both publish SMTP 25, Submissions 465, Submission 587 and IMAPS 993, plus **only** a host-loopback 8080 setup listener (default host port 18080). Validate mail protocol TLS separately from Coolify's HTTP proxy certificate. Confirm mail DNS/MX/PTR/SPF/DKIM/DMARC and port availability. The Stalwart image provides an HTTP healthcheck; a green healthcheck while the wizard is running does not mean mail is available.

`POSTGRES_PASSWORD` and `VALKEY_PASSWORD` are separate, protected deployment-owned secrets. `STALWART_HOSTNAME` is required for each node; never assign the same value to two nodes in one cluster. The Stalwart process receives protected `OTEL_BEARER_TOKEN` because the **native** OpenTelemetry exporter reads it via `SecretKey/EnvironmentVariable`. These examples do not include live domains, addresses, tokens, admin credentials or multi-host topology.

## DataStore: normal wizard or editable Coolify File Mount

Stalwart v1's on-disk `config.json` contains **only** the DataStore connection. OpenID and OpenTelemetry are **database-backed configuration objects**, not extra keys in this file.

- **Wizard:** normal `classic/docker-compose.coolify.yaml` starts without `config.json`. The initial setup wizard selects PostgreSQL and Valkey, and establishes an administrator.
- **Managed file option:** `classic/docker-compose.coolify.managed-config.yaml` is an explicit *alternative* Coolify entrypoint. It adds a non-secret inline `content:` File Mount at `/etc/stalwart-bootstrap/config.json` and sets the documented `CONFIG_PATH` variable to that location. Its content matches `configuration/datastore.postgres.json.example` and uses an `EnvironmentVariable` reference for the PostgreSQL password. It is editable in Coolify's **Persistent Storage → File Mount**; it is not an ordinary Docker Compose feature and is not a Docker named volume. It deliberately omits `read_only` so the dashboard editor remains available. The file mount is separate from the named data volumes and is not part of routine volume backups.

**Important:** With a pre-provisioned `config.json`, the wizard does not initialise the server. For a *fresh* declarative installation the official procedure is to start **temporarily** with `STALWART_RECOVERY_MODE=1` and a protected `STALWART_RECOVERY_ADMIN`, apply a *complete* JMAP configuration including a permanent admin through the official CLI, then **remove both recovery variables and restart**. Leaving the recovery administrator in a persistent runtime grants unrestricted access. This sample does not automate that sensitive bootstrap or claim to be a working zero-touch installation. Coolify File Mount `content` does **not** automatically expand arbitrary environment variables or import OIDC settings.

## Declarative OpenID Connect and OpenTelemetry

`configuration/` provides two NDJSON templates for **official** `stalwart-cli apply`:

- `oidc-otel.ndjson.template`: one external `Oidc` directory, distinct OTLP/HTTP log and span exporters, and an OTLP/HTTP metrics exporter. It does **not** change the live authentication directory.
- `enable-oidc.ndjson.template`: updates the WebUI application's external OAuth client ID and activates the OIDC directory. Execute only after external-client registration and successful recovery-admin/OIDC acceptance.

Input values are supplied to the **trusted configuration-runner process**, not assumed to be recognized automatically by Stalwart:

| Variable | Value / owner |
| --- | --- |
| `OIDC_ISSUER_URL` | Public OpenID issuer **HTTPS** URL |
| `OIDC_AUDIENCE` | Required token `aud` value from external provider |
| `OIDC_CLIENT_ID` | Public external OAuth client registered with PKCE S256 |
| `WEBUI_APPLICATION_ID` | Exact WebUI Application ID queried from Stalwart |
| `OTEL_ENDPOINT` | **HTTPS OTLP/HTTP base URL**, without signal suffix |
| `OTEL_NAMESPACE` | Optional logical `service.namespace` |
| `DEPLOYMENT_ENVIRONMENT` | Resource attribute, e.g. `development` / `production` |
| `STALWART_URL` | Restricted HTTPS management origin for CLI |
| `STALWART_TOKEN` | Separate scoped Stalwart API key for CLI; not the telemetry token |

The HTTP tracer templates use explicit `/v1/logs` and `/v1/traces` URLs. For metrics, Stalwart's HTTP exporter uses the base URL and appends `/v1/metrics`. All three use native `httpAuth: Bearer` with `OTEL_BEARER_TOKEN` resolved inside Stalwart from its **environment**, never copied into NDJSON. TLS certificate checking remains enabled; no `allowInvalidCerts` bypass is used. Keep a local tracer to observe exporter failures.

Render the NDJSON with a JSON-aware template engine or tightly validate URL/identifier values *before* using ordinary `envsubst`, which does **not JSON-escape** substitutions. Run `stalwart-cli apply --file <rendered-plan> --dry-run`, review it, then apply and reload settings with `stalwart-cli create Action/ReloadSettings`. The runner requires the real permission-scoped `STALWART_TOKEN` and should not store or log it. Coolify Shared variables are only available to a resource if explicitly bound to it; they are not automatically visible to a terminal or other applications.

For the external OIDC provider, register correct redirect URIs and ensure it issues tokens with the required audience. Do **not** create a Stalwart-internal `OAuthClient` merely to connect an external IdP. Pre-provision recipients that need to receive mail before first sign-in; ordinary mail clients may still need Stalwart app passwords. Do not replace a recovery login before the new authentication path works.

## Validation and adoption

The YAML, JSON, file-mount shape and variable references can be inspected offline. That is **not** proof of Coolify parser acceptance, editable file persistence, recovery bootstrap, plan/schema compatibility, SMTP delivery, OIDC login or OTLP ingestion. Stalwart CLI's `--dry-run` validates plan structure against a schema; live object matching and signal delivery need separate checks. The Stalwart 1.x documentation changed some exporter fields between revisions: verify the targeted release's `/api/schema` and `stalwart-cli describe` before applying any plan.

No backup tasks, background monitors, automatically activated recovery credentials, or separate metric collectors are created.

Official references: [declarative deployment](https://stalw.art/docs/configuration/declarative-deployments/), [OIDC](https://stalw.art/docs/auth/backend/oidc/), [OpenTelemetry traces/logs](https://stalw.art/docs/telemetry/tracing/opentelemetry/), [OpenTelemetry metrics](https://stalw.art/docs/telemetry/metrics/opentelemetry/), [Coolify File Mounts](https://coolify.io/docs/core/persistent-storage/storage-mounts/file-mounts).
