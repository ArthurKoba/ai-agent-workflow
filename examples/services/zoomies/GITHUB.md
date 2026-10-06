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

Zoomies 1.3.4 uses GitHub's App manifest flow and shows the exact contract before leaving the controller.

Observed webhook endpoint shape:

```text
https://<zoomies-domain>/webhooks/github
```

Observed permissions for an organisation target:

```text
organization_self_hosted_runners: write
actions: write
metadata: read
contents: write
pull_requests: write
workflows: write
event: workflow_job
```

For a repository target, GitHub uses repository administration permission instead of the organisation runner-management permission:

```text
administration: write
```

Purpose observed in the Zoomies flow:

- runner-management write permission — register/remove ephemeral runners;
- `actions: write` — read workflow jobs and allow workflow cancellation from Zoomies;
- `metadata: read` — mandatory GitHub App metadata access;
- `contents: write`, `pull_requests: write`, `workflows: write` — migration wizard support;
- `workflow_job` — low-latency queue/scaling webhook.

If the migration wizard will never be used, review whether its repository-write permissions can be removed after setup. Revalidate actual product behavior after changing App permissions.

Principles:

- use the manifest-created dedicated GitHub App rather than a personal access token;
- install it only for the intended owner/repository scope;
- never commit App private keys, client secrets, webhook secrets or installation secrets.

## Acceptance before host enrollment

GitHub integration is accepted only when:

1. the App is created/connected;
2. the intended owner/repository installation appears in Zoomies;
3. the controller can observe GitHub-side queue state;
4. no unrelated repository scope is granted.

After that, continue with host enrollment and pool creation.


## Organisation versus personal account

GitHub has organisation-level self-hosted runners, but no personal-account-wide runner registration.

Therefore:

- an organisation target can serve multiple repositories through one installation/pool scope;
- a personal account uses a repository target written as `owner/repository`;
- each personal-account repository that should use Zoomies needs its own repository-target installation and pool, while the same Zoomies fleet/hosts can provide the compute.

For first acceptance on a personal account, prefer a private repository so untrusted public pull-request code cannot reach a newly commissioned self-hosted runner before the trust model is proven.


## Manifest creation details

Observed on GitHub.com with Zoomies 1.3.4:

- GitHub App names are limited to 34 characters;
- Zoomies' default name can exceed that limit for a long repository target, so set a shorter explicit name when needed;
- after GitHub authentication, the manifest creation page may show only the App name and a single confirmation button because the webhook URL, permissions and event subscriptions are carried in the manifest payload;
- for a personal-account repository target, GitHub creates the App under that personal account.

A short stable name such as `Koba Zoomies CI` is preferable to embedding a long repository slug in the App name.


## App creation versus installation

A successful manifest creation returns to Zoomies before installation is complete.

Observed sequence:

1. GitHub creates the App and returns the manifest exchange code;
2. Zoomies exchanges the code and seals the generated App private key in controller state;
3. GitHub may send an initial `ping` webhook immediately;
4. before an installation exists, Zoomies can reject that ping because it does not yet have an installation/webhook-secret context to validate against;
5. install the App on the intended repository/account target;
6. only after the installation is recorded should webhook acceptance be used as a connectivity check.

Do not treat a pre-installation rejected `ping` as proof that the public webhook endpoint is broken.


## Repository access at installation

GitHub asks whether the App installation should access:

- **All repositories** — all current and future repositories owned by the selected account;
- **Only select repositories** — an explicit subset.

Choose this independently from the Zoomies connection target.

For a fleet intentionally meant to serve the whole personal account, `All repositories` avoids revisiting the App installation every time a new repository is created. This broadens the App's repository scope, so use it only when the runner trust model is account-wide.

A repository-target Zoomies connection may still be created from a manifest that names one repository even when the underlying GitHub App installation has broader repository access. Validate what Zoomies actually exposes after finishing the installation instead of assuming App installation scope and pool/runner scope are identical.

## Installation callback boundary

After GitHub installs the App, it redirects back with an `installation_id`.

Observed behavior:

- GitHub can emit `installation.created` immediately;
- until Zoomies' local **Finish** step records the installation, that delivery can still be rejected for lack of local installation/webhook-secret context;
- complete **Finish** before judging webhook health.


## Multiple owner scopes

A single Zoomies controller can hold multiple GitHub App connections.

Validated pattern:

- one personal-account-owned App for personal repositories;
- one organisation-owned App for an organisation;
- each connection keeps its own App identity, installation ID, private key and webhook secret inside Zoomies;
- pools can later be attached to the appropriate connection.

For an organisation-wide CI fleet, create the App under the organisation and install it with **All repositories** when the trust model intentionally covers all current and future organisation repositories.

For a personal account, GitHub does not provide account-wide self-hosted runners. A GitHub App may be installed with **All repositories**, but the Zoomies connection target is still repository-scoped for runner registration. Broad App installation access therefore does not turn a personal-account repository connection into an account-wide runner target.

Treat these as separate concepts:

```text
GitHub App installation scope
    !=
Zoomies runner-registration target
```

## Validated owner examples

The live validation used two independent connections:

```text
personal account:
  App owner: personal account
  App installation: All repositories
  Zoomies target type: Repository

organisation:
  App owner: organisation
  App installation: All repositories
  Zoomies target type: Organisation
```

The organisation App requested `organization_self_hosted_runners: write`; the repository-target App used repository `administration: write` instead.

After local Finish, Zoomies should report each connection as `Connected` and healthy and should be able to verify GitHub API access.

## Webhook acceptance

Do not confuse App/API health with webhook acceptance.

During App creation and installation, GitHub can emit `ping` and `installation.created` before Zoomies has completed the local Finish step. Those deliveries may be rejected because the relevant installation/webhook secret is not yet registered.

After all installations are finished, validate webhook behavior again with a post-configuration GitHub event such as `workflow_job`. Until an accepted webhook is observed, Zoomies may fall back to polling GitHub; that is functional but slower and consumes more API quota.
