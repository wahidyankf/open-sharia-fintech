---
title: "Accessibility: Alt Text and Semantic HTML"
description: "Writing descriptive image alt text and using semantic markdown elements instead of bold-as-heading substitutes"
category: explanation
subcategory: conventions
tags:
  - content-quality
  - markdown
  - writing-standards
  - accessibility
  - documentation
created: 2025-12-07
when_to_use: "Read this when adding an image or reviewing whether markdown elements are used semantically."
---

# Accessibility: Alt Text and Semantic HTML

## Alt Text for Images

**ALL images MUST have descriptive alt text** for screen readers and accessibility.

PASS: **Good Alt Text**:

```markdown
![Architecture diagram showing client-server communication flow with database](./images/architecture.png)

![Screenshot of the authentication form with username and password fields](./screenshots/login-form.png)
```

FAIL: **Bad Alt Text**:

```markdown
![image](./images/architecture.png) <!-- Too vague -->

![Screenshot](./screenshots/login-form.png) <!-- Not descriptive -->
```

**Alt Text Guidelines**:

- **Describe the content** - What does the image show?
- **Explain the purpose** - Why is this image here?
- **Keep it concise** - Aim for 1-2 sentences (screen readers)
- **Avoid "image of" or "picture of"** - It's implied
- **Include text from image** - If image contains important text

**Decorative Images**: Use empty alt text `![](image.png)` for purely decorative images that don't add information.

## Semantic HTML

**Use semantic HTML elements** appropriately in markdown.

PASS: **Good (Semantic)**:

```markdown
## Section Title <!-- Semantic heading -->

> **Note**: This is a callout using blockquote <!-- Semantic blockquote -->

- Unordered list item <!-- Semantic list -->
- Another item

1. Ordered list item <!-- Semantic ordered list -->
2. Next step
```

FAIL: **Avoid (Non-Semantic)**:

```markdown
**Section Title** <!-- Using bold instead of heading -->

**Note**: This is a callout <!-- Just bold text, not semantic blockquote -->

**•** List item <!-- Manual bullets instead of list syntax -->
**•** Another item
```

**Why**: Semantic HTML provides meaning and structure for screen readers and assistive technologies.
