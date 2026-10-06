# Jenkins CI Reference Preset

Status: **validated reference architecture**.

This preset reproduces a Jenkins deployment where the controller manages the queue/UI only, builds run on a dedicated inbound agent, and Docker workloads use an isolated Docker-in-Docker daemon instead of the host Docker socket.

Use it when Jenkins is intentionally selected as the CI control plane. If the goal is only centralized self-hosted compute while preserving GitHub Actions or GitLab CI syntax, prefer native runner management instead.

## Architecture

```text
Jenkins controller
  executors = 0
        |
        v
ci-builder-01
  executors = 1
        |
        | TLS :2376
        v
ci-docker
  isolated Docker daemon
        |
        +-- disposable test containers
        +-- PostgreSQL/Valkey/etc.
```

The controller never receives the host `/var/run/docker.sock`.

## Files

- `docker-compose.yaml` — reusable Compose stack.
- `COOLIFY.md` — deployment through Coolify.
- `GITHUB.md` — optional GitHub App and Organization Folder integration.

## Jenkins first-run setup

After the stack is deployed:

1. Open the Jenkins public URL.
2. Unlock Jenkins using the initial administrator password from `/var/jenkins_home/secrets/initialAdminPassword`.
3. Choose **Install suggested plugins**.
4. Create the first administrator account.
5. Confirm the externally reachable HTTPS Jenkins URL.
6. Go to **Manage Jenkins → Nodes → Built-In Node → Configure** and set **Number of executors** to `0`.

The built-in node remains the controller but does not execute CI jobs.

## Create the builder node

Go to **Manage Jenkins → Nodes → New Node**.

Use:

```text
Node name: ci-builder-01
Type: Permanent Agent
Number of executors: 1
Remote root directory: /home/jenkins/agent
Labels: ci-builder linux x64 docker
Usage: Only build jobs with label expressions matching this node
Launch method: Launch agent by connecting it to the controller
Availability: Keep this agent online as much as possible
```

Save the node and obtain its generated inbound-agent secret.

On the first deployment the Compose file intentionally uses a non-secret bootstrap placeholder, so the agent remains offline while the controller is configured. Store the generated node secret outside Git as `JENKINS_AGENT_SECRET`, then redeploy the Compose stack so `ci-builder-01` can authenticate and connect.

## Optional UI/integration plugins

Install only what the deployment needs.

Useful plugins from the validated setup included:

- **Locale** — optionally force the Jenkins UI language.
- **GitHub Branch Source** — normally included by suggested plugins.
- **GitHub Checks** — publish GitHub checks.
- **GitLab Branch Source** — GitLab repository/group discovery.

Do not install the Jenkins Docker plugin merely to execute `docker` commands with this preset. The builder already talks to the dedicated `ci-docker` daemon through the Docker CLI.

## Docker isolation

The builder connects to `tcp://ci-docker:2376` with TLS enabled.

The DinD service generates its own certificates under `/certs`, and `DOCKER_TLS_SAN=DNS:ci-docker` ensures the server certificate validates against the Compose service DNS name.

The Docker API is not published to the host or Internet.

## Resource model

The reference limits are:

```text
jenkins controller: 1 CPU / 2 GiB / 512 PIDs
builder agent:      0.5 CPU / 768 MiB / 256 PIDs
ci-docker daemon:   2 CPU / 4 GiB / 2048 PIDs
```

Individual disposable job containers should also receive their own limits when appropriate, for example:

```text
--cpus=1 --memory=1g --pids-limit=256
```

## Acceptance

A minimal Pipeline smoke test:

```groovy
pipeline {
    agent { label 'ci-builder' }

    stages {
        stage('Docker smoke test') {
            steps {
                sh '''
                    docker version
                    docker info
                    docker run --rm alpine:3.22 echo CI_DOCKER_OK
                '''
            }
        }
    }
}
```

Expected result:

```text
CI_DOCKER_OK
Finished: SUCCESS
```

Resource acceptance can be checked from the builder and a limited job container:

```groovy
pipeline {
    agent { label 'ci-builder' }

    stages {
        stage('Resource limits') {
            steps {
                sh '''
                    cat /sys/fs/cgroup/cpu.max
                    cat /sys/fs/cgroup/memory.max

                    docker run --rm \
                      --cpus=1 \
                      --memory=1g \
                      --pids-limit=256 \
                      alpine:3.22 \
                      sh -c 'cat /sys/fs/cgroup/cpu.max; cat /sys/fs/cgroup/memory.max; echo CI_LIMITS_OK'
                '''
            }
        }
    }
}
```

Do not call the deployment accepted until the builder is online, Docker TLS works, a disposable container completes successfully, and the intended resource ceilings are observed.
