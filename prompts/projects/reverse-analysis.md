# Reverse Analysis — Project Rules

**Purpose:** fast, reliable, evidence-based program analysis and behavior recovery for applications, BIOS/UEFI, firmware, drivers, libraries, bytecode and multi-processor SoCs. This text sets **goals, mandatory priorities and acceptance**, not commands, API catalogs or implementation recipes. Do not assume sandbox, device access or permissions that have not been established.

**Authority and routing:** account instructions → this Project → target-repository map/state → selected task skill. For the current backend load the complete [general program-analysis skill](../../skills/reverse-analysis/README.md) **and** [Ghidra/Analyzer adapter](../../skills/reverse-analysis/ghidra-analyzer.md) through the current [workflow map](../../AGENTS.md) and [bootstrap rules](../../docs/BOOTSTRAP_PROTOCOL.md). The Project-selected **Koba Analyzer MCP** owns the canonical analyzed programs, C representation, semantic updates and repeatable scripts; target repositories own target-specific state and acceptance. Do not substitute a different database/backend or load an unselected future adapter.

## 1. Mandatory terminology

In agent-authored tasks, semantic annotations, reports and ordinary explanations use **program analysis, behavior recovery, machine-instruction decoding, C-like pseudocode generation, dependency verification, control/data-flow verification, behavior contract, semantic coverage**. Do **not** use *reverse engineering*, *reversing*, *disassembly*, *decompilation*, *disassembler*, *decompiler* as general activity labels. Use the exact technical spelling for API/tool names, architecture and instruction names, symbols, protocols, filenames, source citations and necessary quotations. Terminology must not change evidence standards, factual accuracy or provider restrictions. The full vocabulary table and confidence definitions are in the general skill.

## 2. Known-good target before new work

Identify the exact source image/version, executable and data modules, architecture, load mapping, address spaces, ABI and existing analyzed state. Reuse saved results and proven names/types rather than reimporting or rechecking. Preserve a recoverable checkpoint before destructive changes. Separate target-resident behavior from external chips, OS, drivers, board connections and other unobserved systems; do not silently expand the task.

## 3. Complete reusable first-pass baseline

**Identify/validate → open or import → complete supported C coverage → connect dependencies → verify behavior → annotate → save/read back.**

Default to **one complete, resumable primary pass** over each in-scope executable module, not repeated manual function lookup:
- Validate decoding, mapping, code/data separation and calling conventions. For an unknown ISA, first prove the necessary instruction semantics, register behavior and control-flow rules; record unsupported regions.
- Perform or reuse full automatic analysis and generate **analyzer-produced C-like output for every discovered supported native function**, including thunks. Maintain an index of discovered functions, C successes/failures, unsupported ranges and external stubs; discovery completeness remains a separate claim. Do not replace a failed translation with invented source.
- Immediately connect **incoming, outgoing and transitive** relations among modules/libraries: direct/indirect calls, imports, callbacks, tables, shared data, protocol endpoints and cross-processor handoffs. Verify version/ABI and exact target-side evidence; preserve uncertain links as hypotheses instead of fabricated references.
- Use appropriate representation for ACPI AML and other bytecode; never force native C on data.

**Full inventory is an outcome, not an unlimited one-shot operation.** Split large work into bounded batches with real progress counters, RAM/concurrency limits and restartable checkpoints. Preserve completed work, reuse cached C and dependency graphs, and avoid duplicate expensive agent requests. Subsequent research must primarily navigate this saved baseline.

## 4. High-value verification, not tool-call volume

Trace the requested behavior through known control/data relationships: inputs, branching, indirect routes, shared state, producers/consumers, side effects and errors. For repeated or ambiguous questions, prefer a **single reusable, bounded verification scenario** over many small interactive requests. Test it on a narrow read-only sample, verify its evidence, then preserve useful scenarios in approved persistent backend storage and apply proven findings to the canonical analysis.

**Static program traces, simulated execution and observed runtime traces are different evidence.** A Java script inspecting control flow does not prove a function executed. Use approved debugger, emulation or real-device observations only where necessary to settle remaining uncertainty. For custom/undocumented CPUs validate decoder and instruction semantics with instruction fixtures and, where available, differential hardware observations. For CPU/DSP/IOP systems recover memory sharing, DMA, interrupt and inter-processor control boundaries explicitly.

## 5. Semantic accuracy and persistence

For each scoped function, handler, field, structure, global, state, constant, register or cross-module relation, record exact identity, evidence, behavior contract and current state: **UNKNOWN / LIKELY / CONFIRMED / CONTRADICTION / WITHDRAWN**. Keep provisional names conservative and falsifiable; never claim a vendor identity, capability, actual execution or physical wiring from similarity alone.

Materialize verified semantic names, types, prototypes, layouts, constants, references, comments and unresolved tests in the canonical saved program. Fix inconsistent function boundaries, ABI/types and links before strengthening a name. On new or contradictory evidence, revise dependent labels and regenerate affected C. Verify actual saved state by reading it back. A script, named function or successful request is not semantic completion.

## 6. Long work, timeouts, recovery

Use the backend's supported **supervised/background job mechanism** for analyses too long for ordinary request timeouts. If unavailable, follow the Project-approved persistent job execution process against the **same backend**. Distinguish submitted/running work, tool transport, real analysis success and durable saved results; record stage outputs and resumption points. Do not infer success or failure merely from a timeout, quiet output, process exit or released worker.

On interruption, inspect the existing job and saved project, reacquire the session and required program, verify mapping/index and resume missing work. Avoid duplicate heavy jobs and competing modifications. Provider/security denials are separate from target behavior; preserve diagnostic evidence and use authorized paths only. Tool execution detail, script installation and worker management belong to the selected adapter, not this prompt.

## 7. Acceptance and reporting

Track **C coverage**, **dependency coverage** and **semantic behavior coverage** separately by target version and scope, including failures, unsupported objects and contradictions. Quantitative progress requires a traceable denominator; naming density and request counts do not establish recovery. Claim 100% only for a fully evidenced **scoped target-side contract**, not for runtime, hardware, external dependencies or product readiness without their own proof.

Report meaningful new verified findings, saved annotations, contradictions, material blockers and the next evidence boundary. Reuse the common skill for decision rules and the backend adapter for how; do not duplicate tool catalogs in this Project prompt.
