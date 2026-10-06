# Coolify / Docker Compose Contract

Use this module whenever Coolify parses, owns or deploys a Docker Compose resource.

This is a parser/runtime contract, not a generic Docker Compose tutorial. A manifest can be valid Compose and still be wrong for Coolify because Coolify derives environment variables, generated domains, persistent-storage entries and managed files from the Compose source.

## Authority

Keep these layers distinct:

1. **Git Compose** — desired topology, non-secret defaults, parser directives, shared-variable references and managed-file templates.
2. **Coolify** — resolved runtime variables, shared-variable values, domains/certificates, parsed persistent storage and deployment lifecycle.
3. **Container runtime** — actual containers, networks, volumes and mounted files.
4. **Acceptance** — real service behavior.

When parser behavior matters, inspect the deployed Coolify version's parser/source instead of assuming generic Compose behavior.

## Repository and build-path contract

When a Compose manifest contains orchestrator-specific semantics, prefer a layout that names the orchestrator explicitly:

```text
deploy/<orchestrator>/<service>/
```

For Coolify:

```text
deploy/coolify/<service>/
```

This distinguishes a Coolify parser contract from a generic Compose file that might be usable by other runtimes.

Coolify's **Docker compose location is relative to Base directory**. Do not repeat the base path in both fields.

Example:

```text
Base directory: /deploy/coolify/example
Docker compose location: /docker-compose.yaml
Watch paths: deploy/coolify/example/**
```

Do not configure:

```text
Base directory: /deploy/coolify/example
Docker compose location: /deploy/coolify/example/docker-compose.yaml
```

unless the deployed Coolify version explicitly documents a different path contract.

Keep watch paths repository-relative and narrow to the service's deployment directory so unrelated infrastructure changes do not trigger redeployments.

## Configuration classification

Classify every configurable value before writing the manifest.

| Kind | Compose treatment | Coolify treatment |
| --- | --- | --- |
| secret/credential/private key/token | reference only | shared variable at the narrowest useful scope |
| mutable external address, bind IP, remote endpoint, externally meaningful listen port | required: `${VAR:?}` | resource variable, intentionally empty until set |
| safe portable default such as timezone or non-sensitive DNS | optional: `${VAR:-default}` | generated resource variable may keep default |
| internal service-to-service host/port | literal service DNS + container port | do not externalize unless a real consumer needs it |
| deployment identity label/metric label | literal if invariant for that stack; variable only when operationally mutable | keep out of shared secret scope |
| generated domain | `SERVICE_FQDN_*` / `SERVICE_URL_*` directive | Coolify-managed domain variable |
| editable config file | bind mount with inline `content:` | Coolify-managed file mount |

Do not turn every literal into an environment variable. Parameterization is useful only where the value has a real independent lifecycle.

## Naming

Prefer the application's canonical environment variable when it already expresses the right meaning. Do not invent a stack-specific alias merely to forward the same value.

For infrastructure-owned variables that have no upstream canonical name, encode purpose in the key:

- prefer `VPN_PUBLIC_ENDPOINT`, `ADMIN_BIND_IP`, `METRICS_REMOTE_WRITE_URL`;
- avoid ambiguous names such as `PUBLIC_ENDPOINT`, `HOST`, `PORT` when several endpoints/hosts/ports exist;
- distinguish container-local ports from externally meaningful listen ports;
- distinguish public peer endpoints from HTTP/admin domains.

A variable name is part of the operational contract. Renaming a live variable requires the same migration care as changing its value.

## Required variables

For values that must be supplied before deployment:

```yaml
environment:
  PUBLIC_ENDPOINT: ${PUBLIC_ENDPOINT:?}
```

Rules:

- use empty `:?` when the Coolify UI should create a **Required** variable with no default;
- do not use `${VAR:?VAR is required}` for Coolify UI materialization unless the deployed parser version is proven to keep the message only as an error message; some parser/UI flows can persist the text after `?` as the variable value;
- do not give a fallback to a value whose absence should block deployment;
- declare the required variable under the owning service's `environment:` even when Compose also uses it in `ports:`, `command:`, labels or another field. Coolify parser discovery is environment/build-argument oriented; a variable used only elsewhere may fail to appear as a managed Required entry;
- using the same `${VAR:?}` expression again in `ports:` or `command:` is acceptable when Compose interpolation itself must also fail closed.

Bad:

```yaml
ports:
  - '${BIND_IP:-0.0.0.0}:8080:8080'
```

when binding every interface would be unsafe or unintended.

Good:

```yaml
environment:
  BIND_IP: ${BIND_IP:?}
ports:
  - '${BIND_IP:?}:8080:8080'
```

## Optional defaults

Use `${VAR:-default}` only when the default is genuinely safe and portable.

Typical candidates:

- `TZ`;
- non-sensitive DNS resolver choice;
- conventional application-local listener ports when changing them is optional rather than required topology.

Prefer canonical variable names already understood by images. Do not invent a stack-specific forwarding alias solely to map an unchanged value into `TZ`, `HTTP_PROXY`, or another standard variable.

Timezone deserves special treatment because most images already understand the canonical `TZ` key.

Prefer a shared `TZ` variable instead of inventing stack-specific names such as
`APP_TIMEZONE`, `SERVICE_TIMEZONE`, or `VPN_CORE_TIMEZONE` unless the
application itself requires such a key.

Choose the shared scope according to ownership:

- team scope for a broad organizational default;
- project scope when the whole project shares one timezone;
- environment scope when staging/production or regions differ;
- resource scope only when one deployment genuinely differs.

Coolify shared references are explicit, not an automatic cascading inheritance
system. If a project needs to override a team-level default, point that
deployment at the project-scoped value explicitly rather than assuming
`{{project.TZ}}` will transparently fall back to `{{team.TZ}}`.

