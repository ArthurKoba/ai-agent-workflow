# Browser permissions and one-session authorization

Read after [discovery and reuse](discovery.md) establishes that the selected
browser does not already provide sufficient authorized capabilities.

## Determine access before the prompt

Derive the least privileged grant from the actual task and current
provider's permission model:
- Inspect existing tabs or page content only when needed.
- Navigate, click or fill only for an authorized interaction task.
- Debug DOM, Console, Network or DevTools/CDP only for the requested
  investigation.
- Inspect, install and reload browser extensions only with explicitly
  granted extension-management capabilities; uninstall is a separate
  destructive decision.
- Read local artifacts/files only through explicitly authorized and
  actually supported mechanisms.

Determine whether scope is tied to tab, origin, profile, extension,
browser or operation. When the provider supports up-front selection,
request the complete **smallest sufficient** bundle for this task in
**one** approval request. Do not ask repeatedly for each missing action.
If the provider exposes scopes only during actual use, rely on the
documented grant mechanism and operator's approval UI. MCP protocol
`initialize.capabilities` is not a grant of browser permissions.
Changing `clientInfo.name` does not grant debugger/extension rights.

If the selected provider cannot offer the needed capability, report
that boundary. Do not use a different profile/session to evade denial.

## Create and retain one session

Only after reuse is ruled out:
1. Confirm target browser identity, endpoint, task, exact permission set
   and operator authorization to request one new session.
2. Use the selected connector's **supported** session/attach operation
   once. Do not assume any particular tool name exists.
3. Retain provider, browser/profile, session handle, selected tab,
   negotiated protocol, request scope, approval state and ownership in
   the **existing secure, untracked task context**. For stateful MCP
   Streamable HTTP, retain the negotiated protocol and session ID
   immediately after initialization, **before** the first tab access.
   Do not put sensitive handles/cookies/tokens in chat, Git, logs or
   normal environment dumps.
4. Keep using that exact handle across tool calls and context changes;
   opening a tab or switching tabs is not an excuse to reconnect.

## Waiting for the operator

When a permission dialog is pending, mark **that session** pending
and explain the needed access once. Do not spam another connect,
initialize or tab request. A slow tool response or generic timeout
is **not** rejection. Poll read-only status only if supported without
creating another prompt. Once the operator grants access, resume the
same pending session and verify the actual browser/tab and effective
grants before interacting.

Approval is session-specific. A replacement session does not inherit
the first approval. If the operator denies or revokes permission,
stop and request a new grant only after explicit renewed authorization.
