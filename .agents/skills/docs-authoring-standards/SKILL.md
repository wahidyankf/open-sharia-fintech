---
name: docs-authoring-standards
description: Repository-specific documentation authoring standards for docs-maker — the correctness/verification checklist, frontmatter template, and the AGENTS.md navigation-document philosophy. Complements the universal docs-applying-content-quality and docs-applying-diataxis-framework skills. Use when creating or editing docs/ content or AGENTS.md.
---

# Authoring Documentation Standards

## Overview

This Skill packages the `docs-maker` agent's repository-specific authoring standards that
aren't covered by the universal quality/framework skills: how to verify accuracy before
publishing, the frontmatter template, and the distinct rules for editing `AGENTS.md`.

## Reference Modules

- [Verification and Correctness](reference/verification-and-correctness.md) — the
  Documentation First principle, verification requirements per information type, and the
  pre-publish correctness checklist
- [Frontmatter, Tags, and AGENTS.md Philosophy](reference/templates-and-agents-md-philosophy.md) —
  the frontmatter template, date-field convention, tag usage, and the AGENTS.md
  navigation-document rules

## Core Principles

- **Correctness is non-negotiable** — verify against source code, tests, and cited external
  sources rather than assumptions.
- **AGENTS.md is navigation, not a knowledge dump** — 3-5 line summaries with links; detail
  lives in `repo-governance/conventions/` or `repo-governance/development/`.
- **Two-tier rule references**: first mention links, subsequent mentions use inline code — see
  [Linking Convention](../../../repo-governance/conventions/formatting/linking.md).

## Related Skills

- `docs-applying-content-quality` — universal active voice, heading hierarchy, accessibility
- `docs-applying-diataxis-framework` — the four documentation categories and their directories
- `docs-creating-accessible-diagrams` — Mermaid diagram standards and accessible palette
