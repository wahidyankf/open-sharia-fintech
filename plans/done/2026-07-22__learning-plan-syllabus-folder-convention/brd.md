# Business Requirements — Learning-Plan `syllabus/` Folder Convention

## Business Goal

Close the governance asymmetry between UI-bearing and learning-bearing plans, so that a plan which
authors course or tutorial content produces its syllabus **in the right place, in the right shape,
with a written owner and a written end-of-life** — without a human intervening to redirect the
author, and without the corpus forking again.

The UI half of this problem is solved and enforced. The learning half is transmitted by example, and
example-based transmission has already failed twice in the tree.

## Business Impact

### Pain points (each verifiable on the current commit)

- **P1 — No template, so every author guesses.** The per-course format is rich (a `**Course ID**`
  header line, `**Scope note**`, a `## Why this exists · the big idea` section built from
  problem-before-solution / keep-this-if-you-forget-everything / big-ideas-touched, `## Prerequisites`,
  `## Concepts`, `## Worked examples`, `## In which paths`), and it is specified in exactly zero
  governance documents — [Repo-grounded] via a repo-wide search of `repo-governance/` for a governed
  `syllabus` artifact, which returns nothing. It exists only as 174 worked examples.
- **P2 — The format has already forked, silently.** 17 of plan 02's 120 course files render `co-NN`
  and `ex-NN` as ordered lists rather than bullets, and those same 17 omit the `**Short summary**`
  line — a 17-of-17 overlap `[Repo-grounded]`. Nothing in the repo failed when that landed, because
  nothing knows what a course file should look like.
- **P3 — Custody is decided per plan, in the moment.** Plan 02 custodies a corpus that plans 04 and 05
  consume; plans 06 and 07 each custody their own. Whether that split is the intended model or an
  accident of sequencing was never written down — [Repo-grounded]: the split is visible in
  `plans/backlog/README.md`, and no convention states a rule.
- **P4 — Archival is an unexploded charge.** Plan 02 is Wave 1; plans 04 and 05, which link into its
  corpus, are Waves 2 and 3 — [Repo-grounded] in `plans/backlog/README.md`. The custodian therefore
  archives first. Because `md links validate` runs at pre-push and in CI and only excludes
  `plans/done` as a **scan source**, a live consumer's link into a moved corpus becomes a hard push
  failure — [Repo-grounded] in `.husky/pre-push`, `.github/workflows/main-ci.yml`, and
  `.github/workflows/pr-quality-gate.yml`. Today nobody is told that in advance.
- **P5 — The cost of waiting rises monotonically.** Two of the three corpora appeared in a single
  day. A convention written now _describes_ what exists; written after a fourth plan guesses
  differently, it becomes a migration.

### Expected benefits

- A new learning-bearing plan copies a template instead of reverse-engineering a sample, so the
  format converges instead of diverging.
- A shared corpus has exactly one plan allowed to edit it, so concurrent plans cannot race on the
  same files — the same-machine, parallel-agent reality this repo already assumes.
- The archival question is answered before the first custodian archives, rather than discovered as a
  pre-push failure by whoever pushes next.
- The learning surface gains the property the UI surface already has: a checker can refuse a plan
  that skips it.

## Affected Roles

Solo-maintainer repo — these are hats the maintainer wears and agents that consume the artifacts, not
sign-off gates.

| Role / consumer                         | How this plan affects it                                                                          |
| --------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Maintainer as **content architect**     | Stops hand-redirecting authors to a sample file; points at a convention instead                   |
| Maintainer as **governance author**     | Gains one more convention to keep indexed and vendor-neutral                                      |
| `plan-maker`                            | Must require the `syllabus/` artifacts on learning-bearing plans, as it already does for UI plans |
| `plan-checker`                          | Gains a learning-side completeness step, sibling to Step 5k                                       |
| `plan-fixer`                            | Gains a scaffold action for a missing syllabus record                                             |
| `plan-creating-project-plans` skill     | Must describe the learning-bearing trigger alongside the UI-bearing one                           |
| Authors of learning-path plans 04, 05   | Gain a written statement that they consume, and may not edit, plan 02's corpus                    |
| A future syllabus conformance validator | Gains a settled format to validate — the precondition the two-pager set for building one          |

