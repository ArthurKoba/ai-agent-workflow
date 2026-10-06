# Git-backed Infrastructure

Use this module when infrastructure definitions should be version-controlled while a runtime control plane such as Coolify, Portainer, Nomad, Kubernetes, a cloud platform, or another orchestrator owns deployment and live service state.

## Authority split

Keep three authorities distinct:

1. **Git repository** — desired infrastructure definitions, deployment templates, non-secret configuration, change history and review.
2. **Runtime control plane** — live deployment state, domains, certificates, environment/secrets, persistent resources and service lifecycle.
3. **Observability/acceptance surface** — runtime evidence proving that the deployed service works for its real consumer.

Do not treat any one of these as a substitute for the others.

## Public methodology vs private state

Reusable instructions belong in a public/general workflow repository when they do not expose environment-specific state.

Private infrastructure repositories should hold the actual current deployment state, for example:
- concrete Compose manifests;
- service/domain names;
- repository mappings;
- server aliases and resource identifiers;
- watch paths;
- migration state;
- environment-specific runbooks.

Do not put private topology, credentials, host addresses, tokens or current resource IDs into a universal workflow library.

## Repository layout

A useful default for a private infrastructure repository is:

    AGENTS.md
    README.md
    deploy/
      <orchestrator>/
        <service>/
          docker-compose.yaml
          README.md
    inventory/
    docs/
      architecture.md
      migrations/

Use `deploy/<orchestrator>/<service>/` when manifests contain provider/parser-specific semantics. A generic `stacks/<service>/` layout remains reasonable only when the deployment definition is intentionally orchestrator-neutral.

Keep each deployable service in its own directory so the runtime platform can watch and redeploy only the affected deployment.

## Coolify specialization

When the runtime control plane is Coolify and it parses Docker Compose, also load `coolify-compose.md`. Parser-managed environment variables, domains and file mounts are part of the desired-state contract and must be validated on a freshly parsed resource.

## Git-backed deployment pattern

Prefer a Git-backed application/deployment source when the orchestrator supports it.

Typical flow:

1. infrastructure code changes on a working branch;
2. review/merge establishes the desired state;
3. the deployment platform watches the relevant path or receives a deploy webhook;
4. it reparses the stack and redeploys only that service;
5. runtime and consumer-facing acceptance are verified.

Avoid UI-only Compose definitions when the same configuration can live in Git and be reviewed, recovered and modified by automation.

## Watch-path isolation

When several stacks live in one repository:
- give each runtime resource a narrow watch path such as `stacks/<service>/**`;
- avoid repository-wide redeploy triggers unless cross-stack coupling actually requires them;
- document any shared file that intentionally triggers multiple stacks.

This prevents unrelated documentation or another service change from causing unnecessary redeployments.

## Secrets

Git stores variable names and references, never secret values.

Prefer explicit required-variable contracts:

    environment:
      EXAMPLE_TOKEN: ${EXAMPLE_TOKEN:?}

The actual value belongs in the runtime secret/configuration provider.

Never commit:
- `.env` with real values;
- API tokens;
- private keys;
- webhook secrets;
- runner registration secrets;
- generated credentials.

## Browser/admin UI secret exposure

Treat an authenticated infrastructure browser session as a privileged secret-capable surface.

Masking in an admin UI is not a security boundary once a value is deliberately revealed. In the validated Coolify browser flow:

- a masked secret field was returned to the automation layer only as a redacted value;
- after a human manually activated the visibility/reveal control, the plaintext became available in the page DOM and therefore to the browser agent.

Operational rule:

- do not reveal real secrets in a shared browser session while an automation/agent has page access unless that disclosure is intentionally authorized;
- prefer inspecting secret names, scopes and references rather than values;
- use non-sensitive canary secrets when testing browser/DOM exposure behavior;
- navigate away or close the privileged page after the operation.

Assume other browser automation systems may have fewer protective filters than the current toolchain.

## Migration from UI-owned configuration

When moving an existing service from an orchestrator UI into Git:

1. capture the current known-good configuration exactly;
2. preserve volume names, persistent data contracts, domains and secret references;
3. commit the recovered configuration as a reference before refactoring it;
4. create the Git-backed deployment resource without destroying the old one;
5. validate the new deployment;
6. cut over only after runtime acceptance;
7. retire the old UI-owned definition after rollback is no longer required.

Do not combine recovery, refactoring and production cutover into one unverified change.

## CI runner infrastructure

When the goal is centralized compute rather than replacement of a provider's CI language, prefer native CI with self-hosted runner management:

    GitHub Actions ----\
                        +--> managed self-hosted compute/cache
    GitLab CI ---------/

Preserve provider-native workflow files, logs, checks and artifacts when possible.

A runner manager may own:
- host/worker pools;
- scheduling and queues;
- ephemeral runner lifecycle;
- cache;
- CPU/RAM/PID limits;
- isolation;
- telemetry.

It should not force migration to another pipeline language unless that is an explicit product decision.

## Validation levels

Keep these states separate:

- repository/config source validated;
- manifest parsed;
- deployment succeeded;
- service healthy;
- real consumer path accepted;
- replacement/cutover accepted.

A successful Compose parse or deployment is not proof that the service is ready for production use.

## Rollback

For infrastructure replacement:
- preserve the known-good deployment until the replacement is accepted;
- record enough configuration to reconstruct it;
- keep persistent data ownership explicit;
- avoid destructive deletion during exploratory migration.

Useful retired configurations may remain as clearly marked reference stacks when they preserve operational knowledge.
