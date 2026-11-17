## Required diagram acceptance gate

Inspect the **current editable file AND exported SVG**. Verify:

- Every edge has an existing source and target, arrives at the actual visible shape outline, and represents the intended control/data flow. Review every edge, not a sample.
- Every segment is orthogonal (unless the notation requires otherwise); no zero-length segment, accidental crossing, unintended overlapping section, gap or wire through a foreign block.
- Every intentional joining branch hits the continuous primary segment at the declared point. Confirm the main segment is a **single direct edge** without waypoints or inserted logical vertices. Check the correct arrowheads and whether real junctions have (or omit) dots according to the applicable notation; do not mark crossings as joins.
- Every diamond has the required outcomes; no yes/no label lies on a symbol or another line. Input/output return loops have the specified top/bottom ports.
- SVG paths, arrow tips, visible text and node coordinates match the editable source. If Draw.io auto-routes after opening, recheck it: a correct offline SVG with a broken interactive source is a FAILURE.
- Render and inspect the entire sheet at manuscript scale and **magnified crops of each junction, diamond, return and sloping connector**. XML parsing, graph counts or a lint pass do not prove visual quality. Reject the figure on any visible dangling arrow, zigzag, clipping or overlapping labels.

Automate topology, visible-contour endpoint, arrow-count, decision-label, SVG/source parity and intersection checks when possible. Rerun regression checks after each edit. Commit the original and SVG together.

## Integration and handoff

Use the repository's scientific figure ID and caption scheme. Insert SVG in the Markdown manuscript with stable cross-references; keep source workbook or .drawio tracked alongside it. Provide the reviewer with: exact source and SVG paths, reproducible data/formulae, inspection renders, unresolved limitations, checks and Git SHA. Acceptance of rendering does not establish experimental validity, and repository lint does not substitute for visual inspection in the final Word/PDF at actual print scale.
