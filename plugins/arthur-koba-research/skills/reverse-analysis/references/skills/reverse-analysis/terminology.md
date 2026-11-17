## Terminology, semantic contracts and evidence

Use this terminology for both high-level program behavior and native code.

### Vocabulary

Use stable names for concepts: **program**, **module**, **function/method**,
**callback**, **handler**, **state**, **input**, **output**, **side effect**,
**dispatcher**, **branch/transition**, **producer/consumer**, **behavior
contract**, **evidence point** and **semantic coverage**.

Different analyzers may use different names for code units. Check the selected tool's published vocabulary and never equate code with a device or data object.

Raw instruction/register names, ABI/API signatures, imported symbols,
addresses and protocol IDs remain exact evidence even after semantic renaming.

### User-facing terminology

The reusable English vocabulary describes analysis concepts and tool contracts;
it does not require English in reports or human-facing comments. Use the
active project's language and localized business/technical terms when known.
Keep raw identifiers, instructions, registers, API names, symbol spellings and
addresses exact where they are evidence; do not translate those identities.
Project-owned terminology takes precedence over illustrative skill examples.

### Evidence states

- **CONFIRMED**: primary target evidence directly supports the claim:
  instructions, control/data flow, source, runtime observations, or verified
  hardware evidence if applicable.
- **LIKELY**: multiple independent clues support a bounded hypothesis but
  the precise behavior is not fully proved.
- **UNKNOWN**: available information cannot establish the claim.
- **CONTRADICTION**: authoritative findings disagree; affected semantics
  must not be treated as settled.
- **WITHDRAWN**: a historical interpretation was invalidated; this is not
  a live confidence state.

An imported API, SDK feature or code path does not automatically prove that
it runs or is exposed. A firmware capability additionally does not prove
physical wiring. Keep capability, reachability, execution and topology
claims separate.
