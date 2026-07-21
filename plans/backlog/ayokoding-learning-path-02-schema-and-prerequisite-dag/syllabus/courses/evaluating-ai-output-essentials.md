# Evaluating AI Output — Essentials (Annotated-concept, Python)

**Course ID**: `evaluating-ai-output-essentials` · **Format**: Annotated-concept · **Language**: Python.
**NEW** — the **light eval gate**: the first quality checkpoint after a learner's first working LLM
call, placed deliberately before RAG and before agents.

**Scope note**: answering one question and one question only — **"how will you know this works?"** A
learner who has just made an LLM return something plausible has no way to tell a good change from a bad
one. This course installs the smallest honest feedback loop: write down what "good" means, collect a
handful of real cases, score them the same way twice, and put a number on a change before shipping it.
It is **deliberately small in scope** — twelve concepts, not twenty-four. Error analysis, LLM-as-judge
with measured human agreement, judge reliability, and CI gating are **out of scope here** and are owned
by [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md), which runs after agents.
Builds on [`creating-ai-powered-apps`](./creating-ai-powered-apps.md) (the first working model call) and
[`software-testing`](./software-testing.md) (the assertion mindset).

> **Scope guard — light gate vs deep evals.** This course teaches you to _notice_ that output quality
> changed. The deep course teaches you to _explain why_ and to _defend the measurement_. If a technique
> requires computing an agreement statistic, deriving criteria from observed failure modes, or defending
> a judge's scope, it belongs in the deep course, not here. If a technique is "write the expectation
> down, run it twice, compare," it belongs here.

## Why this exists · the big idea

- **The problem before the solution**: the first LLM feature always looks like it works, because the
  first thing anyone tries is the thing they had in mind. Without a fixed set of cases and a fixed way
  of scoring them, every subsequent prompt tweak is a vibe check — the engineer cannot distinguish an
  improvement from a regression, and neither can anyone reviewing the change.
- **Keep-this-if-you-forget-everything**: before you tune anything, write down ten cases and how you
  will score them — an eval you can run twice beats an opinion you can argue about forever.
- **Big ideas touched**: `determinism-vs-emergence` (a stochastic component still needs a pass/fail
  contract), `correctness-vs-pragmatism` (you are establishing "good enough", measurably, not proving
  correctness).

## Prerequisites

- **Prior topics**: [`creating-ai-powered-apps`](./creating-ai-powered-apps.md) (a working model call,
  structured output), [`software-testing`](./software-testing.md) (assertions, fixtures, test doubles),
  [`just-enough-python`](./just-enough-python.md).
- **Tools & environment**: a macOS/Linux terminal; Python 3.x under `uv`; a local or mockable model so
  the examples run without a paid key; `pytest`; a plain JSONL file as the dataset store (no eval
  framework required — deliberately); Neovim/VSCode.
- **Assumed knowledge**: calling a model and parsing its output; writing a `pytest` assertion; reading
  and writing JSON/JSONL from Python.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-20 — **durable spine**: the discipline of fixing a dataset, fixing a scoring rule, and
  comparing two runs predates LLMs entirely and is independent of any model, vendor, or framework.
  Nothing in this course's spine names a product.
