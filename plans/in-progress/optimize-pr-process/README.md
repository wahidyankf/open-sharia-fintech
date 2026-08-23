# Plan: Optimize the Pull Request Process

## Status

- **Lifecycle**: In Progress
- **Control-plan repository**: `wahidyankf/ose-public`
- **Execution scope**: `wahidyankf/ose-public` and `wahidyankf/ose-private`
- **Future delivery mode**: `worktree-to-pr` in each repository
- **Plan shape**: one public control plan, with repo-specific execution and evidence
- **Last research verification**: 2026-08-23

## Context

The two OSE repositories already have a detailed pull request (PR) authoring convention, a
risk-tiered AI review pipeline, a fixer, a merge quality gate, and plan workflows. The pieces do not
yet form one bounded, human-first process. Current rules disagree about clean-cycle counts, allow a
seven-cycle default that recent PRs exceeded, mix human-readable comments with an unused hidden
audit schema, and contain planning instructions that conflict with mandatory PR delivery.
`[Repo-grounded]`

Two recent cross-repository changes show the cost of those contradictions:

- [`ose-public#249`](https://github.com/wahidyankf/ose-public/pull/249) merged on 2026-08-22 with
  151 files, 3,263 changed lines, 22 commits, 115 resolved review threads, 14 consolidated review
  cycles plus an addendum, and 44 workflow runs. The
  [final cycle](https://github.com/wahidyankf/ose-public/pull/249#pullrequestreview-5000721156) and
  [merge audit](https://github.com/wahidyankf/ose-public/pull/249#issuecomment-5382843075)
  record an owner-directed merge while the stated convergence precondition remained unmet.
  Only an ideas-stage plan file was touched, not an active execution plan. `[Repo-grounded]`
- [`ose-private#62`](https://github.com/wahidyankf/ose-private/pull/62) merged on 2026-08-22 with
  141 files, 3,003 changed lines, 20 commits, 76 resolved review threads and 76 replies, 11
  consolidated review artifacts, and 40 workflow runs. Its body records review-driven scope
  additions and retirement of the size ceiling. The
  [checkpoint](https://github.com/wahidyankf/ose-private/pull/62#issuecomment-5381514160),
  [cycle 11](https://github.com/wahidyankf/ose-private/pull/62#pullrequestreview-5000735758), and
  [merge audit](https://github.com/wahidyankf/ose-private/pull/62#issuecomment-5382843178) do not
  reconcile: the merge note refers to cycles 11–14 finding defects although only cycles 1–11 exist
  as consolidated reviews. Only ideas-stage plan files were touched, not an active plan.
  `[Repo-grounded]`

These are two observations, not an industry baseline. They show local failure modes that this plan
must remove: oversized delivery units, scope growth during review, unclear loop exit, and an audit
record whose statements cannot be reconciled from the PR itself.

## Outcome

Execution produces one coherent PR lifecycle that a human can follow without knowing the agent
implementation:

1. The author opens a small, cohesive PR with `Why`, `Scope and non-goals`, `Summary`, an ordered
   `Reading Guide`, `Verification`, and a code cost/benefit statement when code is added. An
   accessible Mermaid diagram is optional when it materially reduces reader effort; adjacent prose
   carries the equivalent meaning.
2. Cycle 1 performs the complete risk-tiered probe. The synthesizer posts one review body and
   line-anchored finding threads in GitHub.
3. The fixer critically appraises each finding and replies in the same thread with exactly one of
   `fix`, `reject`, `defer`, or `clarify`, including evidence and reasoning.
4. Cycle 2 reviews fixes and the current-head delta. Cycle 3 performs a fresh final verification.
5. Cycles 4 and 5 are exceptional recovery cycles. Before each one, the agent posts a concise
   recovery note stating why the prior cycle did not converge and what strategy changes; the note
   is an audit artifact, not a human authorization gate. A sixth AI cycle is forbidden; unresolved
   defects then keep the PR blocked for a human decision.
6. The PR body, reviews, threads, replies, recovery notes, linked follow-ups, checks, and merge note
   are the human-readable audit record. Hidden metadata is optional only when a real consumer is
   demonstrated.
7. Cross-repository work proceeds as one interleaved obligation wave at a time:
   `PUB-A1 -> PRIV-A1 -> PUB-A2 -> PRIV-A2 -> PUB-A3 -> PRIV-A3 -> PUB-B -> PRIV-B`, followed by
   `PUB-C -> PRIV-C` only when the CI mechanism-necessity gate passes. Private work consumes only
   the matching merged, green public PR and commit SHA. A completed wave is in semantic **sync**
   when both repositories express the same portable obligation with recorded repo-specific
   adaptations; it does not require byte-identical files. `[Judgment call]`

The policy is deliberately prose- and artifact-first. It does not add a bot, parser, dashboard,
database, or PR-process validator. `[Judgment call]`

## Hard Boundaries

The following requirements are non-negotiable throughout authoring, implementation, review, and
fixing:

- **Code is a maintenance liability.** Add no mechanical enforcement or tooling unless a measured
  failure proves it necessary and a written cost/benefit test shows the smallest repair is cheaper
  than clear prose and native GitHub behavior.
- **Humans are first-class readers.** PR scope, size, description, findings, replies, and audit
  notes are understandable by an engineer with bootcamp training and practical coding experience,
  without assuming a university/CS bachelor curriculum or treating that reader as less capable.
- **Every PR expects a human reader.** Agent authorship, review, or merge eligibility never makes a
  PR machine-only. The complete artifact remains useful to a human reading it before merge, during
  review, or retrospectively after merge.
- **Descriptions use progressive disclosure.** Lead with the problem and outcome, keep scope and
  conceptual summary brief, provide an ordered reading path and current-head proof, and link deep
  rationale instead of copying research or methodology into the PR. Headings and bullets support
  scanning; tables and diagrams appear only when they reduce prose.
- **Review teaches accessibly.** Each blocking finding is concise, explains the observation and
  observable consequence, provides a reproduction or inspection path and bounded remedy, and
  defines only relevant concepts. It assumes practical coding ability but no academic coursework in
  algorithms, operating systems, compilers, distributed systems, security, or architecture.
- **Review is a conversation.** Findings and dispositions use GitHub-native line comments,
  replies, and resolution. A summary that bypasses the threads does not close them.
- **AI authorship is overt.** Every AI-authored review body, finding, reply, recovery note, and
  escalation ends with:

  ```text
  ---

  Generated by AI
  ```

- **The loop is bounded.** Cycles 1–3 are the target and the process hard-stops before cycle 6. Cycles 4–5
  require an agent-authored changed-strategy recovery note, but not advance human approval; cycle 6
  never starts. The agent escalates earlier only when it needs human judgment or authority. The
  ceiling never waives a defect.
- **The fixer may reject.** It must push back on unsound, obsolete, duplicated, or out-of-scope
  findings with specific evidence; bare agreement or disagreement is invalid.
- **Scope never widens silently.** The stated problem and non-goals anchor the loop. A defect this
  PR introduces and complete repair of the same defect class remain in scope; an adjacent
  improvement becomes a linked follow-up from the original thread.
- **The PR is the audit source.** A future reader can reconstruct every cycle and disposition from
  the PR artifact without consulting a private agent log.
- **One worktree per repository, not per PR.** The plan reuses exactly one public and one private
  worktree across every sequential delivery unit, synchronizing that same worktree from the repo's
  merged `origin/main` after each PR.
- **Rule propagation is canonical and repo-isolated.** Every rule-bearing boundary invokes
  `repo-governance/workflows/repo/repo-rules-propagation.md` with `isolation=current` in that
  repository's one plan worktree. The public repository is the canonical source. A public run
  records a PR-native sibling obligation; a separate private run starts only after the matching
  public PR and source SHA are merged and green, then discharges that exact obligation. One run
  never writes both repositories.
- **Cross-repository `sync` is semantic and wave-complete.** Sync means the portable rule's intent,
  observations, and required behavior agree after allowed repo-specific adaptation. It never means
  byte identity unless an existing rule explicitly names a byte-identity surface. Only one portable
  sibling obligation wave may be open; the next public wave waits for the current private discharge.
- **Downstream discoveries receive one explicit class.** Private review records whether a finding is
  a private implementation/private-only defect, a deliberate repo-specific deviation, a portable
  public-source defect, or a defect on an explicitly byte-identical surface. Private-only defects
  stay private; deviations are reasoned and evidenced; byte-identity defects follow the surface's
  existing parity rule.
- **Portable source defects repair upstream once.** A portable public-source defect stops the
  private wave before merge, repairs the canonical public source first in a merged green correction
  PR, supersedes the obligation's pinned public SHA, and revalidates only the affected rule class in
  public and private. Each wave permits its initial propagation plus at most one upstream
  correction. A second attempted reversal is oscillation: stop, amend and re-review this plan, and
  require human judgment before any further propagation. `[Judgment call]`
- **No chain-reaction machinery or branch chain.** Never copy draft public text into private, stack a
  dependent private PR on an unmerged public branch, send reciprocal public/private correction PRs,
  or create a hidden registry, bot, or validator to coordinate waves. The obligation and its source
  pin live in the human-readable public and private PR records. `[Judgment call]`
- **Transitions require explicit user authority.** The current public worktree remains the one
  public worktree from plan making through every public PR. Plan iteration normally edits only these
  six plan files. On 2026-08-23 the user explicitly expanded plan making to consolidate and delete
  related idea briefs and their indexes/links in both repositories; the one private plan worktree
  was provisioned for that bounded plan-document task and must be reused later. The same instruction
  authorized the formal plan gate, plan delivery, and full execution, as recorded in the
  [delivery authorization ledger](./delivery.md#authorization-ledger). Those transitions remain
  sequential: this plan-editing pass does not itself run the gate, stage, commit, push, open a PR,
  or begin implementation.
- **Large-plan units are sequential and recoverable.** After authorization, execute exactly one
  fixed unit from current `origin/main`, measure cohesion and size before its PR, and merge, record
  evidence, and synchronize the same worktree before the next. Oversized or multi-problem work
  stops for plan amendment and stable-main splitting; dependent PRs are not stacked by default.
- **Every multi-PR sequence preserves stable `main`.** Each delivery unit declares a lightest-fit
  integration-safety strategy under the umbrella term **feature flag**: an existing feature/config
  flag, a dormant default-off path, a compatibility bridge, ordered activation, or another
  reversible mechanism. Prose and rules normally use compatibility wording or ordered activation;
  no new feature-flag framework is created by default.
- **Diagrams earn their place.** A PR description may use an accessible Mermaid diagram only when
  it materially clarifies architecture, dependency, state, or sequence. The diagram has descriptive
  labels, an approved accessible palette, and a prose equivalent; decorative diagrams are omitted.

## Convergence Approach

Five cycles are a stop condition, not a guarantee. The process makes convergence likely by reducing
avoidable discovery and rework before and between cycles:

1. **Enter review ready.** Before cycle 1, the agent self-reviews the complete diff, removes
   accidental or unrelated changes, makes the body and acceptance criteria match the current head,
   runs relevant local checks, confirms scope and non-goals, and selects the full risk-tier probe.
   A draft, knowingly incomplete implementation, unstable scope, or unexplained failing check does
   not enter the counted loop.
2. **Make cycle 1 complete.** All selected specialists inspect the same head. Synthesis deduplicates
   their output and admits a blocking finding only when it is evidence-backed, in scope,
   consequential, non-duplicative, and has a bounded disposition path. Known review disciplines are
   not saved for later cycles.
3. **Close one coherent batch.** The fixer appraises every finding, resolves clarifications first,
   makes one cohesive repair batch, runs relevant checks, updates the PR body, and replies with
   evidence in every original thread before requesting another cycle. Partial pushes do not
   intentionally manufacture extra rounds.
4. **Narrow later review.** Cycle 2 examines prior dispositions, repair-induced risks, and the
   current-head delta. Cycle 3 is a fresh final verification. A resolved or rejected point is not
   reopened without new evidence, and the process exits as soon as the current head is safe; it
   does not run cycles merely to reach a number.
5. **Change strategy for recovery.** Before cycle 4 or 5, the agent posts a recovery note identifying
   the non-convergence cause, remaining blockers, stable scope, and a different bounded strategy.
   Repeating the same review/fix attempt is invalid. Material scope change, repeated recurrence,
   or an unresolvable product/architecture choice triggers split, rework, or human escalation
   instead of blind iteration.
6. **Leave an inspectable record.** Each cycle records the reviewed head, admitted findings,
   dispositions, checks, scope movement, and recovery reasoning in the PR. Humans can assess both
   the outcome and how efficiently the agent converged, including after merge.

## Idea-Brief Consolidation

The user authorized immediate consolidation and deletion of related `plans/ideas` briefs in both
repositories. Deletion follows this recorded disposition; it is not evidence that every proposal was
accepted.

| Retired idea                                          | Disposition in this plan                                                                                                                                                                                                                                                                                                                                           |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `class-sweep-completeness`                            | Absorb class-level closure: inspect definitions, producers, consumers, validators, root instructions, normative copies, exclusions, and the enclosing edited block. Use human judgment; add no discovery tool.                                                                                                                                                     |
| `plan-archival-in-pr-multi-repo-gap`                  | Absorb a final public closure/archival PR after every private delivery is evidenced; do not use a direct-push carve-out.                                                                                                                                                                                                                                           |
| `plan-quality-gate-convergence`                       | Absorb complete, independently scoped first-pass lenses, evidence-backed fixes, class-level remediation, and a fixed review surface. Reject a new registry or validator without the mechanism-necessity proof. The formal plan gate and full execution were authorized on 2026-08-23; see the [delivery authorization ledger](./delivery.md#authorization-ledger). |
| `pr-review-bot-identity`                              | Reject. Native review bodies, threads, severity, dispositions, unresolved-thread checks, and the `Generated by AI` marker are sufficient. A GitHub App/token is new security and maintenance machinery without demonstrated necessity.                                                                                                                             |
| `pr-review-disciplines-applicability-shard-empty`     | Absorb the placement repair: write the promised public applicability/disposition rule or remove the promise after canonical conflict scanning; do not leave an index pointing to empty content.                                                                                                                                                                    |
| `recurring-defect-family-escalation`                  | Absorb a second-occurrence trigger: the next pass becomes a bounded root-cause/invariant review instead of fixing another shape. Escalation remains within scope and does not authorize broad redesign.                                                                                                                                                            |
| `repo-rules-quality-gate-convergence`                 | Absorb ground-truth inventories, known-positive control probes for zero-result searches, and class-complete fixes into prose and existing workflows. Reject a new blind-spot registry/validator by default.                                                                                                                                                        |
| `review-loop-reviews-its-own-record`                  | Absorb concise PR-native records pinned to reviewed heads. Do not grow a branch-side correction ledger or mandatory hidden schema that becomes its own repeated review surface.                                                                                                                                                                                    |
| `ose-private: pr-review-governance-reference-defects` | Absorb the still-reproducible cold-reader defects: useless index annotations, stale/nonexistent agent paths, undefined classifier evidence, and missing two-repository archival semantics. Prefer prose/catalog repairs; validator changes remain behind the necessity gate.                                                                                       |

`merge-queue-adoption` and incidental ideas merely discovered during a review cycle remain separate:
they solve different product, CI, or concurrent-merge problems and are not silently swallowed by
this plan.

## Human-Reviewability Policy

The intended local heuristic is:

- **Preferred target**: at most 200 review-relevant, hand-authored changed lines and 10
  hand-authored files.
- **Local upper ceiling**: at most 400 review-relevant, hand-authored changed lines and 20
  hand-authored files.
- **Primary test**: one minimal, self-contained problem whose diff is conceptually cohesive.
- **Exceptions**: generated mirrors, indivisible atomicity, or a mechanically repetitive sweep may
  exceed a numeric target only with an explicit rationale and an ordered reading guide.
- **Enforcement**: reviewer/author judgment, not a new CI check. `[Judgment call]`

The 200/10 preference is a local policy choice informed by research, not an industry law. Google
states that there is no universal maximum, that about 100 lines is usually reasonable and 1,000 is
usually too large, and that a change should be one minimal self-contained unit. The SmartBear/Cisco
case study reported better outcomes below 200 lines and a practical 400-line inspection ceiling in
that setting. One Google observational study reported a median change size of 24 lines and roughly
90% of changes touching fewer than 10 files; observational review research also associates larger
file/line spread with slower or less useful feedback. `[Web-cited]`

## Scope

### In scope

| Surface                  | Intended result                                                                                                                                                                         |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Planning                 | One stage-ownership model, PR-compatible delivery language, non-circular checker/fixer ordering, and unambiguous archival/cleanup                                                       |
| PR authoring             | Concise progressive-disclosure description, cohesive scope, review focus, related-work links, preferred size/ceiling, ordered reading and skip paths, current-head verification         |
| Review                   | Risk-tiered but simpler contracts; practical-reader findings under the defined bootcamp/no-university-CS baseline; one complete first-cycle probe                                       |
| Fixing                   | Four-way evidence-based disposition in the original thread, including rejection and scope deferral                                                                                      |
| Loop exit                | Target cycles 1–3, changed-strategy recovery in cycles 4–5, hard stop before cycle 6                                                                                                    |
| Audit                    | Native GitHub artifact as the primary human-readable record; overt AI markers                                                                                                           |
| Existing quality gate    | Revalidate fail-open, self-mutation, and duplicate-work concerns; repair only proven defects in existing machinery                                                                      |
| Cross-repo propagation   | Interleaved canonical waves: one merged-green public Step 9 obligation followed by one private adaptation/discharge before the next public wave opens                                   |
| Large-plan decomposition | Ordered PRs for plan establishment, rules, executable bindings, conditional code, private propagation, and closure, each with dependency, compatibility, rollback, and scope boundaries |
| Integration safety       | A declared lightest-fit feature-flag strategy for every multi-PR sequence so each intermediate `main` remains coherent and reversible                                                   |

### Out of scope

- Application feature work or product behavior changes.
- A general CI redesign, branch-protection change, merge queue, or hosted review service.
- A new bot, GitHub App, parser, database, dashboard, metrics service, or PR-process validator.
- Automatic PR-size rejection.
- Private infrastructure details copied into the public repository.
- A sixth AI review cycle or a policy that treats the cycle cap as permission to merge defects.

## Single-Control-Plan Deviation

Current multi-repository planning governance calls for one plan in each target repository.
`[Repo-grounded]` The user chose the more recent single-control-plan precedent demonstrated by
[`2026-08-06__pr-review-cycle-scout-and-typesafety`](../../done/2026-08-06__pr-review-cycle-scout-and-typesafety/README.md):
the public repo carries the control plan while each repo receives its own worktree, PRs, validation,
evidence, and closure. `[Judgment call]`

This is a documented deviation, not a silent exception:

- `ose-public` owns this plan, the cross-repo decision matrix, research, and final archival.
- `ose-private` receives no duplicate plan folder, but its execution track must produce a complete
  PR-native audit trail and a repo-specific closure record linked from the public plan.
- Each repository remains independently mergeable; public decisions are propagated through
  separate canonical runs and repo-local placement, never byte-copied blindly.
- Future implementation must not use this precedent to bypass the one-plan-per-repo rule for a
  different project without a new explicit decision.

## Delivery Shape

Both repositories use `worktree-to-pr` and one worktree per repository for this plan:

- `ose-public`: `worktrees/optimize-pr-process/` — already provisioned.
- `ose-private`: `worktrees/optimize-pr-process/` — provision once only when explicitly authorized
  execution reaches private work.

The public source contract lands first in each small wave. Each public canonical run records one
private sibling obligation at Step 9, including the merged public PR and source SHA once green.
Private propagation then uses a separate canonical run from private `origin/main` to place the
semantic rule, record any repo-specific adaptation, and discharge that obligation. The next public
wave does not open until the private discharge merges green. The fixed order is
`PUB-A1 -> PRIV-A1 -> PUB-A2 -> PRIV-A2 -> PUB-A3 -> PRIV-A3 -> PUB-B -> PRIV-B`, followed by the
conditional `PUB-C -> PRIV-C` wave only when necessary. Each repository uses separate PRs, checks,
reviews, replies, convergence decisions, and merge evidence. The public control plan is archived
inside the final public PR.

A completed wave is semantically synchronized, not byte-identical by default. If private review
finds a portable source defect, the private PR stops and the public source receives the sole
allowed upstream correction before private resumes from the superseding merged-green SHA. A second
attempt to reverse direction is oscillation and requires plan amendment plus human judgment. Draft
copying, stacked dependent PRs, reciprocal ping-pong, and hidden coordination machinery are
forbidden. `[Judgment call]`

The large plan decomposes in dependency order: the plan itself establishes intent; human-facing
rules and templates land before or atomically with executable agent/skill bindings; conditional
workflow code follows only after its necessity gate; private PRs adapt already-merged public
semantics; closure and archival come last. Every boundary declares what keeps intermediate `main`
compatible and how reverting that PR restores the prior safe state.

## Plan Documents

- [Business requirements](./brd.md) — why the process must change and what business outcome matters.
- [Product requirements](./prd.md) — personas, user stories, and Gherkin acceptance criteria.
- [Technical design](./tech-docs.md) — target contracts, diagrams, cross-repo matrix, and file impact.
- [Delivery checklist](./delivery.md) — execution-grade cross-repo phases and gates.
- [Learnings](./learnings.md) — execution-time knowledge-capture log.

## Authoritative Research Sources

All links below were accessed 2026-08-23. The plan paraphrases conservatively and preserves short,
compliant supporting passages in the
[`tech-docs.md` source-verification cache](./tech-docs.md#supporting-excerpt-cache) rather than
repeating quotations throughout the human-facing plan.

- [Google: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [Google: CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html)
- [Google: Navigate a CL in review](https://google.github.io/eng-practices/review/reviewer/navigate.html)
- [Google: Review comments](https://google.github.io/eng-practices/review/reviewer/comments.html)
- [Google: Speed of code reviews](https://google.github.io/eng-practices/review/reviewer/speed.html)
- [Google: The standard of code review](https://google.github.io/eng-practices/review/reviewer/standard.html)
- [Google: Pushback in code reviews](https://google.github.io/eng-practices/review/reviewer/pushback.html)
- [GitHub: About pull request reviews](https://docs.github.com/en/pull-requests/reference/pull-request-reviews)
- [GitHub: Commenting on a pull request](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/commenting-on-a-pull-request)
- [GitHub: Resolving a pull request review](https://docs.github.com/en/pull-requests/concepts/resolving-reviews)
- [GitHub: Helping others review your changes](https://docs.github.com/en/pull-requests/concepts/helping-others-review-your-changes)
- [GitHub: Creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)
- [Microsoft: Code review author guidance](https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/author-guidance/)
- [MSR 2026: Pull Request Description Information and Developer Satisfaction](https://doi.org/10.1145/3793302.3793368)
- [IEEE TSE: Pull Request Template Study](https://doi.org/10.1109/TSE.2022.3224053)
- [Stripe: Minions, part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
- [Stripe: Minions, part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Bacchelli and Bird: Expectations, Outcomes, and Challenges of Modern Code Review](https://doi.org/10.1109/ICSE.2013.6606617)
- [SmartBear/Cisco code-review case study](https://static0.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf)
- [Google code-review study](https://storage.googleapis.com/gweb-research2023-media/pubtools/pdf/80735342aebcbfc8af4878373f842c25323cb985.pdf)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [Trunk Based Development: Short-Lived Feature Branches](https://trunkbaseddevelopment.com/short-lived-feature-branches/)
