# Zoomies CI Reference Preset

Status: **single-host rootless controller + embedded-agent path accepted, including ordinary ephemeral runners and Docker-in-Docker jobs**.

This preset captures the accepted one-host architecture for Zoomies 1.3.4 behind Coolify. It keeps the deployment entrypoint in one Compose file, uses a privileged one-shot bootstrap only to prepare the host rootless Docker runtime, and leaves the persistent Zoomies service unprivileged.

## Validated version

```text
Zoomies: 1.3.4
```

Revalidate the preset after meaningful Zoomies or host-runtime upgrades.

## Accepted architecture

```text
Coolify / rootful Docker
  +-- zoomies-bootstrap        trusted, privileged, one-shot
  |     `-- prepares/validates dedicated host rootless Docker
  |
  `-- zoomies                  persistent, unprivileged
        +-- controller
        +-- embedded agent
        `-- /run/user/<uid>/docker.sock
                |
                `-- dedicated rootless Docker daemon
                      +-- ephemeral ordinary runner
                      `-- ephemeral runner + privileged DinD sidecar
```

The rootful host Docker socket is never mounted into Zoomies or jobs. A DinD sidecar is privileged inside the dedicated rootless Docker user namespace; it is not the host rootful daemon.

## Files

- `docker-compose.yaml` — accepted single-host Compose entrypoint.
- `bootstrap/Dockerfile` — one-shot bootstrap image.
- `bootstrap/entrypoint.sh` — volume preparation + host namespace handoff.
- `bootstrap-host.sh` — idempotent Ubuntu 24.04 rootless-Docker host bootstrap used by the one-shot container.
- `COOLIFY.md` — Coolify parser/deployment contract.
- `GITHUB.md` — GitHub App connection and credential-rotation notes.
- `HOSTS.md` — rootless host, embedded-agent and pool-mode contract.
- `VALIDATION.md` — demonstrated acceptance and remaining non-runner gates.
- `RECOVERY.md` — host reboot, zero-touch recovery, proxy, backup, Watch paths and legacy-runner cutover acceptance.
- `test-contract.sh` — runnable non-privileged regression checks of the reusable Compose/bootstrap contract.
- `agent-compose.yaml` — optional additional-host standalone-agent example; not the default single-host path.

## Security boundary

The deployment control plane is trusted infrastructure authority. The one-shot bootstrap may enter host namespaces because rootless Docker must live on the host; it exits after convergence.

The persistent Zoomies container:

- runs as the dedicated unprivileged runtime UID/GID;
- drops all Linux capabilities and uses `no-new-privileges`;
- sees `/run/user` read-only;
- explicitly talks only to its rootless Docker socket;
- never receives `/var/run/docker.sock`.

Jobs:

- ordinary pools use `docker_mode: none`;
- Docker-building/integration pools use `docker_mode: dind`;
- `host-socket` is prohibited.

## State

Durable controller state:

```text
zoomies-controller-data -> /var/lib/zoomies
```

Embedded-agent state:

```text
zoomies-agent-state -> /var/lib/zoomies-agent
```

Recreatable runtime/cache state:

```text
/home/zoomies/.local/share/docker
/var/lib/zoomies/shared
/run/user/<uid>/docker.sock
```

Preserve the controller database together with the same external `ZOOMIES_ENCRYPTION_KEY`.

## Required configuration

The preset defaults the dedicated runtime to UID/GID 1001. If you override the UID/GID, also override the socket path consistently.

```text
ZOOMIES_ENCRYPTION_KEY     required external secret
ZOOMIES_EXTERNAL_URL      optional explicit override under Coolify
ZOOMIES_RUNTIME_USER      default zoomies
ZOOMIES_RUNTIME_UID       default 1001
ZOOMIES_RUNTIME_GID       default 1001
ZOOMIES_RUNTIME_SOCKET    default /run/user/1001/docker.sock
ZOOMIES_AGENT_NAME        default zoomies-ci
ZOOMIES_AGENT_CAPACITY    default 1
ZOOMIES_AGENT_LABELS      optional
```

## Accepted pool pattern

Use separate labels/pools for different trust/capability needs.

Ordinary pool:

```yaml
runs-on: zoomies-linux-x64
```

- ephemeral;
- Docker backend;
- Docker in jobs: none.

DinD pool:

```yaml
runs-on: zoomies-linux-x64-dind
```

- ephemeral;
- Docker backend;
- Docker in jobs: DinD;
- separate privileged sidecar per job inside the rootless daemon.

The accepted DinD smoke covered daemon access, image build/run and communication between multiple containers.

## Completion boundary

Runner implementation is accepted when:

1. the rootless backend is healthy;
2. the embedded host is Online;
3. an ordinary ephemeral job succeeds and the runner disappears;
4. a DinD job builds/runs an image;
5. a DinD job can run multiple communicating containers;
6. both pools return to zero live/busy/idle/queued runners;
7. no pool uses `host-socket`.

Reboot recovery, reverse-proxy client-IP attribution, off-host backups and retirement of a legacy runner are operational hardening/cutover concerns, not reasons to pretend the runner path itself is still unproven. Follow `RECOVERY.md` before any full-host acceptance or retirement claim.

The reusable source contract can be checked with Bash, Python 3 and standard Unix utilities, without a Docker daemon, using `bash test-contract.sh`. The result is a **static/regression** gate only, not proof of Coolify deployment, real rootless Docker, or host reboot.
