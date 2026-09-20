# Terminal / Remote Operations

## Mandatory trigger

Load this skill before emitting any human-operated shell/PowerShell/WSL/SSH/UART/bootloader command block. This is a hard routing rule, not an optional optimization.

If command-format rules were just violated or the user reports they were forgotten, reload this skill before issuing the next command block.

Use for shell, PowerShell, WSL, SSH, UART, bootloader or remote command execution.

## Lanes
Know which lane every command belongs to:
- local host;
- WSL/container;
- remote SSH target;
- UART/serial target;
- bootloader;
- privileged/service host.

Do not silently switch lanes.

## Human-operated command format
- one logical step per copyable code block;
- each command on its own physical line;
- explicit `cd` before cwd-dependent commands;
- avoid ordinary `&&`, `;` and backslash continuation when separate lines are clearer;
- group proven routine commands, but stop at real decision boundaries;
- do not combine separate decision boundaries merely to reduce the number of code blocks;
- do not split one proven routine stage into one-code-block-per-command noise.

## Minimal targets
Do not assume GNU coreutils, Python, `file`, full shell features, SSH/SFTP or writable storage.

Use the project/local-context transport contract.

Legacy flags such as `scp -O` belong in project/local context, not global prompts.

## UART
Avoid long multiline pasted scripts, complex quoting and fragile loops. Prefer a helper/script plus one simple invocation.

## Safety
Before destructive commands confirm lane, target, current state and recovery/rollback when relevant.


## Local contract precedence

A generic/default command pattern must never silently override a known project/local transport or execution contract.

Examples:
- if the project/local context defines legacy SCP with `scp -O`, use that exact contract;
- if the project defines a normal firmware-update procedure as routine operation, do not relabel it as exceptional/destructive merely from a generic safety template.

Before emitting a command:
1. check whether repository/project/local context defines a transport or operation-specific contract;
2. if defined, that local contract overrides the generic default;
3. if the local contract is expected but cannot be recovered, stop at that boundary and report the missing context;
4. do **not** fall back to a familiar/default command merely because the universal skill does not encode the project-specific flag.

“Not universal” means “resolve from project/local context”, not “ignore the rule”.
