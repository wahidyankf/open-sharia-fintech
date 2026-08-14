---
title: "Anti-Pattern 10: Enumeration-Based Guards (Denylist Guards That Fail Open)"
description: "Describes the enumeration-based (denylist) guard anti-pattern, where a guard silently fails open on an unenumerated input."
category: explanation
subcategory: development
tags:
  - ai-agents
  - anti-patterns
  - development
  - best-practices
created: 2025-11-23
when_to_use: Use when reviewing a guard, validator, or permission check that enumerates disallowed values instead of allowed ones.
---

# Anti-Pattern 10: Enumeration-Based Guards (Denylist Guards That Fail Open)

**Problem**: A safety guard is written as a list of the specific cases it forbids, and is placed in
a section the agent only reaches once it already suspects the hazard. Every axis the guard does not
enumerate is silently permitted, and the guard never fires for an agent that never got to that
section. Each time a hole is discovered, another enumerated clause is appended — and the next
unnamed axis is still open.

**Bad Example** (five consecutive guards, each correct on its own axis, each leaving another open):

```markdown
## Confidence Assessment

...

### Recipe: applying a finding

- Never auto-apply a fix to a step tagged `[HUMAN]`. <!-- axis: tag value -->
- Never DELETE a merge step, only rewrite it. <!-- axis: verb -->
- Never touch merge steps in `*-to-pr` mode. <!-- axis: delivery mode -->
- Never auto-apply at MEDIUM confidence. <!-- axis: confidence level -->
- Never act on a "stale reference" finding here. <!-- axis: finding type -->
```

Nothing in this list protects a merge step against a finding type nobody thought to name — for
example, deletion justified as removing an unverified claim.

**Solution**: Hoist the invariant to the **point of entry** — ahead of every recipe, and wired into
the first assessment step the agent runs — and state it by **what it protects**, not by what it
enumerates:
