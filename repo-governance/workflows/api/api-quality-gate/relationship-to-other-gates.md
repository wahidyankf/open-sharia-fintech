---
description: How the API quality gate's surface-conditional applicability and merge-precondition status relate to the UI gates and PR review.
when_to_use: Use when determining whether a plan must run the API quality gate, the UI gates, both, or neither.
---

# Relationship to Other Gates

This gate is **surface-conditional**: it applies to a plan that ships an API or backend surface. A
UI-bearing plan runs the two UI gates instead; a plan bearing both runs both.

A plan bearing neither of those two surfaces is **not thereby exempt** — that is the routing table
running out, not the rule ending. If it still changes behaviour a user or caller can reach (a CLI, a
library, a hook, a CI workflow), it exercises that behaviour through its own interface and records
what was run. Exemption belongs only to a plan with no reachable behavioural delta at all, and it
**states that exemption explicitly** in its `tech-docs.md` rather than leaving it implicit. See
[PR Merge Protocol](../../../development/workflow/pr-merge-protocol.md) and
[Surface-Conditional Tester Gates](../../plan/plan-planning/surface-conditional-tester-gates.md#surface-conditional-tester-gates), which
this paragraph must stay congruent with.

It is also a **merge precondition** for every applicable API-bearing delivery. A `partial`, `fail`,
or pending lifecycle result blocks merge under the [PR Merge Protocol](../../../development/workflow/pr-merge-protocol.md).