## Business-Level Success Metrics

Every metric below is an **observable check**, runnable on demand. No fabricated numeric targets.

1. **The convention exists and is indexed.**
   `grep -c 'learning-plan-syllabus' repo-governance/conventions/structure/README.md` exits 0 with a
   count ≥ 1. Before the work it exits 1.
2. **A copy-paste template exists inside the convention.**
   `grep -c 'Course ID' repo-governance/conventions/structure/learning-plan-syllabus.md` exits 0 with
   a count ≥ 1. Before the work the file does not exist and the command exits non-zero.
3. **Every existing corpus has a written custodian and disposition.**
   `grep -c 'Custodian' plans/backlog/*/syllabus/README.md` exits 0 printing a non-zero count for each
   of the three syllabus READMEs. Before the work it exits 1 (zero matches in all three).
4. **The enforcement chain names the learning trigger.**
   `grep -c 'learning-bearing' .claude/agents/plan-maker.md` exits 0 with a count ≥ 1; likewise for
   `.claude/agents/plan-fixer.md` and `.claude/skills/plan-creating-project-plans/SKILL.md`, and
   `grep -c 'Step 5n' .claude/agents/plan-checker.md` exits 0. Before the work, each of those four
   commands exits 1 — verified on the current commit.
5. **The tree still validates.** `npm run lint:md` exits 0, and both
   `rhino-cli md links validate` and `rhino-cli md readme-index validate` exit 0 — the same gates that
   run at pre-push and in CI.

_Judgment call:_ the deeper aim — "the next learning-bearing plan needs no human redirection" — has no
baseline and cannot be measured from the repo. It is the reason for the work, not a metric of it. The
nearest observable proxy is metric 4: a checker that can refuse the omission.

## Business-Scope Non-Goals

- **Not a corpus migration.** No existing course file is reformatted, moved, or renamed. The 17-file
  ordered-list cohort stays exactly as it is, explicitly grandfathered. (174 course files today;
  corpora 06/07 remain under active authorship, so the count is pinned in the census — see
  [tech-docs §Corpus Census](./tech-docs.md#corpus-census--the-derivation-basis).)
- **Not a validator.** Building a deterministic `rhino-cli` conformance check is deliberately
  deferred; a format must settle before a machine polices it.
- **Not a re-statement of the UI rule.** The `assets/` funnel is already governed and is out of
  bounds for this plan except as the shape being mirrored.
- **Not a content decision.** Nothing here decides which courses exist, what they teach, or how
  ayokoding-www renders them.

## Business Risks and Mitigations

| Risk                                                                                                            | Mitigation                                                                                                                                      |
| --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Over-specification** makes the format brittle for non-course learning content (a workshop, a tutorial series) | The template splits sections into REQUIRED / RECOMMENDED / OPTIONAL by measured frequency; only sections present in ≥ 99% of files are REQUIRED |
| **The convention describes without equipping**, repeating the failure mode it exists to fix                     | A copy-paste template block is a Phase 1 acceptance criterion, not an afterthought; the phase gate fails without it                             |
| **Codifying an accident**: the observed layout may be an artifact of one authoring session                      | The census measures all three corpora independently; only sections that agree across all three become REQUIRED                                  |
| **Custody rule conflicts with a live plan** whose sequencing already violates it                                | The rule is written to fit the live case (custodian in an earlier wave than its consumers) rather than assuming an idealized ordering           |
| **Scope creep into the UI half** or into corpus retrofitting                                                    | Both are named Non-Goals above and re-stated as out-of-scope in `prd.md`; the delivery checklist contains no step touching a course file's body |
| **Concurrent edits** to plans 06/07 while this plan executes                                                    | Phase 3 touches only the `syllabus/README.md` and `tech-docs.md` of those plans, in a worktree, after their own authoring settles               |

## Related Documents

- [prd.md](./prd.md) — the testable scenarios behind the claims above
- [tech-docs.md](./tech-docs.md) — the census that grounds P1, P2, and the template tiering
- [delivery.md](./delivery.md) — the phased execution checklist
