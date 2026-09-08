---
description: "Content is deployed without running a checker, skipping the quality gate between creation and publication."
when_to_use: "Use when a workflow proposes deploying maker output without a checker validation step."
---

# Anti-Pattern 2: Skipping Validation Workflow

**Problem**: Deploying content without running checker.

**Bad Example:**

```markdown
1. Maker creates content
2. Deploy immediately (NO VALIDATION!)
```

**Solution:**

```markdown
1. Maker creates content
2. Checker validates quality → audit report
3. Review audit report
4. Fixer applies fixes (if needed)
5. Re-check (optional)
6. Deploy
```

**Rationale:**

- Catches issues before publication
- Provides audit trail
- Systematic quality improvement
- Prevents broken production content
