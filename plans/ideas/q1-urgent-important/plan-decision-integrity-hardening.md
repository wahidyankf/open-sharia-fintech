# Plans that ship pre-loaded with their own successor

One-line summary: a plan that eliminates a design option on an unmeasured claim, or selects an option
that loses the criterion the plan itself calls its thesis, has not made a decision — it has deferred
one, and the deferred decision comes back as a second plan and sometimes a third; four authoring-time
rules plus one mechanical `plan-checker` step would catch that at authoring time, when it costs a
table row.

> Derived from the three-plan AI Model Benchmark chain in `plans/done/`. Authored as a full
> five-document plan (README, `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md`, `learnings.md`) with
> verbatim rule texts, a twelve-row deviation matrix, twenty Gherkin acceptance criteria, a ten-phase
> gated delivery checklist across seven delivery units, and a `worktree-to-pr` delivery mode. Briefly
> promoted to `in-progress/`, returned to `backlog/` on 2026-08-05, and demoted to this two-pager the
> same day.

## Problem / context

Three archived plans built and rebuilt the same page. The first
([`ayokoding-www-tools-ai-benchmark`](../../done/2026-07-30__ayokoding-www-tools-ai-benchmark/README.md))
built it with two stacked charts; the second
([`ai-benchmark-merged-chart`](../../done/2026-07-30__ayokoding-www-ai-benchmark-merged-chart/README.md))
replaced them with one merged chart — which was the first plan's own rejected Option C; the third
([`ai-benchmark-responsive-overhaul`](../../done/2026-08-01__ayokoding-www-ai-benchmark-responsive-overhaul/README.md))
deleted the second plan's SVG chart for DOM bars and renamed a class. Every trigger for plans two and
three was observable in plan one's own documents, at plan-one authoring time:

- **The requester's phrasing was scored as a design criterion.** The Stage-4 Justify table's first row
  was "Matches the stated requirement (2 charts × 3 classes)" — the requester's description of a
  candidate solution, not a statement of the reader's job. The same document calls the _second_ row
  the page's "real thesis". The selected option loses that row. The entire second plan (2,628 lines of
  plan document plus a full delivery cycle) exists to build the option that won it.
- **An option was eliminated on a responsive claim that was never rendered.** Option C was dropped
  with "degenerates to A below 768px", and its only sub-768px representation was a prose note inside
  the desktop code fence. No artefact for that option at any width below 768px was ever produced. The
  convention permitted this: it allows "an ASCII wireframe (or an inline note)" with no distinction
  between an option being carried forward and an option being dropped. The compounding cost is
  visible downstream — the second plan's sign-off recorded "responsive usability: pass at
  320/375/768/1280/1440px" while its chart labels rendered at 4.3 CSS pixels.
- **A closed identifier set mixed two naming kinds.** The dataset defined `opus`, `sonnet`, `light` —
  two model-tier proper nouns beside one weight adjective, readable off the schema with no execution.
  The third plan renamed `light` to `haiku`, by which time the identifier had reached six binding
  surfaces (feature types, two URL query values, design tokens, both i18n keys, both step-binding
  layers), and that plan's PR review caught seven stale `sortLight` sites the sweep had missed.
- **The prevention landed in one parity repo out of two.** The third plan triaged five Knowledge
  Capture learnings and routed all five into `repo-governance/`. A ten-cell grep (five routings ×
  the two parity repos) reads present in `ose-public` and absent in `ose-private` for all five. All
  ten target files exist in both repos, so this is drift, not a structural difference — the rules
  written to prevent a recurrence protect one repo out of two.

## Why now

The cost has already been paid twice, in full: two successor plans each carrying planning, gating,
worktree, PR-review cycles, CI, and deploy, spent reversing a decision the predecessor had already
recorded as suspect. Work built under the reversed decision was thrown away wholesale. Meanwhile the
window on the cheap fixes is closing continuously — a rename costs one file while the vocabulary
lives in one file, and grows with every binding surface it reaches. The retroactive-audit rationale
from this work is already load-bearing elsewhere: the 2026-08-01 renumbering of the
`ayokoding-learning-path-*` series (see [`plans/backlog/README.md`](../../backlog/README.md)) cites this
plan's retrofit reasoning for splitting plans `05`-`07` back inside the governance course band, so the
argument is in circulation even though the rules themselves are not.

