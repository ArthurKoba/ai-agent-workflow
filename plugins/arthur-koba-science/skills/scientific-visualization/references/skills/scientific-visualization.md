# Scientific Visualizations — Editable Diagrams and Quantitative Charts

Load this skill when creating, modifying, reviewing, exporting or embedding an algorithm, block/functional diagram, plot or scientific figure. A vector export, editable original and reproducible numeric source are separate deliverables; none substitutes for the others.

## Select the authoring workflow

- **Algorithm and functional/block diagram:** author in an editable diagram editor; use connected Draw.io MCP wherever the project mandates diagrams.net. Save native .drawio and publish genuine vector SVG, sourced from the same geometry. A screenshot, generated picture, or raster wrapped in SVG is not an editable diagram.
- **Electrical/circuit diagram:** require actual board, connections, components, pins and sourced power/signal values. Use the applicable CAD and electrical standard. A functional flowchart is not an electrical drawing.
- **Measured or calculated chart:** use the preserved spreadsheet or reproducible plot script plus exact input data. Excel-style charts are preferred where practical; Matplotlib SVG is an acceptable reproducible fallback.
- **Original raster evidence:** preserve authentic source and metadata. Never convert an unknown picture into a purportedly accurate vector or fabricate missing features.

Use the editor whose capabilities are supported by current tools; respect project-specific mandatory tool requirements. A valid SVG cannot replace opening and examining its native editable file.

## Diagram construction — graph first, geometry second

1. List every symbol and directed relation before drawing: node IDs, inputs, outputs, decision alternatives, failure paths and return loops. Use the applicable diagram-symbol standard (e.g. ISO 5807 / GOST 19.701 for algorithms where applicable): rectangle for process, diamond for decision, parallelogram for input/output. A component-level functional diagram does not substitute for an executable decision algorithm.
2. Arrange nodes on a regular grid with room for readable labels. Use short Russian labels in Russian documents. Draw connectors orthogonally, with consistent stroke weight, one clear direction and no line through another block or its text. Put caption, method and long explanations **below the figure**, not inside its geometry.
3. For a straight **primary path between two blocks**, create **one direct edge** from its source contour to its destination contour. Do NOT split that edge through a transparent/invisible intermediate node to attach another branch: diagrams.net autorouting can add a visually disastrous zigzag or disconnect.
4. A **secondary branch** approaching the main vertical or horizontal trunk ends with a **single arrowhead at the trunk**, if that is the intended directional merge. The main trunk stays continuous and straight; it has its own final arrowhead at the receiving block. Do not draw a junction dot, duplicate heads, an elbow immediately before the receiving block, or two competing terminal arrows.
5. Place separate side arrivals at separate heights. Crossing two lines without connecting them is not a merge. If routing requires a join placeholder in the editor, it must not become an endpoint or waypoint **on the primary path**. The visual junction has no dot, no gap and no overlap.
6. Label **both** exits of each diamond, e.g. да/нет; keep labels next to the correct segment, outside symbols. Route reject and retry paths in free lanes. Never let one branch pass through an unrelated decision or connector label.
7. Attach arrows to the **visible perimeter**, not the shape's bounding rectangle. For parallelograms, compute the sloped side exactly. If the algorithm returns from an output parallelogram to an input parallelogram, normally leave from the **bottom midpoint of the output** and enter the **top midpoint of the input**; route along a separate outer corridor. Do not attach to the sloping sides when the figure requires top/bottom.
8. On every change, inspect **all** connections and decisions. Moving one block can make previously accepted connections, labels or returns invalid. Preserve the meaning and unaffected verified elements.

## Required diagram acceptance gate

Inspect the **current editable file AND exported SVG**. Verify:

- Every edge has an existing source and target, arrives at the actual visible shape outline, and represents the intended control/data flow. Review every edge, not a sample.
- Every segment is orthogonal (unless the notation requires otherwise); no zero-length segment, accidental crossing, unintended overlapping section, gap or wire through a foreign block.
- Every intentional joining branch hits the continuous primary segment at the declared point. Confirm the main segment is a **single direct edge** without waypoints or inserted logical vertices. Check the right number and location of arrowheads; no junction dots.
- Every diamond has the required outcomes; no yes/no label lies on a symbol or another line. Input/output return loops have the specified top/bottom ports.
- SVG paths, arrow tips, visible text and node coordinates match the editable source. If Draw.io auto-routes after opening, recheck it: a correct offline SVG with a broken interactive source is a FAILURE.
- Render and inspect the entire sheet at manuscript scale and **magnified crops of each junction, diamond, return and sloping connector**. XML parsing, graph counts or a lint pass do not prove visual quality. Reject the figure on any visible dangling arrow, zigzag, clipping or overlapping labels.

Automate topology, visible-contour endpoint, arrow-count, decision-label, SVG/source parity and intersection checks when possible. Rerun regression checks after each edit. Commit the original and SVG together.

## Scientific charts: restrained Excel-like presentation

- Obtain real measurements or execute a declared, deterministic mathematical/model calculation. Keep provenance and distinguish MODEL EXAMPLE from MEASURED RESULT. Never invent data merely to draw attractive curves.
- Prefer a readable **Microsoft Excel-like flat line/bar/scatter chart**: thin unobtrusive gridlines, sensible tick marks, restrained line widths and colors, no 3D decoration, shadows or ornamental backgrounds. Matplotlib/Python can produce an equivalent scientific SVG, especially when spreadsheet SVG export is unavailable.
- Both axes must carry the **quantity and unit** (e.g. Время, с; Частота, Гц; Темп, долей/мин), numeric ticks and an intelligible scale. Dimensionless measures must be clearly identified when needed. Check interval direction, unit conversions, decimal placement, legend values, normalization and uncertainty; never create a misleading truncation.
- **No long prose or explanation inside the plot.** Normally omit plot titles: the figure caption below it supplies subject, dataset and method. If multiple subplots, use small **Cyrillic** letters А, Б, В as necessary and explain each panel below. Do not confuse Cyrillic А with Latin A.
- A compact legend is allowed when multiple curves differ. Explain curve color, dash style or marker with short Russian labels; do not rely solely on red/green. Keep math symbols and short panel identifiers; move interpretations to prose.
- All visible labels in a Russian paper are Russian, apart from fixed symbols, units and necessary proper terms.

### Reproducible spreadsheet-first workflow

Store a real .xlsx workbook (or project-approved spreadsheet format) with the scientific artifacts. Organize actual sheets for original measurements/imports, parameters, formulas/calculations, summaries and charts when useful. **Every derived number must arise from recorded spreadsheet formulas or documented executable computation**, not manually typed facsimiles. Link series to actual calculated ranges and retain precision, filters, source file identifiers, denominators, units and any recalculation assumptions.

Export to SVG only if the available Excel-compatible stack **actually provides valid vector export**. Verify all SVG curves and labels against the workbook's real chart/source values. Do not assert that Excel produced an SVG merely because a workbook exists. If the workbook cannot export reliable SVG, retain it as the calculation source and render the exact same dataset with a saved Python/Matplotlib script to vector SVG. Preserve the workbook, code, source data and relative figure links together under the project's governed artifact location, not only in a temporary workspace.

## Integration and handoff

Use the repository's scientific figure ID and caption scheme. Insert SVG in the Markdown manuscript with stable cross-references; keep source workbook or .drawio tracked alongside it. Provide the reviewer with: exact source and SVG paths, reproducible data/formulae, inspection renders, unresolved limitations, checks and Git SHA. Acceptance of rendering does not establish experimental validity, and repository lint does not substitute for visual inspection in the final Word/PDF at actual print scale.
