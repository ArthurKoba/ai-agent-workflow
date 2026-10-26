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

4. **Use the smallest file structure.** Every new or changed skill Markdown
   file is limited to **5,000 Unicode characters**, including spaces,
   frontmatter and line breaks normalized to LF; this is not a byte limit
   or a size target. First remove duplication without losing requirements.
   If still too large, use `skills/<name>/README.md` as a short router to
   focused modules, each within the same limit. Preserve established entry
   paths as short routers when needed. Do not load unrelated modules.
   Unchanged legacy files are migration debt, not a reason for a bulk rewrite.

5. **Preserve correctness when changing files.** On a move or split, update
   inbound routes and relative links, compare old and new requirements for
   omissions, and verify the result with repository checks. Do not restore
   superseded duplicates merely to preserve history.
