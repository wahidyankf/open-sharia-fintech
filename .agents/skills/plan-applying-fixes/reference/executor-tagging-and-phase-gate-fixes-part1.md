# Executor-Tagging and Phase-Gate Fixes (Part 1)

## Executor-Tagging and Phase-Gate Fixes (Step 5h Findings)

Per
[Plans Organization Convention §Execution Markers](../../../../repo-governance/conventions/structure/plans/executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule)
and
[§Phase Gates and Natural Pauses](../../../../repo-governance/conventions/structure/plans/phases-as-natural-pauses.md#phases-as-natural-pauses-with-clear-gates-hard-rule).

**1. Missing Executor Legend** — **HIGH**: insert the canonical legend as the first lines of
`delivery.md` (before `## Worktree`), or at the top of a single-file plan's Delivery Checklist:

```markdown
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
```

**2. Human-Only Step Tagged `[AI]`** — **HIGH** when unambiguously human-only (physical action,
out-of-band approval, real-credential handling outside a sanctioned `[AI]` channel): prepend
`[HUMAN]`, phrase the acceptance criterion as a human confirmation. **MEDIUM** when it's unclear
whether a sanctioned `[AI]` channel exists — don't guess.

**3. Over-Tagged `[HUMAN]` Mechanical Step** — **HIGH** when a file edit, shell command, or grep is
tagged `[HUMAN]` with no justification: retag `[AI]`. **FALSE_POSITIVE** when the plan documents a
real reason (a sanctioned-channel exception explicitly declined). The three git-mechanical lifecycle
steps are the most common over-tags — retag each `[AI]` at **HIGH**:
`[HUMAN] Create worktree: git worktree add …` → `[AI]`;
`[HUMAN] Review the diff and approve push …` → rewrite as `[AI] Commit and push to origin
<pr-branch>` (default `worktree-to-pr`) or `[AI] Commit and push to origin main` (direct-push) —
drop the approve-push gate either way, pushing to a PR branch is not a merge;
`[HUMAN] Remove the worktree: git worktree remove …` → `[AI]`.

**Never apply this recipe to a merge step.** The PR merge is a separate step from the push; `[AI]`
is its default actor, and a `[HUMAN]` tag on it is itself the legitimate opt-in — the tag IS the
declaration, no separate field to check. See the merge-step guard in
`01-merge-step-guard.md`. Retagging a declared `[HUMAN]` merge step to `[AI]` — or
rewriting it into a direct push to `origin main` — would strip a deliberate gate and bypass the PR
entirely. **FALSE_POSITIVE** only when the user's prompt or the plan explicitly requested an
out-of-band sign-off for that change.

**4. Missing `### Phase N Gate`** — **HIGH**: append a gate derived from that phase's work items:

```markdown
### Phase N Gate

> All checks below must pass before starting Phase N+1.

- [ ] [AI] `<verification command derived from a phase work item>` — <acceptance>

> **Pause Safety**: <coherent state after this phase>. Safe to stop. To resume: `<re-verify command>`.
```

If work items lack concrete acceptance criteria to derive gate checks from, classify **MEDIUM**
rather than inventing verification commands.

**5. Missing Pause Safety Note** — **HIGH** when a gate exists but has no following
`> **Pause Safety**:` blockquote — add one stating the safe-to-stop state and the resume command,
derived from the phase's effect. **MEDIUM** if the end-state cannot be confidently summarized.
