---
description: The procedure for rendering a 3-4-leaf decision envelope through a native tool limited to 2-3 options, via branch groups, plus the markdown fallback for non-interactive roots.
when_to_use: Use when a native interactive tool's option limit is smaller than the number of substantive leaves in a decision envelope.
---

# Staged Native Rendering

When a native tool can display only 2–3 substantive options while a decision envelope contains
3–4 substantive leaves, the root MUST render a complete staged decision tree rather than trimming
the envelope. This procedure applies to Claude, Codex, and every other native tool with that
effective limit:

1. Retain every original leaf, its stable ID, trade-off, and the one recommendation in the envelope.
2. Partition the leaves into two named branch groups: one leaf versus the remaining two for three
   leaves, or two leaves versus two leaves for four. Each root-stage label and description MUST name
   every leaf it contains; a grouped branch is navigation, never a collapsed or selected outcome.
3. Render the two branch groups plus **"Let's chat about this"**. The tool-provided free-form
   **"Other"** entry remains the type-your-own blank state. The root-stage recommendation identifies
   the recommended branch and gives its context-grounded rationale.
4. After the user selects a group containing multiple original leaves, render those leaves as the
   next single-choice question, again with chat and type available and exactly one context-grounded
   recommendation. If the selected group contains one original leaf, it is terminal: record that
   original leaf ID immediately and do not pose a singleton follow-up. Continue staging only when a
   selected group has multiple leaves; a write-in that creates a new branch follows Rule 7 before
   continuing.
5. Record the final original leaf ID through the `selected_option` form in the Resolved User
   Decisions Envelope. Every original leaf MUST remain reachable exactly once; the root MUST NOT
   omit, silently collapse, auto-select, or reinterpret any leaf to fit a native tool's limit.

The staged UI is a rendering of the exhaustive envelope, not a weaker substitute for it. Chat and
the blank-state type path are required at every rendered stage, and the resulting final leaf remains
subject to the envelope's one-decision, trade-off, and recommendation requirements. Every staged
root renders two branch groups plus Chat at the first stage, and two leaves plus Chat at a multi-leaf
follow-up; its platform binding defines any additional native-tool constraints.

Only a genuinely non-interactive root or harness without a native tool falls back to the
[markdown fallback format](./markdown-fallback-format.md).
