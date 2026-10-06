# Deploy and migrate Zoomies through Coolify

This guide covers the validated controller-only deployment model and the in-place Git-path migration used for Zoomies.

## Git-backed resource

Recommended repository layout:

```text
deploy/coolify/zoomies/
├── README.md
└── docker-compose.yaml
```

Configure the Coolify application with:

```text
Base directory: /deploy/coolify/zoomies
Docker Compose location: /docker-compose.yaml
Watch paths: deploy/coolify/zoomies/**
```

The Compose location is relative to Base directory.

## Public endpoint

Expose the controller's internal HTTP port `8080` through Coolify/Traefik and terminate TLS at Coolify.

Set:

```text
ZOOMIES_EXTERNAL_URL=https://<zoomies-domain>
```

Keep `ZOOMIES_TLS_MODE=off` in the container when Coolify owns TLS.

## Shared encryption key

Declare the Compose variable:

```yaml
ZOOMIES_ENCRYPTION_KEY: ${ZOOMIES_ENCRYPTION_KEY:?}
```

Store the real secret at the chosen Coolify shared scope and point the resource variable at that reference, for example:

```text
ZOOMIES_ENCRYPTION_KEY={{project.ZOOMIES_ENCRYPTION_KEY}}
```

Do not commit the secret value.

## Persistent state

The critical volume is:

```text
zoomies-controller-data -> /var/lib/zoomies
```

The prebuilt image expects this state path and runs non-root. Preserve the native path instead of remapping controller state to an arbitrary directory.

## In-place repository-path migration

When the same Coolify resource already runs Zoomies from an older repository path, prefer an in-place source-path migration so the resource UUID and its UUID-prefixed controller volume remain stable.

Before the change:

1. confirm the resource is healthy;
2. record the current resource UUID and controller-state volume;
3. confirm the current `ZOOMIES_ENCRYPTION_KEY` reference;
4. confirm the public domain;
5. keep the old Git source available until acceptance.

Then update only the Git source contract:

```text
Base directory -> /deploy/coolify/zoomies
Docker Compose location -> /docker-compose.yaml
Watch paths -> deploy/coolify/zoomies/**
```

Reload/reparse the Compose source, inspect the parsed variables/storage, then deploy.

Acceptance:

- deployment finishes;
- resource returns `running:healthy`;
- controller login still works;
- controller state is preserved;
- `ZOOMIES_ENCRYPTION_KEY` remains resolved;
- webhook/watch-path redeploys are scoped to the Zoomies directory.

## Stale parser storage

An existing resource can retain storage records created by older Compose experiments.

Do not delete a stale storage record merely because the current Compose no longer references it. First prove:

1. the current running container does not mount it;
2. the desired Git Compose does not reference it;
3. its data is not needed for rollback.

Only the controller-state volume is part of the validated controller-only contract.

## Security boundary

The controller must not mount:

```text
/var/run/docker.sock
```

and should not run an embedded agent when the design calls for a separately enrolled trusted host.

Host-agent and DinD details are documented only after runtime acceptance.
