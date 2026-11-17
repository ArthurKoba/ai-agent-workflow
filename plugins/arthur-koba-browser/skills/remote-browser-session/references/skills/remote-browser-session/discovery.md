# Browser session discovery and reuse

This module applies to an already-authorized browser or a request for
a remote/operator browser session. The goal is **one sufficient,
reusable, authorized connection**, not a fresh grant per operation.

## Reuse-before-reconnect gate

**Before any new initialization, attach, tab grant or new session**:
1. Identify the selected browser provider from current project configuration
   or live connector status. Do not guess a historical endpoint or switch
   providers after a timeout. Distinguish the operator's external browser
   from an isolated managed Chromium profile.
2. Inspect read-only connection/session state, browser identity, accessible
   tabs and effective grants. Look for a previously approved session owned
   by this agent, including its handle stored in *restricted, untracked*
   task state. A visible session owned by another agent is not shareable
   unless explicitly authorized.
3. If a prior session handle exists, test it with the provider's supported
   harmless status/tab-list operation **on the same endpoint and handle**.
   Verify returned tab identity and actual access, not merely HTTP 200,
   connector `connected` or a tool catalog entry.
4. Select the already-open authorized tab if suitable. Do not create a
   duplicate application tab just to rediscover it.
5. If the connector wrapper is broken, investigate that wrapper's state.
   A wrapper `connected: false`, TCP timeout or lost proxy session does
   not prove the upstream approved session or user grant expired.
   Use [transport diagnosis](transport-and-recovery.md) before creating
   a replacement connection.

**Decision:** reuse the existing approved session whenever it has
the needed target and capabilities. New sessions are permitted only
when none can be safely reused, a grant was truly revoked/denied or
separate capacity/isolation is justified by the provider and operator.
Do not reset another agent's active session or switch to a different
browser profile to avoid an authorization prompt.
