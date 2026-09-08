---
description: Introduces the four delivery modes (worktree-to-pr, worktree-to-origin-main, main-to-origin-main, main-to-pr), their work location, integration target, and merge authority.
when_to_use: Use when identifying which of the four delivery modes a plan's work location and integration target correspond to.
---

# Delivery Mode

Every plan resolves to exactly one **delivery mode** before execution begins. The delivery mode
determines where implementation work happens and how it reaches `origin/main`. This is a sibling
concern to [Worktree Specification](./worktree-specification.md#worktree-specification) above: a worktree is a **work
location**, while delivery mode additionally fixes the **integration target** and **merge
authority**.

**The four modes**:

| Mode                           | Work location                  | Integration target             | Merge authority                                       |
| ------------------------------ | ------------------------------ | ------------------------------ | ----------------------------------------------------- |
| `worktree-to-pr` **(default)** | `worktrees/<plan-identifier>/` | Draft PR opened against `main` | `[AI]` — merges once the preconditions hold           |
| `worktree-to-origin-main`      | `worktrees/<plan-identifier>/` | Direct push to `origin main`   | `[AI]` — pushes directly, per Trunk Based Development |
| `main-to-origin-main`          | Primary checkout (no worktree) | Direct push to `origin main`   | `[AI]` — pushes directly, per Trunk Based Development |
| `main-to-pr`                   | Primary checkout (no worktree) | PR opened against `main`       | `[AI]` — merges once the preconditions hold           |

A bare repository (`core.bare=true`) has no primary checkout, so `main-to-origin-main` and
`main-to-pr` are unavailable there — a bare repo has nothing to check code out into directly, and
every mutation flows through a linked worktree instead. See the
[Bare-Repo Base-Worktree Landing Method](../../../development/workflow/bare-repo-landing-method.md) for
the worktree-based procedure that lands changes there. Choosing one of these two modes for a
bare-repo target is an authoring-time correctness error that the three-tier precedence resolver
below does not itself catch — the resolver (and the invalid-value rule following it) validates only
that a value is one of the four mode strings, not repo-topology compatibility, so this is a check
the human or agent declaring the mode must make, not one the algorithm enforces on its own.

`worktree-to-pr` is the **default** when no mode is otherwise specified: it isolates work in a
disposable worktree and routes it through review before it touches `main`, so it is the safest
choice absent a reason to pick another mode.

See [Delivery Mode — main-to-origin-main Content Restriction](./delivery-mode-content-restriction.md) for when direct-push modes are actually valid, and [Delivery Mode — Merge Authority and Resolution Precedence](./delivery-mode-merge-authority-and-precedence.md) for how the active mode is resolved.
