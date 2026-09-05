---
title: "Quality Checklist"
description: The full pre-publish checklist covering production readiness, standard-library-first, code quality, structure, diagrams, framework integration, and frontmatter.
when_to_use: Use as a final checklist before publishing an In-the-Field guide.
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - in-the-field
  - education
  - production-ready
created: 2026-02-04
---

# Quality Checklist

Before publishing in-the-field content, verify:

## Production Readiness

- [ ] Code includes comprehensive error handling
- [ ] Resource management with try-with-resources
- [ ] Logging at appropriate levels
- [ ] Security practices (input validation, secret management)
- [ ] Configuration externalized (no hardcoded values)
- [ ] Integration tests demonstrating framework usage

## Standard Library First

- [ ] Built-in approach shown before framework
- [ ] Limitations of standard approach explained
- [ ] Framework justification provided
- [ ] Trade-offs discussed (complexity vs capability)
- [ ] When to use each approach clarified

## Code Quality

- [ ] Annotation density meets target PER CODE BLOCK (1.0-2.25 comment lines per code line)
- [ ] `// =>` or `# =>` notation shows framework behaviour
- [ ] Configuration impact documented
- [ ] Integration points explained
- [ ] Security implications noted
- [ ] Performance characteristics documented

## Guide Structure

- [ ] Why It Matters section present (2-3 paragraphs)
- [ ] Standard library approach shown first
- [ ] Production framework introduced with rationale
- [ ] Best practices section included
- [ ] Trade-offs and when-to-use guidance provided
- [ ] Diagrams for complex patterns (when appropriate)

## Diagrams

- [ ] 10-20 total diagrams across all guides (25-50% of guides)
- [ ] Diagrams use color-blind friendly palette
- [ ] Architecture, flow, and integration patterns visualized
- [ ] No diagrams for simple linear processes

## Framework Integration

- [ ] Framework selection justified
- [ ] Installation/setup steps provided
- [ ] Dependency versions specified (not LATEST)
- [ ] Configuration for production documented
- [ ] Links to framework documentation

## Frontmatter

- [ ] Title descriptive and specific
- [ ] Description clear and concise
- [ ] Weight assigned logically
- [ ] Tags include language + topic + frameworks
