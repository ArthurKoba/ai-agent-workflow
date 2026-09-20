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
