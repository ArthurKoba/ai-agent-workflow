# Repeatable analysis automation — method, not tool commands

Use a narrow, read-only script or controlled experiment when repeated manual
queries would introduce error or make a control/data-flow audit irreproducible.

## When automation is justified

- Repeated cross-module imports, calls, writers/readers, state transitions,
  computed addresses or register accesses can justify a bounded scripted pass.
- Define the exact program, architecture, mapping, question and output before
  execution. Avoid scripts for a question already resolved by saved XREFs,
  the existing control-flow graph, source or a closed behavior contract.
- Keep code/data classification separate. A raw numeric hit is not proof
  that an instruction executed or that a semantic relation exists.
- Prefer an analyzer's supported read-only scripting facility. Discover
  capabilities, parameters, security restrictions and persistence semantics
  from the chosen project/tool; never assume a particular engine or API.

## Validation and promotion

1. Preserve a known-good checkpoint and identify the target bytes/program.
2. Probe the smallest read-only query, bounded by program region and work.
   Inspect returned evidence, counts and contradictions; an invocation
   timeout does not prove success or failure.
3. If useful, preserve the reviewed script in the project's **approved**
   persistent script store using that tool's supported facility. A temporary
   execution cache or staging copy is not durable registration.
4. Compare the retained source against the reviewed source, execute by the
   tool's documented persistent identity and verify actual output.
   Do not overwrite same-name content silently.
5. Materialize proven semantics in the canonical analysis database, save,
   read back and retire temporary artifacts only once recovery is established.

A reusable script is an evidence-producing instrument, not a recovered
program contract; do not count stored scripts as semantic coverage.
If persistence/execution is unsupported or forbidden, report the exact
capability boundary instead of inventing a new storage route or bypass.

## Safety and reporting

Default to read-only. Mutations require verified target, scoped evidence,
recoverable baseline, explicit authorization and saved-state readback.
Use bounded work, cancellation/checkpoints when supported and output
counts that distinguish confirmed results, hypotheses and unsupported data.
Follow [confidence and materialization](semantic-naming.md) and
[scope/coverage](coverage.md); don't claim runtime proof from static output.
