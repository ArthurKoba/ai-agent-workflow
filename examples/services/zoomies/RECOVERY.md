# Zoomies host recovery and cutover acceptance

This is the reusable operational checklist for the **single-host Coolify + rootless Docker + embedded-agent** Zoomies 1.3.4 preset. It is not evidence that a particular host has been reboot-tested.

The accepted runner implementation and full host recovery are separate gates. A successful Compose re-deploy, controller restart, or rootless Docker API check does **not** prove a host reboot.

## Authority and scope

- **Git** owns the reviewed Compose/bootstrap source.
- **Coolify** owns the live resource, generated domain, secrets, volumes and deployment lifecycle.
- **The host** owns the dedicated rootless Docker user service, user manager, cgroup delegation and persistent runtime/cache paths.
- **Zoomies/GitHub Actions** prove actual job dispatch, execution and ephemeral teardown.

Do not reboot a production host through a runner, a CI job or the Zoomies controller. Require an authorised host-maintenance channel and an accepted outage/recovery window. This preset does not grant that channel.

## Pre-reboot evidence and safeguards

1. Identify the actual host, its maintenance owner and any other applications affected by a host reboot. Do not assume a dedicated CI-only host.
2. Check Coolify reports the Zoomies application healthy and confirm the Git-backed Compose/ref plus configured generated URL. Record the current known-good revision and rollback path.
3. Confirm a stable external `ZOOMIES_ENCRYPTION_KEY`, plus a recoverable controller-data backup. For disaster recovery also preserve agent identity state or plan safe re-enrollment. A local Docker volume alone is **not** an off-host backup.
4. Ensure no ordinary or DinD job is running or queued in the pools before the maintenance event. Preserve the legacy runner while cutover is unfinished.
5. Record the configured runtime user/UID, rootless socket path and current rootless Docker service state. Verify the real Docker API as that user, not just the existence of a socket.
6. Record controller health, embedded-agent Online state, both pool identities/labels and currently connected GitHub Apps. Confirm the external URL and webhook URL are correct.
7. Preserve deployment/host logs covering the pre-reboot baseline. Never put keys, setup tokens or account credentials into evidence artifacts.

## Reboot and recovery test

Only an authorised host operator or established host-management integration performs the **full host reboot**. A container restart is not an acceptable substitute. Do not trigger a reboot when other services' recovery requirements, rollback or maintenance scope are unknown.

After the host is back:

1. Verify host systemd/Coolify and the ordinary rootful Docker control plane returned without manual repair.
2. Verify the dedicated user's linger and `user@<uid>.service` are active.
3. Verify the dedicated user's `docker.service` is active and the socket is owned/accessed by the intended runtime user.
4. Run a *behavioral* `docker info` through that user's rootless socket. Confirm rootless mode, cgroup v2, `systemd` driver, delegated cpu/cpuset/io/memory/pids controllers and a data root outside `/var/lib/docker`.
5. Verify Zoomies is `running:healthy`, uses the expected persistent controller and agent volumes, and has **not** gained privileges, extra capabilities, a rootful socket, or a native host `zoomies-agent.service`.
6. Verify the embedded host reconnects automatically with the Docker backend; the administrator and existing GitHub App connections work without re-enrollment. Confirm public HTTPS and Zoomies' own external/webhook URL.
7. Dispatch one ordinary ephemeral Actions job and one DinD job (image build/run plus communication between separate containers). Verify both finish successfully with fresh runner identities.
8. Confirm **both** pools return to zero live/busy/idle/queued runners, and the DinD sidecar and ephemeral runner containers have disappeared from the dedicated rootless Docker daemon.
9. Record host boot identity/time, job run IDs, screenshots/logs and any manual intervention. If intervention was required, recovery is **not** yet zero-touch accepted.

Do not claim reboot acceptance from pre-reboot job successes.

## Other environment-specific gates

**Reverse-proxy IP attribution.** Inspect the actual deployed reverse-proxy path and the observed peer IPs before setting Zoomies `server.trusted_proxies`. Trust only the real proxy address ranges; do not guess CIDRs or use an indiscriminate trust-all setting. Prove audit/rate-limit records show the correct original client IP, including a direct/untrusted forwarded-header negative test where feasible.

**Backup policy.** Back up the controller database volume and preserve the same external encryption key securely. Decide explicitly whether an off-host destination and a restore drill are required; if deliberately local-only, record who accepted that risk. Do not imply backup readiness from named-volume persistence.

**Coolify Watch paths.** Persist paths limited to deployment inputs (Compose, bootstrap scripts and build context). A documentation-only commit must not trigger a redeploy; a runtime-input change must still trigger one. Verify Coolify's saved setting, not just Git guidance.

**Legacy runner cutover.** Retain the known-good `github-runner` until the full reboot and post-reboot workload gates pass. Retirement is a separate, reversible change after validating real workflows, repository/pool labels and fallback arrangements.

**Webhook delivery.** Connected GitHub Apps and successful polled jobs do not alone prove that post-installation `workflow_job` webhooks are accepted. If low-latency webhook dispatch is part of the acceptance contract, inspect recent signed deliveries independently.

**Version changes.** The source preset is qualified for Ubuntu 24.04 and Zoomies 1.3.4. Host upgrades and Zoomies releases require a fresh compatibility and lifecycle pass, not an inherited acceptance claim.

## Failure and rollback

When recovery fails, first separate host boot/systemd, rootless Docker, Coolify/Compose, Zoomies agent, GitHub integration and job-level failures by their own logs and behavior. Do not run a destructive re-bootstrap, reset a persistent volume, rotate the encryption key or delete legacy runner state to conceal the failure.

Preserve the known-good Git ref and durable state. If necessary, re-enable the previously accepted runner workflow while investigating, without granting CI jobs host-root or rootful Docker privileges.

The gate is closed only when **full reboot + zero-touch service recovery + post-reboot ordinary/DinD runner acceptance** is evidenced, alongside the environment-specific security/backup/cutover decisions.

