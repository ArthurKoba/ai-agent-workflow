# Configure GitHub Actions runner pools

This guide is for the accepted Zoomies 1.3.4 pattern: a GitHub App connection, an Online embedded agent on **dedicated host rootless Docker**, and separate ephemeral runner pools. It is a reusable setup guide; live owner names, repository selections and fleet capacities belong to private infrastructure inventory.

## Preconditions

1. Finish first-admin setup and connect the intended GitHub App/installation as described in `GITHUB.md`. Confirm Zoomies reports a healthy connected installation.
2. In **Hosts**, confirm the embedded agent is Online and advertises the Docker backend. Confirm its Docker endpoint is the **dedicated rootless** socket from `HOSTS.md`, not host rootful Docker.
3. Determine the repository/organisation target, allowed workflow trust boundary, expected runner group and required capacity. GitHub organisation runners and personal-account repository runners are different registration scopes.
4. Confirm the host's qualified agent capacity and pool limits. The reference Compose defaults to a single agent slot; do not increase concurrency without revisiting CPU/memory/cgroup limits and host isolation.

## Pool creation

In Zoomies open **Pools → Create a pool**. For each pool, bind it to the correct connected GitHub installation and target, choose an explicit runner label and use Docker as the runner backend. Confirm the pool can schedule on the intended Online rootless Docker host.

| Property | Ordinary jobs | Docker-building/integration jobs |
| --- | --- | --- |
| Example `runs-on` label | `zoomies-linux-x64` | `zoomies-linux-x64-dind` |
| Backend | Docker on the dedicated rootless host | Docker on the same rootless host |
| Docker in jobs | `none` / disabled | `dind` |
| Ephemeral runners | Enabled | Enabled |
| Minimum ready runners | Zero if scale-to-zero is desired and supported | Zero if scale-to-zero is desired and supported |
| Capacity/limits | Within the agent's accepted slot and resource limits | Within the same capacity; allow for additional DinD sidecar resource use |
| GitHub scope/group | Appropriate installation target and intended runner group | Appropriate installation target and intended runner group |

The labels are reusable examples from the accepted test topology, not mandatory product-defined names. Use the labels actually configured for the installation, and propagate them consistently into workflow files. Do not assume that setting a label creates or broadens the GitHub App's permission scope.

**Never choose `host-socket`.** A Docker-building job must use `dind`. Its sidecar may be reported as privileged by Zoomies; under this accepted architecture that privilege is inside the dedicated rootless Docker user namespace, not host rootful Docker. The warning is still a reminder of kernel-sharing and container escape risk. It should be evaluated against the real host runtime, not globally suppressed without review.

## Workflow selection

For the ordinary pool:

```yaml
jobs:
  smoke:
    runs-on: zoomies-linux-x64
    steps:
      - run: echo "ordinary-runner-ok"
```

For the Docker-capable pool:

```yaml
jobs:
  docker-smoke:
    runs-on: zoomies-linux-x64-dind
    steps:
      - run: docker version
      - run: docker info
```

These fragments demonstrate label selection only; the accepted end-to-end smoke additionally checks out a repository, builds and runs a real image, and tests communication between separate containers on a dedicated Docker network.

The Zoomies repository migration wizard can propose workflow label replacements and PRs. Inspect its **Review** diff before approving a migration, especially for jobs requiring DinD, different trust boundaries or different runner groups.

## Acceptance for each pool

1. Confirm the intended GitHub repository/organisation sees the runner group/label and that Zoomies observes the `workflow_job` event or its fallback poller picks up the job.
2. Run an ordinary smoke job. Verify actual checkout/shell execution under the non-root runner account, success and a newly created ephemeral runner identity.
3. Verify the ordinary pool returns to zero live/busy/idle/queued runners, and the runner container has disappeared.
4. Run the DinD job with `docker version` and `docker info`; build and run an image, then validate traffic between separate containers on a dedicated Docker network.
5. Verify the DinD pool returns to zero live/busy/idle/queued runners and its runner **and sidecar** disappear from the rootless Docker daemon.
6. Confirm no pool exposes a host Docker socket and no job obtained host-root/Coolify deployment credentials. Capture run IDs and pool evidence without exporting secrets.
7. Run the same ordinary and DinD acceptance **again after a full host reboot** before declaring zero-touch host recovery. See `RECOVERY.md`.

Successful jobs and clean ephemeral teardown qualify **runner implementation**. They do not qualify backup restoration, reverse-proxy client-IP attribution, host reboot recovery or legacy runner retirement. Those remain independent environment-specific gates.
