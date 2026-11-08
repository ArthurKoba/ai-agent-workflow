# Stalwart Community — reusable Compose examples

**Source-only examples.** Live Stalwart, Coolify parser, TLS, OAuth and OpenTelemetry ingestion have not been accepted. No panel container, no per-node Git directories.

| Variant | Contents |
| --- | --- |
| `classic/` | Stalwart, PostgreSQL, Valkey plus optional one-shot `bootstrap` in one Compose |
| `node/` | One universal Stalwart node; each Coolify resource supplies its own ENV |
| `dependencies/` | Shared PostgreSQL/Valkey for a future distributed arrangement |

Every variant has `docker-compose.yaml` and `docker-compose.coolify.yaml`. The latter uses `extends` and repeats persistent volumes. Copy one reviewed preset into the owning infrastructure repository; use its folder as Coolify Base Directory, `/docker-compose.coolify.yaml` as Compose Location, and the corresponding copied folder as Watch Paths. `classic` and independent `dependencies` are **alternative** owners of the database, not stacks to start together. Docker bridge does **not** connect physical hosts; future nodes need an authenticated private route, shared stores and coordinator.

The classic mail listener exposes TCP 25, 465, 587 and 993, but bootstrap HTTP stays on host loopback. Configure proper mail-protocol certificates, DNS and SPF/DKIM/DMARC. Keep `POSTGRES_PASSWORD`, `VALKEY_PASSWORD` and `OTEL_BEARER_TOKEN` protected; `STALWART_HOSTNAME` is a unique stable node identity.

## Inline one-shot bootstrap

The `classic` Compose declares `bootstrap` with `profiles: [configure]`, `restart: "no"` and `depends_on: stalwart: service_healthy`. It is **not** a permanent application service.

A `dockerfile_inline` build copies the verified upstream `stalwart-cli` executable into a minimal non-root Python image. The entire runner is inline in the Compose `command`: it creates JSON objects from environment values, serializes them as **NDJSON in memory**, and invokes the official CLI in sequence:

1. `stalwart-cli apply --stdin --dry-run` — structural validation against the server schema.
2. `stalwart-cli apply --stdin` — apply the idempotent configuration.
3. `stalwart-cli create Action/ReloadSettings` — activate settings.

There are **no extra shell scripts, Python files, NDJSON templates, Dockerfiles, or editable File Mounts**. OIDC and OpenTelemetry configuration is persisted by Stalwart in its database, not in an operator-edited `config.json`. The server resolves its OpenTelemetry Bearer token from its **own protected environment**; the CLI plan contains only the native `EnvironmentVariable` secret reference. Collector endpoints must use HTTPS with valid TLS certificates. OpenTelemetry traces/logs and metrics use OTLP/HTTP; no particular observability vendor is required.

### Configuration inputs

The one-shot service uses these Compose variables. Required values are checked **when the profile runs**, so missing bootstrap secrets never prevent the main mail stack from parsing:

| Key | Meaning |
| --- | --- |
| `STALWART_URL`, `STALWART_TOKEN` | Existing management **HTTPS** URL and permission-scoped API key |
| `OIDC_ISSUER_URL`, `OIDC_AUDIENCE` | External OpenID issuer HTTPS URL and required access-token audience |
| `OIDC_USERNAME_CLAIM` | Optional, defaults to `email` |
| `OTEL_ENDPOINT` | **HTTPS OTLP/HTTP base** endpoint |
| `OTEL_NAMESPACE`, `DEPLOYMENT_ENVIRONMENT` | Optional OpenTelemetry resource attributes |
| `OIDC_ACTIVATE` | Optional, defaults to `false` |
| `OIDC_CLIENT_ID`, `WEBUI_APPLICATION_ID`, `MAIL_PUBLIC_URL` | Required **only** when activating SSO |

The bootstrap does not get `OTEL_BEARER_TOKEN`, a database password, or an identity-provider client secret. Its own API token is supplied only to that one-shot container, not to the mail server or Git. The Python runner JSON-encodes every operation to avoid unsafe template substitution.

**The bootstrap is run after minimal first-time setup.** Stalwart needs its DataStore connection and a permanent administrator before a management API token can exist. The initial wizard can supply these, or a separately managed temporary recovery procedure can initialise them. This example does **not** enable unattended `STALWART_RECOVERY_ADMIN`: leaving it set would grant unrestricted access in normal mode. Once initial access and HTTPS are working, invoke the profile deliberately (e.g. `docker compose --profile configure run --rm bootstrap` on a Docker Compose host). **Coolify profile execution and inline builds require parser/runtime validation**; do not assume its UI exposes an identical command.

### Safe SSO activation

By default the plan configures an external `Oidc` Directory but **does not** change the global authentication directory. `OIDC_ACTIVATE=true` is a separate operator decision after external client registration, redirect verification, admin recovery, and SMTP application-password validation. When enabled it also registers Stalwart's own OAuth recovery client with `full` scope, adjusts the WebUI Application and sets `Authentication.directoryId`. That privileged operation requires an appropriately authorized admin token. A static external client ID can otherwise break login through Stalwart's own OAuth server.

The Community edition provides a single server-wide default directory. External mail accounts may need provisioning before first login to receive mail. Never infer that successful CLI `apply --dry-run` proves actual SSO or telemetry delivery.

## Validation boundary

Local source checks cover Compose shape and the bootstrap's generated NDJSON/CLI call order with a mocked CLI; they do not prove live object-schema acceptance, cross-host networking, mailbox availability or HTTPS OpenTelemetry delivery. A real target must independently validate its Coolify parser, chosen Stalwart release, protected secret references, initial administrator bootstrap, client redirects and all OTLP signals.

References: [Stalwart declarative deployments](https://stalw.art/docs/configuration/declarative-deployments/), [CLI apply](https://stalw.art/docs/management/cli/apply/), [Web Applications](https://stalw.art/docs/management/applications/), [OpenTelemetry tracers](https://stalw.art/docs/telemetry/tracing/opentelemetry/), [OpenTelemetry metrics](https://stalw.art/docs/telemetry/metrics/opentelemetry/).
