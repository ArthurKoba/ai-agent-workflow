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

## ENV design gate — expose only genuine operator configuration

Apply this gate **before** inventing a variable, adding it to `.env.example`,
creating a Coolify Shared Variable, or adding an `environment:` entry.
**An ENV key is an external contract, not a place to move application constants.**

For every proposed key, answer all of these:

1. **Who operates it?** Name the human/operator or external system that must
   supply or legitimately change the value between deployments. If nobody does,
   keep it in code or a versioned deployment definition, not ENV.
2. **Who owns it?** Name the exact application subsystem or deployment resource
   consuming it. Do not group unrelated database, authentication, invitation,
   idempotency and storage concerns into one generic settings object/prefix.
3. **Is it independent?** If the application can derive it unambiguously from
   existing inputs or its known topology, compute it once. Do not demand both
   database components and an independently supplied connection URL, or expose
   duplicated public/internal addresses without a distinct consumer contract.
4. **Where does it belong?** Choose application code for invariant behavior;
   Git Compose for stable service DNS, internal ports and topology; Coolify
   operator settings for actual external inputs; and a protected secret provider
   for credentials. A runtime's ENV is a *delivery mechanism*, not necessarily
   the owner of the value.
5. **Is there a safe default?** Mark genuinely unpredictable required values
   empty/required and fail fast. Keep safe, canonical defaults in the owning
   code/Compose. Do not advertise internal tuning knobs just because a settings
   framework supports an override.

### Naming is relative to the service boundary

- Prefer short, recognizable **purpose nouns**: `POSTGRES_PASSWORD`,
  `ADMIN_UI_PUBLIC_URL`, `CREDENTIAL_ENCRYPTION_KEY`, `SIGNING_PRIVATE_KEY`.
  Use upstream image/application variable names where those are authoritative.
- Inside a single service, its own product/service name is already implied.
  Avoid redundant `MY_SERVICE_`, `PLATFORM_` or application-brand prefixes.
  Add a domain prefix only when it genuinely distinguishes two concepts in
  the **same consumer** (`ADMIN_JWT_SIGNING_KEY` vs an unrelated signing key).
- Deployment identity is already represented by the chosen environment,
  project and service. Do not bake `DEV_`, `STAGING_`, `PROD_`, environment
  names or deployment IDs into keys unless the **same process** really consumes
  independent values for multiple environments.
- Name the **meaning**, not internal encoding or incidental implementation:
  avoid `_B64`, generic `_TOKEN`, `_CONFIG` and vague `URL` when a clearer
  purpose name exists. Specify PEM/base64/format separately in the consuming
  contract when needed. Do not shorten so far that ownership becomes unclear.
- One concept gets one canonical key. Do not add an alias/wrapper only to
  translate a value that the image or application already consumes directly.

### Required, default, internal: three different outcomes

| Decision | Placement | Example |
| --- | --- | --- |
| Operator must supply a secret or external origin | protected secret store / required Coolify variable; empty until supplied | `POSTGRES_PASSWORD=` or `ADMIN_UI_PUBLIC_URL=` |
| Operator may override a genuinely portable value | owning service's documented default, optionally exposed | `POSTGRES_PORT=5432`, `TZ=UTC` |
| Value follows from architecture, selected deployment or product state | code, service topology or state machine; **not** an operator ENV | internal service DNS, normal timeout, first-user onboarding state |

An `.env.example` is a **minimal contract for its own deployment**, not a
full list of every settings-model field. Separate historical/legacy and new
service examples; do not mix incompatible default databases, URLs or secrets.
Keep tuning overrides undocumented/unexposed until there is a real operator
use case. An optional key with a safe preset does not become a required blank.

### Feature and security switches are not substitutes for correct design

Do not expose environment toggles that answer whether a deployed service
really runs its own core function, whether mandatory authentication/service
identity is enforced, or whether an unfinished preview is enabled. Deploy a
correctly secured runtime, or **do not deploy that runtime**. Required trust
material must fail startup closed when absent; never let a boolean silently
turn off a required security boundary.

When behavior is determined by durable product state (for example, whether
initial administrator setup remains necessary), derive it from authoritative
state, not `ENABLE_PREVIEW`, `PRINT_BOOTSTRAP_SECRET` or similar operator flags.
If an initial code must be shown until setup is completed, use the approved
restricted operator channel and stop when the state changes; do not expose
recoverable secrets through general application logs as a configuration choice.
A real independently supported product feature may have an operator setting,
but its owner, purpose and supported lifecycle must be explicit.

