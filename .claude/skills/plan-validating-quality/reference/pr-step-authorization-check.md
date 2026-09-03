# PR Step Authorization Check

Authoritative source:
[Plans Organization Convention §Delivery Mode](../../../../repo-governance/conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode).

A PR-creation step is **expected and correct** when the plan's resolved Delivery Mode is
`worktree-to-pr` (default) or `main-to-pr` — validate via rule 19 (Step 5m) instead (exact-head/base
PR CI present, merge tag correct). Flag **HIGH** a PR-creation step on a plan resolved to
`worktree-to-origin-main` or `main-to-origin-main` (direct-push) — remove the step or correct the
mode. Executing inside a worktree does not by itself select a mode either way — only the resolved
Delivery Mode is the authorizing signal.

**Phase 0 Never Opens a PR — mode-independent (HIGH)**. Authoritative source:
[Plans Organization Convention §Phase 0 Opens No PR](../../../../repo-governance/conventions/structure/plans/phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).
Flag **HIGH**, regardless of mode, any of the following inside `## Phase 0` (steps, sub-bullets, or
its Gate): a PR-creation step; a branch-push step to any target; a semantic-review step
or completion reference; a merge step, `gh pr ready` step, or post-push CI-verification step. A
`*-to-pr` mode authorizes PR steps only at delivery boundaries — Phase 0 produces nothing reviewable,
so the earliest PR-opening phase is Phase 1, and only if Phase 1 is a declared boundary. Also flag
**HIGH** a Per-Phase Integration Protocol block not scoped to Phase 1 onward.

Remediation: delete the offending step; if Phase 0 wrote evidence artifacts, note they land through
the first change-producing unit's mode-specific integration; if Phase 0 genuinely produces
reviewable changes, flag it as mis-scoped and move the work to Phase 1.

**Detection command** (from the plan folder; Phase 0 slice only):

```bash
awk '/^## Phase 0/{f=1} /^## Phase 1/{f=0} f' delivery.md \
  | grep -nEi 'gh pr create|gh pr ready|open (a )?(draft )?pr|create pr|git push|push to origin|pr-review|semantic review|merge(d)? (the )?PR' \
  | grep -c .
```

Acceptance: returns `0`. Falsifiable both ways: a `gh pr create --draft` line inside Phase 0 makes it
return `1`. Read the printed number (don't `&&`-chain — `grep -c` exits 1 on zero count). Single-file
plan: substitute `README.md`.

## No PR Outside a Declared Delivery Boundary (HIGH)

Flag **HIGH** any PR-creation, explicitly requested semantic-review, `gh pr ready`, merge, or post-push CI-verification
step in a phase not declared a boundary in `### Delivery Boundaries`.
