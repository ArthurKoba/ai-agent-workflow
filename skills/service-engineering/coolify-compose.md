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

## Mandatory deployment contract

- **Unrequested changes require prior approval.** Do not edit, rename, add, remove, migrate, deploy or otherwise change anything beyond the user's explicit request. If an extra change seems necessary or beneficial, first state the exact proposed change and wait for explicit authorization. Neither conventions, best practices, nor a broad request to proceed imply consent.
- **Get explicit user approval of the complete operator-variable contract** before adding, renaming, aliasing or removing keys: exact names, purpose, Required/Default semantics, owner and secret scope. Never infer approval from a general implementation request.
- Prefer existing approved or upstream names. Do not invent prefixes, duplicate credentials, intermediary aliases or new privileged identities for convenience.
- Keep a single canonical Compose owner and only justified orchestrator overrides. Ensure every effective deployment input is tracked by Watch Paths; verify inheritance in the actual parser.
- Treat generated domains, Shared references and parser-managed variables as runtime state. Verify the resulting application configuration and reconcile stale entries before declaring changes complete.
- Preserve data, privilege boundaries and existing deployments. Distinguish source validation from parser, deployment and real-consumer acceptance; never use a speculative redeploy to settle an unresolved contract.

## ENV design gate — expose only genuine operator configuration

**Before** adding an ENV key, `.env.example`, Shared Variable or Compose `environment:`, decide whether it is genuinely operated or derivable. ENV is an **external contract**, not a repository of constants.

For every key identify:
1. **Operator:** who legitimately sets/changes it? If nobody, use code/Git.
2. **Owner:** which exact subsystem/resource consumes it? Do not blend DB, authentication, invitations, idempotency and storage into one generic prefix.
3. **Independence:** can the consumer derive it from topology or existing inputs? Avoid redundant DB URL plus components, or internal/public addresses without separate consumers.
4. **Placement:** invariants in code, stable DNS/ports/topology in Compose, operator inputs in Coolify, secret values in protected storage. ENV delivers values, not necessarily owns them.
5. **Default:** unpredictable external origins/secrets are blank Required and fail closed; safe canonical defaults stay in code/Compose. Do not expose internal tuning without operator use.

### Naming
Prefer upstream keys and short purpose nouns (`POSTGRES_PASSWORD`, `ADMIN_UI_PUBLIC_URL`, `SIGNING_PRIVATE_KEY`). Omit redundant service/brand prefixes within one service; qualify competing concepts only when needed. Environment/deployment identity should not enter keys unless one process consumes multiple environments. Name purpose, not encoding (`_B64`) or vague `_TOKEN`, `_CONFIG`, `URL`; document format separately. One concept has one canonical name, never an unnecessary forwarding alias.

### Required, default and internal
- **Required operator input:** blank Required Coolify variable or protected secret (for example `POSTGRES_PASSWORD=`).
- **Safe optional override:** owning service's portable default (for example `POSTGRES_PORT=5432`, `TZ=UTC`).
- **Derived architecture/product state:** internal service DNS, normal timeout, first-admin onboarding state belong in code/topology, not ENV.

A deployment-specific `.env.example` lists minimal approved operator inputs. Do not combine incompatible old/new databases, origins and secrets. Optional keys with defaults are not Required.

### Feature/security switches
Never expose a toggle to bypass core behavior or mandatory auth/service identity. Deploy secure runtime or do not deploy. Absent trust material fails closed. Infer first-admin setup from durable state, not `ENABLE_PREVIEW` or `PRINT_BOOTSTRAP_SECRET`. Show initial codes only via approved restricted channel until setup, not recoverable general logs. Genuine independent supported features may have explicitly owned switches.

### Secret visibility
- Secret **values** live in protected Shared/secret-provider scope, not in Git/images/samples/pasted ENV. Preserve Project secret access boundaries against agents editing Application ENV; do not relocate secrets into agent-readable scope.
- Resource ENV can carry references but resolved process ENV may be plaintext. Do not grant agents process/shell-env, raw logs, reveal controls or value APIs because they can edit ENV. Verify RBAC, not UI masks.
- Select Team/Project/Environment/Server shared scope by consumer and visibility, without implicit inheritance or duplicate values. Rotating, renaming or removing cryptographic material is a migration preserving encrypted data, token verification and replay guarantees; do not substitute plaintext storage.

