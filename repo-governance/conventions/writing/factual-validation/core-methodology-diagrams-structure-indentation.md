---
description: Verification process for Mermaid diagram color accessibility, markdown H1/heading structure, bullet indentation direction, and language-specific code block indentation.
when_to_use: Use when validating a Mermaid diagram's color palette, a document's heading structure, or a code block's indentation against the language-specific convention.
---

# Core Validation Methodology — Diagrams, Structure, and Indentation Validation

Continues from [Code Examples, External References, and Mathematical Notation](./core-methodology-code-references-math.md).

## 7. Diagram Color Accessibility Validation

**What to Verify:**

- Mermaid diagrams use color-blind friendly colors
- Inaccessible colors (red, green, yellow) are NOT used
- Shape differentiation is used (not relying on color alone)
- Black borders (#000000) are included for definition
- Color scheme is documented in comments
- Contrast ratios meet WCAG AA standards (4.5:1 for text)

**Accessible Palette:**

- Blue: `#0173B2`
- Orange: `#DE8F05`
- Teal: `#029E73`
- Purple: `#CC78BC`
- Brown: `#CA9161`

**Verification Process:**

```
1. Extract Mermaid diagrams from content
2. Check style declarations for fill colors
3. Verify all colors are from accessible palette
4. Flag any red, green, or yellow usage
5. Confirm black borders present
```

## 8. Markdown Structure Format Validation

**What to Verify:**

- File has H1 heading at start (`# ...`)
- Traditional sections are used (`## H2`, `### H3`, etc.)
- Proper document structure with paragraphs
- Single H1 per file (not multiple)

**Verification Process:**

```
1. Read file content
2. Check first non-frontmatter line is H1 (`# Title`)
3. Verify only one H1 in entire file
4. Confirm proper heading hierarchy (no H3 without H2)
```

## 9. Bullet Indentation Validation

**What to Verify:**

- Correct pattern: `- Text` (dash, space, text) for same-level
- Nested: `- Text` (2 spaces BEFORE dash)
- Deeper: `- Text` (4 spaces BEFORE dash)
- NOT: `-  Text` (spaces AFTER dash - wrong)

**Common error:**

```markdown
FAIL: WRONG - Spaces after dash:

- First level (spaces after dash - WRONG!)
- Nested level (spaces after dash - WRONG!)

PASS: CORRECT - Spaces before dash:

- First level
  - Nested level (2 spaces before dash)
    - Deeper level (4 spaces before dash)
```

## 10. Code Block Indentation Validation

**What to Verify:**

- Language-specific idiomatic indentation (NOT tabs, except Go)
- JavaScript/TypeScript: 2 spaces per indent level
- Python: 4 spaces per indent level
- YAML: 2 spaces per indent level
- JSON: 2 spaces per indent level
- CSS: 2 spaces per indent level
- Bash/Shell: 2 spaces per indent level
- Go: tabs (ONLY exception where tabs are correct)

**Rationale:** Code blocks must use language-specific idiomatic indentation to ensure examples can be copied and pasted correctly into actual code files.
