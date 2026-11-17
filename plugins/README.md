# Arthur Koba AI Agent Workflow — selectable marketplace plugins

This independent GitHub repository owns the [marketplace
manifest](../.agents/plugins/marketplace.json). Import it in ChatGPT
from https://github.com/ArthurKoba/ai-agent-workflow, ref `main`,
without selective paths. The marketplace contains **8 separately
installable plugins with 19 distinct Skills**. Each plugin is useful by
itself and bundles its own selected Skills and relevant reference
documents; neither other plugins nor Briareus are prerequisites.

| Plugin | Included Skills | Recommended for |
| --- | --- | --- |
| Backend | `backend-engineering` | Backend/API/service developers, including Rust or Python |
| Architecture | `software-architecture`, `project-bootstrap` | Software architects, new project/toolchain setup |
| Frontend | `frontend-engineering`, `interface-design-review` | Frontend/UI developers and reviewers |
| Quality | `software-testing`, `code-review` | Testers, QA and code reviewers |
| DevOps | `git-workflow`, `terminal-operations`, `services-deployment`, `domain-acquisition` | Infrastructure operators and Git workflows |
| Agent Workflows | `orchestration`, `context-engineering`, `skill-authoring`, `workflow-audit` | People creating and coordinating AI agents |
| Research | `reverse-analysis`, `openipc-porting`, `scientific-visualization` | Reverse engineering, porting and technical research |
| Browser Sessions | `remote-browser-session` | Optional remote browser/tab permission management |

## Upgrade from the old all-in-one package

The previous installable plugin `ai-agent-workflow` has been **retired from
the marketplace**, not silently replaced in the client's installed apps.
If that old plugin is still installed in ChatGPT, **uninstall it using
the client's plugin management**, then install only the new categories
you need. Otherwise old and new Skills may be exposed twice. Refreshing
the marketplace alone does not uninstall an existing client plugin.

Each category is a plugin card, not a separate Git repository; everything
continues to be published under the one Arthur Koba marketplace.
Skill frontmatter and each plugin's display name carry human-readable
names. A generic plugin icon is independent from a Skill's folder
and no personal logo is included in these packages.

## Source of truth and publishing

The authoritative library remains under [skills](../skills/README.md).
Each `##` section in that task map owns membership of exactly one package.
The generator [build-plugin-marketplace.py](../scripts/build-plugin-marketplace.py)
discovers Skills from that map, copies only their relevant reference closure,
and fails closed if a category has no Skills, has an unknown name, or a Skill
appears more than once. Generated files are tracked under
`plugins/arthur-koba-*/`. **Do not edit generated copies by hand.**

Run `python3 scripts/build-plugin-marketplace.py` before committing.
The Git hook and CI validate deterministic output. An event-driven
GitHub Actions publisher regenerates and commits generated packages on
source changes without depending on Briareus, remote credentials,
Docker rebuilds or recurring polling. GitHub publication does not
prove the installed client has refreshed or activated any plugin.

Browser Sessions is optional and provider-neutral; it governs session
reuse and permissions, not a legacy connector. Concrete provider APIs,
endpoints and deployment troubleshooting belong to the selected provider's
own project Skill, not this universal library.
