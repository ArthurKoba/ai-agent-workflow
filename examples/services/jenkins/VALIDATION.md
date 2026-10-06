# Jenkins validation and debugging history

This document records the sequence that produced the final reference Compose architecture.

It is useful because several settings in `docker-compose.yaml` exist specifically to close problems discovered during runtime acceptance.

## Acceptance surface

The validation Pipeline executed on the dedicated inbound builder, not on the Jenkins controller.

The final acceptance covered:

- Docker CLI available in the builder;
- remote Docker daemon reachable;
- Docker Engine functional;
- disposable containers functional;
- Docker API protected by TLS;
- TLS server identity valid for the Compose DNS name;
- builder CPU/RAM cgroup limits active;
- per-job container CPU/RAM/PID limits active.

## Stage 1 — functional prototype

The first Docker smoke test succeeded with an unencrypted Docker TCP endpoint.

The test proved:
- the builder could execute `docker version`;
- the builder could execute `docker info`;
- `docker run --rm alpine:3.22 echo CI_DOCKER_OK` succeeded.

However Docker reported that the API was reachable through insecure TCP `2375`.

That configuration was rejected as the final design.

**Do not recreate the insecure `2375` stage.** It is documented only to explain the migration path.

## Stage 2 — enable TLS

The builder was switched to:

```text
DOCKER_HOST=tcp://ci-docker:2376
DOCKER_TLS_VERIFY=1
DOCKER_CERT_PATH=/certs/client
```

The first TLS run failed with an x509 hostname error: the DinD certificate was valid for container-generated names such as `docker`/`localhost`, but not for the Compose service DNS name `ci-docker`.

This is why the final DinD configuration includes:

```yaml
environment:
  DOCKER_TLS_CERTDIR: /certs
  DOCKER_TLS_SAN: "DNS:ci-docker"
```

After regenerating the DinD TLS material with that SAN, the same Docker smoke test succeeded over `2376`.

## Stage 3 — Docker daemon logging

The isolated daemon was then started with:

```text
--storage-driver=overlay2
--log-driver=local
```

The smoke test remained successful.

The `local` logging driver avoids unbounded default JSON log growth for disposable CI containers.

## Stage 4 — resource acceptance

The builder cgroup reported:

```text
cpu.max    = 50000 100000
memory.max = 805306368
```

This corresponds to the configured:

```text
0.5 CPU
768 MiB RAM
```

A disposable job container was then launched with:

```text
--cpus=1
--memory=1g
--pids-limit=256
```

Inside that container the observed limits were:

```text
cpu.max    = 100000 100000
memory.max = 1073741824
```

and the job returned:

```text
CI_LIMITS_OK
```

## Final acceptance criteria

The reference stack is accepted only when all of the following are true:

1. Jenkins controller is healthy.
2. Built-In Node has zero executors.
3. Dedicated inbound builder is online with one executor.
4. `docker version` reaches the isolated daemon over TLS `2376`.
5. No host Docker socket is mounted.
6. A disposable Alpine container returns `CI_DOCKER_OK`.
7. Builder cgroup CPU/RAM limits match the Compose limits.
8. A limited disposable job container reports the requested CPU/RAM limits and `CI_LIMITS_OK`.

If TLS fails with a hostname mismatch, verify `DOCKER_TLS_SAN=DNS:ci-docker` and recreate the DinD TLS material rather than disabling certificate verification.
