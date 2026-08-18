---
title: "Quality Checklist, Related Conventions, and References"
description: "The full pre-commit quality checklist plus links to related universal and context-specific conventions"
category: explanation
subcategory: conventions
tags:
  - content-quality
  - markdown
  - writing-standards
  - accessibility
  - documentation
created: 2025-12-07
when_to_use: "Read this before committing markdown content, to run through the quality checklist and find related conventions."
---

# Quality Checklist, Related Conventions, and References

## Quality Checklist

Before committing markdown content, verify:

- [ ] **Writing Style**
  - Active voice used (passive only when appropriate)
  - Professional yet approachable tone
  - Clear and concise language (no filler words)
  - Audience-appropriate complexity level

- [ ] **Heading Hierarchy**
  - Single H1 (document title)
  - Proper H2-H6 nesting (no skipped levels)
  - Descriptive heading text
  - Headings used for structure, not styling

- [ ] **Accessibility**
  - All images have descriptive alt text
  - Semantic HTML elements used correctly
  - Color not sole means of conveying information
  - Descriptive link text (not "click here")
  - Proper table headers and list structure

- [ ] **Formatting**
  - Code blocks specify language
  - Text formatting used purposefully (not overused)
  - Lists use proper markdown syntax
  - Blockquotes and callouts formatted consistently
  - Tables aligned and readable
  - Mermaid diagrams use correct comment syntax (`%%`, not `%%{ }%%`)

- [ ] **Readability**
  - Lines ≤80-100 characters (prose)
  - Paragraphs ≤3-5 sentences
  - Blank lines between paragraphs
  - Logical flow and structure

## Related Conventions

**Universal Conventions (apply to all markdown)**:

- [Mathematical Notation Convention](../../formatting/mathematical-notation.md) — LaTeX in markdown
- [Color Accessibility Convention](../../formatting/color-accessibility.md) — Accessible color palette for diagrams
- [Diagrams and Schema Convention](../../formatting/diagrams.md) — Mermaid diagram standards (includes comment syntax requirements)
- [Emoji Usage Convention](../../formatting/emoji.md) — Semantic emoji use

**Context-Specific Conventions**:

- [File Naming Convention](../../structure/file-naming.md) — File naming standards
- [Linking Convention](../../formatting/linking.md) — Internal and external linking
- [Tutorial Convention](../../tutorials/general.md) — Tutorial structure and pedagogy
- [Diátaxis Framework](../../structure/diataxis-framework.md) — Documentation organization

## References

**Web Content Accessibility Guidelines (WCAG)**:

- [WCAG 2.1 Level AA](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM: Writing for Screen Readers](https://webaim.org/articles/screenreader/)
- [WebAIM: Contrast Checker](https://webaim.org/resources/contrastchecker/)

**Writing Guides**:

- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [The Chicago Manual of Style](https://www.chicagomanualofstyle.org/)

**Markdown References**:

- [CommonMark Spec](https://commonmark.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
