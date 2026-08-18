---
title: "When to Use Each Stage"
description: "Decision guidance for maker vs. fixer."
category: explanation
subcategory: development
tags:
  - maker-checker-fixer
  - workflow
  - content-quality
  - agent-patterns
  - validation
  - automation
created: 2025-12-14
when_to_use: "Use when unsure which stage applies."
---

# When to Use Each Stage

## When to Use Maker vs Fixer

**Use Maker when:**

- PASS: User explicitly requests content creation or updates
- PASS: Creating NEW content from scratch
- PASS: Making significant changes to EXISTING content
- PASS: Need comprehensive dependency management (indices, cross-refs)
- PASS: **User-driven workflow** (user says "create" or "update")

**Use Fixer when:**

- PASS: Checker has generated an audit report
- PASS: Issues are convention violations (not content gaps)
- PASS: Fixes are mechanical (field values, formatting, etc.)
- PASS: **Validation-driven workflow** (checker found issues)

**Example Distinction**:

```markdown
User: "Add a new tutorial about Docker" → Use MAKER (user-driven creation)
User: "Fix issues from the latest audit report" → Use FIXER (validation-driven fixes)
```

## When Checker is Optional vs Required

**Checker is OPTIONAL when:**

- Small, trivial updates (fixing typo, adding sentence)
- Content created by experienced maker (high confidence in quality)
- Time-sensitive changes (can validate later)

**Checker is REQUIRED when:**

- PASS: New content created from scratch
- PASS: Major refactoring or updates
- PASS: Before publishing to production
- PASS: Complex content (tutorials, Next.js web content)
- PASS: Critical files (AGENTS.md, convention docs)

**Best Practice**: When in doubt, run the checker. Validation is fast and prevents issues.

## When to Skip Fixer (Manual Fixes Preferred)

**Skip Fixer when:**

- FAIL: Issues require human judgment (narrative quality, engagement)
- FAIL: Fixes are context-dependent (different solutions for different cases)
- FAIL: Checker reports are unclear or ambiguous
- FAIL: User prefers manual control over changes

**Use Fixer when:**

- PASS: Issues are mechanical (missing fields, wrong values)
- PASS: Fixes are unambiguous (clear right answer)
- PASS: Many repetitive fixes needed (efficiency gain)
- PASS: Audit report has HIGH confidence findings

**Example**:

```markdown
# Use Fixer (mechanical fixes)

- Missing frontmatter fields → Fixer
- Wrong date format → Fixer
- Broken internal links → Fixer

# Manual fixes (human judgment required)

- Paragraph too long → Manual (needs content restructuring)
- Engaging hook missing → Manual (creative writing)
- Jargon detected → Manual (context-dependent rewording)
```
