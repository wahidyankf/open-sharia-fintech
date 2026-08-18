---
title: "Notes"
description: Why the emoji vocabulary was chosen, cultural considerations avoided, and a decision flow for whether an emoji not in the vocabulary should be added.
when_to_use: Use when deciding whether a new emoji not already in the vocabulary should be proposed for addition.
category: explanation
subcategory: conventions
tags:
  - emoji
  - accessibility
  - scannability
  - conventions
  - markdown
created: 2025-12-04
---

# Notes

## Why These Specific Emojis?

The emoji vocabulary was chosen based on:

1. **Universal recognition** - Emojis with clear, consistent meanings
2. **Professional context** - Appropriate for technical/enterprise documentation
3. **Accessibility** - Screen reader friendly with clear alt text
4. **Render consistency** - Display consistently across platforms (GitHub, VS Code)

## Cultural Considerations

While emojis generally have universal meanings, we've avoided:

- Hand gestures (can have different cultural meanings)
- Flags (potentially political)
- Food/animals (may not render consistently)
- Faces (except for status like PASS: FAIL: ️)

## When in Doubt

If unsure whether to use an emoji:

1. Ask: "Does this emoji add semantic meaning or just decoration?"
2. If decoration → skip it
3. If semantic → check if it's in the vocabulary
4. If not in vocabulary → consider if it should be added (propose via PR/issue)
