# LLM-maintained Wiki

This reference describes a persistent knowledge-base pattern for long-running work with LLM agents.

## Core idea

Ordinary retrieval answers a question by finding source fragments each time. A persistent LLM-maintained wiki adds a durable synthesis layer: the agent integrates useful knowledge once, links it to related concepts, records contradictions and updates existing pages as new evidence arrives.

The wiki is cumulative, but it is not automatically the source of truth. Source repositories, authoritative documents and live systems remain authoritative for facts they own.

## Three layers

### Sources

Original material: repositories, documents, meeting notes, datasets, web sources, logs or other evidence. Preserve provenance and do not rewrite source evidence merely to make the wiki consistent.

### Wiki

LLM-maintained Markdown pages containing summaries, concepts, entities, decisions, comparisons and cross-project synthesis. The agent may update this layer as evidence changes.

### Operating contract

`AGENTS.md`, Project instructions or another routing document defines:

- where source authority lives;
- how pages are named and linked;
- what belongs in project vs shared knowledge;
- how contradictions are represented;
- how ingestion and maintenance are validated.

Do not copy the whole wiki into the operating prompt.

## Main operations

### Ingest

1. Read the new source and identify its authority/provenance.
2. Extract durable facts, decisions and relationships.
3. Update existing owner pages before creating new pages.
4. Create a new page only when the concept has a stable independent owner.
5. Add links from indexes/related pages.
6. Record contradictions instead of silently overwriting incompatible evidence.

### Query

1. Start from indexes/search to identify likely owner pages.
2. Read a bounded set of relevant pages.
3. Return the answer using source/live evidence when freshness matters.
4. If the resulting synthesis is reusable, write it back to the appropriate owner page rather than leaving it only in chat history.

### Lint

Periodically check for:

- orphan pages;
- broken/unresolved links;
- duplicate owners for one concept;
- stale claims superseded by newer evidence;
- contradictions that were never resolved;
- generic filenames that lose ownership context;
- important recurring concepts that have no stable page.

## Index and log

A content index and a chronological change log solve different problems.

- The index helps agents discover what knowledge exists and where its owner is.
- The log records what changed and when; it is useful for recent-history inspection but should not become a second architecture/source-of-truth document.

Both are optional. Small knowledge bases may need only an index.

## Search and graph tooling

Full-text search, vector/BM25 retrieval, backlinks and graph traversal can improve discovery as the corpus grows. They are acceleration layers, not authority layers.

If an external semantic index is used, keep reindex/cache-refresh behavior explicit after renames or large structural changes.

## Human/agent responsibilities

Humans or project owners curate goals, sources and important decisions. Agents perform the repetitive maintenance: synthesis, linking, index updates, contradiction detection and consistency checks.

## Design rule

Keep the system modular. A project may use plain Git Markdown, Obsidian, a semantic index, or another editor/search surface. The durable contract is ownership + provenance + linked synthesis, not a specific UI or plugin.
