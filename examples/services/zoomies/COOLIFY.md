# Deploy Zoomies through Coolify

This guide describes the accepted single-host pattern: one Git-backed Compose resource performs a one-shot trusted host bootstrap and then runs one persistent unprivileged Zoomies controller with its embedded agent.

## Git-backed resource

Recommended repository layout:

```text
deploy/coolify/zoomies/
├── bootstrap/
│   ├── Dockerfile
│   └── entrypoint.sh
├── bootstrap-host.sh
└── docker-compose.yaml
```

Configure:

```text
Base directory: /deploy/coolify/zoomies
Docker Compose location: /docker-compose.yaml
```

Watch the actual runtime inputs, not README/runbook files. Typical Watch paths:

```text
deploy/coolify/zoomies/docker-compose.yaml
deploy/coolify/zoomies/bootstrap/**
deploy/coolify/zoomies/bootstrap-host.sh
```

A broad directory Watch path can make documentation-only commits redeploy the service.

## Clean-host contract

Qualified clean host:

- Ubuntu 24.04;
- systemd + logind;
- normal Coolify/rootful Docker already present;
- no Zoomies-native agent service;
- no existing conflicting dedicated runtime identity/state.

The one-shot bootstrap:

1. validates the host contract;
2. creates/reuses the dedicated unprivileged runtime identity;
3. allocates subordinate UID/GID ranges;
4. enables user namespaces and required AppArmor/rootless compatibility;
5. configures cgroup-v2 delegation;
6. enables the user's persistent systemd manager/linger;
7. installs rootless extras matching the already-installed `docker-ce` version;
8. installs/starts the user's rootless `docker.service`;
9. proves the real rootless Docker API and cgroup behavior;
10. prepares `/var/lib/zoomies/shared`;
11. exits.

The persistent Zoomies service starts only after bootstrap exits successfully.

## Generated public URL

The Compose declares:

```yaml
SERVICE_URL_ZOOMIES_8080: /
ZOOMIES_EXTERNAL_URL: ${ZOOMIES_EXTERNAL_URL:-${SERVICE_URL_ZOOMIES}}
```

The port-qualified magic variable owns Coolify routing to internal port 8080. The application-level URL is a normal overridable variable that defaults to Coolify's canonical generated service URL.

Validate both surfaces:

- the public HTTPS route answers;
- Zoomies startup/runtime reports a non-empty correct external URL.

A working proxy route alone does not prove the application received its own public URL.

## Shared encryption key

The Compose requires:

```yaml
ZOOMIES_ENCRYPTION_KEY: ${ZOOMIES_ENCRYPTION_KEY:?}
```

Store the value in the narrowest appropriate Coolify Shared Variable scope and point the generated resource variable at it, for example:

```text
ZOOMIES_ENCRYPTION_KEY={{project.ZOOMIES_ENCRYPTION_KEY}}
```

Do not commit the key and do not make `/etc/zoomies` writable as a fallback. Backups of controller state require the same encryption key.

## Persistence

Durable:

```text
zoomies-controller-data -> /var/lib/zoomies
zoomies-agent-state     -> /var/lib/zoomies-agent
```

Recreatable:

```text
rootless Docker image/container store
/var/lib/zoomies/shared
/run/user/<uid>/docker.sock
```

Named volumes use `nocopy`; bootstrap establishes the intended ownership before the persistent service starts.

## Lifecycle acceptance

Validate at least:

- clean creation from Git;
- repeat deployment;
- known legacy cache migration only when its structure is recognized;
- unknown/foreign persisted state fails closed;
- controller health;
- embedded-agent backend health;
- ordinary ephemeral job + teardown;
- DinD build/run + multi-container networking + teardown.

Treat reboot/recovery as a separate host lifecycle gate.

## Security

- one-shot bootstrap is the only privileged Compose service;
- persistent Zoomies is unprivileged;
- rootful `/var/run/docker.sock` is never mounted;
- jobs never receive the rootless host socket;
- `host-socket` pools are prohibited;
- DinD privilege remains inside the dedicated rootless Docker user namespace.
