# Local agent context

status: CURRENT
updated: <date/time>

## Workspace
workspace_root: <path>
downloads_root: <path or unavailable>
artifact_root: <path or unavailable>

## Build
authoritative_build_surface: <description>
toolchain_path: <path or unavailable>

## Target
target_control_lane: <UART/SSH/... or unavailable>
target_address: <address or unavailable>
file_transfer_method: <method or unavailable>
boot_mode: <state or unknown>
active_owner: <process/state or unknown>

## Local tools
<tool>: <available/unavailable + notes>

## Notes
Only current environment facts. No project history or secrets here.
