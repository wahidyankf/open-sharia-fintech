# Business Requirements Document: PR Review Cycle Scout + Cycle-Number + Type-Soundness

## Business Goal and Rationale

The PR Review Quality Gate pipeline (nine agents: eight discipline specialists +
`pr-review-synthesis-maker`, feeding `pr-review-fixer`, per the fixed 3-cycle loop) is the mandatory
pre-merge gate for every `*-to-pr` delivery in this repo. Its own
[Post-Cutover Monitoring Plan](../../../repo-governance/development/quality/pr-review-disciplines.md#post-cutover-monitoring-plan)
already commits to tracking precision, per-discipline acceptance rate, outdated rate, cost/latency per
risk-tier, and human-override rate — but two of those five metric families (cost/latency per
risk-tier, and the trend of "do later cycles find fewer issues") are unobservable from a posted review
today, because the review carries no cycle number. Separately, the eight-discipline table has no owner
for type-system soundness — a category of defect distinct from compiler errors (already CI-gated) and
from behavioral correctness (already `pr-review-logic-maker`'s job) — in a repo that ships production
code in four statically-typed languages.

The business goal is to close both gaps and to give the existing D12 risk-tier-classification duty its
own dedicated pipeline stage, so:

1. A maintainer scanning a PR's review history can immediately tell which cycle produced which
   finding, without cross-referencing GitHub timestamps against the workflow's fixed cycle count.
2. The opus-tier `pr-review-synthesis-maker` agent's remaining job (the highest-risk
   architecture-vs-correctness re-categorization boundary, plus dedup/filter/verify/post) is not
   also carrying the separate judgment call of "what should even be reviewed here" — a distinct
   concern this plan gives its own dedicated agent.
3. A stray `any`, a non-exhaustive `match`, an unjustified `unsafe` block, or a nullable-reference
   violation gets caught by a reviewer whose charter explicitly owns it, rather than falling through
   the gap between "the compiler didn't complain" and "no specialist's charter covers this."

## Current-State Baseline (Mechanically Verified, 2026-08-05)

- **Pipeline agent count**: 10 files under `.claude/agents/pr-review-*.md` (8 discipline specialists +
  `pr-review-synthesis-maker` + `pr-review-fixer`), mirrored identically under `.opencode/agents/`.
  Verified: `ls .claude/agents/ | grep -c pr-review` → `10`.
- **"eight" mentions**: `pr-review-disciplines.md` contains 26 occurrences of the literal string
  `eight`; `pr-review-quality-gate.md` contains 6. Verified via
  `grep -c eight repo-governance/development/quality/pr-review-disciplines.md` and the same against
  `repo-governance/workflows/pr/pr-review-quality-gate.md`. Every one of these needs inspection during
  Phase 1/2 — not all become `nine` (some describe an unrelated count or a fixed historical fact, e.g.
  "the eight discipline specialists" retiring the single monolith), so each occurrence is
  individually judged rather than blindly sed-replaced.
- **No cycle-number field exists today**: `grep -c "Cycle" .claude/agents/pr-review-synthesis-maker.md`
  under the `## Consolidated Review Header` section returns `0` — the five existing header fields are
  Risk tier, Specialists fanned out, Security-sensitive-path override, Diff coverage, and Prior-cycle
  human dismissals; none names the cycle.
- **No type-soundness discipline exists today**: `grep -ci "type.soundness\|type.safety" repo-governance/development/quality/pr-review-disciplines.md`
  returns `0` in the discipline table itself (the term does not appear as an owned scope anywhere in
  the Eight Reviewer Disciplines table).
- **`AGENTS.md` byte budget is already tight**: 28,944 bytes measured (`wc -c AGENTS.md`,
  re-verified 2026-08-05) against a documented 27,000 B warn / 30,000 B hard-fail threshold (see
  [Instruction-File Size Budget Convention](../../../repo-governance/conventions/structure/instruction-file-size-budget.md)),
  and the pre-existing
  [`agents-md-progressive-disclosure` idea](../../ideas/agents-md-progressive-disclosure.md) already
  flags this exact tightness. This figure is a **point-in-time snapshot, not a guaranteed
  pre-execution value** — `AGENTS.md` is a live, frequently-edited file, so Phase 0's own re-baseline
  step re-measures it immediately before execution and halts if it has drifted since this figure was
  recorded. **Constraint this imposes on this plan**: the `AGENTS.md` PR Review Cycle bullet edit must
  be net-neutral-to-negative in byte count relative to whatever the re-measured baseline turns out to
  be (`eight` → `nine` is net `-1` byte); it must NOT grow to individually name
  `pr-review-scout-maker` or `pr-review-types-maker` — those stay documented in
  `.claude/agents/README.md` and `pr-review-disciplines.md`, which carry no such budget.

## Business Impact

- **Faster trend-spotting on review effectiveness.** A visible `Cycle: N of 3` on every posted review
  lets a human (or a future automated report) read a PR's review history top-to-bottom and see
  whether findings tapered off across cycles — the "healthy trend" signal the workflow's Success
  Metrics section already names as worth tracking but currently cannot observe from the review text
  alone.
- **Cleaner separation of coordinator responsibilities.** Splitting "what does this PR need reviewed"
  (scout) from "consolidate what was found" (synthesis-maker) follows the same single-responsibility
  reasoning that justified splitting the original `pr-review-maker` monolith into eight disciplines in
  the first place — applied one level up, to the coordinator's own two distinct jobs.
- **A new defect category becomes catchable.** Type-unsoundness that compiles cleanly (a broad `any`,
  an unjustified `unsafe`, a non-exhaustive match silently defaulting) is exactly the kind of defect
  that ships silently today because no specialist's charter names it and CI's build step, by
  definition, cannot catch what still compiles.

## Affected Roles

- **The maintainer** (sole reviewer of this repo's own PRs, `[AI]`-merge authority under the five
  hardened preconditions) — gains cycle-number visibility and a ninth discipline's worth of coverage
  on every future `full`-tier PR.
- **`pr-review-synthesis-maker`** — loses the D12/D13 pre-fan-out duties (scoped down to its
  post-fan-out job only); gains one new header field to populate.
- **`pr-review-fixer`** — unaffected in charter; simply sees findings that may now originate from a
  ninth discipline and carry a cycle-number-stamped header.
- **Every future contributor reading `pr-review-disciplines.md` or `pr-review-quality-gate.md`** —
  reads an updated nine-discipline table and an updated ten-agent (soon twelve-agent) pipeline
  diagram/algorithm.

## Business-Level Success Metrics

- **Observable fact**: every consolidated review posted by `pr-review-synthesis-maker` after this
  plan's PR merges carries a `**Cycle**: N of {total}` header line. Verifiable by reading any
  post-merge PR's review comments.
- **Observable fact**: `pr-review-scout-maker` exists at `.claude/agents/pr-review-scout-maker.md`,
  is mirrored at `.opencode/agents/pr-review-scout-maker.md`, and is invoked as pipeline stage 0 in
  this plan's own delivering PR (dogfooded, per the `worktree-to-pr` Delivery Mode).
- **Observable fact**: `pr-review-types-maker` exists at `.claude/agents/pr-review-types-maker.md`,
  mirrored identically, and appears in the `full`-tier specialist set the next time a `full`-tier PR
  runs the pipeline.
- **Judgment call** (no baseline measured; this plan does not fabricate a precision/acceptance-rate
  number for a discipline that has not run yet): the type-soundness discipline's actual value —
  precision, acceptance rate — is only knowable after real PRs exercise it. The existing
  [Post-Cutover Monitoring Plan](../../../repo-governance/development/quality/pr-review-disciplines.md#post-cutover-monitoring-plan)
  already owns measuring this going forward; this plan's job is only to stand the discipline up
  correctly, not to pre-validate its hit rate.

## Business-Scope Non-Goals

- Not attempting to reduce the fixed 3-cycle ceiling or change the CI-green hard gate between cycles —
  both stay exactly as documented.
- Not attempting to close the `REQUEST_CHANGES`/bot-identity gap (tracked separately, see README.md
  Out of Scope).
- Not adding a persistent cross-PR metrics log (the maintainer's explicit grill answer — header
  fields only for now).
- Not propagating any part of this to the other three repos — this is `ose-public`-only governance
  infrastructure, not part of either cross-repo parity boundary.

## Business Risks and Mitigations

- **Risk**: a second opus-tier call per cycle (scout, in addition to synthesis-maker) increases
  per-PR cost beyond what the convention's existing
  [Cost and Latency Budgeting](../../../repo-governance/development/quality/pr-review-disciplines.md#cost-and-latency-budgeting)
  future-work section estimated. **Mitigation**: scout runs once per cycle regardless of tier (even a
  `trivial`-tier PR needs classifying), so its cost is bounded and predictable, unlike the
  per-specialist multiplier the risk-tier fan-out already controls; the added cost is documented
  explicitly in [tech-docs.md](./tech-docs.md#design-decisions) rather than silently absorbed, so a
  future maintainer revisiting the Cost and Latency Budgeting section has the real number to react to.
- **Risk**: the type-soundness discipline overlaps with `pr-review-architecture-maker` (which already
  owns "quality-attribute effects") or `pr-review-governance-maker` (mechanical conformance),
  producing duplicate or misfiled findings. **Mitigation**: a new grey-zone ruling (g) is added to
  `pr-review-disciplines.md` alongside the existing six, explicitly separating "does it compile"
  (not this discipline's job at all — CI already gates it) from "is it sound" (this discipline's
  job) from "should this boundary exist" (architecture's job) — see
  [tech-docs.md Design Decision DD-2](./tech-docs.md#design-decisions).
- **Risk**: `AGENTS.md`'s tight byte budget silently regresses further. **Mitigation**: the baseline
  above measures the exact current byte count and the planned edit's exact delta before any edit
  lands; Phase 4's delivery item re-measures after the edit as an explicit acceptance criterion.

## Related Documentation

- [README.md](./README.md) — plan overview, scope, resolved design decisions
- [prd.md](./prd.md) — product scope and Gherkin acceptance criteria
- [tech-docs.md](./tech-docs.md) — architecture and detailed design
- [PR Reviewer-Discipline Convention](../../../repo-governance/development/quality/pr-review-disciplines.md)
- [PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md)
- [Instruction-File Size Budget Convention](../../../repo-governance/conventions/structure/instruction-file-size-budget.md)
