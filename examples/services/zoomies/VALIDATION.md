# Zoomies validation history

This file separates observed acceptance from planned architecture.

## Stage 1 — controller bootstrap

Validated:

- Zoomies 1.3.4 controller starts under Coolify;
- controller health check succeeds;
- public HTTPS endpoint works through Coolify;
- controller serves HTTP internally on port 8080;
- embedded agent is disabled;
- no host Docker socket is mounted;
- controller state persists at `/var/lib/zoomies`.

## Stage 2 — Git-backed source-path migration

Validated using an in-place Coolify resource migration:

- the same resource was switched from an old repository path to:
  - Base directory `/deploy/coolify/zoomies`;
  - Compose location `/docker-compose.yaml`;
  - watch path `deploy/coolify/zoomies/**`;
- deployment completed successfully;
- resource returned healthy;
- login state survived;
- encryption-key shared-variable resolution survived.

Important finding:

Coolify can retain stale persistent-storage metadata from earlier Compose revisions. Do not confuse those records with the desired current mount contract.

## Stage 3 — administrator

Validated:

- first administrator exists;
- normal sign-in succeeds;
- authenticated Overview loads;
- controller reports a live application connection.

## Pending acceptance

Still required:

1. GitHub App connection and installation;
2. trusted host enrollment;
3. pool creation;
4. normal GitHub Actions job success;
5. Docker-in-Docker job success;
6. ephemeral runner teardown;
7. resource/capacity behavior;
8. legacy runner retirement decision.

The legacy runner remains rollback until these gates pass.
