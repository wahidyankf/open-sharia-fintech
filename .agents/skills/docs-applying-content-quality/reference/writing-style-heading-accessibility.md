# Content Quality — Writing Style, Heading Hierarchy, and Accessibility

## Writing Style and Tone

**Active Voice Required**: Use active voice for clarity and directness.

✅ **Good**: "The agent validates the content against the convention."
❌ **Avoid**: "The content is validated against the convention by the agent."

**Professional Tone**: Maintain professional, welcoming tone without being overly formal.

**Clarity and Conciseness**: Write clear, direct sentences. Avoid jargon without context.

**Audience Awareness**: Consider reader's technical level and provide necessary context.

## Heading Hierarchy

**Single H1 Rule**: Each markdown file MUST have exactly one H1 heading (# Title).

**Proper Nesting**: Follow hierarchical structure without skipping levels:

- H1 (#) - Document title
- H2 (##) - Major sections
- H3 (###) - Subsections
- H4 (####) - Sub-subsections
- H5/H6 - Use sparingly

❌ **Invalid nesting** (skips level):

```markdown
# Title

### Subsection ← Skips H2!
```

✅ **Valid nesting**:

```markdown
# Title

## Section

### Subsection
```

## Accessibility Standards

**Alt Text Required**: All images MUST have descriptive alt text.

```markdown
✅ ![Architecture diagram showing six-layer hierarchy](./diagram.png)
❌ ![](./diagram.png) ← Missing alt text
```

**WCAG AA Color Contrast**: Text must meet WCAG AA contrast ratios:

- Normal text: 4.5:1 minimum
- Large text (18pt+): 3:1 minimum

**Semantic Formatting**:

- Use **bold** for emphasis, not italics
- Use proper heading structure (not bold text as headers)
- Use lists for list content (not manual bullets)

**Screen Reader Support**: Content must be accessible to screen readers through proper HTML structure and ARIA labels when needed.
