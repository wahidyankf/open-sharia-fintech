---
title: "Table Formatting, Line Length, and Paragraph Structure"
description: "Table and alignment syntax, optimal prose line length, and paragraph structuring for web readability"
category: explanation
subcategory: conventions
tags:
  - content-quality
  - markdown
  - writing-standards
  - accessibility
  - documentation
created: 2025-12-07
when_to_use: "Read this when formatting a table or reviewing a document for line length and paragraph structure."
---

# Table Formatting, Line Length, and Paragraph Structure

## Table Formatting

**Use tables for structured data comparison**.

### Basic Table

```markdown
| Feature         | Free Tier | Pro Tier  |
| --------------- | --------- | --------- |
| Users           | 5         | Unlimited |
| Storage         | 1 GB      | 100 GB    |
| API Calls/month | 1,000     | Unlimited |
| Support         | Community | Priority  |
```

**Table Guidelines**:

- **Align headers** with content using pipes and dashes
- **Keep cells concise** - Long content makes tables hard to read
- **Use header row** - First row should describe columns
- **Consider alternatives** - For complex data, use lists or separate sections

### Table Alignment

```markdown
| Left Aligned | Center Aligned | Right Aligned |
| :----------- | :------------: | ------------: |
| Default      |    Centered    |       Numbers |
| Text         |      Text      |        123.45 |
```

**Alignment Syntax**:

- Left: `:---` (default)
- Center: `:---:`
- Right: `---:`

## Line Length and Readability

**Optimize line length for readability**.

**Guidelines**:

- **Prose text**: Aim for 80-100 characters per line (hard limit: 120)
- **Code blocks**: Follow language conventions (often 80-120 chars)
- **Tables**: May exceed line length (tables are wider by nature)
- **URLs**: Don't break URLs for line length

**Why**: Studies show ~80 characters per line optimizes reading speed and comprehension.

PASS: **Good (Readable Line Length)**:

```markdown
Authentication tokens expire after 1 hour of inactivity. To extend the
session, the client must send a refresh token before expiration. Failed
refresh attempts result in automatic logout.
```

FAIL: **Avoid (Too Long)**:

```markdown
Authentication tokens expire after 1 hour of inactivity and to extend the session the client must send a refresh token before expiration otherwise failed refresh attempts will result in automatic logout and the user will need to log in again.
```

## Paragraph Structure

**Structure paragraphs for web readability**.

**Guidelines**:

- **One main idea per paragraph** - Split complex ideas into multiple paragraphs
- **3-5 sentences maximum** - Short paragraphs are easier to scan on screens
- **Topic sentence first** - Lead with the main point
- **Blank line between paragraphs** - Visual separation improves scannability
