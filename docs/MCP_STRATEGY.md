# MCP Strategy

Move repetitive, environment-heavy, error-prone or privileged operations into specialized MCP tools as early as practical.

A good MCP capability encapsulates dependency setup, credentials, environment, command syntax, validation, safe defaults and structured output.

## Preference
When provided by the project:
1. specialized project MCP;
2. structured connector/API;
3. controlled runner/shell;
4. manual user action only when physically/privileged necessary.

## Good MCP candidates
Operations repeated across agents/sessions, easy to invoke incorrectly, dependency-heavy, permission-sensitive, naturally structured or useful to audit centrally.

Examples:
- Git mutation/review;
- reverse database operations;
- immutable artifacts;
- HTTP/download/stream capture;
- CI/build orchestration;
- inventory/evidence ingestion.

## Tool contract
Prefer:
- typed parameters;
- dry-run for risky mutation;
- expected-state guards;
- deterministic outputs;
- provenance/identity reporting;
- capability/permission introspection;
- separate review and mutation surfaces where useful.

## Agent rule
If a specialized MCP exists, use it instead of rebuilding/installing the same workflow manually.

If capability is missing, report the gap. Do not silently bypass the project’s primary tool surface unless allowed.

Concrete MCP names, endpoints, presets and App identities belong in infrastructure authority, not the account prompt.
