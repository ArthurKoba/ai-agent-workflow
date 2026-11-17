# Long-running analysis — safe progress and job semantics

Use a provider-supported asynchronous analysis operation when available.
A synchronous tool with a timeout is **not** automatically a durable job.

For a long operation, use an authorized existing job runner only if it
supports the chosen analysis tool and project without creating an alternate
analysis database or sidestepping permission restrictions.

1. Preserve the project/program identity, script identity, expected result
   and exact outer and inner execution budgets. The outer budget must allow
   setup, tool execution and output.
2. Capture the assigned job identity and use its state and incremental
   output cursor. Do not start a second run because a client disconnected.
3. Judge success from **both** the job process exit, analyzer operation
   result and evidence produced. Exit 0 without successful analysis output
   does not prove completion or correct semantic findings.
4. A live process is not proof of per-function progress; an inner synchronous
   operation may buffer output. Use bounded stages, saved checkpoints or a
   genuine progress facility. Never estimate completion from elapsed time.
5. After a timeout/disconnect, inspect existing job and project/session state
   before reissuing anything. Cancellation/worker recovery must respect
   unsaved changes and the last known-good checkpoint.
6. Report examined functions/regions, distinct traced relations, confirmed
   versus likely findings, saved changes and unresolved contradictions.
   Avoid inflating completion by counting queued jobs or repeated searches.

The selected integration owns the concrete job API, script installation,
resource limits and permissions. Use [project/session recovery](projects-and-sessions.md)
for a lost handle, and [safety](safety-and-completion.md) for rejected calls.
