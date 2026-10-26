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

## Reuse-before-reconnect gate (mandatory)

**Before any `initialize`, `browser_external_connect`, tab grant or new
session, test an already-approved session handle if one is available.** A
broken intermediary or its `connected: false` flag does not prove that an
upstream Playwright MCP session or its operator grant was lost.

1. Recover endpoint, `Mcp-Session-Id`, negotiated `MCP-Protocol-Version`,
   ownership and grant state from **restricted, untracked task/workspace
   state**. Never guess a handle or read another agent's secrets.
2. Test **the same handle** by calling `browser_tabs` with `action: list`
   via Streamable HTTP at the **same confirmed endpoint**. Check the MCP
   result and actual permitted tab, not merely an HTTP status.
3. If Koba Web fails, try the same approved session through its HTTP tool.
   If Koba Web itself is unavailable, a Project-authorized terminal/runner
   may POST to that **same endpoint and same handle**. This is transport
   recovery, not permission bypass. Do not switch to managed Chromium,
   reset sessions, or probe arbitrary hosts.
4. A timeout, `connected: false` or broken wrapper is **not** a revocation.
   Confirm invalid/expired state before requesting one replacement with
   explicit operator approval.

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
5. Locate the existing session handle and negotiated protocol in secure
   Task Context; wrapper connection state is not an upstream session registry.

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
or operation. For an approved extension-debugging task, establish up front
whether the operator's grant includes **tab read/navigation/click/type,
DOM/Console/Network, debugger/CDP, and installed-extension
inspect/reload/install**. Uninstall remains a separate destructive
authorization. Request the smallest sufficient set **together at the initial
authorization opportunity**; include extension management up front if the
task requires it. Do not claim permission exists merely because a tool is
listed. If the provider exposes grants only when a specific operation is
attempted, use its documented grant mechanism and await the operator; do not
invent scope flags or bypass its approval UI. MCP `initialize.capabilities`
describes protocol/client capabilities, **not browser permissions**. If
the connector offers no grant-scope parameters, describe the required
permissions to the operator and rely on its browser authorization UI.
Changing `clientInfo.name` cannot grant CDP or extension control.

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
   **Persist `Mcp-Session-Id`, negotiated protocol and approved endpoint
   immediately after `initialize`, BEFORE `browser_tabs` or any approval
   request. Verify recovery from approved, access-restricted, untracked
   task state before telling the operator to approve.** Keep sensitive
   handles out of chat, commits, logs, and tool-output transcripts.
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
   already connected, reuse it instead of requesting another grant. Even
   when `connected: false`, **check an existing upstream handle first**;
   the value describes only the proxy's local persistent client.
3. For a new approved session, call `browser_external_connect` **once**,
   **only when no reusable approved handle exists**.
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
   configured MCP HTTP endpoint, **first probe an existing approved session
   using that same handle, without `initialize`.** Try Koba Web's
   `curl_request` through the bridge. If `bridge_tools(web)` is
   `not_available`, the Web backend reports `Client is not connected`,
   or `curl_request` fails, use a **Project-authorized terminal/runner**
   capable of reaching that **same** confirmed endpoint with the **same
   approved session ID**. Do not invent a new endpoint or use a different
   browser profile. This recovers transport, not user permissions.
   Only when the old handle is conclusively unavailable and the operator
   has authorized a replacement should Koba Web's `curl_request` create
   **one** new MCP Streamable HTTP session. Send JSON-RPC
   `initialize` with `clientInfo` identifying this agent, supported
   `protocolVersion`, and `capabilities`; accept
   `application/json, text/event-stream`. **Immediately persist the
   negotiated version and `Mcp-Session-Id` response header**. Then send
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

**First: recover an existing approved Streamable HTTP session (NO
`initialize`, NO new permission prompt):**

```text
POST <same confirmed upstream MCP endpoint>
Accept: application/json, text/event-stream
Content-Type: application/json
Mcp-Session-Id: <previously granted session from restricted state>
MCP-Protocol-Version: <protocol negotiated by that session>
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"browser_tabs","arguments":{"action":"list"}}}
```

A correct `200` MCP response with the actual approved operator tab
demonstrates that the **original session is still usable**. A `200` from
`tools/list` alone tests only the protocol, not the tab grant. Verify
`result.isError`, `error` and actual `result.content`; parse either
JSON or `event: message` / `data:` SSE frames. Avoid printing raw
session headers, user tab URLs or network bodies.

