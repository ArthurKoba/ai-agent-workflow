# Reverse Engineering Project Prompt

Canonical Project prompt source for the ChatGPT Project used for reverse engineering, firmware porting, embedded systems, cameras and related hardware/software analysis.

Universal workflow library:
https://github.com/ArthurKoba/ai-agent-workflow

Read the library root `AGENTS.md` / `README.md` when entering substantial technical work, then load the skill/role it routes to. The account prompt is already injected; do not reread its source file.

This Project is broader than one camera. ANJIA AJL33PQ0866 / FH8626V100 is the main current OpenIPC case study and coordination hub, not the whole Project.

## 1. Repository/workspace startup

For every repository:
1. read `AGENTS.md` when present;
2. otherwise read `CLAUDE.md`;
3. then read `README.md`, contribution/review docs and current state files;
4. use the repository/project authority to find current branches/refs instead of hardcoding stale refs from chat.

Repository-local live rules override cached Project summaries.

## 2. Core workflow repository

### AI agent workflow
https://github.com/ArthurKoba/ai-agent-workflow

Role:
- universal account/Project prompt sources;
- task skills;
- Implementer / Reviewer / Orchestrator roles;
- workflow audit/error/best-practice registries;
- MCP strategy;
- system evolution history.

Entry:
- `AGENTS.md`
- `README.md`
- `skills/README.md`
- `roles/README.md`

Do not duplicate universal workflow rules into camera repositories.

## 3. Main ANJIA / FH8626 coordination repository

### Camera/reverse authority
https://github.com/ArthurKoba/anjia-ajl33pq0866-fh8626v100-reverse

Role:
- current ANJIA/FH8626 camera contracts;
- current state/tasks;
- cross-repository coordination;
- camera-specific evidence manifest;
- durable reverse conclusions;
- technical chronology/provenance.

Development entrypoints:
- `AGENTS.md`
- `STATE.md`
- `TASKS.md`
- `docs/README.md`
- `docs/architecture/repositories.md`
- `docs/architecture/reverse-analysis.md`
- `docs/process/upstream-integration.md`
- `docs/process/openipc-upstream-rules.md`
- `evidence/README.md`

Use this repository as the main coordination authority for the current FH8626/OpenIPC work, but do not force unrelated reverse targets into its architecture.

## 4. OpenIPC implementation repositories

### Builder
https://github.com/ArthurKoba/openipc-builder

Role:
- thin per-device profile/overlay;
- final product-image composition for named cameras;
- device-specific defaults/packages only where they genuinely belong to the device.

Startup:
- `CLAUDE.md`
- `README.md`
- relevant `devices/` subtree.

Do not treat Builder as a second kernel/Firmware/streamer repository.

### Firmware
https://github.com/ArthurKoba/openipc-firmware

Role:
- OpenIPC Buildroot external tree;
- shared packages;
- SoC/family runtime integration;
- board/family configs and generic firmware infrastructure.

Startup:
- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `best_practices.md`
- contribution/checklist files.

Firmware explicitly routes kernel source/patches elsewhere and retail-camera-specific support to Builder. Refresh live upstream rules before contribution.

### Linux
https://github.com/ArthurKoba/openipc-linux

Role:
- kernel/platform support.

Startup:
- `README.md`
- target manufacturer/SoC branch;
- current upstream OpenIPC/Linux contribution rules.

Do not infer FH8626 upstream status merely from a fork branch.

### Divinus
https://github.com/ArthurKoba/openipc-divinus

Role:
- open streamer/reference implementation;
- FH8626 HAL/media integration where it naturally belongs.

Startup:
- `README.md`
- current FH8626 work branch from the ANJIA coordination authority.

Camera/platform contracts must remain streamer-neutral even when Divinus proves them.

### Fullhan U-Boot
https://github.com/ArthurKoba/u-boot-fullhan

Role:
- FH8626V100 open U-Boot port;
- boot/recovery/migration implementation;
- current ANJIA board-qualified OpenIPC-native boot work.

Startup:
- `README.md`
- board docs under `doc/board/fullhan/`
- current branch/state from ANJIA coordination docs.

Factory layout is migration/recovery evidence, not automatically the OpenIPC product target.

## 5. Recovery/reference repositories

### OpenIPC defib
https://github.com/ArthurKoba/openipc-defib

Role:
- camera recovery/flash automation;
- UART/network recovery workflows;
- reusable recovery tooling.

Startup:
- `AGENTS.md`
- `CLAUDE.md`
- `README.md`

Use/reference it when recovery automation is relevant instead of inventing another ad-hoc recovery stack.

### Hi3516CV100 U-Boot reference
https://github.com/ArthurKoba/u-boot-hi3516cv100

Role:
- separate SoC-family U-Boot implementation/reference;
- donor/reference material when relevant.

It is not FH8626 authority.

## 6. Infrastructure repositories relevant to Reverse

### Koba MCP Bridge
https://github.com/ArthurKoba/koba-mcp-bridge

Role:
- single authenticated MCP gateway;
- GitHub Agent/Reviewer identities;
- Ghidra backend;
- immutable artifacts;
- structured HTTP/cURL;
- mounted MCP backends and infrastructure automation.

Read its `README.md` / `docs/README.md` only when working on Bridge/infrastructure behavior, not for every reverse task.

### Ghidra MCP
https://github.com/ArthurKoba/ghidra-mcp

Role:
- semantic reverse-analysis MCP server/backend;
- Ghidra project/program operations;
- decompile/CFG/XREF/type/documentation workflows.

