# Idea Disposition Map: Optimize the Pull Request Process

This planning-only map records what the active plan retains before any idea is retired. It does not
edit an idea brief, idea index, or routing artifact. Historical `plans/done/**` references remain
unchanged.

## Source Evidence

- [Repo-grounded] Public source: `ose-public` commit
  `62608547df0d2063d369537e0753f22699456f44`. Its `plans/ideas/` tree contains 83 Markdown paths:
  82 briefs plus the index. The tree count used pinned `git ls-tree`; brief sizes used pinned
  `git show | wc -l -w`; inbound references used pinned `git grep -n -F`. All 19 paths below exist.
- [Repo-grounded] Private source: `ose-private` commit
  `718c20c923707d777a89639f760f98d53740bd70`. The one brief is 135 lines and 1,381 words; its
  tracked inbound index entry is `plans/ideas/README.md:22`.
- [Repo-grounded] No private retirement has merged. The pinned private source remains authoritative
  until PRIV-IDEAS records retirement against an activated public plan pin.

## Current Public Retirement State

The original 19-brief catalog below is immutable planning evidence, not a command to re-open a
completed unit. PRs #269–#271 retired nine briefs before ACTIVATE; PUB-IDEAS-4 completed two more
in PR #276; and PUB-IDEAS-5 completed two in PR #281. Those 13 retirements and their associated
backlink repairs are historical evidence only.

Exactly six public briefs remain: PUB-IDEAS-6 owns
`nx-affected-cross-worktree-contamination.md` and `stale-checkout-ref-advance-drift.md`; PUB-IDEAS-7
owns `cross-repo-governance-link-parity.md` and `plan-archival-in-pr-multi-repo-gap.md`; and
PUB-IDEAS-8 owns `propagation-checklist-under-coverage.md` and
`recurring-defect-family-escalation.md`. PUB-IDEAS-6 is the sole candidate successor and remains
frozen until the plan-state correction and strict revalidation recorded in `delivery.md` are clean.

## Historical Public Dispositions

1. `plans/ideas/q1-urgent-important/acceptance-clause-vacuity.md`
   **Outcome:** `valid`. **Family:** falsifiable planning evidence. **Owner:** `REQUIREMENTS`.
   **Retirement:** `PUB-IDEAS`. Retain executable pass/fail evidence and a tool-capable executor;
   reject a general vacuity tool.
2. `plans/ideas/q1-urgent-important/deletion-authorized-by-absence.md`
   **Outcome:** `partial`. **Family:** recurring-defect root cause. **Owner:** `B`.
   **Retirement:** `PUB-IDEAS`. Retain the worked example; exclude runtime emitter/property tests.
3. `plans/ideas/q1-urgent-important/plan-checker-forward-reference-detection.md`
   **Outcome:** `partial`. **Family:** executable slice ordering. **Owner:** `EXECUTION`.
   **Retirement:** `PUB-IDEAS`. Earlier slices supply later inputs; prefer human/prompt judgment and
   reject a dependency parser.
4. `plans/ideas/q1-urgent-important/plan-decision-integrity-hardening.md`
   **Outcome:** `partial`. **Family:** decision traceability. **Owner:** `A1`.
   **Retirement:** `PUB-IDEAS`. Retain user-job evidence and reversal reasons; reject Step-5o tooling.
5. `plans/ideas/q2-not-urgent-important/class-sweep-completeness.md`
   **Outcome:** `valid`. **Family:** complete defect-class repair. **Owner:** `B`.
   **Retirement:** `PUB-IDEAS`. Check definitions, producers, normative copies, and enclosing blocks;
   reject an ownership registry or new discovery tool.
6. `plans/ideas/q2-not-urgent-important/cross-repo-governance-link-parity.md`
   **Outcome:** `partial`. **Family:** destination validation. **Owner:** `C`.
   **Retirement:** `PUB-IDEAS`. Reuse destination checks on propagated files; reject a general engine.
7. `plans/ideas/q2-not-urgent-important/gate-exclusions-need-a-named-owner.md`
   **Outcome:** `partial`. **Family:** review applicability. **Owner:** `A2`.
   **Retirement:** `PUB-IDEAS`. Explain every skip and alternate evidence; reject gate-schema tooling.
8. `plans/ideas/q2-not-urgent-important/governance-path-ownership-registry.md`
   **Outcome:** `conflict`. **Family:** single applicability authority. **Owner:** `A2`.
   **Retirement:** `PUB-IDEAS`. Retain one clear authority; reject the glob registry/schema/validator.
9. `plans/ideas/q2-not-urgent-important/merge-queue-adoption.md`
   **Outcome:** `partial`. **Family:** unstacked integration freshness. **Owner:** `EXECUTION`.
   **Retirement:** `PUB-IDEAS`. Recheck current base and CI; reject queue/vendor infrastructure.
