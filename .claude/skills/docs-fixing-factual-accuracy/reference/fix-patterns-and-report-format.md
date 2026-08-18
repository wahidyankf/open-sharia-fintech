# Fix Application Patterns and Fix Report Format

## Fix Application Patterns

### Pattern 1: Command Syntax Correction

**Finding**: Incorrect command flag
**Validation**: Checker verified correct syntax in official docs
**Confidence**: HIGH (objective error)
**Action**: Use Edit tool to replace incorrect flag with correct one

### Pattern 2: Version Number Update

**Finding**: Outdated version number
**Validation**: Checker verified latest version in registry
**Confidence**: HIGH if claim says "latest", MEDIUM otherwise
**Action**: Update version number if HIGH confidence

### Pattern 3: API Method Correction

**Finding**: Wrong or deprecated API method
**Validation**: Checker verified current API in documentation
**Confidence**: HIGH if method doesn't exist, MEDIUM if deprecated
**Action**: Replace with correct method if HIGH confidence

### Pattern 4: Internal Link Fix

**Finding**: Broken internal link
**Validation**: Check target file exists using Glob/Read
**Confidence**: HIGH (objective - file exists or doesn't)
**Action**: Update link path or create missing file reference

### Pattern 5: Mathematical Notation Fix

**Finding**: LaTeX delimiter error (single `$` on own line)
**Validation**: Pattern match against
[Mathematical Notation Convention](../../../../repo-governance/conventions/formatting/mathematical-notation.md)
**Confidence**: HIGH (objective syntax error)
**Action**: Replace single `$` on own line with `$$`

### Pattern 6: Diagram Color Accessibility Fix

**Finding**: Inaccessible color used in diagram (red, green, yellow)
**Validation**: Check against accessible palette from
[Color Accessibility Convention](../../../../repo-governance/conventions/formatting/color-accessibility.md)
**Confidence**: HIGH (objective palette violation)
**Action**: Replace with accessible color from verified palette

## Fix Report Format

```markdown
# Documentation Fix Report

**Date**: YYYY-MM-DD
**Fixer**: docs-fixer
**Source Audit**: docs**{UUID}**{TIMESTAMP}\_\_audit.md
**Mode Level**: {mode} (CRITICAL/HIGH/MEDIUM/LOW threshold)

## Validation Summary

**Mode Level**: {mode}

- **Total findings in audit**: X
- **Findings in scope**: Y (CRITICAL: A, HIGH: B, MEDIUM: C, LOW: D)
- **Findings skipped**: Z (below mode threshold)
- **Fixes applied (HIGH confidence)**: N
- **False positives detected**: M
- **Needs manual review (MEDIUM confidence)**: K

## Fixes Applied (HIGH Confidence)

### Fix 1: [Issue Title]

**File**: `path/to/file.md:line`
**Criticality**: CRITICAL/HIGH
**Confidence**: HIGH_CONFIDENCE
**Issue**: [Description]
**Fix Applied**: [What was changed]
**Verification**: [How re-validated]

## Needs Manual Review (MEDIUM Confidence)

### Finding 1: [Issue Title]

**File**: `path/to/file.md:line`
**Criticality**: MEDIUM
**Confidence**: MEDIUM_CONFIDENCE
**Issue**: [Description]
**Why Manual**: [Reason for manual review needed]
**Suggestion**: [Recommended action]

## False Positives Detected

### Finding 1: [Issue Title]

**File**: `path/to/file.md:line`
**Confidence**: FALSE_POSITIVE
**Checker Claim**: [What checker reported]
**Re-Validation Result**: [Why it's a false positive]
**Suggestion for Checker**: [How to improve detection]

## Skipped Findings (Below Mode Threshold)

**Mode Level**: {mode} (fixing {threshold} only)

**MEDIUM findings** (X skipped):

1. [File] - [Issue]

**LOW findings** (X skipped):

1. [File] - [Issue]

**Note**: Run with higher mode to fix these.

## Execution Summary

- **Start Time**: YYYY-MM-DD HH:MM:SS+07:00
- **End Time**: YYYY-MM-DD HH:MM:SS+07:00
- **Status**: Executed
- **Files Modified**: N
- **Total Changes**: M lines modified

## Next Steps

**All HIGH confidence fixes applied** - Review git diff for changes
**Manual review needed** - K findings require human judgment
**Checker improvements** - M false positives detected, suggest checker updates
```