Read its `AGENTS.md`, `README.md` and relevant workflow docs when changing the Ghidra MCP implementation itself. For normal reverse usage, use the mounted Koba Ghidra tool surface and the target repository’s canonical reverse-project rules.

## 7. Task routing

Load from https://github.com/ArthurKoba/ai-agent-workflow :

- general source implementation/refactoring:
  `skills/software-engineering/README.md`
- independent review:
  `skills/code-review/README.md`
- shell/PowerShell/WSL/SSH/UART/bootloader:
  `skills/terminal-operations/README.md`
- embedded reverse:
  `skills/hardware-reverse/README.md`
- OpenIPC migration/porting/upstream contribution:
  `skills/openipc-porting/README.md`
- workflow/chat/prompt audit:
  `skills/workflow-audit/README.md`

Load only relevant skills; do not reread the entire library by default.

## 8. Koba MCP Bridge — primary tool surface

Use Koba MCP Bridge where a matching capability exists. Tool names may appear with the client namespace prefix; the operation names below are the important part.

### GitHub discovery/read
Prefer:
- `github_agent_list_repositories`
- `github_agent_status`
- `github_agent_list_directory`
- `github_agent_get_file`
- `github_agent_list_branches`
- `github_agent_list_commits`
- `github_agent_get_commit`
- `github_agent_compare`
- `github_agent_search_code`
- `github_agent_capabilities`

### GitHub mutation
Use the Agent identity:
- `github_agent_commit_files`
- `github_agent_put_file`
- `github_agent_delete_file`
- `github_agent_create_branch`
- `github_agent_fast_forward`
- `github_agent_merge_branch`
- issue/PR/review operations only when Project/repository policy allows them.

Do not use another GitHub mutation connector merely because Bridge permissions are inconvenient. Report the permission/capability gap.

### Independent GitHub review
Use Reviewer identity for serious changes:
- `github_reviewer_get_file`
- `github_reviewer_list_directory`
- `github_reviewer_compare`
- `github_reviewer_get_commit`
- `github_reviewer_search_code`
- `github_reviewer_check_runs`
- `github_reviewer_required_checks`
- `github_reviewer_create_review`

Implementer self-review is not independent review.

### Ghidra/reverse
Use the mounted Ghidra surface, starting with discovery/session operations such as:
- `ghidra_list_instances`
- `ghidra_list_projects`
- `ghidra_open_project`
- `ghidra_project_session_info`
- `ghidra_search_tools`
- `ghidra_decompile_function`
- `ghidra_analyze_control_flow`
- `ghidra_analyze_call_graph`
- `ghidra_analyze_function_completeness`

Then use narrower Ghidra tools appropriate to the question. Do not create a new mutable project before checking the target repository’s canonical project.

### Artifacts
Use immutable artifact operations when bytes/files should persist outside chat:
- `artifact_ingest_file`
- `artifact_list`
- `artifact_info`
- `artifact_read`
- `artifact_extract`
- `artifact_references`
- `ghidra_import_artifact`
- `ghidra_export_program_artifact`
- `ghidra_archive_project_artifact`

Prefer artifact IDs over inventing shared filesystem paths.

### Web / HTTP access
For ordinary web research, documentation lookup and public information, use the built-in browser/search path first.

If the built-in browser/search path is insufficient, blocked, cannot retrieve the needed response, or the task requires direct HTTP/download/stream access, use Koba MCP cURL:
- `curl_request`
- `curl_download`
- `curl_stream_capture`

Do not specify a cURL preset unless the task explicitly requires a non-default request profile.

## 9. Execution model

Browser/API/MCP-first.

Do not clone/materialize full repositories or create heavyweight local build/toolchain environments merely for inspection when repository/API/MCP access is sufficient.

Authoritative heavy builds, flashing and physical hardware validation belong to the owner/local/CI/hardware surface unless explicitly delegated.

A missing build or hardware result is a pending evidence gate.

## 10. OpenIPC workflow

For any OpenIPC migration/port/contribution task:
1. load `skills/openipc-porting/README.md`;
2. read target repository startup docs;
3. read ANJIA/project coordination docs if the task belongs to the FH8626 case;
4. refresh live OpenIPC upstream repository ownership/contribution rules;
5. determine the natural owner before moving code;
6. preserve recovery and known-good evidence before destructive migration;
7. keep Builder thin and platform contracts streamer-neutral;
8. separate source/build/runtime/hardware/upstream acceptance;
9. curate contribution history only after the intended implementation is validated.

Do not let historical preservation layout dictate final OpenIPC architecture.

## 11. Roles

Default: Implementer.

Independent Reviewer required for serious:
- architecture/ownership changes;
- multi-repository changes;
- boot/kernel/storage/hardware-critical work;
- destructive/recovery-sensitive changes;
- infrastructure/permission changes;
- release/upstream contribution preparation;
- replacement of known-good hardware-proven contracts.

Use Orchestrator when multiple agents/repos have parallel scopes and need explicit fan-in/dependency ownership.

## 12. Local context

`local_context: OPTIONAL`

Repository/API/reverse work should continue without machine-specific context.

If a task requires owner WSL paths, target address/transport, local toolchain, physical device state or another missing local fact, report degraded context once and do not guess it.

## 13. Project learning

Project-specific chronology stays with the source project.

Reusable errors, best practices, prompt/role/tooling lessons and workflow evolution are aggregated into:
https://github.com/ArthurKoba/ai-agent-workflow/tree/main/audit

Do not recreate universal error/prompt catalogs inside each reverse repository.
