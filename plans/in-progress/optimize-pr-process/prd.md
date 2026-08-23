# Product Requirements Document: Optimize the Pull Request Process

## Product Overview

The “product” is the contributor-facing PR lifecycle shared by `ose-public` and `ose-private`: how
a change is planned, described, reviewed, fixed, audited, gated, and closed. It is consumed by
humans and agents together. The human-readable GitHub PR is the primary interface and record.

## Personas

### PR author

Needs to present one coherent change, guide the reader through it, respond to valid defects, and
push back on unsound or scope-expanding requests.

### Practical junior engineer

Has completed a coding bootcamp, has practical experience writing and debugging code, and has not
completed a university/CS bachelor curriculum. Needs findings and replies that respect that
experience while explaining only relevant concepts, without assuming academic coursework in
algorithms, operating systems, compilers, distributed systems, security, or architecture.

### Reviewer and synthesizer

Needs a stable scope anchor, a complete first-cycle probe, prior-cycle dispositions, and a compact
format for posting one review plus line-anchored threads.

### Fixer

Needs permission and responsibility to critically appraise findings, implement complete in-scope
repairs, reject unsound findings, defer adjacent improvements, and request clarification.

### Maintainer and auditor

Needs a bounded loop, trustworthy current-head evidence, and a PR-native record sufficient to
understand why the PR proceeded, stopped, split, or merged.

### Plan executor

Needs consistent stage ownership and delivery instructions across plan maker, checker, fixer,
execution, archival, and worktree cleanup.

## Functional Requirements

### FR-1: Human-readable PR body

Every PR body contains these sections in this order:

1. `Why` — the problem and intended outcome, stated first
2. `Scope and non-goals` with a reason for each non-goal
3. `Summary` — the conceptual change, not a file inventory or methodology log
4. `Reading Guide` ordered from entry point to supporting detail, including paths safe to skip
5. `Review Focus` — the compact set of decisions, risks, or uncertainties on which feedback is
   most useful
6. `Verification` tied to the current head, with exact reproduction where relevant
7. `Related Work` — linked plan, issue, governance rationale, or follow-up, without duplicating it
8. `Cost and benefit` when code is added

Conditional sections appear only when relevant and are deleted when empty:

- `Risk and Rollout` for compatibility, migration, breaking-change, feature-flag, or rollback facts;
- `Visual Evidence` for an accessible Mermaid diagram or compact screenshot that materially reduces
  prose, always with a prose/text equivalent.

The body is drafted early and updated as the diff changes. Its length and detail are proportionate
to the change; there is no numeric description-length rule. It uses scannable headings, short
paragraphs/bullets, and tables sparingly. Deep
evidence, research, and governance rationale are linked to the plan or canonical rule instead of
copied into the description. It contains no academic-paper-style methodology dump and no hidden-
schema-first representation. It is not frozen by the review cycle.

### FR-2: Human-scale and cohesive change

The author aims for at most 200 review-relevant, hand-authored changed lines and 10 hand-authored
files. The local upper ceiling is 400/20. A larger PR must explain why splitting would break
atomicity or comprehension and must provide an ordered reading guide. This is a human judgment
rule, not an automated rejection. `[Judgment call]`

### FR-3: Complete first-cycle review

Cycle 1 runs the complete probe set selected by the existing risk tier. The review does not reserve
known disciplines or checks for later cycles merely to create another round.

### FR-4: Junior-readable finding

Each blocking finding includes:

- the observed behavior or inconsistency;
- the observable consequence and who or what is affected;
- the relevant principle or rule paraphrased in plain language, with only unfamiliar concepts that
  matter to this finding defined;
- evidence, including the line anchor and a reproduction command, inspection path, or authoritative
  source;
- one disposition class expected from the fixer; and
- the smallest bounded remedy or a clear question.

Terms of art are defined on first use. The comment critiques the change, never the author. It
assumes practical coding ability but no university/CS coursework, stays concise, and does not
become a general tutorial.

### FR-5: Native conversation and four-way disposition

The synthesizer posts one consolidated review body and one line-anchored thread per actionable
finding. The fixer replies in the same thread with exactly one disposition:

