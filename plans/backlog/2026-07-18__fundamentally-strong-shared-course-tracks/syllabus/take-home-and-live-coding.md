# Take-Home & Live Coding (By Example, Python)

**Course ID**: `take-home-and-live-coding` · **Format**: By Example · **Language**: Python. **NEW** —
interview course.

**Scope note**: the two interview formats the whiteboard round does not cover — the **asynchronous
take-home project** (build a small, complete, reviewable deliverable on your own time) and the
**live / pair-coding session** (collaborate with an interviewer in a shared editor on a realistic
task). Complements `coding-interview`: that course drills isolated algorithmic problems; this one
drills _shipping a small piece of real software under evaluation_. A refresh for the experienced
re-entrant.

## Why this exists · the big idea

- **The problem before the solution**: take-homes and live rounds fail experienced engineers for
  non-algorithmic reasons — an over-engineered take-home that misses the actual ask, a missing README or
  tests, or a live round where the candidate goes silent, ignores the interviewer's steer, or cannot
  drive an editor fluently under observation.
- **Keep-this-if-you-forget-everything**: a take-home is _a small production PR you would be proud to
  submit_ — scoped, tested, documented, and honest about trade-offs; a live round is _pair programming_
  — think aloud, take the steer, and keep the code running at every step.
- **Big ideas touched**: `correctness-vs-pragmatism` (scope discipline: the smallest thing that fully
  satisfies the ask beats an unfinished grand design), `taming-state` (keep the code green and runnable
  at every checkpoint rather than a big-bang reveal).

## Prerequisites

- **Prior topics**: `just-enough-python`, `just-enough-bash`,
  `version-control-and-git`, and `coding-interview`.
- **Tools & environment**: a macOS/Linux terminal; Python 3.x; `pytest`; `git`; a README/Markdown
  habit; Neovim/VSCode driven fluently _without_ leaning on autocomplete during a shared session.
- **Assumed knowledge**: writing small Python programs with tests; committing incrementally with git;
  writing a clear README.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-18 — take-home evaluation rubrics (correctness, scope, readability, tests, docs, git hygiene)
  and live-round signals (communication, collaboration, editor fluency, debugging) are **stable,
  vendor-independent** practice.
- 2026-07-18 — `[Needs Verification]`: any named collaborative-editor / screen-share tool used in live
  rounds — keep the text tool-agnostic and re-verify a named tool at authoring.
- 2026-07-18 — `[Needs Verification]`: typical take-home time expectations and "please cap at N hours"
  norms vary by company and region — state as ranges, not fixed facts.

## Concepts

1. **co-01 · read-the-brief-literally** — deliver exactly what the prompt asks before anything else;
   unrequested features are scope risk, not bonus points.
2. **co-02 · scope-discipline** — the winning take-home is the smallest complete solution that fully
   satisfies the ask, finished and polished, not an unfinished larger one.
3. **co-03 · project-structure** — a reviewer-friendly layout (clear entry point, module boundaries,
   `tests/`, `README.md`) signals professional habits.
4. **co-04 · readme-as-the-front-door** — a README stating how to run, how to test, decisions made, and
   known trade-offs is often read before the code.
5. **co-05 · runnable-from-clean-checkout** — the reviewer must be able to clone, install pinned deps,
   and run/test with the documented commands and no hidden setup.
6. **co-06 · tests-that-demonstrate-thought** — tests covering the happy path, edge cases, and one error
   path show engineering judgment more than raw coverage percentage.
7. **co-07 · git-hygiene** — small, well-messaged, thematic commits tell the reviewer the story of the
   work and signal trunk-friendly habits.
8. **co-08 · dependency-restraint** — using the standard library and a minimum of pinned, CVE-clean
   dependencies keeps the deliverable auditable and reproducible.
9. **co-09 · documented-tradeoffs** — explicitly naming what was cut, deferred, or assumed turns a
   limitation into a demonstration of judgment.
10. **co-10 · error-handling-and-validation** — validating inputs and failing with clear messages
    distinguishes a toy from a small production artifact.
11. **co-11 · code-readability** — naming, small functions, and consistent style make the reviewer's job
    easy — readability is a graded axis, not an afterthought.
12. **co-12 · time-boxing-a-take-home** — respecting the stated cap and documenting what more time would
    buy is honest and scores better than an over-invested submission.
