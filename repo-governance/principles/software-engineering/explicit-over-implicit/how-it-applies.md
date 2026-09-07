---
description: Explicit-vs-implicit examples for agent tool permissions, file naming, and color.
when_to_use: Use when reviewing tool permissions, a filename, or a color value.
---

# How It Applies

## AI Agent Tool Permissions

**Context**: Agent files specify which tools they can use.

PASS: **Explicit (Correct)**:

```yaml
---
name: docs-checker
tools: Read, Glob, Grep
---
```

**Why this works**: Clear whitelist of exactly three tools. Anyone reading this knows the agent can read files, glob patterns, and grep content. No surprises.

FAIL: **Implicit (Avoid)**:

```yaml
---
name: docs-checker
tools: all
---
```

**Why this fails**: "All tools" is implicit. What does "all" include? Write? Bash? Can this agent delete files? Run commands? Requires knowledge of what tools exist. Security risk.

## File Naming

**Context**: Filenames should clearly describe their content so readers can identify a file without opening it.

PASS: **Explicit (Correct)**:

```
explicit-over-implicit.md
```

**Why this works**: The basename is a full, readable kebab-case description of the content. The directory hierarchy (`repo-governance/principles/software-engineering/`) explicitly encodes the category.

FAIL: **Implicit (Avoid)**:

```
eoi.md  # "clever" abbreviation
```

**Why this fails**: What does "eoi" mean? Requires insider knowledge. Not self-documenting.

## Color Specification

**Context**: Mermaid diagrams use colors.

PASS: **Explicit (Correct)**:

```css
fill: #0173b2;
```

**Why this works**: Exact hex code. Renders identically everywhere. No ambiguity about which blue.

FAIL: **Implicit (Avoid)**:

```css
fill: blue;
```

**Why this fails**: CSS color names vary by browser and system. "Blue" could be #0000FF, #0173B2, or any blue. Not predictable.