### Secret ownership and agent access are distinct from ENV transport

- Keep real secret **values** in the designated protected Coolify Shared
  Variables/secret-provider scope, never in Git, images, sample files or
  pasted application-variable values. If a project deliberately protects
  project-scoped Shared Variables from agents while allowing them to manage
  Application ENV, **preserve that security boundary**, even for a secret
  consumed by one service; don't relocate it to Application scope for neatness.
- Application ENV may contain **references**, nonsecret topology and
  nonsecret operator options. The resolved runtime environment may nonetheless
  contain plaintext secrets. Do not grant agents shell/process-env access,
  reveal-secret controls, unredacted logs, or variable-value APIs merely
  because Application ENV configuration is editable. Verify actual tool/RBAC
  permissions; UI masking alone is not an access boundary.
- Share a value only where consumers and **visibility policy** require it.
  Project/Team/Environment scopes are security/ownership decisions, not
  synonyms for convenience. Resolve references explicitly; no implicit
  inheritance, invented default credentials or extra copies of secret values.
- Secret introduction, renaming, rotation or removal is a migration: preserve
  durable encrypted data, token verification and replay guarantees. Remove
  cryptographic ENV inputs only after the replacement design proves those
  guarantees; never replace encryption with plaintext persistence.

### Acceptance before a Coolify deployment

Independently review the full proposed variable inventory, not just spelling:
for each key record its real operator use case, consuming owner, scope,
required/default rule, origin (operator / derived / secret reference) and
removal/migration path if legacy. Reject unused keys, duplicate sources of
truth, imaginary configurability, redundant service/environment prefixes,
unnecessary secrets and bypass switches. Verify on the actual Coolify parser
that required entries are blank, safe defaults stay defaults, Shared
references resolve **without showing secret values**, and the agent's
observable controls do not expose resolved runtime secrets. A passing YAML
parse alone does not meet this gate.

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

For Git-backed Coolify resources, **Watch paths are mandatory** unless the repository explicitly documents why the resource must react to repository-wide changes. Set them repository-relative and as narrowly as possible to the actual deployment inputs.

Do not automatically watch the whole service directory when it also contains README/runbook/audit files. A docs-only commit must not restart a production service unless documentation is itself a deployment input.

Prefer explicit inputs such as:

```text
deploy/coolify/example/docker-compose.yaml
deploy/coolify/example/bootstrap/**
deploy/coolify/example/config/**
```

Use `deploy/coolify/example/**` only when the directory is intentionally deployment-only or every file in it should trigger a redeploy.

A missing or overly broad Watch paths contract is an acceptance blocker for Git-backed deployments: it can cause unrelated documentation/metadata commits to rebuild/redeploy the service, while an incomplete path set can prevent required changes from triggering deployment. Treat the persisted Coolify Watch paths value as runtime state and verify it after resource creation/recreation.

If the service consumes shared repository files outside its own directory, list those paths explicitly rather than falling back to an unrestricted repository-wide trigger.

## Configuration classification

Classify every configurable value before writing the manifest.

| Kind | Compose treatment | Coolify treatment |
| --- | --- | --- |
| secret/credential/private key/token | reference only | protected shared-variable scope selected by ownership and access policy |
| mutable external address, bind IP, remote endpoint, externally meaningful listen port | required: `${VAR:?}` | resource variable, intentionally empty until set |
| safe portable default such as timezone or non-sensitive DNS | optional: `${VAR:-default}` | generated resource variable may keep default |
| internal service-to-service host/port | literal service DNS + container port | do not externalize unless a real consumer needs it |
| deployment identity label/metric label | literal if invariant for that stack; variable only when operationally mutable | keep out of shared secret scope |
| generated domain | `SERVICE_FQDN_*` / `SERVICE_URL_*` directive | Coolify-managed domain variable |
| editable config file | bind mount with inline `content:` | Coolify-managed file mount |

Do not turn every literal into an environment variable. Parameterization is useful only where the value has a real independent lifecycle.

## Naming

