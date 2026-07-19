# 30 · Software Engineering Practices (Annotated-concept, Python \*)

**prd row**: Pass 2 · Depth, Design & Craft · Annotated-concept · Python \* · Learn 130 / Drill 230 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the professional practices that turn code into engineering — version control (the Git
model + trunk-based development), testing discipline, code quality, CI/CD, collaboration/process, and
debugging/observability basics. Testing mechanics come from
[`15-software-testing`](./15-software-testing.md); this topic is the surrounding workflow, driven from the
`git` CLI (DD-17). It underpins the whole repo's own conventions.

## Why this exists · the big idea

- **The problem before the solution**: code that works on your machine isn't engineering — without version
  control, tests, review, and CI, a growing team and codebase regress faster than they progress.
- **Keep-this-if-you-forget-everything**: the practices exist to make change _safe and reversible_ — small
  commits, green tests, and an automated gate let you move fast _because_ you can always undo.
- **Big ideas touched**: `correctness-vs-pragmatism` (CI gates, coverage, and review are risk management,
  not bureaucracy), `coupling-vs-cohesion` (trunk-based dev and small PRs cut the merge coupling between people).

## Prerequisites

- **Prior topics**: [topic 5 Just Enough Bash](./05-just-enough-bash.md) (terminal + `git` CLI),
  [topic 15 Software Testing](./15-software-testing.md) (the testing discipline this workflow wraps), and a
  working app from Pass 1 (e.g. [topic 11 Backend Essentials](./11-backend-essentials.md)) to practice on.
- **Tools & environment**: a macOS/Linux terminal; **`git`**; **Python 3.x** with a linter/formatter
  (`ruff`/`black`) and `pytest`; a CI runner concept (GitHub Actions YAML shown, run locally where possible).
- **Assumed knowledge**: basic `git` add/commit; running tests from the CLI; editing YAML.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: Conventional Commits is at a stable final **v1.0.0** (no newer major). `git` CLI
  and GitHub Actions YAML schema broadly stable — standard spot-check at authoring. (conventionalcommits.org)
- 2026-07-12 — verified (CORRECTION of framing): as of 2026 (**Ruff 0.15**), `ruff format` is a credible
  full **Black replacement** (>99.9% output-identical) and Ruff is the de facto single consolidated tool
  (replaces flake8 + isort + Black + pyupgrade in one binary). Prefer "**ruff** (formatter + linter,
  Black-compatible)" over teaching `ruff` + `black` side by side. Not a hard error (both still function).
  (astral.sh / docs.astral.sh/ruff)
