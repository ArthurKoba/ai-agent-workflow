# Remote browser transport and recovery

Use this only for a real connector transport/session problem, not normal
tab navigation. The selected project's browser tool remains the
authority for available operations. This Skill contains no vendor
endpoints, tool names, credentials or protocol-version assumptions.

## Classify instead of replaying connections

- Wrapper disconnected or internal error: may mean wrapper state was lost,
  not that the upstream operator session or grant expired.
- Tool timeout after navigation: may mean page execution, approval pending,
  transport stall or proxy timeout; it does not prove session revocation.
- MCP initialization succeeded: protocol transport only, *not* tab access.
- A tool catalog lists browser methods: it does not grant tab, CDP or
  extension permissions.
- Read-only page/DOM access: does not imply click, debugger or extension
  install rights.
- A different managed profile lists tabs: not evidence of access to the
  operator's external browser.
- Browser process restart near a failure: correlation, not root-cause proof.
- GET returning a protocol 400: may simply be an unsupported probe; do
  not classify the session from an invalid handshake.

## Preserve an approved existing session

1. Inspect documented provider diagnostics and the approved session
   locator from protected task state.
2. Test a harmless supported operation on the **same** session and
   confirmed upstream endpoint. Validate the returned permitted tab.
3. If the project supports an alternative **authorized** transport to
   the same endpoint/handle, use that only with explicit authorization,
   protocol support and permission scope. It is transport recovery,
   not permission bypass. Never probe arbitrary origins or another
   browser profile.
4. Only when the old handle is confirmed unusable, request operator
   approval for **one** replacement and use the selected provider's
   normal documented connection mechanism. Do not build an ad hoc
   bridge/terminal script or invent a tool to avoid a failed connector.

For MCP Streamable HTTP where a stateful session was negotiated, the
`Mcp-Session-Id` and `MCP-Protocol-Version` must match the original
session. Persist them securely, do not print them. The client's
`initialize` and `notifications/initialized` handshake may finish
before a tab-list operation triggers browser authorization. Check
JSON-RPC errors and real result content (including SSE framing if
supported), not a bare HTTP 200. A new initialize with a new session
ID is not recovery of the old session or its browser grant.

## Rights are not transport state

Never retry the same blocked mutation merely via a different provider
or transport. A pre-tool safety block or explicit permission rejection
is a distinct stop boundary. Escalate the connector defect to its
owning integration; this universal Skill does not describe provider
implementation or offer a hidden direct-HTTP bypass.
