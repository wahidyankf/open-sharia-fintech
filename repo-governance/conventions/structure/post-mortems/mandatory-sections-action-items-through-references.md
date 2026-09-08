---
description: The required Action Items, What Went Well, Lessons Learned, and References sections that close out a post-mortem document, in reading order
when_to_use: Read this when authoring the closing mandatory sections of a post-mortem, from the action-item table through source references.
---

# Mandatory Sections: Action Items Through References

## 11. Action Items

Each action item must be:

- **Actionable** — starts with a verb
- **Specific** — names the system, file, or process to change
- **Bounded** — has a clear definition of done
- **Owned** — assigned to a role or team
- **Prioritized** — P0 / P1 / P2 (see below)
- **Tracked** — linked to a `plans/` reference or issue id

Priority definitions:

| Priority | Meaning                                                                              |
| -------- | ------------------------------------------------------------------------------------ |
| **P0**   | Blocks recurrence or eliminates data-loss risk; complete before `doc_status: closed` |
| **P1**   | Important improvement; schedule promptly                                             |
| **P2**   | Nice-to-have; schedule when capacity allows                                          |

Table columns (use this exact structure):

```markdown
| #   | Action                                                     | Owner      | Priority | Ticket                            | Status |
| --- | ---------------------------------------------------------- | ---------- | -------- | --------------------------------- | ------ |
| 1   | Add generated binding dirs to .prettierignore              | Maintainer | P0       | plans/backlog/prettierignore-fix/ | Open   |
| 2   | Document generated-artifact exclusion pattern in AGENTS.md | Maintainer | P1       | —                                 | Open   |
```

`Ticket` must be a `plans/` folder reference or an issue id. Use `—` only if the item has not
yet been promoted to a plan — do not leave it empty permanently.

## 12. What Went Well

Include things that limited impact and places where the team got lucky. "Where we got lucky"
is important: luck is a latent risk to address, not a thing to celebrate silently.

## 13. Lessons Learned

Distill the key insights from this incident that generalize beyond the immediate fix. Keep it
concise — two to five bullets. These should inform CI strategy, design decisions, or operating
procedures going forward.

## 14. References

Links to CI run logs, Vercel deployment dashboards, related plans, related post-mortems, or
external sources consulted.
