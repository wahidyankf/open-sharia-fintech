---
title: "Anti-Patterns — Verbal Tradition, Missing READMEs, and Outdated Docs"
description: Why verbal-only knowledge, missing READMEs, and outdated docs fail contributors.
category: explanation
subcategory: principles
tags:
  - principles
  - documentation
created: 2025-12-28
when_to_use: Use when auditing a project for missing or stale documentation.
---

# Anti-Patterns — Verbal Tradition, Missing READMEs, and Outdated Docs

## Verbal Tradition Instead of Written Documentation

FAIL: **Problem**: Knowledge passed verbally but never written down.

**Symptoms**:

- "Just ask Alice, she knows how this works"
- "We discussed this in a meeting last month"
- "Everyone on the team knows this convention"

**Why it's bad**:

- Alice might not always be available
- Meeting discussions are not searchable or permanent
- "Everyone knows" excludes newcomers and future contributors

PASS: **Solution**: Document all important knowledge in permanent, searchable formats (markdown docs, code comments, convention documents).

## README-less Repositories

FAIL: **Problem**: Repositories without README files.

**Why it's bad**: No entry point for understanding what the code does, why it exists, or how to use it.

PASS: **Solution**: Every repository, library, and application MUST have a README explaining:

- What it is
- Why it exists
- How to use it
- How to contribute

## Outdated Documentation

FAIL: **Problem**: Documentation that doesn't match current reality.

**Why it's bad**: Worse than no documentation - misleads users and maintainers.

PASS: **Solution**:

- Update documentation when changing code (documentation is part of the change)
- Use automated validation (checker agents verify docs match reality)
- Mark deprecated sections clearly
- Remove obsolete documentation rather than leaving it to confuse

## Documentation Without Context

FAIL: **Problem**: Technical details without explanation of WHY.

```markdown
## Configuration

Set `PROFIT_RATE=15` in environment variables.
```

**Why it's bad**: Doesn't explain WHY 15, whether it can change, or what it represents.

PASS: **Solution**: Always provide context.

```markdown
## Configuration

Set `PROFIT_RATE` to the Murabahah profit markup percentage approved by
your Shariah board. Default is `15` (representing 15% markup), which aligns
with our Shariah board's standard for short-term asset financing contracts.

This rate must be:

- Fixed (not variable) per Murabahah Shariah principles
- Approved by qualified Islamic scholars
- Clearly disclosed to all parties

Example: `PROFIT_RATE=15`
```
