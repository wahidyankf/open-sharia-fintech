# Making PDF-to-Markdown Conversions: Assembly, Output, and Invariants

## Step 3: Convert Each Chunk to Markdown

**Headings** — infer `#` depth: primary method is section-numbering depth (no number/document
title → H1; `1.`/`A.` → H2; `1.1` → H3; `1.1.1` → H4; `1.1.1.1`+ → H5). Fallback: font-size
heuristic when numbering is absent (larger/bolder lines get shallower depths). Never assign the
same depth to two structurally distinct heading levels.

**Tables** — detect grid structures (rows of aligned whitespace-separated columns), convert to
standard Markdown table syntax.

**Figures and Diagrams** — on `Figure N`, `Diagram`, `Chart`, or whitespace-heavy non-table
structured content: attempt to describe from surrounding labels/captions, generate a Mermaid stub
if the type is identifiable (flowcharts → `graph TD`, sequence → `sequenceDiagram`, state →
`stateDiagram-v2`, class/entity → `classDiagram`) with the caption as a blockquote below it; if the
type can't be determined, use `[FIGURE N: description from caption — diagram type could not be
determined]`.

**Lists** — detect bulleted (`•`/`-`/`*`) and numbered items; use column offset from `pdftotext
-layout` to determine nesting level (each indent level = 2 spaces before `-`, 3 spaces before
`1.`); preserve multi-level lists as genuinely nested, never flattened.

**Footnotes** — preserve as numbered references at section bottom: `[^N]: footnote text`.

**Headers/Footers** — include only if they carry meaningful content (chapter/section names); skip
decorative page numbers.

## Step 4: Assemble Full Markdown

Concatenate all processed chunks in order. Add YAML front matter only if the PDF has clear
title/metadata. Do NOT add any content not present in the source PDF.

## Step 5: Write Output File

Default output: `${PDF_FILE%.pdf}.md` (same dir/name, `.md` extension). `mkdir -p` the parent
directory before writing (no-op for the default path; needed for custom `md-file` paths).
Overwrite if the file already exists.

## Key Invariants

Never omit text (every PDF word must appear); never fabricate text; every figure has a Mermaid
diagram or `[FIGURE N: ...]` placeholder; OCR pages are tagged so the checker applies appropriate
tolerance; chunk boundaries are invisible in the final file; "verbatim" allows whitespace
normalization but never word changes.

## Graceful Degradation

| Tool Missing                      | Behavior                                                                                  |
| --------------------------------- | ----------------------------------------------------------------------------------------- |
| `crane` not found                 | Prefix with `cargo run --manifest-path apps/crane-cli/Cargo.toml --`                      |
| `tesseract` not found (image PDF) | Fail: `ERROR: tesseract required for image-only PDFs. Install: brew install tesseract`    |
| `jq` not found                    | Parse JSON manually; `crane pdf --info` returns `{"pages":N,...}` — extract with grep/cut |
| `pdftoppm` not found              | Try `convert` (ImageMagick) as fallback for image extraction                              |