Prefer the application's canonical environment variable when it already expresses the right meaning. Do not invent a stack-specific alias merely to forward the same value.

For infrastructure-owned variables with no upstream canonical name, include only the distinction needed at **their actual scope**:

- inside one service, use `METRICS_ENDPOINT`, `AUTH_USERNAME` or `AUTH_PASSWORD` when the purpose is unambiguous; adding the service name again conveys nothing;
- in a shared namespace serving several systems, qualify colliding concepts, for example `VPN_PUBLIC_ENDPOINT` and `VICTORIA_METRICS_ENDPOINT`; a shared-store key may be more qualified than the consuming application's own key;
- use a transport-specific suffix such as `_REMOTE_WRITE_URL` only when distinguishing several endpoints is operationally necessary;
- pair credentials consistently, including qualified shared keys such as `VICTORIA_METRICS_AUTH_USERNAME` and `VICTORIA_METRICS_AUTH_PASSWORD` when needed;
- avoid ambiguous names such as `PUBLIC_ENDPOINT`, `HOST`, `PORT`, `URL` when several endpoints/hosts/ports exist;
- avoid awkward implementation verbs in long-lived variable names when a stable noun communicates the contract better;
- distinguish container-local ports from externally meaningful listen ports;
- distinguish public peer endpoints from HTTP/admin domains.

A variable name is part of the operational contract. Renaming a live variable requires the same migration care as changing its value. Prefer names that remain valid if the implementation behind the endpoint changes.

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

If one canonical value feeds components with different names, declare one
resource variable in Compose and map both consumer keys from it:

```yaml
environment:
  TZ: ${TZ:?}
  tz: ${TZ:?}
```

Then assign the Coolify resource variable to the selected shared scope, for example:

```text
TZ={{team.TZ}}
```

Use the actual selected scope for the deployment. Do not assume a reference at one scope falls back to another.

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

For Git-backed Compose on Coolify 4.3.23, use a two-step contract:

```yaml
environment:
  METRICS_ENDPOINT: ${METRICS_ENDPOINT:?}
  METRICS_AUTH_USERNAME: ${METRICS_AUTH_USERNAME:?}
  METRICS_AUTH_PASSWORD: ${METRICS_AUTH_PASSWORD:?}
```

Then set the generated resource variables in Coolify to the shared references:

```text
METRICS_ENDPOINT={{team.METRICS_ENDPOINT}}
METRICS_AUTH_USERNAME={{team.METRICS_AUTH_USERNAME}}
METRICS_AUTH_PASSWORD={{team.METRICS_AUTH_PASSWORD}}
```

Rules:

- verify that the referenced shared variable exists at the exact scope and exact key before deployment;
- do not treat `is_shared=true` on a resource variable as proof that resolution succeeded;
- an unresolved shared reference can remain literal and reach the container, so validate the runtime value indirectly through application behavior/logs without printing secrets;
- on versions where direct `{{scope.KEY}}` inside Git Compose has not been proven, do not hard-code shared references as service environment values; prefer `${VAR}` in Git and put the shared reference in the Coolify resource variable;
- choose the scope that protects secret ownership and visibility while covering authorized consumers;
- an agent usually needs variable names, scopes and references, not plaintext values;
- never reveal or log secret values merely to verify that the reference exists;
- absence of a required shared reference is a deployment/configuration error, not a reason to hard-code a temporary credential.

### Required state is not an unset-value diagnosis

Coolify's **Required** flag describes a configuration obligation; it may remain visible after the value is supplied. Likewise a name-only API returning `is_shared=false` proves neither that the variable is empty nor that its content is correct; `is_shared=true` does not prove the reference resolved. When the user says Shared credentials already exist, read the exact current scope and key metadata, preserve them and configure only the Application reference. Never guess `{{project.KEY}}` versus `{{environment.KEY}}` from a project name or a previous example, invent undocumented `{{scope.name}}` magic properties, recreate existing Shared entries, or replace an owner-scoped principal with a general database administrator just to make startup pass. Validate resolution without revealing secrets.

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

## Public-route inventory before generating domains

