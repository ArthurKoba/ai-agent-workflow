# Zoomies validation history

This file separates demonstrated acceptance from reusable design.

## Accepted baseline

Validated service version:

```text
Zoomies 1.3.4
```

### Controller / Coolify

Demonstrated:

- clean Git-backed deployment;
- one Compose deployment entrypoint;
- one-shot privileged bootstrap exits successfully;
- persistent Zoomies runs unprivileged;
- public HTTPS route works through Coolify;
- application external URL resolves correctly;
- controller state persists on its native path;
- required encryption key is supplied externally.

### Rootless host runtime

Demonstrated:

- dedicated runtime user;
- rootless Docker user service;
- real Docker API access through the dedicated socket;
- rootless security mode;
- cgroup v2 with systemd driver and delegated controllers;
- rootless data root distinct from `/var/lib/docker`;
- embedded agent joins the controller and advertises Docker backend;
- no native Zoomies agent service is required.

### GitHub App connections

Demonstrated:

- first administrator flow;
- GitHub App manifest/manual-existing-App paths;
- organisation target connection;
- personal-account repository target connection;
- credential rotation by generating a new App private key and setting the same webhook secret on GitHub and Zoomies;
- existing App import requires App ID, Installation ID, target, PEM private key and webhook secret;
- App private keys/webhook secrets are sealed in controller state.

Do not use personal access tokens as the runner-management authority.

### Ordinary ephemeral runner

Demonstrated:

- explicit ordinary pool label;
- Docker backend with Docker-in-jobs disabled;
- runner group selection;
- GitHub job checkout and shell execution;
- unprivileged runner user;
- different runner identities on sequential jobs;
- zero live/busy/idle/queued runners after teardown.

### Docker-in-Docker

Demonstrated:

- separate explicit DinD pool label;
- private Docker daemon available inside the job;
- `docker version` and `docker info`;
- image build;
- container run;
- communication between multiple containers on a dedicated Docker network;
- cleanup and return to zero pool counters.

The DinD daemon uses a privileged sidecar created by the dedicated rootless host Docker daemon. `host-socket` is not part of the accepted architecture.

## Acceptance boundary

Runner implementation is accepted when both ordinary and DinD jobs pass and their ephemeral runners are torn down.

For reproducible source-level regression checks on the public preset, run `bash test-contract.sh` from this directory. This does **not** test an actual rootless daemon, Coolify runtime or host reboot.

The following are operational/environment hardening rather than runner-implementation proof:

- host reboot/recovery;
- reverse-proxy trusted-client-IP configuration;
- off-host backup policy;
- narrowing orchestrator Watch paths;
- retirement of any pre-existing legacy runner after cutover.

Do not promote these untested concerns into a false claim that the runner path itself is still unproven, and do not claim full host/product readiness until the environment-specific gates that matter to that deployment are actually tested. The host-level recovery and cutover matrix is in `RECOVERY.md`; no reusable test script or historical Actions run can replace the required full-host reboot evidence.
