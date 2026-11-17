# Arthur Koba AI Agent Workflow — selectable packages

The [marketplace manifest](../.agents/plugins/marketplace.json) is
published from https://github.com/ArthurKoba/ai-agent-workflow, Git ref
`main`. It offers **6 independently installable plugins with 28 Skills**.
Each package groups a kind of work, not a software-development stage.
Backend, frontend, architecture and quality belong to **one Development
package**. Each package is self-contained and installable without Briareus.

| Package | Skills | Purpose |
| --- | --- | --- |
| **Development** | `backend-engineering`, `software-architecture`, `project-bootstrap`, `frontend-engineering`, `interface-design-review`, `software-testing`, `code-review` | Software development, Rust/Python/Go backends, UI, architecture, tests and review |
| **DevOps** | `git-workflow`, `terminal-operations`, `services-deployment` | Git, terminals, infrastructure and deployments |
| **Agent Workflows** | `orchestration`, `context-engineering`, `skill-authoring`, `workflow-audit` | Designing, maintaining and orchestrating AI agents |
| **Software Research** | `reverse-analysis`, `openipc-porting` | Reverse engineering, firmware behavior and OpenIPC porting |
| **Science** | `scientific-research-design`, `scientific-novelty`, `scientific-literature`, `scientific-experiments`, `scientific-implementation`, `scientific-writing`, `scientific-formatting-ru`, `scientific-mathematics`, `scientific-review`, `scientific-visualization` | Research design, scientific novelty, source review, reproducible experiments, implementation evidence, papers, equations, peer review and editable diagrams |
| **Other** *(optional)* | `domain-acquisition`, `workflow-marketplace` | Domain purchase/renewal/transfer and discovering/contributing useful AI Agent Workflow updates |

## Science methods: one package, task-routed Skills

The Science plugin has **10 separate Skills**. Install it once and
read only the matching methodological Skill as the task requires:

- `scientific-research-design` — scientific problem, research objective,
  assumptions, method, measurable proof plan;
- `scientific-novelty` — closest prior work, verifiable difference,
  author contribution and evidence boundaries;
- `scientific-literature` — primary-source discovery, bibliographic
  provenance and critical synthesis rather than abstract lists;
- `scientific-experiments` — reproducible data/baselines, metrics,
  uncertainty and defensible quantitative comparisons;
- `scientific-implementation` — link from method to executable
  algorithm, tested system and real adoption evidence;
- `scientific-writing` — scientific articles, evidence-based prose,
  document structure, venue formatting and editorial review;
- `scientific-formatting-ru` — Russian venue-specific standards,
  typography and publication requirements (opt-in, not global);
- `scientific-mathematics` — formula definitions, domains,
  units, LaTeX fidelity and export checks;
- `scientific-review` — independent science-content gates,
  revision traceability, comment resolution and acceptance;
- `scientific-visualization` — quantitative plots and
  editable diagram/source/SVG, with project/standard-specific
  junction notation and reproducible source data.

These general methods were **synthesized from an existing scientific
research workflow**, not copied wholesale from its private scientific
archive. No unpublished research data, private correspondence,
unique experiments, thesis-specific requirements, fixed degree specialty,
absolute workspace paths or vendor-specific MCP tool calls were
added to the public package.

The **original** research project's discipline, degree/journal
regulations, publishing profile, source corpus and approval decisions
remain its own authority, not global rules. For example, a scientific
specialty passport may be mandatory in one dissertation but does not
apply to all research. Likewise, schematic junction dots depend on
the applicable notation/project contract, not a universal prohibition
or universal requirement. Science does not install Draw.io or any
other external app; connected editors and actual permissions are
selected independently.

`workflow-marketplace` is a new, **on-demand** Skill for checking the
current Arthur Koba AI Agent Workflow source catalog, comparing published
changes against an installed revision when possible, recommending suitable
packages, and contributing reusable improvements with explicit permission.
It does not browse the repository during unrelated tasks, monitor
changes periodically, create unsolicited PRs or install apps automatically.

## Retired packages and migration

The legacy all-in-one `ai-agent-workflow`, short-lived
`arthur-koba-backend`, `arthur-koba-architecture`,
`arthur-koba-frontend`, `arthur-koba-quality`, and former
`arthur-koba-browser` and `arthur-koba-domains` are no longer
offered in the current marketplace.

**The Remote Browser Session Skill was removed entirely from this
repository's current source and generated packages.** Existing
client installations and earlier Git commits are separate:
refreshing a marketplace does not uninstall an already installed
plugin. Remove those retired installations using the client's
plugin management before selecting the replacements, otherwise
duplicate Skills may remain enabled.

Install `arthur-koba-development` for development,
`arthur-koba-research` for software research,
`arthur-koba-science` for diagrams/charts, and
`arthur-koba-other` only when domain ownership or marketplace
discovery/contribution is useful. Each is an independent install.

## Source of truth and publication

[The Skill Map](../skills/README.md) owns plugin membership:
each `##` section maps to exactly one installable plugin and
each entry is one task-routed Skill. The generator
[build-plugin-marketplace.py](../scripts/build-plugin-marketplace.py)
packs each Skill with its local reference closure. Source
documents remain authoritative; never hand-edit generated
content under `plugins/arthur-koba-*/`.

Use `python3 scripts/build-plugin-marketplace.py` to regenerate
the marketplace and `--check` to verify consistency.
The repository's pre-push hook and CI run the necessary tests.
An event-driven GitHub Actions publisher commits generated files
without connecting to Briareus, rebuilding containers or
initiating scheduled checks. GitHub publication does **not**
prove that the ChatGPT client has refreshed or installed a
particular plugin.
