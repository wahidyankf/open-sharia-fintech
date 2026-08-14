# Fixer Mechanics

Maps `specs-checker`'s nine categories (see
[01-validation-categories.md](01-validation-categories.md)) to `specs-fixer`'s fix disposition,
plus the fixer's execution pattern, report format, and safety rules.

## Fix Disposition by Category

**Fixable automatically (HIGH confidence)**: Category 1 missing README (generate from directory
contents using the standard template, for all five canonical folders and per-surface subfolders);
Category 2 README scenario/feature counts and domain listings (recount from actual `.feature`
files); Category 3 feature file naming (kebab-case via `git mv`); Category 5 C4 color palette
(replace non-standard colors with the accessible palette) and C4 README file listings; Category 6
broken cross-references (fix relative paths from actual file locations); Category 8 directory
structure violations (move feature files to correct nesting via `git mv`, per
[Specs Directory Structure Convention](../../../../repo-governance/conventions/structure/specs-directory-structure.md));
allowlist-gate findings from `nx run rhino-cli:validate:specs-counts`/`-links` (create missing
folder + `README.md` + placeholder spec; repair or remove a broken link).

**Requires Review (MEDIUM confidence)**: Category 1 missing user-story blocks (template
generatable, content needs human review); Category 4 cross-folder coverage gaps, contradictions
(needs domain decision), actor-name inconsistency (may cascade to implementations); Category 3
Background step inconsistency (may change test behavior); Category 9 adoption gaps — always
flagged and documented, **never auto-fixed**, adoption is a team decision; Category 8 tree-shape
migrations at the subtree level — flagged and documented, **never auto-fixed**, migration is a
plan-level operation requiring an atomic commit across rhino-cli path constants, Nx cache inputs,
and step definitions; drift-detection re-introduction (routes/endpoints/contracts) — flags only,
requires a new dedicated plan.

**Skip (FALSE_POSITIVE or unfixable)**: implementation alignment (Category 7 — out of scope, that
is a developer agent's job); step wording consistency (subjective); scenario count variance across
perspectives (legitimate).

## Execution Pattern

1. Read audit report — parse "Folders validated" and findings by criticality/confidence.
2. Verify scope — every fix targets only files within the validated folders.
3. Filter by mode — see `repo-applying-maker-checker-fixer` Skill for the full
   lax/normal/strict/ocd logic.
4. Sort by priority: P0 (CRITICAL/HIGH confidence) → P1 (CRITICAL/MEDIUM) → P2 (HIGH/HIGH) → etc.
5. Re-validate each finding — confirm the issue still exists before fixing.
6. Apply — Edit for markdown, `git mv` via Bash for renames,
   `nx run rhino-cli:validate:specs-{counts,links}` output for missing-folder/broken-link fixes.
7. Post-fix verify — read the modified file to confirm the fix is correct.
8. Generate the fix report.

## Fix Report Format

```markdown
# Specs Fix Report

**Source Audit**: {audit-report-path}
**Folders scoped**: {list from audit report}
**Timestamp**: YYYY-MM-DD--HH-MM UTC+7
**Mode**: {mode}

## Summary

| Action                      | Count |
| --------------------------- | ----- |
| Fixed                       | N     |
| Skipped (below threshold)   | N     |
| Skipped (MEDIUM confidence) | N     |
| Skipped (FALSE_POSITIVE)    | N     |
| Failed                      | N     |
| Requires Review             | N     |

## Changes Applied

### Fix 1: {Brief description}

**Finding**: [CRITICAL] {original finding}
**Action**: Updated scenario count in README from 76 to 78
**File**: `specs/apps/organiclever/behavior/organiclever-be/README.md`
**Verified**: Yes — count now matches actual feature files

## Requires Review

### Review 1: Adoption Gap — DDD not adopted for organiclever web

**Finding**: [MEDIUM] Category 9 — ddd/ absent for full-stack app
**Reason not auto-fixed**: BDD/DDD/Contracts adoption requires explicit team decision
**Recommended action**: Create a plan item to adopt DDD for organiclever-app-web, following
the organiclever pilot pattern
**Reference**: App README vs Specs Convention Standard 6
```

## Safety Rules

Always re-validate before applying any fix. Never modify files outside the validated folder list
from the audit report. Never delete feature files — only rename or modify content. Never modify
`.feature` scenario content — only structural fixes (file names, READMEs). Preserve git history —
use `git mv` for renames. Skip uncertain fixes — MEDIUM confidence logs and skips unless mode is
strict/ocd. FALSE_POSITIVE carry-forward maintained in
`generated-reports/.known-false-positives.md`. Adoption gaps and tree-shape migrations are never
auto-fixed regardless of mode.

## Capture Changed Files for Scoped Re-validation

After applying all fixes: `git diff --name-only HEAD`. Include in the fix report under
`## Changed Files (for Scoped Re-validation)` so the next checker run can scope to exactly what
changed.
