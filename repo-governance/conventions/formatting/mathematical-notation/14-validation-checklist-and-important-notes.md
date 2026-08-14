---
title: "Validation Checklist and Important Notes"
description: The pre-commit LaTeX validation checklist, plus notes on browser compatibility, rendering performance, accessibility, and version history.
when_to_use: Use when doing a final review pass on mathematical notation before committing.
category: explanation
subcategory: conventions
tags:
  - latex
  - mathematics
  - formulas
  - notation
  - conventions
created: 2025-12-02
---

# Validation Checklist and Important Notes

## PASS: Validation Checklist

When adding or reviewing mathematical notation:

- [ ] All mathematical expressions use LaTeX syntax
- [ ] Inline math uses `$...$` for terms within text
- [ ] Display math uses `$$...$$` for standalone equations
- [ ] Single `$` delimiters are ONLY used inline (on same line as text)
- [ ] Display-level equations use `$$` delimiters (on separate lines)
- [ ] All multi-line equations use `\begin{aligned}...\end{aligned}` (NOT `\begin{align}`) for KaTeX compatibility
- [ ] All `\begin{aligned}` blocks use `$$` delimiters (not single `$`)
- [ ] Variables are defined after formulas
- [ ] Notation is consistent throughout the document
- [ ] Formulas render correctly on GitHub
- [ ] No LaTeX inside code blocks (use plain text)
- [ ] No LaTeX inside Mermaid diagrams (use plain text)
- [ ] Complex formulas have clear alignment and structure
- [ ] All Greek letters, fractions, and summations use proper commands

## Important Notes

### Browser Compatibility

LaTeX rendering works in all modern browsers:

- **Chrome/Edge** - Full support
- **Firefox** - Full support
- **Safari** - Full support (macOS and iOS)
- **Mobile browsers** - Full support on GitHub mobile app

No special configuration or extensions needed.

### Performance

LaTeX rendering is fast and lightweight:

- **Client-side rendering** - MathJax/KaTeX in browser
- **No server-side processing** - Pure markdown with math syntax
- **Cacheable** - Rendered math is cached by browsers

Large documents with many formulas render quickly on GitHub.

### Accessibility

LaTeX math has good accessibility:

- **Screen readers** - MathJax provides screen reader support
- **Zoom** - Math scales properly with page zoom
- **Copy-paste** - Can copy LaTeX source from rendered math
- **Search** - Full-text search works on LaTeX source

### Version History

- **2025-12-02** - Initial convention document created
- LaTeX math support verified on GitHub (since May 2022)
