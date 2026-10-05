# Persistent Knowledge Base

Use this skill when designing or maintaining a Git-backed LLM/project wiki: project spaces, shared knowledge, decision pages, cross-links, ingestion/synthesis and optional Obsidian graph maintenance.

## Model

Keep three concerns separate:

- source/project authority — raw documents, repositories and live systems;
- persistent knowledge base — synthesized reusable knowledge and links;
- agent policy — account/project/skill/role instructions.

A knowledge base is not a substitute for current source/state authority. It accelerates discovery and preserves synthesis; live facts still require the owning source.

## Recommended layout

```text
wiki/
  wiki-index.md
  wiki-log.md
  shared/
    shared-index.md
  projects/
    projects-index.md
    <project>/
      <project>-index.md
      <project>-context.md
      <project>-architecture.md
      <project>-decisions.md
      <project>-open-questions.md
  meta/
```

This is a reusable default, not a mandatory filesystem contract. Existing repositories may use another structure.

## Ownership

- Project-specific architecture/decisions → that project's space.
- Cross-project knowledge → shared owner with project pages linking to it.
- Mandatory agent behavior → workflow/project/skill authority, not the wiki.
- Dynamic runtime facts → state/local-context authority, not durable narrative pages.

## Agent workflow

1. Start from the knowledge-base index and the project/repository authority map.
2. Read only pages relevant to the question or change.
3. When new evidence changes durable knowledge, update the owner page and dependent links in the same iteration.
4. Record contradictions explicitly; do not silently reconcile incompatible sources.
5. Periodically lint for orphan pages, stale claims, duplicated owners and broken links.

## Optional modules

- `llm-wiki.md` — conceptual model and ingestion/query/lint ideas.
- `obsidian-graph/README.md` — optional Obsidian Graph maintenance workflow.

Obsidian, vector search and Second-Brain-style tools are optional interfaces. Git/source files remain the durable authority unless a Project explicitly declares another system.
