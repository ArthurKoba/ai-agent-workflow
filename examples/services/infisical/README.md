# Infisical: self-hosted Secrets Manager

**Single-node infrastructure preset:** one Coolify Compose resource for Infisical, its PostgreSQL 16 and Valkey 8.1. No shared DB, PgBouncer or additional KMS; **not runtime-certified** on the target Coolify release.

Infisical upstream uses Redis; this preset uses **Valkey**. Verify Redis API/queue compatibility before production use. Upstream: [Infisical Docker Compose](https://infisical.com/videos/self-host-infisical), [production Compose](https://github.com/Infisical/infisical/blob/main/docker-compose.prod.yml).

## What to copy

```text
infrastructure-repo/
  deploy/
    infisical/
      docker-compose.yaml
      docker-compose.coolify.yaml
      README.md
      COOLIFY.md
      VALIDATION.md
```

Copy the directory to your **own** infrastructure repository, record the source revision and watch that copy, not upstream `main`. One resource/network, two volumes: `postgres-data`, `valkey-data`. No DB/Valkey host ports. The standalone base requires an external reverse proxy; Coolify supplies a public route. App DB URL uses the internal alias `database:5432`; it resolves to the dedicated PostgreSQL today and can move to optional PgBouncer later without changing Infisical settings.

## Required operator inputs

| Key | Value/ownership |
| --- | --- |
| `SITE_URL` | Required absolute external `https://...` URL, set to the **actual** Coolify public domain, without trailing slash |
| `POSTGRES_PASSWORD` | Required protected secret; generate URL-safe characters only (hex recommended) |
| `VALKEY_PASSWORD` | Required protected secret; URL-safe; only the `default` ACL account is used |
| `ENCRYPTION_KEY` | Required Infisical master encryption key; **32 hex characters** from 16 random bytes |
| `AUTH_SECRET` | Required login/JWT secret; base64-encoded 32 random bytes |

`POSTGRES_USERNAME` and `POSTGRES_DATABASE` are optional with approved defaults `postgres`. Never generate `DB_CONNECTION_URI` or `REDIS_URL` as **extra** operator credentials: both are assembled in Compose from the above values and internal service DNS. URI embedding requires URL-safe passwords; avoid `%`, `@`, `:`, `/`, `#`, `?` and whitespace in these particular passwords. `VALKEY_USERNAME` remains the literal `default` because a separate ACL user is not needed in this isolated stack.

Generate inputs **locally in a trusted operator shell**, store in protected Coolify variables or an independent secret authority (not Git/chat/logs):

```sh
openssl rand -hex 32    # POSTGRES_PASSWORD (64 characters)
openssl rand -hex 32    # VALKEY_PASSWORD (64 characters)
openssl rand -hex 16    # ENCRYPTION_KEY (32 characters)
openssl rand -base64 32 # AUTH_SECRET
```

These values are **root-of-trust secrets**: Infisical cannot fetch its own startup secrets from itself. Back them up in an independent recovery authority. Changing `ENCRYPTION_KEY` can make stored ciphertext unreadable.

## Behavior and boundaries

- Images are explicitly versioned: Infisical `v0.167.1`, PostgreSQL `16.15-alpine`, Valkey `8.1.10-alpine`. Review [Infisical release migrations](https://upgrade.infisical.com/) before upgrading; never switch to `latest` by default.
- PostgreSQL initialization creates the configured user/database on the **first empty volume**. Changing an ENV after initialization does **not** rename credentials or an existing database. The simple initial role is privileged; use separate limited DB identities later only via an approved migration.
- Valkey creates a private `0600` ACL file at each startup and serves the `default` user with a generated password. Its AOF is persisted to `valkey-data`; no password is embedded in the server's command-line arguments. Test file permissions and authentication in the actual container image before accepting the deployment.
- Infisical runs its own schema migrations at startup. First signup generally creates the instance administrator: expose public signup only after you are ready to claim the instance and secure registration. SMTP is optional and belongs to a separately agreed mail configuration.
- The Coolify FQDN route is independent from Infisical's `SITE_URL`; verify both. Internal database/Valkey services never need separate public domains. On the first install, Coolify's secret-manager integration **for other resources** can be enabled only after this instance is healthy and its machine identity is configured.

Read [`COOLIFY.md`](COOLIFY.md) for installation and [`VALIDATION.md`](VALIDATION.md) for acceptance/backup. Do not execute a cutover or overwrite an existing instance from this preset without separate operator approval.
