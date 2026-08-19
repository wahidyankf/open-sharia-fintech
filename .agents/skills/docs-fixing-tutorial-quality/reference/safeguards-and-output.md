# Safeguards and Output Format

## Important Notes

1. Re-validation is mandatory — NEVER skip the validation step
2. Confidence matters — apply fixes only when confidence is HIGH
3. Subjectivity awareness — flag subjective quality assessments for manual review
4. Report everything — document all decisions (fixed/skipped/flagged)
5. Improve checker — provide actionable feedback on false positives
6. Audit trail — always generate a fix report for transparency

## When to Refuse

Refuse to:

- Apply fixes without re-validation
- Modify files without HIGH confidence
- Apply subjective quality improvements automatically
- Skip reporting false positives
- Proceed without a readable audit report

## Your Output

Always provide:

1. **Fix summary** — what was fixed, skipped, flagged
2. **False positive report** — detailed analysis of checker errors
3. **Manual review list** — subjective items needing human judgment
4. **Recommendations** — how to improve `docs-tutorial-checker`
5. **Fix report file** — complete audit trail in `generated-reports/`

## Convergence Safeguards

See `repo-applying-maker-checker-fixer` Skill for:

- **Capture Changed Files**: after applying all fixes, capture the changed-files list for scoped
  re-validation
- **Persist FALSE_POSITIVE Findings**: append each FALSE_POSITIVE to
  `generated-reports/.known-false-positives.md`
- **Self-Verification After Edits**: re-read modified sections and log APPLIED/FAILED status in
  the fix report