## Prior art / precedents

- [UI Mockups in Plan Docs](../../../repo-governance/conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope) —
  the design-funnel convention whose Justify table and inline-note allowance are the two surfaces the
  first two rules would amend.
- [User-Facing Delivery Hardening](../../../repo-governance/development/quality/user-facing-delivery-hardening.md) —
  the existing sixteen-rule authoring-phase convention; the vocabulary-consistency rule is the same
  shape as its current members and would extend the set rather than fragment it.
- [Plans Organization Convention](../../../repo-governance/conventions/structure/plans.md) — already
  carries conditional required-section rules for `tech-docs.md` (the `## Corpus Disposition`
  requirement has the identical shape), which is the natural home for a reversal record.
- [`2026-06-19-ui-design-parity-shipped-past-green-gates.md`](../../../docs/explanation/post-mortems/2026-06-19-ui-design-parity-shipped-past-green-gates.md) —
  the direct sibling post-mortem, whose action items produced the delivery-hardening convention this
  work would extend; governed by the
  [Post-Mortems Convention](../../../repo-governance/conventions/structure/post-mortems.md).
- [`acceptance-clause-vacuity`](./acceptance-clause-vacuity.md) and
  [`propagation-checklist-under-coverage`](../q2-not-urgent-important/propagation-checklist-under-coverage.md) — sibling briefs
  in the same genre; the first shares the "a check that never fires is indistinguishable from a check
  that passes" argument, the second shares the propagation-drift failure mode.

## Proposed direction (sketch)

Four authoring-time rules, each landing in an existing convention rather than a new one, plus one
mechanical enforcement step:

- **Primary Job Criterion.** Every Stage-4 Justify table marks exactly one criterion row as the job
  the screen exists to do for its reader, traceable to an anchor in the plan's own `brd.md`. Fidelity
  to the requester's phrasing ("matches the stated requirement", "as requested") becomes an
  inadmissible criterion. When the option winning that row is not the selected one, the plan carries a
  written override record — a legitimate outcome; the silent case is what is forbidden.
- **Elimination-Grade Evidence.** The inline-note allowance applies to an option carried forward, not
  to a drop reason. No option may be eliminated on a responsive, legibility, density, or performance
  claim without either a low-fidelity wireframe at the width the claim names or a cited measurement of
  the rendered result. Deliberately asymmetric: describing an option is cheap, eliminating one is the
  irreversible act.
- **Prior-Decision Reversal Record.** A plan whose selection resurrects a predecessor's rejected
  option, or reverses a predecessor's recorded decision, says so in `tech-docs.md`, names the
  predecessor and the original reason, and assigns one disposition — `obsolete`, `never-measured`,
  `wrong-at-the-time`, or `changed-constraint`. A `never-measured` disposition must cite the
  measurement that settles the original claim; reversing an untested assertion with a second untested
  assertion is not a decision.
- **Enumerated-Vocabulary Consistency.** A closed set of user-visible identifiers reaching more than
  one binding surface states its naming rule in one sentence and lists every member against it with a
  per-member verdict. Sets reaching exactly one surface are exempt.
- **Mechanical enforcement — `plan-checker` Step 5o, the Successor-Plan Debt Scan.** Six clauses
  (seven rows, since one splits) with fixed severities: structural absences are HIGH, pattern-matched
  or inferred detections are MEDIUM so a first false positive is dismissible rather than a gate
  blocker. Matching `plan-maker` emission plus a grill question, `plan-fixer` scaffolds per clause, and
  the `plan-creating-project-plans` skill mirrored. The step is proven non-vacuous against a
  deliberately non-compliant fixture before its gate closes.
- **Two-repo propagation and retroactive application.** The identical rule text lands in
  `ose-public` and `ose-private`, with the same grep that detected the
  original drift used as the parity gate. Every plan open in `plans/in-progress/` and `plans/backlog/`
  across both repos is audited and **fixed**, not merely reported.

