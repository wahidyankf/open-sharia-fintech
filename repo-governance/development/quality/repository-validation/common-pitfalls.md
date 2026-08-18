---
title: "Common Pitfalls"
description: "Common pitfalls when writing validation scripts."
category: explanation
subcategory: development
tags:
  - validation
  - consistency
  - bash
  - awk
  - frontmatter
  - automation
created: 2025-12-14
when_to_use: "Use when debugging a validation script that behaves unexpectedly."
---

# Common Pitfalls

## False Positives from Markdown Headings

**Problem:** Searching entire file for `#` flags markdown headings as violations.

**Solution:** Extract frontmatter first, then search isolated content.

**Example:**

```bash
# FAIL: Produces false positive
grep "#" .opencode/agents/agent.md
# Flags: # Agent Title (markdown heading, NOT a violation)

# PASS: Correct - no false positive
awk 'BEGIN{p=0} /^---$/{if(p==0){p=1;next}else{exit}} p==1' .opencode/agents/agent.md | grep "#"
# Only flags actual YAML comments in frontmatter
```

## Case Sensitivity Issues

**Problem:** YAML field names and values are case-sensitive. Searches may miss violations if case doesn't match.

**Solution:** Use exact case matching or explicitly handle case-insensitive scenarios.

**Example:**

```bash
# Exact match (case-sensitive)
grep "^model:" frontmatter.txt

# Case-insensitive (if needed)
grep -i "^model:" frontmatter.txt
```

## Path Resolution Problems

**Problem:** Relative links may resolve incorrectly if working directory differs from file location.

**Solution:** Always resolve paths from file's directory, not current working directory.

**Example:**

```bash
# FAIL: WRONG - resolves from pwd
resolved="$link_target"

# PASS: CORRECT - resolves from file's directory
resolved="$(dirname "$file")/$link_target"
```

## Regex Metacharacter Issues

**Problem:** Field names or patterns containing regex metacharacters cause unexpected matches.

**Solution:** Escape metacharacters or use fixed-string matching.

**Example:**

```bash
# Field name: "some.field"
field="some.field"

# FAIL: WRONG - '.' matches any character
grep "^$field:" frontmatter.txt

# PASS: CORRECT - escape the dot
escaped=$(echo "$field" | sed 's/\./\\./g')
grep "^$escaped:" frontmatter.txt

# OR use fixed-string matching
grep -F "^$field:" frontmatter.txt
```
