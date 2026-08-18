---
title: "Why Mermaid First?"
description: "Explains Mermaid's wide platform support and advantages over ASCII art, and when ASCII is still useful."
when_to_use: "Use when justifying or challenging the Mermaid-first policy for a specific rendering context."
category: explanation
subcategory: conventions
tags:
  - diagrams
  - mermaid
  - ascii-art
  - visualization
  - conventions
  - accessibility
  - color-blindness
created: 2025-11-24
---

# Why Mermaid First?

Mermaid diagram support has become ubiquitous across modern development tools:

## Wide Platform Support

- **GitHub**: Native Mermaid rendering in markdown files (since May 2021)
- **Text Editors**: VS Code, IntelliJ IDEA, Sublime Text (via plugins/extensions)
- **Documentation Platforms**: GitLab, Notion, Confluence all support Mermaid
- **Mobile Apps**: GitHub mobile renders Mermaid correctly

## Advantages Over ASCII Art

1. **Professional Appearance**: Clean, crisp diagrams with proper styling
2. **Maintainability**: Text-based source is easier to edit than ASCII positioning
3. **Expressiveness**: Supports complex relationships (sequence diagrams, entity relationships, state machines)
4. **Interactive**: Many platforms allow zooming and inspection
5. **Accessible**: Screen readers can parse the source text structure

## When ASCII Art Is Still Useful

ASCII art is now **optional** and only recommended for rare edge cases:

- Terminal-only environments without rich markdown support
- Extremely limited bandwidth scenarios where rendering is disabled
- Simple directory tree structures (where ASCII is clearer than Mermaid)

**In practice**: Most users will view markdown files through GitHub or modern text editors, all of which support Mermaid.