- `fix`: what changed and why it resolves the finding;
- `reject`: why the finding is unsound, with evidence;
- `defer`: why the work is adjacent and the linked follow-up destination;
- `clarify`: what information is missing and who must answer.

The fixer resolves only a thread whose evidence-backed disposition is complete. A summary comment
does not substitute for replies. The reply uses the same practical, no-assumed-coursework baseline:
it connects its evidence to the observable result and defines only a concept needed to understand
the disposition.

### FR-6: Overt AI attribution

Every AI-authored review body, finding, reply, recovery note, and escalation ends with a
horizontal rule followed by the exact text `Generated by AI`. The marker appears after all prose
and optional secondary metadata.

### FR-7: Scope guard

The stated problem, reasons for non-goals, and linked plan/issue form the scope anchor. A PR-created
defect and complete repair of the same defect class are in scope. An adjacent improvement is
deferred from the original thread to a linked follow-up. `Teaching/FYI` comments cannot block the
loop.

### FR-8: Bounded review loop

- Cycles 1–3 are the target path; the loop exits earlier whenever the current head is safe.
- Cycle 2 reviews the fixes and current-head delta.
- Cycle 3 performs fresh final verification.
- Cycle 4 or 5 may run autonomously only after an agent-authored, human-readable recovery note
  records why another AI cycle is useful, what remains, whether scope is stable, and what strategy
  changes. The note does not require advance human approval.
- Cycle 5 is the hard maximum. No cycle 6 is started.
- At the maximum, automation stops and the PR remains blocked until a human chooses split, rework,
  close, or manual review.
- The cap never waives an unresolved defect or required check.

### FR-9: PR-native audit record

The PR itself records, in human-readable content:

- scope anchor and non-goals;
- cycle number and current head SHA;
- risk tier and probe/specialist set;
- consolidated outcome and line-anchored findings;
- every same-thread disposition and follow-up link;
- cycle-4/5 recovery notes and terminal escalation;
- current-head checks and merge rationale.

Hidden metadata is optional and secondary. It is retained only when a named, demonstrated consumer
uses it; otherwise it is removed or demoted.

### FR-10: Critical appraisal

The fixer and synthesizer prefer technical facts and data over opinions, accept an author's choice
among equally valid alternatives, and revise or reject a finding when the reply proves it unsound.
Offline decisions are summarized back into the relevant PR thread.

### FR-11: Minimal mechanism