- 2026-07-12 — DD-35 primary-source pass (fetched and read each): **SemVer 2.0.0**
  (<https://semver.org/>) — MAJOR/MINOR/PATCH tied to incompatible / backward-compatible-addition /
  backward-compatible-fix. **Keep a Changelog 1.1.0** (<https://keepachangelog.com/en/1.1.0/>) — six
  categories `Added`/`Changed`/`Deprecated`/`Removed`/`Fixed`/`Security` under a `## [Unreleased]` heading.
  **pre-commit** (<https://pre-commit.com/>) — config file is exactly `.pre-commit-config.yaml`; commands
  `pre-commit install` and `pre-commit run --all-files`. **`gh` flags** verified off the official manual:
  `gh pr create` (`-t/--title`, `-b/--body`, `-B/--base`, `-d/--draft`, `-f/--fill`), `gh pr review`
  (`-a/--approve`, `-c/--comment`, `-r/--request-changes`, `-b/--body`), `gh pr view` (`-c/--comments`,
  `--json`). **`git bisect`** (<https://git-scm.com/docs/git-bisect>) — `start`/`bad`/`good`/`run`/`reset`/
  `skip`; `run` exit codes 0=good, 1–127 (except 125)=bad, 125=skip. **`git log --pretty` `%s`** = commit
  subject. **Technical Debt Quadrant** (Fowler) — prudent/reckless × deliberate/inadvertent. **Feature
  toggles** (Hodgson, martinfowler.com) — release/experiment/ops/permission categories. **Google
  eng-practices Small CLs** — "~100 lines reasonable, ~1000 too large" (non-absolute). **Scrum Guide 2020**
  — Definition of Done. **#NoEstimates** (Woody Zuill, ~2012) — questions estimate value, not a blanket ban.
- 2026-07-18 — RESOLVED (supersedes the 2026-07-12 [Needs Verification] entry): `gh pr view --json
reviewDecision` maps to GitHub's GraphQL `PullRequestReviewDecision` enum, confirmed off the primary
  schema reference at <https://docs.github.com/en/graphql/reference/pulls> — exactly three values,
  `APPROVED`, `CHANGES_REQUESTED`, `REVIEW_REQUIRED` (casing as already used in this doc). The
  `reviewDecision` field itself is nullable (no dedicated "no decision" enum member — the field returns
  `null` when there's no review activity yet).
- 2026-07-18 — re-confirmed (no material change since 2026-07-12): Conventional Commits still at stable
  **v1.0.0** (conventionalcommits.org/en/v1.0.0/); **SemVer** still at **2.0.0** (semver.org); `gh pr
create`, `gh pr review`, `gh pr view` flags (as cited above) unchanged per the official `gh` manual
  (cli.github.com/manual), despite the `gh` CLI binary itself advancing to **v2.96.0** (released
  2026-07-02, github.com/cli/cli/releases) in the interim. **Ruff** remains on the **0.15** minor line
  (patch releases through 0.15.16/0.15.17 as of this check, astral.sh/blog/ruff-v0.15.0) — the
  Black-replacement/consolidated-tool framing is unaffected.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Annotated-concept). Each example below cites the co-NN it exercises. -->

- **co-01 · trunk-based-vs-feature-branch** — short-lived branches integrated frequently to trunk trade
  release isolation for lower merge-conflict cost, and the right choice depends on team size and release
  cadence, not fashion.
- **co-02 · conventional-commits** — the Conventional Commits format (`<type>[optional scope]: <description>`,
  an optional `!` and `BREAKING CHANGE` footer) encodes intent and severity directly in the commit message.
- **co-03 · semantic-versioning** — SemVer's MAJOR.MINOR.PATCH rule ties a version bump to the exact kind of
  API change: incompatible, backward-compatible addition, or backward-compatible fix.
- **co-04 · changelog-discipline** — a curated changelog using Keep a Changelog's
  Added/Changed/Deprecated/Removed/Fixed/Security categories, kept under an `Unreleased` heading, tells a
  human what changed — distinct from the raw commit log.
- **co-05 · code-review-etiquette** — a review names blocking issues versus nits, gives feedback promptly, and
  stays respectful of the author, per established reviewer/author guidance.
- **co-06 · pr-hygiene-and-size** — a pull request scoped to one concern and kept small (roughly a
  "reasonable" ~100-line bar) reviews faster, more thoroughly, and rolls back more safely than a sprawling one.
- **co-07 · pr-workflow-with-gh-cli** — creating, reviewing, and inspecting a pull request from the terminal
  (`gh pr create`/`gh pr review`/`gh pr view`) closes the review loop without leaving the CLI.
- **co-08 · ci-pipeline-stages** — a minimal pipeline runs lint, then test, then build as ordered, gated
  stages so a failure stops early and cheaply.
- **co-09 · quality-gates** — a required check blocks a merge on failure, while a lower-value check should
  demote to a warning, so gates protect production without ossifying into pure ceremony.
- **co-10 · pre-commit-hooks** — a `.pre-commit-config.yaml`-driven hook framework catches a class of defect
  before it ever reaches a commit or a CI run.
- **co-11 · test-pyramid-as-practice** — day-to-day, the pyramid's "many fast, few slow" shape is a design
  choice a reviewer can name and flag when a change skews it.
- **co-12 · coverage-as-signal-not-target** — a coverage percentage is a proxy for testedness, not proof of
  correctness, and turning it into a hard target invites assertion-free tests.
- **co-13 · systematic-debugging-practice** — debugging as a practice is a disciplined loop (hypothesize,
  change one thing, observe) plus bisection to halve the search space, applied before reaching for a fix.
- **co-14 · refactoring-cadence** — continuous small refactors, folded into ordinary feature work, beat a
  deferred big-bang rewrite for both risk and cost.
- **co-15 · boy-scout-rule** — leave the code you touch slightly cleaner than you found it, as a tiny
  incidental improvement, not a separate crusade.
- **co-16 · technical-debt-tracking** — naming a shortcut's quadrant (Fowler's prudent/reckless ×
  deliberate/inadvertent) and logging it with an owner keeps debt a visible, prioritizable backlog item
  instead of a silent tax.
- **co-17 · documentation-as-code** — docs colocated with the code, versioned in the same repo, and reviewed
  in the same PR resist the drift a separate wiki invites.
- **co-18 · adr-as-engineering-practice** — a hard-to-reverse, architecturally significant code decision earns
  a linked ADR; a routine one does not.
- **co-19 · estimation-pitfalls-and-noestimates** — hour-based estimates fake a precision that does not exist,
  and the #NoEstimates critique asks whether some decisions can be made well without estimating at all.
- **co-20 · pairing-and-mobbing** — two (pairing) or a whole team (mobbing/ensemble) working one problem at a
  shared keyboard trades solo throughput for shared context and fewer defects, worth it for high-risk or
  unfamiliar work.
- **co-21 · definition-of-done** — an explicit, shared checklist (tests pass, docs updated, reviewed) gates
  when work actually counts as finished, per the Scrum Guide's framing.
- **co-22 · feature-flags-as-a-release-decoupler** — a release toggle ships incomplete code to trunk disabled,
  decoupling deploy from release and enabling trunk-based development; ops/experiment/permission toggles serve
  different lifespans.
- **co-23 · incident-hygiene-and-blameless-response** — detect, then mitigate, then root-cause an incident,
  and write it up in blameless, actor-neutral language that treats failure as systemic.

## Tensions & trade-offs — when NOT to reach for this

- **Process vs velocity**: every gate — review, CI, required coverage — trades throughput for safety. On a
  solo throwaway prototype the full ceremony is pure drag; on a shared production system skipping it is how
  you get a 3am incident. The skill is dialing ceremony to the blast radius, not maxing or zeroing it.
- **Branching models**: trunk-based development optimizes for integration frequency and small diffs;
  long-lived feature branches / GitFlow optimize for release isolation but pay in merge hell. Team size,
  release cadence, and review culture decide — neither is universally right.
- **Coverage as a target**: a coverage number is a proxy, and chasing 100% tests trivia and breeds
  assertion-free tests. Goodhart's law bites — the moment a metric becomes a target it stops measuring what
  you wanted.

## Lineage — why it beat the alternative

- These practices are scar tissue from specific, expensive failures. Version control (SCCS → CVS → SVN → Git)
  grew because coordinating shared code by hand lost work; continuous integration (Kent Beck / XP, late 1990s)
  answered the "integration hell" of big-bang merges; conventional commits and trunk-based dev answered the
  review-and-conflict costs that long branches produced at scale; DevOps / CI-CD (from ~2009) collapsed the
  dev↔ops wall that made releases rare and terrifying. The through-line: each practice removed one class of
  recurring failure — so adopt a practice for the failure it prevents, not because it's on a checklist. This
  is the ground the repo's own conventions and [`32-software-product-engineering`](./32-software-product-engineering.md) /
  [`09-project-management`](./09-project-management.md) build on.

## Worked examples

Colocated under `software-engineering-practices/learning/code/` for runnable command sequences and CI/hook
config (`.pre-commit-config.yaml`, workflow YAML), and `software-engineering-practices/learning/artifacts/`
for non-code artifacts (changelog entries, ADRs, postmortems, decision memos). Contiguous `ex-01..ex-54`.
Every example cites the `co-NN` it exercises; every concept above is exercised by ≥1 example.

### Beginner

- **ex-01 · conventional-commit-fix** — write a commit message `fix(parser): handle empty input` — verify
  `git log -1 --pretty=%s` prints a subject matching the `type(scope): description` grammar. (co-02)
- **ex-02 · conventional-commit-feat-with-scope** — write `feat(auth): add token refresh` — verify the `feat`
  type is mapped to a MINOR bump under SemVer's rule. (co-02, co-03)
- **ex-03 · conventional-commit-breaking-bang** — write `feat(api)!: drop v1 endpoint` with a
  `BREAKING CHANGE:` footer — verify both the `!` marker and the footer independently signal a MAJOR bump.
  (co-02, co-03)
- **ex-04 · semver-bump-decision-table** — given three changes (a bugfix, a new backward-compatible option, a
  removed public method), assign each the correct SemVer bump — verify each decision matches the spec's
  "backward compatible" test. (co-03)
- **ex-05 · changelog-entry-keepachangelog** — add an `Added`/`Fixed` entry under a `## [Unreleased]` heading
  in `CHANGELOG.md` — verify the entry uses one of Keep a Changelog's six categories. (co-04)
- **ex-06 · changelog-vs-raw-commit-dump** — compare a curated changelog entry to the raw `git log` for the
  same release — verify the changelog reads as user-facing intent, not implementation history. (co-04, co-02)
- **ex-07 · trunk-vs-feature-branch-decision** — given a two-person team shipping daily and a five-person team
  on a quarterly release train, pick trunk-based or feature-branch for each — verify each pick cites the
  cadence/team-size property that drove it. (co-01)
- **ex-08 · self-review-before-request** — diff your own branch against trunk before opening a PR and fix one
  obvious issue — verify the opened PR's diff no longer contains the self-caught issue. (co-06)
- **ex-09 · pr-create-with-gh** — run `gh pr create --title "..." --body "..." --base main` — verify
  `gh pr view` shows the new PR with the given title and base branch. (co-07)
- **ex-10 · pr-size-under-100-lines** — split a 300-line change into three PRs, each under roughly a
  "reasonable" size — verify each PR's diffstat lands near the ~100-line bar cited by Google's review guide.
  (co-06)
- **ex-11 · pr-description-one-concern** — write a PR description scoped to one concern with a what/why summary
  — verify a reviewer can state the PR's single purpose in one sentence. (co-06)
- **ex-12 · request-review-with-gh** — run `gh pr review <number> --request-changes --body "needs a regression
test"` — verify `gh pr view <number> --comments` lists the new review comment. (co-07)
- **ex-13 · approve-with-gh** — run `gh pr review <number> --approve --body "LGTM"` — verify
  `gh pr view <number> --comments` lists the approval comment. (co-07)
- **ex-14 · minimal-ci-pipeline-lint-test-build** — a 3-stage pipeline (lint → test → build) with a Mermaid
  flow diagram — verify each stage is annotated and the diagram's order matches the pipeline config's job
  order. (co-08)
- **ex-15 · required-check-blocks-merge** — mark the pipeline as a required status check — verify a
  deliberately failing commit is blocked from merging. (co-09)
- **ex-16 · lint-warning-vs-blocking-gate** — classify two checks (a redundant style nit vs a failing test) as
  warn vs block — verify the blocking gate is reserved for the check that actually protects production. (co-09)
- **ex-17 · install-pre-commit-framework** — add `.pre-commit-config.yaml` and run `pre-commit install` —
  verify a subsequent `git commit` triggers the configured hooks. (co-10)
- **ex-18 · pre-commit-run-all-files** — run `pre-commit run --all-files` — verify it reports a pass/fail
  result per hook across the whole repo, not just changed files. (co-10)

### Intermediate

- **ex-19 · pyramid-shape-check-in-review** — during review, flag a PR that adds ten new e2e tests and zero
  unit tests — verify the review comment names the pyramid shape the change violates. (co-11)
- **ex-20 · coverage-number-without-assertions** — a function with 100% line coverage exercised by a test with
  no real assertion — verify the coverage number is high while the behavior is unverified. (co-12)
- **ex-21 · goodhart-coverage-target-memo** — write a short memo on why mandating "100% coverage" as a merge
  gate backfires — verify it names the assertion-free-test failure mode. (co-12)
- **ex-22 · rubber-duck-explain-the-bug** — narrate a bug sentence by sentence before touching code — verify
  the narration surfaces the wrong assumption before any code change. (co-13)
- **ex-23 · hypothesis-before-fix** — write the expected-vs-actual and one falsifiable hypothesis before
  opening the debugger — verify the hypothesis is confirmed or refuted by exactly one check. (co-13)
- **ex-24 · bisect-as-workflow-decision** — given a regression with 40 candidate commits, choose bisection over
  a linear scan and outline the `git bisect start`/`bad`/`good` sequence — verify the chosen approach is
  justified by the logarithmic step count. (co-13)
- **ex-25 · refactor-during-a-feature-pr** — refactor one nearby function while adding a feature, in a separate
  commit from the feature itself — verify the PR's history separates the refactor commit from the feature
  commit. (co-14, co-15)
- **ex-26 · boy-scout-rule-applied** — rename one poorly-named variable encountered while fixing an unrelated
  bug — verify the fix commit and the cleanup stay a tiny, incidental diff, not a drive-by rewrite. (co-15)
- **ex-27 · refactoring-cadence-vs-big-bang** — compare continuous small refactors against a proposed
  month-long rewrite for the same debt — verify the continuous option is chosen with a stated risk rationale.
  (co-14)
- **ex-28 · tech-debt-log-entry** — log a shortcut taken under deadline pressure as a tracked debt item with an
  owner and rationale — verify the entry names its quadrant (Fowler's prudent/reckless × deliberate/
  inadvertent). (co-16)
- **ex-29 · tech-debt-prioritization** — rank three logged debt items by ongoing friction rather than recency
  — verify the ranking picks the item costing the most ongoing friction, not the newest. (co-16)
- **ex-30 · docstring-to-api-doc** — write a typed Python docstring and generate its API reference page from it
  — verify the generated doc matches the function signature with no hand-duplicated copy. (co-17)
- **ex-31 · doc-in-same-pr-as-code** — update the README in the same PR that changes the behavior it documents
  — verify the PR diff contains both the code change and its doc update. (co-17)
- **ex-32 · adr-trigger-decision** — given three changes (rename a variable, swap the database, add a log
  line), decide which one earns an ADR — verify only the hard-to-reverse architectural choice gets one.
  (co-18)
- **ex-33 · adr-cross-referenced-from-code** — link a code comment to the ADR that justifies an unusual pattern
  — verify the ADR file and the code each point at the other. (co-18)
- **ex-34 · estimation-pitfall-single-point** — estimate one task in raw hours, then again in relative points
  against a reference story — verify the raw-hour estimate reads overconfident next to the relative one.
  (co-19)
- **ex-35 · noestimates-alternative** — propose a #NoEstimates-style alternative (slice smaller, count
  throughput) for a backlog where estimates keep missing — verify the alternative removes the estimate step
  without removing the ability to forecast. (co-19)
- **ex-36 · pairing-driver-navigator** — run a short pairing session with explicit driver/navigator roles and a
  timed switch — verify the roles swap at the agreed interval and both partners can explain the resulting diff.
  (co-20)
- **ex-37 · mob-programming-session** — run a mobbing/ensemble session on one hard problem with one shared
  keyboard and rotation — verify every participant can explain the final solution, not just the person who
  typed it. (co-20)
- **ex-38 · definition-of-done-checklist** — write a team Definition of Done (tests pass, docs updated,
  reviewed) and apply it to a finished PR — verify the PR is marked done only once every checklist item is
  checked. (co-21)
- **ex-39 · done-vs-done-done** — contrast a PR that's merged against one that's merged-and-deployed-and-
  monitored — verify the Definition of Done explicitly distinguishes the two states. (co-21)
- **ex-40 · feature-flag-release-toggle** — wrap an incomplete feature in a release toggle and merge it to
  trunk disabled — verify the trunk build stays green with the flag off. (co-22, co-01)
- **ex-41 · feature-flag-kill-switch** — flip an ops toggle to disable a misbehaving feature without a redeploy
  — verify the feature turns off while the rest of the system stays up. (co-22)
- **ex-42 · incident-detection-to-mitigation** — walk a Mermaid-backed timeline from alert → mitigation →
  resolution for a seeded incident — verify the timeline names a mitigation step before the root-cause fix.
  (co-23)
- **ex-43 · blameless-language-check** — rewrite a postmortem draft that names an individual into
  actor-neutral, systemic language — verify no sentence attributes the incident to a person. (co-23)

### Advanced

- **ex-44 · capstone-preview-commit-history-cleanup** — take a messy 8-commit branch and rewrite it into a
  clean conventional-commit history via interactive rebase — verify `git log --oneline` shows each commit
  correctly typed and scoped. (co-02, co-01)
- **ex-45 · semver-changelog-from-commits** — derive the correct SemVer bump and Keep a Changelog entries
  directly from a set of conventional commits since the last tag — verify the derived bump matches the
  highest-severity commit type present. (co-02, co-03, co-04)
- **ex-46 · quality-gate-pipeline-with-pre-commit** — wire `pre-commit run --all-files` as a required CI stage
  ahead of the test stage — verify a commit that fails a hook locally also fails the pipeline identically.
  (co-10, co-08, co-09)
- **ex-47 · coverage-plus-review-double-gate** — combine a coverage-not-below-baseline check with a required
  human review — verify a change that passes coverage but carries an unreviewed risky diff is still blocked.
  (co-12, co-05, co-09)
- **ex-48 · full-pr-review-cycle** — open a PR with `gh pr create`, request changes with
  `gh pr review --request-changes`, address the feedback, then `gh pr review --approve` — verify
  `gh pr view <number> --comments` shows the requested-changes comment followed by the approval comment, in
  order. (co-07, co-05, co-06)
- **ex-49 · debt-driven-refactor-with-flag** — pay down a logged debt item behind a feature flag so the
  refactor ships incrementally — verify old and new code paths coexist behind the flag until the refactor is
  verified. (co-16, co-22, co-14)
- **ex-50 · postmortem-to-tracked-debt** — turn a blameless postmortem's root cause into a tracked tech-debt
  item with an owner — verify the follow-up item traces back to the specific postmortem line that justified it.
  (co-23, co-16)
- **ex-51 · adr-plus-definition-of-done** — require a linked ADR as a Definition-of-Done item for
  architecturally significant PRs — verify a PR of that category lacking a linked ADR fails the checklist.
  (co-18, co-21)
- **ex-52 · review-etiquette-severity-labels** — label review comments by severity (blocking vs nit vs praise)
  per established reviewer guidance — verify the author can tell which comments must be resolved before merge.
  (co-05)
- **ex-53 · pairing-vs-solo-tradeoff-memo** — write a memo choosing pairing for a high-risk change and solo
  work for a well-understood one — verify the memo cites the risk/familiarity property that drove each choice.
  (co-20)
- **ex-54 · systematic-debug-in-review** — during code review, apply the hypothesize-then-bisect method to
  localize a reviewer-spotted bug to one commit before proposing a fix — verify the located commit matches the
  one a full `git bisect` run would find. (co-13, co-07)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: take a small Python feature and run it through a full professional workflow: TDD it on a
  feature branch, produce a clean conventional-commit history, wire a CI pipeline (lint → test → build)
  that gates the change, and record an ADR — ending with a green, reviewable change and its decision trail.
- **Concepts exercised**: [ ] TDD red→green→refactor (co-11, co-13) [ ] a feature branch + clean conventional
  commits (co-01, co-02) [ ] a SemVer bump + changelog entry (co-03, co-04) [ ] linting/formatting +
  pre-commit gate (co-09, co-10) [ ] a CI pipeline (lint→test→build) as a required check (co-08) [ ] an ADR
  (co-18) [ ] a self-review + review-etiquette pass (co-05, co-06, co-07).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — TDD the feature: failing test first, then implement. Verify the test
     goes red→green and `ruff`/`black` are clean.
  2. Craft the history: a feature branch with conventional commits; squash/rebase a messy sequence into a
     clean one. Verify `git log` shows a clean, conventional history.
  3. `ci.yml` — a lint→test→build pipeline. Verify each stage runs (locally via `act` or documented run)
     and a deliberately broken commit fails the gate.
  4. `adr-0001.md` — record the decision, context, consequences. Verify it references the actual change.
- **Acceptance criteria**: the feature is TDD-built and passing; history is clean + conventional; the CI
  pipeline gates green and fails on a bad commit; the ADR documents the real decision.
- **Done bar**: runnable end-to-end (pipeline gates the change) + produces the ADR + web-verified.

## Read more

**Books**

- **The Pragmatic Programmer** — David Thomas & Andrew Hunt (1999; 20th anniversary ed. 2019). Foundational collection of practical software-craftsmanship heuristics.
- **Clean Code: A Handbook of Agile Software Craftsmanship** — Robert C. Martin (2008). Widely read standard reference on naming, functions, and code-level craftsmanship.
- **Code Complete** — Steve McConnell (1993; 2nd ed. 2004). Comprehensive handbook of software construction practices grounded in empirical research.
- **Working Effectively with Legacy Code** — Michael Feathers (2004). The standard reference for safely modifying untested, poorly structured existing code.
- **Refactoring: Improving the Design of Existing Code** — Martin Fowler (1999; 2nd ed. 2018). Canonical catalog of code smells and refactorings for continuous code improvement.

**Papers & articles**

- **How to Do a Code Review (Google Engineering Practices)** — Google (continually maintained). Widely adopted industry-standard guide to code review culture, mechanics, and reviewer/author responsibilities. <https://google.github.io/eng-practices/review/>

---

← Previous: [29 · Advanced Networking](./29-advanced-networking.md) · Next: [31 · Agentic Coding](./31-agentic-coding.md) →
