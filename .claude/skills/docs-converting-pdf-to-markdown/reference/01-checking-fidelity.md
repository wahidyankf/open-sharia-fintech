# Checking PDF-to-Markdown Fidelity

Validate a Markdown file against its source PDF across seven dimensions: text completeness, text
accuracy, heading level accuracy, content nesting accuracy, structural fidelity, figure coverage,
and technical validity (Mermaid syntax, OCR quality).

## Criticality Levels

| Finding                                                    | Criticality |
| ---------------------------------------------------------- | ----------- |
| Missing entire section or page                             | CRITICAL    |
| Text altered to change meaning                             | CRITICAL    |
| Missing table (entirely absent)                            | CRITICAL    |
| OCR text gibberish (>10% error rate)                       | CRITICAL    |
| Missing paragraph within section                           | HIGH        |
| Wrong table data (cell values incorrect)                   | HIGH        |
| Missing footnote or reference                              | HIGH        |
| Invalid Mermaid syntax (unparseable)                       | HIGH        |
| Figure with no representation (no Mermaid, no placeholder) | HIGH        |
| Minor heading hierarchy drift                              | MEDIUM      |
| Missing page header/footer content                         | MEDIUM      |
| Sub-optimal Mermaid (valid but imprecise)                  | MEDIUM      |
| Whitespace or minor punctuation difference                 | LOW         |
| OCR confidence tags missing                                | LOW         |

## Validation Workflow

**Step 0 — Initialize report**: `crane report --init "$PDF_FILE" --md "$MD_FILE" --scope pdf-to-md`
creates a UUID-chained, UTC+7-timestamped report at
`generated-reports/pdf-to-md__{uuid-chain}__{timestamp}__audit.md`.

**Step 1 — Pre-flight**: verify both files exist and the MD file is non-empty; get page count via
`crane pdf --info "$PDF_FILE"`.

**Step 2 — Text completeness (preferred single-pass)**: `crane check-all "$PDF_FILE" "$MD_FILE"`
runs all six core dimensions (text, heading, nesting, table, figure, mermaid) with one shared PDF
extraction; add `--cache-dir "$CACHE_DIR"` on repeat runs against the same PDF. Each finding's
`category` field carries its dimension label. **Fallback (per-dimension)**: `crane text --check
"$PDF_FILE" "$MD_FILE"` when investigating a single failure. **Large-PDF timeout protocol**: `crane
check-all` may exceed practical completion time above ~200 pages (text-completeness dominates cost)
— on timeout or empty output, fall back to per-dimension subcommands, and if a dimension was sampled
rather than exhausted, disclose the sampling scope in the report's `## Workflow Deviations` footer.
Criticality: CRITICAL for missing headings/section starts, HIGH for paragraphs, MEDIUM for short
phrases.

**Step 3 — Heading level accuracy**: `crane heading --check "$PDF_FILE" "$MD_FILE"`. HIGH when off
by 2+ levels or an entire family is wrong; MEDIUM for a single isolated heading off by 1 level;
HIGH_CONFIDENCE when section numbering gives unambiguous evidence.

**Step 4 — Content nesting accuracy**: `crane nesting --check "$PDF_FILE" "$MD_FILE"`. HIGH when
nesting hierarchy is inverted; MEDIUM when off by one level.

**Step 5 — Table integrity**: `crane table --check "$PDF_FILE" "$MD_FILE"` — count rows/columns in
the PDF source, find the corresponding MD table by header-row keywords, verify row/column counts,
spot-check 3-5 cell values. Missing table entirely → CRITICAL; wrong cell data → HIGH.

**Step 6 — Figure/diagram coverage**: `crane figure --check "$PDF_FILE" "$MD_FILE"`. No
representation (no Mermaid, no placeholder) → HIGH; placeholder-only when type was determinable →
MEDIUM.

**Step 7 — Mermaid syntax validation**: `crane mermaid --validate "$MD_FILE"` — validates 18 known
diagram type keywords, balanced brackets/parentheses, non-empty blocks. Invalid block → HIGH.

**Step 8 — OCR quality** (if applicable): `crane ocr --quality "$MD_FILE"` on `<!-- OCR: ... -->`
tagged sections, using 4 error patterns (non-ASCII runs, repeated l/I/1, repeated 0/O, long
concatenated words). Error rate >10% → CRITICAL, 5-10% → HIGH, 2-5% → MEDIUM.

**Step 9 — Structural integrity**: MD starts with an H1; major PDF sections present as headings;
section ordering matches PDF reading order; no content before the H1. Inverted order → HIGH; missing
H1 → MEDIUM.

**Step 10 — Finalize**: update status "In Progress" → "Complete"; add a summary (pages checked,
findings by criticality, dimensions checked, pass/needs-fixes recommendation).

## Report Format

```markdown
# PDF-to-Markdown Fidelity Audit

**Date**: YYYY-MM-DD HH:MM (UTC+7)
**Checker**: pdf-to-md-checker
**PDF**: path/to/source.pdf (N pages)
**Markdown**: path/to/source.md
**UUID Chain**: {uuid-chain}

## Summary

- **Pages Checked**: N
- **Text Segments Verified**: X
- **Tables Verified**: Y
- **Figures Checked**: Z
- **CRITICAL/HIGH/MEDIUM/LOW Findings**: A/B/C/D
- **Overall Status**: PASS / NEEDS FIXES

## CRITICAL Findings

### CRITICAL: Missing Section — "Section Title"

**Location in PDF**: Page N, section heading
**Location in MD**: Not found
**PDF Text**: "[first 50 chars of section...]"
**Issue**: Entire section absent from Markdown

## HIGH Findings

### HIGH: Invalid Mermaid Block

**Location in MD**: `source.md:line_N`
**Issue**: Block starts with unknown diagram type `xyz`
**Fix**: Replace `xyz` with valid type (e.g., `graph TD`)

## Verified (sample)

- Pages 1-10: Full text match confirmed
- Table on page 12: 4 columns, 8 rows verified
- Figure 1 placeholder present
```
