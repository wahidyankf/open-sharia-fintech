---
title: "Choosing Between conventions/ and development/"
description: "How to decide whether offloaded content belongs in conventions/ or development/."
category: explanation
subcategory: development
tags:
  - content-preservation
  - condensation
  - offload
  - zero-loss
  - documentation
created: 2025-12-14
when_to_use: "Use when deciding where to offload extracted content."
---

# Choosing Between conventions/ and development/

When offloading content, you must choose the appropriate destination folder. Both are valid offload targets with distinct purposes.

## repo-governance/conventions/ - Content and Format Standards

**Focus:** How to write and format documentation

**Examples:**

- File naming, linking, emoji usage
- Diagram formats, color accessibility
- Content quality, mathematical notation
- Tutorials, acceptance criteria
- Documentation organization (Diátaxis)
- Timestamp format

## repo-governance/development/ - Development Processes and Workflows

**Focus:** How to work and process

**Examples:**

- AI agent standards and guidelines
- Commit message conventions
- Git workflow (Trunk Based Development)
- Code review processes
- Testing strategies
- Release management
- CI/CD workflows

## Decision Rule

- **Conventions** = "How to write and format"
- **Development** = "How to work and process"
- **If unclear**, ask: "Is this primarily about content or process?"
