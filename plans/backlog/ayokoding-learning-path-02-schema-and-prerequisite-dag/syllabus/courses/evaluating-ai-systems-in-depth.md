# Evaluating AI Systems In Depth (By Example, Python)

**Course ID**: `evaluating-ai-systems-in-depth` · **Format**: By Example · **Language**: Python.
**NEW** — the library's **single owner** of evaluation depth; placed after agents, because agent
trajectories are what make the hard eval problems concrete.

**Scope note**: the discipline of measuring a system whose output has no single right answer —
**error analysis first** (read failures before inventing metrics), **task-specific criteria derived from
observed failure modes** rather than borrowed from a leaderboard, **LLM-as-judge with measured human
agreement** (a judge you have not agreed-with is a random number generator with a confident tone),
**judge-scope reliability** (which questions a judge can be trusted on and which it cannot),
**trajectory and multi-step evaluation** for agents, and **CI gating** so a regression blocks a merge.
Absorbs the evaluation material previously scattered across
[`creating-ai-powered-apps`](./creating-ai-powered-apps.md) co-19,
[`agentic-ai`](./agentic-ai.md) co-25/co-26, and
[`agent-orchestration-subagents-and-observability`](./agent-orchestration-subagents-and-observability.md)
Theme D — see [surgery.md](./surgery.md) for the extraction and its four-path blast radius. Depends on
the statistical machinery taught in [`statistics-for-evaluation`](./statistics-for-evaluation.md).

> **Scope guard — deep evals vs the light gate.**
> [`evaluating-ai-output-essentials`](./evaluating-ai-output-essentials.md) owns "notice that quality
> changed": fixed dataset, deterministic scorers, pass rate, before/after comparison. This course owns
> everything that requires **explaining why** or **defending the measurement itself**: failure
> taxonomies, derived criteria, judges validated against humans, agreement statistics, judge scope
> limits, trajectory scoring, and merge-blocking gates. If a technique needs an agreement number, it is
> here. If it needs only an assertion, it is there.

## Why this exists · the big idea

- **The problem before the solution**: teams reach for a metric before they have read their failures, so
  they measure something that is easy to compute instead of something that predicts user harm — and then
  they adopt an LLM judge whose agreement with a human they never measured, which converts an unknown
  quality problem into a confidently-scored unknown quality problem. Both moves feel like rigor and
  supply none.
- **Keep-this-if-you-forget-everything**: read a hundred failures before you write a metric, and never
  trust a judge you have not measured against a human on the exact question you are asking it.
- **Big ideas touched**: `determinism-vs-emergence` (measurement is how you govern a stochastic system),
  `correctness-vs-pragmatism` (the goal is a defensible decision procedure, not proof),
  `abstraction-and-its-cost` (every score is a lossy projection of what you actually care about).

## Prerequisites

- **Prior topics**: [`evaluating-ai-output-essentials`](./evaluating-ai-output-essentials.md) (the light
  gate — dataset, scorers, pass rate), [`statistics-for-evaluation`](./statistics-for-evaluation.md)
  (agreement, sampling, significance — a hard prerequisite, not a nice-to-have),
  [`agentic-ai`](./agentic-ai.md) and
  [`agent-orchestration-subagents-and-observability`](./agent-orchestration-subagents-and-observability.md)
  (agent trajectories and traces are the objects under evaluation),
  [`cicd-and-release-engineering`](./cicd-and-release-engineering.md) (the pipeline the gate runs in),
  [`software-testing`](./software-testing.md).
- **Tools & environment**: a macOS/Linux terminal; Python 3.x under `uv`; a local or mockable model plus
  a second, different mockable model to act as judge (so judge-model separation is demonstrable
  offline); a spreadsheet or notebook for the manual error-analysis pass; `pytest`; a CI runner;
  Neovim/VSCode. All model SDKs pinned CVE-clean at authoring.
- **Assumed knowledge**: the light gate's dataset/scorer/pass-rate loop; agreement statistics and
  confidence intervals at the level taught in `statistics-for-evaluation`; reading an agent trace; how a
  CI job blocks a merge.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-20 — **durable spine**: error-analysis-before-metrics, deriving criteria from observed failure
  modes, validating a judge against human labels, reporting agreement rather than asserting it, and
  gating merges on a measured regression bar are methodology. None of them depend on a model, vendor, or
  framework, and none has changed as models improved.
