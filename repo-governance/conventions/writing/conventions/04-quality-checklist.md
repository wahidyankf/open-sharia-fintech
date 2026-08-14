---
title: "Convention Writing Convention — Quality Checklist"
description: The completeness, clarity, usability, convention-compliance, integration, and accessibility checks to run before publishing a convention document.
when_to_use: Use immediately before publishing or merging a new or updated convention document.
category: explanation
subcategory: conventions
tags:
  - meta
  - conventions
  - standards
  - documentation
created: 2025-12-07
---

# Quality Checklist

Before publishing a convention document, verify:

## Completeness

- [ ] Has all required sections (frontmatter, introduction, Principles Implemented/Respected, purpose, scope, standards)
- [ ] Principles Implemented/Respected section lists ALL relevant principles with links and explanations
- [ ] Includes concrete examples (not just abstract rules)
- [ ] Cross-references related conventions
- [ ] Specifies what is OUT of scope (prevents confusion)

## Clarity

- [ ] Uses clear, imperative language ("Use X", not "You could use X")
- [ ] Defines all technical terms or links to definitions
- [ ] Examples show both correct PASS: and incorrect FAIL: usage
- [ ] Rationale provided for non-obvious rules

## Usability

- [ ] Scannable structure (headings, lists, tables)
- [ ] Code blocks use proper syntax highlighting
- [ ] Tables formatted correctly
- [ ] Links work and use relative paths with `.md` extension

## Convention Compliance

- [ ] Follows [File Naming Convention](../../formatting/linking.md) — Relative paths with `.md`
- [ ] Follows [Content Quality Principles](../quality.md) — Active voice, single H1, etc.
- [ ] YAML frontmatter uses 2 spaces for indentation

## Integration

- [ ] Referenced in `repo-governance/conventions/README.md`
- [ ] Mentioned in AGENTS.md if it affects agent behavior
- [ ] Used by at least one agent OR enforced in a hook/process
- [ ] Cross-referenced by related conventions

## Accessibility

- [ ] Diagrams use color-blind friendly palette ([Color Accessibility Convention](../../formatting/color-accessibility.md))
- [ ] Images have alt text
- [ ] Acronyms defined on first use
- [ ] Clear hierarchy (proper heading nesting)