- 2026-07-20 — verified in the sibling course: Anthropic's published eval principles are "Be
  task-specific … Automate when possible … Prioritize volume over quality"; the "prioritize volume"
  guidance is the one that most surprises engineers coming from hand-written unit tests. Source:
  [Anthropic develop tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
  (re-verify the wording at authoring).
- 2026-07-20 — `[Needs Verification]` **volatile, accuracy-note only**: eval-framework names, hosted
  eval products, and their schemas change fast. This course deliberately uses a plain JSONL file and
  `pytest` so nothing in the spine depends on a framework. Name a framework at authoring only as an
  aside, never as structure.
- 2026-07-20 — `[Needs Verification]` **volatile**: model IDs, pricing, and per-token costs cited in any
  cost-per-eval-run example are snapshots — read them from config, never hard-code.

## Concepts

<!-- co-NN · concept enumeration: deliberately capped at 12. Floor ≥ 10 (Annotated-concept, code-bearing). Anything requiring an agreement statistic or a derived criterion belongs to evaluating-ai-systems-in-depth. -->

1. **co-01 · why-a-vibe-check-fails** — trying the feature by hand tests the case you already imagined,
   so it cannot detect a regression on the cases you did not.
2. **co-02 · what-good-means-written-down** — a criterion you can hand to another person and get the
   same verdict from is the minimum unit of an eval.
3. **co-03 · the-ten-case-dataset** — a small fixed set of real inputs, versioned in the repo, is the
   whole gate; the fixed-ness matters more than the size.
4. **co-04 · golden-outputs** — for cases with one right answer, storing the expected output turns the
   eval into an ordinary test.
5. **co-05 · deterministic-scorers** — exact match, schema validation, substring/regex, and numeric
   tolerance are scorers that cost nothing and never drift.
6. **co-06 · schema-validation-as-an-eval** — for structured output, "does it parse against the schema"
   is the cheapest and highest-value eval there is.
7. **co-07 · pass-rate-as-the-headline-number** — the fraction of cases passing is the single number
   you compare across runs; one number beats a wall of output.
8. **co-08 · run-it-twice** — a stochastic system gives different answers to the same input, so a single
   run's pass rate is not yet evidence; re-running is the cheapest reliability check available.
9. **co-09 · before-and-after-comparison** — the eval's job is comparing a candidate change against the
   current baseline, not certifying absolute quality.
10. **co-10 · regression-cases-from-real-bugs** — every failure a human reports becomes a permanent case
    in the set; this is how the dataset earns its coverage.
11. **co-11 · cost-and-latency-in-the-same-run** — record tokens, cost, and latency alongside the score,
    because a quality win paid for with a 4× cost is a decision, not a free lunch.
12. **co-12 · knowing-this-gate-is-not-enough** — a pass rate on ten cases cannot tell you _why_ the
    failures happen or whether a subjective scorer is trustworthy; recognising that boundary is what
    sends you to the deep course.

## Tensions & trade-offs — when NOT to reach for this

- **Ten cases vs a real dataset**: ten cases catch gross regressions and nothing subtler. That is the
  intended trade — a gate you actually run beats a rigorous eval suite you postpone until "after the
  prototype". But do not mistake a green ten-case run for evidence that the feature is good.
- **Deterministic scorers vs the things that matter**: exact match and schema validation are free and
  stable, but most of what users care about (is this summary faithful? is this tone right?) is not
  exact-matchable. This course deliberately stops at what deterministic scorers can reach rather than
  reaching for a judge it cannot yet validate.
- **When NOT to reach for this**: if the output is genuinely single-valued and deterministic downstream
  — a classifier over a fixed label set, an extraction with one correct answer — you do not need an
  "eval", you need an ordinary test suite. Reaching for eval machinery there adds ceremony without
  adding information.
- **When this gate is not enough**: the moment you are asked "why is it failing?" or you want to score
  something subjective, this course is out of road. Go to
  [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md).

## Lineage — why it beat the alternative

- The alternative that lost was tuning by inspection — change the prompt, eyeball a few outputs, ship.
  It failed for the same reason manual QA failed before automated tests: it does not scale past the
  cases the engineer happens to remember, and it produces no artefact anyone else can re-run. The
  discipline that won is the oldest one in software testing, transplanted: fix the inputs, fix the
  scoring, compare runs. What is genuinely new for LLMs is only that the system under test is
  stochastic, which forces two adjustments — re-run to see variance (co-08), and accept a pass _rate_
  rather than a pass/fail (co-07). Everything else is testing. This course sits deliberately early,
  before [`creating-ai-powered-apps`](./creating-ai-powered-apps.md)'s RAG material and well before
  [`agentic-ai`](./agentic-ai.md), because a learner who adds retrieval and agency without a gate has
  no way to tell which of the two made things worse. The rigor — error analysis, judges, CI —
  is deferred to [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md), which needs
  agent trajectories to be worth teaching against.

## Worked examples

No fixed Beginner/Intermediate/Advanced bands (Annotated-concept); grouped by theme. Code where it
clarifies (scorers, runners, comparison reports), prose + WCAG-accessible Mermaid diagrams where the
loop's shape is the point. Colocated under `evaluating-ai-output-essentials/learning/code/` (runnable)
and `.../artifacts/` (diagrams). Contiguous `ex-01..ex-46`. Every example cites the `co-NN` it exercises.
All examples run against a local/mockable model so no paid key is required.

### Theme A · Why you cannot eyeball it (ex 01–10)

1. **ex-01 · the-vibe-check-fails** — tune a prompt by hand against one case, then show a second case it
   silently broke — verify the regression was invisible. (co-01)
2. **ex-02 · same-input-two-answers** — call the model twice on one input — verify the outputs differ.
   (co-08)
3. **ex-03 · write-down-what-good-means** — turn a vague "make it better" into a written criterion two
   people would score identically — verify both verdicts match. (co-02)
4. **ex-04 · criterion-that-fails-the-two-person-test** — an ambiguous criterion scored differently by
   two readers, then a rewrite that fixes it — verify the disagreement disappears. (co-02)
5. **ex-05 · collect-ten-real-inputs** — assemble ten real inputs into a versioned JSONL file — verify
   the file is committed and loadable. (co-03)
6. **ex-06 · fixed-dataset-diagram** — a Mermaid diagram of the loop (dataset → run → score → compare) —
   verify every stage appears. (co-03, co-09)
7. **ex-07 · why-fixed-beats-fresh** — re-run against fresh random inputs vs the fixed set — verify only
   the fixed set supports comparison. (co-03, co-09)
8. **ex-08 · dataset-in-version-control** — evolve the dataset across two commits — verify the diff shows
   exactly which cases changed. (co-03, co-10)
9. **ex-09 · ten-cases-is-not-coverage** — annotate what a ten-case set provably does and does not tell
   you — verify the honest limits. (co-03, co-12)
10. **ex-10 · dataset-schema** — a minimal case schema (`id`, `input`, `expected`, `criterion`) — verify
    every case validates. (co-03, co-04)

### Theme B · Scorers that cost nothing (ex 11–22)

1. **ex-11 · exact-match-scorer** — score a single-answer case by exact match — verify pass and fail.
   (co-05, co-04)
2. **ex-12 · normalized-match** — strip whitespace/case before matching — verify a cosmetic diff no
   longer fails. (co-05)
3. **ex-13 · substring-scorer** — assert a required fact appears in the answer — verify a missing fact
   fails. (co-05)
4. **ex-14 · regex-scorer** — assert a format (a date, an ID) with a regex — verify a malformed output
   fails. (co-05)
5. **ex-15 · numeric-tolerance-scorer** — score a number within a tolerance — verify the boundary cases.
   (co-05)
6. **ex-16 · schema-validation-scorer** — validate structured output against its JSON schema — verify a
   missing required field fails. (co-06)
7. **ex-17 · schema-eval-catches-the-most** — annotate why schema validation catches the highest share of
   real breakage per line of eval code — verify the claim against the run. (co-06)
8. **ex-18 · scorer-returns-a-reason** — every scorer returns pass/fail plus a human-readable reason —
   verify the reason explains the failure. (co-05)
9. **ex-19 · scorer-registry** — map each case to its scorer by name — verify the right scorer runs per
   case. (co-05, co-03)
10. **ex-20 · a-scorer-that-lies** — a substring scorer that passes a wrong answer, then a tightened
    version — verify the false pass and the fix. (co-05, co-02)
11. **ex-21 · never-score-with-the-generating-model** — annotate why a subjective scorer is deferred to
    the deep course rather than improvised here — verify the scope boundary. (co-12)
12. **ex-22 · scorer-comparison-diagram** — a Mermaid diagram placing scorers on a cost-vs-reach axis —
    verify deterministic scorers sit cheap-and-narrow. (co-05, co-06, co-12)

### Theme C · The runner and the number (ex 23–34)

1. **ex-23 · minimal-eval-runner** — load the dataset, call the model per case, apply the scorer, print
   results — verify it runs end to end. (co-03, co-05, co-07)
2. **ex-24 · pass-rate** — reduce per-case results to a single pass rate — verify the arithmetic. (co-07)
3. **ex-25 · per-case-report** — print a table of case, verdict, and reason — verify each failure is
   traceable. (co-07, co-05)
4. **ex-26 · run-it-twice** — run the same eval twice and diff the pass rates — verify the run-to-run
   variance is visible. (co-08)
5. **ex-27 · flaky-case-detection** — flag cases whose verdict flips across runs — verify the flaky set
   is identified. (co-08)
6. **ex-28 · n-of-k-pass-criterion** — pass a case only if it passes k of n runs — verify a flaky case is
   correctly failed. (co-08, co-07)
7. **ex-29 · seed-and-temperature-note** — annotate that lowering temperature reduces but does not remove
   variance — verify the caveat holds in the run. (co-08)
8. **ex-30 · record-tokens-and-cost** — capture tokens and estimated cost per case — verify the totals.
   (co-11)
9. **ex-31 · record-latency** — capture per-case latency and the run's p95 — verify the figures. (co-11)
10. **ex-32 · quality-cost-tradeoff-report** — a report showing pass rate alongside cost and latency —
    verify a quality win with a cost regression is visible. (co-11, co-07)
11. **ex-33 · results-as-a-committed-artefact** — write results to a file another engineer can read —
    verify the artefact is reproducible. (co-07, co-09)
12. **ex-34 · runner-as-a-pytest-suite** — express the eval as ordinary `pytest` cases — verify it runs
    under the existing test command. (co-05, co-07)

### Theme D · Using the gate on a real change (ex 35–46)

1. **ex-35 · baseline-run** — record a baseline pass rate before any change — verify it is stored.
   (co-09)
2. **ex-36 · candidate-run** — run a prompt change against the same dataset — verify a comparable number.
   (co-09)
3. **ex-37 · compare-baseline-vs-candidate** — a diff report of per-case verdict changes — verify wins
   and regressions are separated. (co-09, co-07)
4. **ex-38 · a-change-that-helps-and-hurts** — a prompt edit that fixes three cases and breaks two —
   verify the net number hides the trade and the per-case diff reveals it. (co-09, co-07)
5. **ex-39 · regression-case-from-a-bug-report** — turn a reported bad output into a permanent case —
   verify it fails before the fix and passes after. (co-10)
6. **ex-40 · the-dataset-grows-by-failure** — annotate the discipline of only ever adding cases that
   something actually got wrong — verify the growth pattern. (co-10, co-03)
7. **ex-41 · model-swap-under-the-same-eval** — swap the mockable model's behavior and re-run — verify
   the eval detects the change without edits. (co-09, co-03)
8. **ex-42 · eval-before-adding-retrieval** — run the gate, then add a retrieval step, then re-run —
   verify you can attribute the delta to the retrieval change. (co-09)
9. **ex-43 · eval-gate-in-the-loop-diagram** — a Mermaid diagram of where the gate sits relative to
   prompt changes, retrieval, and agents — verify the placement is before both. (co-09, co-12)
10. **ex-44 · what-this-gate-cannot-tell-you** — annotate three questions this gate provably cannot
    answer, each mapped to the deep course's owning concept — verify the hand-off. (co-12)
11. **ex-45 · handoff-to-deep-evals** — annotate the exact trigger conditions for graduating to
    [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md) — verify each trigger is
    concrete. (co-12)
12. **ex-46 · capstone-first-eval-gate** — the complete gate: a versioned dataset, a scorer registry, a
    twice-run runner reporting pass rate with cost and latency, and a baseline-vs-candidate diff applied
    to a real prompt change — verify it detects both an improvement and a regression. (co-01–co-12)

## Capstone spec — intra-topic (concept → full runnable)

- **Goal**: build the smallest honest eval gate for a feature the learner already has working from
  [`creating-ai-powered-apps`](./creating-ai-powered-apps.md) — a versioned ten-to-twenty-case dataset,
  a registry of deterministic scorers, a runner that executes each case twice and reports a pass rate
  alongside tokens, cost, and latency, and a comparison report that diffs a candidate run against a
  stored baseline — then use it to accept one real prompt change and reject another.
- **Concepts exercised**: [ ] a written, two-person-stable criterion (co-02) [ ] a fixed versioned
  dataset (co-03, co-04) [ ] deterministic + schema scorers (co-05, co-06) [ ] pass rate as the headline
  (co-07) [ ] repeat runs and flake handling (co-08) [ ] baseline-vs-candidate comparison (co-09)
  [ ] a regression case sourced from a real failure (co-10) [ ] cost and latency recorded in the same run
  (co-11).
- **Ordered steps**:
  1. `evaluating-ai-output-essentials/learning/capstone/code/dataset.jsonl` — collect and commit real
     cases with written criteria. Verify every case validates against the case schema and two readers
     score three sample outputs identically.
  2. `scorers.py` — implement exact-match, normalized-match, regex, numeric-tolerance, and schema
     scorers, each returning a verdict plus a reason. Verify each scorer's pass and fail path, including
     one deliberately over-permissive scorer and its tightened replacement.
  3. `runner.py` — execute every case twice against the mockable model, apply the mapped scorer, and
     emit pass rate, flaky-case list, tokens, cost, and p95 latency to a committed results file. Verify
     the run is reproducible and the flaky-case detection fires on a known-unstable case.
  4. `compare.py` — diff a candidate results file against the baseline, separating wins from
     regressions. Verify it accepts a genuinely better prompt and rejects a prompt that raises the pass
     rate while breaking a previously passing case.
- **Acceptance criteria**: the dataset is versioned and schema-valid; every scorer is deterministic and
  explains its verdict; the runner reports a pass rate with cost and latency and identifies flaky cases
  across repeat runs; the comparison report distinguishes wins from regressions on a real change; the
  suite runs offline against a mockable model with no API key committed; and the learner can state, in
  writing, three questions this gate cannot answer.
- **Done bar**: runnable end-to-end (offline, mockable model) + web-verified.

## Read more

- **Designing Machine Learning Systems** — Chip Huyen (2022). Practitioner-oriented treatment of
  evaluation as a production concern rather than a research one.
- **Anthropic — Create strong empirical evaluations** — the "be task-specific, automate when possible,
  prioritize volume over quality" principles this course's dataset discipline follows.
  <https://platform.claude.com/docs/en/test-and-evaluate/develop-tests>
- **OpenAI — Evals** — the golden-JSONL + testing-criteria shape, useful as a second reference point for
  the plain-file dataset pattern taught here.
  <https://developers.openai.com/api/docs/guides/evals>

## In which paths

- `immediately-effective/ai-engineer` — **owning path**: the light eval gate,
  placed immediately after the first working LLM call and before retrieval and agents (D5).
- `interview-ready/software-engineer` — candidate placement in the AI & harness engineering deepening
  tail — pending manifest re-verification (D8 four-path rule).
- `immediately-effective/software-engineer` — candidate placement in the deepening band — pending
  manifest re-verification (D8 four-path rule).
- `fundamentally-strong/software-engineer` — candidate placement in Stage 12 · AI & harness engineering
  — pending manifest re-verification (D8 four-path rule).

---

← Back to [README.md — course library catalog](./README.md)
