# Executor Tagging — [AI] vs [HUMAN] (HARD RULE)

Every delivery checklist item MUST make clear **who can execute it**. Some work cannot be done by an AI agent at all — physical actions (unplug a power cable, swap a drive), out-of-band approvals (approve a production deploy, accept a contract), or actions needing real credentials or authority the agent must not hold. Tagging up front lets the executor hand off to the human cleanly instead of fabricating a completion.

**Tags** (placed at the START of the checkbox, right after `- [ ]`):

- **`[AI]`** — an agent can fully perform the step. **Default**: an unmarked checkbox is treated as `[AI]`.
- **`[HUMAN]`** — only a human can do it (physical action, out-of-band approval/sign-off, real-secret or privileged-credential handling, real-world authority).
- **`[AI+HUMAN]`** (optional) — agent prepares/drafts; human reviews, approves, or performs the irreversible final action.

**Required legend** — open `delivery.md` (or a single-file plan's Delivery Checklist section) with:

```markdown
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
```

**Default bias (prefer `[AI]`, HARD RULE)**: use `[AI]` as much as possible and `[HUMAN]` as little as possible. Reserve `[HUMAN]` for what is genuinely inevitable — impossible or unsafe for an agent, or requiring real-world authority or credentials an agent must not hold — OR for steps the user or plan has explicitly asked to keep `[HUMAN]`. A sanctioned channel that lets an agent do something seemingly human-only (e.g. copying a real secret via an `[AI]`-authored script through the `guard-env-file-access` path) stays `[AI]` — document the channel inline. When both an `[AI]` and a `[HUMAN]` path would accomplish the step, choose `[AI]`.

**Git-mechanical steps are `[AI]` (HARD RULE)**: provision the worktree (`git worktree add …`), commit, push (to `origin main` for `*-to-origin-main` modes, or to the PR branch for `*-to-pr` modes), and remove the worktree (`git worktree remove …`) are git-mechanical steps the agent performs directly — always tag them `[AI]`, never `[HUMAN]`. For the default `worktree-to-pr` mode, do **not** author a `[HUMAN]` "review the diff and approve push" gate for the push itself — pushing to the PR branch is `[AI]`, and so is the final PR merge to `main`, once the hardened preconditions hold and the PR-Review Maker→Fixer Cycle has completed (per [delivery-mode.md](delivery-mode.md)). Author a `[HUMAN]` merge step only where the plan explicitly opts into that gate. See [Git Push Default Convention](../../../../repo-governance/development/workflow/git-push-default.md).

**Execution semantics**: the [plan-execution workflow](../../../../repo-governance/workflows/plan/plan-execution.md) STOPS at a `[HUMAN]` item, surfaces it with the acceptance criterion, and waits for the human to confirm before continuing. This is a legitimate stop that overrides "never stop between phases".

See [Plans Organization Convention §Executor Tagging](../../../../repo-governance/conventions/structure/plans/executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule) for the authoritative rule.
