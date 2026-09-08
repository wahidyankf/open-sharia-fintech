---
description: "Step 7: reports the final status (pass/partial/fail), iteration count, and summary report."
when_to_use: "Use when implementing or debugging the workflow's final reporting step."
---

# 7. Finalization (Sequential)

Report final status and summary.

**Output**: `{final-status}`, `{lifecycle-status}`, `{iterations-completed}`, `{pdf-to-md-report}`

Derive `lifecycle-status` separately from the latest lifecycle evidence (`verified`, `pending`, or
`not-applicable`). It never changes domain `final-status`.

**Status determination**:

- **pass**: Zero threshold-level findings across all dimensions on 2 consecutive checks
- **partial**: Findings remain after max-iterations; or some fixes require manual intervention
  (e.g., OCR quality disputes)
- **fail**: Technical errors (missing tools, corrupt PDF, empty output)

**Notes**:

- Below-threshold findings reported in final audit but don't prevent success
- Manual intervention cases (e.g., true OCR quality issues) always result in `partial` — re-run
  after manual correction
- Final report includes page coverage, table count, figure count, Mermaid block count
