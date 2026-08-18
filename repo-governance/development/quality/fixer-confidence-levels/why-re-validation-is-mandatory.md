---
title: "Why Re-Validation Is Mandatory"
description: "Why fixers must re-validate before applying a fix."
category: explanation
subcategory: development
tags:
  - fixer-agents
  - confidence-levels
  - validation
  - automation
  - quality-assurance
created: 2025-12-14
when_to_use: "Use when tempted to apply a checker finding without re-validating."
---

# Why Re-Validation is Mandatory

## Never Trust Checker Findings Blindly

**CRITICAL PRINCIPLE:** Fixer agents MUST re-validate all findings before applying fixes.

**Why:**

1. **Checkers can be wrong** - Detection logic may have bugs or edge cases
2. **Context changes** - File may have been modified between checker run and fixer run
3. **Ambiguity exists** - What looks like violation may be valid in specific context
4. **Confidence assessment requires verification** - Can't assess confidence without re-checking

**Process:**

```
Checker Report → Read Finding → Re-execute Validation → Assess Confidence → Apply/Skip/Report
```

**Re-validation methods:**

- Extract frontmatter using same AWK pattern as checker
- Check file existence for broken links
- Count objective metrics (paragraph lines, H1 headings)
- Verify patterns match (date format, naming convention)
- Analyze context (content type, directory, file purpose)

**See:** [Repository Validation Methodology Convention](.././repository-validation.md) for standard re-validation patterns.
