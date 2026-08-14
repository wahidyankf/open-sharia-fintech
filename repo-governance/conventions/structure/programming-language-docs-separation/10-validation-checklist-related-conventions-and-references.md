---
title: "Validation Checklist, Related Conventions, and References"
description: Pre-publish checklists for both docs/explanation/ style guides and ayokoding-www educational content, plus related-convention and platform-documentation references
when_to_use: Read this when doing a final check before publishing programming-language documentation, or looking up a related convention or reference.
category: explanation
subcategory: conventions
tags:
  - documentation
  - programming-languages
  - style-guides
  - content-separation
  - dry-principle
created: 2026-02-04
---

# Validation Checklist, Related Conventions, and References

## Validation Checklist

Before publishing programming language documentation:

### For docs/explanation/ Style Guides

- [ ] README.md includes explicit prerequisite statement linking to ayokoding-www
- [ ] Content focuses on OSE Platform-specific conventions, not language fundamentals
- [ ] No duplication of educational content from ayokoding-www
- [ ] Alignment section links to [Software Engineering Principles](../../../principles/software-engineering/README.md)
- [ ] Cross-references to ayokoding-www for language learning
- [ ] Clear scope: "This is NOT a tutorial, see ayokoding-www"

### For ayokoding-www Educational Content

- [ ] Content covers language fundamentals and generic patterns (0-95% coverage)
- [ ] No OSE Platform-specific conventions (framework choices, naming standards)
- [ ] By-example tutorial follows [By Example Convention](../../tutorials/swe-by-example.md)
- [ ] In-practice guides follow [Programming Language Content Standard](../../tutorials/programming-language-content.md)
- [ ] Optional cross-reference to docs/explanation/ for contributors
- [ ] Clear scope: Generic programming education, not repository-specific

## Related Conventions

**Documentation Organization**:

- [Diátaxis Framework](../diataxis-framework.md) — Four-category documentation organization (docs/ follows this)
- [File Naming Convention](../file-naming.md) — Kebab-case file naming rules
- [Plans Organization](../plans.md) — Project planning structure (not covered here)

**Tutorial Standards**:

- [Programming Language Content Standard](../../tutorials/programming-language-content.md) — Full Set Tutorial Package for programming languages (ayokoding-www follows this)
- [By Example Tutorial](../../tutorials/swe-by-example.md) — Code-first tutorial standards (Component 3 of Full Set)
- [Tutorial Naming](../../tutorials/naming.md) — Tutorial type standards and naming patterns

**Content Quality**:

- [Content Quality Principles](../../writing/quality.md) — Universal quality standards for markdown content
- [README Quality](../../writing/readme-quality.md) — README-specific quality standards

**Principles**:

- [Documentation First](../../../principles/content/documentation-first.md) — Documentation is mandatory, not optional
- [Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md) — Clear separation prevents confusion
- [Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md) — Explicit prerequisite statements
- [Software Engineering Principles Index](../../../principles/software-engineering/README.md) — Software engineering principles that style guides align with

## References

**Platform Documentation**:

- [Software Design Index](../../../../docs/explanation/software-engineering/README.md) — Parent documentation for programming language style guides
- [ayokoding-www](../../../../apps/ayokoding-www/README.md) — Educational programming content platform

**Repository Architecture**:

- [Repository Governance Architecture](../../../repository-governance-architecture.md) — Six-layer architecture (this convention is Layer 2)
- [Conventions Index](../../README.md) — Index of all documentation conventions

**External Resources**:

- [ayokoding.com](https://ayokoding.com/en/learn/software-engineering/programming-languages/) - Live educational platform (public URL)
