# Ghidra / Analyzer Backend Contract

Load with the [general program-analysis skill](README.md) **only** when the Project selects the Ghidra-backed Analyzer service. The Project owns available operations, access permissions and the canonical analysis project; this adapter describes **what must happen and what constitutes proof**, not literal calls, command syntax, argument names or deployment paths.

## Canonical project and program lifecycle

- Discover the **existing saved project**, then select the exact program and its architecture, memory spaces, loader, address mapping and ABI before analysis. A persistent project, a live worker/session and an opened program handle are distinct; none is interchangeable with a worker ID.
- Reuse verified imports, completed C, names, types and references. Do not create a second editable copy or rerun destructive analysis to recover a lost handle.
- If a program disappears from a session: check saved project contents, reopen the project/session, reopen the saved program and verify its mapped bytes and indices. Only diagnose missing/corrupt storage after those checks. After worker restart, the same project may attach to a different worker.
- Preserve a known-good checkpoint before broad reanalysis, image remapping, mass renames or repairs. Treat session failures, missing indices and backend errors as infrastructure state, not evidence about the target.

## Complete supported baseline and dependency linking

- Validate the CPU/language, instruction decoding, code/data boundaries, memory map, loader and calling convention **before** automated function discovery.
- Run or reuse complete native analysis and generated C **for every discovered supported native function**, in bounded restartable batches. Index the output and successes/failures by program. Separate stubs and unsupported regions.
- Build incoming/outgoing/transitive relationships, including imports, indirect calls, callbacks, shared data, references and cross-program interfaces. Use exact call/data evidence, provider version and ABI. Save only grounded links; an external import or coincident symbol is not proof of an executed call.
- Use indexed analyzer output to drive semantic recovery. When it conflicts with actual machine instructions, IR or runtime observations, resolve the discrepancy and regenerate affected C. Preserve existing annotations during regeneration.

## Reusable Java analysis scenarios

Use **bounded Java/GhidraScript** for recurring static evidence questions: writer/reader maps, call-chain candidates, dispatch tables, pointer flow, globals, register access and post-correction checks. This is *static code/data tracing*, not a recorded runtime execution trace. Actual execution proof requires authorized debugging, modeled execution distinguished from real execution, or observed hardware.

1. **Scope:** choose the exact saved program, address space, question, function/instruction range and evidence to be collected. Reuse existing results before initiating another pass.
2. **Probe:** test a small, read-only scenario first; inspect actual return status, output, counts, sample addresses and contradictions. An inline source is temporary and a transport timeout is inconclusive.
3. **Promote:** retain a useful/repeatable script in the provider's **verified persistent script storage**, not in temporary compilation cache or as an imported program. Source version control may coexist where the Project allows it; it does not substitute for the installed executable script.
4. **Verify installation:** discover the actual approved script storage, check permissions/persistence, register reviewed source without overwriting divergent content, and read back exact bytes or an equivalent strong identity. Do not infer a shared path or use an unauthorized write mechanism.
5. **Run registered:** verify the installed identity was used, inspect execution outcome and evidence, then annotate the canonical analysis separately; save and read back semantic changes. A registered script by itself contributes no semantic coverage.

Only promote scripts that reduce future agent work. Keep their purpose, versions, input scope, evidence and repeatability recoverable. Do not install failed one-off probes merely to increase script count.

## Long-running operations and timeout recovery

- Prefer a **native supervised/background job facility** if offered by the configured provider. If the analysis operation is synchronous and may exceed a client timeout, use the Project-approved persistent job runner calling that **same canonical Analyzer service**, not a substitute database.
- Give long operations explicit internal/external time budgets, bounded stages, real work counters and recoverable checkpoints. The supervisor budget must account for startup and provider execution, not just the script.
- Distinguish **running job**, **transport response**, **provider success**, **script result** and **persisted change**. Require evidence from the relevant levels; a command process exiting successfully is insufficient. Intermediate Java output may be buffered, so an apparently quiet job is not automatically stuck.
- Read incremental logs/status from the existing job; do not repeatedly fetch all output. After timeout or disconnect inspect job, project and unsaved work **before any retry**. Avoid concurrent duplicate heavy analysis against one mutable program.
- Restart/cancel workers only after checking recoverability and current work; reopening a session is not a reason to discard saved analysis.

## Annotation, incidents and migration limits

Materialize supported names, types/prototypes, fields/enums, comments, references and state transitions with the confidence model in the common skill. Save coherent mutation batches, read back altered objects, and regenerate affected C. Treat scripts and indexes as reusable analysis artifacts, not as a substitute for canonical semantic annotations.

A provider/policy refusal is **not a target-code failure**. Preserve sanitized operation, denial, whether the backend was reached and legitimate alternatives; infrastructure owns incident tickets and access rules. Do not repeat blocked operations or switch surfaces to evade a restriction.

Ghidra Java analyzers, full project internals and runtime Trace databases are not automatically compatible with another engine. XML/structured export may migrate annotations, **not** promise lossless transfer of scripts or dynamic traces. Retain the original canonical database until representative parity checks succeed.
