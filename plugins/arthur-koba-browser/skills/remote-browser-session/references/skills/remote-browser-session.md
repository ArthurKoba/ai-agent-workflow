# Remote Browser Session Lifecycle

Use when an agent needs an operator-authorized remote browser,
external Playwright/DevTools attachment, existing tab access or
browser extension permissions. This is **generic session and
grant management**, not a specific MCP connector implementation
or a browser testing skill.

**Hard rule:** before attaching/initializing, always test whether
an existing approved session owned by this agent is actually
reusable. A wrapper disconnection is not revocation. Never
multiply browser tabs, sessions or permission prompts through
blind retries, and never use another profile to evade permissions.

Read modules by the current decision:
- [Discover and reuse](remote-browser-session/discovery.md) — browser
  identity, tab/session inventory, existing-grant checks.
- [Request appropriate permission](remote-browser-session/permissions-and-approval.md)
  — minimum scopes, one approval request and secure handle state.
- [Diagnose transport and reconnect](remote-browser-session/transport-and-recovery.md)
  — errors, stateful MCP, same-session tests and recovery stops.
- [Operate and finish](remote-browser-session/operation-and-completion.md)
  — controlled actions, extension permission, release and acceptance.

The selected project's actual browser tool owns its endpoint,
API names, secure identity handling and availability. This Skill
does **not** require a particular browser, provider, or
named integration. Never infer a capability from a tool's presence.
