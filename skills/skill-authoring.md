# Skill Authoring

Apply when creating, editing, reviewing, merging or splitting skills.

1. **Describe decisions.** State the trigger, required inputs, reasoning or
   search strategy, decision points, expected evidence and stop/completion
   criteria. Describe the method, not a transcript of tool calls.

2. **Leave tool selection to the agent.** Specify capabilities and verification,
   not MCP names, exact commands, parameters or fixed call sequences. The agent
   discovers the available tools and checks their current descriptions, schemas
   and permissions before using them. Prescribe an exact tool, command or order
   only when required by a real safety constraint, protocol or integration
   contract; explain that exception briefly.

3. **Keep only operational content.** Remove obvious advice, filler, repeated
   rules, tutorials, lengthy examples and implementation-specific details.
   Keep every condition that materially changes an action, decision or check.

4. **Use the smallest file structure.** A self-contained skill is one
   `skills/<name>.md` file, **at most 32,768 UTF-8 bytes (32 KiB)**. This is a
   hard ceiling, not a size target. If too large, first eliminate unnecessary
   text and duplication without losing unique requirements. Only if it still
   exceeds the limit, use `skills/<name>/README.md` as a short router to
   independent, task-specific modules. Each Markdown file stays within the
   limit; do not require unrelated modules to be loaded.

5. **Preserve correctness when changing files.** On a move or split, update
   inbound routes and relative links, compare old and new requirements for
   omissions, and verify the result with repository checks. Do not restore
   superseded duplicates merely to preserve history.
