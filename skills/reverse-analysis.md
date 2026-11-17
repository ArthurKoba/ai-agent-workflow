# Reverse Analysis — tool-independent methods

Apply when examining program behavior: applications, binaries, libraries,
firmware, drivers and bytecode supported by the selected analyzer.
This Skill explains **what evidence proves behavior, why to perform
specific analysis and when to stop**. It does not select an MCP product,
name an API/tool or prescribe a provider-specific storage location.
Use the relevant project/integration Skill for concrete tools, permissions,
session management, scripting interfaces and failure recovery.

Read the affected modules completely; do not load the entire library:

- [Evidence and high-level baseline](reverse-analysis/evidence-and-baseline.md)
  — preflight, target identity, external reference stopping, full analysis.
- [Control/data tracing](reverse-analysis/tracing.md) — causal behavior paths.
- [Vocabulary and confidence](reverse-analysis/terminology.md) — what terms
  mean and how strong each evidence claim is.
- [Semantic naming and save/readback](reverse-analysis/semantic-naming.md)
  — evolving names, types, comments, conflicts and materialization.
- [Validation and scoped completion](reverse-analysis/validation-and-scope.md)
  — static/execution/integration/physical evidence and success boundaries.
- [Coverage accounting](reverse-analysis/coverage.md) — honest denominators
  for features, registers and large programs.
- [Safety and failure reports](reverse-analysis/safety-and-completion.md)
  — stopped/blocked tool calls, contradiction and scope.
- [Persistent projects and sessions](reverse-analysis/projects-and-sessions.md)
  — project versus worker/handle, reattach before reimport.
- [Automation methodology](reverse-analysis/script-methodology.md)
  — when repeatable scripting beats manual inspection, proof and promotion.
- [Long-running analysis](reverse-analysis/long-running-analysis.md)
  — status, cursors, asynchronous recovery and acceptance.

If a project/integration owns tool or interface semantics, follow its
authoritative instructions. Never infer that a given analyzer implements
the above capabilities; lack of a supported tool is a reported boundary,
not permission to fabricate a fallback.
