# Delivery Mode Verification (Step 5i continued): Phase 0 and Delivery Boundaries

1. **No PR was opened for Phase 0** — under **every** mode, Phase 0 is Environment Setup and Baseline
   and must not have produced a pull request. Enumerate the plan's PRs and confirm none corresponds to
   Phase 0 — no `…/phase-0` branch, no PR whose title or body scopes it to Phase 0, and no PR whose
   diff contains only baseline evidence artifacts. A PR actually opened for Phase 0: **HIGH**. Also
   confirm the plan's Phase 0 checklist has no ticked PR/push/merge checkbox — a ticked one is the
   same finding with on-disk evidence. See
   [Plans Organization Convention §Phase 0 Opens No PR](../../../../repo-governance/conventions/structure/plans/phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).
2. **PRs match the declared delivery boundaries** — a PR opens at a **delivery boundary**, not at
   every phase. Read the plan's `### Delivery Boundaries` table, then enumerate the PRs actually
   opened. Confirm: (a) each PR corresponds to a declared delivery unit — a PR scoped to an
   intermediate phase is **HIGH**; (b) every declared delivery unit has a PR that **merged** — an
   unmerged unit is **HIGH**; and (c) the count of PRs does not exceed the count of declared
   boundaries. If the plan predates this rule and carries no table, record that as a grandfathering
   note rather than a finding, and check only that no work was left unmerged. See
   [Plans Organization Convention §PRs Open at Delivery Boundaries](../../../../repo-governance/conventions/structure/plans/prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).

### Finding Severity

- A PR was opened, reviewed, or merged for the plan's Phase 0 (any mode): **HIGH**
- A PR was opened for a phase the plan does not declare a delivery boundary: **HIGH**
- A declared delivery unit whose PR never merged: **HIGH**
- `*-to-pr` mode: PR missing: **CRITICAL**
- `*-to-pr` mode: PR's CI gates not green: **CRITICAL**
- `*-to-pr` mode: no review-loop evidence at all: **CRITICAL**
- `*-to-pr` mode: loop exited with a code-related MEDIUM/HIGH/CRITICAL finding outstanding, or hit
  the seven-cycle ceiling with one open (`blocked`): **CRITICAL**
- `*-to-pr` mode: loop ran past the seven-cycle ceiling, last cycle clean: **HIGH**
- `*-to-pr` mode: a low cycle count whose final cycle was clean: **not a finding** (the ceiling is
  not a floor — earliest clean exit is the correct behavior)
- `*-to-pr` mode: unresolved thread with no reply and no `[HUMAN]` escalation note: **HIGH**
- `*-to-pr` mode: archival-in-PR missing or deferred post-merge (where applicable): **HIGH**
- Filing a finding solely because a `*-to-pr` PR remains unmerged: **not a finding** (false positive
  to avoid — flag the CHECK itself as wrong if this occurs)
