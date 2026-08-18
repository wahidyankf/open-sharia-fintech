---
title: "Governance Vendor-Independence Convention"
description: Governance prose must be vendor-neutral. Vendor-specific bindings belong in platform-binding directories, not in repo-governance/.
when_to_use: Use when writing or reviewing repo-governance/, AGENTS.md, or CLAUDE.md prose and checking it stays vendor-neutral.
category: explanation
subcategory: conventions
tags:
  - conventions
  - governance
  - vendor-independence
  - agents
  - platform-bindings
created: 2026-05-02
---

# Governance Vendor-Independence Convention

All prose under `repo-governance/` must be readable and actionable by any contributor — human or agent — regardless of which AI coding platform they use. Vendor-specific implementation details belong in dedicated platform-binding directories, not in the governance layer.

## Principles Implemented/Respected

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: One clear rule (governance is vendor-neutral) is easier to apply consistently than per-file exceptions.
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: The allowlist mechanism makes every vendor reference deliberate and visible.
- **[Accessibility First](../../principles/content/accessibility-first.md)**: Broadly read — governance should be accessible to contributors using any tool or no tool.
- **[Documentation First](../../principles/content/documentation-first.md)**: The rule is codified here before bulk rewriting begins so writers have a stable reference.

## Children

- [Purpose and Scope](./governance-vendor-independence/01-purpose-and-scope.md) — why governance prose must be vendor-neutral and exactly which files this convention governs vs. exempts.
- [Forbidden Vendor Terms — Product Names and Paths](./governance-vendor-independence/02-forbidden-vendor-terms-names-and-paths.md) — forbidden coding-agent product names, binding directory paths, and model-vendor company names.
- [Forbidden Vendor Terms — Models and Branded Concepts](./governance-vendor-independence/03-forbidden-vendor-terms-models-and-concepts.md) — forbidden model names and branded concepts, plus the combined audit regex and false-positive notes.
- [Allowlist Mechanism](./governance-vendor-independence/04-allowlist-mechanism.md) — the two mechanisms (binding-example fences, Platform Binding Examples heading) that permit vendor references.
- [Vocabulary Map](./governance-vendor-independence/05-vocabulary-map.md) — vendor-specific terms mapped to their vendor-neutral equivalents.
- [Platform Binding Directory Pattern, and Migration Guidance](./governance-vendor-independence/06-platform-binding-directory-pattern-and-migration.md) — the per-platform binding-directory catalog and the file-refactoring process.
- [Enforcement, and Exceptions and Escape Hatches](./governance-vendor-independence/07-enforcement-and-exceptions.md) — how the audit is run, what it respects, and the explicit list of permitted exceptions.

## Related Conventions

- [File Naming Convention](../structure/file-naming.md) — Kebab-case file naming
- [Plans Organization](../structure/plans.md) — How plans are structured
- [Platform Bindings Catalog](../../../docs/reference/platform-bindings.md) — Full catalog of all platform bindings

## Conventions Implemented/Respected

- **[File Naming Convention](../structure/file-naming.md)**: This file uses kebab-case.
- **[Linking Convention](../formatting/linking.md)**: All cross-references use GitHub-compatible markdown with `.md` extensions.
- **[Content Quality Principles](../writing/quality.md)**: Active voice, proper heading hierarchy, single H1.