### Acceptance gate
Review every variable's operator, consuming owner, purpose, scope, origin (operator/derived/secret), Required/default and legacy removal plan. Reject unused/duplicate/unsafe toggles, redundant aliases and unnecessary secrets. Verify the **actual Coolify parser** produces blank Required inputs, approved defaults and resolved Shared references without disclosing values or granting agent access. YAML parsing is not proof.

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

This is a **new-project preference**, not authorization to reorganize an established repository. If the project uses `deploy/<domain>/<service>/` with Compose and README side by side, keep that structure. Do not add an extra `compose/` directory without an independent deployment requirement.

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

For Git-backed Coolify resources, **Watch Paths are mandatory** unless a repository-wide trigger is explicitly approved. Paths are repository-relative. Follow the **project's existing service layout and intended redeploy semantics**, rather than a universal docs-only prohibition.

**A whole-service-directory glob such as `deploy/vpn/example/**` is valid even when README/runbooks share the folder.** Documentation-only commits may deliberately redeploy the service: do **not** flag this as an error, block acceptance, or invent a nested `compose/` directory. Keep manifests beside README where that is the established layout.

For a project that explicitly requires deployment-input isolation, watch specific Compose/bootstrap/config paths instead. Do not silently change policy in either direction. Missing Watch Paths or paths spanning unrelated services without approval are blockers. Verify the **persisted Coolify value** on resource creation/recreation, not just the documentation.

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

Use `${VAR:-default}` only for genuinely safe portable defaults: `TZ`, non-sensitive resolver, or optionally configurable container listener port. Prefer upstream names (`TZ`, `HTTP_PROXY`) over invented service-specific aliases. A shared `TZ` should replace per-app keys unless required by the image.

Select Team/Project/Environment/Resource shared scope according to ownership; Coolify Shared references **do not cascade** or inherit. Project overrides must be explicit. For consumers needing both `TZ` and `tz`, map both from one variable bound to a verified reference such as `{{team.TZ}}`; do not introduce two timezones.

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

### Coolify destinations and Compose network ownership

- **Destination selection is not Compose attachment.** A Destination has a display **Name** and a separate, actual Docker **Network**. Git-backed Docker Compose applications use their resource-specific network by default; enable **Advanced → Docker Compose → Connect To Predefined Network** for each resource that must also join its selected Destination.
- Let Coolify inject the selected Destination's actual network into the generated deployment Compose. Do not hard-code the Destination's display name as an `external: true` Compose network or invent another shared network merely to mirror a UI selection. Explicit Compose network management needs a separate approved ownership reason.
- Verify the actual Docker Network exists on the target host, the enabled setting, generated network declarations, container membership and cross-resource DNS/port reachability. A Destination record alone does not prove that Docker created its network. On missing-network errors, diagnose the Destination/network provisioning path before modifying Compose; check health-gated startup behavior in the deployed parser version.

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

Coolify declares managed public routes with version-supported `SERVICE_FQDN_*` / `SERVICE_URL_*` ENV magic variables (for example `SERVICE_FQDN_APP_8080: /` for service `app` exposed on port 8080). Match the **actual service name**, normalize separators to underscores, and target the intended internal port. Declare under the owner service's `environment:` in Coolify-parsed Compose; `extends` may require an explicit override for discovery. Do not invent magic variants, manually populate managed keys or use conflicting ordinary `SERVICE_*` keys. Confirm behavior against the deployed parser.

Generated domains are **service-keyed**: two independently editable domains/ports may not coexist under one service. When the parser permits only one domain per service, expose separate lightweight ingress adapters mapping each public HTTP route to the appropriate private listener; never grant them unrelated capabilities. Validate domain count, owner, internal ports and stale state on a fresh parser resource.

### Canonical application URL is separate from proxy route
A magic key like `SERVICE_URL_APP_8080: /` declares a proxy route; it need not set the application URL. If the app actually needs a public origin for OAuth issuer/redirects, webhooks, cookies or links, expose a separate genuinely consumed Required key (e.g. `APP_EXTERNAL_URL: ${APP_EXTERNAL_URL:?}`), bound after the managed domain exists. Omit it otherwise.

Observed with Git-backed Coolify 4.4.1: Compose interpolation of `${SERVICE_URL_*}` (even a nested fallback) sometimes occurs before magic values exist, leaving app ENV empty despite a working domain. Never interpolate magic URLs into ordinary ENV without parser/runtime proof. Check the **public route** and the **resolved application canonical URL** independently; HTTP 200 via proxy proves neither app URL nor issuer.

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
