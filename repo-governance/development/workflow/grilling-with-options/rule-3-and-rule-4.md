---
description: The requirement that every option states a context-specific trade-off, and that exactly one option is marked Recommended.
when_to_use: Use when writing an option's trade-off sentence or deciding which single option to mark Recommended.
---

# Rule 3 and Rule 4 — Trade-Off Per Option; Exactly One Recommended Option

## Rule 3 — Trade-Off Per Option

Each option MUST state its implication or trade-off in one sentence. The trade-off must be
specific to this decision context, not generic filler ("Option A is simpler").

**Good trade-off**: "Adds a new `development/workflow/grilling-with-options.md` convention
— layer-coherent and matches adjacent workflow docs, but requires updating the development/
README."

**Bad trade-off**: "This option is simpler." (non-specific, not actionable)

## Rule 4 — Exactly One Recommended Option

Exactly one option MUST be marked as Recommended with a one-line rationale grounded in the
specific context (repo state, existing conventions, the user's stated constraints). Marking
more than one option Recommended is forbidden — if two options are genuinely equal, the
agent must choose one based on context.

**Rationale**: An agent that refuses to recommend abdicates its expertise. Users engage with
AI agents precisely to get a grounded recommendation, not just a menu.
