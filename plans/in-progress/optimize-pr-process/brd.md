# Business Requirements Document: Optimize the Pull Request Process

## Business Goal

Make each pull request in `ose-public` and `ose-private` a bounded, understandable engineering
conversation that improves the change and teaches the team, while reducing avoidable AI review
cost, scope growth, process contradictions, and maintenance code. `[Judgment call]`

The business outcome is not “more review.” It is a smaller number of higher-value review cycles
whose decisions are legible to a human and recoverable from the PR itself.

## Problem Statement

The repositories already invest heavily in PR review, but the process has five business-level
failure modes:

1. **Review effort can exceed the change's human reviewability.** Two recent parity PRs each
   exceeded 140 files and 3,000 changed lines. One required 14 consolidated review cycles and the
   other records 11 review artifacts. `[Repo-grounded]`
2. **Review can grow the work it is meant to bound.** `ose-private#62` explicitly records
   review-driven scope additions and retirement of its ceiling. `[Repo-grounded]`
3. **The written process does not have one authoritative stop condition.** Current surfaces refer
   to seven-cycle defaults, extensions beyond the ceiling, and conflicting clean-cycle rules.
   `[Repo-grounded]`
4. **The audit trail can contradict itself.** `ose-private#62`'s merge note refers to cycles 11–14,
   while the PR exposes only 11 consolidated review artifacts. `[Repo-grounded]`
5. **Process machinery can become its own product.** Existing comments, native threads, checks,
   and PR descriptions already provide the necessary durable surface; new parsers, schemas, or
   validators would add code that must be understood, tested, secured, and maintained.
   `[Judgment call]`
6. **Cross-repository correction can become a chain reaction.** If private work consumes a public
   draft, treats semantic parity as byte identity, or sends each downstream discovery back and
   forth without a bounded source-repair rule, both repositories can accumulate dependent PRs and
   reverse each other's decisions. `[Judgment call]`

## Evidence Baseline

### Local observations

| Observation                   |                                    `ose-public#249` |                          `ose-private#62` |
| ----------------------------- | --------------------------------------------------: | ----------------------------------------: |
| Files changed                 |                                                 151 |                                       141 |
| Additions                     |                                               2,678 |                                     2,561 |
| Deletions                     |                                                 585 |                                       442 |
| Total changed lines           |                                               3,263 |                                     3,003 |
| Commits                       |                                                  22 |                                        20 |
| Review threads                |                                                 115 |                                        76 |
| Consolidated review artifacts |                                    14 plus addendum |                                        11 |
| Workflow runs                 |                                                  44 |                                        40 |
| Merge state                   | Owner-directed while convergence precondition unmet | Owner-directed while exit condition unmet |

All values are `[Repo-grounded]` measurements taken on 2026-08-23 from GitHub's PR, GraphQL, and
Actions APIs. They are case studies, not representative averages.

### Industry rationale

