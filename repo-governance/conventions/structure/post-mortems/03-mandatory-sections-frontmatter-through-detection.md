---
title: "Post-Mortem Convention: Mandatory Sections — Frontmatter Through Detection"
description: The required Frontmatter, Metadata Table, Summary, Impact, and Detection sections of a post-mortem document, in reading order
when_to_use: Read this when authoring the opening mandatory sections of a post-mortem, from frontmatter through how the incident was detected.
category: explanation
subcategory: conventions
tags:
  - post-mortem
  - incidents
  - blameless
  - reliability
  - structure
created: 2026-06-05
---

# Mandatory Sections: Frontmatter Through Detection

Every post-mortem MUST contain the following sections in this order.

## 1. Frontmatter

```yaml
---
title: "Post-Mortem: <System> — <Short Failure>"
description: One-sentence summary of the incident
category: explanation
subcategory: post-mortem
tags:
  - post-mortem
  - <system>
  - <relevant-tag>
doc_status: draft
---
```

`doc_status` values:

- `draft` — initial write-up, may have gaps
- `reviewed` — factual accuracy confirmed by at least one other perspective (second reading,
  peer review, or log cross-check)
- `closed` — all P0 action items resolved; document is the settled record

`doc_status` is the **document status**, distinct from the incident `Status` field in the
metadata table below.

## 2. Metadata Table

Immediately after the H1, before any prose:

```markdown
| Field              | Value                                             |
| ------------------ | ------------------------------------------------- |
| Incident date      | YYYY-MM-DD                                        |
| Investigation date | YYYY-MM-DD                                        |
| Severity           | Sev-N — label (see severity scale)                |
| Status             | Investigating / Resolved                          |
| Author             | Role or initials (not full name unless preferred) |
```

## 3. Summary

Two to four sentences. State what failed, how long it lasted, and the outcome. Write it last but
place it first — it is the executive snapshot.

## 4. Impact

Quantify impact wherever possible. Include:

- Services or users affected
- Duration
- MTTD (Mean Time to Detect) and MTTR (Mean Time to Resolve) — use `unknown — no alerting` if
  detection was manual and latency is not measurable

## 5. Detection

How the incident was discovered. Append one of the following category labels in parentheses:

- **Manual** — a person noticed through inspection or a failed task
- **Monitoring Alert** — an automated alerting rule fired (e.g., Vercel uptime alert, GitHub
  Actions failure notification)
- **Automated Health Check** — a health-check endpoint or CI watchdog detected failure
- **User Report** — an end-user or external party reported the problem

Example: `"A contributor noticed the pre-push hook was rejecting clean commits on all affected
branches. (Manual)"`
