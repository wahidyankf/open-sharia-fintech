---
title: "Common Violations and Fixes"
description: "Before/after examples for common markdown violations."
category: explanation
subcategory: development
tags:
  - markdown
  - linting
  - formatting
  - prettier
  - markdownlint
  - quality
created: 2026-01-17
when_to_use: "Use when fixing a markdown lint violation and you want a concrete example."
---

# Common Violations and Fixes

## Bare URLs

**Violation**:

```markdown
Check out https://example.com for more info.
```

**Fix**:

```markdown
Check out [example.com](https://example.com) for more info.
```

## Trailing Spaces

**Violation**:

```markdown
This line has trailing spaces.
```

**Fix**: Remove trailing spaces (Prettier handles this automatically)

## Multiple Blank Lines

**Violation**:

```markdown
First paragraph.

Second paragraph.
```

**Fix**:

```markdown
First paragraph.

Second paragraph.
```

## Hard Tabs

**Violation**: Using tab characters for indentation

**Fix**: Use spaces instead (Prettier converts automatically)

## Missing Blank Lines Around Headings

**Violation**:

```markdown
Previous paragraph.

## Heading

Next paragraph.
```

**Fix**:

```markdown
Previous paragraph.

## Heading

Next paragraph.
```
