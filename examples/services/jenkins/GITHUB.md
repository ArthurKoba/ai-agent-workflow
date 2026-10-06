# GitHub integration

This integration is optional. It is useful when Jenkins is intentionally used as the CI control plane for many GitHub repositories.

## Jenkins plugins

Install:

- GitHub Branch Source
- GitHub Checks

The GitHub Branch Source plugin may already be present after installing the suggested Jenkins plugins.

## GitHub App

Create a dedicated GitHub App for Jenkins rather than using a personal access token when repository-wide discovery/check publication is required.

Use the Jenkins public HTTPS URL as the homepage. Use the standard Jenkins GitHub webhook path:

```text
https://<jenkins-domain>/github-webhook/
```

Recommended repository permissions for the validated discovery/checks model:

```text
Contents: Read-only
Metadata: Read-only
Pull requests: Read-only
Commit statuses: Read and write
Checks: Read and write
```

Subscribe to the GitHub events exposed for those permissions. Do not grant unrelated repository administration, secrets, workflow-write or deployment permissions just to run CI.

Configure a high-entropy webhook secret. Store the same value in Jenkins Credentials as a **Secret text** credential.

The validated Jenkins configuration used:

```text
Manage Jenkins → System → GitHub → Advanced

Shared secret: GitHub webhook HMAC secret
Signature algorithm: SHA-256
GitHub API rate limiting strategy: Throttle at/near rate limit
```

Do not expose the secret value in documentation.

Generate a GitHub App private key and convert it to unencrypted PKCS#8 PEM before creating the Jenkins **GitHub App** credential. The credential consists of the GitHub App ID plus that private key. Never commit the private key.

## Multiple GitHub installations

When the same public GitHub App is installed for multiple owners/organizations, do not rely on automatic installation selection if repository discovery becomes ambiguous.

Create one Jenkins GitHub App credential profile per owner while reusing the same App ID/private key, and restrict each credential to its owner through the credential's repository access strategy.

The validated owner-bound credential settings were:

```text
Repository access strategy: Specify accessible repositories
Owner: <one GitHub owner>
Repositories: empty
Default permissions strategy: All permissions available to the app installation
```

With no repositories listed, the credential can access any repository available to that App installation for the specified owner. This avoids installation ambiguity while keeping owner boundaries explicit.

Example:

```text
github-app-ci-owner-a -> owner-a
github-app-ci-owner-b -> owner-b
```

This keeps Organization Folder discovery deterministic.

## Organization Folder

Create an **Organization Folder** for each GitHub owner and add a **GitHub Organization** repository source.

Set:

```text
Credentials: owner-specific GitHub App credential
Owner: <GitHub owner or organization>
```

Recommended discovery behaviour for a persistent self-hosted builder:

```text
Discover branches:
  Exclude branches that are also filed as PRs

Discover pull requests from origin:
  Both the current PR revision and the PR merged with the current target branch revision

Discover pull requests from forks:
  disabled
```

Disabling fork PR discovery is deliberate for a persistent trusted self-hosted builder. Add a separate trust/approval or ephemeral isolation boundary before executing untrusted fork code.

The project recognizer should use the repository `Jenkinsfile` when Jenkins owns the pipeline definition.

The validated Organization Folder configuration also used:

```text
API endpoint: https://api.github.com
Scan Organization Triggers:
  Periodically if not otherwise run: enabled
  Interval: 1 day

Child Scan Triggers:
  Periodically if not otherwise run: enabled
  Interval: 1 day

Automatic branch project triggering:
  Branch names to build automatically: .*
  Suppression strategy: schedule all builds / nothing suppressed
```

Webhooks remain the primary near-real-time trigger; the one-day scan is a recovery/reconciliation path.

## Scope warning

This GitHub integration changes the CI control plane: repositories need a Jenkins pipeline definition. If the actual requirement is only self-hosted compute while preserving GitHub Actions workflow syntax and native GitHub logs/checks, use a native GitHub Actions runner manager instead of this Jenkins integration.
