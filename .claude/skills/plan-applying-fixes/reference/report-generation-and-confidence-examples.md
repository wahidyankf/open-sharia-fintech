# Fix Report Generation, Re-validation Bookkeeping, and Confidence Examples

## Fix Report Generation

Use `repo-generating-validation-reports` Skill for comprehensive fix report generation.

## Capture Changed Files for Scoped Re-validation

After applying all fixes, capture the changed files list (`git diff --name-only HEAD`) under
`## Changed Files (for Scoped Re-validation)`:

```markdown
## Changed Files (for Scoped Re-validation)

The following files were modified. The next checker run uses this list to enable scoped re-validation:

- path/to/modified-file-1.md
- path/to/modified-file-2.md
```

## Persist FALSE_POSITIVE Findings

After every fix run, append each FALSE_POSITIVE to `local-tmp/.known-false-positives.md`:

```bash
cat >> local-tmp/.known-false-positives.md << 'EOF'
## FALSE_POSITIVE: [category] | [file] | [brief-description]

**Accepted**: [YYYY-MM-DD--HH-MM]
**Category**: [finding category]
**File**: [path/to/file.md]
**Finding**: [Brief description]
**Reason**: [Why accepted as false positive]

---
EOF
```

Also list in the fix report under `## Accepted FALSE_POSITIVE Findings`.

## Self-Verification After Edits

After every edit (Edit tool or Bash sed/awk):

1. Re-read the modified file section to confirm the change was applied.
2. For Bash edits: `grep -q "expected-pattern" file.md || echo "WARNING: fix NOT applied"`.
3. Log as **APPLIED (verified)** or **FAILED (not applied)** in the fix report.
4. Do NOT count FAILED fixes as resolved — they will be re-flagged by the checker.

## Confidence Level Assessment

The `repo-assessing-criticality-confidence` Skill provides complete confidence-level definitions and
assessment criteria. Domain-specific examples for plan content:

**HIGH Confidence** (apply automatically): missing required section (objectives, user stories,
delivery checklist); incomplete user story (missing Given/When/Then); missing acceptance criteria;
broken internal link; invalid folder naming pattern; missing git workflow specification.

**MEDIUM Confidence** (manual review): requirements clarity (subjective); technical-documentation
completeness (context-dependent); step granularity (varies by complexity); design-decision
justification quality.

**FALSE_POSITIVE** (report to checker): checker flagged a section as missing when it exists under a
different heading; checker reported an incomplete user story that is actually complete; checker
misidentified plan structure.

## Factual Accuracy Fixes

1. WebSearch/WebFetch to verify the correct value before applying the fix.
2. Update version numbers to latest stable when the checker identifies outdated versions.
3. Fix deprecated package names with correct replacements (e.g. `@trpc/react-query` →
   `@trpc/tanstack-react-query`).
4. Correct command syntax with verified flags and options.
5. Add missing dependencies identified by the checker's compatibility analysis.

Use `docs-validating-factual-accuracy` Skill for systematic verification before applying fixes.
