---
title: "Anti-Pattern 7: Ignoring False Positive Feedback"
description: "Fixer-detected false positives are discarded instead of being fed back to improve the checker."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when a fixer finds a false positive and there is no mechanism to report it back to the checker."
---

# Anti-Pattern 7: Ignoring False Positive Feedback

**Problem**: Not using fixer reports to improve checkers.

**Bad Example:**

```markdown
# Workflow (missing feedback loop)

1. Checker flags issue (potential false positive)
2. Fixer detects false positive
3. Skip fix, move on
4. NO feedback to checker
5. Same false positive next run (repeated waste!)
```

**Solution:**

```markdown
# Workflow (with improvement loop)

1. Checker flags issue
2. Fixer re-validates → detects FALSE_POSITIVE
3. Fixer reports false positive with suggestion
4. User updates checker logic
5. Next run: improved accuracy
```

**Rationale:**

- Continuous improvement
- Reduces false positive rate
- Checkers become more accurate
- Systematic quality enhancement
