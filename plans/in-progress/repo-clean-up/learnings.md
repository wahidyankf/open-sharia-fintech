# 📓 Learnings — Repository Clean-Up

_Captured during execution. Empty sections are filled as each phase completes._

## Captured Before Execution

**A dormant tool hides the gap it was supposed to fill.** Both CLIs were believed to cover their
content trees. The `md-links` gate excluded exactly those trees on that belief. Neither CLI had run
in months, so the exclusion was load-bearing for nothing — the trees were unchecked and the board was
green. Deleting dead code is the cheap half; noticing what its existence was excusing is the
valuable half.

**"Leftover from the old stack" was wrong, and checking mattered.** The initial reading was that
these were Hugo-era leftovers. They were not: both were deliberately ported Go→Rust in 2026-05.
Acting on the assumption would have produced a correct decision from a false premise, and the plan
would have recorded the false premise as its justification.

**Test-fixture strings look like real references.** Four `apps/rhino-cli/**` files name the deleted
paths. All four are `TempDir` fixtures or doc comments. A grep-driven cleanup would have "fixed"
them and opened a four-repo parity propagation obligation for zero functional change.

## Captured During Execution

_To be filled._

## Follow-Ups Filed

_To be filled._
