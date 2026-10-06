# Deploy Jenkins through Coolify

This guide deploys the Jenkins reference preset from `docker-compose.yaml`.

## Create the resource

Use Coolify on the intended server/project/environment.

Preferred deployment modes:

1. **Git-backed Docker Compose Application** when the preset is copied into a repository that should be the deployment source of truth.
2. **Docker Compose Service** for temporary/manual evaluation.

For long-lived agent-managed infrastructure, prefer Git-backed deployment so changes can be reviewed and recovered from Git.

## Compose

Use:

```text
examples/services/jenkins/docker-compose.yaml
```

If the preset is copied to another repository, keep the canonical filename `docker-compose.yaml`.

## Public endpoint

Expose only the `jenkins` component HTTP port `8080` through Coolify.

Assign an HTTPS domain in Coolify. Let Coolify own the reverse proxy and TLS certificate.

Do not publish:
- the Docker daemon port `2376`;
- an inbound-agent TCP port when WebSocket launch is used.

The builder connects to Jenkins over the internal Compose network using `http://jenkins:8080`, while Jenkins users access the public HTTPS URL through Coolify.

## Environment variable

Create a secret in the appropriate Coolify project/environment/shared-variable scope:

```text
JENKINS_AGENT_SECRET=<generated Jenkins node secret>
```

Reference that variable from the deployment. Never commit the value.

The first deployment does not require this value: the Compose preset supplies a `bootstrap-pending` placeholder so Jenkins can start before the node secret exists. The builder will remain offline until the real secret is added and the stack is redeployed.

The `SERVICE_URL_JENKINS_8080` variable is Coolify-managed service URL metadata and should not be treated as a reusable secret.

## Persistent volumes

Preserve these named volumes across redeployments:

- `jenkins-home` — Jenkins configuration, plugins, users and job state.
- `ci-workspace` — builder workspace.
- `ci-cache` — shared CI cache location.
- `ci-docker-data` — isolated Docker image/layer cache.
- `docker-cli` — Docker CLI copied for the builder.
- `ci-docker-tls` — DinD TLS material.

The `jenkins-home` volume is the critical state volume. Do not rename or delete it during an in-place redeploy unless a fresh Jenkins installation is intended.

## Deployment sequence

1. Save/validate the Compose definition in Coolify.
2. Deploy the stack.
3. Wait for the Jenkins component health check.
4. Complete Jenkins first-run setup.
5. Create `ci-builder-01` in Jenkins.
6. Store its generated secret in Coolify as `JENKINS_AGENT_SECRET`.
7. Redeploy.
8. Verify the node becomes online.
9. Run the Docker smoke test from the main README.
10. Verify resource limits.

## Security boundary

The stack intentionally does not mount the host Docker socket into Jenkins or the builder.

`ci-docker` is privileged because Docker-in-Docker requires that capability, but the resulting daemon is isolated from the host Docker control socket and reachable only through the private Compose network using TLS.

Do not route untrusted public-fork code onto a persistent trusted builder without an explicit trust/approval or ephemeral-runner boundary.