Before supplying Coolify Application settings, derive the public/private route inventory from the **accepted product/API contract**, not from whichever containers happen to exist or which endpoints are currently mounted. For each intended route identify its owner Compose service, externally used hostname/protocol, internal listener port, consumer, and activation/security prerequisite. When OAuth is split from MCP resource ingress, check whether the Authorization Server needs its own public issuer, discovery, login and token routes while the Gateway owns MCP resource endpoints. A health-only stub does **not** satisfy the required OAuth route, and a not-yet-active public service must not be mistakenly classified as permanently internal. Do not expose the private identity/data owner merely because it participates in authentication.

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


Match the magic variable to the **actual Compose service name** (uppercase with service separators normalized to underscores) and the port exposed by that service: for example `auth-server` on `8000` uses `SERVICE_URL_AUTH_SERVER_8000: /` if that magic form is supported by the deployed parser. Declare it under the owning service's `environment:` in the **Coolify-parsed Compose input**, including an explicit override when the source uses `extends`; a declaration hidden in an unresolved base file is not sufficient evidence of parser discovery. Choose the parser-supported `SERVICE_FQDN_*` or `SERVICE_URL_*` form from the exact deployed version, rather than inventing variants or manually populating managed `SERVICE_*` entries. Avoid ordinary application configuration keys starting with `SERVICE_*` when they could collide with Coolify's generated-variable namespace.

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

### Consuming generated URLs inside the application

Keep routing declaration and application-visible canonical URL conceptually separate.

A port-qualified magic variable such as:

```yaml
SERVICE_URL_APP_8080: /
```

primarily declares a Coolify-managed public route to internal port 8080. If the application also needs to know its own public URL for webhooks, secure-cookie derivation, OAuth redirects or generated links, use a separate ordinary explicitly configured application variable, for example:

```yaml
environment:
  SERVICE_URL_APP_8080: /
  APP_EXTERNAL_URL: ${APP_EXTERNAL_URL:?}
```

Only declare `APP_EXTERNAL_URL` when the application actually consumes a canonical public URL. If needed, set this ordinary required Application variable **after** the managed domain has been established, through a verified operator/source binding. Do not promise that a generated route automatically becomes an application ENV value; omitting the unnecessary ordinary variable is preferable.

Observed on a Git-backed Coolify 4.4.1 path: directly assigning an application variable from a port-qualified magic variable in the same Compose environment could reach the final Docker Compose interpolation before that generated value was present, producing an unset-variable warning and an empty application value even though the public proxy route later existed. **Do not put `${SERVICE_URL_*}`, including nested fallback interpolation, in Compose values unless the actual parser/runtime contract was explicitly validated.** Keep the literal magic route directive separate from application configuration. Treat this as parser/runtime ordering, not generic Compose behavior.

Therefore validate both surfaces separately:

1. the public route answers on the generated domain;
2. application startup/runtime evidence shows its own external/canonical URL is non-empty and correct.

An HTTP 200 through the proxy does not prove the application received its external URL.

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

## Git-backed migration

When converting a UI-owned Coolify service into Git-backed Compose:

1. capture the known-good Compose and parser-managed state;
2. inventory required/shared/default variables;
3. capture generated domains and their target ports;
4. capture managed-file contents;
5. capture old persistent volume names and determine how the deployed Coolify version names replacement volumes;
6. refactor only after the preservation contract is explicit;
7. create/recreate the Git-backed resource and inspect parser output before deployment;
8. when the parser namespaces named volumes to the new resource UUID, do not assume top-level Compose `external:`/`name:` will preserve cross-resource attachment; explicitly copy old volume contents into the new resource volumes after verifying source and destination identities;
9. stop the old service before copying or attaching writable state;
10. deploy and validate;
11. retain the old resource and old volumes as rollback until acceptance.

Do not run two stacks concurrently against the same writable state volume unless the application explicitly supports it.

## Parser state and stale variables

Treat an existing Coolify resource as stateful parser output, not as a pure reflection of the current Git file.

Observed consequences on Coolify 4.3.23:

- variables removed from Compose can remain as stale resource variables until explicitly deleted;
- generated file/domain/storage records can survive source changes;
- a successful reparse does not prove stale state was removed;
- a disposable **diagnostic** resource can distinguish fresh-parser behavior from stale state, but never recreate a real existing application merely to diagnose a domain/ENV mismatch; inspect and preserve its domains, variables, live credentials, volumes and rollout history first.

During migration or refactors, compare current Git requirements with the actual resource variable/storage/domain inventory and remove only entries proven obsolete. Do not delete unknown state merely because it is absent from the latest Compose.

