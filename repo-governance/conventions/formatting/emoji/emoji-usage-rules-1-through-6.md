---
title: "Emoji Usage Rules 1-6"
description: "Six binding usage rules: semantic consistency, restraint, heading-level placement, no emoji in technical content, accessibility, and no emoji in frontmatter."
when_to_use: Use when checking a specific emoji placement against the repository's binding usage rules.
category: explanation
subcategory: conventions
tags:
  - emoji
  - accessibility
  - scannability
  - conventions
  - markdown
created: 2025-12-04
---

# Emoji Usage Rules 1-6

## Rule 1: Semantic Consistency

**Each emoji must have a single, consistent meaning across all documents.**

PASS: **Correct:**

```markdown
## Security Considerations

## Authentication

## Authorization
```

FAIL: **Incorrect:**

```markdown
## Security Considerations

## Authentication <!-- Don't use different security emojis -->

## ️ Authorization <!-- Stick to one emoji per concept -->
```

## Rule 2: Restraint and Balance

**Use 1-2 emojis per section. Avoid emoji overload.**

PASS: **Correct:**

```markdown
## Purpose

This section explains the core objectives...

## PASS: Best Practices

1. Configure for your stack
2. Tune rules
3. Set thresholds
```

FAIL: **Incorrect:**

```markdown
## Purpose

This section explains the core objectives...

## PASS: Best Practices ️ ️

1. Configure for your stack
2. ️ Tune rules
3. Set thresholds
```

## Rule 3: Heading-Level Placement

**Place emojis at the start of headings (H2, H3, H4), not inline in body text.**

PASS: **Correct:**

```markdown
## Configuration

Configure the application by editing...
```

FAIL: **Incorrect:**

```markdown
## Configuration

Configure the application by editing...
```

**Exception:** Status indicators (PASS: FAIL: ️) can be used inline for examples or lists.

## Rule 4: No Emojis in Technical Content

**Never use emojis in code blocks, commands, file paths, or technical specifications.**

PASS: **Correct:**

```markdown
## Quick Start

Install dependencies:
\`\`\`bash
npm install
npm run dev
\`\`\`
```

FAIL: **Incorrect:**

```markdown
## Quick Start

Install dependencies:
\`\`\`bash
npm install
npm run dev
\`\`\`
```

## Rule 5: Accessibility Consideration

**Use emojis that enhance, not replace, text meaning. Screen readers will read emoji alt text.**

PASS: **Correct:**

```markdown
## Security Warning

This feature has security implications...
```

FAIL: **Incorrect:**

```markdown
## ️

This feature has security implications... <!-- Heading must have text -->
```

## Rule 6: No Emojis in Frontmatter or Metadata

**Keep YAML frontmatter, file names, and metadata emoji-free.**

PASS: **Correct:**

```yaml
---
title: Security Best Practices
category: explanation
---
```

FAIL: **Incorrect:**

```yaml
---
title: Security Best Practices
category: explanation
---
```
