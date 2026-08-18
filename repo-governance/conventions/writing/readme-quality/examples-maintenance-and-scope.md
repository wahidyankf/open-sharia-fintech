---
title: "Examples, Maintenance, and Scope vs Structural Conventions"
description: Worked good-example excerpts from this project, README maintenance triggers, and the boundary with the structural-placement convention
category: explanation
subcategory: conventions
tags:
  - conventions
  - readme
  - engagement
  - accessibility
  - writing
created: 2025-12-07
when_to_use: Read this for real worked examples of good README writing, or to know when a README needs a maintenance review.
---

# Examples, Maintenance, and Scope vs Structural Conventions

## Examples from This Project

### Good Example: Motivation Hook

```markdown
**The Challenge**: Organizations worldwide need enterprise software that respects Islamic principles, but most solutions treat Sharia-compliance as an afterthought—bolted on rather than built in.

**Our Solution**: We're building an open-source platform with Sharia-compliance at its core.
```

**Why it works**:

- Clear problem statement (one sentence)
- Emotional connection (afterthought vs built-in)
- Clear solution (one sentence)
- No jargon
- Scannable structure

### Good Example: Benefits-Focused

```markdown
**What this means:**

- **Your data is portable** - Plain text and open formats you can read anywhere
- ️ **No forced dependencies** - Pick your own hosting, database, or infrastructure
- **Easy migration** - Export and move to alternatives anytime
```

**Why it works**:

- User benefits, not features
- Active voice ("Your data")
- Plain language ("keep you free")
- Visual markers (emojis)
- Short, clear statements

### Good Example: Navigation Focus

```markdown
### Monorepo Architecture

This project uses Nx to manage applications and libraries:

- **apps/** - Deployable applications
- **libs/** - Reusable libraries

**Learn More**:

- [Monorepo Structure Reference](../../../docs/reference/monorepo-structure.md)
- [How to Add New App](../../../docs/how-to/add-new-app.md)
```

**Why it works**:

- Brief summary (3 lines)
- Links to detailed docs
- Doesn't duplicate comprehensive content
- Easy to scan

## Maintenance

**When Updating README**:

1. Use `readme-maker` agent to help write new sections
2. Use `readme-checker` agent to validate changes
3. Run through quality checklist before committing
4. Get feedback from non-technical reviewers if making major changes

**Red Flags** (triggers for review):

- Any paragraph exceeds 5 lines
- Any acronym without context
- Any jargon from "avoid" list above
- The word-budget gate reports the README over target
- Complaints from contributors about clarity

## Scope vs Structural Conventions

This convention governs README quality — clarity, voice, scannability, engagement, and plain language. It applies to all `README.md` files across the repository.

Structural placement of content — what belongs in an app or infra README vs in `specs/apps/<app-family>/` — is governed by a separate convention: [App README vs Specs Convention](../../structure/app-readme-vs-specs.md). That convention defines the Category A (dev-runtime, stays in README) and Category B (behavior/architecture, moves to specs/) split, line-count caps, and forbidden headings. Both conventions apply to app READMEs simultaneously: this convention governs HOW to write the content, the other governs WHAT content to include.
