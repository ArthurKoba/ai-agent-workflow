# Local Context Contract

Local context is **dynamic environment state**, not a prompt layer.

The instruction hierarchy remains:

`account → project → skill`

Local context supplies values those layers may reference.

## What belongs here

Examples:
- workspace root;
- downloads/artifact locations;
- target control lane;
- target address;
- file-transfer method;
- toolchain path;
- authoritative local build surface;
- current boot mode;
- active owner/process;
- locally available tools.

Do not put project history here.

Avoid credentials/tokens/private keys when possible; use dedicated secret storage.

## Storage

Recommended runtime file:

`LOCAL_AGENT_CONTEXT.md`

It should normally be untracked/private or supplied by the Project/harness/tooling.

Tracked repositories may contain only a template:

`LOCAL_AGENT_CONTEXT.example.md`

## Project declaration

Project/repository bootstrap declares:

- `local_context: REQUIRED`
- `local_context: OPTIONAL`
- `local_context: NOT_USED`

If REQUIRED context is unavailable, report degraded-start once before environment-dependent work:

> Local execution context is unavailable. I can continue repository/source analysis, but I will not guess local paths, target addresses, transport or build environment.

Do not repeat this warning in every message.

## Precedence

When values conflict:

1. direct current user instruction;
2. live tool/repository/target evidence;
3. injected project/account rules;
4. repository state/tasks;
5. local context;
6. historical handoff/summary;
7. memory/assumption.

A saved machine-specific value never overrides fresher live evidence merely because it was written earlier.

## Design goal

Machine-specific state can change without rewriting universal prompts or polluting source history.

Missing local context becomes visible and fail-closed instead of producing guessed paths/IPs.