## Rough scope & non-goals

In scope: the four rule texts in their existing convention homes; `plan-checker` Step 5o plus the
matching `plan-maker`/`plan-fixer`/skill wiring; the non-compliant fixture that proves the step fires;
the five-routing parity backfill into both sibling repos; a blameless post-mortem of the three-plan
split; a recorded audit verdict and applied fix for every open plan in both parity repos; platform
binding regeneration wherever `.claude/` changes.

Out of scope:

- Any change to the AI Model Benchmark page, its dataset, or its tests. It is shipped, deployed, and
  archived.
- Binding the first two rules to non-UI option tables — architecture-choice or tooling-choice tables
  in `tech-docs.md`. The evidence covers the UI design funnel only, so the rules bind where the
  evidence is.
- Any deterministic validator in `apps/rhino-cli` or a CI markdown gate. Enforcement stops at the
  `plan-checker` step the repo already runs on every plan.
- Re-opening or amending any plan already under `plans/done/`. The archive is immutable; the
  post-mortem is the only new document that reads it.
- Any change to how funnel **artefacts** are produced (both-tiers rule, Excalidraw tooling, asset
  placement). This changes only how options are **scored and eliminated**.

## Risks & open questions

- Whether the rules should bind option tables beyond the UI design funnel is unresolved. The same
  failure — a winner that loses the stated purpose, an option eliminated on an untested claim — is
  clearly possible in an architecture or tooling table, but binding there applies the rules to a shape
  the evidence never covered and forces the checker to recognise option tables generically, which is
  where the false-positive risk lives. (open)
- Whether `plan-checker` is the right and sufficient enforcement owner, or whether a deterministic
  validator eventually earns its surface, is unresolved. Stopping at the checker was a deliberate
  choice to keep this governance-only, not a finding that a validator is wrong. (open)
- The Primary Job Criterion can degrade into a box-ticking row that restates whichever option the
  author already preferred. The `brd.md`-anchor requirement is the intended defence; whether it
  actually binds in practice is untested. (open)
- The retrofit's blast radius is real: 25 open plan folders at authoring time across the parity repos, some
  of them mid-execution in other sessions' worktrees. Confining retrofit edits to `prd.md` funnel
  tables and `tech-docs.md` records, and touching no `delivery.md` checkbox state, is the proposed
  containment.
- Four rules landing at once risks producing prose nobody reads, against an already-long convention
  that is also under an instruction-size budget. Each rule stating its gap, its application, and its
  enforcing clause is what is meant to keep them consequential.
- No baseline exists for the headline outcome. Three plans is not a rate, so "fewer plans exist
  principally to reverse a predecessor" stays reasoning rather than a measured target.
- One plan with propagation phases versus three sibling plans was decided in favour of one, on the
  grounds that the diff is byte-identical and three folders would create three places for the rule
  text to drift. That decision should be re-taken at promotion, not inherited.

## What success looks like + promotion signal

Success: a UI-bearing plan's Justify table names one job criterion traceable to a stated problem; no
option is dropped on a claim nobody rendered; a plan that reverses a predecessor says so and disposes
of the original reason; a multi-surface identifier set is settled while the rename is a one-file edit.
Each new rule is present in both parity repos, verified by the same per-repo grep that detected the
drift, and the ten-cell routing table reads present in every cell. Step 5o is demonstrated firing
against a deliberately non-compliant fixture, so it is proven non-vacuous rather than assumed to work.

Promotion signal — any one of these:

- The fifteen-cell parity grep is re-run and still reads absent in the ten sibling-repo cells, meaning
  the drift has persisted rather than been repaired incidentally.
- A second independent chain appears: a plan whose principal purpose is reversing a predecessor's
  recorded design decision, outside the AI Model Benchmark lineage.
- An audit of currently-open UI-bearing plans finds one whose Justify table records the selected
  option losing the row the plan itself calls its thesis.

Until one of those fires, the scope question in the first open item — funnel-only versus any option
table — is the thing to settle first, because it determines whether this is a design-funnel amendment
or a general plan-decision convention.