When Koba Web's MCP backend is unavailable, a scoped terminal's Python
standard library (`urllib.request`) can issue this exact POST via the
already-authorized infrastructure path. The terminal must use the **same
existing handle**, and its URL/handle/version must be injected from
protected local task state, never hardcoded into a reusable skill or a
tracked helper:

```python
# Run only inside a Project-approved terminal with an approved session.
import json
import os
from urllib.request import Request, urlopen

endpoint = os.environ["APPROVED_MCP_ENDPOINT"]
session_id = os.environ["APPROVED_MCP_SESSION_ID"]
version = os.environ["APPROVED_MCP_PROTOCOL_VERSION"]
payload = {
    "jsonrpc": "2.0", "id": 1, "method": "tools/call",
    "params": {"name": "browser_tabs", "arguments": {"action": "list"}},
}
headers = {
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json",
    "Mcp-Session-Id": session_id,
    "MCP-Protocol-Version": version,
}
request = Request(endpoint, data=json.dumps(payload).encode(),
                  headers=headers, method="POST")
with urlopen(request, timeout=15) as response:
    raw = response.read(65536).decode()
json_text = (
    raw if raw.lstrip().startswith("{")
    else "\n".join(line[6:] for line in raw.splitlines()
                    if line.startswith("data: "))
)
reply = json.loads(json_text)
if reply.get("error") or reply.get("result", {}).get("isError"):
    raise RuntimeError("Existing MCP session could not list tabs")
blocks = [
    item.get("text", "")
    for item in reply.get("result", {}).get("content", [])
    if item.get("type") == "text"
]
# Inspect tab identities only in the approved private task context.
# Never print session headers, private URLs, credentials or full snapshots.
if not blocks:
    raise RuntimeError("No browser tab-list result; grant not verified")
print("Existing MCP session returned a tab-list response")
```

This example is a transport template, **not** an invitation to place
session identifiers in environment dumps, shell history or ordinary logs.
Use a protected mechanism to supply the variables and avoid echoing them.
If that mechanism is unavailable, stop and recover the credential locator
instead of bypassing permissions.

**Only when reuse is impossible and the operator approves a new grant:**

**New-session initialize sequence (illustrative JSON-RPC):**

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

**Failure classifier — do not infer a cause from one symptom:**

| Observed response | What it proves / next action |
| --- | --- |
| `browser_external_status.connected: false` | Only that wrapper's in-memory client is not connected. Verify the existing upstream handle first. |
| `bridge_tools(web): not_available` or `Client is not connected` | Koba Web proxy/backend unavailable; the approved upstream MCP may still work. Try the same handle via a permitted terminal. |
| Wrapper `Server returned an error response` | Non-specific: the failure may be MCP initialization, tool listing, tab listing or permission wait. Inspect source/logs, do not assume the grant expired. |
| `POST tools/call(browser_tabs)` returns a real tab under an existing handle | Existing session and tab access confirmed at that moment. **Do not create another session.** |
| `initialize` returns HTTP 200 + `Mcp-Session-Id` | MCP transport initialized only. Persist ID **before** first tab-grant request; permissions still unverified. |
| `tools/call` timeout or browser click stalls | Could be pending permission, transport, page execution or proxy timeout. Keep handle; investigate, don't immediately reinitialize. |
| Plain GET returns `400 Invalid request` | Not a valid MCP handshake test; cannot diagnose session from it. |
| Managed `devtools_list_pages` / `browser_pages` lists unrelated tabs | Different Chrome/profile. Don't manipulate it or claim external browser access. |
| Snapshot/evaluate reads work | Page read/DOM permissions only. Doesn't establish click, real CDP/debugger or extension management. |

**Evidence levels:** a server's MCP `200` is not a browser grant; a tab
listing is not debugger authorization; DOM and Network observations alone
do not prove Chrome extension-install/reload privileges. Also, a service
restart seen near a failure is correlation, **not proof** that the restart
caused the session failure.

**Incorrect shortcuts:** `browser_devtools_connect`,
`browser_devtools_target`, managed `browser_pages` and
`devtools_list_pages` do not inherently bind to the operator's external
Playwright session; they may control a different managed browser. Don't
call them as an alternate session recovery path unless the exact external
browser identity and permissions are independently established.

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
MCP implementation through `service-deployment/README.md` rather than
circumventing the provider's access control.
