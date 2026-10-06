# Zoomies CI Reference Preset

Status: **controller/Coolify migration validated; GitHub App, host enrollment, pools and DinD acceptance in progress**.

This preset supports a controller-only bootstrap and a hardened single-host mode where the controller embeds the agent but receives only a dedicated rootless CI Docker socket, never the system-wide rootful Docker socket.

## Validated version

```text
Zoomies: 1.3.4
```

Revalidate the setup after meaningful Zoomies upgrades.

## Architecture

Current validated bootstrap:

```text
GitHub
  |
  v
Zoomies controller
  public HTTPS through Coolify
  no host Docker socket
  embedded agent disabled
  |
  +-- persistent controller state
```

Target CI architecture for one Compose/Coolify host:

```text
GitHub Actions
     |
     v
Zoomies controller + embedded agent
     |
     v
dedicated rootless Docker daemon
     |
     +-- ephemeral runners
     +-- DinD sidecars only for jobs that require Docker
```

Additional runner machines use standalone agent containers.

The controller must not receive the host rootful `/var/run/docker.sock`.

## Files

- `docker-compose.yaml` — controller-only reusable Compose.
- `COOLIFY.md` — Git-backed Coolify deployment and in-place migration procedure.
- `GITHUB.md` — first-admin, GitHub App and repository migration notes.
- `HOSTS.md` — host enrollment, rootless runtime and Docker-mode contract.
- `bootstrap-host.sh` — one-shot fail-closed rootless Docker runtime bootstrap.
- `agent-compose.yaml` — preferred standalone agent container using the prepared rootless socket.
- `VALIDATION.md` — observed acceptance state and remaining gates.

## Controller configuration

The published image uses `/var/lib/zoomies` for controller state. Preserve the named volume on that native path:

```text
zoomies-controller-data -> /var/lib/zoomies
```

The Compose preset deliberately keeps:

```text
ZOOMIES_AGENT_EMBEDDED=false
ZOOMIES_TLS_MODE=off
ZOOMIES_BIND=0.0.0.0:8080
```

Coolify owns the public TLS boundary.

## Required runtime variables

```text
ZOOMIES_EXTERNAL_URL
ZOOMIES_ENCRYPTION_KEY
```

Keep the encryption key in a Coolify shared variable at the narrowest useful scope. Do not commit it.

## Bootstrap sequence

1. Deploy the controller.
2. Confirm the health check passes.
3. Create the first administrator.
4. Sign in and verify the Overview reports a live connection.
5. Connect GitHub using the product's GitHub App flow.
6. Prepare the trusted host's rootless runtime once, then enable the embedded agent against that socket (or use a standalone agent container for additional hosts).
7. Create a first pool with conservative capacity.
8. Validate one normal GitHub Actions job against that pool.
9. Validate Docker-in-Docker for workflows that require Docker.
10. Use **Migrate repositories** to rewrite existing `runs-on` labels, review exact diffs and open PRs across the intended repositories.
11. Retain the legacy runner until real workload acceptance succeeds and migration PRs are accepted.

Do not promote later steps to "validated" until the real job path has succeeded.