If one canonical value feeds components with different names, map from the same
shared value directly:

```yaml
environment:
  TZ: '{{project.TZ}}'
  tz: '{{project.TZ}}'
```

Use the actual selected scope for the deployment; the example above shows project scope.

## Coolify variable flags

Use Coolify variable flags intentionally:

- **Runtime** — enable when the running container needs the value;
- **Buildtime** — enable only when image/build interpolation actually needs it; do not expose runtime-only secrets to builds by default;
- **Literal** — use when characters such as the dollar sign must remain unexpanded;
- **Multiline** — use for certificates, keys or configuration blobs that genuinely contain line breaks; treat them as secret when sensitive;
- **Preview** — keep separate values only when preview deployments really need a distinct contract.

Do not accept whatever flags Coolify generated without checking whether they match the consumer.

Managed/generated `SERVICE_*` variables belong to Coolify's parser state. Do not convert them into hand-maintained business configuration.

## Secrets and shared variables

Never commit secret values to Compose, Dockerfiles, tracked env files or generated config.

Use the narrowest Coolify shared-variable scope that matches ownership:

- `{{team.NAME}}`
- `{{project.NAME}}`
- `{{environment.NAME}}`
- `{{server.NAME}}`

Example:

```yaml
environment:
  METRICS_URL: '{{project.METRICS_URL}}'
  METRICS_USERNAME: '{{project.METRICS_USERNAME}}'
  METRICS_PASSWORD: '{{project.METRICS_PASSWORD}}'
```

Rules:

- reference the shared value directly from Compose when the deployed Coolify version supports it;
- do not create redundant resource-level copies merely to relay an existing shared variable;
- choose the narrowest scope covering all consumers;
- an agent usually needs variable names, scopes and references, not plaintext values;
- never reveal or log secret values merely to verify that the reference exists;
- absence of a required shared reference is a deployment/configuration error, not a reason to hard-code a temporary credential.

## Internal vs external networking

Internal traffic should stay internal.

Prefer:

```text
api -> postgres:5432
collector -> exporter:9550
frontend -> backend:8080
```

over host/LAN hairpins such as:

```text
api -> 192.168.x.x:5432
collector -> host-ip:9550
```

Rules:

- use Docker service DNS and fixed container ports for internal communication;
- use `expose:` to document/discover internal ports when useful;
- use `ports:` only when a host or external consumer really needs the port;
- do not publish metrics/admin/debug endpoints merely because another container consumes them;
- mutable remote hosts, cross-server targets, bind addresses and externally meaningful ports belong in required runtime variables.

## Generated domains

Coolify can generate domains from service magic variables.

Typical pattern:

```yaml
services:
  app:
    environment:
      SERVICE_FQDN_APP_8080: /
    expose:
      - '8080'
```

The port suffix tells Coolify which internal service port the generated domain targets.

Important parser boundary:

- generated domain state is keyed by Compose service;
- multiple independently editable public domains on different ports should not be assumed to coexist correctly merely by adding several `SERVICE_FQDN_<SAME_SERVICE>_<PORT>` variables;
- when the current parser stores one domain per service, model independent public routes as independent Compose services.

If several public HTTP routes actually terminate in one shared network namespace, use lightweight ingress adapters when appropriate:

```text
public domain A -> ingress-a -> shared-service:port-A
public domain B -> ingress-b -> shared-service:port-B
```

The adapters should expose only the intended HTTP port and should not acquire unrelated capabilities or host ports.

After parser changes, validate the number of generated domains, owning services and internal ports on a **freshly parsed resource**. Existing resources can retain stale managed state.

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

## Git-backed migration

When converting a UI-owned Coolify service into Git-backed Compose:

1. capture the known-good Compose and parser-managed state;
2. inventory required/shared/default variables;
3. capture generated domains and their target ports;
4. capture managed-file contents;
5. preserve exact persistent volume names/ownership;
6. refactor only after the preservation contract is explicit;
7. create/recreate the Git-backed resource and inspect parser output before deployment;
8. stop the old service before attaching the same writable volumes to the replacement;
9. deploy and validate;
10. retain the old resource as rollback until acceptance.

Do not run two stacks concurrently against the same writable state volume unless the application explicitly supports it.

## Fresh-parse validation

Parser-driven features require parser validation, not only YAML validation.

Before declaring the source ready, inspect a fresh Coolify resource and verify:

- every required variable exists, is marked Required and is empty until intentionally set;
- optional variables contain only approved defaults;
- shared secret references are present without exposing secret values;
- generated domains exist in the expected count, under the expected services, with the expected target ports;
- managed file mounts appear at the intended paths;
- internal-only ports are not host-published;
- persistent volumes refer to the intended existing data;
- Compose parser output contains no stale placeholders or unintended generated values.

Then perform deployment/runtime/consumer acceptance separately.

## Source references

Use current documentation for user-facing contracts, then inspect the parser source for version-specific behavior:

- Docker Compose: https://coolify.io/docs/applications/builds/docker-compose
- Service environment variables: https://coolify.io/docs/services/configuration/environment-variables
- Shared variables: https://coolify.io/docs/core/team/shared-variables
- File mounts: https://coolify.io/docs/core/persistent-storage/storage-mounts/file-mounts
- Coolify v4 Compose parser: https://github.com/coollabsio/coolify/blob/v4.x/bootstrap/helpers/parsers.php
- Environment variable model: https://github.com/coollabsio/coolify/blob/v4.x/app/Models/EnvironmentVariable.php

When the deployed version is known, prefer that exact tag/commit over `v4.x` for debugging parser behavior.
