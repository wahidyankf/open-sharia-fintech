# Fixing Software Engineering Documentation Separation Violations

Guidance for `docs-software-engineering-separation-fixer`, which applies validated fixes from
`docs-software-engineering-separation-checker` audit reports.

## Domain-Specific Confidence Examples

**HIGH** (apply automatically, all objectively verifiable): missing Prerequisites section (README
has no Prerequisites heading), wrong AyoKoding path (target path doesn't exist), broken
cross-reference link (file doesn't exist at target), missing prerequisite mapping (absent from
Software Design Reference table), missing required AyoKoding file (filesystem check).

**MEDIUM** (manual review, subjective): Prerequisites section exists but wording may be
intentionally different; AyoKoding path reference uses an alternative but valid format; content
organization or Prerequisites placement may be an intentional variation.

**FALSE_POSITIVE** (skip and report): Prerequisites section exists under a different heading format
the checker missed; AyoKoding path is correct but checker used the wrong base path; file exists but
checker checked the wrong location; prerequisite mapping exists in a different table section.

## What to Fix

**Software Design Reference updates**: add missing prerequisite mappings to the table, correct
wrong paths, fix table formatting. HIGH confidence when the mapping is simply absent; MEDIUM when
table structure differs from convention or it's uncertain whether a new relationship should be
added.

**Prerequisites section additions**: add the missing section to `docs/explanation` READMEs using
the standard template from this skill's SKILL.md, update wrong AyoKoding path references, fix
formatting. HIGH confidence for a clean addition; MEDIUM when the section exists with different
wording, placement is ambiguous, or multiple AyoKoding paths could be referenced.

**Cross-reference link fixes**: update broken/incorrect links to the correct AyoKoding path. HIGH
confidence for a clear fix; MEDIUM when link text could be improved (subjective), multiple valid
targets exist, or absolute-vs-relative path choice is ambiguous.

**AyoKoding content structure — outside this fixer's scope**: if the checker reports missing
AyoKoding files/directories, do NOT create the content — log the finding, skip the fix, and
recommend `apps-ayokoding-www-general-maker` or the relevant domain maker. Content creation needs
specialized domain conventions (annotation density, production patterns) this fixer doesn't own.

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
