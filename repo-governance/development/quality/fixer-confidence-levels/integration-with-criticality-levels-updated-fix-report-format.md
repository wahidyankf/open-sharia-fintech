---
description: "The updated fix-report format and why priority-based execution matters."
when_to_use: "Use when authoring a fix report with priority-based sections."
---

# Integration with Criticality Levels: Updated Fix Report Format

## Updated Fix Report Format

Fix reports should now group fixes by priority to show criticality context:

```markdown
# Repository Governance Fix Report

**Source Audit**: repo-rules**a1b2c3**2025-12-27--10-30\_\_audit.md
**Fix Date**: 2025-12-27T11:15:00+07:00

---

## Execution Summary

- **P0 Fixes Applied**: 5 (CRITICAL + HIGH confidence)
- **P1 Fixes Applied**: 12 (HIGH + HIGH confidence)
- **P1 Flagged for Urgent Review**: 2 (CRITICAL + MEDIUM confidence)
- **P2 Fixes Applied**: 8 (MEDIUM + HIGH confidence, batch mode)
- **P2 Flagged for Standard Review**: 3 (HIGH + MEDIUM confidence)
- **P3-P4 Suggestions**: 15 (LOW priority, no action)
- **False Positives Detected**: 3

---

## P0 Fixes Applied (CRITICAL + HIGH Confidence)

### 1. Missing Required `when_to_use` Field

**File**: `repo-governance/development/agents/ai-agents.md`
**Criticality**: CRITICAL - Breaks routing and validation
**Confidence**: HIGH - Confirmed field missing in frontmatter
**Fix Applied**: Added `when_to_use` at line 3

[... more P0 fixes ...]

---

## P1 Fixes Applied (HIGH + HIGH Confidence)

[Same format showing HIGH criticality + HIGH confidence fixes]

---

## P1 Flagged for Urgent Review (CRITICAL + MEDIUM Confidence)

### 1. Ambiguous Link Target

**File**: `repo-governance/conventions/formatting/linking.md:89`
**Criticality**: CRITICAL - Broken link to convention doc
**Confidence**: MEDIUM - Multiple possible target files found
**Reason for Flag**: Cannot determine correct link target automatically
**Action Required**: Manually select correct target from candidates

---

## P2 Fixes Applied (MEDIUM + HIGH Confidence)

[Medium criticality issues with high confidence fixes]

---

## P3-P4 Suggestions (No Action Taken)

**Total**: 15 findings

[List of LOW criticality suggestions]

---

## False Positives Detected

[Grouped by criticality for context on checker improvement urgency]
```

## Why Priority-Based Execution Matters

**Before criticality integration**:

```
Fixer applies all HIGH confidence fixes in discovery order:
  1. Fix LOW priority style issue
  2. Fix MEDIUM priority format issue
  3. Fix CRITICAL build-breaking issue ← Should be first!
```

**After criticality integration**:

```
Fixer applies fixes in priority order:
  1. Fix CRITICAL build-breaking issue (P0)
  2. Fix HIGH priority issues (P1)
  3. Fix MEDIUM priority issues (P2)
  4. LOW priority suggestions last (P3-P4)
```

**Benefits**:

- CRITICAL issues fixed before deployment proceeds
- Clear prioritization aligns with user urgency
- Manual review items properly flagged by importance
- Low priority suggestions don't clutter urgent work
