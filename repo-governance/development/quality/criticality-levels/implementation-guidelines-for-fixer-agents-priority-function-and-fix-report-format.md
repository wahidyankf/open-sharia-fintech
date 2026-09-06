---
title: "Fixer Guidelines: Priority Function and Fix Report Format"
description: "Priority-determination function and a fix-report example."
category: explanation
subcategory: development
tags:
  - criticality
  - validation
  - checker-agents
  - fixer-agents
  - quality-assurance
created: 2025-12-27
when_to_use: "Use for priority determination or a fix-report template."
---

# Implementation Guidelines for Fixer Agents: Priority Function and Fix Report Format

## Priority Determination Function

```python
def determine_priority(criticality, confidence):
    """Determine priority based on criticality × confidence matrix."""

    priority_matrix = {
        ("CRITICAL", "HIGH"): "P0",
        ("CRITICAL", "MEDIUM"): "P1",
        ("CRITICAL", "FALSE_POSITIVE"): "REPORT",
        ("HIGH", "HIGH"): "P1",
        ("HIGH", "MEDIUM"): "P2",
        ("HIGH", "FALSE_POSITIVE"): "REPORT",
        ("MEDIUM", "HIGH"): "P2",
        ("MEDIUM", "MEDIUM"): "P3",
        ("MEDIUM", "FALSE_POSITIVE"): "REPORT",
        ("LOW", "HIGH"): "P3",
        ("LOW", "MEDIUM"): "P4",
        ("LOW", "FALSE_POSITIVE"): "REPORT",
    }

    return priority_matrix.get((criticality, confidence), "P4")
```

## Fix Report Format Updates

**Fixer agents should group fixes by priority in their reports**:

````markdown
# Repository Governance Fix Report

**Source Audit**: repo-rules**a1b2c3**2025-12-27--10-30\_\_audit.md
**Fix Date**: 2025-12-27T11:15:00+07:00
**Fixer Version**: rules-fixer v2.0

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

### 1. Missing Required Subcategory Field

**File**: `repo-governance/development/agents/ai-agents.md`
**Original Issue**: CRITICAL - Missing `subcategory: development` field
**Validation**: Confirmed field missing in frontmatter (HIGH confidence)
**Fix Applied**: Added `subcategory: development` at line 5

**Before**:

```yaml
---
name: AI Agents Convention
category: development
---
```
````

**After**:

```yaml
---
name: AI Agents Convention
category: development
subcategory: development
---
```

[... continue for all P0 fixes ...]

---
