# Making PDF-to-Markdown Conversions

Workflow for `pdf-to-md-maker`: produce a complete, verbatim Markdown representation of a PDF —
every word, table, figure, footnote, and structural element faithfully represented, with no
sections omitted and no text fabricated.

## Step 1: Detect PDF Type

```bash
PDF_TYPE=$(crane pdf --type "$PDF_FILE" | jq -r .type)
```

`"text"` (exit 0) → text-based PDF, proceed with crane extraction. `"image"` (exit 1) → image-only
PDF, use the OCR path. If `crane` not found: prefix with `cargo run --manifest-path
apps/crane-cli/Cargo.toml --`.

## Step 2a: Text-Based PDF Extraction

Process in chunks (default 50 pages) to handle arbitrarily large PDFs:

```bash
TOTAL_PAGES=$(crane pdf --info "$PDF_FILE" | jq .pages)
CHUNK_SIZE=50
CHUNKS=$(( (TOTAL_PAGES + CHUNK_SIZE - 1) / CHUNK_SIZE ))
for i in $(seq 0 $((CHUNKS - 1))); do
  FIRST=$(( i * CHUNK_SIZE + 1 )); LAST=$(( (i + 1) * CHUNK_SIZE ))
  [ $LAST -gt $TOTAL_PAGES ] && LAST=$TOTAL_PAGES
  crane pdf --extract "$PDF_FILE" --start-page $FIRST --end-page $LAST > "/tmp/chunk_${i}.txt"
done
```

Read each chunk file and process text into Markdown.

## Step 2b: Image-Only PDF (OCR Path)

```bash
command -v tesseract >/dev/null 2>&1 || { echo "[REQUIRES TESSERACT] Install tesseract-ocr"; exit 1; }
TOTAL_PAGES=$(crane pdf --info "$PDF_FILE" | jq .pages)
for PAGE in $(seq 1 $TOTAL_PAGES); do
  pdftoppm -f $PAGE -l $PAGE -r 300 "$PDF_FILE" /tmp/pdf_page
  tesseract /tmp/pdf_page-1.ppm /tmp/ocr_page_$PAGE -l eng 2>/dev/null
done
```

Tag each OCR-extracted page with `<!-- OCR: page N -->`.

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
