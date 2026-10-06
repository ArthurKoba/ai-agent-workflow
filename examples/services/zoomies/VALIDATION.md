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


## Stage 5 — multi-owner GitHub connections

Validated:

- personal-account GitHub App created and connected;
- personal App installation granted **All repositories**;
- Zoomies repository target connected and API verification succeeded;
- organisation-owned GitHub App created for a second owner scope;
- organisation App installation granted **All repositories**;
- organisation target connected and API verification succeeded;
- Zoomies reported two healthy GitHub connections simultaneously;
- both connections had healthy API quota readings.

Observed architecture difference:

- personal-account connection remains repository-scoped for runner registration even when the App installation can access all personal repositories;
- organisation connection is organisation-scoped and can use organisation self-hosted runner management.

Webhook acceptance remains pending until a post-Finish GitHub event is accepted. Pre-Finish `ping` and `installation.created` rejections are recorded but are not acceptance failures.


## Stage 6 — host enrollment contract

Validated from the Zoomies 1.3.4 host wizard and runtime/security documentation:

- standalone agents connect outbound to the controller;
- a direct HTTPS controller address is sufficient;
- join tokens are single-use and short-lived;
- capacity and host labels are bound during enrollment;
- the agent runtime can be pinned with `ZOOMIES_DOCKER_HOST` / `--docker-host`;
- runtime autodetection prefers rootless sockets before `/var/run/docker.sock`;
- rootless Docker is supported;
- Docker-in-Docker is a pool mode and must be accepted with a real job;
- `host-socket` is not part of the accepted architecture.

A first 15-minute enrollment token was intentionally discarded before use because the rootless runtime had not yet been proven. No host is marked accepted yet.


## Stage 7 — reproducible rootless host bootstrap

A reusable one-shot rootless-runtime bootstrap is now part of the preset.

Static validation completed:

- Bash syntax validation passes;
- the script is idempotent by construction around existing user/socket/service state;
- cgroup v2 is required;
- root/sudo/docker-group exposure is treated as a blocker;
- the accepted runtime must report Docker rootless mode;
- the accepted runtime socket must be owned by the Zoomies user;
- the bootstrap deliberately does not enroll/install the agent.

Live host acceptance remains pending until the bootstrap is executed on the target host and the resulting agent/runtime capabilities are observed in Zoomies.


## Stage 8 — standalone agent container contract

Validated from Zoomies 1.3.4 upstream documentation:

- `ghcr.io/eyupio/zoomies-agent` is the supported standalone agent image;
- the agent container redeems `ZOOMIES_JOIN_TOKEN` on first start;
- the lasting host credential is persisted in the agent state volume;
- later starts reuse that credential without another join;
- `ZOOMIES_AGENT_NAME` should be explicit for stable unique host identity;
- the agent image runs unprivileged;
- the agent requires a runtime socket only for its own runner-container management;
- workflow jobs do not receive that socket unless a pool explicitly selects `host-socket`.

Preset-specific hardening:

- use the dedicated rootless Docker socket rather than `/var/run/docker.sock`;
- pass only the rootless socket-owning group to the agent container;
- keep `host-socket` pool mode prohibited;
- remove the spent join token from deployment environment after first successful enrollment.

Live container-agent acceptance remains pending.


## Stage 9 — embedded rootless single-host contract

Validated from Zoomies 1.3.4 deployment/configuration documentation:

- Docker Compose deployments support an embedded agent in the controller;
- the agent backend is selected independently through `ZOOMIES_DOCKER_HOST`;
- rootless Docker is supported as an agent backend;
- the runtime socket is Zoomies' control plane for creating runner containers and is not given to workflow jobs unless a pool explicitly selects host-socket mode.

For a single Coolify host, the preset therefore permits an embedded agent when the controller receives only the dedicated rootless CI daemon socket. This removes standalone-agent join-token/state lifecycle while preserving separation from the system-wide rootful Docker daemon.

Live embedded-agent acceptance remains pending.
