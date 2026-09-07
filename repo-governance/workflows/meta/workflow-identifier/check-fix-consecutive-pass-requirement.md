---
description: Why every *-check-fix workflow requires two consecutive zero-finding validations before declaring success, and its mechanism and iteration-budget impact.
when_to_use: Use when explaining or implementing the double-zero confirmation rule in a *-check-fix workflow.
---

# \*-check-fix Workflow Pattern — Consecutive Pass Requirement

All \*-check-fix workflows require **two consecutive zero-finding validations** before declaring
success. A single zero-finding check is insufficient — the checker must confirm zero findings
on a second independent run before the workflow terminates with `pass`.

**Rationale**: A single zero-finding check may be a false negative. Checker agents operate
non-deterministically — prompt variation, context window limitations, or evaluation order can
cause a checker to miss findings on one run that it catches on the next. Requiring two
consecutive zero-finding checks provides statistical confidence that the content truly meets
the quality standard for the active mode.

**Mechanism**:

- The workflow tracks `consecutive_zero_count` across check iterations
- Each zero-finding check increments the counter; any non-zero check resets it to 0
- Success requires `consecutive_zero_count >= 2`

**Impact on workflow flow**:

- After the first zero-finding check, the workflow loops back to Step 4 (re-validate) — no fix
  is needed, just a confirmation re-check
- If the confirmation check also returns zero findings, the workflow succeeds (double-zero)
- If the confirmation check finds new issues, the counter resets and the workflow loops back to
  Step 3 (fix) — then the cycle continues

**Impact on iteration budget**:

- The minimum iterations to achieve success is **2** (initial zero + confirmation zero), even
  when `min-iterations` is not explicitly set
- Each confirmation re-check counts toward `max-iterations`, so the default `max-iterations: 7`
  allows ample room for fix cycles and confirmation checks
- Workflows with `max-iterations: 1` can never achieve `pass` — they will always terminate
  with `partial` at best

**Applies to all modes**: lax, normal, strict, and ocd all require double-zero confirmation.
No mode is exempt.
