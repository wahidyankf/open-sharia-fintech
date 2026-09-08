---
description: Defines the [AI]/[HUMAN]/[AI+HUMAN] executor tags and the hard-rule bias toward [AI] whenever a step can be engineered as agent-executable.
when_to_use: Use when deciding whether a delivery.md checkbox should be tagged [AI], [HUMAN], or [AI+HUMAN].
---

# Executor Tagging — [AI] vs [HUMAN] (HARD RULE)

Every delivery checklist item MUST make clear **who can execute it**. Some work cannot be done by an AI agent at all — physical actions (unplug a power cable, swap a drive, press a hardware button), out-of-band approvals (approve a production deploy, accept a contract), or actions requiring real credentials or authority the agent must not hold. Marking executor capability up front lets the executor hand off cleanly to the human at the right moment instead of fabricating a completion, and tells the human exactly what they must do personally.

**Tags**:

- **`[AI]`** — an AI agent can fully perform the step (edit files, run commands, call tools). This is the **default**: an unmarked checkbox is treated as `[AI]`.
- **`[HUMAN]`** — only a human can perform the step. Reserve for physical-world actions, out-of-band approvals or sign-offs, actions requiring real secrets or privileged credentials the agent must not access, and decisions requiring real-world authority (legal, financial, safety).
- **`[AI+HUMAN]`** (optional) — AI prepares or drafts; a human reviews, approves, or performs the irreversible final action.

See [Executor Tagging — Git-Mechanical Steps](./executor-tagging-git-mechanical-steps.md) for the bias-to-[AI] rule and the three lifecycle steps most often mis-tagged, and [Executor Tagging — Placement, Legend, and Execution Semantics](./executor-tagging-placement-legend-and-execution-semantics.md) for how the tag is placed and enforced.
