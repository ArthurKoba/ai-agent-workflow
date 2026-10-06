# Deploy Jenkins through Coolify

This guide deploys the Jenkins reference preset from `docker-compose.yaml`.

## Create the resource

Use Coolify on the intended server/project/environment.

The validated deployment was a **Coolify Service** using the Docker Compose editor.

For reusable long-lived infrastructure there are two reasonable modes:

1. **Git-backed Docker Compose Application** when another repository should be the deployment source of truth.
2. **Docker Compose Service** when the Compose definition is intentionally managed in Coolify.

This preset was validated through the second mode. If moving it to Git-backed deployment later, preserve the same volumes, environment references, domain, and runtime behavior before retiring the old resource.

## Compose

Use:

```text
examples/services/jenkins/docker-compose.yaml
```

If the preset is copied to another repository, keep the canonical filename `docker-compose.yaml`.

## Network

The validated Coolify service used:

```text
Network attachment: Use the stack network only
```

No host Docker socket or host-level Docker TCP port is exposed.

## Public endpoint

Expose only the `jenkins` component HTTP port `8080` through Coolify.

Assign an HTTPS domain in Coolify. Let Coolify own the reverse proxy and TLS certificate.

The validated domain behavior was:

```text
service port: 8080
HTTP → HTTPS redirect: enabled
DNS: matching
indexing: enabled
```

Do not publish:
- the Docker daemon port `2376`;
- an inbound-agent TCP port when WebSocket launch is used.

The builder connects to Jenkins over the internal Compose network using `http://jenkins:8080`, while Jenkins users access the public HTTPS URL through Coolify.

## Environment variables

The validated Coolify setup kept the generated Jenkins node secret at a shared scope and referenced it from the Jenkins resource rather than duplicating the secret value.

### Shared/project variable

Create the sensitive value at the chosen Coolify shared scope, for example project-wide:

```text
JENKINS_AGENT_SECRET=<generated Jenkins node secret>
```

Mark it secret/sensitive according to the available Coolify controls. Never commit the value.

### Resource environment reference

In the Jenkins Coolify resource, expose the variable to the Compose deployment by referencing the shared variable instead of copying its value. For a project-scoped variable, the validated pattern was:

```text
JENKINS_AGENT_SECRET={{project.JENKINS_AGENT_SECRET}}
```

Use the equivalent Coolify reference syntax if the variable is stored at environment/team scope instead. The principle is: one stored secret value, explicit references from consumers.

The Compose file then consumes the runtime variable through:

```yaml
JENKINS_SECRET: ${JENKINS_AGENT_SECRET:-bootstrap-pending}
```

The first deployment does not require the real value: `bootstrap-pending` lets the controller start before a node secret exists. The builder remains offline until the real node secret is created in Jenkins, stored in Coolify and the stack is redeployed.

Coolify automatically adds service URL/FQDN metadata variables such as:

```text
SERVICE_URL_JENKINS
SERVICE_FQDN_JENKINS
SERVICE_URL_JENKINS_8080
SERVICE_FQDN_JENKINS_8080
```

Do not move these into manually maintained shared variables.

The remaining builder/DinD variables are derived directly from `docker-compose.yaml` and appear as component-scoped runtime variables in Coolify.

## Persistent volumes

Preserve these named volumes across redeployments:

- `jenkins-home` — Jenkins configuration, plugins, users and job state.
- `ci-workspace` — builder workspace.
- `ci-cache` — shared CI cache location.
- `ci-docker-data` — isolated Docker image/layer cache.
- `docker-cli` — Docker CLI copied for the builder.
- `ci-docker-tls` — DinD TLS material.

The `jenkins-home` volume is the critical state volume. Do not rename or delete it during an in-place redeploy unless a fresh Jenkins installation is intended.

Coolify prefixes named volumes with the service UUID to prevent collisions. The logical Compose names remain the source contract; do not copy Coolify's generated UUID-prefixed names back into the preset.

After changing volume definitions, Coolify may show **stale volume entries** from an older Compose revision. Treat those as runtime leftovers, not desired state. Remove a stale entry only after confirming the current Compose no longer references it and its data is not needed.

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
