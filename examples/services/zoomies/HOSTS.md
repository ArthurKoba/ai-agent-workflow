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

## One-shot rootless runtime bootstrap

Use `bootstrap-host.sh` once per runner host. It prepares only the unprivileged runtime; it does **not** install a native Zoomies agent.

The bootstrap is idempotent and fail-closed. It:

- creates/reuses the dedicated `zoomies` account;
- locks password login;
- removes `docker`, `sudo` and `wheel` group membership;
- refuses passwordless sudo;
- installs rootless Docker prerequisites;
- requires cgroup v2;
- enables persistent user services with systemd lingering;
- installs/starts rootless Docker under the `zoomies` uid;
- verifies socket ownership and Docker's reported `rootless` security mode;
- refuses the rootful Docker data root;
- writes the accepted uid/gid/socket values to `/etc/zoomies/rootless-runtime.env`.

Root is used only for this host bootstrap. No Zoomies agent process is installed as a root-owned native service.

Run the reviewed bootstrap once:

```bash
curl -fsSL <pinned-bootstrap-url> | bash
```

For production, pin the URL to a reviewed commit rather than a moving branch. The script prints the accepted uid/gid/socket values and writes them to `/etc/zoomies/rootless-runtime.env`.

## Preferred standalone agent: container

Zoomies officially supports a standalone agent container. This is the preferred pattern for Compose/Coolify-managed hosts.

Use `agent-compose.yaml`.

On the first start:

1. `ZOOMIES_JOIN_TOKEN` is redeemed once;
2. Zoomies receives a lasting host credential;
3. that credential is stored in `zoomies-agent-data`.

On subsequent starts, the volume credential is reused. The one-time join token is no longer needed and should be removed from the deployment environment after acceptance.

The image runs as an unprivileged account. It needs access to a container-runtime socket because it creates runner containers as siblings, not nested containers.

The upstream example mounts the host rootful `/var/run/docker.sock`. This hardened preset deliberately does not. Instead it bind-mounts the dedicated rootless socket prepared by `bootstrap-host.sh`:

```text
host: /run/user/<zoomies-uid>/docker.sock
container: /run/zoomies/docker.sock
```

The numeric group owning that rootless socket is passed through with `group_add`.

Required deployment variables:

```text
ZOOMIES_CONTROLLER_URL=https://<zoomies-domain>
ZOOMIES_JOIN_TOKEN=<fresh single-use token; first start only>
ZOOMIES_AGENT_NAME=<stable unique host name>
ZOOMIES_RUNTIME_GID=<from /etc/zoomies/rootless-runtime.env>
ZOOMIES_RUNTIME_SOCKET=<from /etc/zoomies/rootless-runtime.env>
ZOOMIES_IMAGE_TAG=v1.3.4
```

A container hostname is not a stable fleet identity across multiple hosts, so set `ZOOMIES_AGENT_NAME` explicitly.

For a first host, mint the token in **Hosts → Add a host** with conservative capacity and labels. Those token-bound values win during enrollment.

After the host becomes Online, remove `ZOOMIES_JOIN_TOKEN` and redeploy. Do not delete `zoomies-agent-data`; losing it requires a new join token and a new enrollment.

## Native agent alternative

The one-line native installer is also supported. On systemd hosts, root/sudo is needed only to write/install the system service. The resulting service runs under a dedicated unprivileged account.

For a Compose/Coolify-managed environment, prefer the standalone agent container above because its lifecycle and persistent credential are represented directly in deployment state.

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