- 2026-07-20 — verified in the sibling course: Anthropic's stated best practice is "to use a different
  model to evaluate than the model used to generate", and its eval principles are "Be task-specific …
  Automate when possible … Prioritize volume over quality". Sources:
  [Anthropic develop tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
  (re-verify wording at authoring).
- 2026-07-20 — verified in the sibling course: LangSmith trajectory evaluation examines "the exact
  sequence of tool calls", scored either by a trajectory-match evaluator or an LLM judge. Treat the
  **trajectory-vs-outcome distinction as durable spine** and the **named product as volatile**. Source:
  [LangSmith trajectory evals](https://docs.langchain.com/langsmith/trajectory-evals) (re-verify at
  authoring).
- 2026-07-20 — `[Needs Verification]` **volatile, accuracy-note only**: eval framework and hosted
  eval-product names, their schemas, and their default metrics. Teach the method against plain files and
  `pytest`; name a product only as an illustration.
- 2026-07-20 — `[Needs Verification]` **volatile, accuracy-note only**: OpenTelemetry GenAI semantic
  conventions are explicitly pre-stable — any span/attribute name used when wiring traces into evals is
  a moving target and must carry the "may change" caveat.
- 2026-07-20 — `[Needs Verification]` **volatile**: model IDs, judge-model pricing, and any published
  benchmark leaderboard position are snapshots with a short half-life. Never place a leaderboard number
  in the spine.
- 2026-07-20 — **contested, teach as contested**: there is no settled industry threshold for "good
  enough" judge-human agreement. Teach the learner to report the agreement statistic and its confidence
  interval and to justify their own threshold against their decision's stakes, rather than citing a
  magic number.

## Concepts

<!-- co-NN · concept enumeration. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · error-analysis-first** — before choosing any metric, read a large sample of real failures;
  the metric is an output of that reading, not an input to it.
- **co-02 · open-coding-failures** — label failures with descriptive tags invented while reading, not
  with a pre-existing taxonomy.
- **co-03 · failure-taxonomy** — cluster the open codes into a small set of named, mutually intelligible
  failure modes with observed frequencies.
- **co-04 · frequency-weighted-prioritization** — fix and measure the failure modes that are common and
  costly, not the ones that are interesting.
- **co-05 · derived-task-specific-criteria** — each criterion traces to a failure mode you actually
  observed; a criterion with no failure behind it is speculation.
- **co-06 · criterion-operationalization** — turning a named criterion into an instruction precise enough
  that two independent human labelers agree.
- **co-07 · human-labeling-protocol** — a written labeling guide, independent labelers, and a
  disagreement-resolution rule are what make human labels a usable ground truth.
- **co-08 · ground-truth-set** — a human-labeled subset is the reference every automated scorer is
  validated against; without it nothing downstream is checkable.
- **co-09 · llm-as-judge** — a model prompted to score another model's output against an operationalized
  criterion.
- **co-10 · judge-human-agreement-is-mandatory** — a judge's value is exactly its measured agreement with
  human labels on the same items; unmeasured, it is decoration.
- **co-11 · judge-scope-reliability** — agreement is per-question, not global: a judge trustworthy on
  "is this grounded in the source" may be worthless on "is this tone appropriate".
- **co-12 · judge-model-separation** — the judge should not be the model that generated the output, and
  the reason is correlated blind spots, not fairness.
- **co-13 · judge-bias-modes** — position bias, verbosity bias, self-preference, and score compression
  are systematic and must be tested for, not assumed absent.
- **co-14 · pairwise-vs-pointwise-judging** — asking "which is better" is usually more reliable than
  asking "score this 1-5"; the trade is that pairwise needs a baseline.
- **co-15 · rubric-design-for-judges** — short, binary, single-question rubrics agree with humans far
  better than long multi-dimensional scoring sheets.
- **co-16 · judge-recalibration** — agreement decays when the model, prompt, or data distribution
  changes, so it is re-measured on a schedule, not once.
- **co-17 · reference-free-vs-reference-based** — scoring against a gold answer versus scoring the output
  on its own terms; each fails differently.
- **co-18 · trajectory-evaluation** — for agents, the sequence of tool calls is an object of evaluation
  distinct from the final answer.
- **co-19 · outcome-vs-process-scoring** — a right answer reached by a wrong path is a latent failure;
  scoring both catches what either alone misses.
- **co-20 · multi-step-failure-attribution** — locating which step in a trajectory caused the failure is
  what makes an agent eval actionable.
- **co-21 · eval-dataset-construction** — sourcing cases from production traffic, red-team probes, and
  regression reports, with deliberate coverage of the failure taxonomy.
- **co-22 · dataset-contamination-and-leakage** — cases that leaked into a prompt, a cache, or a
  fine-tune produce scores that do not transfer.
- **co-23 · eval-in-ci** — the eval suite runs in the pipeline and its result is a merge decision, not a
  report.
- **co-24 · regression-bar-and-noise-floor** — the merge-blocking threshold must sit above the suite's
  own run-to-run noise, or the gate blocks at random.
- **co-25 · cost-of-evaluation** — judge calls and repeat runs cost real money and wall time; the suite
  is budgeted and tiered like any other test suite.
- **co-26 · tiered-eval-suites** — a fast deterministic tier on every commit, a full judged tier on merge
  or nightly, mirroring the unit/integration/e2e split.
- **co-27 · evals-drive-improvement** — the loop closes only when failing cases route back into error
  analysis and produce the next change.
- **co-28 · what-evals-cannot-catch** — novel harms, distribution shift, and anything absent from the
  dataset remain invisible; an eval suite bounds risk, it does not eliminate it.

## Tensions & trade-offs — when NOT to reach for this

- **Rigor vs shipping speed**: a validated judge with measured agreement, a human-labeled ground-truth
  set, and a tiered CI suite is weeks of work. For a prototype nobody depends on, the light gate is the
  correct stopping point and this course is over-engineering. Reach for this when a regression would
  reach users, cost money, or be hard to detect by hand.
- **Judge cost vs judge value**: judged evals multiply the cost of every CI run and add their own noise.
  A cheap deterministic scorer that agrees with humans 90% of the time beats an expensive judge that
  agrees 92% — measure both before assuming the judge wins.
- **More criteria vs usable signal**: every criterion added dilutes attention and adds noise. A suite
  with twenty criteria nobody reads is worse than three criteria that map to the three most frequent
  observed failure modes.
- **When NOT to use LLM-as-judge at all**: if a deterministic scorer can answer the question (schema
  validity, exact match, presence of a required citation), a judge adds cost, variance, and a new thing
  to validate for no gain. Judges are for questions deterministic scorers genuinely cannot reach.
- **When NOT to gate CI on evals**: gating on a suite whose noise floor exceeds the regression bar
  produces random build failures, which teaches the team to ignore the gate — strictly worse than no
  gate. Measure the noise floor first (co-24).

## Lineage — why it beat the alternative

- The first wave of LLM evaluation borrowed academic benchmarks wholesale — leaderboard tasks and
  reference-overlap metrics designed to compare research systems, not to catch product regressions. They
  lost because they measured a distribution nobody's users were drawn from, and because a benchmark's
  score cannot tell a team which of their failures to fix. The second wave swung to LLM-as-judge and
  mostly repeated the error in a new form: adopting a judge without ever measuring it against a human on
  the specific question being asked, which produces scores that are precise, cheap, reproducible, and
  unvalidated. What won is the practice this course teaches — the same order of operations qualitative
  research settled on decades ago: look at the data first, code the failures openly, cluster them into a
  taxonomy, derive criteria from what you actually saw, then and only then automate, validating every
  automated scorer against human labels and reporting the agreement rather than asserting it. The
  agent-era addition is genuinely new: once a system takes many steps, the trajectory becomes an object
  of evaluation in its own right, because a right answer via a wrong path is a failure waiting for a
  different input. This course is the library's single owner of that material — it absorbs the
  treatments previously duplicated in [`creating-ai-powered-apps`](./creating-ai-powered-apps.md),
  [`agentic-ai`](./agentic-ai.md), and
  [`agent-orchestration-subagents-and-observability`](./agent-orchestration-subagents-and-observability.md),
  each of which now forward-links here rather than teaching a fourth parallel version.

## Worked examples

Colocated under `evaluating-ai-systems-in-depth/learning/code/`; each is typed, `pyright`-clean Python
runnable against a local/mockable generator model and a second, different mockable judge model, so
judge-model separation and agreement measurement are demonstrable with no paid key. Contiguous
`ex-01..ex-50`. Every example cites the `co-NN` it exercises. Concepts come before examples.

> **Volume-target floor**: this syllabus lists **50** of the required **≥75** (the 75–85 By-Example/
> Primer band, floor not cap — see
> [prd.md §Volume-target bands](../../prd.md#new-course--capstone-specifications)).
> The maker adds **≥25** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its by-example quality gate.

### Beginner (ex 01–16)

- **ex-01 · metric-before-analysis-fails** — pick a plausible metric without reading failures, then show
  it misses the dominant failure mode — verify the miss. (co-01)
- **ex-02 · read-a-hundred-failures** — sample and read failing outputs into a review sheet — verify
  every sampled case has a written observation. (co-01)
- **ex-03 · open-code-a-failure-sample** — invent descriptive tags while reading, without a prior
  taxonomy — verify tags are grounded in quoted output. (co-02)
- **ex-04 · premature-taxonomy-contrast** — apply a borrowed taxonomy to the same sample — verify cases
  that do not fit any bucket. (co-02, co-03)
- **ex-05 · cluster-codes-into-modes** — merge open codes into a small named failure taxonomy — verify
  each mode has example cases. (co-03)
- **ex-06 · failure-frequency-table** — count each mode's frequency in the sample — verify the counts sum
  to the sample. (co-03, co-04)
- **ex-07 · frequency-times-cost-ranking** — rank modes by frequency × user cost — verify the top mode is
  not the most interesting one. (co-04)
- **ex-08 · derive-a-criterion-from-a-mode** — write a criterion that exists because of an observed mode
  — verify the traceability link. (co-05)
- **ex-09 · criterion-with-no-failure-behind-it** — annotate a speculative criterion and delete it —
  verify the deletion rationale. (co-05)
- **ex-10 · operationalize-a-criterion** — rewrite a vague criterion until two labelers agree — verify
  the agreement improves. (co-06)
- **ex-11 · labeling-guide** — write the labeling protocol (definition, edge cases, tie-breaks) — verify
  a new labeler can apply it unaided. (co-07)
- **ex-12 · two-independent-labelers** — label the same items independently — verify labels are collected
  without cross-contamination. (co-07)
- **ex-13 · disagreement-resolution** — adjudicate disagreements by the written rule — verify every
  disagreement resolves to a recorded decision. (co-07)
- **ex-14 · build-the-ground-truth-set** — assemble the adjudicated labels into a reference set — verify
  it is versioned and schema-valid. (co-08)
- **ex-15 · ground-truth-coverage-check** — verify the reference set covers every failure mode in the
  taxonomy — verify no mode has zero cases. (co-08, co-03)
- **ex-16 · deterministic-scorer-vs-ground-truth** — measure a cheap deterministic scorer against the
  human labels — verify its agreement before reaching for a judge. (co-08, co-17)

### Intermediate (ex 17–34)

- **ex-17 · first-judge-prompt** — a judge scoring one operationalized criterion — verify it returns a
  parseable verdict. (co-09, co-15)
- **ex-18 · measure-judge-human-agreement** — compute agreement between judge and ground truth — verify
  the statistic and its interpretation. (co-10)
- **ex-19 · agreement-with-a-confidence-interval** — report agreement with an interval, not a point —
  verify the interval width reflects the sample size. (co-10)
- **ex-20 · an-unvalidated-judge-is-decoration** — annotate a judge deployed without agreement
  measurement and the decision it silently corrupted — verify the failure mode. (co-10)
- **ex-21 · judge-scope-per-question** — measure one judge's agreement on two different criteria — verify
  agreement differs sharply by question. (co-11)
- **ex-22 · retire-a-judge-out-of-scope** — drop a judge from a criterion where its agreement is too low
  — verify the criterion falls back to human review. (co-11)
- **ex-23 · self-preference-bias** — have a model judge its own output versus another's — verify the
  self-preference effect. (co-12, co-13)
- **ex-24 · judge-model-separation** — swap in a different judge model — verify the correlated blind spot
  disappears. (co-12)
- **ex-25 · position-bias-probe** — swap the order of two candidates in a pairwise prompt — verify the
  verdict flips more often than chance. (co-13, co-14)
- **ex-26 · verbosity-bias-probe** — pad a worse answer with length — verify the judge's score rises.
  (co-13)
- **ex-27 · score-compression** — annotate a 1-5 judge clustering on 3-4 — verify the lost resolution.
  (co-13, co-14)
- **ex-28 · pairwise-beats-pointwise** — compare pairwise and pointwise agreement on the same items —
  verify which tracks humans better. (co-14)
- **ex-29 · binary-rubric-beats-long-rubric** — contrast a single-question binary rubric with a
  multi-dimensional sheet — verify the agreement difference. (co-15)
- **ex-30 · rubric-iteration-loop** — iterate a rubric until agreement clears the stated threshold —
  verify each iteration's measured change. (co-15, co-06)
- **ex-31 · reference-based-scoring** — score against gold answers — verify where it breaks on valid
  alternative phrasings. (co-17)
- **ex-32 · reference-free-scoring** — score groundedness against the source rather than a gold answer —
  verify it accepts valid paraphrase. (co-17)
- **ex-33 · recalibrate-after-a-model-change** — re-measure agreement after swapping the generator —
  verify the drift is detected. (co-16)
- **ex-34 · recalibration-schedule** — annotate a recalibration cadence tied to model, prompt, and data
  changes — verify each trigger is concrete. (co-16)

### Advanced (ex 35–50)

- **ex-35 · trajectory-capture** — capture an agent run's tool-call sequence as an evaluable object —
  verify the trajectory is complete. (co-18)
- **ex-36 · trajectory-match-scoring** — score a trajectory against a reference sequence — verify an
  extra or missing tool call is caught. (co-18)
- **ex-37 · right-answer-wrong-path** — an agent reaching the correct output through an invalid path —
  verify outcome scoring passes while process scoring fails. (co-19)
- **ex-38 · process-scoring-catches-latent-failure** — show the same wrong path failing on a neighbouring
  input — verify the latent failure was real. (co-19)
- **ex-39 · attribute-failure-to-a-step** — locate the causing step in a failed trajectory — verify the
  attribution against the trace. (co-20)
- **ex-40 · subagent-failure-attribution** — attribute a failure to a subagent rather than the
  orchestrator — verify the boundary. (co-20, co-18)
- **ex-41 · dataset-from-production-traffic** — construct eval cases from real traffic with taxonomy
  coverage — verify each mode is represented. (co-21, co-03)
- **ex-42 · red-team-cases-in-the-suite** — fold adversarial probes into the eval set — verify they run
  as ordinary cases. (co-21)
- **ex-43 · detect-dataset-leakage** — detect a case that leaked into a prompt or cache — verify the
  inflated score and the fix. (co-22)
- **ex-44 · measure-the-noise-floor** — run the unchanged suite repeatedly to establish run-to-run
  variance — verify the measured floor. (co-24)
- **ex-45 · set-the-regression-bar-above-noise** — set the merge-blocking bar from the measured floor —
  verify a within-noise change does not block. (co-24, co-23)
- **ex-46 · eval-gate-blocks-a-merge** — wire the suite into CI so a real regression fails the build —
  verify the merge is blocked. (co-23)
- **ex-47 · tiered-suites** — a fast deterministic tier per commit and a judged tier on merge — verify
  each tier's runtime and cost. (co-26, co-25)
- **ex-48 · eval-cost-budget** — budget and report judge-call cost per CI run — verify a budget breach is
  flagged. (co-25)
- **ex-49 · failures-route-back-to-error-analysis** — feed CI failures into the next error-analysis pass
  — verify the taxonomy gains a mode. (co-27, co-01)
- **ex-50 · capstone-validated-eval-system** — the complete system: an error-analysis-derived taxonomy, a
  human-labeled ground-truth set, criteria traced to observed modes, a judge with measured and
  interval-reported agreement scoped per question, trajectory plus outcome scoring for the agent, and a
  tiered CI gate with a noise-floor-justified regression bar — verify it blocks a real regression, passes
  a within-noise change, and reports every judge's agreement. (co-01–co-28)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a defensible evaluation system for the agent the learner already built in the harness
  cluster — starting from a manual error-analysis pass over real failures, deriving criteria from the
  resulting taxonomy, standing up a human-labeled ground-truth set, validating an LLM judge against it
  with a reported agreement statistic and confidence interval scoped per question, adding trajectory and
  outcome scoring, and gating CI on a regression bar justified against the suite's measured noise floor.
- **Concepts exercised**: [ ] error analysis → open coding → taxonomy (co-01–co-03) [ ] criteria derived
  from observed modes and operationalized to labeler agreement (co-05, co-06) [ ] labeling protocol +
  ground-truth set (co-07, co-08) [ ] judge with measured agreement, separated model, scoped per question
  (co-09–co-12) [ ] bias probes + rubric design (co-13–co-15) [ ] trajectory + outcome scoring with step
  attribution (co-18–co-20) [ ] tiered CI gate above a measured noise floor (co-23, co-24, co-26)
  [ ] the loop back into error analysis (co-27) [ ] a written statement of what the suite cannot catch
  (co-28).
- **Ordered steps**:
  1. `evaluating-ai-systems-in-depth/learning/capstone/analysis/` — sample and read at least a hundred
     real failures from the agent, open-code them, and cluster into a frequency-ranked taxonomy. Verify
     every mode is defined, exemplified by quoted output, and counted.
  2. `criteria.md` + `labeling-guide.md` — derive criteria from the top modes and operationalize each
     until two independent labelers agree on a held-out sample. Verify the agreement statistic clears the
     threshold the learner justified in writing, and that every criterion traces to a mode.
  3. `ground_truth.jsonl` + `judge.py` — build the adjudicated human-labeled reference set, then
     implement a judge on a different model from the generator. Verify the judge's agreement is measured
     against the reference with a confidence interval, reported per criterion, and that position and
     verbosity bias probes are run and their results recorded.
  4. `trajectory.py` — score the agent's tool-call sequence alongside its final answer, with step-level
     failure attribution. Verify a right-answer-wrong-path case fails process scoring while passing
     outcome scoring.
  5. `ci/` — measure the suite's noise floor over repeated unchanged runs, set the regression bar above
     it, and wire a fast deterministic tier plus a judged merge tier into the pipeline with a cost
     budget. Verify a real regression blocks the merge, a within-noise change does not, and the judged
     tier's cost is reported and budgeted.
- **Acceptance criteria**: every criterion traces to a failure mode observed in the analysis pass; the
  ground-truth set is human-labeled under a written protocol with adjudicated disagreements; every
  automated scorer — deterministic or judge — reports measured agreement with the ground truth as a
  statistic with a confidence interval, scoped per question, and any judge below the learner's justified
  threshold is retired rather than shipped; the agent is scored on both trajectory and outcome with
  step-level attribution; the CI gate blocks a genuine regression, does not block a within-noise change,
  and reports its cost; the suite runs offline against mockable generator and judge models with no key
  committed; and the learner documents, in writing, what this suite provably cannot catch.
- **Done bar**: runnable end-to-end (offline, mockable models) + web-verified.

## Read more

- **Designing Machine Learning Systems** — Chip Huyen (2022). Evaluation as a production discipline,
  including the argument for measuring against your own distribution rather than a benchmark's.
- **Anthropic — Create strong empirical evaluations** — the task-specific / automate / volume principles
  and the different-model-as-judge guidance this course's judge chapter builds on.
  <https://platform.claude.com/docs/en/test-and-evaluate/develop-tests>
- **OpenAI — Evals** — the schema data-spec + testing-criteria + golden-JSONL shape as a second reference
  implementation. <https://developers.openai.com/api/docs/guides/evals>
- **LangSmith — Trajectory evals** — the trajectory-versus-outcome distinction applied to agents; cite
  the durable distinction, treat the product surface as volatile.
  <https://docs.langchain.com/langsmith/trajectory-evals>

## In which paths

- `immediately-effective/ai-engineer` — **owning path**: placed after the agent
  courses, because agent trajectories are what make derived criteria and process scoring concrete (D5).
- `interview-ready/software-engineer` — candidate placement in the AI & harness engineering deepening
  tail — pending manifest re-verification (D8 four-path rule).
- `immediately-effective/software-engineer` — candidate placement in the deepening band — pending
  manifest re-verification (D8 four-path rule).
- `fundamentally-strong/software-engineer` — candidate placement in Stage 12 · AI & harness engineering
  — pending manifest re-verification (D8 four-path rule).

---

← Back to [README.md — course library catalog](./README.md)
