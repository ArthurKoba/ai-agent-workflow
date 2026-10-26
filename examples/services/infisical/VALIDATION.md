# Acceptance and recovery: Infisical

**Before production use** (especially with Valkey instead of upstream Redis), establish the following evidence in the target Coolify and Docker versions:

- **Generic source:** standalone `docker-compose.yaml` parses, has exactly `infisical`, `postgres`, `valkey` and two named volumes. It does not depend on Coolify extensions or expose host ports. External HTTPS reverse proxy is required outside Coolify.
- **Coolify parser:** `docker-compose.coolify.yaml` expands all three `extends`, repeats both top-level volumes, materializes five Required inputs and optional PostgreSQL defaults, and generates exactly one public FQDN route to `infisical:8080`.
- **Bootstrap:** empty PostgreSQL volume initializes; both PostgreSQL and Valkey report healthy before Infisical starts; Infisical `/api/status` responds. Confirm the alias `database:5432` resolves to PostgreSQL and no shell/URI parsing problem with URL-safe passwords.
- **Access:** public `https` origin equals `SITE_URL`; first administrator signup works, login/session survives an application restart, and a test secret can be created and read through Infisical. Validate machine identity/API retrieval separately before using Coolify Secret Manager integration.
- **Isolation:** PostgreSQL `5432` and Valkey `6379` are not published to the host/public internet. Valkey requires authentication and the ACL file is owner-readable only. Check the actual images, container UID/GID and `valkey-data` AOF persistence after restart.
- **Persistence:** verify the **physical Docker volume names** saved by Coolify, restore a test PostgreSQL backup with the **same `ENCRYPTION_KEY` and `AUTH_SECRET`**, confirm encrypted secrets can still be decrypted, and separately inspect Valkey cache/queue behavior.
- **Recovery:** track the last-good Infisical image and database schema before upgrading; PostgreSQL schema migrations may be forward-only. Recover using a tested backup and saved bootstrap secrets, not only a Git SHA revert.

This preset is **source-validated** until its actual Coolify parser/deployment, Valkey compatibility, and data-restore behavior have been verified. Record runtime results in the private deployment repository, not here. Never collect or commit secret plaintext as evidence.
