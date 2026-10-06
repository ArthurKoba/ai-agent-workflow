# Zoomies CI Reference Preset

Status: **controller/Coolify migration validated; GitHub App, host enrollment, pools and DinD acceptance in progress**.

This preset keeps the Zoomies controller as a public scheduler/UI only. It does not mount the host Docker socket and does not embed a runner agent in the controller container.

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

Target CI architecture:

```text
GitHub Actions
     |
     v
Zoomies controller
     |
     | outbound agent enrollment
     v
trusted host agent
     |
     +-- ephemeral runners
     |
     +-- DinD runner mode for jobs that require Docker
```

The controller must not receive the host rootful `/var/run/docker.sock`.

## Files

- `docker-compose.yaml` — controller-only reusable Compose.
- `COOLIFY.md` — Git-backed Coolify deployment and in-place migration procedure.
- `GITHUB.md` — first-admin and GitHub App integration notes.
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
6. Add a trusted host running the Zoomies agent.
7. Create a first pool with conservative capacity.
8. Validate one normal GitHub Actions job against that pool.
9. Validate Docker-in-Docker for workflows that require Docker.
10. Use **Migrate repositories** to rewrite existing `runs-on` labels, review exact diffs and open PRs across the intended repositories.
11. Retain the legacy runner until real workload acceptance succeeds and migration PRs are accepted.

Do not promote later steps to "validated" until the real job path has succeeded.
