# GitHub integration for Zoomies

Status: **first administrator validated; GitHub App connection not yet fully accepted**.

Zoomies uses a GitHub App flow to observe queued GitHub Actions jobs and register ephemeral runners.

## First administrator

After the controller starts for the first time, Zoomies shows a one-time first-account flow.

Create the administrator using the setup token from the controller logs. Do not store the setup token or administrator password in Git.

Acceptance:

- the first-account page disappears after creation;
- normal sign-in works;
- the Overview reports `Connection: Live`.

## GitHub App

From the authenticated Overview, use **Connect GitHub** / **Installations**.

Do not pre-document exact permissions from memory. Record the actual App permissions, callback/webhook behavior and installation scope observed during the product flow.

Principles:

- use a dedicated GitHub App rather than a personal access token;
- grant only the permissions required by Zoomies;
- install it only for the repositories/owner scope intended for this runner fleet;
- do not grant workflow-write or repository-administration permissions unless the product demonstrably requires them;
- never commit App private keys, client secrets, webhook secrets or installation secrets.

## Acceptance before host enrollment

GitHub integration is accepted only when:

1. the App is created/connected;
2. the intended owner/repository installation appears in Zoomies;
3. the controller can observe GitHub-side queue state;
4. no unrelated repository scope is granted.

After that, continue with host enrollment and pool creation.
