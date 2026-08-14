---
title: "How It Applies"
description: Concrete pass/fail examples of color accessibility, alt text, heading hierarchy, contrast, and semantic HTML.
category: explanation
subcategory: principles
tags:
  - principles
  - accessibility
  - wcag
created: 2025-12-15
when_to_use: Use when implementing or reviewing content for compliance with color, alt-text, heading, contrast, or semantic-HTML accessibility rules.
---

# How It Applies

## Color Accessibility

**Context**: All diagrams, visual aids, and styling.

**Requirement**: Use only color-blind friendly palette.

PASS: **Accessible Palette** (Correct):

```css
/* Verified safe for all color blindness types */
#0173B2  /* Blue */
#DE8F05  /* Orange */
#029E73  /* Teal */
#CC78BC  /* Purple */
#CA9161  /* Brown */
```

FAIL: **Inaccessible Colors** (Avoid):

```css
/* Invisible or problematic for color-blind users */
#FF0000  /* Red - invisible to protanopia/deuteranopia */
#00FF00  /* Green - invisible to protanopia/deuteranopia */
#FFFF00  /* Yellow - invisible to tritanopia */
```

**See**: [Color Accessibility Convention](../../../conventions/formatting/color-accessibility.md) - The master reference for all color usage

## Image Alt Text

**Context**: All images in documentation.

**Requirement**: Descriptive alt text for every image.

PASS: **Good Alt Text**:

```markdown
![Architecture diagram showing client-server communication flow with database](./images/architecture.png)
```

**Why this works**: Describes what the image shows and its purpose. Screen reader users understand the content.

FAIL: **Bad Alt Text**:

```markdown
![image](./images/architecture.png)
```

**Why this fails**: Generic "image" provides no information. Screen reader users learn nothing.

## Heading Hierarchy

**Context**: All markdown documents.

**Requirement**: Single H1, proper H2-H6 nesting, no skipped levels.

PASS: **Correct Hierarchy**:

```markdown
# Document Title (H1)

## Section (H2)

### Subsection (H3)

#### Detail (H4)

## Another Section (H2)
```

**Why this works**: Screen readers build document outline from headings. Proper nesting creates logical structure.

FAIL: **Incorrect Hierarchy**:

```markdown
# Document Title (H1)

### Subsection (H3) <!-- WRONG! Skipped H2 -->

##### Detail (H5) <!-- WRONG! Skipped H4 -->
```

**Why this fails**: Skipped levels break screen reader navigation. Users can't understand document structure.

## Color Contrast

**Context**: All text and UI elements.

**Requirement**: WCAG AA minimum contrast ratios.

**Standards**:

- Normal text: **4.5:1** minimum
- Large text (18pt+ or 14pt+ bold): **3:1** minimum
- UI components: **3:1** minimum

PASS: **Sufficient Contrast**:

```
Blue (#0173B2) on White (#FFFFFF): 8.59:1 (AAA)
Orange (#DE8F05) on White: 6.48:1 (AAA)
```

FAIL: **Insufficient Contrast**:

```
Light gray on white: 2:1 (fails WCAG AA)
Yellow on white: 1.5:1 (fails WCAG AA)
```

## Semantic HTML

**Context**: All markdown content.

**Requirement**: Use semantic elements, not styling hacks.

PASS: **Semantic Structure**:

```markdown
## Section Heading

- Unordered list item
- Another item

> **Note**: This is a callout using blockquote
```

**Why this works**: Proper markdown syntax creates semantic HTML. Screen readers understand structure.

FAIL: **Non-Semantic**:

```markdown
**Section Heading**

**•** List item
**•** Another item

**Note**: This is just bold text
```

**Why this fails**: Manual formatting doesn't create semantic HTML. Screen readers see only styled text.
