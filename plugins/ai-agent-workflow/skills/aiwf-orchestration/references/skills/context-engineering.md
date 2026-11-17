# Context-Efficient AI Engineering

Use this skill when designing repository documentation, agent bootstrap/context loading, multi-agent engineering workflows, or staged implementation/refactoring so agents can work accurately without preloading the whole system.

## Core principle

Context is a constrained engineering resource.

The goal is not to maximize how much documentation an agent reads. The goal is to load the smallest authoritative context that lets the agent make the next correct decision, then retrieve more evidence only when the task crosses a real boundary.

A large always-on context creates three costs:

- token and context-window consumption;
- slower evidence retrieval and more irrelevant attention;
- higher risk that stale narrative documentation competes with current source code.

Prefer progressive disclosure over mandatory bulk reading.

**Progressive disclosure selects files, not fragments.**
Read a selected mandatory map, skill or contract completely through the
Project's authoritative source. A tool-success signal, preview, summary or
truncated response is not proof of complete reading. The injected Account
and Project prompts govern missing sources; do not introduce another
mandatory startup layer here.

## Conditional modules

Read only the complete module needed for the current decision:

- documentation ownership, repository maps and work tracking → [Documentation](context-engineering/documentation.md);
- startup, just-in-time loading, correction recovery and escalation → [Loading](context-engineering/loading.md);
- separating implementation and quality passes → [Passes](context-engineering/passes.md);
- documentation synchronization, context audit and acceptance → [Maintenance](context-engineering/maintenance.md).

Agent assignments, communication and PDCA belong to the [orchestration skill](orchestration/README.md). Context Engineering owns only the selection and organization of context.
