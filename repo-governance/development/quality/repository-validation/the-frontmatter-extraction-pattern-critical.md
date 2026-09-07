---
description: "The critical pattern for extracting frontmatter safely in validation scripts."
when_to_use: "Use when writing a script that extracts frontmatter from a markdown file."
---

# The Frontmatter Extraction Pattern (CRITICAL)

## The Standard AWK Command

This is THE canonical pattern for extracting YAML frontmatter from markdown files:

```bash
awk 'BEGIN{p=0} /^---$/{if(p==0){p=1;next}else{exit}} p==1' file.md
```

**What it does:**

1. Starts with `p=0` (print flag off)
2. When it sees first `---`, sets `p=1` (print flag on) and skips that line
3. Prints all lines while `p==1` (content between the two `---` delimiters)
4. When it sees second `---`, exits (stops processing)

**Result:** Outputs ONLY the YAML frontmatter content, excluding the `---` delimiters.

## Why This Pattern Exists

Markdown files contain many `#` symbols, hyphens, and other characters that can appear in both frontmatter and document body. Searching the entire file produces false positives.

**Problem:** Need to check if frontmatter contains YAML comments (`#` symbols)

**Common Mistake:**

```bash
# FAIL: WRONG: Searches entire file including markdown body
grep "#" .opencode/agents/agent-name.md
# This incorrectly flags markdown headings like "# Agent Title" as violations
```

**Correct Method:**

```bash
# PASS: CORRECT: Extract frontmatter first, then search
awk 'BEGIN{p=0} /^---$/{if(p==0){p=1;next}else{exit}} p==1' .opencode/agents/agent-name.md | grep "#"

# If grep returns results → VIOLATION (YAML comment in frontmatter)
# If grep returns nothing → COMPLIANT (clean frontmatter)
```

## What to Flag vs What NOT to Flag

**FAIL: VIOLATION - Comment in frontmatter:**

```yaml
---
name: agent-name
description: Description here
tools: Read, Write # This comment is a violation
model: sonnet
color: blue
---
```

**PASS: COMPLIANT - Clean frontmatter with markdown headings in body:**

```yaml
---
name: agent-name
description: Description here
tools: Read, Write
model: sonnet
color: blue
---
# Agent Title  ← This is a markdown heading, NOT a violation
## Section      ← This is also NOT a violation

# Why This Matters  ← Still NOT a violation (markdown body)
```

## Verification Steps

1. Extract frontmatter using awk (lines between first two `---`)
2. Search extracted frontmatter for target pattern
3. If found → report as violation with line number and context
4. If not found → mark as compliant
5. Never flag content in markdown body (after second `---`)
