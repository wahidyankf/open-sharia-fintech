---
description: "Step 5: re-runs all checkers and applies the consecutive-zero-count loop logic to decide continue vs. finalize."
when_to_use: "Use when implementing or debugging the loop/termination decision logic between checkers and fixers."
---

# 5. Iteration Control (Sequential)

Determine whether to continue fixing or finalize.

**Logic**:

- Re-run all checkers (step 1) with `{step4.outputs.updated-lifecycle-evidence}`; keep delegated
  predicates filtered
- Count findings based on mode level (same as Step 2):
  - **lax**: Count CRITICAL only
  - **normal**: Count CRITICAL + HIGH
  - **strict**: Count CRITICAL + HIGH + MEDIUM
  - **ocd**: Count all levels
- Track `consecutive_zero_count` across iterations (resets to 0 when threshold-level findings > 0, increments when = 0)
- If consecutive_zero_count >= 2 AND iterations >= min-iterations (or min not provided): Proceed to step 6 (Success — double-zero confirmed)
- If consecutive_zero_count >= 2 AND iterations < min-iterations: Loop back to step 1 (re-validate)
- If consecutive_zero_count < 2 AND threshold-level findings = 0: Loop back to step 1 (confirmation check — no fix needed, just re-verify)
- If threshold-level findings > 0 AND max-iterations provided AND iterations >= max-iterations: Proceed to step 6 (Partial)
- If threshold-level findings > 0 AND (max-iterations not provided OR iterations < max-iterations): Loop back to step 3

**Below-threshold findings**: Continue to be reported in audit but don't affect iteration logic

**Depends on**: Step 4 completion

**Notes**:

- **Default behaviour**: Runs up to 7 iterations (default max-iterations). Override with higher value for more attempts
- **Consecutive pass requirement**: Zero findings must be confirmed by a second independent check before declaring success
- **Optional min-iterations**: Prevents premature termination before sufficient iterations
- Each iteration uses the latest audit reports from all validators
- Tracks iteration count for observability
- **Broken links block zero-finding achievement** (no auto-fix available)
