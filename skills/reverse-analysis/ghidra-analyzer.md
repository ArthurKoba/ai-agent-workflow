# Ghidra / Analyzer MCP Adapter

Load **after** [the common program-analysis skill](README.md) when the Project selects Ghidra through Koba **Analyzer MCP**. The Project/target repository owns the canonical saved database, current program list, and primary tools. Use the actual advertised operation names/capabilities; "Analyzer" and "action node" are intentional provider vocabulary. This adapter describes the currently deployed backend, not a requirement for all future engines.

## Project, import and analysis

- Discover existing projects, stable project_id, project/session status and saved program paths **before** import, duplication or mutation. Always send the selected project_id and program on project-scoped operations when available. Session-local open-program handles and worker assignment are not durable project identity.
- Verify loader/language/ABI/base/relocations and mapped memory before analysis. Reopen a saved program if an open handle disappears; do **not** reimport merely because the worker/session expired. If an index or function vanishes, check the exact bytes, memory space, address mapping and index before rebuilding.
- For every supported program, run or reuse auto-analysis, gather discovered functions/thunks and generate analyzer-produced C for the **complete supported inventory**. Batch by program/function, persist a program-linked C index and completion/failure counts. Use existing analyzed/annotated programs; avoid destructive repeated auto-analysis.
- Link imports and cross-program call/data boundaries with exact target evidence, version/ABI and endpoint readback. A cross-program annotation is not an invented runtime CALL reference.
- Prefer one script or structured composite analysis to repeated N tool calls for repeated mapping, indirect-call, field writer/reader, virtual dispatch or register access questions.

## Semantic updates

Operate on the canonical Analysis project. Map functions/methods, Analyzer action nodes, globals, comments, parameter types, structures, enums, control/data references and C. Use read-only inspection to establish proof; commit bounded, coherent mutation batches only after necessary evidence. Read back saved names/types/links and regenerate affected C. Do not treat an inline script response as saved project state. Respect uncertainty/status conventions from the common skill.

## Persistent Java/GhidraScript workflow

Use Java/GhidraScript when bounded static program queries, p-code, SLEIGH processing or a repeatable test would replace many manual calls. **Static Java scripts are not physical/runtime execution traces**; use a debugger, supported emulator or observed hardware for execution proof. Prefer read-only scripts; check cancellation and bounded ranges for large loops.

1. **Identify:** exact project/program, ISA, address space, range/function budget, existing names and data.
2. **Probe:** call run_analysis_script_inline(project_id, program, code, args?, dry_run?) with a short, controlled Java GhidraScript. Check success, output, counters, addresses, exceptions and contradictions. Inline code is an **ephemeral server-side source**, not permanent registration. A transport timeout proves neither success nor failure.
3. **Promote:** keep only reproducible/reused scripts. Use the backend's **persistently configured script root** or an authorized script-install API. A version-controlled source may be a development artifact where the Project authorizes it; the installed copy in the Analysis service is the **execution authority**. Do not confuse workspace files, imported Program bytes, temporary compilation cache or server scripts.
4. **Register safely:** query get_storage_info(project_id) for script_root.path, existence and writability. Prefer an advertised installation API; never assume shared mounts. If absent, a narrowly authorized one-time bootstrap may write reviewed ClassName.java from inside the Ghidra process only after matching the configured GHIDRA_MCP_SCRIPT_ROOT, checking project identity and protecting the filename against traversal. Use no-clobber or exact-content comparison, read back bytes/digest; do not overwrite a different script, patch the binary, or import Java source as Program.
5. **Execute registered:** call run_analysis_script(project_id, program, script_name, args?, timeout_seconds?, capture_output=true, dry_run?) with the confirmed **absolute installed source path**. Verify script path, success, output and observed effects. list_scripts may represent GUI Script Manager rather than the authoritative headless inventory; installed-source readback plus execution is stronger proof.
6. **Materialize independently:** transfer proven findings into names, types, links and notes in the canonical program; save and read back. A reusable script is a tool, **not** recovered semantic coverage.

Keep the script source/name, tested program, input arguments, output counts, execution constraints and stable purpose recoverable. Scripts needed after worker restart require script-root persistence/shared visibility verified across those sessions.

## Long-running script jobs and session recovery

Prefer a backend-advertised asynchronous Analysis task API when available; **do not invent one**. Where run_analysis_script is synchronous (may have timeout_seconds but no task ID), run a small controlled client against the **same Analyzer MCP**, supervised by the project's approved persistent Terminal job interface:

- Start job_start(workspace_id, command, label, timeout_seconds) with an outer budget greater than the script's own timeout. The client names canonical project_id and program, and calls run_analysis_script or run_analysis_script_inline.
- Record job_id, project/program, script name, scoped count and expected output. Use job_status / job_read(next_cursor) / job_wait and advance the cursor; never reread entire logs.
- Verify **all three**: terminal process exit, Analyzer response success, and script result/evidence. Exit 0 alone is not proof. Buffered Java output may arrive only at completion; for progress use bounded stages, actual counters or provider progress, not guessed percentages.
- On timeout/disconnect, inspect the **existing** job, saved state and project worker before resubmitting. Do not start duplicate heavy script jobs on the same mutable program; cancel only after considering uncommitted modifications.

When a saved program seems missing: inspect the project catalogue and session; reconnect project, reopen saved program, verify mapping and index, then resume. A released worker or ephemeral handle is not deleted analysis. A worker can change after idle release; do not use worker ID as persisted identity. If storage/mapping corruption is proven, preserve a checkpoint before repair.

## Safety and failure evidence

Backend/provider refusal is not a failed target behavior contract. Preserve exact sanitized operation, refusal, whether the provider reached the backend, affected project and any authorized alternate evidence route; send provider incidents to the owning infrastructure tracker. Do not repeat blocked calls or use another connector to evade a policy block. The analysis skill does not own incident-board formatting or permission policy.

For each useful script run retain scope/versions, examined functions/instructions, distinct matches, contradictions, runtime vs static status, annotations actually saved and unresolved questions. Script repository location and persistent Analysis program are separate artifacts.

## Limits

Ghidra projects, proprietary Java analyzers, Trace database and Analyzer-specific action-node metadata are **not** automatically portable to radare2. XML export can assist annotation transfer, not guarantee lossless project or runtime-trace migration. Keep the original canonical analysis as an archive until explicit parity checks succeed.