10. `plans/ideas/q2-not-urgent-important/nx-affected-cross-worktree-contamination.md`
    **Outcome:** `partial`. **Family:** worktree isolation. **Owner:** `EXECUTION`.
    **Retirement:** `PUB-IDEAS`. Reuse one plan worktree per repo, keep WIP out of the primary
    checkout, and reject Nx or hook changes.
11. `plans/ideas/q2-not-urgent-important/plan-archival-in-pr-multi-repo-gap.md`
    **Outcome:** `valid`. **Family:** multi-repo plan closure. **Owner:** `EXECUTION`.
    **Retirement:** `PUB-IDEAS`. Name folder owner, PR order, final signal, and archival vehicle.
12. `plans/ideas/q2-not-urgent-important/plan-quality-gate-convergence.md`
    **Outcome:** `partial`. **Family:** planning convergence. **Owner:** `A1`.
    **Retirement:** `PUB-IDEAS`. Retain distinct lenses, class repair, and reproducible evidence;
    reject registries, new validators, saturation, and the superseded 3–5 target.
13. `plans/ideas/q2-not-urgent-important/pr-review-bot-identity.md`
    **Outcome:** `conflict`. **Family:** PR-native review status. **Owner:** `A3`.
    **Retirement:** `PUB-IDEAS`. Keep body/thread authority and AI markers; reject bot/App/token work.
14. `plans/ideas/q2-not-urgent-important/pr-review-disciplines-applicability-shard-empty.md`
    **Outcome:** `valid`. **Family:** risk-based review routing. **Owner:** `A2`.
    **Retirement:** `PUB-IDEAS`. Retain applicability and four-way fixer judgment, not fixed review.
15. `plans/ideas/q2-not-urgent-important/propagation-checklist-under-coverage.md`
    **Outcome:** `valid`. **Family:** actual-diff propagation. **Owner:** `C`.
    **Retirement:** `PUB-IDEAS`. Use `repo-rules-propagation`, the actual merged diff, justified
    exclusions, and live destination measurement; reject a new CLI.
16. `plans/ideas/q2-not-urgent-important/recurring-defect-family-escalation.md`
    **Outcome:** `valid`. **Family:** changed-strategy recovery. **Owner:** `B`.
    **Retirement:** `PUB-IDEAS`. Keep a PR-native family ledger; a second occurrence triggers a
    bounded invariant probe. Reject mechanical detection and scope exemptions.
17. `plans/ideas/q2-not-urgent-important/repo-rules-quality-gate-convergence.md`
    **Outcome:** `partial`. **Family:** rule-quality convergence. **Owner:** `C`.
    **Retirement:** `PUB-IDEAS`. Retain varied lenses, known-positive probes, and bounded ground
    truth; reject new machinery and saturation as an exit rule.
18. `plans/ideas/q2-not-urgent-important/review-loop-reviews-its-own-record.md`
    **Outcome:** `valid`. **Family:** bounded merge-ready state. **Owner:** `B`.
    **Retirement:** `PUB-IDEAS`. Keep scope stable, audit exact, target 1–3, recover 4–5, and stop
    before 6; reject mandatory three cycles, two-clean confirmation, or an indefinite loop.
19. `plans/ideas/q2-not-urgent-important/stale-checkout-ref-advance-drift.md`
    **Outcome:** `partial`. **Family:** safe worktree reuse. **Owner:** `EXECUTION`.
    **Retirement:** `PUB-IDEAS`. Re-pin and inspect without ref-writing a checked-out branch; reject
    detector/wrapper tooling.

## Private Disposition

1. `plans/ideas/q2-not-urgent-important/pr-review-governance-reference-defects.md` in `ose-private`
   **Outcome:** `partial`. **Family:** cold-reader reference clarity. **Owner:** `REQUIREMENTS`;
   secondary `DESIGN`. **Retirement:** `PRIV-IDEAS`. Retain clear artifact/path/term references,
   two-repo archival and N/A semantics, scope guarding, semantic propagation, and fresh pins. Replace
   ambiguous `classifier evidence` with the review-route record. Reject “worthless without
   validator,” legacy Cycle 10/12/two-clean rules, three-repo assumptions, the stale five-consumer
   count (the pinned base has six), and the unrelated 168-annotation sweep. Private PR
   [#62 review 5000710561](https://github.com/wahidyankf/ose-private/pull/62#pullrequestreview-5000710561)
   remains historical discovery evidence, not current authority.

## Retirement Rule

The original forecast allocated ten remaining briefs to five named `PUB-IDEAS-4`–`PUB-IDEAS-8`
subdeliveries. It is now historical: PUB-IDEAS-4 and PUB-IDEAS-5 are immutable completed evidence,
and only the six paths named in **Current Public Retirement State** may be retired through
PUB-IDEAS-6–8. Only PUB-IDEAS-8's terminal proof may authorize `PRIV-BASE`; its clean or
overlay-owned result, or an evidenced failure repaired by `PRIV-REPAIR`, may then authorize
`PRIV-IDEAS`, which retires the private brief and index entry separately. Every retirement PR
preserves historical references and cites its exact predecessor; no subdelivery may exceed the
plan's human-size boundary.
