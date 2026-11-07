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

## Native OTLP telemetry (optional)

Both the standalone and shared **base Compose** files now expose ZITADEL v4.20 native trace, metric and log exporters on **`zitadel-core`**. Coolify overlays repeat the same declarations for parser visibility. No additional collector, gateway, host port or mandatory credential is introduced. Structured JSON logs are also written to stderr.

To enable remote telemetry, set `OTEL_ENDPOINT` to the receiver **host:port** (no `http://` or `https://`) and configure each desired native `ZITADEL_INSTRUMENTATION_{TRACE,METRIC,LOG}_EXPORTER_TYPE` to `http` for OTLP/HTTP or `grpc` for OTLP/gRPC. All three default to `none`; omission of a receiver must not make an otherwise usable identity stack fail. TLS is used by default; for an approved cleartext internal collector, set the corresponding `ZITADEL_INSTRUMENTATION_*_EXPORTER_INSECURE=true` inputs. Never expose these private receivers via a new Coolify Domain.

For authenticated receivers, supply the upstream `OTEL_EXPORTER_OTLP_HEADERS` in protected configuration (for example, a URL-encoded `authorization=Bearer%20…` header). No token or prebuilt Authorization value belongs in Git. `OTEL_RESOURCE_ATTRIBUTES` is optional for deployment/namespace labels, and `ZITADEL_INSTRUMENTATION_SERVICENAME` is the stable `zitadel` identity. If the deployment owns an `OTEL_BEARER_TOKEN`, construct the headers in that owning overlay rather than requiring all generic installations to use Bearer.

**Scope:** these exporters instrument ZITADEL Core only. Login V2 has no native traces/metrics exporter; its stdout logs and Caddy logs require an existing platform log collector. Confirm actual traces, metrics and logs in the receiver; enabling exporter flags or HTTP 200 is not ingestion evidence.

## Evidence and boundaries

The previous Koba installation on 2026-11-02 verified an **older direct-Traefik** configuration, not this universal Caddy preset. An Intens-specific Caddy installation has returned HTTP 200 for issuer discovery, Login V2 health and console, but real login/logout, authenticated gRPC and restore still require verification. The reusable variants remain **source-ready, not independently runtime-accepted**.

PostgreSQL/Valkey ownership, Redis cache connectors and DB offset, named PAT bootstrap volume, native ZITADEL master key and Login session secret retain their established contracts. Never copy real credentials or project-specific domains into these templates. Do not reset volumes or rotate the master key to troubleshoot routes.

See `standalone/README.md`, `shared/README.md` and `VALIDATION.md`.
