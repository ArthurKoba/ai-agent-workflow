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

Regenerate after changing an owner document with:

    python3 scripts/build-plugin-marketplace.py

The existing pre-push and GitHub CI verification also check that generated
package contents exactly match the authoritative library. The published
Git branch is the delivery artifact; an installed marketplace's refresh
cadence and automatic activation are client-product concerns, not an upstream
GitHub Actions or Docker deployment.
