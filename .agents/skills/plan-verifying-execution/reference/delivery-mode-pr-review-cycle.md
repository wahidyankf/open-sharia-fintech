# Delivery Mode and PR-Review Cycle Verification (Step 5i)

## 2. Delivery Mode and PR-Review Cycle Verification (Step 5i — MANDATORY)

After the Knowledge Capture blocking gate (Step 5h), verify that execution actually matched the
plan's resolved
[Delivery Mode](../../../../repo-governance/conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode).
For `*-to-pr` modes this replaces the plain-`main` assumption baked into Step 5d (Archival) and Step
5e (Worktree) above: archival lands **inside the delivering PR**, and completion does not require the
PR to be merged.

### What to Validate

1. **Resolved mode matches actual execution** — confirm the mode declared in `delivery.md` (or the
   tier-3 default `worktree-to-pr` if undeclared) matches what actually happened: worktree vs.
   primary-checkout work location, and PR vs. direct-push integration target. A mismatch: **HIGH**
   finding.
2. **For `worktree-to-pr` / `main-to-pr`**:
   - **PR exists** and targets `main` from the plan's branch. Missing: **CRITICAL**.
   - **PR's CI gates are green** on the current head SHA. Not green: **CRITICAL** — plan is not done,
     regardless of other criteria.
   - **Review loop ran** — evidence of the PR-Review Maker→Fixer Cycle (default N=3 sequential
     maker→fixer cycles — a **hard ceiling, not a floor**, never extended and never exited early)
     actually executing. Fewer cycles than the plan specified: **HIGH** — there is no legitimate
     early-exit reason under the hard-ceiling rule. No review-loop evidence at all: **CRITICAL**.
   - **Every thread answered/resolved** — zero unresolved threads, OR each remaining open thread
     carries an explicit escalation-to-`[HUMAN]` note in the PR description. An unresolved thread with
     no reply and no escalation note: **HIGH**.
   - **Archival-in-PR present** — the archival commit (`git mv` to `plans/done/` + README updates) is
     part of the delivering PR's own commit history, not deferred to a separate post-merge commit.
     N/A for repos where the plan folder is not tracked. Missing or post-merge-deferred archival on an
     applicable repo: **HIGH**.
   - **Completion does not require merge** — do NOT file a finding solely because the PR is still
     open/unmerged; a green, fully-reviewed, archival-committed PR awaiting its merge is the correct
     terminal state for this mode.
3. **For `worktree-to-origin-main` / `main-to-origin-main`**: confirm no PR-review-cycle evidence is
   expected (its absence is correct, not a finding) and that the final push landed directly on
   `origin main` with CI green — this reuses Step 5d/5e's existing plain-`main` checks unchanged.
