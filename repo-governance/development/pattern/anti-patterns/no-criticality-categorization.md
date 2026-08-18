---
title: "Anti-Pattern 8: No Criticality Categorization"
description: "Checker findings are listed as a flat, unprioritized list instead of being grouped by criticality."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when reviewing an audit report that treats all issues as equally important."
---

# Anti-Pattern 8: No Criticality Categorization

**Problem**: Treating all issues as equally important.

**Bad Example:**

```markdown
# Issues (15)

- Broken authentication endpoint
- Missing alt text
- Typo in paragraph
- SQL injection vulnerability
- Extra whitespace
  (All treated equally - no prioritization!)
```

**Solution:**

```markdown
# CRITICAL Issues (2)

- Broken authentication endpoint
- SQL injection vulnerability

# HIGH Issues (4)

- Missing alt text on images

# MEDIUM Issues (6)

- Typo in paragraph

# LOW Issues (3)

- Extra whitespace
```

**Rationale:**

- Clear prioritization
- Critical issues fixed first
- Efficient resource allocation
- Aligns with fix priority matrix
