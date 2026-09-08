---
description: Why every PR opens as a GitHub draft, and the four-step lifecycle from draft open through the merge that follows the precondition gate.
when_to_use: Use when opening a PR under worktree-to-pr or main-to-pr, or when deciding whether flipping a PR to ready authorizes merging it.
---

# Draft PR Lifecycle

Per the [Trunk Based Development Convention](../trunk-based-development/why-draft-and-direct-push-modes.md#why-draft-not-ready-for-review-on-open),
every PR opened under `worktree-to-pr` or `main-to-pr` is **opened as a GitHub draft**
(`gh pr create --draft`), not as a ready-for-review PR. This protocol's precondition gate fires at the
moment the AI flips the draft to ready for review (having met the done-definition above), not at PR
open time.

**Lifecycle**:

1. **Draft opened** -- `[AI]` runs `gh pr create --draft --base main ...`. No precondition gate yet. CI may still run on the draft.
2. **Iterate on the branch** -- `[AI]` pushes additional commits and drives exact-current-head PR
   CI plus applicable finite surface gates to green. A semantic review runs only on explicit user
   request. The PR stays in draft status throughout iteration. No merge precondition gate yet.
3. **`[AI]` flips to ready** -- once the done-definition is met, `[AI]` runs `gh pr ready` (or marks it ready in the GitHub UI). **This is where the PR Merge Protocol precondition gate fires.** The agent must:
   - Verify all quality gates have passed (see Quality Gates above).
   - Verify all five preconditions in [The Rule](./the-rule.md#the-rule) hold.
   - Surface the PR status and how each precondition was satisfied.
4. **The merge** -- `[AI]`, once the preconditions hold. This step is outside the AI's done-boundary.

An agent that opens a draft PR is **not** authorized to merge it on readiness alone --
flipping to ready is the deliberate signal that the AI's own work is done, and the merge follows only
from the preconditions, never from the agent's own judgment that the PR looks finished.
