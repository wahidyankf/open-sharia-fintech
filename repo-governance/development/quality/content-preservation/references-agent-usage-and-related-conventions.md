---
title: "References, Agent Usage, and Related Conventions"
description: "References, which agents use this convention, and related conventions."
category: explanation
subcategory: development
tags:
  - content-preservation
  - condensation
  - offload
  - zero-loss
  - documentation
created: 2025-12-14
when_to_use: "Use when you need a related convention or the agents that apply this one."
---

# References, Agent Usage, and Related Conventions

## References

- [Convention Writing Convention](../../../conventions/writing/conventions.md) - How to write convention documents (target for offloaded content)
- [AI Agents Convention](../../agents/ai-agents.md) - Agent standards (agents apply content preservation principles)
- [Trunk Based Development Convention](../../workflow/trunk-based-development.md) - Git workflow example of development convention
- [File Naming Convention](../../../conventions/structure/file-naming.md) - Example of content convention

## Agent Usage

### rules-maker

When condensing files or extracting duplications, `rules-maker` must:

1. Follow the offload decision tree
2. Choose appropriate option (A/B/C/D)
3. Use correct folder (conventions/ or development/)
4. Complete all verification checklist items
5. Confirm zero content loss

### rules-checker

When validating condensation, `rules-checker` must verify:

- Content was MOVED (not deleted)
- Target convention/development doc exists and is indexed
- Links are correct with `.md` extension
- Correct folder choice (conventions/ vs development/)
- No unique content lost

### docs-maker

When creating new convention or development documents during offload, `docs-maker` must:

- Place files in the correct subdirectory (`conventions/` or `development/`) with lowercase kebab-case filenames
- Include comprehensive content from source
- Add frontmatter with appropriate subcategory
- Update index files

## Related Conventions

- [AI Agents Convention](../../agents/ai-agents.md) - Agent complexity tiers and condensation
- [Convention Writing Convention](../../../conventions/writing/conventions.md) - How to structure convention documents
