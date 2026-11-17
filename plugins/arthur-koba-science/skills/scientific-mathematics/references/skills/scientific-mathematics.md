# Scientific Mathematics — Formula Completeness and Fidelity

Use when defining, reviewing, importing, editing or publishing
scientific equations and their associated notation. The goal
is **mathematical completeness and faithful rendering**,
not simply obtaining parseable LaTeX, MathML or DOCX.

## Formula meaning comes first

1. Identify the role of each expression in the problem, method,
   algorithm or experiment. Distinguish a known published
   relation from a new derivation, model approximation and
   illustrative example.
2. Define every important symbol and index, its physical/
   mathematical meaning, unit and domain near the equation.
   Keep reused symbols consistent across paragraphs, tables,
   diagrams, code and datasets. Do not silently change
   definitions or normalize dimensions between sections.
3. For sums, products, minimizations, maxima and selected
   subsets, define bounds or the membership predicate,
   including what constitutes the set and whether it
   can be empty. An explicitly defined set can replace
   a numeric upper limit; don't invent one to fill space.
4. Specify nonzero denominators, feasible inputs, boundary
   conditions, cardinality, missing values, quantization,
   saturation and undefined cases where they affect behavior.
   Verify that ranges and normalization match code and
   experiment. Check dimensional consistency.
5. Compare against the original method/source when adapting
   an expression: preserve sign, operator, index nesting,
   powers, brackets, floor/ceiling, units and conditions.
   Do not simplify a meaningful operator because an exporter
   fails to render it.

## Source and export are different evidence

For Markdown/LaTeX-based works, preserve a stable, human-readable
source and its explicit cross-reference IDs where supported.
The chosen publisher/toolchain owns the exact reference syntax;
do not mix manual equation numbers with auto-generated ones.
An internal citation/label key is not itself a validated
bibliographic or mathematical reference.

For imported DOCX/MathType/OMML/PDF, distinguish:
- semantic transcription (correct mathematical structure),
- parse or conversion success,
- rendered result and line wrapping/number alignment,
- cross-reference and numbering correctness.

Visually compare original and independently regenerated
complex equations, especially nested fractions, aligned
multiline expressions, scripts, limits and delimiters. Where
editable mathematical output is required, check that the
export contains genuine equation objects rather than raster
facsimiles, and verify displayed numbering and line wrapping.
Matching text tokens, math-object counts, XML existence,
the source file hash or one cached preview does **not**
establish equivalent mathematical structure. Unknown
symbols or unreadable original fragments remain explicit
unresolved questions, never guessed data.

The use of Word, native math objects, MathType, KaTeX,
Pandoc or a particular GOST depends on the actual journal,
institution or tool capabilities; this Skill mandates none
as a universal dependency.

**Completion:** each mathematical expression is defined,
traceable to its derivation/input, internally consistent,
and faithful in the final required output.
