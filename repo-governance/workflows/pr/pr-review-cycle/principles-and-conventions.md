---
description: "The five principles (Explicit Over Implicit, Root Cause Orientation, Accessibility First, No Time Estimates, Simplicity Over Complexity) and five conventions this workflow implements."
when_to_use: "Use when auditing this workflow's principle/convention compliance, or tracing which convention governs a specific formatting choice (file naming, linking, diagrams)."
---

# Principles and Conventions Implemented/Respected

## Principles Implemented/Respected

- PASS: **Explicit Over Implicit**: the loop's cycle count, gate conditions, done-definition, and
  escalation rules are all stated explicitly rather than left to agent judgment.
- PASS: **Root Cause Orientation**: the fixer applies real fixes (or cites a reasoned rejection) per
  thread rather than suppressing findings; escalation surfaces repeated disagreement to a human
  instead of silently dropping it.
- PASS: **Accessibility First**: findings carry cited evidence and clear severity labels; diagrams in
  this document use the repo's color-blind-friendly palette.
- PASS: **No Time Estimates**: the loop is bounded by cycle count and gate conditions, not by
  duration.
- PASS: **Simplicity Over Complexity**: a fixed sequential loop with one hard gate (CI-green) between
  cycles, rather than an open-ended or parallel review process.

## Conventions Implemented/Respected

- **[File Naming Convention](../../../conventions/structure/file-naming.md)**: workflow file uses
  lowercase kebab-case.
- **[Linking Convention](../../../conventions/formatting/linking.md)**: all cross-references use
  GitHub-compatible markdown with `.md` extensions.
- **[Content Quality Principles](../../../conventions/writing/quality.md)**: active voice, proper
  heading hierarchy, single H1.
- **[Diagram and Schema Convention](../../../conventions/formatting/diagrams.md)**: diagrams use
  `sequenceDiagram` and `flowchart LR`, the color-blind-friendly palette, and a documented
  color-scheme comment.
- **[Plans Organization Convention §Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode)**:
  this workflow implements the `*-to-pr` modes' review-cycle and done-definition requirements defined
  by that convention.
- **[Executor Tagging](../../../conventions/structure/plans/executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule)**:
  the merge actor is explicit — `[AI]` by default, `[HUMAN]` only where a plan says so — so the
  AI/human executor boundary stays legible rather than assumed.
