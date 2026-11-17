# AI Agent Workflow plugin marketplace

The source owner is this repository, not Briareus. Its marketplace is at
[marketplace.json](../.agents/plugins/marketplace.json).

Import from GitHub with source https://github.com/ArthurKoba/ai-agent-workflow,
Git ref main and no selective paths, then install the single **AI Agent Workflow**
plugin. It bundles **18 independent Skills** under its skills directory.
ChatGPT selects skills by task. The user does **not** need to install each skill
as a separate plugin or open this repository to read routine reference modules.

Each skill has a short entrypoint and a self-contained local reference closure
derived from the existing authoritative library. Original skills remain in
the top-level skills directory; do not edit generated copies. The plugin
package does not carry credentials, project accounts, tools, registered Briareus
MCP app IDs, or project-specific operating state.

An event-driven GitHub Actions publisher regenerates and validates the
native Skill package after relevant changes in the source library, then
commits only generated marketplace files to main if they changed. It does
not invoke Briareus, require a cross-repository secret, schedule polling,
or rebuild any MCP image.

For local development, regenerate before committing a changed owner file:

    python3 scripts/build-plugin-marketplace.py

The tracked Git pre-push hook checks deterministic generated contents;
CI first generates the package to validate the candidate source, and the
publisher separately verifies and publishes the final Git version. The
installed ChatGPT client's refresh cadence and activation remain client
behavior and are not guaranteed by the GitHub push alone.
