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

If REQUIRED context is unavailable or cannot be fully read,
identify the missing source and report degraded execution capability once.
Stop only work depending on its environment values; unrelated authorized
repository/source inspection can continue. The Project may declare a
stricter boundary, and required task/skill authorities still have their
own full-document reading gate in `../docs/BOOTSTRAP_PROTOCOL.md`.
Do not repeatedly warn or guess missing paths, targets, transports or tools.

## Precedence: instructions versus observed facts

Instruction precedence belongs to the active runtime and governing
Project/repository/tool contracts, **not** this cached environment file.
A user-provided value is not permission to override higher-priority rules
or tool access restrictions.

For mutable environment facts, prefer recent verified live observations to
saved or historical notes. Reconcile a conflicting current user value with
live evidence rather than silently overriding either. Treat saved local
context as a cached reference, not proof of current machine state.

## Design goal

Machine-specific state can change without rewriting universal prompts or polluting source history.

Missing local context becomes visible and fail-closed instead of producing guessed paths/IPs.