13. **co-13 · live-round-is-pairing** — a live session is collaborative pair programming; the
    interviewer is a partner to think with, not only an examiner.
14. **co-14 · think-aloud-while-coding** — continuous narration of intent and reasoning is the primary
    signal a live round scores.
15. **co-15 · take-the-steer** — treating an interviewer's hint or nudge as useful direction (not a
    trap) is a positive collaboration signal.
16. **co-16 · keep-it-running** — building in small, always-runnable increments beats a long stretch of
    broken code and a big-bang reveal.
17. **co-17 · editor-and-shell-fluency** — driving the editor, running tests, and using the shell
    smoothly under observation is itself evaluated (the raw-form-first habit pays off here).
18. **co-18 · live-debugging-out-loud** — reproducing, isolating, and fixing a bug while narrating the
    hypothesis is a strong, common live-round test.
19. **co-19 · asking-clarifying-questions-live** — surfacing assumptions and constraints early in a live
    round prevents building the wrong thing in real time.
20. **co-20 · incremental-delivery** — starting with a minimal working slice and extending it keeps a
    scoreable artifact alive throughout the session.
21. **co-21 · handling-i-dont-know** — saying what you would look up and how, rather than bluffing, is a
    credible senior signal.
22. **co-22 · submission-review-pass** — a final self-review (run it clean, re-read the README, skim the
    diff) catches the embarrassing misses before you submit.

## Tensions & trade-offs — when NOT to reach for this

- **Polish vs completeness**: gold-plating one corner while leaving the core ask unfinished loses; a
  complete, plain solution beats a partial, ornate one. Spend the marginal hour on the missing
  requirement, not the extra abstraction.
- **Framework vs standard library**: reaching for a heavy framework on a small take-home adds setup
  cost and audit surface the reviewer must wade through — justify every dependency or drop it.
- **When NOT to over-narrate**: in a live round, a running monologue that never lets the interviewer
  speak is as bad as silence — narrate intent, then pause to let the steer land.

## Lineage — why it beat the alternative

- Take-homes emerged as a fairer, lower-pressure complement to the whiteboard: they test the skills the
  job actually uses — structuring, testing, documenting, and shipping a small deliverable — that a 40-
  minute algorithm sprint cannot. Live/pair rounds emerged to test collaboration and editor fluency
  that a take-home cannot verify (and to deter take-home ghost-writing). Together they triangulate the
  candidate; this module drills both, handing forward to the [Phase 1 mock loop
  capstone](./capstone-interview-loop.md) and drawing on the raw-form-first editor fluency from the
  [prologue](./capstone-forge-ready.md).

## Worked examples

Colocated under `take-home-and-live-coding/learning/code/`. Take-home examples are small complete
projects (with README + tests); live examples are recorded pairing transcripts. Contiguous
`ex-01..ex-50`. Every example cites the `co-NN` it exercises.

