# Stalwart Community — reusable Compose examples

**Source-only examples.** Live Stalwart, Coolify parser, TLS, OAuth and OpenTelemetry ingestion have not been accepted. No panel container, no per-node Git directories.

| Variant | Contents |
| --- | --- |
| `classic/` | Stalwart, PostgreSQL, Valkey plus an automatic one-shot `bootstrap` in one Compose |
| `node/` | One universal Stalwart node; each Coolify resource supplies its own ENV |
| `dependencies/` | Shared PostgreSQL/Valkey for a future distributed arrangement |

Every variant has `docker-compose.yaml` and `docker-compose.coolify.yaml`. The latter uses `extends` and repeats persistent volumes. Copy one reviewed preset into the owning infrastructure repository; use its folder as Coolify Base Directory, `/docker-compose.coolify.yaml` as Compose Location, and the corresponding copied folder as Watch Paths. `classic` and independent `dependencies` are **alternative** owners of the database, not stacks to start together. Docker bridge does **not** connect physical hosts; future nodes need an authenticated private route, shared stores and coordinator.

The classic mail listener exposes TCP 25, 465, 587 and 993, but bootstrap HTTP stays on host loopback. Configure proper mail-protocol certificates, DNS and SPF/DKIM/DMARC. Keep `POSTGRES_PASSWORD`, `VALKEY_PASSWORD` and `OTEL_BEARER_TOKEN` protected; `STALWART_HOSTNAME` is a unique stable node identity.

## Inline one-shot bootstrap

The `classic` Compose declares `bootstrap` with `restart: "no"` and `depends_on: stalwart: service_healthy`. **It starts automatically during ordinary Compose deployment**, without a profile flag, then exits. It is not a permanent application service.

A `dockerfile_inline` build copies the verified upstream `stalwart-cli` executable into a minimal non-root Python image. The entire runner is inline in the Compose `command`: it creates JSON objects from environment values, serializes them as **NDJSON in memory**, and invokes the official CLI in sequence:

1. `stalwart-cli apply --stdin --dry-run` — structural validation against the server schema.
2. `stalwart-cli apply --stdin` — apply the idempotent configuration.
3. `stalwart-cli create Action/ReloadSettings` — activate settings.

There are **no extra shell scripts, Python files, NDJSON templates, Dockerfiles, or editable File Mounts**. OIDC and OpenTelemetry configuration is persisted by Stalwart in its database, not in an operator-edited `config.json`. When supplied, the server resolves its OpenTelemetry Bearer token from **protected environment variables**; the generated CLI plan contains a reference rather than the token value. Without a token, the plan omits HTTP authentication. Collector endpoints must use HTTPS with valid TLS certificates. OpenTelemetry traces/logs and metrics use OTLP/HTTP; no particular observability vendor is required.

### Configuration inputs

The one-shot service checks **which integration parameters are present**, without enable/disable flags. If no OIDC issuer and no OpenTelemetry endpoint are supplied, it exits successfully without requiring a management API token. If an integration is configured, management credentials are required. Incomplete OIDC settings fail before applying anything:

| Key | Meaning |
| --- | --- |
| `STALWART_URL`, `STALWART_TOKEN` | Existing management **HTTPS** URL and permission-scoped API key |
| `OIDC_ISSUER_URL`, `OIDC_AUDIENCE` | External OpenID issuer HTTPS URL and required access-token audience |
| `OIDC_USERNAME_CLAIM` | Optional, defaults to `email` |
| `OTEL_ENDPOINT` | **HTTPS OTLP/HTTP base** endpoint |
| `OTEL_NAMESPACE`, `DEPLOYMENT_ENVIRONMENT` | Optional OpenTelemetry resource attributes |
| `OIDC_CLIENT_ID` | Optional static external OAuth client ID (when provider does not support client metadata documents) |
| `WEBUI_APPLICATION_ID`, `MAIL_PUBLIC_URL` | Required **only** when a static client ID is supplied |
| `OTEL_BEARER_TOKEN` | Optional: enables HTTPS Bearer authentication when present |

The bootstrap receives the optional `OTEL_BEARER_TOKEN` only to decide whether exporters need a Bearer reference. **Its literal value never enters the generated plan**: the mail server resolves it from protected ENV. When absent, the `httpAuth` field is omitted completely. The runner receives no database password or IdP client secret. Its separate API token is supplied only to the one-shot container, not Git. All configuration objects are JSON-encoded.

**First-install prerequisite:** Stalwart needs its DataStore connection, permanent administrator and management API token before configuration can succeed. A completely fresh installation with OIDC/OTLP already set may leave the one-shot bootstrap failed while the mail service remains available for setup. After initial credentials/HTTPS are established, recreate or rerun bootstrap; `restart: "no"` avoids unlimited retry loops. Later ordinary deployments attempt configured integrations automatically. This example does **not** enable persistent recovery credentials. Coolify one-shot and inline-build acceptance are still necessary.

### Automatic independent activation

**OpenID Connect:** presence of `OIDC_ISSUER_URL` triggers configuration and **activation of the global Authentication directory**. `OIDC_AUDIENCE` is required with it. A static `OIDC_CLIENT_ID` is optional and, when supplied, requires `WEBUI_APPLICATION_ID` and `MAIL_PUBLIC_URL` so that the recovery OAuthClient and WebUI Application are configured *before* switching Authentication. Without a static client ID, the external provider must support Client ID Metadata Documents. Partial OIDC inputs fail explicitly.

**OpenTelemetry:** presence of `OTEL_ENDPOINT` triggers the log/span tracers and metrics exporter; absence leaves OpenTelemetry untouched. `OTEL_BEARER_TOKEN` is optional: when present, exporters use a native Bearer secret reference, otherwise **no Authorization header** is configured. HTTPS certificate validation remains enabled. The two integrations are independent: either may be configured without the other. There is no `OIDC_ACTIVATE` flag.

Activating OIDC globally can deny an existing administrator access. Register/verify the external client, its redirect URIs and the recovery administrator before entering OIDC values in Coolify. The Community edition has one server-wide default directory. External mail users may need provisioning before first sign-in; a successful CLI dry-run alone does not prove working browser authentication.

## Validation boundary

Local source checks cover Compose shape and the bootstrap's generated NDJSON/CLI call order with a mocked CLI; they do not prove live object-schema acceptance, cross-host networking, mailbox availability or HTTPS OpenTelemetry delivery. A real target must independently validate its Coolify parser, chosen Stalwart release, protected secret references, initial administrator bootstrap, client redirects and all OTLP signals.

References: [Stalwart declarative deployments](https://stalw.art/docs/configuration/declarative-deployments/), [CLI apply](https://stalw.art/docs/management/cli/apply/), [Web Applications](https://stalw.art/docs/management/applications/), [OpenTelemetry tracers](https://stalw.art/docs/telemetry/tracing/opentelemetry/), [OpenTelemetry metrics](https://stalw.art/docs/telemetry/metrics/opentelemetry/).
