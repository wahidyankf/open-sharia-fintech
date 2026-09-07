---
description: The two-tier formatting rule for referencing repository rules — markdown link on first mention, inline code on subsequent mentions — with correct and incorrect examples.
when_to_use: Use when writing prose that references a vision, principle, convention, development practice, or workflow document more than once in a section.
---

# When to Link Rule References: Formatting and Examples

When referencing repository rules (visions, principles, conventions, development practices, workflows), use a **two-tier formatting approach**:

## First Mention: MUST Use Markdown Link

The **first mention** of a rule in any document section MUST use a markdown link:

```markdown
[Rule Name](./path/to/rule.md)
```

**Rule categories requiring this treatment:**

- Vision documents (`repo-governance/vision/`)
- Core Principles (`repo-governance/principles/`)
- Conventions (`repo-governance/conventions/`)
- Development practices (`repo-governance/development/`)
- Workflows (`repo-governance/workflows/`)

## Subsequent Mentions: MUST Use Inline Code

**Subsequent mentions** of the same rule within the same section MUST use inline code formatting:

```markdown
`rule-name`
```

## Examples

### PASS: Correct - Two-Tier Formatting

```markdown
## Implementation Details

This feature implements the [Linking Convention](./linking.md) by using relative paths. The `Linking Convention` requires `.md` extensions, which helps maintain compatibility across viewers. When applying `Linking Convention` rules, verify all paths are relative.
```

**Analysis:**

- First mention: `[Linking Convention](./linking.md)` PASS: (markdown link)
- Second mention: `` `Linking Convention` `` PASS: (inline code)
- Third mention: `` `Linking Convention` `` PASS: (inline code)

### PASS: Correct - Multiple Rules

```markdown
## Standards Compliance

All documentation follows the [File Naming Convention](../structure/file-naming.md) and [Linking Convention](./linking.md). The `File Naming Convention` defines kebab-case filename rules, while the `Linking Convention` specifies link syntax. Both `File Naming Convention` and `Linking Convention` are validated by docs-checker.
```

**Analysis:**

- File Naming Convention: First mention (link) , subsequent mentions (inline code)
- Linking Convention: First mention (link) , subsequent mentions (inline code)

### FAIL: Incorrect - All Plain Text

```markdown
## Standards Compliance

All documentation follows the Linking Convention. The Linking Convention requires .md extensions. When applying Linking Convention rules, verify paths.
```

**Issue:** No links or inline code formatting - readers cannot navigate to convention document.

### FAIL: Incorrect - All Links

```markdown
## Standards Compliance

All documentation follows the [Linking Convention](./linking.md). The [Linking Convention](./linking.md) requires .md extensions. When applying [Linking Convention](./linking.md) rules, verify paths.
```

**Issue:** Redundant links create visual clutter and maintenance burden.

### FAIL: Incorrect - All Inline Code

```markdown
## Standards Compliance

All documentation follows the `Linking Convention`. The `Linking Convention` requires .md extensions. When applying `Linking Convention` rules, verify paths.
```

**Issue:** First mention lacks navigable link - readers cannot discover the convention document.
