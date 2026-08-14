# Fixing Separation Violations — Confidence and What to Fix

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
