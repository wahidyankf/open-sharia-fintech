---
description: "Step 1: conditionally invokes pdf-to-md-maker to convert the source PDF to Markdown when no Markdown file exists yet or force-remake is set."
when_to_use: "Use when implementing or debugging the conditional Markdown-generation step of the quality gate."
---

# 1. Generate Markdown (Conditional)

Convert the PDF to Markdown. Skipped if MD file already exists AND `force-remake=false`.

**Condition**: Run if `md-file` does not exist OR `force-remake=true`

**Agent**: `pdf-to-md-maker`

- **Args**: `pdf-file: {input.pdf-file}, md-file: {input.md-file}`
- **Output**: Markdown file at `{input.md-file}` (or derived default path)

**Success criteria**: Maker completes without error; MD file exists and is non-empty.

**On failure**: Terminate workflow with status `fail`. Common failure causes:

- `pdftotext` (poppler-utils) not installed
- `tesseract` not installed for image-only PDFs
- Source PDF is corrupt or unreadable

**Notes**:

- Text-based PDFs: uses `pdftotext -layout` in 50-page chunks
- Image-only PDFs: uses `pdfimages` + `tesseract` OCR per page; OCR pages tagged `<!-- OCR: page N -->`
- Diagrams/figures: converted to Mermaid stubs or `[FIGURE N: ...]` placeholders
- Default output path: same directory and filename as PDF, `.md` extension
- **Directory creation**: if `md-file` parent directory does not exist, maker runs `mkdir -p`
  before writing — applies to custom output paths; the default path (same dir as PDF) always
  exists and is a no-op
- **Heading level inference**: maker uses `pdftotext -layout` font-size heuristics and section
  numbering depth (e.g. `1.2.3` = H3) to assign the correct `#` depth — title = H1, top-level
  chapters/parts = H2, sections = H3, subsections = H4, sub-subsections = H5
- **Content nesting inference**: list indentation depth from PDF layout output is preserved;
  nested bullets and numbered lists carry the correct nesting level into Markdown
