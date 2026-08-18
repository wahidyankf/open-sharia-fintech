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

**A green build can cause a red test.** `nx affected -t build,test:quick,lint` passed; the next
`git push` failed its pre-push `test:quick` on five failures that did not exist minutes earlier.
The build had written `apps/ayokoding-www/.next/standalone/` — flattened copies of `src/`, including
its `*.unit.test.ts` files — and the `unit` project's `**/*.unit.{test,spec}.{ts,tsx}` glob, whose
only exclusion is `node_modules`, then discovered them. They fail because the flattening breaks
their relative imports. Deleting `.next/standalone` cleared it. The lesson is ordering: a gate suite
that runs `build` before `test` in the same tree is not testing the same tree it started with.

## Knowledge Capture — Triage

Both safety gates were run on every entry below before any home was chosen. **Secret/sensitivity**:
no entry contains a credential, token, key, hostname, or insecure implementation detail — nothing
needed sanitizing. **Repo-relevance**: every entry is public-governance or public-tooling knowledge
about `ose-public`'s own gates, sweeps, and plan conventions; none touches infra-private material,
so none is scoped down. All ten entries reach a terminal state below — the tenth surfaced after the first nine were routed,
during the delivery-boundary push.

| #   | Entry                                                                                                                                                                  | Terminal state                                                                                                                                                                                                                                          |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | A dormant tool hides the gap it was supposed to fill                                                                                                                   | **Filed** as [`gate-exclusions-need-a-named-owner`](../../ideas/q2-not-urgent-important/gate-exclusions-need-a-named-owner.md) — future-work idea, not yet plan-ready                                                                                   |
| 2   | "Leftover from the old stack" was wrong                                                                                                                                | **Discarded** — the [Repo-Grounding Rule](../../../repo-governance/development/quality/plan-anti-hallucination/05-repo-grounding-rule-hard.md) already forbids the unverified claim; routing it would change no durable surface, so it fails the litmus |
| 3   | Test-fixture strings look like real references                                                                                                                         | **Routed inline** into [`class-sweep-completeness`](../../ideas/q2-not-urgent-important/class-sweep-completeness.md)                                                                                                                                    |
| 4   | A sweep's exception list is the sweep                                                                                                                                  | **Routed inline** into `class-sweep-completeness`                                                                                                                                                                                                       |
| 5   | Deleting a token can weaken a test                                                                                                                                     | **Routed inline** into `class-sweep-completeness`                                                                                                                                                                                                       |
| 6   | Correcting one stale fact surfaces its neighbours                                                                                                                      | **Routed inline** into `class-sweep-completeness`                                                                                                                                                                                                       |
| 7   | A count in a plan is an estimate until execution re-runs it                                                                                                            | **Routed inline** into [`acceptance-clause-vacuity`](../../ideas/q1-urgent-important/acceptance-clause-vacuity.md) as a sixth vacuity shape                                                                                                             |
| 8   | Git pathspec globs do not cross `/`                                                                                                                                    | **Routed inline** into [`trustworthy-measurement` Rule 1](../../../repo-governance/development/practice/trustworthy-measurement/01-rule-1-prove-the-command-ran.md), which already collects the false-zero family                                       |
| 9   | The prettier gate is scoped by affected file type                                                                                                                      | **Routed inline** into [`markdownlint-ci-gate-lints-zero-files`](../../ideas/q1-urgent-important/markdownlint-ci-gate-lints-zero-files.md) as a second independent instance                                                                             |
| 10  | A green build can cause a red test: `nx build ayokoding-www` writes `.next/standalone/` copies of `src/`, which the `unit` project's glob then discovers as real tests | **Routed inline** into [`vitest-glob-coverage-guard`](../../ideas/q2-not-urgent-important/vitest-glob-coverage-guard.md) as the mirror image of its glob-too-narrow case                                                                                |

Entries 3-6 all describe the same class and fold into one existing brief rather than four new ones,
per the "fold into an existing two-pager rather than duplicating" rule. No entry implies a code
change, so no `plans/backlog/` follow-up is required by the code-routing downstream rule.

## Follow-Ups Filed

- [`ayokoding-course-root-overview-parity`](../../ideas/q2-not-urgent-important/ayokoding-course-root-overview-parity.md)
  — 23 of 181 courses lack a course-root `overview.md`; two layouts coexist and cross-course links
  already guessed wrong once. Filed rather than fixed: authoring 23 overview pages is content work.
- [`gate-exclusions-need-a-named-owner`](../../ideas/q2-not-urgent-important/gate-exclusions-need-a-named-owner.md)
  — a gate `exclude:` entry cannot express who covers the excluded tree, so a delegation outlives
  its owner silently. Filed rather than fixed: the remedy needs an exclusion census first.
- [`coverage-artifact-relative-paths`](../../ideas/q2-not-urgent-important/coverage-artifact-relative-paths.md)
  — corrected inline (the `fsharp-crane-core` claim), with the re-adjudication of its conclusion
  left as an open question in the brief itself.
