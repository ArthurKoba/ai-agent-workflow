# OpenIPC Porting / Firmware Migration / Contribution

Use this skill for:
- adding a new camera/SoC to OpenIPC;
- migrating a vendor camera to OpenIPC;
- splitting work between Linux/Firmware/Builder/streamer/U-Boot;
- preparing changes for upstream contribution;
- reconciling a preservation snapshot into maintainable OpenIPC architecture.

This module is an engineering workflow, not a source of permanent upstream facts. OpenIPC rules and repository ownership can change; refresh live upstream documentation before contribution work.

## 1. Establish target truth first

Before implementation, identify and record the target-specific facts actually proven:
- SoC/revision;
- board/device identity;
- sensors;
- flash geometry;
- RAM;
- network/PHY;
- storage;
- bootloader;
- GPIO/power/reset/clock sequencing;
- media/ISP/audio/PTZ dependencies;
- known recovery paths.

Separate:
- factory observation;
- hypothesis;
- source/reverse-confirmed contract;
- hardware-proven behavior.

Do not generalize one retail board into SoC-wide truth without evidence.

## 2. Preserve recovery before migration

Before destructive flash/layout/boot work:
- preserve a complete recovery path;
- retain unique factory firmware/flash evidence;
- document serial/bootloader/recovery access;
- prefer RAM/non-destructive bring-up where practical;
- verify external recovery when migration risk justifies it.

A working factory layout is valuable evidence, but not automatically the target OpenIPC architecture.

## 3. Use OpenIPC conventions as the product target

When OpenIPC already has a standard convention for:
- partitioning;
- environment variables;
- package placement;
- device composition;
- kernel ownership;
- updater artifacts;
- streamer integration;

prefer the OpenIPC-native convention over preserving factory quirks.

Retain factory compatibility only when it is needed for migration/recovery or is technically required by the hardware.

## 4. Map every change to its natural owner

Before moving/adding code, determine the current upstream repository ownership from live OpenIPC docs.

Current model must be verified live, but typical separation is:

- kernel source/drivers/SoC kernel work → OpenIPC Linux repository;
- shared Buildroot packages/configuration/runtime integration → Firmware;
- device-specific minimal overlay/configuration → Builder;
- streamer/HAL implementation → streamer repository;
- probing/diagnostic tooling → the current OpenIPC diagnostic/tool repository;
- documentation/how-to → current OpenIPC docs/wiki authority;
- U-Boot → the current SoC/family U-Boot ownership selected by OpenIPC maintainers.

Do not keep a file in a repository merely because that is where the historical migration snapshot happened to contain it.

## 5. Builder must stay thin

For a named device profile:
- keep only genuinely device-specific deltas;
- reuse common Firmware/kernel/streamer support;
- avoid copying generic packages or entire runtime trees;
- avoid raw binary blobs when a reproducible source/package owner exists;
- compose variants from common device base + small runtime-specific fragments when multiple streamer/diagnostic directions exist.

Current upstream Builder explicitly asks contributors to minimize device files and keep common material in Firmware. Recheck this before contribution.

## 6. Keep camera/platform contracts streamer-neutral

Sensor sequencing, ISP/media lifecycle, board GPIO/power, audio/PTZ and boot contracts should not exist only inside one streamer branch.

Store durable platform/device knowledge in the project coordination authority and implement it in the natural owning repositories.

A Divinus or Majestic implementation may prove a contract; it should not monopolize that contract.

## 7. Treat proprietary/runtime blobs as transitional dependencies

Classify every retained binary:
- unique primary evidence;
- temporary runtime dependency;
- reproducibly source-built output;
- replaceable/retired.

A factory-extracted blob may be necessary for bring-up, but it is not the desired final source contribution merely because it works.

Do not remove a runtime-critical dependency before a replacement/package owner exists.

## 8. Separate migration branch from contribution series

During exploration:
- work on a clear development line;
- use topic branches only where isolation helps;
- preserve known-good hardware checkpoints;
- keep PR-facing/submission branches out of scratch development.

Before upstream:
- reread live upstream base/rules;
- reconstruct/curate coherent commits from the verified base if migration history is noisy;
- compare final tree with the intended tested implementation;
- keep generated artifacts out of source history unless upstream policy explicitly requires them;
- use one controlled submission/history update, not repeated force-pushed checkpoints.

## 9. Validation ladder

Track separately:
- reverse/source confidence;
- host/static checks;
- build;
- artifact/layout inspection;
- RAM/live test;
- cold boot;
- subsystem hardware acceptance;
- full product/runtime acceptance;
- upstream/release readiness.

Never promote a reconstructed or rebuilt artifact by inheriting a PASS from different bytes.

## 10. Cross-repository integration

When one repository changes a contract/ref/ownership boundary:
- update the project coordination authority in the same iteration;
- propagate the change to dependent repos deliberately;
- avoid stale branch/ref documentation;
- verify the actual Builder/Firmware composition consumes the intended kernel/runtime/streamer state.

Do not make the user manually relay shared platform facts between parallel agents if the agents can read a shared authority.

## 11. Upstream refresh before contribution

Immediately before OpenIPC contribution work:
1. open the target OpenIPC repository;
2. read current README/AGENTS/CLAUDE/contribution/review rules;
3. inspect current base branches and repository ownership;
4. open current OpenIPC documentation/wiki pages relevant to the change;
5. compare those live rules with the local project summary;
6. update the local summary if stale;
7. only then curate the contribution.

Local cached rules are a convenience, not authority over current upstream.

## 12. Contributor package

For substantial new platform/device support, prepare:
- concise target identity;
- scope/ownership map;
- source series;
- build instructions/results;
- hardware validation evidence;
- recovery/provenance notes where boot/flash is involved;
- known unsupported/pending features;
- exact upstream base/rules rechecked.

Do not present “works on my migration tree” as equivalent to an upstream-ready contribution.

## 13. Completion

OpenIPC porting is not complete merely because:
- firmware builds;
- bootloader starts;
- one stream works;
- one streamer works;
- the device appears in Builder.

Completion is defined by the project acceptance surface: boot/update/recovery, kernel, media, device functions, selected runtime variants, reproducible build integration and the intended upstream/contribution state.


## Buildroot / WSL preflight

OpenIPC Firmware/Builder builds use Buildroot and should run in a clean Linux build environment.

When the owner build surface is WSL:
- treat WSL as a Linux build lane, not as a Windows shell with Linux commands;
- before Buildroot/OpenIPC build commands, ensure `PATH` does not contain inherited Windows entries such as `/mnt/c/.../Program Files/...`;
- use the project/local Linux-only `PATH` contract and run `hash -r` before starting the build;
- keep the working tree/output/toolchain on a Linux filesystem when practical;
- do not diagnose a Buildroot `PATH contains spaces/TAB/newline` failure as a source/build-system defect before checking Windows→WSL environment leakage.

If the project has already established a canonical clean WSL build `PATH`, reuse that exact contract instead of inventing a new one for each camera/build.

This preflight is part of the build lane and should be applied before retrying a failed Buildroot build caused by environment contamination.
