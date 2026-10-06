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

## Stage 4 — GitHub App manifest discovery

Validated from the authenticated Zoomies 1.3.4 Installations flow:

- controller offers GitHub App manifest creation;
- webhook endpoint is derived from the controller external URL at `/webhooks/github`;
- target scope is explicitly either organisation or single repository;
- the UI exposes the exact requested GitHub App permissions before redirecting to GitHub;
- personal-account use requires repository-target installations because GitHub has no account-wide personal runner registration.

Additional observed details:

- the generated default App name can exceed GitHub's 34-character name limit for a long repository target;
- the manifest creation page accepted the shortened App name and was ready to create the App under the personal account;
- GitHub authentication is a user-interactive step; credentials are not handled by the automation.

Observed after manifest creation:

- GitHub App object creation completed and Zoomies sealed the generated key;
- the controller advanced to the explicit installation step;
- GitHub delivered a `ping` webhook before installation existed;
- Zoomies rejected that early ping because no installation/webhook-secret context was configured yet.

This is expected pre-installation behavior, not webhook acceptance.

Observed installation stage:

- GitHub installation was granted **All repositories** for the personal account;
- GitHub redirected back with an installation ID;
- `installation.created` arrived before the controller's local Finish step and was rejected for the same missing-local-installation context as the earlier ping.

No GitHub installation is marked accepted until the local Finish step records the installation and Zoomies shows it as connected.

## Pending acceptance

Still required:

1. complete the first repository-target GitHub App installation;
2. trusted host enrollment;
3. pool creation;
4. normal GitHub Actions job success;
5. Docker-in-Docker job success;
6. ephemeral runner teardown;
7. resource/capacity behavior;
8. legacy runner retirement decision.

The legacy runner remains rollback until these gates pass.
