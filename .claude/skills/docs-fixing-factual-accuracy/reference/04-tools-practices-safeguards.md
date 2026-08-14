# Tools Usage, Best Practices, and Convergence Safeguards

## Tools Usage

- **Read**: Read audit reports and documentation files
- **Edit**: Apply fixes to documentation files
- **Glob**: Find files referenced in audit report
- **Grep**: Extract specific content for validation
- **Write**: Generate fix report in generated-reports/
- **Bash**: Get timestamps, UUID chains, file operations

## Best Practices

1. **Always re-validate** - Never trust checker blindly
2. **Be conservative** - When in doubt, classify as MEDIUM (manual review)
3. **Document reasoning** - Explain confidence assessments clearly
4. **Report false positives** - Help improve checker accuracy
5. **Preserve context** - Don't break documentation flow with fixes
6. **Test fixes mentally** - Ensure fix makes sense in context
7. **Track all actions** - Comprehensive fix report for audit trail

## Convergence Safeguards

See `repo-applying-maker-checker-fixer` Skill for:

- **Capture Changed Files**: After applying all fixes, capture changed files list for scoped
  re-validation
- **Persist FALSE_POSITIVE Findings**: Append each FALSE_POSITIVE to
  `generated-reports/.known-false-positives.md`
- **Self-Verification After Edits**: Re-read modified sections and log APPLIED/FAILED status in fix
  report
