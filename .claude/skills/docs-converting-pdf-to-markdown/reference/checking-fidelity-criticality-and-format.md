# Checking PDF-to-Markdown Fidelity: Criticality Levels and Report Format

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
