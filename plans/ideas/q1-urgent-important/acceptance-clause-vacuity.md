# Acceptance clauses that cannot fail

One-line summary: a whole class of acceptance clause in this repo's plans is unfalsifiable — it
passes no matter what the world looks like — so it certifies nothing while reading exactly like a
discharged check; clauses should state what makes them **fail**, not only what makes them pass.

> Surfaced 2026-07-21/22 during `bare-repo-governance-hardening` execution (Phases 2-6, five
> distinct instances).

## Problem / context

Five vacuous clauses were caught inside a single plan, each vacuous for a different reason; a
sixth shape surfaced later in an unrelated plan and is listed alongside them:

- **Wrong identifier.** A step asserted two briefs were absent from a sibling, and its clause
  grepped for the slug of the one that genuinely _was_ absent. The clause was well-formed,
  falsifiable in principle, and pointed at the wrong string — so it exited 1 vacuously and could
  never have detected the brief that was actually present. Indistinguishable from passing.
- **Measured before the fact was fetchable.** The terminal-reconcile clause
  `git rev-list --left-right --count origin/main...main` printed `0 0` when run **before**
  `git fetch`, because both refs were equally stale — a clean reading produced by ignorance. After
  fetching, the true reading was `1 0`.
- **Executor could not run the named command.** Phases 2 and 3 had acceptance clauses naming
  literal shell commands, but the executing agents had no `Bash` tool. Both substituted a
  differently-scoped tool and reported plausible numbers as the clause's result — disclosed, which
  is the good outcome, but the substitution was **not uniform in reach**. The markdown gates could
  not be run at all and were skipped entirely, and five markdownlint violations reached the
  pre-commit hook undetected.
- **The named target is a no-op.** A clause citing an Nx target that is an `echo` stub is vacuous by
  construction; it reports success for a command that does nothing.
- **A planning-time count frozen into the clause.** A clause read "the two-pager names each of the
  22 directories". The 22 was counted while the plan was written; execution re-counted 23. The
  clause is falsifiable in form, but it now certifies conformance to a stale number, and an
  executor who trusts it produces a deliverable that fails its own check. Counts discovered at
  authoring time belong in the prose as estimates; the clause should name the command that derives
  the number, not the number.
  Surfaced 2026-08-18 in `repo-clean-up`.
- **A tooling layer rewrote a hard error into a clean pass.** A worktree-removal precondition phrased
  as "`git stash list` is empty" was checked in a bare repo. Raw `git` answers
  `fatal: this operation must be run in a work tree` and exits non-zero — the command cannot run
  there at all. Through this repo's RTK filter, the same invocation prints **`No stashes`** and exits
  **0**. Ten stashes actually exist on that repo's `refs/stash`
  (`git rev-list --walk-reflogs --count refs/stash` → `10`). So the clause reports the exact reading
  that discharges it, in a situation where it is not merely false but unrunnable. Note the clause was
  never written into any governance document — it lived only in an orchestrator's briefing text —
  which is why no doc-level review would have caught it. Same family as the `grep`-is-ugrep `-L`
  false-zero: a wrapper silently changes a command's failure semantics, and the clause reads the
  wrapper's answer.

The common shape: everyone verifies that the clause **passes**. Nobody verifies that it **could
have failed**. The fifth instance sharpens this — a clause can pass while naming a command that
_cannot execute_ in the environment it was pointed at, because a filtering layer supplied a
plausible answer on the failing command's behalf.

**Additional 2026-08-02 instances** (`vercel-function-cost-reduction`): an execution plan disabled
the paid aggregate-observability product, then later required the aggregate query it had made
unavailable; a `Googlebot` user-agent spoof was used to test a control that authenticates crawler
identity by source IP; and an apex-domain remediation was assigned to Vercel before verifying that
the apex was actually served elsewhere. These are all the same failure class: an acceptance clause
or execution step describes a world its named control plane cannot observe or change.

**Related sub-class — self-contradictory acceptance steps** (further instances 2026-07-23,
`ayokoding-learning-path-01-url-restructure` Phases 1-2): a step is not vacuous but internally
inconsistent — it mandates X and, elsewhere in the same phase, mandates not-X, so no execution can
discharge it as written. Three concrete cases: (a) DD-49 required a childless section index to carry
a hand-written body sentence _and_ to pass `validate-indexes`, but the index generator rewrites every
section `_index.md` body from its live children, erasing the sentence — mutually exclusive until the
prose moved to a generator-preserved `description:` frontmatter field. (b) A pure-rename proof scoped
`git diff --cached --summary -M` to the destination pathspec only, but git cannot pair a rename when
the source side is excluded — the commit-level unscoped `git show --summary -M <sha>` is the form that
proves it. (c) A Gherkin acceptance assumed a standing legacy `_index.md` tree that a later same-plan
`git mv` + root-deletion step removes, so the acceptance prose and the implementation reality diverged.
Same enforcement owner as the vacuity class (`plan-checker` at authoring time): a consistency check
that cross-reads a phase's later overrides against its earlier acceptance prose, and flags a step
whose own two halves cannot both hold.

### Three more instances, and the largest one yet (2026-08-21)

`repository-onboarding-readme-refresh` produced three, from Phases 1 and 2. The first two are the
brief's already-pass and never-pass poles at a scale it had not yet recorded; the third is a shape
it does not cover.

**Never-pass, times 745.** 745 of that plan's 814 ledger rows shared one acceptance template naming
a bare, unscoped `md links validate`. At the recorded revision that command reports `found 312
broken links` — every one inside `plans/done/**`, a tree the same ledger classifies
`historical-exempt` and forbids editing. The clause could never pass for any row, whatever the
executor did to that row's own document. Seven self-checks read it as well-formed; the independent
reviewer at the phase gate was the first to **run** it.

