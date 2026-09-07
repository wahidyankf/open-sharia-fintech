---
description: "Use the fixer's false positive reports to improve checker accuracy over time."
when_to_use: "Use when a fixer detects a false positive and needs to feed that signal back into checker logic."
---

# Practice 9: Iterative Improvement via False Positive Feedback

**Principle**: Use fixer's false positive reports to improve checkers.

**Good Example:**

```markdown
# Workflow

1. Checker flags issue
2. Fixer re-validates → detects FALSE_POSITIVE
3. Fixer reports false positive with improvement suggestion
4. User updates checker logic
5. Next run: improved accuracy
```

**Bad Example:**

```markdown
# Ignore false positives (DO NOT DO THIS)

1. Checker flags issue
2. Fixer detects false positive
3. Skip fix, move on
4. No feedback to checker
5. Same false positive next run
```

**Rationale:**

- Continuous improvement cycle
- Checkers become more accurate over time
- Reduces false positive rate
- Systematic quality enhancement