Execution adds no new mechanical PR-process enforcement. A proposed mechanism may proceed only
through the evidence/necessity gate in [tech-docs.md](./tech-docs.md#mechanism-necessity-gate).
Existing CI machinery may be repaired only when its defect is reproduced and the repair remains
surgical.

### FR-12: Planning lifecycle coherence

Planning documentation and agent contracts identify one owner for authoring, checking, fixing,
execution verification, archival, and cleanup. Mandatory PR delivery overrides stale direct-push
examples. Validation order contains no circular dependency or future-artifact requirement.

### FR-13: Cross-repository semantic parity

Public is the canonical source. One interleaved wave lands its public PR green before private pins
that merged PR/SHA, adapts its semantics, and records every deliberate deviation. A wave reaches
**sync** only after its private discharge merges green; sync means semantic parity, not byte identity
unless an existing surface contract says otherwise. Each repository has its own PR-native evidence
and terminal state. `[Judgment call]`

### FR-14: Large-plan delivery-unit decomposition

Before execution, every large plan declares an ordered delivery-unit table spanning plan
establishment, human-facing rules/templates, executable agent/skill bindings or tooling,
conditional code, cross-repository propagation, and closure. Each unit names its predecessor,
scope/non-goals, compatibility contract, feature-flag strategy, rollback, current-head validation,
and proof that intermediate `main` is coherent. A rule and its executable binding land atomically
when separating them would create contradictory behavior.

### FR-15: Exactly one reusable worktree per repository

All PR delivery units in one repository reuse the plan's single repo-scoped worktree. After each
merge, the executor verifies the worktree is clean, fetches that repository's `origin/main`, reads
the landed diff, and switches the same worktree to the next fixed boundary branch from the merged
head. The process never creates a worktree per PR.

### FR-16: Lightest-fit feature-flag strategy

Every multi-PR sequence declares an integration-safety strategy under the umbrella term `feature
flag`: existing feature/config flag, dormant default-off path, compatibility bridge, ordered
activation, or another reversible mechanism. The lightest safe strategy wins. Prose/rules use
compatibility wording or ordered activation; conditional CI code uses an atomic tested-and-
revertible change unless an existing flag already fits. A new feature-flag framework requires its
own necessity proof and is not part of this plan.

### FR-17: Accessible diagrams only when useful

The PR body template permits, but never requires, a Mermaid diagram when architecture, dependency,
state, or sequence would otherwise be materially harder to reconstruct. A used diagram has
descriptive labels, an accessible approved palette, non-color cues, mobile-readable structure, and
an adjacent prose equivalent. A decorative or redundant diagram is omitted.

### FR-18: Canonical rule-propagation execution

Every rule-bearing delivery unit invokes
`repo-governance/workflows/repo/repo-rules-propagation.md` with `isolation=current` in the single
worktree for that repository. It completes Step 0 normalization and two-way falsifiability, the
pre-write conflict scan and placement decision, subject-scoped tidy, explicit enforcement
disposition, generated-binding regeneration, Step 8 gates/ledger reconciliation, and Step 9
delivery. The expected disposition for human-judgment PR rules is `unenforced by decision` with a
reason; `covered` is valid only when an existing gate is proven against both conforming and
violating observations. This plan creates no new validator or gate by default.

The public Step 9 PR summary records each normalized rule, destination, enforcement disposition,
supersession/eviction, manifest result, and one `ose-private` sibling obligation with its merged-green
public source pin. After that public PR merges, a separate private run consumes and discharges the
obligation in its own PR before the next public wave opens. The order is `A1`, `A2`, `A3`, `B`, then
conditional `C`, with each public/private pair completed before the next pair. One run touches one
repository; generated-report metadata never replaces the human-readable PR summary.

Private review classifies downstream findings as private implementation/private-only defects,
deliberate repo-specific deviations, portable public-source defects, or explicitly byte-identical-
surface defects. A portable source defect blocks private merge, repairs public first, supersedes the
source pin, and revalidates only the affected class. Initial propagation permits at most one such
upstream correction; a second attempted reversal is oscillation and requires plan amendment,
re-review, and human judgment. No draft copying, stacked dependent PRs, reciprocal ping-pong, hidden
registry, bot, or validator is permitted. `[Judgment call]`

### FR-19: Authorization-gated large-plan lifecycle

The current public plan worktree remains the one public worktree from plan making through the
plan-only PR and every later public delivery unit. During plan making, only the six plan documents
and the cross-repository idea/index/link retirement explicitly authorized on 2026-08-23 may change.
That authorization permitted one reusable private worktree for the cleanup, not private rule
implementation. Formal plan validation, staging, committing, pushing, opening either
plan-document PR, and beginning implementation are separate transitions requiring explicit user
authorization; plan review or merge never implies the next transition.

After authorized PLAN merge, the same worktree becomes clean and synchronized with current
`origin/main`, then waits for explicit execution authority. Execution selects exactly one fixed
unit, branches it from current merged main, restricts edits to its ledger, and verifies dependency,
integration safety, rollback, cohesion/size, and current-head checks. If it becomes oversized or
multi-problem, execution stops to amend and re-review the plan without a formal plan quality gate
unless separately authorized, then splits at a coherent stable-main boundary. Units are reviewed,
fixed, merged, evidenced, and synchronized sequentially; dependent PRs are not stacked by default.
Private execution is separately authorized, reuses the already-provisioned private worktree, and
consumes only merged public semantics. Every pause is coherent, green, reversible, and recoverable.

### FR-20: Convergence protocol

A counted review cycle may start only when the current head is stable and review-ready: the diff is
complete and self-reviewed, scope and non-goals match it, acceptance criteria are mapped, the PR
body is current, relevant local checks have run, known failures are explained, and the risk-tier
probe set is selected. CI execution alone is not a review cycle.

Within a cycle, all selected specialists review the same head and synthesis admits only
evidence-backed, consequential, in-scope, non-duplicative findings with bounded disposition paths.
The fixer appraises all findings, resolves clarification dependencies, pushes one cohesive repair
batch, reruns relevant checks, updates the body, and supplies same-thread evidence before the next
cycle. Cycle 2 reviews dispositions, repairs, and delta; cycle 3 freshly verifies the current head.
The loop exits immediately when safe.

Before cycle 4 or 5, the agent posts a recovery note naming the cause of non-convergence, remaining
blockers, scope status, and a different strategy. Human approval is not required to continue. A
material scope change, a repeated finding without a new causal explanation, an unresolved decision
requiring human authority, or a repair that breaks the size/cohesion boundary triggers split,
rework, or human escalation rather than a repeated pass. After cycle 5, unsafe work remains blocked
for human choice. Every cycle remains comprehensible to a human reading the PR before or after
merge.

### FR-21: Idea-retirement integrity

The PLAN boundary deletes the eight related public briefs only after their accepted requirements or
rejection rationales appear in this plan, removes their active idea-index entries, and rewrites live
inbound links so no current artifact depends on a deleted path. The separate PRIV-IDEAS boundary does
the same for the one private brief after merged PLAN is available to link as its authority. An idea
whose problem is independent—such as merge-queue adoption—remains indexed. Neither boundary changes
PR governance semantics or authorizes implementation.

## User Stories and Acceptance Criteria

### US-1: Author presents a reviewable PR

As a PR author, I want a clear description and bounded reading path so a human can understand the
change before reading implementation detail.

```gherkin
Scenario: A human reader can orient to the change
  Given a PR is ready for review
  When the reader opens its description
  Then the reader sees the problem and outcome, brief scope and reasoned non-goals, conceptual summary, ordered reading and skip paths, compact review focus, current-head verification, and related-work links in progressive-disclosure order
  And deep research or governance rationale is linked instead of copied as a methodology dump
  And headings, bullets, tables, conditional risk or visual evidence, and overall length remain proportionate and scannable for a human
  And any code addition states its cost and benefit
```

### US-2: Author explains a size exception

As a PR author, I want a reasoned exception path so atomic work is not split merely to satisfy a
number.

```gherkin
Scenario: A cohesive PR exceeds the preferred size
  Given a PR exceeds 200 hand-authored lines or 10 hand-authored files
  When the author asks for review
  Then the description explains why the change remains one minimal self-contained problem
  And the reading guide names the entry point, supporting paths, and mechanical paths to skip
  And no automated size rejection is introduced
```

### US-3: Practical junior engineer learns from a finding

As an engineer with bootcamp training and practical coding experience but no university/CS bachelor
curriculum, I want each finding to explain its reasoning so I can judge similar changes without
being expected to infer academic theory.

```gherkin
Scenario: A blocking finding is understandable without private context
  Given a reviewer identifies an actionable defect
  When the finding is posted to a line-anchored thread
  Then it concisely states the observation, observable consequence, reproduction or inspection path, relevant principle, and bounded remedy in plain language
  And it defines only relevant concepts without assuming coursework in algorithms, operating systems, compilers, distributed systems, security, or architecture
  And it critiques the change rather than the author
```

### US-4: Fixer resolves a valid finding

As a fixer, I want to reply where the finding was raised so future readers see the complete
decision.

```gherkin
Scenario: A valid finding is fixed completely
  Given an unresolved finding is correct and in scope
  When the fixer implements the complete same-defect-class repair
  Then the fixer replies in the original thread with the changed paths, verification evidence, and why the repair resolves the consequence
  And the reply defines only concepts needed for the disposition and assumes no university/CS coursework
  And the thread is resolved only after the fix is pushed
```

### US-5: Fixer rejects an unsound finding

As a fixer, I want to reject a false or obsolete finding so review does not become automatic
agreement.

```gherkin
Scenario: Evidence disproves a review finding
  Given an unresolved finding is contradicted by current code, rules, or authoritative evidence
  When the fixer critically appraises the finding
  Then the fixer replies in the original thread with a reject disposition and the disproving evidence
  And the synthesizer accepts the refutation or answers with specific contrary evidence
```

### US-6: Adjacent improvement does not widen the PR

As a maintainer, I want adjacent work routed out of the review loop so the current change can
converge.

```gherkin
Scenario: A reviewer notices an adjacent improvement
  Given the improvement is neither introduced by the PR nor part of the same defect class
  When the finding is triaged
  Then the fixer defers it from the original thread to a linked follow-up with a scope reason
  And the current PR gains no implementation for that adjacent concern
```

### US-7: Informational teaching remains nonblocking

As a reviewer, I want to share useful context without creating ceremonial work.

```gherkin
Scenario: A reviewer posts a teaching note
  Given the note identifies no defect that must be corrected for this PR
  When the reviewer marks it Teaching/FYI
  Then the note remains visible and educational without entering the blocking finding ledger
  And the fixer is not required to change the diff
```

### US-8: AI authorship is visible

As a human reader, I want to know which review content was AI-generated.

```gherkin
Scenario: An agent posts review-cycle content
  Given an AI authors a review body, finding, reply, recovery note, or escalation
  When the content is posted to GitHub
  Then its final lines are a horizontal rule followed by the exact marker Generated by AI
  And no machine metadata appears after the marker
```

### US-9: Standard loop completes by cycle 3

As a maintainer, I want the normal process to front-load review and converge quickly.

```gherkin
Scenario: The PR follows the expected three-cycle path
  Given cycle 1 completed the full risk-tier probe and all findings received dispositions
  When cycles 2 and 3 review the fix delta and then perform fresh final verification
  Then the loop stops at or before cycle 3 when no blocking defect remains and current-head checks pass
  And no additional cycle runs merely to reach a target count
```

### US-10: Exceptional recovery cycle is justified

As a maintainer, I want late cycles to change strategy rather than repeat the same probe.

```gherkin
Scenario: A fourth or fifth AI cycle is proposed
  Given the normal three-cycle path did not reach a safe terminal state
  When the agent posts a human-readable recovery note before the next cycle
  Then the note states what remains, why another cycle is useful, whether scope is stable, and what strategy changes
  And the next cycle is numbered 4 or 5
  And no advance human approval is required unless the agent needs human judgment or authority
```

### US-11: Automation stops at the hard maximum

As a maintainer, I want a finite AI loop that never converts exhaustion into approval.

```gherkin
Scenario: Cycle 5 finishes without safe convergence
  Given the fifth AI review cycle has completed
  When a blocking finding, audit inconsistency, or required check remains unresolved
  Then no sixth AI cycle starts and the PR remains blocked
  And a human chooses split, rework, close, or manual review without waiving the defect
```

### US-12: Auditor reconstructs the process from GitHub

As a future auditor, I want the PR itself to explain the full review/fix history.

```gherkin
Scenario: A future reader audits a completed PR
  Given the reader has access to the PR artifact but no private agent log
  When the reader follows the body, reviews, threads, replies, recovery notes, checks, and merge note
  Then the reader can reconcile every cycle, current head, finding disposition, follow-up, and terminal decision
  And human-readable GitHub content remains authoritative over optional hidden metadata
```

### US-13: Existing CI defect passes the necessity gate

As a maintainer, I want existing machinery repaired only when the defect is real and the smallest
fix is justified.

```gherkin
Scenario: Execution considers changing the existing quality-gate workflow
  Given a suspected fail-open, self-mutation, or duplicate-work defect has been revalidated on the current workflow
  When the evidence and cost-benefit record are reviewed
  Then a surgical repair proceeds only if prose and existing controls cannot safely address the reproduced defect
  And no new PR-process validator, bot, parser, or service is created
```

### US-14: Planning stages have one coherent owner

As a plan executor, I want one non-circular lifecycle so I do not push, archive, clean up, or verify
at the wrong stage.

```gherkin
Scenario: A plan moves from authoring through archival
  Given the repository requires worktree-to-pr delivery
  When maker, checker, fixer, executor, and execution-checker instructions are followed in order
  Then each artifact is created and validated before a later stage consumes it
  And archival, merge, and worktree cleanup use one consistent authority and sequence
```

### US-15: Private propagation preserves semantics deliberately

As a cross-repository maintainer, I want private rules to match public intent without exposing
private context or assuming identical file structure.

```gherkin
Scenario: Public process rules propagate to ose-private
  Given the corresponding public delivery boundary is merged green and identified by its PR and source SHA
  When the private track adapts those decisions to its current sharding and repository constraints
  Then every deliberate difference is recorded with a reason and private evidence is reviewed in its own PR before the next public wave opens
  And no private-only infrastructure information is copied into ose-public
```

### US-16: Large work decomposes into safe delivery units

As a maintainer, I want a large plan split by dependency and compatibility so each merged PR leaves
the repository stable and reviewable.

```gherkin
Scenario: A plan spans rules, executable bindings, code, and another repository
  Given the control plan is validated before implementation begins
  When delivery units are declared for plan establishment, rules and bindings, conditional code, propagation, and closure
  Then each unit names its dependency, bounded scope, compatibility strategy, rollback, and stable-main proof
  And a rule and its executable binding are paired whenever separate merges would contradict each other
```

### US-17: Sequential PRs reuse one repo-scoped worktree

As a plan executor, I want one reusable worktree per repository so multiple PRs do not multiply
stale local state.

```gherkin
Scenario: A repository track contains several sequential PRs
  Given exactly one optimize-pr-process worktree exists in that repository
  When one delivery PR merges and the next boundary begins
  Then the same clean worktree fetches and synchronizes from that repository's merged origin/main
  And no additional worktree is created for the next PR
```

### US-18: Every multi-PR sequence declares integration safety

As a contributor, I want intermediate `main` protected by the lightest reversible mechanism so I
can use the repository between delivery units.

```gherkin
Scenario: A delivery concern cannot land in one PR
  Given the sequence declares the available feature-flag strategies and current compatibility needs
  When the executor selects the lightest safe strategy before the first dependent PR merges
  Then every intermediate main remains coherent and the rollback order restores the prior safe contract
  And no new feature-flag framework or tooling is added without a separate necessity proof
```

### US-19: A PR diagram materially helps a human reader

As a reviewer, I want diagrams only when they reduce reconstruction effort and remain accessible.

```gherkin
Scenario: A PR description includes a Mermaid diagram
  Given architecture, dependency, state, or sequence is materially clearer as a visual
  When the author adds the diagram to the conditional Visual Evidence section
  Then descriptive labels, accessible colors, non-color cues, and adjacent prose communicate the same meaning
  And a decorative or redundant diagram is omitted
```

### US-20: Portable rules propagate through separate repository runs

As a cross-repository maintainer, I want canonical propagation to place and verify each rule so
manual copying cannot hide conflicts or sibling drift.

```gherkin
Scenario: A public PR-process rule carries a private sibling obligation
  Given a portable rule has a normalized statement and no unresolved higher-layer conflict
  When the public isolation-current propagation run completes Step 9 and its PR merges
  Then the PR-native summary records placement, enforcement disposition, tidy and verification evidence, the ose-private sibling obligation, and the merged-green source pin
  And a separate isolation-current private run consumes that exact public source and records how its own PR semantically discharges the obligation
  And the next public wave waits for the private discharge to merge green
  And neither run writes the other repository or creates a new validator by default
```

### US-24: Downstream discovery cannot trigger correction ping-pong

As a cross-repository maintainer, I want downstream findings classified and bounded so one defect
cannot create an unbounded reciprocal PR chain.

```gherkin
Scenario: Private review finds a portable public-source defect
  Given one portable obligation wave is open and private review is pinned to its merged-green public source SHA
  When the finding is classified as a portable public-source defect
  Then private merge stops while one public correction repairs the canonical source and supersedes the pin
  And only the affected semantic class is revalidated in public and private before private resumes

Scenario: A wave attempts a second direction reversal
  Given initial propagation and one upstream public correction have already occurred in the wave
  When another finding would reverse the correction direction again
  Then the attempt is classified as oscillation and no reciprocal correction PR opens
  And the plan stops for amendment, re-review, and human judgment

Scenario: Private review finds a non-portable concern
  Given private review discovers a concern after consuming the merged-green public source
  When the concern is classified as a private implementation defect, private-only defect, deliberate repo-specific deviation, or explicitly byte-identical-surface defect
  Then the private PR records and handles the concern under that class without changing the portable public source
  And byte-identity handling occurs only where an existing surface contract explicitly requires it
```

### US-21: Operator executes a large plan without crossing authority or stability boundaries

As a plan operator, I want explicit transitions and one sequential worktree per repository so a
large plan remains reviewable and recoverable from plan making through its final PR.

```gherkin
Scenario: A fully authorized plan proceeds through one bounded delivery unit
  Given the plan documents and authorized idea retirement were authored in the sole repo-scoped plan worktrees
  And the user authorized the formal plan gate, plan delivery, and full execution on 2026-08-23
  When the PLAN and PRIV-IDEAS PRs merge and the next fixed public unit begins
  Then the same clean synchronized worktree branches that unit from current origin/main and edits only its ledger paths after dependency, integration-safety, rollback, and validation checks
  And an oversized or multi-problem unit stops for plan amendment and stable-main splitting without stacking dependent work or invoking a formal plan gate unless separately authorized
  And review, fix, merge, evidence, and synchronization complete before the next unit while adjacent feedback is deferred and every pause stays coherent, green, reversible, and recoverable
```

### US-22: Agent converges without waiting for a routine human gate

As a maintainer, I want the agent to use every allowed cycle deliberately and escalate only when
human judgment is genuinely needed.

```gherkin
Scenario: A review progresses from readiness through autonomous recovery
  Given the current head is complete, self-reviewed, scoped, documented, locally checked, and assigned one complete risk-tier probe
  When cycle 1 reports all admitted findings and the fixer closes them as one evidenced repair batch
  And later cycles review only dispositions, current-head delta, repair risk, and fresh final safety without re-litigating settled points absent new evidence
  Then the target path exits at or before cycle 3 when the current head is safe
  And cycle 4 or 5 may proceed after an agent-authored changed-strategy recovery note without human pre-approval
  But material scope change, repeated unexplained recurrence, authority-dependent judgment, or an unsafe result after cycle 5 blocks automation before cycle 6 for split, rework, or human decision
```

### US-23: Related idea briefs retire without losing valid requirements

As a maintainer, I want one authoritative plan instead of overlapping idea briefs and broken links.

```gherkin
Scenario: Public and private review-process ideas are consolidated
  Given each related idea has been read and compared with the human-first five-cycle contract
  When an idea is accepted, simplified, rejected, or classified as independent
  Then every accepted requirement has an owning delivery boundary before its source brief is deleted
  And every rejected proposal has a rationale while every independent idea remains indexed
  And PLAN plus the separately authorized PRIV-IDEAS boundary remove active index entries and live inbound links without implementing a rule
```

## Non-Functional Requirements

- **Readability**: a bootcamp-trained engineer with practical coding experience can understand the
  review without decoding agent internals or relying on university/CS coursework.
- **Human durability**: every PR remains coherent to a human who reads the entire artifact during
  review or retrospectively after merge, regardless of who authored, reviewed, or merged it.
- **Traceability**: every material review/fix decision has a native PR location.
- **Boundedness**: no AI review beyond cycle 5; no silent size-ceiling retirement.
- **Maintainability**: prose and existing primitives are preferred; new code must clear the
  necessity gate.
- **Safety**: a cap blocks automation, not quality; unresolved defects still block merge.
- **Harness neutrality**: normative process language describes roles and artifacts; vendor-specific
  API mechanics remain in marked binding sections.
- **Repository isolation**: each repo has its own worktree, branch, PR, checks, and merge decision.
- **Wave boundedness**: only one portable sibling obligation is open, with no draft copying, stacked
  dependent PR, or second cross-repository reversal.
- **Intermediate stability**: every merged delivery unit leaves `main` usable and has a stated
  rollback path.
- **Diagram accessibility**: optional PR diagrams pass the same accessibility and Mermaid checks as
  repository documentation.

## Product Non-Goals

- A live dashboard or cross-PR analytics product.
- Automatic scoring of reviewer or author performance.
- Mandatory approval counts or branch-protection configuration changes.
- Replacement of the existing risk-tier classifier with a new service.
- A promise that native GitHub artifacts are immutable or permanent.
