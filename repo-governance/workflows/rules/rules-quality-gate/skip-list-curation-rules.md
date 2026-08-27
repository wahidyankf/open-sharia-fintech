---
title: "Skip-list Curation Rules"
description: How generated-reports/.known-false-positives.md is maintained — who owns it, when to add an entry vs. fix at source, the per-entry schema, and triage priority.
when_to_use: Use when deciding whether a preflight finding should be fixed at source or added to the skip-list.
---

# Skip-list Curation Rules

The skip-list at `generated-reports/.known-false-positives.md` filters out known intentional findings from the preflight deterministic categories.

**Who maintains it**: The repository maintainer who runs the quality gate.

**When to add vs fix**: Add a skip-list entry only when a finding is genuinely intentional — test fixtures, archived legacy content, third-party vendored content. Fix every other finding at the source.

**Per-entry schema**:

- `key`: category | path | finding signature (matches the `key` field in the preflight JSON)
- `rationale`: why this is intentional
- `date accepted`: ISO 8601 date
- `approver`: GitHub handle

**Skip-list keys must be prefix-stable**: a `path` key that embeds a leading `NN-` ordinal breaks the
moment the file is renamed under
[Ordinal Filename Prefixes](../../../conventions/structure/ordinal-filename-prefixes.md). Prefer a
key that survives renaming, and re-verify entries after any sweep.

**Per-category triage priority**:

1. CRITICAL findings first — fix or escalate, never skip
2. Traceability findings second — fix at source or skip with explicit rationale
3. Everything else last — curate by category

## Deterministic findings → skip-list pipeline

On each iteration, every preflight finding NOT already in `generated-reports/.known-false-positives.md` lands in the audit's `## Deterministic Findings (rhino-cli preflight)` section. The maintainer reviews each entry between workflow runs and either (a) fixes the underlying issue (one-time, removes the finding for future runs) OR (b) appends an explicit skip-list entry with rationale + date + approver. Findings never auto-migrate to the skip-list — every entry requires explicit operator approval.
