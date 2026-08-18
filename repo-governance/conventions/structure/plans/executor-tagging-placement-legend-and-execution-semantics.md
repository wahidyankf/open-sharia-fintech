---
title: "Executor Tagging — Placement, Legend, and Execution Semantics"
description: Covers the fourth PR-merge step's default [AI] tagging, where the tag goes in a checkbox, the required top-of-file legend, and how execution stops at a [HUMAN] item.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when adding the executor-tag legend to a delivery.md file or handling a [HUMAN] stop during execution.
---

# Executor Tagging — Placement, Legend, and Execution Semantics

Continues [Executor Tagging — Git-Mechanical Steps](./executor-tagging-git-mechanical-steps.md).

**The PR merge is a fourth, separate step — and it is `[AI]` by default too.** Do not conflate it with the push above. Under `*-to-pr` modes the merge is tagged `[AI]` and happens once the hardened merge preconditions hold; a `[HUMAN]` merge gate applies only where a plan's own step says so explicitly. That opt-in is legitimate and MUST NOT be "corrected" to `[AI]` — the preconditions are identical either way and only the actor differs. See [Delivery Mode](./delivery-mode-the-four-modes.md#delivery-mode) and the [PR Merge Protocol](../../../development/workflow/pr-merge-protocol.md).

**Placement**: the tag goes at the START of the checkbox text, immediately after `- [ ]`:

```markdown
- [ ] [AI] Edit `apps/ose-www/src/server/trpc.ts`: … — acceptance: …
- [ ] [HUMAN] Unplug the power cable to the test rig and confirm the LED is off — acceptance: operator confirms power removed
```

**Legend (required)**: every `delivery.md` (or a single-file plan's Delivery Checklist section) MUST open with a short legend defining the tags it uses and stating that unmarked steps are `[AI]`:

```markdown
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
```

**Default bias**: prefer `[AI]` for anything an agent can mechanically do; reserve `[HUMAN]` for what is genuinely impossible or unsafe for AI. When a sanctioned channel lets an agent do something that looks human-only (for example, copying a real secret via an `[AI]`-authored script through the [`guard-env-file-access`](../../security/env-file-access.md) sanctioned path), it stays `[AI]` — document the channel inline.

**Execution semantics**: when the [plan-execution workflow](../../../workflows/plan/plan-execution.md) reaches a `[HUMAN]` item, it STOPS, surfaces the item to the user with the instruction and the acceptance criterion, and waits for the human to confirm completion before continuing. A `[HUMAN]` step is a legitimate, expected stop — it overrides the "never stop between phases" execution default.

**Enforcement**: `plan-checker` flags as **HIGH** any delivery checkbox describing an action no agent can perform (physical or out-of-band) that is tagged `[AI]` or left unmarked, and flags a missing top-of-file legend as **MEDIUM**. `plan-fixer` adds the legend and corrects mis-tags.
