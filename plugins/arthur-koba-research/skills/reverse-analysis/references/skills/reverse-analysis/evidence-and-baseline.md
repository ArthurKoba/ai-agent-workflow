## Evidence-first

- Check existing analysis, names and proof before re-tracing a closed behavior.
- Prefer one canonical indexed project and preserved target bytes/source over
  extracting or importing duplicate mutable copies.
- Record the target's identity where relevant: version, binary hash, PE/ELF
  section layout, firmware/BIOS region, platform, CPU/language, image base,
  address mapping, relocations, loader/compiler and ABI assumptions.
- Define the observable question and the next evidence boundary before
  starting a broad scan.

## External reference stopping rule

External SDKs, symbols, PDB/DWARF data, libraries, protocol documents,
vendor information and related builds are possible clues, **not proof of
the target's behavior**. Use them when they materially reduce uncertainty.

For a poorly documented program, chipset or proprietary application,
once broad searches for sources and documentation have been exhausted,
do not repeat them as a ritual on each session. Reopen research only with
a new concrete lead (exact version, hash, symbol server, vendor SDK,
artifact locator, document or direct user request). Preserve useful and
negative search results. Target code and observed behavior take precedence
over analogies to another version or platform.

## Mandatory high-level-first analysis after import

1. **Identify and enable the architecture.** Inventory every imported module
   and classify executable code, ACPI/bytecode and data. Verify format, ISA,
   ABI, loader and mapping; attach the correct analyzer support. If missing,
   implement/integrate the decoder, language/loader and decompiler before
   claiming native-code coverage; record unsupported regions explicitly.
2. **Preserve the known-good project first.** Before any full-system pass,
   checkpoint/backup the canonical project and verify that saved names, types,
   structures, links and comments can be recovered. Never erase prior analysis,
   overwrite annotated programs or run destructive reanalysis just to get C.
3. **Analyze and decompile the complete inventory.** Complete (or reuse proven
   completed) auto-analysis for every executable module, then run a bounded,
   resumable **bulk decompilation of every discovered native function**, not
   just individually selected functions. Record total/success/failed/unsupported
   per program, the exact failure, and a project-linked index of generated
   C-like pseudocode. Do not claim full conversion with unprocessed functions.
   Native tracing/refactoring starts from this complete high-level baseline.
4. **Work on analyzer-generated pseudocode.** Generated C-like output is the
   primary representation: recover names, prototypes, types, structures and
   fields in the canonical analysis database; regenerate affected C after
   repairs and save/read back. **Do not hand-write, invent or maintain your
   own pseudocode/C translations of functions** as a substitute for a complete
   analyzer pass. A separately authored model is allowed only for a documented,
   narrow unsupported/ambiguous construct and must be labeled as a model,
   never recovered source or a second authoritative codebase.
5. **Use low-level evidence only when necessary.** Decompilers can misread an
   ABI, width, indirect call, branch, register or side effect. Inspect bounded
   instructions/registers/IR/bytes for that specific uncertainty, repair
   metadata and return to regenerated pseudocode. Continuous assembly/hex-first
   analysis is not the default while high-level output is available.
6. **Use the right representation.** Inspect ACPI AML as decompiled ASL;
   use an appropriate high-level decoder for other bytecode/packet formats.
   Do not force data-only regions into native C or claim missing support was
   successfully decompiled.
