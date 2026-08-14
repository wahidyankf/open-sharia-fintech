# Content Quality — Formatting Conventions and Common Mistakes

## Formatting Conventions

**Code Blocks**: Always specify language for syntax highlighting.

````markdown
✅ Good:

```javascript
const x = 10;
```
````

❌ Bad:

```
const x = 10;  ← No language specified
```

**Paragraph Length**: Keep paragraphs concise (≤5 lines for readability).

**Line Length**: Aim for 80-100 characters per line for better readability.

**Lists**: Use consistent formatting:

- Unordered lists: Use `-` (hyphen) for consistency
- Ordered lists: Use `1.` numbering
- Nested lists: Indent with 2 spaces per level

## No Time Estimates

**CRITICAL**: Never include time-based framing in content.

❌ **Forbidden**:

- "This tutorial takes 30 minutes"
- "Complete this in 2-3 weeks"
- "You can do this in 5 minutes"

✅ **Instead**:

- Describe what will be accomplished
- List concrete outcomes
- Let users determine their own pace

**Rationale**: Time estimates create artificial pressure and vary widely by experience level.

## Common Quality Checklist

Before publishing any markdown content, verify:

- [ ] Active voice used throughout
- [ ] Exactly one H1 heading
- [ ] Proper heading nesting (no skipped levels)
- [ ] All images have descriptive alt text
- [ ] Code blocks specify language
- [ ] No time-based estimates or framing
- [ ] Professional, welcoming tone
- [ ] Paragraphs ≤5 lines
- [ ] Clear, jargon-free language (or jargon explained)
- [ ] WCAG AA color contrast for any custom colors
- [ ] Semantic formatting (bold for emphasis, proper lists)

## Common Mistakes

### ❌ Mistake 1: Missing alt text

**Wrong**: `![](./image.png)`
**Right**: `![Detailed description of image content](./image.png)`

### ❌ Mistake 2: Skipped heading levels

**Wrong**:

```markdown
# Title

### Subsection ← Skips H2
```

**Right**:

```markdown
# Title

## Section

### Subsection
```

### ❌ Mistake 3: Time-based framing

**Wrong**: "This tutorial takes 30 minutes to complete."
**Right**: "This tutorial covers X, Y, and Z concepts."

### ❌ Mistake 4: Passive voice overuse

**Wrong**: "The file is created by the command."
**Right**: "The command creates the file."

### ❌ Mistake 5: Code blocks without language

**Wrong**:

```
npm install
```

**Right**:

```bash
npm install
```
