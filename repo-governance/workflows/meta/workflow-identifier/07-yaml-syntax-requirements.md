---
title: "YAML Syntax Requirements"
description: Which characters require quoting in workflow YAML frontmatter, with good/bad examples, to avoid breaking some YAML parsers.
category: explanation
subcategory: workflows
tags:
  - workflows
  - agents
  - orchestration
  - patterns
created: 2025-12-23
when_to_use: Use when writing or reviewing a workflow's YAML frontmatter and unsure whether a value needs quoting.
---

# YAML Syntax Requirements

**CRITICAL**: All YAML frontmatter values containing special characters MUST be wrapped in quotes to prevent parser errors in some YAML parsers.

**Characters requiring quotes**:

- Colon `:` (most common)
- Square brackets `[`, `]`
- Curly braces `{`, `}`
- Hash `#`
- Ampersand `&`
- Asterisk `*`
- Exclamation mark `!`
- Pipe `|`
- Greater-than `>`
- Single quote `'`
- Double quote `"`
- Percent `%`
- At sign `@`
- Backtick `` ` ``

**Quoting guidelines**:

- Use double quotes `"` for consistency
- Quote ALL values containing special characters, not just the character itself
- Escape inner quotes if needed: `"Description with "quoted" text"`
- Quote complex descriptions containing colons (e.g., mode descriptions with multiple options)

**Examples**:

Good:

```yaml
description: "Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)"
goal: "Validate repository consistency across all layers, apply fixes iteratively until zero findings achieved"
values: [lax, normal, strict, ocd]
```

Bad:

```yaml
description: Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)
goal: Validate repository consistency across all layers, apply fixes iteratively until zero findings achieved
values: [lax, normal, strict, ocd]  # This is OK - arrays are fine without quotes
```

**Why this matters**:

- Unquoted colons break some YAML parsers (they may display raw frontmatter or fail to load)
- YAML parsers interpret unquoted special characters as syntax, not content
- Quoted values ensure consistent parsing across all tools (GitHub, static site generators, editor previews)
