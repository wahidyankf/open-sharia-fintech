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

**A sweep's exception list is the sweep.** The Phase 2 acceptance clause named three exempt roots.
Execution found five more legitimate ones — inert `#[cfg(test)]` fixture strings behind a parity
boundary, another in-progress plan's dated audit ledger, an `assert_no_match` guard that must name
the removed thing to prove its absence, the plan's own prose, and a dated retarget note. Every one
of those would have read as a failure against the written clause, and the tempting fix for each is
to edit the file rather than the clause. The exception list was widened, with a per-root reason,
so a future reader can tell an accepted hit from a missed one.

**Deleting a token can weaken a test.** `infra/dev/beavernest-app/tests/workflow-contract.sh:9`
asserts the stag workflow does _not_ mention `beavernest-app-web`. The sweep flagged it like any
other stale reference. Removing the token would have silently deleted a passing assertion — the
CI-gaming shape, arrived at by mechanical tidying rather than intent.

**Correcting one stale fact surfaces its neighbours.** Fixing a `rust-commons` mention in
`coverage-artifact-relative-paths.md` required reading the sentence around it, which claimed no
`fsharp-crane-core` existed in the repo. It does, along with the exact coverage file that idea says
is absent — which inverts one of its findings. Class sweeps that match on a token never look at the
sentence; the sentence is where the other errors live.

**A count in a plan is an estimate until execution re-runs it.** The plan said 22 courses lacked a
root `overview.md`; the real figure is 23 of 181. Small, but the acceptance clause said "names each
of the 22 directories" — an executor trusting the number would have written a two-pager that failed
its own check.

**Git pathspec globs do not cross `/`.** `git diff --name-only origin/main -- 'apps/*/content'`
returned empty and read as "nothing under content changed". The real answer was one file. A check
that returns empty for the wrong reason is indistinguishable from a passing check. Re-running it as
a full diff piped through `grep 'content/'` gave the true result. Same false-zero class as the
`grep -L` and RTK-trailer traps already recorded.

**The prettier gate is scoped by affected file type, so a docs-only branch can go unformatted.**
Five changed Markdown files failed `prettier --check` with every gate green. Sweeping the branch's
own changed set with the repo-pinned binary is the only thing that catches it.

## Follow-Ups Filed

- [`ayokoding-course-root-overview-parity`](../../ideas/q2-not-urgent-important/ayokoding-course-root-overview-parity.md)
  — 23 of 181 courses lack a course-root `overview.md`; two layouts coexist and cross-course links
  already guessed wrong once. Filed rather than fixed: authoring 23 overview pages is content work.
- [`coverage-artifact-relative-paths`](../../ideas/q2-not-urgent-important/coverage-artifact-relative-paths.md)
  — corrected inline (the `fsharp-crane-core` claim), with the re-adjudication of its conclusion
  left as an open question in the brief itself.
