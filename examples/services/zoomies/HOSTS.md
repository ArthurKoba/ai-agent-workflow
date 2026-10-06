# Zoomies hosts and runner runtime

Status: **host enrollment design validated from Zoomies 1.3.4 UI/docs; live rootless host acceptance pending**.

## Security boundary

The controller and runner runtime are separate concerns.

The controller must not receive the host Docker socket.

A standalone agent may use a container-runtime socket to create and remove runner containers, but workflow jobs do not receive that socket unless a pool is explicitly configured with the dangerous `host-socket` Docker mode.

For this preset:

- use a dedicated rootless Docker daemon for the trusted runner host;
- pin the agent to that daemon's Unix socket;
- do not use the host rootful `/var/run/docker.sock`;
- use pool `docker_mode: none` for ordinary jobs;
- use pool `docker_mode: dind` for jobs that need Docker;
- do not use `docker_mode: host-socket`.

## Runtime selection

Zoomies supports rootful/rootless Docker and rootful/rootless Podman.

The agent runtime socket is controlled by:

```text
ZOOMIES_DOCKER_HOST
```

or the equivalent agent flag:

```text
--docker-host
```

When left empty, Zoomies autodetects in this order:

1. `$DOCKER_HOST`;
2. `$XDG_RUNTIME_DIR/docker.sock`;
3. `/run/user/<uid>/docker.sock`;
4. Docker Desktop user socket;
5. `/var/run/docker.sock`.

For a hardened shared host, do not rely on the final rootful fallback. Pin the intended rootless socket explicitly after proving it exists and is reachable by the agent service account.

## Rootless acceptance

Prefer cgroup v2.

Before enrollment, validate:

- the rootless Docker daemon exists and stays up under systemd/user lingering or another persistent service model;
- its socket is reachable by the account Zoomies will run as;
- `docker info` through that socket succeeds;
- CPU, memory and PID-limit capabilities reported by Zoomies are usable;
- Docker-in-Docker is validated with a real job rather than assumed from daemon connectivity.

Rootless Docker on cgroup v2 can enforce delegated resource controllers when the host is configured correctly. A successful socket connection alone is not resource-limit acceptance.

## Agent enrollment

Hosts → Add a host generates a single-use, short-lived join token and one-line installer command.

Validated UI choices for a conservative first host:

```text
connection: direct outbound HTTPS
capacity: 1
host label: node=tambov-ci
join token TTL: 15 minutes
```

The installer:

- downloads a release-matched Zoomies binary and verifies it;
- redeems the join token;
- writes agent credentials;
- installs a persistent service;
- uses outbound-only communication to the controller.

Never store the join token in Git or long-lived documentation.

If runtime preparation is not complete, discard the generated token and mint a fresh one later instead of leaving a valid enrollment capability unused.

## Agent ownership

For a native root install, Zoomies creates/runs the agent as a dedicated unprivileged system user and gives it only the container-runtime access it needs. The systemd unit is sandboxed.

The agent owns its state/work directories and the runner containers it creates.

If the Docker daemon is shared or externally managed, set the agent Docker build-cache target to zero so Zoomies does not prune that daemon's builder cache:

```text
ZOOMIES_AGENT_DOCKER_BUILD_CACHE_MB=0
```

A dedicated rootless daemon for the Zoomies runner fleet may instead allow Zoomies to manage its own cache according to the chosen fleet policy.

## Pool Docker modes

`none`:
- default;
- no Docker daemon is exposed inside the job;
- preferred for ordinary build/test workflows.

`dind`:
- gives each runner its own private Docker daemon sidecar;
- preferred when a workflow builds/runs containers;
- must be runtime-validated on the selected rootless daemon.

`host-socket`:
- mounts the host runtime socket into the job;
- gives the job host-daemon authority;
- prohibited by this preset.

## Enrollment acceptance

A host is accepted only when:

1. it appears online in Zoomies;
2. the expected label is present;
3. capacity is the intended value;
4. backend reports the intended rootless Docker socket;
5. resource-limit capabilities are visible;
6. a normal runner can be created and destroyed;
7. a `dind` runner can complete a Docker smoke test;
8. no job receives the host runtime socket.