When a parser-managed feature is introduced after a resource already exists, a reparse can materialize the variable/storage record without reproducing the same initialization path as a brand-new resource. If generated state looks impossible or internally inconsistent, recreate a disposable resource from the same Git revision before changing the manifest again. Fresh-resource reproduction distinguishes parser-state drift from source defects.

### Persistent-state migration discipline

Do not repair a named volume by recursively changing ownership or deleting unknown contents merely because a new container UID/GID differs.

For a layout migration:

1. identify which subpaths are durable authority and which are documented recreatable cache/runtime data;
2. whitelist only proven disposable legacy paths for automatic cleanup/migration;
3. validate their expected structure before deleting them;
4. fail closed on unknown siblings/content;
5. re-run the same migration on a regression fixture so repeat deploy remains idempotent.

In user-namespace/rootless scenarios, files created by runner/container identities may appear on the host with subordinate mapped IDs. That alone is not corruption.

## Deploy and restart acceptance

A Git change does not configure an existing Coolify resource until the **reviewed commit is on the resource's real configured branch** and the orchestrator has parsed/deployed that exact revision. Before telling an operator to deploy, verify the published ref, native Base Directory/Compose location, saved Watch Paths, and whether merge/webhooks will auto-deploy a resource whose database or security prerequisites are still unapproved. A source-level `activation: blocked` label is not an orchestrator stop mechanism. Avoid telling the operator to recreate a resource or to set manually generated magic variables as a workaround.

Choose `restart:` from the accepted failure lifecycle: when an unrepairable configuration/credential/schema/trust failure must stop a service, a policy such as `unless-stopped` causes an endless startup loop, while `restart: "no"` allows inspection after one failure. Do not impose fail-stop on healthy long-lived workers without that contract. Verify the **effective** policy/container after Coolify reparse, rather than assuming that updating Git changed a running container. Diagnose failures from safe, actionable error categories and bounded runtime evidence; an intentionally redacted generic startup exception is not proof of a particular SQL/password cause.

A successful image build, a Coolify deployment marked `finished`, a container marked `running:healthy`, application `/health/live`, readiness/authorization and an external user-facing HTTPS/OAuth/MCP operation are **different acceptance levels**. Check the intended consumer's actual route, DNS/TLS and expected response; missing top-level `fqdn` on a Compose Application alone is not evidence that the service-specific managed domain is absent.

## Fresh-parse validation

Parser-driven features require parser validation, not only YAML validation.

Before declaring the source ready, inspect a fresh Coolify resource and verify:

- every required variable exists, is marked Required and is empty until intentionally set;
- optional variables contain only approved defaults;
- each shared-variable reference points to an existing key at the exact intended scope;
- shared secret references are present without exposing secret values;
- runtime logs/behavior show that shared references resolved to usable values rather than remaining literal `{{scope.KEY}}` strings;
- generated domains exist in the expected count, under the expected services, with the expected target ports;
- if the application consumes its own public URL, startup/runtime evidence shows the resolved canonical URL rather than only proving proxy reachability;
- managed file mounts appear at the intended paths;
- internal-only ports are not host-published;
- persistent volumes refer to the intended existing data;
- Compose parser output contains no stale placeholders or unintended generated values.

Then perform deployment/runtime/consumer acceptance separately. For telemetry pipelines, query the actual backend (for example through Grafana's configured datasource proxy) after deployment; container health and successful exporter scrape are not enough to prove remote-write delivery.

## Source references

Use current documentation for user-facing contracts, then inspect the parser source for version-specific behavior:

- Docker Compose: https://coolify.io/docs/applications/builds/docker-compose
- Service environment variables: https://coolify.io/docs/services/configuration/environment-variables
- Shared variables: https://coolify.io/docs/core/team/shared-variables
- File mounts: https://coolify.io/docs/core/persistent-storage/storage-mounts/file-mounts
- Coolify v4 Compose parser: https://github.com/coollabsio/coolify/blob/v4.x/bootstrap/helpers/parsers.php
- Environment variable model: https://github.com/coollabsio/coolify/blob/v4.x/app/Models/EnvironmentVariable.php

When the deployed version is known, prefer that exact tag/commit over `v4.x` for debugging parser behavior.
