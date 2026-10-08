# Targeted programmable reverse analysis: GhidraScript lifecycle

Read this module before using programmable Analysis/Ghidra evidence tools or
designing a repeatable firmware-wide trace. It is the owner of the script
execution, promotion, persistence and monitored-job workflow.

## When to script

Use a bounded, read-only Ghidra Java/GhidraScript, P-code/SLEIGH pass or
controlled emulation when it is more reliable than repeated manual lookups,
especially for:

- cross-module MMIO/constant inventories and register owner searches;
- calculated/indirect addresses, data flow and control-flow traces;
- repeated checks of call/return edges, instruction/data classification and
  saved action boundaries;
- exhaustive writer/reader audits of a hardware field or protocol state;
- reproducible verification after a targeted metadata correction.

Do **not** write a new script for a straightforward question already answered
by instructions, XREF, CFG or a saved contract. Never redo confirmed reverse
work merely to increase script counts.

## Required two-stage script lifecycle

**Explore inline → verify evidence → register useful script in Analysis →
execute the registered script → retain findings in the canonical project.**

1. **Identify the target.** Confirm the canonical `project_id`, exact
   `program`, architecture, mapped addresses and existing metadata. One
   program must be selected explicitly when several are open. Bound the
   instruction/function count and the range being inspected.
2. **Probe online.** Submit a small Java `GhidraScript` source to
   `run_analysis_script_inline(project_id, program, code, args?, dry_run?)`.
   This is for early hypothesis tests and small, read-only surveys. Inspect
   the returned `success`, `console_output`, counters, instruction addresses
   and contradictions. A transport timeout is **not** proof of script failure
   or success. An inline execution uses an ephemeral server-side source/cache;
   it does **not** register the script for future sessions.
3. **Promote after useful proof.** Once the script produces a reproducible
   finding or is useful for follow-up/regression, store its **Java source in
   the Analysis/Ghidra server's configured persistent script root**, not as
   a permanent local file or a Git-tracked firmware artifact. Do not
   promote disposable failed experiments merely to keep everything.
4. **Prove registration.** Read back and compare the complete source bytes
   or digest; reject an existing same-name file with different contents
   rather than overwriting it silently. Run the registered script by its
   permanent path and verify its actual output. Only then discard any
   temporary local Java source. Preserve the script's stable name and
   purpose in the appropriate Analysis project knowledge.
5. **Materialize findings separately.** A stored script is a reusable tool,
   not semantic coverage. Write proven names, contracts, register fields,
   links and evidence to the canonical analysis program; save and read back
   those edits. Scripts and reverse annotations are different artifacts.

## How to register and run a persistent GhidraScript

First call `get_storage_info(project_id)` and read the **live**
`script_root.path`, existence and writeability. Where available, use the
Analysis provider's dedicated script upload/install API. Do not infer that
the Terminal workspace, an imported firmware `Program`, the temporary
inline compilation cache and the Ghidra script root are the same storage.

On an Analysis installation without a dedicated upload API, a **one-time,
narrowly scoped, authorized inline Java/GhidraScript bootstrap** may register
the reviewed source from inside the running Ghidra process:

- Resolve the configured `GHIDRA_MCP_SCRIPT_ROOT` and cross-check it with
  `get_storage_info.script_root.path`; refuse missing, unexpected or
  non-writable roots. Do not invent a mount path.
- Verify the expected canonical program and guard the target filename
  against directory traversal. Place only the intended `<ClassName>.java`
  under that root (not under a worker-specific temporary cache).
- Supply the reviewed source payload (for example as a bounded embedded
  UTF-8/Base64 payload), decode it **inside Ghidra**, and create the file
  with no-clobber semantics. If it exists, compare exact bytes and fail on
  a mismatch. Read back the resulting file; emit installed/identical counts.
- Do not patch firmware bytes, import the `.java` as a Ghidra `Program`,
  alter unrelated scripts or claim durable registration from a successful
  inline execution alone.

Run the registered source with
`run_analysis_script(project_id, program, script_name, args?,
timeout_seconds?, capture_output=true, dry_run?)`, setting `script_name`
to the **absolute source path in the discovered script root**. Prefer a
bounded but sufficiently long `timeout_seconds` for substantial audits.
Check the returned `success`, `script_path`, output and measured results.

**Headless caveat:** `list_scripts` may only describe desktop Script Manager
usage; it is not an authoritative inventory of headless installed sources.
Successful execution **by permanent absolute path**, with an exact source
readback, is stronger registration evidence. If the configured script root
is not persistent/shared across the intended worker restarts, fix that
storage contract before relying on the script across sessions.

## Long-running analyses as monitored jobs

Prefer an Analysis-native asynchronous task/status API if the current
provider exposes one. **Do not invent one:** on versions where
`run_analysis_script` is synchronous, it may expose an execution
`timeout_seconds` but no script task ID, while
`run_analysis_script_inline` may not expose a tool-level timeout.

For longer scripts use the project's approved **Terminal job surface** with
a small, bounded client/runner that submits a real Analysis MCP request
against the canonical project (not an alternate analysis database):

1. `job_start(workspace_id, command=<approved Analysis MCP client command>,
   label=<audit purpose>, timeout_seconds=<outer budget>)` returns `job_id`.
   The client calls `run_analysis_script` for a registered script (or
   `run_analysis_script_inline` for the initial proof), explicitly
   specifying `project_id` and `program`. Set the inner script timeout
   separately and make the outer job budget larger to allow setup/output.
2. Capture `job_id`, script name, program, intended scope and expected
   output. `job_status(job_id)` checks lifecycle; `job_read(job_id,
   cursor, max_bytes?, wait_seconds?)` retrieves only new output and returns
   `next_cursor`; `job_wait(job_id, timeout_seconds)` waits for an
   intermediate or terminal state. Advance the cursor instead of rereading
   old logs.
3. Interpret **terminal job exit**, Analysis tool `success` and script
   output together. An outer process that exited with `0` is not enough if
   the Analysis response reports failure or script output contains an
   execution error. Count a trace as proven only from its actual findings.
4. A running job proves only that the client process is alive; a synchronous
   Analysis call may buffer Java `println` output until completion. For
   meaningful intermediate progress use smaller bounded stages/checkpoints,
   explicit per-stage counts, or a provider-supported progress endpoint.
   Do not invent progress percentages from elapsed time.
5. On a client timeout or disconnect, **inspect the existing job and
   project/worker state before resubmitting**. Never stack identical heavy
   scripts on a busy program. Use `job_cancel` or worker recovery only at a
   real decision boundary, accounting for unsaved edits and the project's
   known-good state.

A transient runner may live in an approved orchestration workspace; it is
**not** the canonical home for promoted `.java` scripts. Never require the
user to operate a terminal when an authorized job tool can do so.

## Evidence and safety

- Default to read-only Java scripts. Mutation requires a scoped proof,
  known-good baseline, exact target verification and save/readback.
- Enforce bounded scans, cancellation checks, and a clear distinction
  between instruction-decoded hits and raw words that might be data.
- For every useful run, record *examined instructions/functions, distinct
  owners, new traced edges, confirmed vs likely claims, changes actually
  saved, script count, and remaining contradictions*. Report deltas rather
  than repeated worker/queue bookkeeping.
- Static script output is implementation/behavior evidence, not runtime
  execution proof, board proof, or completion of a whole hardware block.
- Respect script-execution permissions and provider security decisions.
  If installation/execution is unavailable, report the exact missing
  capability; do not silently replace the analyzer's script library with
  local or Git storage, or route around a security block.
