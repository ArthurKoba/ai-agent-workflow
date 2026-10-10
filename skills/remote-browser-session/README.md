# Remote Browser Session Lifecycle

Load this skill **before** an agent accesses an existing browser, asks for a tab
grant, attaches to remote DevTools/Playwright, or installs/reloads a browser
extension in an operator's browser. This skill governs the **session and
permission lifecycle**, not browser UI testing or the implementation of an MCP
connector.

## Outcome

Reuse an existing suitable authorized session whenever possible. Otherwise,
request **one** new session with the needed capabilities, allow the operator
time to approve it, and keep using that same session throughout the task.
Never multiply browser sessions, tabs or permission prompts through polling or
connection retries.

## Procedure

### 1. Discover the existing browser and session state

Before any connect, initialize, open-tab, or permission-request operation:

1. Identify the browser provider selected by the Project (for example,
   external Playwright, remote DevTools or a managed browser). Discover its
   configured endpoint from its authoritative settings or live connector
   status. Do not guess an address from an old report or switch providers
   because one command is inconvenient.
2. Inspect **read-only** connection/session status, accessible session
   inventory, target browser identity and already granted capabilities.
   Include a current session handle owned by this agent, if one exists.
   Distinguish the external operator's browser from a separate managed
   Chromium profile.
3. Check whether a currently authorized session is **actually reusable**
   through the supported connector; a visible session owned by another agent
   is not automatically shareable. Do not disconnect, reset or take over an
   active session belonging to another agent.
4. Choose the required tab from existing accessible tabs when permitted.
   Do not open a duplicate of an existing application tab to discover it.

**Decision:** If a usable session already has the needed permissions and
target access, select it and continue. Do **not** create another session.

### 2. Determine permission requirements *before* requesting access

Derive capabilities from the actual task and the provider's supported
permission model:

- Read/inspect pages and existing tabs.
- Navigate, click and fill only when the task requires interaction.
- Use DevTools/DOM/network inspection when browser debugging is required.
- Inspect, install, reload or remove extensions only for explicitly authorized
  extension work; inspect and reload do not imply permission to uninstall.
- Use local build artifacts or file access only through supported, explicitly
  authorized mechanisms.

Check whether grants are scoped to a browser, profile, tab, origin, extension
or operation. Request the smallest sufficient set **together at the initial
authorization opportunity**; include extension management up front if the
task requires it. Do not claim permission exists merely because a tool is
listed. If the provider exposes grants only when a specific operation is
attempted, use its documented grant mechanism and await the operator; do not
invent scope flags or bypass its approval UI.

If the required capability is unavailable in the selected provider, report
that boundary; do not work around it with a different, unapproved profile.

### 3. Create one session only when needed

Create a new connection only if **no reusable authorized session** exists,
the existing one was explicitly denied/closed, or an independently justified
capacity/isolation requirement makes another session necessary.

1. Choose the confirmed endpoint and permission set.
2. Start **one** supported connector session and trigger **one** access request.
3. Capture its durable session/connection handle, provider, target browser
   identity, selected tab (when known), requested permissions and state.
4. Keep the connector process/session alive across tool calls and context
   changes; subsequent operations must use **the same handle**.

The session handle belongs in existing secure task/workspace state, not in
a tracked skill, source document, chat transcript or exposed logs if sensitive.
Never store credentials, authentication cookies or access tokens.

### 4. Wait for the operator's grant

Once a permission dialog is pending:

- Mark the **existing** session as `PENDING_APPROVAL`. Tell the operator
  which access is being requested once, then give them time to respond.
- Do not issue another initialize/connect, open a replacement tab or retry an
  access-triggering call in a loop. Do not interpret a slow response or an
  ordinary timeout as rejection.
- Use a non-invasive status operation **on the same session** only when the
  provider explicitly supports it without another prompt. Otherwise wait for
  the outstanding result or the operator's confirmation.
- When the operator says access was granted, resume/verify **that same
  pending session**, not a freshly initialized one.

An approval request remains associated with its original session; creating
a replacement does not transfer the grant.

### 5. Operate only through the authorized session

After grant, verify the **actual** browser/profile, tab identity and allowed
operations. Keep the session handle stable for navigation, UI inspection,
DevTools and extension work. A tab switch or page reload is not a reason to
create a second connection.

For extension work, first inspect installed extension identity/version and
the operator-approved target; use supported install/reload controls only on
that target. Do not switch silently to the managed-browser extension catalog
when the requested extension is in an external Chrome profile.

Record a narrow session checkpoint in the existing task context: provider,
session ownership/handle locator, selected target/tab, approved capabilities,
grant state and the next operation. Avoid creating a separate planning file.

### 6. Handle insufficient permission or a genuinely broken session

- **Insufficient grant:** Stop the blocked operation. Close **only this
  agent's owned session**, then request **one** replacement with the complete
  revised permission set. Wait for the operator to grant access on that new
  session before proceeding. Never silently request broader access or run
  simultaneous old and new permission requests.
- **Denied/revoked grant:** Stop using the affected session. Do not repeatedly
  request access; start one replacement only after the operator authorizes
  another attempt.
- **Timeout/transport error:** First inspect the existing connection and
  connector diagnostics. A timed-out tool call does not prove that the
  session was denied or lost. Do not initialize a new session as the first
  recovery step.
- **Other agents are active:** Never reset their sessions, browser profile
  or shared transport to repair this agent's connection. Escalate a real
  provider-level limitation rather than disrupting active work.
- **Additional capacity requested:** Add a separate session only when needed
  and supported by the provider, with explicit browser/profile isolation and
  ownership; avoid unnecessary parallel load.

Close an owned session only when the task ends and the operating contract
requires release, or when it must be replaced as above. Closing a session
must not close unrelated tabs, uninstall extensions or reset another agent's
work.

## Completion gate

Before browser operations, confirm:

- Existing sessions were checked; the selected connection was reused or a
  **single justified new** connection was created.
- The correct browser/tab and effective permission scope are verified.
- The operator's grant was awaited on that same session; no repeated prompts
  were produced by retries.
- Extension operations have their required, separately verified access.
- The session handle is preserved for subsequent actions and other agents'
  sessions remain untouched.

This skill defines workflow decisions. Project/local infrastructure owns
concrete endpoints, authentication transport, session IDs and connector
implementation. For tool or transport defects, investigate the authoritative
MCP implementation through `../service-engineering/README.md` rather than
circumventing the provider's access control.
