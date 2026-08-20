# Making PDF-to-Markdown Conversions: Detection and Extraction

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
