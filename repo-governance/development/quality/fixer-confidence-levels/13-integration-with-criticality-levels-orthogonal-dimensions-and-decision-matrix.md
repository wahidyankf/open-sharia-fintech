---
title: "Integration with Criticality Levels: Orthogonal Dimensions and Decision Matrix"
description: "Confidence vs criticality as orthogonal dimensions, plus the decision matrix."
category: explanation
subcategory: development
tags:
  - fixer-agents
  - confidence-levels
  - validation
  - automation
  - quality-assurance
created: 2025-12-14
when_to_use: "Use when combining a criticality level with a confidence level."
---

# Integration with Criticality Levels: Orthogonal Dimensions and Decision Matrix

## Confidence vs Criticality: Orthogonal Dimensions

**Confidence levels (HIGH/MEDIUM/FALSE_POSITIVE)** and **criticality levels (CRITICAL/HIGH/MEDIUM/LOW)** are orthogonal dimensions that work together to determine fix priority.

**Confidence** measures **CERTAINTY**:

- Can we confidently apply this fix?
- Is re-validation clear and unambiguous?
- Is the issue objective and verifiable?

**Criticality** measures **IMPORTANCE** (see [Criticality Levels Convention](.././criticality-levels.md)):

- How urgent is fixing this issue?
- What breaks if we don't fix it?
- What's the impact on users/system?

**Example showing both dimensions**:

```markdown
## CRITICAL Issues (Must Fix)

### 1. Missing Required Field Breaks Content Validation

**File**: `apps/ayokoding-www/content/en/programming/python/_index.md:3`
**Criticality**: CRITICAL - Breaks Next.js content validation
**Confidence**: HIGH - Field objectively missing from frontmatter

**Finding**: Required `draft` field missing from frontmatter
**Impact**: Content validation fails with "required field missing" error
**Recommendation**: Add `draft: false` to frontmatter
```

In this example:

- **Criticality = CRITICAL** → Must fix before deployment (breaks functionality)
- **Confidence = HIGH** → Fixer can apply automatically (objective, verifiable)
- **Result**: Automatic fix with P0 priority (highest urgency)

## Criticality × Confidence Decision Matrix

When processing audit reports, fixers use this matrix to determine **priority** and **action**:

| Criticality  | HIGH Confidence                                               | MEDIUM Confidence                                   | FALSE_POSITIVE                                             |
| ------------ | ------------------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------------- |
| **CRITICAL** | **P0** - Auto-fix immediately<br>Block deployment until fixed | **P1** - URGENT manual review<br>High priority flag | Report with CRITICAL context<br>Improve checker urgently   |
| **HIGH**     | **P1** - Auto-fix after P0<br>Fix before publication          | **P2** - Standard manual review<br>Normal priority  | Report with HIGH context<br>Improve checker soon           |
| **MEDIUM**   | **P2** - Auto-fix after P1<br>Requires user approval          | **P3** - Optional review<br>Low priority            | Report with MEDIUM context<br>Note for checker improvement |
| **LOW**      | **P3** - Include in batch fixes<br>User decides if/when       | **P4** - Suggestions only<br>No urgency             | Report with LOW context<br>Informational only              |

**Priority Levels**:

- **P0** (Blocker) - Must fix before any publication/deployment
- **P1** (Urgent) - Should fix before publication, can proceed with approval
- **P2** (Normal) - Fix in current cycle when convenient
- **P3** (Low) - Fix in future cycle or batch operation
- **P4** (Optional) - Suggestion only, no action required
