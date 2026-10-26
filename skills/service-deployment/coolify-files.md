# Coolify Managed Files and Telemetry

Load when Coolify manages a mounted file, durable state or telemetry pipeline; keep mount and external collector contracts independent of application business configuration. When a local collector is justified for protocol translation, buffering or routing, treat it as a dependency with explicit failure policy; do not require one for every service.

## Managed file mounts

When a service needs an editable configuration file, prefer Coolify's inline-content bind mount rather than an unmanaged host file:

```yaml
volumes:
  - type: bind
    source: ./managed/app/config.yaml
    target: /etc/app/config.yaml
    content: |
      key: value
```

This gives three useful properties:

- Git retains the bootstrap/recovery template;
- Coolify materializes the file mount during Compose parsing;
- the exact container path remains declarative.

Rules:

- use `content:` for generated/managed files when a repository-relative source does not already exist as the authoritative file;
- on Coolify 4.3.23, a repository-relative bind such as `./config.alloy:/etc/alloy/config.alloy:ro` without inline `content:` can be classified as a directory; use an explicit file mount with `content:` when the parser must materialize a file;
- existing Coolify File Storage content at the same mount path takes precedence over the Git inline bootstrap content on later reparses; treat inline `content:` as bootstrap/recovery, not forced synchronization;
- do not replace a production config during migration until its current content is captured or the operator explicitly chooses a new template;
- keep directory/named volumes for durable state and overlay only the specific managed config file when needed;
- a deleted/changed managed storage entry may require a fresh parse/recreate depending on Coolify version/state; do not assume reload always reconstructs deleted managed state;
- test the actual deployed Coolify version because file-mount behavior has changed across releases.

Avoid mounting host `/etc/localtime` or `/etc/timezone` merely to set timezone when the image supports `TZ` and contains timezone data.

## Metrics / observability

Separate connection authority from metric identity.

- shared backend URL/user/password/token -> shared variables;
- stack-local labels such as service/role/zone -> Compose literals when they are stable identity, otherwise ordinary runtime variables;
- exporter/collector communication -> internal Docker DNS;
- do not publish exporter ports to the host unless an external scraper is an actual dependency;
- preserve existing scrape intervals, relabel rules and WAL/queue behavior when migrating observability configs. A minimal replacement config is not equivalent acceptance.
