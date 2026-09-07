---
description: "A maker agent is used to apply fixes from an audit report, when a validation-driven fixer is the correct tool."
when_to_use: "Use when deciding whether to invoke a maker or a fixer to address audit-report findings."
---

# Anti-Pattern 10: Using Maker Instead of Fixer

**Problem**: Using maker for validation-driven fixes.

**Bad Example:**

```markdown
User: "Fix issues from the latest audit report"
→ Use docs-maker (WRONG - maker is for user-driven creation!)
```

**Solution:**

```markdown
User: "Fix issues from the latest audit report"
→ Use docs-fixer (CORRECT - fixer is validation-driven)
```

**Rationale:**

- Clear workflow boundaries
- Makers handle comprehensive creation
- Fixers handle validated remediation
- Prevents tool misuse
