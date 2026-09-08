---
description: The core principles this convention implements — Documentation First, Explicit Over Implicit, Simplicity Over Complexity, Accessibility First, and Progressive Disclosure.
when_to_use: Use when you need the rationale behind the README/specs split and PM-readability contract.
---

# Principles Implemented/Respected

This convention implements the following core principles:

- **[Documentation First](../../../principles/content/documentation-first.md)**: The split makes documentation a deliberate, maintained artifact rather than content that accumulates wherever it is written first. Specs are the canonical record of what the system does.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: The two-category mapping table eliminates judgment calls. Every piece of content belongs to exactly one category, with explicit rules for splitting mixed content.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: App READMEs become thin, focused entry points. Specs become complete, organized references. Neither has to carry both roles.

- **[Accessibility First](../../../principles/content/accessibility-first.md)**: The PM-readability contract calibrates glossing precisely — niche terms get plain-language notes on first use; mainstream SWE vocabulary does not. Over-glossing is patronizing noise; under-glossing bars non-specialist readers.

- **[Progressive Disclosure](../../../principles/content/progressive-disclosure.md)**: The app README carries a single pointer into `specs/`. The specs tree structures content by zoom level (C4 L1 → L2 → L3) so readers can drill as far as they need.
