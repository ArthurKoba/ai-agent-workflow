# Coolify Managed Files and Telemetry

Load when Coolify manages a mounted file, durable state or telemetry pipeline; keep mount and external collector contracts independent of application business configuration. When a local collector is justified for protocol translation, buffering or routing, treat it as a dependency with explicit failure policy; do not require one for every service.

## Ownership and editability

Use **File Mount** for one editable application configuration file (not a named data volume or Host File Mount). `content:` is the Git bootstrap/recovery template and Coolify materializes the file under its managed storage. If an operator edits its Content in Coolify, the **saved runtime file** can diverge from the Git template; later parses may keep the existing file instead of overwriting it. Define the owner and reconciliation policy: export/redact/back up approved changes, review before importing into Git, and never assume Git changes overwrite live content. Prefer one tracked file when Git must remain authoritative; use a Coolify-managed file only when runtime editing is an explicit requirement.

Before editing, inspect current content and mount permissions. The application may require reload/restart; verify behavior after saving. Whether dashboard editing works with read-only mounts is release-specific: verify before relying on it. Coolify's managed file editor has size/format limitations, and File Mounts are not covered by ordinary volume backups; document a separate recovery/export method. Do not confuse managed File Mount with an unmanaged host-file bind.

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

- Templates may refer to **approved names** of environment variables; the application/collector must consume those references at runtime (e.g. Alloy `sys.env("...")`). A `content:` YAML block is not automatically a secure secret interpolator. Never embed resolved passwords/tokens in Git templates, inline config or readable Coolify File Storage; keep secret values with approved Shared/Secret Manager scope and pass references through runtime ENV or a verified secret-file mechanism.
- Do not use `content:` for files containing credentials that the dashboard operator or agent should not be allowed to view. Keep resource-editor permissions and environment access limited; loading file Content can expose any literal secrets already present.
- When `extends` hides File Storage metadata, declare the managed-file mount again in the Coolify entrypoint and validate effective source/target and content synchronization; see `coolify-compose.md`.

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
