---
description: Why per-harness upstream research is delegated to web-researcher sub-tasks rather than performed inline, keeping the audit context lean.
when_to_use: Use when understanding how the checker gathers current upstream harness conventions.
---

# Research Delegation

The checker delegates **multi-page per-harness research** to `web-researcher` rather
than performing web lookups inline. This keeps the audit context lean and lets the checker
focus on diffing and reporting.

For each supported harness, the checker spawns a `web-researcher` sub-task that:

- Fetches current authoritative upstream documentation (official docs site, changelog,
  migration guides)
- Extracts the harness's current configuration conventions (frontmatter schema, file
  locations, model identifier format, permission schema, tool declarations)
- Returns a structured summary that the checker compares against the local catalog entry
  and committed binding files

The checker cites the upstream source URL and retrieval date in the audit report so reviewers
can verify research independently.
