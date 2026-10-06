# Service Presets

Reusable service deployment presets for common infrastructure components.

Each preset should be self-contained and safe to publish. A typical preset contains:

```text
<service>/
├── README.md
├── COOLIFY.md
└── docker-compose.yaml
```

## Contract

- `docker-compose.yaml` is the canonical Compose filename for presets in this directory.
- Presets contain no real credentials, private keys, domains, host addresses or environment-specific resource IDs.
- Required secrets are represented by variable references such as `${EXAMPLE_SECRET:?}`.
- `README.md` explains the service architecture and application-level setup.
- `COOLIFY.md` explains how to deploy the preset through Coolify.
- A preset may preserve a previously validated architecture even when it is not the preferred current product choice; its status must be stated explicitly.

## Available presets

- `jenkins/` — Jenkins controller with a dedicated inbound builder and an isolated TLS-protected Docker-in-Docker daemon.