**Passes on nothing.** `git ls-tree -r --name-only <sha> -- '*.md'` returns zero paths and exits 0 —
`git ls-tree` does not accept glob pathspec magic, so the wildcard matches literally. The true count
was 9,294. An inventory clause whose acceptance is "every path is classified" passes trivially on an
empty list, which is the most dangerous form this failure takes: it looks like success. The fix is a
non-zero floor plus a cross-check against an independent enumerator.

**A shape this brief does not yet cover: the carve-out that becomes a loophole.** A clause read
"every npm script the document names resolves." Swept across the corpus that is wrong three
different ways for the _same string_: a script named inside a fenced example teaching a general
pattern is not a claim about this repository; a script labelled "Future" or "Implementation pending"
makes the document accurate, and a literal check would fail it for being honest; the same
non-existent script named with no qualifier in a sibling file is a real defect the check should
catch. So the clause needs an exemption — and an exemption is itself a loophole any unresolvable
command can hide behind, unless it passes **on the stated framing being present** rather than on the
executor's judgement. A clause can be non-vacuous and still be wrong if it cannot tell a claim from
an illustration.

## Why now

These four were caught only because a PR-review cycle and a knowledge-capture phase happened to
look. A vacuous clause leaves no trace — it produces a green tick — so the population of them
already in `plans/backlog/` and in the plan-authoring agents' output is unmeasured and, by
construction, invisible to any check anyone currently runs. Each new plan adds more. The cost is
already visible: one of the four let a false premise through into an executed propagation step, and
another let five lint violations reach a git hook.

## Prior art / precedents

- **Maker-Checker-Fixer pattern** — the natural home for "a disclosed substitution is not a
  discharged check", the rule the `Bash`-less-executor instance argues for.
  [maker-checker-fixer](../../../repo-governance/development/pattern/maker-checker-fixer.md)
- **Subagent Orchestration Convention** — where a briefing rule belongs: match the executor's tool
  grant to the commands its acceptance clauses name, before dispatch.
  [subagent-orchestration](../../../repo-governance/development/agents/subagent-orchestration.md)
- **`plan-checker` / `plan-execution-checker` agents** — the existing validators of plan quality
  and executed-plan quality; whichever gains a falsifiability check, this is where it lands.
  [plan-execution workflow](../../../repo-governance/workflows/plan/plan-execution.md)
- **Mutation testing** — the established software-testing analogue: a test suite is only trusted
  once a deliberately broken program makes it fail. The same argument applied to acceptance clauses.
- **`propagation-checklist-under-coverage`** — the sibling brief; several of its expired premises
  were protected by clauses from this class.
  [brief](../q2-not-urgent-important/propagation-checklist-under-coverage.md)

## Proposed direction (sketch)

- **Falsifiable in both directions.** Every acceptance clause states the reading that makes it fail
  alongside the reading that makes it pass. "Returns 0" is half a check; "returns 0 now, and would
  return non-zero if X were present" is a whole one.
- **Simulate the negative case before trusting it.** For a clause that must exit non-zero pre-edit
  and zero post-edit, confirm both halves — a pre-state assertion that already holds is a signal the
  clause is measuring the wrong thing, not a head start.
- **Check the executor's tool grant against the commands the clause names.** A phase whose gate is
  written in shell commands needs an executor that can run shell commands. A disclosed substitution
  is a finding, not a pass.
- **Scope the gate to everything the phase touched.** A phase that edits markdown lints every path
  it edited, not only its headline directory.
- **Refuse no-op targets as evidence.** Read a target's actual command before citing it in a clause.
- **Confirm the named command can run where it is pointed, unfiltered.** A clause whose command is
  rewritten by a wrapper (RTK, the `grep`-to-ugrep shim) must be spot-checked through the raw
  binary at least once, because a wrapper can turn a `fatal:` into a clean pass. Corollary for
  bare repositories specifically: any clause phrased over the working tree, the index, or the stash
  is unrunnable there by construction, and `refs/stash` is repo-level rather than per-worktree, so
  emptiness of the stash is not a statement about any one worktree even where it can be read.

## Rough scope & non-goals

In scope: a falsifiability requirement in the plan-authoring surface; the "disclosed substitution is
not a discharged check" rule in the maker-checker-fixer pattern; the tool-grant/clause-command match
in the subagent briefing convention.

Out of scope (for now): a mechanical validator that detects vacuity (interesting, probably
undecidable in general, and certainly premature before the rule exists); rewriting acceptance
clauses in already-archived plans; changing what the checkers validate structurally.

## Risks & open questions

- Requiring an explicit failure condition on every clause makes plans longer, and length is already
  in tension with the instruction-size and readability pressures elsewhere. Whether the requirement
  should apply to all clauses or only to those asserting absence/pre-state is unresolved. (open)
- Which agent owns enforcement — `plan-checker` at authoring time, `plan-execution-checker` at
  verification time, or both — changes what the rule can look like. An authoring-time check can only
  inspect wording; an execution-time check could actually attempt the negative case. (open)
- "Simulate the negative case" is cheap for a grep and expensive for anything that mutates state.
  The rule needs a stated boundary or it will be quietly ignored on the expensive cases.

## What success looks like + promotion signal

Success: a new plan's absence- and pre-state-asserting clauses each name their failure reading, and
a spot-check of a sample of them confirms each would actually have fired against a seeded
counterexample. Secondary: no phase in a new plan is dispatched to an executor that cannot run the
commands its own gate names.

Ready to promote once the enforcement-owner question is answered — the rule's shape depends on
whether it is checked as text or as behaviour.
