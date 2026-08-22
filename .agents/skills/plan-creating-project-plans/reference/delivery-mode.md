# Delivery Mode (Mandatory — Applies to ALL Plans)

Every plan resolves to exactly one **delivery mode** before execution begins, declared alongside the `## Worktree` / `## Worktree Specification` section (see [worktree-specification.md](worktree-specification.md)). Delivery mode is a sibling concern to the worktree declaration: the worktree fixes the **work location**; delivery mode additionally fixes the **integration target** and **merge authority**.

**The four modes** (full table and precedence algorithm: [Plans Organization Convention §Delivery Mode](../../../../repo-governance/conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode)):

- **`worktree-to-pr`** — **the default** when no mode is otherwise specified. Work in `worktrees/<plan-identifier>/`, draft PR opened against `main`, `[AI]` merges once the hardened preconditions hold (a `[HUMAN]` merge gate applies only where the plan's own step says so).
- **`worktree-to-origin-main`** — work in the worktree, direct push to `origin main`, `[AI]` pushes directly.
- **`main-to-origin-main`** — primary checkout (no worktree), direct push to `origin main`, `[AI]` pushes directly.
- **`main-to-pr`** — primary checkout (no worktree), PR opened against `main`, `[AI]` merges once the hardened preconditions hold (a `[HUMAN]` merge gate applies only where the plan's own step says so).

**Per-Repository Delivery Mode Restrictions (HARD RULE)**: the two direct-push modes above are not
freely selectable in every repo. `main` is branch-protected (including for admins) in `ose-public`,
so neither direct-push mode has an executable path there — `worktree-to-pr` is
**mandatory**, not merely the safest default. Only `ose-private` retains a
narrow surviving exception, and only for a genuinely infrastructure-as-code plan. See [Plans
Organization Convention §Per-Repository Delivery Mode Restrictions (HARD RULE)](../../../../repo-governance/conventions/structure/plans/per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule)
for the full per-repo table and enforcement detail.

`worktree-to-pr` is mandatory in `ose-public` — it is the safest choice everywhere
else too, absent a reason to pick another mode in the one repo (`ose-private`) where an alternative
is actually available.

**Declare it explicitly**: `## Delivery Mode: worktree-to-pr` (or one of the other three modes, subject to the restriction above), placed immediately alongside the `## Worktree` declaration. An unmarked plan resolves to the tier-3 default (`worktree-to-pr`) per the three-tier precedence algorithm (invocation argument → plan field → default).

**Every PR uses the behavior classifier**: for `worktree-to-pr` and `main-to-pr`, the delivery checklist records the [PR-Review Maker→Fixer Cycle workflow](../../../../repo-governance/workflows/pr/pr-review-quality-gate.md). Eligible executable work runs the sequential reviewer pipeline to the earliest clean code M/H/C result within the seven-cycle maximum; noneligible static work requires the named `pr-quality-gate.yml` workflow. **A PR touching `plans/**`is always eligible** — plan documents run the specialist loop AND the quality gate by default, waived only by an explicit user instruction on that PR. The merge sits outside this done-boundary and`[AI]` merges once hardened preconditions hold.

**Invalid values are a finding, never silently coerced**: a delivery-mode value that is not one of the four modes above is a `plan-checker` HIGH finding, not a silent fallback to the default.
