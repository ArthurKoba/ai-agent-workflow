# Arthur Koba Workflow Marketplace — Discover and Contribute

Use this Skill when the user wants to discover reusable agent workflows,
see newly published Arthur Koba AI Agent Workflow Skills, decide which
packages to install, improve an existing workflow, or contribute a new
general-purpose Skill to the library. This is an **on-demand guide**, not
a requirement to browse the repository during unrelated tasks and not
authorization to schedule ongoing monitoring.

## Find relevant skills and changes

1. Identify the user's task, tools, experience and required capabilities.
   Inspect currently installed/enabled Skills first when the client offers
   a trustworthy inventory; a local cache or marketplace sync alone is not
   proof of an active installation.
2. When fresh discovery is requested or genuinely useful, consult the
   authoritative marketplace at
   https://github.com/ArthurKoba/ai-agent-workflow and its
   `.agents/plugins/marketplace.json` and `skills/README.md` on `main`.
   Use the repository's current state, not an old memorized catalog,
   as the source for offered installable packages. If live access is
   unavailable, say so; do not invent recently added Skills or versions.
3. Check source commit/date and compare with the user's verified installed
   revision when available. Classify additions, changed behavior, renamed
   packages and removals separately. Do not claim that Git sync proves
   ChatGPT installed or activated any Skill.
4. Recommend only the package(s) relevant to the requested activity.
   A plugin package contains multiple task-routed Skills. Avoid installing
   an entire marketplace, duplicating similar Skills or mixing universal
   guidance with provider-specific MCP operations without need.
5. Explain the practical benefit and any migration/removal implications.
   Installation, connection and permission changes require the user's
   explicit action or authorization. Do not uninstall existing packages
   or alter user settings merely because a catalog changed.

## Contribute improvements

Before proposing a change, establish whether the idea is broadly reusable
or belongs to a particular project's instructions, MCP provider or
deployment. Universal techniques belong in AI Agent Workflow; specific
tool schemas, production paths, and Briareus-only behavior do not.

If the user authorizes a contribution:
1. Read the repository's current `AGENTS.md` and its linked authoring
   and Git/publication contracts completely, then inspect relevant Skills,
   issue/PR history and existing work to avoid duplicates.
2. Define one reproducible need, intended trigger, scope, source owner,
   expected evidence and acceptance criteria. Modify the canonical Skill
   source and task map, not generated plugin copies.
3. Keep the Skill independent of specific services, project credentials,
   machine paths and deployment state. Respect source attribution,
   licensing, privacy and required reviews.
4. Run the repository's existing generator, focused tests, full relevant
   checks and Git hooks. Validate the resulting packaged Skill and links.
5. Publish only through the permitted identity and repository protections;
   report actual commit/CI status, not an assumed deployment. Let the
   operator decide whether to install or refresh the resulting package.

Record concrete new use cases and recurring workflow defects as candidate
contributions only when supported by evidence. Do not create unsolicited
issues, PRs, recurring searches, notifications or background tasks.

**Completion:** the latest verified relevant Skills are identified, gaps
and freshness limits are explicit, and any approved contribution is
validated and attributed to its actual commit.
