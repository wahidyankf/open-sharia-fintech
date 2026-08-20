# Fixing Separation Violations — Workflow and Patterns

## Fixing Workflow

Step 0 — read the audit report, extract findings with criticality/verification labels, group by
type. Step 1 — re-validate each finding against current file state (objective issues → HIGH;
subjective → MEDIUM; resolved → FALSE_POSITIVE), writing results to the fix report progressively.
Step 2 — apply HIGH-confidence fixes in P0 (CRITICAL+HIGH) then P1 (HIGH+HIGH) order, verifying
each fix and recording it immediately. Step 3 — write MEDIUM-confidence findings as "SKIPPED -
MANUAL REVIEW REQUIRED" with reasoning and manual-fix guidance. Step 4 — write FALSE_POSITIVE
findings as "SKIPPED - FALSE POSITIVE" with the disproof reason. Step 5 — finalize: count fixes by
priority, count skips, write an executive summary.

Write results immediately after each re-validation/fix — do not buffer in memory, since context
compaction can lose buffered results during long fix runs.

## Re-Validation Patterns

**Missing Prerequisites section**: read the README, search for `## Prerequisites` or `## Before
You Begin` — not found → HIGH (confirmed); found → FALSE_POSITIVE (checker missed it).

**Wrong AyoKoding path**: read the Prerequisites section, extract the linked path, check it exists
on the filesystem — wrong/broken → HIGH; correct → FALSE_POSITIVE.

**Missing prerequisite mapping**: read the Software Design Reference, search the prerequisite table
for the mapping — not found → HIGH; found → FALSE_POSITIVE.

**Broken cross-reference link**: extract the link path from the finding, resolve to absolute, check
the target file exists — missing → HIGH; exists → FALSE_POSITIVE (checker path-resolution error).

## Default Fixing Scope

When the user doesn't specify an audit report, ask for its path and confirmation to proceed. When
provided: read the full report, re-validate all findings, apply HIGH-confidence fixes (P0-P1),
report MEDIUM-confidence and FALSE_POSITIVE findings, generate the fix report.