The compact, access-dated supporting excerpts for the recurring Google, GitHub, Microsoft, Trunk
Based Development, and Anthropic claims are preserved in
[`tech-docs.md`'s source-verification cache](./tech-docs.md#supporting-excerpt-cache). Each bullet
below maps to that cache by source name; the longer source table retains the non-normative research
context without repeating quotations here.

- Google recommends one minimal, self-contained change, reports that roughly 100 lines is often a
  reasonable review size, and says 1,000 lines is usually too large while explicitly rejecting one
  universal numeric rule. `[Web-cited]` [Source](https://google.github.io/eng-practices/review/developer/small-cls.html),
  accessed 2026-08-23.
- Google asks authors to explain what changed and why, include relevant context, and write the
  description for future readers. `[Web-cited]` [Source](https://google.github.io/eng-practices/review/developer/cl-descriptions.html),
  accessed 2026-08-23.
- Google also advises reviewers to establish the main parts and inspect the change in a logical
  order; this supports an author-provided consequential-file reading path rather than a file dump.
  `[Web-cited]` [Source](https://google.github.io/eng-practices/review/reviewer/navigate.html),
  accessed 2026-08-23.
- GitHub asks authors to explain the problem, approach, result, and rationale; point reviewers to
  important files and desired feedback; and self-review and test before requesting review.
  `[Web-cited]`
  [Source](https://docs.github.com/en/pull-requests/concepts/helping-others-review-your-changes),
  accessed 2026-08-23.
- GitHub supports Mermaid rendering in Markdown. That establishes capability only; the OSE rule to
  use a diagram only when it reduces prose is a local judgment call. `[Web-cited]`
  [Source](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams),
  accessed 2026-08-23.
- Microsoft's engineering guidance favors a short title, concise what/why/change/impact/solution,
  exact validation, logical review sequence, relevant rollout/migration facts, and visual evidence
  only when useful; it also recognizes flags or hidden paths as split-safety mechanisms.
  `[Web-cited]`
  [Source](https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/author-guidance/),
  accessed 2026-08-23.
- A 2026 MSR observational study consolidated common description elements including purpose, why,
  change explanation, related issues, requested feedback, review order, tests, and screenshots, but
  reported mostly negligible associations; this plan treats the taxonomy as a prompt set, not proof
  that more fields improve outcomes. `[Web-cited]`
  [Cache `MSR-DESC`](./tech-docs.md#supporting-excerpt-cache),
  [source](https://doi.org/10.1145/3793302.3793368), accessed 2026-08-23.
- An IEEE TSE template study found that irrelevant or duplicated prompts and verbose instructions
  can increase effort and harm readability; this supports removing empty conditional sections and
  keeping the core template concise. `[Web-cited]`
  [Cache `TSE-TEMPLATE`](./tech-docs.md#supporting-excerpt-cache),
  [Source](https://doi.org/10.1109/TSE.2022.3224053), accessed 2026-08-23.
- Google asks reviewers to explain reasoning, critique code rather than people, distinguish
  required comments from optional or informational comments, and help improve developer skill.
  `[Web-cited]` [Source](https://google.github.io/eng-practices/review/reviewer/comments.html),
  accessed 2026-08-23.
- Bacchelli and Bird found that modern code review supports knowledge transfer and team awareness,
  not only defect discovery. `[Web-cited]`
  [Cache `BAC-BIRD`](./tech-docs.md#supporting-excerpt-cache),
  [source](https://doi.org/10.1109/ICSE.2013.6606617), accessed 2026-08-23.
- GitHub defines PR review as a conversation with reviews, line comments, replies, and resolution;
  this native structure is the appropriate durable record for review decisions. `[Web-cited]`
  [Sources](https://docs.github.com/en/pull-requests/reference/pull-request-reviews),
  [commenting](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/commenting-on-a-pull-request),
  and [resolution](https://docs.github.com/en/pull-requests/concepts/resolving-reviews), accessed
  2026-08-23.
- GitHub recommends that authors self-review the diff, remove accidental changes, and confirm
  relevant builds or tests before requesting review. Google recommends small changes and complete,
  prompt review rounds rather than delaying major feedback across repeated passes. These practices
  reduce avoidable late discovery but do not guarantee a fixed number of cycles. `[Web-cited]`
  [GitHub](https://docs.github.com/en/pull-requests/concepts/helping-others-review-your-changes),
  [Google small changes](https://google.github.io/eng-practices/review/developer/small-cls.html),
  and [Google review speed](https://google.github.io/eng-practices/review/reviewer/speed.html),
  accessed 2026-08-23.
- Trunk Based Development permits PR branches when they remain short-lived, return to trunk, and do
  not merge part-complete work into another feature branch. This supports merged-main handoffs
  instead of stacked public/private branch chains; the exact OSE wave protocol remains a local
  judgment call. `[Web-cited]`
  [Source](https://trunkbaseddevelopment.com/short-lived-feature-branches/), accessed 2026-08-23.
- Stripe's Minions articles report allowing only one or two full CI rounds because of cost, time,
  and diminishing returns. This supports bounded automation but is **CI evidence, not an
  authoritative PR-review cycle count**. `[Web-cited]`
  [Cache `STRIPE-CI`](./tech-docs.md#supporting-excerpt-cache),
  [Part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) and
  [Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2),
  accessed 2026-08-23.
- Anthropic recommends evaluator-optimizer loops only where clear criteria exist and describes
  maximum-iteration stops, while warning that agent complexity should earn its cost. It gives no
  universal PR-review maximum. `[Web-cited]`
  [Source](https://www.anthropic.com/engineering/building-effective-agents), accessed 2026-08-23.
- NIST's generative-AI risk profile supports provenance and disclosure that help people distinguish
  content origin and trace outcomes. The exact `Generated by AI` footer remains an OSE convention,
  not a universal NIST prescription. `[Web-cited]`
  [Cache `NIST-PROVENANCE`](./tech-docs.md#supporting-excerpt-cache),
  [Source](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf), accessed 2026-08-23.

## Affected Roles

| Role                      | Current cost                                                                                                                                                                       | Intended benefit                                                                                                                         |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| PR author                 | Repeatedly reacts to findings and can absorb adjacent work                                                                                                                         | Starts with a clear, cohesive contract and can push back with evidence                                                                   |
| Practical junior engineer | Has completed a coding bootcamp, writes working code, and has not completed a university/CS bachelor curriculum; specialist shorthand may assume coursework they have never needed | Learns from concise observation, observable consequence, reproduction evidence, and bounded remedy without being treated as less capable |
| Reviewer                  | Reconstructs scope, prior decisions, and cycle state                                                                                                                               | Reads an ordered diff and a compact, native cycle record                                                                                 |
| Fixer                     | Can appear to accept every finding and grow the PR                                                                                                                                 | Uses explicit four-way critical appraisal with scope protection                                                                          |
| Maintainer                | Pays CI, agent, and attention cost; may override an unbounded loop                                                                                                                 | Gets a bounded escalation point and a reconstructable record                                                                             |
| Future auditor            | Must reconcile agent logs, comments, and contradictory merge notes                                                                                                                 | Reconstructs decisions from the PR artifact itself                                                                                       |

## Business Requirements

### BR-1: Human-readable delivery units

Every PR must describe one cohesive problem, its non-goals and reasons, the ordered reading path,
and current-head verification. The primary human reader sees the problem and outcome first, then a
brief scope/non-goal contract, a conceptual summary rather than a file inventory, and only the
detail needed to review. Deep research and governance rationale are linked, not copied into a
methodology dump. Headings and short lists support scanning; tables and diagrams are sparse and
must reduce prose. The preferred local target is 200 review-relevant hand-authored lines and 10
hand-authored files; 400/20 remains a local upper ceiling. Conceptual cohesion is the primary rule,
and exceptions require a human-readable rationale. `[Judgment call]`

### BR-2: Educational review

Every finding and reply must be understandable by an engineer who completed a coding bootcamp, has
practical coding experience, and has not completed a university/CS bachelor curriculum. The review
must not assume academic coursework in algorithms, operating systems, compilers, distributed
systems, security, or architecture. It defines only the concepts relevant to this finding, connects
evidence to an observable consequence, supplies a reproduction or direct inspection path, and
offers a bounded remedy. It remains concise and never turns the thread into a lecture. This target
describes prior educational access, not capability or potential.

### BR-3: Critical appraisal, not compliance theater

The fixer must evaluate whether a finding is correct, current, in scope, and proportionate. It may
reject a finding with evidence, defer adjacent work to a linked follow-up, or ask for clarification.
No disposition may be a bare “yes,” “done,” or “disagree.”

### BR-4: Bounded, quality-preserving automation

AI review should normally complete within three cycles and may autonomously attempt changed-strategy
recovery through cycle 5. Before cycle 4 or 5, the agent posts a PR-native recovery note; this is an
audit record, not a human gate. No sixth AI cycle runs. The agent escalates earlier when progress
requires human judgment or authority. Reaching the cap does not convert outstanding defects into
approval; it transfers an unsafe next decision to a human and leaves the PR blocked.

### BR-5: PR-native traceability

The PR artifact must show cycle identity, scope anchor, current head, specialists/probes used,
findings, dispositions, linked follow-ups, recovery decisions, checks, and merge rationale. The
human-readable record is authoritative. Machine metadata is optional and secondary only when a
demonstrated consumer exists.

### BR-6: No scope creep

The loop may repair defects introduced by the PR and all occurrences of the same defect class. It
must not add a second problem. Adjacent improvements become linked follow-ups from the finding
thread; informational teaching comments never create blocking work.

### BR-7: Minimal machinery

The default solution is clearer governance, agent instructions, templates, and native GitHub
behavior. New code or a new automation surface is prohibited unless execution records:

1. a reproduced failure that prose and existing GitHub controls cannot address;
2. the smallest possible mechanism;
3. ongoing ownership, tests, failure mode, rollback, and deletion criteria; and
4. a written cost/benefit comparison showing the mechanism is necessary.

### BR-8: Cross-repository coherence without blind copying

`ose-public` defines the canonical general process first. `ose-private` consumes only the matching
public PR and source SHA after they merge green, then adapts the portable semantics to its own
sharding, licensing, infrastructure constraints, and current state. Cross-repository **sync** is
declared only after both sides of a wave merge green and means semantic agreement with reasoned
deviations, not byte identity unless an existing surface contract explicitly requires it. Each repo
has separate PRs, CI evidence, review threads, and merge decisions. `[Judgment call]`

### BR-9: Coherent planning lifecycle

Plan maker, checker, fixer, execution, delivery, archival, and cleanup instructions must agree on
who owns each stage and when it occurs. Direct-push examples must not contradict a repository's
mandatory PR mode. Validation must not require an artifact that a later stage is supposed to
create.

### BR-10: Explicit large-plan decomposition

A plan spanning plan documents, repo rules, executable agent/skill bindings, conditional tooling or
code, and cross-repository propagation must decompose into ordered delivery units. Every unit names
its dependency, compatibility contract, rollback, scope boundary, and proof that `main` is useful
and coherent immediately after merge. Plan establishment precedes implementation; a rule precedes
or lands atomically with the binding that executes it; code follows a passed necessity gate; private
propagation consumes merged public semantics; closure comes last.

### BR-11: One reusable worktree per repository

Git worktrees are repository-scoped. This plan uses exactly one public worktree and one private
worktree for its entire execution, including all sequential PRs. After each merge, the same clean
worktree synchronizes from that repository's latest `origin/main` before the next delivery branch is
created. No PR receives its own worktree.

### BR-12: Integration safety for every multi-PR sequence

Every multi-PR sequence declares a lightest-fit **feature flag** strategy. The umbrella includes an
existing feature/config flag, a dormant default-off path, a compatibility bridge, ordered
activation, or another reversible mechanism. Rules/prose may use compatibility wording and ordered
activation as their flag-equivalent. The strategy must keep intermediate `main` stable, name the
rollback order, and avoid a new feature-flag framework unless independently justified under BR-7.

### BR-13: Useful and accessible PR diagrams

A PR description may include Mermaid when a dependency, architecture, sequence, or state
relationship is materially easier to understand visually. The diagram must use descriptive labels,
an accessible palette, and an adjacent prose equivalent. Decorative diagrams add review burden and
are excluded.

### BR-14: Canonical, repository-isolated rule propagation

Future implementation of every rule-bearing delivery boundary must invoke
`repo-governance/workflows/repo/repo-rules-propagation.md`; it must not manually copy rule text.
Each public run uses `isolation=current` in the one public plan worktree, completes normalization,
pre-write conflict and placement decisions, subject-scoped tidy, enforcement disposition,
generated bindings, verification/ledger reconciliation, and Step 9 delivery. Step 9 records the
portable sibling obligation, merged-green public source pin, and acceptance statement in the public
PR. Only after that source merges may a separate `isolation=current` run in the one private plan
worktree discharge it. One run touches one repository, and only one portable obligation wave may be
open. The fixed order is `PUB-A1 -> PRIV-A1 -> PUB-A2 -> PRIV-A2 -> PUB-A3 -> PRIV-A3 -> PUB-B ->
PRIV-B`, then conditional `PUB-C -> PRIV-C`.

Private discovery classifies each concern as private implementation/private-only defect, deliberate
repo-specific deviation, portable public-source defect, or explicitly byte-identical-surface
defect. A portable source defect stops private, repairs public first, supersedes the pinned source
with the correction's merged-green SHA, and revalidates only the affected class on both sides. A
wave permits initial propagation plus at most one upstream correction; a second attempted reversal
is oscillation and requires plan amendment, re-review, and human judgment. Draft copying, stacked
dependent PRs, reciprocal ping-pong, and hidden registries, bots, or validators are prohibited.
`[Judgment call]`

### BR-15: Explicitly authorized, sequential large-plan execution

The existing public worktree is the sole public execution container from plan making through plan
delivery and every later public PR. Plan making changes the six plan documents plus only the
cross-repository idea/index/link retirement explicitly authorized on 2026-08-23. That authorization
permitted one private worktree for the bounded cleanup, not private rule implementation. Formal plan
validation, staging, committing, pushing, opening either plan-document PR, and beginning
implementation require explicit user authorization for that transition; neither plan approval nor
plan merge implies the next authority. After authorized execution begins, each
delivery unit starts from current merged `origin/main`, owns one problem and an explicit ledger,
declares integration safety and rollback, and completes review/merge/evidence before the same
worktree synchronizes for the next unit. Oversized or multi-problem units stop for plan amendment
and stable-main splitting. Private work starts only when explicitly authorized, uses one reusable
private worktree, and consumes merged public semantics.

### BR-16: Convergence is designed, not counted

The process must maximize the chance of safe convergence within five cycles without weakening
review. A counted cycle starts only on a review-ready, stable head. Cycle 1 performs the complete
selected probe; the fixer closes findings as one evidence-backed batch; cycle 2 reviews repairs and
delta; cycle 3 freshly verifies the full current head. Cycles 4–5 use a different strategy recorded
in a recovery note and need no advance human approval. Resolved points are not re-litigated without
new evidence, adjacent work is deferred, and material scope change or repeated recurrence triggers
split, rework, or human escalation. The PR remains readable as a complete retrospective record for
humans even when an agent is permitted to merge it.

### BR-17: Related idea briefs retire with explicit disposition

Every dedicated public/private idea brief absorbed by this plan must be classified as accepted,
accepted in a simpler prose-first form, rejected, or independent. Accepted requirements receive an
owning delivery boundary before the brief is deleted. Rejected machinery records why it is
unnecessary. Idea indexes and live inbound links are reconciled in the same plan-document boundary;
historical evidence may name the retired idea in plain text but must not remain a broken dependency.

## Business Success Measures

No fabricated percentage or time target is introduced. Success is established by observable
properties on the first two qualifying delivery PRs after rollout in each repository:

- The PR body contains every required human-readable section and matches the current head.
- A bootcamp-trained engineer with practical coding experience can follow every blocking finding
  and reply without external agent logs or assumed university/CS coursework.
- Each unresolved thread has one explicit disposition and supporting evidence.
- No review-driven diff growth lacks an in-scope finding or same-defect-class explanation.
- The PR record contains no cycle-number contradiction.
- No AI review runs after cycle 5.
- A cycle-4 or cycle-5 run has a preceding changed-strategy recovery note.
- No later cycle repeats or reopens a disposition without recorded new evidence.
- Every retired review-process idea has a recorded disposition and boundary or rejection rationale,
  while independent ideas remain indexed.
- No new PR-process program, parser, dashboard, database, or size gate was added.
- Public and private process semantics agree, with deliberate deviations listed.
- Every completed wave links one merged-green public source pin to one merged-green private
  discharge; no later public wave opened while its predecessor obligation remained open.
- Every downstream discovery has one classification, and any portable source correction superseded
  its pin at most once and revalidated only the affected semantic class.
- Planning workflows no longer contain the named delivery/stage/archival contradictions.
- Every delivery PR identifies its predecessor, stable-main compatibility strategy, rollback, and
  bounded concern.
- `git worktree list` shows no more than one `optimize-pr-process` worktree in each in-scope repo
  throughout execution.
- Each multi-PR sequence names one lightest-fit feature-flag strategy without adding a general flag
  framework.
- A PR diagram, when present, has a prose equivalent and passes the repository Mermaid
  accessibility validation; diagrams that add no material clarity are absent.
- Every rule-bearing PR has a PR-native propagation summary, and every public sibling obligation is
  either linked to its merged private discharge or remains explicitly open.
- Every delivery transition has explicit authority evidence; no implementation begins merely
  because PLAN merged, and no dependent PR is stacked by default.

## Business Risks and Mitigations

| Risk                                              | Business effect                                                    | Mitigation                                                                                                                                    |
| ------------------------------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Numeric size heuristics become cargo cult         | Artificial slicing harms atomicity                                 | Make cohesion primary; document exceptions; keep enforcement human                                                                            |
| Five-cycle cap hides quality problems             | Defects merge because “time is up”                                 | Cap automation, not quality; remain blocked and require human split/rework/close/manual review                                                |
| Teaching requirement creates verbose reviews      | Readers stop engaging                                              | Define only relevant concepts; require one concise observable consequence, reproduction path, and bounded remedy; Teaching/FYI is nonblocking |
| Fixer rejection becomes dismissiveness            | Valid findings are lost                                            | Require evidence, same-thread reasoning, and synthesis re-check                                                                               |
| Audit requirements create a new schema product    | Maintenance burden grows                                           | Use native GitHub content first; demote unused hidden schema from mandatory status                                                            |
| Public/private drift                              | Process differs silently                                           | Pair one merged-green public source with one private semantic discharge and record reasoned deviations                                        |
| Cross-repo correction chain                       | Dependent PRs and reciprocal fixes amplify review cost             | Keep one open wave; classify discoveries; allow one upstream correction; stop a second reversal for plan amendment and human judgment         |
| Conditional CI repair expands into redesign       | Plan scope grows                                                   | Separate necessity gate; only surgical existing-machinery fixes may proceed                                                                   |
| Intermediate PR leaves `main` contradictory       | Other contributors inherit an unusable state                       | Declare dependency and feature-flag strategy; pair rules and executable bindings when separation is unsafe                                    |
| Worktree-per-PR multiplies state                  | Stale branches and cleanup risk accumulate                         | Reuse exactly one repo-scoped worktree and synchronize after every merge                                                                      |
| Diagram becomes decoration or excludes readers    | PR description becomes noisier or inaccessible                     | Require material clarity, accessible palette/labels, and adjacent prose equivalent                                                            |
| Rules are copied outside canonical propagation    | Placement conflicts, duplicates, or sibling drift become invisible | Use repo-isolated workflow runs; public Step 9 records the obligation and a separate post-merge private run discharges it                     |
| Plan approval is mistaken for execution authority | Work begins before the user intended                               | Record each transition; PLAN merge returns to a synchronized wait until execution is explicitly commanded                                     |
| Oversized work is improvised or stacked           | Reviewability and stable-main guarantees collapse                  | Amend and re-review the plan, split at a coherent reversible boundary, and merge before starting a dependent successor                        |

## Business Non-Goals

- Increase the number of reviewers, agent calls, or mandatory comments for its own sake.
- Guarantee that every PR fits a universal numeric size.
- Replace human technical judgment with an automated approval score.
- Make a PR artifact immutable; GitHub content is durable and auditable, but can still be edited or
  deleted by authorized actors.
- Create repository-wide byte identity where the existing surface contract requires only semantic
  parity, or add a cross-repository obligation registry, synchronization bot, or validator.
- Optimize application delivery, deployment, or infrastructure behavior outside the PR and
  planning process.
