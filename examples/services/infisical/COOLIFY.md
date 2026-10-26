# Coolify: Infisical deployment

Use one Git-backed **Docker Compose Application**. Do not create separate Coolify PostgreSQL/Valkey resources: they already belong to this Compose stack. Copy the preset into the infrastructure repository first, then configure:

| Setting | Value |
| --- | --- |
| Repository / branch | The owned infrastructure repository / approved branch |
| Base Directory | `/deploy/infisical` |
| Compose Location | `/docker-compose.coolify.yaml` |
| Watch Paths | `deploy/infisical/**` (save and verify) |
| Domain target | Compose service `infisical`, port `8080`, via `SERVICE_FQDN_INFISICAL_8080` |
| External storage | Two **named volumes**, not Coolify File Mounts |

1. Validate the three services shown after Coolify parses `extends`. Inspect Deployable Compose, the three service images, `postgres-data`/`valkey-data` volume attachments, internal service DNS and the generated route. If inheritance drops a volume, env or healthcheck, stop before deploy and fix the parser-specific entrypoint. Do not make an unreviewed live deployment just to test inheritance.
2. Choose/create the Coolify HTTPS domain for the `infisical` service. Set `SITE_URL` separately to the **same final HTTPS public origin**. `SERVICE_FQDN_INFISICAL_8080` is a proxy directive, not a safe substitute for `SITE_URL` inside application ENV.
3. Fill the five **Required** inputs from `README.md`. Set secret flags/protected storage appropriately. Coolify and the selected server must be able to resolve the chosen secret references **before** the first container starts; Infisical itself cannot provide them. The generated `POSTGRES_USERNAME=postgres` and `POSTGRES_DATABASE=postgres` defaults can remain unchanged.
4. Verify `POSTGRES_PASSWORD` and `VALKEY_PASSWORD` are URL-safe before deploying. Both are interpolated into `DB_CONNECTION_URI` and `REDIS_URL` by Compose. Do not print or copy resolved values during agent review. Ensure Buildtime is **off** for runtime-only credentials.
5. Confirm PostgreSQL/Valkey have **no published host ports**, and only the UI/API route is public. Keep the Coolify resource network private. Start the resource only after verifying env, routes, storage, images and root-of-trust backup location.
6. Complete the **first administrator** registration through the actual HTTPS URL, restrict ongoing access/registration as the product permits, and then set up the machine identity/Coolify Secret Manager connection for **other** resources. Do not attempt to bootstrap this resource from Infisical itself.

### State and upgrades

One Compose resource owns three services. The named volumes will usually receive **resource/project-specific physical names** under Coolify. Record the actual mappings before migration, backup or replacement; a Compose volume key by itself does not identify the underlying data. Avoid changing Compose service names, volume keys, project name or database version without explicit migration planning.

For upgrades pin a reviewed Infisical release after checking release notes and migrations, back up PostgreSQL and encryption keys, and verify startup with the current database; a Git rollback may not reverse schema changes. Changing a Coolify domain also requires changing `SITE_URL` and checking redirects/cookies. Use [`VALIDATION.md`](VALIDATION.md) for acceptance and restore criteria.
