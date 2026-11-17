# Browser operations, release and verification

Operate through the one selected, authorized browser/session with the
actual scope established by
[discovery](discovery.md) and [approval](permissions-and-approval.md).

## Execute with stable identity

- Verify the precise browser/profile and tab before navigation or
  inspection. Reuse a current open tab when allowed; do not create
  duplicates due to a lost wrapper response.
- Read-only inspection or snapshot does not imply authorization to
  click, type, debug CDP, manage extensions or install software.
- For extension tasks, verify installed extension identity and version
  and the operator-approved target before supported install/reload.
  Inspect/reload grants do not grant uninstall.
- Retain a narrow checkpoint in secure existing task context:
  provider, session ownership and handle locator, selected tab/profile,
  effective permissions, approval state and next operation. Do not
  create a second public plan or expose token/session values.

## Insufficient grant or failed session

- Insufficient grant: stop that operation. After operator approval,
  close only this agent's owned session if replacement is necessary
  and ask for **one** replacement with the revised complete scope.
  Do not silently request a broader grant or run simultaneous prompts.
- Denied/revoked grant: stop using it. Reattempt only with explicit
  renewed consent.
- Timeout/disconnect: inspect existing session, connector diagnostics
  and any in-flight operation before retry. Do not initialize or reset
  a browser as the first step.
- Another agent's active session: never reset, take over, close its
  tabs or clear its profile.
- Extra capacity: another isolated session is an exception requiring
  a documented need, supported isolation and explicit authorization.

Release this agent's owned session when the task ends and the operating
contract requires it, or when an authorized replacement makes it
obsolete. Never close unrelated tabs or uninstall extensions as
an implicit cleanup.

## Completion gate

- Existing sessions were checked before a single justified new one.
- Correct browser/profile, tab, permissions and active connection
  were demonstrated by actual supported operations.
- Approval was awaited on the same session; no repeated prompts
  were caused by retries.
- Extension and DevTools privileges were checked separately.
- Session state remains recoverable for the task, and other agents'
  sessions, tabs and profiles were preserved.

Tool defects belong to the **project's provider/integration owner**,
not to generic session workflow rules. Do not replace an integration's
concrete API description with this universal Skill.
