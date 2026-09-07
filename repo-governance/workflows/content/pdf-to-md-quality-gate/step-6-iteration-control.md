---
description: "Step 6: the iteration-control logic tracking consecutive-zero counts and consecutive-zero-fixes to decide pass, partial (stagnation exit), or loop back."
when_to_use: "Use when implementing or debugging the loop/termination decision logic between checker and fixer iterations."
---

# 6. Iteration Control (Sequential)

Determine whether to continue or finalize.

**Logic**:

- Track `consecutive_zero_count` across iterations (resets to 0 when threshold-level findings > 0,
  increments when = 0)
- Track `consecutive_zero_fixes` across iterations: read `**Applied (HIGH_CONFIDENCE)**: A` from
  the most recent fix report. Increment when `A = 0`. Reset to 0 when `A > 0`. No fix report this
  iteration (e.g. iteration ran no fixer) leaves the counter unchanged.
- If `consecutive_zero_fixes >= 2`: Proceed to step 7 (**partial** — stagnation exit). Two
  back-to-back fixer runs that applied nothing prove the remaining findings are deterministically
  manual-only; further iteration is wasted work.
- If `consecutive_zero_count >= 2` AND iterations >= min-iterations (or min not provided): Proceed
  to step 7 (double-zero confirmed — **pass**)
- If `consecutive_zero_count >= 2` AND iterations < min-iterations: Loop back to step 5
  (Re-validate to satisfy min-iterations)
- If `consecutive_zero_count < 2` AND threshold-level findings = 0: Loop back to step 5
  (confirmation check — no fix needed, just re-verify)
- If threshold-level findings > 0 AND max-iterations provided AND iterations >= max-iterations:
  Proceed to step 7 (**partial**)
- If threshold-level findings > 0 AND (max-iterations not provided OR iterations < max-iterations):
  Loop back to step 4 (Apply Fixes)

**Below-threshold findings**: Reported in audit but don't affect iteration logic.

**Notes**:

- **Consecutive pass requirement**: Zero findings must be confirmed by a second independent check
  before declaring success
- **Stagnation exit**: When the fixer applies zero `HIGH_CONFIDENCE` fixes on two consecutive
  iterations, the orchestrator terminates `partial` rather than burning the remaining
  max-iterations budget on a deterministic no-op. The fix report's
  `**Applied (HIGH_CONFIDENCE)**: A` line is the canonical signal — no new schema needed.
- **Why two iterations, not one**: A single `Applied=0` could indicate transient causes (crane
  subprocess error, partial fixer crash recovered by retry, race with a concurrent skip-list
  write). Requiring TWO consecutive zero-applied iterations distinguishes deterministic-skip
  stagnation from transient failure. Cost: one extra checker+fixer invocation in the worst
  case (mitigated by the carry-forward audit in Step 5 when `changed_sections` is empty).
  Benefit: no false `partial` exit on transient errors.
- Escalation warning logged at iteration 5 if not converging
- Default max-iterations: 7
