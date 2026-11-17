# Arthur Koba AI Agent Workflow — selectable packages

The [marketplace manifest](../.agents/plugins/marketplace.json) is
published from https://github.com/ArthurKoba/ai-agent-workflow, Git ref
`main`. It offers **6 installable plugins, containing 19 distinct Skills**.
The packages group tasks by *kind of work*, not by development phase.

| Installable plugin | Included Skills | Who needs it |
| --- | --- | --- |
| **Development** | `backend-engineering`, `software-architecture`, `project-bootstrap`, `frontend-engineering`, `interface-design-review`, `software-testing`, `code-review` | Software development as a whole: Rust/Python/Go backend, frontend, architecture, testing, code review |
| **DevOps** | `git-workflow`, `terminal-operations`, `services-deployment` | Git, terminal and infrastructure work |
| **Agent Workflows** | `orchestration`, `context-engineering`, `skill-authoring`, `workflow-audit` | Building and orchestrating AI-agent workflows |
| **Research** | `reverse-analysis`, `openipc-porting`, `scientific-visualization` | Program analysis, firmware porting and technical research |
| **Domains** *(optional)* | `domain-acquisition` | Registrar price/availability research, buying, renewing, transferring domains, and DNS/mail continuity |
| **Browser Access** *(optional)* | `remote-browser-session` | Reusing an authorized browser session, managing tab/DevTools/extension permissions and reconnection |

**Backend + architecture + frontend + quality are ONE Development
installation.** These remain distinct task-routed Skills *inside* that
single plugin; their reference modules are read conditionally.
Backend is language-independent, and a Rust task does not imply Python
or PostgreSQL requirements.

The optional **Domains** plugin is not DevOps: it handles registrar
procurement and domain ownership economics. The optional **Browser Access**
plugin is not a browser or an automation tool: it governs safe authorization
and reuse of an operator-controlled remote browser. Neither is required
for normal development, DevOps, research or agent orchestration.
Users who don't need them should not install them.

## Upgrading

The former all-in-one plugin `ai-agent-workflow` and the earlier short-lived
`arthur-koba-backend`, `arthur-koba-architecture`,
`arthur-koba-frontend` and `arthur-koba-quality` plugin cards are **retired
from the marketplace**, but ChatGPT may retain already installed copies.
Uninstall retired copies in the client UI when replacing them with
`arthur-koba-development`. Otherwise duplicate Skills may remain active.
A marketplace refresh does not uninstall plugins from a user's account.

Each plugin is independently usable and includes its own local
reference closure. No plugin requires Briareus, another package,
credentials, running MCP Hands or a Git clone. The public package names
retain the Arthur Koba AI Agent Workflow identity. No personal logo has
been added.

## Source authority

The task routes and plugin membership are owned by [the Skill
Map](../skills/README.md). Each `##` section is an installable plugin;
each entry is one Skill. The generator
[build-plugin-marketplace.py](../scripts/build-plugin-marketplace.py)
uses those routes, rejects unknown/empty/duplicate categories and
regenerates only the managed files under `plugins/`. Do not modify
generated copies manually.

Regenerate via `python3 scripts/build-plugin-marketplace.py` when
changing sources. Git hooks and CI check deterministic generated output;
the event-driven publisher commits it to `main`. It does not rebuild
Briareus or install plugins for users. ChatGPT UI refresh and activation
are separate client-side steps.
