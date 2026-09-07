---
description: "Checkers should categorize findings by criticality (CRITICAL/HIGH/MEDIUM/LOW) to prioritize fixes."
when_to_use: "Use when designing a checker's audit report format or prioritizing which findings to fix first."
---

# Practice 8: Use Criticality Levels for Prioritization

**Principle**: Checkers categorize findings by criticality (CRITICAL/HIGH/MEDIUM/LOW).

**Good Example:**

```markdown
# CRITICAL Issues (2)

- [ ] Broken authentication endpoint
- [ ] SQL injection vulnerability

# HIGH Issues (5)

- [ ] Missing alt text on images
- [ ] Incorrect frontmatter dates
```

**Bad Example:**

```markdown
# Issues (7)

- Broken authentication endpoint
- Missing alt text on images
- Typo in paragraph
  (All treated equally - no prioritization!)
```

**Rationale:**

- Clear prioritization of fixes
- Critical issues fixed first
- Efficient resource allocation
- Aligns with fix priority matrix
