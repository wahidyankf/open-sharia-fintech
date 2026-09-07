---
description: How to open a README motivation section with a problem-solution hook instead of a dense paragraph
when_to_use: Read this when writing or reviewing the opening of a README's motivation section.
---

# 1. Hook Readers Immediately

**Problem-Solution Narrative**: Start motivation sections with a clear problem statement followed by your solution.

**FAIL: Bad** (jumps straight to solution):

```markdown
## Purpose

This convention establishes quality standards for README.md files to make them engaging, accessible, and scannable. It ensures READMEs use problem-solution hooks, plain language, proper structure, and benefits-focused language that welcomes all readers including those new to the project.

## Scope

### What This Convention Covers

- **README structure** - Essential sections and their order
- **Opening hooks** - Problem-solution framing to engage readers
- **Plain language** - No jargon, acronym context, accessible writing
- **Paragraph limits** - Maximum 5 lines per paragraph for scannability
- **Benefits-focused language** - Emphasizing value to users
- **Accessibility** - Making READMEs welcoming to all skill levels

### What This Convention Does NOT Cover

- **Technical accuracy** - Factual validation covered in [Factual Validation Convention](./factual-validation.md)
- **Code examples in README** - Code quality covered in development conventions
- **App-specific content** - Covered in app-specific content conventions (e.g., [Programming Language Content Standard](../tutorials/programming-language-content.md))
- **OSS compliance** - License, contribution guidelines covered in [OSS Documentation Convention](./oss-documentation.md)

## Motivation

This project aims to make Sharia-compliant enterprise solutions accessible to organizations worldwide. By creating an open-source platform...
```

**PASS: Good** (problem → solution):

```markdown
## Motivation

**The Challenge**: Organizations worldwide need enterprise software that respects Islamic principles, but most solutions treat Sharia-compliance as an afterthought—bolted on rather than built in.

**Our Solution**: We're building an open-source platform with Sharia-compliance at its core...
```

**Why**: Readers immediately understand the context and relevance instead of having to extract it from a long paragraph.