> **Volume-target floor**: this syllabus lists **50** of the required **≥75** (the 75–85 By-Example/
> Primer band, floor not cap — see
> [prd.md §Volume-target bands](../prd.md#new-course--capstone-specifications)).
> The maker adds **≥25** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its by-example quality gate.

### Beginner (ex 01–17)

1. **ex-01 · restate-the-brief** — turn a take-home prompt into an explicit requirements checklist —
   verify every requirement maps to a checklist item. (co-01)
2. **ex-02 · scope-a-minimal-solution** — sketch the smallest complete design for the brief — verify no
   unrequested feature appears. (co-02)
3. **ex-03 · project-skeleton** — lay out entry point + module + `tests/` + `README.md` — verify the
   tree matches a reviewer-friendly layout. (co-03)
4. **ex-04 · write-the-readme-first** — draft run/test/decisions/trade-offs before coding — verify all
   four sections exist. (co-04)
5. **ex-05 · pin-dependencies** — pin the (minimal) deps to exact versions — verify a clean install
   reproduces them. (co-08)
6. **ex-06 · run-from-clean-checkout** — clone to a temp dir and follow the README verbatim — verify it
   runs with no extra step. (co-05)
7. **ex-07 · happy-path-test** — one test for the core requirement — verify it passes. (co-06)
8. **ex-08 · edge-case-test** — add empty/boundary tests — verify they pass or reveal a bug to fix.
   (co-06, co-10)
9. **ex-09 · input-validation** — reject malformed input with a clear message — verify the error path.
   (co-10)
10. **ex-10 · readable-refactor** — rename + split a long function for clarity — verify tests still
    green. (co-11)
11. **ex-11 · thematic-commits** — stage the work as small, well-messaged commits — verify each commit
    is cohesive and builds. (co-07)
12. **ex-12 · document-a-tradeoff** — record one deferred feature and why in the README — verify it is
    stated as a deliberate choice. (co-09)
13. **ex-13 · time-box-and-note** — cap the effort and note what more time would buy — verify the note
    is honest and specific. (co-12)
14. **ex-14 · submission-review** — final clean run + README re-read + diff skim — verify a checklist of
    the review pass. (co-22)
15. **ex-15 · clarify-live-assumptions** — a live transcript opening with clarifying questions — verify
    assumptions are surfaced before coding. (co-19)
16. **ex-16 · minimal-working-slice-live** — start a live task with a runnable one-line slice — verify
    it runs before extension. (co-16, co-20)
17. **ex-17 · think-aloud-live** — narrate intent through a small live task — verify no step is silent.
    (co-14)

### Intermediate (ex 18–36)

1. **ex-18 · take-home-cli-tool** — a complete small CLI (parse args, do work, print result) with
   README + tests — verify clean-checkout run + green tests. (co-01–co-06)
2. **ex-19 · take-home-file-parser** — parse a data file into a summary with validation + error paths —
   verify malformed input is rejected. (co-10, co-06)
3. **ex-20 · take-home-mini-api** — a tiny HTTP JSON endpoint with one route + a test — verify `curl`
   round-trips and the test passes. (co-03, co-06)
4. **ex-21 · standard-library-first** — solve a take-home without third-party deps where feasible —
   verify the dependency list is empty or justified. (co-08)
5. **ex-22 · readme-decision-log** — a README section justifying each design decision — verify each
   decision names its alternative. (co-04, co-09)
6. **ex-23 · test-a-failure-mode** — write a test proving the error path behaves — verify it fails
   before the guard and passes after. (co-06, co-10)
7. **ex-24 · coverage-with-judgment** — cover the risky paths, not vanity lines; note what is
   deliberately untested — verify the note explains the gaps. (co-06, co-09)
8. **ex-25 · git-history-tells-a-story** — a commit sequence a reviewer can follow — verify each
   message states the why. (co-07)
9. **ex-26 · reproducible-setup-script** — a `setup.sh`/`make` target that installs + runs + tests —
   verify one command bootstraps the project. (co-05)
10. **ex-27 · live-pair-feature-add** — a live transcript adding a feature while taking the
    interviewer's steer — verify a hint changed the approach. (co-13, co-15)
11. **ex-28 · live-keep-it-green** — build a live feature in increments that each pass tests — verify
    the suite is green at every checkpoint. (co-16, co-20)
12. **ex-29 · live-debug-out-loud** — reproduce → hypothesize → isolate → fix a planted bug while
    narrating — verify the transcript names the hypothesis before the fix. (co-18)
13. **ex-30 · live-editor-fluency** — drive an edit/run/test loop smoothly in the terminal editor —
    verify the transcript shows no fumbling on basic motions. (co-17)
14. **ex-31 · take-the-steer-gracefully** — a transcript where the candidate adopts a better approach
    the interviewer nudges toward — verify the pivot is acknowledged, not resisted. (co-15)
15. **ex-32 · handle-i-dont-know-live** — a moment where the candidate states how they would look
    something up instead of bluffing — verify the recovery is concrete. (co-21)
16. **ex-33 · incremental-refactor-live** — refactor live in small safe steps under time pressure —
    verify tests stay green throughout. (co-16, co-20)
17. **ex-34 · take-home-scope-cut** — deliberately cut a nice-to-have to finish the core, documented —
    verify the core is complete and the cut is noted. (co-02, co-09, co-12)
18. **ex-35 · error-messages-for-humans** — improve a cryptic error into an actionable one — verify the
    message names the fix. (co-10, co-11)
19. **ex-36 · self-score-a-take-home** — grade a finished take-home against a rubric (scope, tests,
    docs, git, readability) — verify each axis is rated. (co-01–co-11)

### Advanced (ex 37–50)

1. **ex-37 · full-take-home-walkthrough** — a complete take-home from brief to submission: checklist →
   skeleton → README → tests → commits → review pass — verify every stage artifact exists. (co-01–co-22)
2. **ex-38 · take-home-with-persistence** — a small service backed by SQLite with a schema + migration
   note — verify data survives a restart and the test seeds it. (co-03, co-05, co-06)
3. **ex-39 · concurrency-in-a-take-home** — a bounded concurrent task done safely with a note on the
   approach — verify no race under the test. (co-09, co-10)
4. **ex-40 · defend-the-tradeoffs** — a follow-up interview transcript defending the take-home's
   decisions — verify each answer maps to a README decision. (co-09, co-13)
5. **ex-41 · live-system-under-observation** — a 45-minute live build with continuous narration + steer
   - green increments — verify the artifact runs and the transcript is unbroken. (co-13–co-20)
6. **ex-42 · live-recover-from-a-wrong-turn** — a transcript that goes down a wrong path and backs out
   cleanly — verify the code returns to green after the detour. (co-16, co-18)
7. **ex-43 · minimal-deps-audit** — run a dependency audit on the take-home and show it is CVE-clean —
   verify the audit is clean. (co-08)
8. **ex-44 · readme-quickstart-verified** — have a fresh reader follow only the README quickstart —
   verify they reach a running state with no outside help. (co-04, co-05)
9. **ex-45 · git-bisect-friendly-history** — a history where each commit builds + tests green (bisect-
   friendly) — verify a mid-history checkout still runs. (co-07)
10. **ex-46 · live-pairing-etiquette** — a transcript balancing narration with listening to the
    interviewer — verify both parties contribute. (co-13, co-14)
11. **ex-47 · scope-negotiation-live** — negotiate scope live when the task is larger than the time —
    verify an agreed reduced scope is stated. (co-02, co-19)
12. **ex-48 · take-home-observability-note** — add a logging/observability note appropriate to the
    deliverable's size — verify it is proportionate, not over-built. (co-02, co-10)
13. **ex-49 · full-mock-live-round** — a complete self-run live round with a rubric self-score — verify
    the artifact runs and each rubric axis is rated. (co-13–co-22)
14. **ex-50 · capstone-both-formats** — one take-home + one live round on the same domain, self-scored —
    verify both deliverables run and both score sheets are complete. (co-01–co-22)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: complete one full **take-home** (a small, scoped, tested, documented deliverable runnable
  from a clean checkout) and one self-run **live round** (a recorded incremental build with continuous
  narration and green checkpoints), each self-scored against its rubric.
- **Concepts exercised**: [ ] brief → checklist + scope discipline (co-01, co-02) [ ] structure +
  README + clean-checkout run (co-03–co-05) [ ] judgment-bearing tests + validation (co-06, co-10)
  [ ] git hygiene + documented trade-offs (co-07, co-09) [ ] live pairing: think-aloud + steer + keep-
  it-running (co-13–co-16) [ ] submission/self-review pass (co-22).
- **Ordered steps**:
  1. `take-home-and-live-coding/learning/capstone/take-home/` — the deliverable + README + tests +
     commit history. Verify a clean-checkout `setup` runs it and all tests pass.
  2. `take-home-and-live-coding/learning/capstone/live/transcript.md` + `code/` — a recorded live build
     with green checkpoints. Verify the code runs and the transcript narrates each increment.
  3. `take-home-and-live-coding/learning/capstone/scoresheet.md` — self-score both against their rubrics.
     Verify every axis is rated with justification.
- **Acceptance criteria**: the take-home runs from a clean checkout with green tests and a complete
  README; the live artifact runs with an unbroken narrated transcript; both score sheets are complete.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

- **The Pragmatic Programmer** — Andrew Hunt & David Thomas (20th Anniversary ed.). On the craft
  habits a take-home is graded against: scope, clarity, and honest trade-offs.
- **A Philosophy of Software Design** — John Ousterhout. On readability and minimizing complexity — the
  axes a small reviewable deliverable is judged on.

## In which paths

- `job-seeking-software-engineer` — Phase 1 · Interview Preparation (through senior).
- `software-engineer` — Optional tail · Ready to job-hunt? (bridge into the interview courses, RESOLVED
  OQ-3).

---

← Back to [README.md — course library catalog](./README.md)
