# Zoomies hosts and runner runtime

Status: **single-host embedded agent on dedicated rootless Docker accepted; ordinary and DinD runner paths accepted**.

## Default single-host model

For a host that already runs the controller through Coolify/Compose, use the controller's embedded agent against a dedicated host rootless Docker daemon.

```text
controller + embedded agent
        |
        v
/run/user/<uid>/docker.sock
        |
        v
rootless Docker (dedicated unprivileged user)
        |
        +-- ordinary ephemeral runner
        `-- runner + DinD sidecar
```

This avoids a second persistent agent container, a join token and a separate host credential lifecycle for the first machine.

## Why rootless Docker lives on the host

Running rootless Docker nested inside the normal host Docker would require a permanently privileged outer container. The accepted pattern therefore uses a privileged one-shot deployment bootstrap to create the dedicated host user service, then leaves only the unprivileged persistent Zoomies service.

Rootless is a blast-radius boundary, not a VM boundary. Containers still share the host kernel.

## Rootless acceptance

Do not accept the backend from socket existence alone. Prove:

- user `docker.service` is active;
- socket owner is the configured runtime UID and owner has read/write;
- `docker info` succeeds as that user;
- Docker reports `rootless`;
- cgroup v2 is active;
- cgroup driver is `systemd`;
- cpu/cpuset/io/memory/pids are delegated to the user's systemd service;
- Docker data root is not `/var/lib/docker`.

The bootstrap in this preset qualifies Ubuntu 24.04 only.

## Embedded-agent configuration

The Compose sets:

```text
ZOOMIES_AGENT_EMBEDDED=true
ZOOMIES_AGENT_NAME=<stable name>
ZOOMIES_AGENT_CAPACITY=<slot count>
ZOOMIES_AGENT_LABELS=<optional labels>
ZOOMIES_AGENT_BACKEND=docker
ZOOMIES_DOCKER_HOST=unix:///run/user/<uid>/docker.sock
ZOOMIES_AGENT_DOCKER_BUILD_CACHE_MB=0
```

Embedded enrollment is internal to Zoomies; no operator-managed join token is required for the local host.

## Pool Docker modes

### none

Use for ordinary CI:

- checkout;
- dependency install;
- lint/typecheck;
- compile/link;
- unit tests;
- application builds that do not require a Docker daemon.

No Docker daemon is exposed inside the job.

### dind

Use when the workflow itself needs Docker operations:

- `docker build` / `docker run`;
- service containers;
- multi-container integration tests;
- Compose-like container topologies.

Zoomies creates a private Docker-in-Docker daemon sidecar for the runner. The sidecar is privileged, but under this preset it is created by the dedicated rootless host daemon rather than host rootful Docker.

Runtime acceptance must include a real image build/run and a multi-container networking test.

### host-socket

Prohibited.

It would mount the host runtime socket into the job and give the workflow authority over that daemon.

## Ephemeral acceptance

For each pool:

1. queue a job with the pool's explicit label;
2. observe a new runner identity;
3. complete the job;
4. verify the runner is removed;
5. verify pool live/busy/idle/queued counters return to zero.

Run ordinary and DinD pools separately so Docker capability is opt-in rather than universal.

## Additional hosts

For extra machines, Zoomies also supports standalone agents. `agent-compose.yaml` remains an optional reference for that topology.

That path has a different lifecycle:

- run the reviewed `bootstrap-host.sh` on the additional host;
- set the standalone deployment's runtime UID/GID/socket variables from the accepted rootless runtime;
- mint a one-time join token;
- persist the standalone agent credential;
- remove the spent join token after enrollment.

Do not confuse this optional multi-host path with the accepted single-host embedded-agent default.
