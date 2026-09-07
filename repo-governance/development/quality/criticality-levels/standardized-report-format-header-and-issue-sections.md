---
description: "The report header and issue-section template."
when_to_use: "Use when authoring a report header or issue section."
---

# Standardized Report Format: Header and Issue Sections

## Standardized Report Format

All checker agents must generate reports following this template.

### Report Header

```markdown
# [Agent Name] Audit Report

**Audit ID**: {uuid-chain}\_\_{timestamp}
**Scope**: {scope-description}
**Files Checked**: N files
**Audit Start**: YYYY-MM-DDTHH:MM:SS+07:00
**Audit End**: YYYY-MM-DDTHH:MM:SS+07:00
**Duration**: Mm Ss

---

## Executive Summary

- **CRITICAL Issues**: X (must fix before publication)
- **HIGH Issues**: Y (should fix before publication)
- **MEDIUM Issues**: Z (improve when time permits)
- **LOW Issues**: W (optional enhancements)

**Total Issues**: X + Y + Z + W = TOTAL

**Overall Status**: [PASS | PASS WITH WARNINGS | FAIL]

**Status Determination**:

- PASS: Zero CRITICAL and HIGH issues
- PASS WITH WARNINGS: Zero CRITICAL, some HIGH/MEDIUM/LOW issues
- FAIL: One or more CRITICAL issues present

---
```

### Issue Sections

Each criticality level has its own section with consistent formatting:

````markdown
## CRITICAL Issues (Must Fix)

**Count**: X issues found

---

### 1. [Issue Title - Brief Description]

**File**: `path/to/file.md:line`
**Criticality**: CRITICAL - [One-line justification why critical]
**Category**: [Missing Required Field | Broken Link | Syntax Error | Security Vulnerability | etc.]

**Finding**:
[Clear, specific description of what's wrong]

**Impact**:
[What breaks or fails if not fixed - user/system consequences]

**Recommendation**:
[Specific, actionable fix - exact change needed]

**Example**:

```yaml
# Current (broken)
---
title: "Example"
# Missing required 'draft' field
---
# Expected (fixed)
---
title: "Example"
draft: false
---
```
````

**Confidence**: HIGH
[If confidence differs from HIGH, explain assessment]

---
