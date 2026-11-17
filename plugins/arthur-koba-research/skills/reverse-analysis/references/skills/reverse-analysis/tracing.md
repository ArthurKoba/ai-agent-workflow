## Trace and recovery process

Trace program behavior through actual control and data dependencies,
not by naming isolated functions or repeatedly proving known facts.

1. **Locate anchors:** program entry, exports/imports, callbacks, event or
   command handlers, API calls, literals, strings, objects/vtables, types,
   exception handlers, device registers (when present), or external inputs.
2. **Trace control:** callers/callees, CFG, XREF, dispatch tables, indirect
   branches/calls, state-machine transitions and error/cleanup/retry paths.
   Distinguish *code present* from *reachable or observed executing*.
3. **Trace data:** inputs, return values, calling convention/ABI, object
   fields, globals, buffers, producers/consumers, transforms and
   externally visible effects (files, network, UI, services, peripherals).
4. **Reconstruct behavior:** identify the algorithm/contract, parameters,
   preconditions, outputs, modes, limits, errors, resource ownership and
   interaction with other modules. Work from the high-level representation
   above; verify disputed claims with targeted instructions/IR or observations.
5. **Materialize:** apply defensible semantic names, types, structures,
   transitions, references, evidence comments and uncertainty to the
   canonical analysis project. Save, then read back the changed objects.
6. **Move to a new gap:** avoid repeated proof of closed branches; track
   uncertain edges and meaningful work needed to close the feature.

A PE/EXE application, BIOS/UEFI boot path, library function, driver,
DSP algorithm or firmware service can all follow this workflow. Hardware
registers, pin routing and board acceptance are optional target-specific
concerns, **not requirements for ordinary program analysis**.

## Program identity and environment

Before mutation identify the canonical project, selected program and
actual mapped code/data. Related program versions can suggest semantics,
but do not assume identical API/ABI, offsets, structures, callbacks,
device registers or lifecycle. The examined target wins.

When static evidence cannot settle behavior, define a bounded authorized
debugger/emulation/trace experiment and the required observation. Preserve
the known-good baseline. For hardware or other stateful targets use:
`baseline → action → observation → rollback → postcondition`.

Stateful software processes, drivers, media pipelines or hardware interfaces
need clear ownership. Do not launch competing sessions or change target
state speculatively. A static behavior contract is sufficient for an
analysis-only task; implementing a replacement or achieving system
integration is a separate acceptance level.
