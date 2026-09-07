---
description: "Run a checker agent after creation or before publication to validate content quality."
when_to_use: "Use when deciding whether to validate content before it is published or deployed."
---

# Practice 3: Use Checkers for Validation Workflow

**Principle**: Run checkers after creation or before publication.

**Good Example:**

```markdown
1. Maker creates content
2. User reviews content
3. Checker validates quality → generates audit report
4. User reviews audit report
5. Fixer applies validated fixes (if needed)
```

**Bad Example:**

```markdown
1. Maker creates content
2. Deploy immediately (NO VALIDATION!)
```

**Rationale:**

- Catches issues before publication
- Provides audit trail
- Enables systematic quality improvement
- Validates conventions compliance
