---
description: Standards for semantic emoji usage to enhance document scannability and engagement with accessible colored emojis
when_to_use: Use when deciding whether, where, or which emoji to use in repository documentation.
---

# Emoji Usage Convention

This document defines conventions for emoji usage in markdown documentation across the Open Sharia Enterprise repository. Emojis serve as **semantic visual markers** that enhance document scannability and engagement while maintaining professionalism.

## In This Convention

- [Principles, Scope, and Purpose](./emoji/principles-scope-and-purpose.md) — What this convention covers and why emojis are used
- [Tasteful Usage: Where Emojis Help and Hurt](./emoji/tasteful-usage-where-emojis-help-and-hurt.md) — Jobs emojis do well versus common anti-patterns
- [Tasteful Usage: Density Cap and Examples](./emoji/tasteful-usage-density-cap-and-examples.md) — Soft density limits and good-vs-bad worked examples
- [Emoji Vocabulary: Document, Status, and Process Markers](./emoji/emoji-vocabulary-document-status-and-process-markers.md) — Standard emojis for document types, status, and process
- [Emoji Vocabulary: Domain-Specific Markers](./emoji/emoji-vocabulary-domain-specific-markers.md) — Standard emojis for technical, enterprise/financial, and AI agent domains
- [Color Accessibility for Colored Emojis](./emoji/color-accessibility-for-colored-emojis.md) — Accessible use of colored square emojis for categorization
- [Emoji Usage Rules 1-6](./emoji/emoji-usage-rules-1-through-6.md) — Consistency, restraint, placement, technical content, accessibility, and frontmatter rules
- [Emoji Usage Rule 7: Scope - Where to Use Emojis](./emoji/emoji-usage-rule-7-scope-where-to-use-emojis.md) — The full allowed-vs-forbidden file scope rule
- [Document Type Specific Guidelines](./emoji/document-type-specific-guidelines.md) — Recommended emojis per document type with worked examples
- [Migration Strategy and Validation Checklist](./emoji/migration-strategy-and-validation-checklist.md) — Phased rollout plan and pre-review checklist

## Related Conventions

- [File Naming Convention](../structure/file-naming.md)
- [Linking Convention](../formatting/linking.md)
- [Diátaxis Framework](../structure/diataxis-framework.md)
- [AI Agents Convention](../../development/agents/ai-agents.md) — For agent color categorization using colored square emojis
- [Color Accessibility Convention](../formatting/color-accessibility.md) — For accessible color palette and WCAG standards

## Notes

### Why These Specific Emojis?

The emoji vocabulary was chosen based on:

1. **Universal recognition** - Emojis with clear, consistent meanings
2. **Professional context** - Appropriate for technical/enterprise documentation
3. **Accessibility** - Screen reader friendly with clear alt text
4. **Render consistency** - Display consistently across platforms (GitHub, VS Code)

### Cultural Considerations

While emojis generally have universal meanings, we've avoided:

- Hand gestures (can have different cultural meanings)
- Flags (potentially political)
- Food/animals (may not render consistently)
- Faces (except for status like PASS: FAIL: ️)

### When in Doubt

If unsure whether to use an emoji:

1. Ask: "Does this emoji add semantic meaning or just decoration?"
2. If decoration → skip it
3. If semantic → check if it's in the vocabulary
4. If not in vocabulary → consider if it should be added (propose via PR/issue)
