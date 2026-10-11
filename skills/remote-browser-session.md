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

### External Playwright MCP via Koba Web — concrete connection path

Apply this subsection **only** when the Project selects the external Playwright
MCP provider exposed by Koba Web. These are provider-specific tool names, not
rules for all remote browsers. Resolve tool signatures and the endpoint from
**live MCP discovery/settings**; never hardcode an IP, port, browser profile,
protocol version or credentials in this reusable skill.

1. Discover `mcp__Koba_MCP_Bridge__bridge_backends`, then
   `bridge_tools({backend: "web"})`. The root tool catalog may expose only a
   subset of Web MCP's tools. Use
   `mcp__Koba_MCP_Bridge__bridge_call({backend: "web", tool_name: ...,
   arguments: ...})` for the backend's actual tools. Do **not** infer that
   `browser_devtools_connect` or `browser_pages` attaches to the operator's
   external Playwright session: those are distinct managed/DevTools surfaces.
2. Call `browser_external_status` **first**. Check `configured`, `enabled`,
   `connected`, provider and configured endpoint. `enabled: false` means the
   operator must enable **External Browser** in Admin; managed-browser
   Developer Access is a separate switch. If a usable external session is
   already connected, reuse it instead of requesting another grant.
3. For a new approved session, call `browser_external_connect` **once**.
   When it succeeds, retain its session and use the `external` browser tools
   through the same provider; select an existing permitted tab. The browser
   permission prompt may occur only when the first tab operation is attempted.
4. If this specialized connector fails **during MCP initialization** with a
   generic server error, inspect `browser_external_status` and connector
   diagnostics before changing anything. A confirmed server response to a
   proper MCP `initialize` request means it is reachable; it does **not**
   prove the wrapper completed its own handshake. Do not keep retrying
   `browser_external_connect`, ask for an endpoint already in Admin, reset
   another agent's browser or switch silently to managed Chromium.
5. **Conditional recovery when the native Web connector itself is broken:**
   with the operator's permission for this external browser and the confirmed
   configured MCP HTTP endpoint, use Koba Web's `curl_request` through the
   bridge to perform **one** MCP Streamable HTTP session. Send JSON-RPC
   `initialize` with `clientInfo` identifying this agent, supported
   `protocolVersion`, and `capabilities`; accept
   `application/json, text/event-stream`. Read the negotiated version and
   `Mcp-Session-Id` response header. Then send
   `notifications/initialized` **on the same session**. Invoke
   `tools/list` if tool names are not already verified, followed by
   `tools/call` with `{name: "browser_tabs", arguments: {action: "list"}}`.
   This tab-discovery call may be the actual **extension authorization
   trigger**: an operator-visible request identifies the `clientInfo.name`.
   This is an explicit fallback for a diagnosed connector defect, not the
   default route or a way around the extension permission dialog.
6. For every subsequent fallback `tools/call`, send that **same**
   `Mcp-Session-Id` and negotiated `MCP-Protocol-Version` headers. Parse MCP
   JSON-RPC responses from JSON or `event: message` / `data:` SSE frames,
   not from a guessed HTML page. Keep the session identifier only in secure,
   nontracked task state. Once the operator grants access, call
   `browser_tabs` with `action: "list"` again on that session, choose the
   already-open application tab, then inspect it with `browser_snapshot`,
   `browser_console_messages`, `browser_network_requests` and, if needed,
   read-only `browser_evaluate`. Never reopen or replace the tab just to find
   it. Browser interaction or mutation still requires its actual grant.

**Minimal Streamable HTTP fallback sequence (illustrative JSON-RPC):**

```text
POST <configured MCP endpoint>
Accept: application/json, text/event-stream
Content-Type: application/json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"<supported>","capabilities":{},"clientInfo":{"name":"<agent and task>","version":"1.0"}}}

POST <same endpoint> with Mcp-Session-Id: <response header>
{"jsonrpc":"2.0","method":"notifications/initialized"}

POST <same endpoint> with Mcp-Session-Id: <same header>
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"browser_tabs","arguments":{"action":"list"}}}
```

Use the negotiated `MCP-Protocol-Version` on subsequent requests. The first
request returns an MCP session handle; **the tab-list request may prompt the
human**. Do not confuse these two separate phases. After an actual grant,
repeat only the permitted tab operation using the same session handle.

**Observed failure distinctions:** `browser_external_status.connected: false`
means the specialized wrapper has no session; it does not by itself invalidate
an independently established, explicitly authorized fallback MCP session.
A plain HTTP `GET` returning `400 Invalid request` is **not** a valid MCP
handshake test. `Server returned an error response` from the wrapper can be an
MCP-client negotiation defect even when a valid JSON-RPC `initialize` gets
`200` with a session ID. An initialized MCP session is **not** proof of tab
access: wait for the operator's separate extension grant, then confirm tab
list and effective permissions before using it.

**Tooling owner:** diagnose or fix the wrapper in its owning MCP service so
agents can normally use `browser_external_connect` without the fallback.
Do not embed the external server address, a real session ID, authorization
headers, target tab URL or operator-specific extension state in this skill.

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
MCP implementation through `service-engineering/README.md` rather than
circumventing the provider's access control.
