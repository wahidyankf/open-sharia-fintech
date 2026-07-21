# Statistics for Evaluation (Annotated-concept, Python)

**Course ID**: `statistics-for-evaluation` · **Format**: Annotated-concept · **Language**: Python.
**NEW** — the library's only statistics course, and deliberately **not** a general one.

**Scope note**: exactly the statistics that evaluating a probabilistic system demands, and nothing else —
**inter-rater agreement** (why raw percent agreement overstates and what to use instead), **judge
concordance** (measuring an automated scorer against human labels), **sampling** (how many cases you
need before a pass rate means anything, and how to draw them without biasing the estimate),
**uncertainty** (confidence intervals on a rate, bootstrap resampling when the closed form does not
apply), and **significance** (whether a pass-rate difference between two runs is a real effect or noise,
including paired comparisons and the multiple-comparisons trap). Scoped by a single rule: a technique
earns a place here only if [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md)
cannot be taught honestly without it. Regression, causal inference, and experiment design for product
A/B testing are **out of scope** — those belong to
[`analytics-and-experimentation`](./analytics-and-experimentation.md), which is a sibling and a scope
mismatch for evals, not a substitute for this course.

> **Scope guard — why this is not a statistics course.** The research verdict this course answers is
> that "no ML background needed" is credible for training theory (backpropagation, architectures) and
> **oversold for statistics**: judge concordance and significance testing are irreducibly statistical,
> and an engineer who cannot compute an agreement coefficient or an interval on a pass rate cannot
> defend an eval result. Every concept below is present because an eval decision depends on it. If a
> statistical technique does not change an eval decision, it is out of scope by construction.

## Why this exists · the big idea

- **The problem before the solution**: eval results get reported as bare numbers — "the judge agrees 85%
  of the time", "the new prompt scores 3 points higher" — and both are frequently meaningless. Eighty-five
  percent agreement on a task where one label occurs 80% of the time is barely better than a coin
  weighted to the majority; a 3-point difference on forty cases is indistinguishable from noise. Without
  the statistics, an eval suite produces confident, precise, reproducible, and wrong decisions.
- **Keep-this-if-you-forget-everything**: a number without an interval is an opinion, and agreement that
  is not corrected for chance is not agreement.
- **Big ideas touched**: `correctness-vs-pragmatism` (quantified uncertainty is how you make a decision
  you can defend without proof), `abstraction-and-its-cost` (every summary statistic discards structure,
  and you must know which structure).

## Prerequisites

- **Prior topics**: [`evaluating-ai-output-essentials`](./evaluating-ai-output-essentials.md) (you must
  have a pass rate in hand before its uncertainty is a meaningful question),
  [`just-enough-python`](./just-enough-python.md),
  [`data-structures-and-algorithms-essentials`](./data-structures-and-algorithms-essentials.md) (loops,
  arrays, and the cost of a resampling procedure). No prior statistics course is assumed.
- **Tools & environment**: a macOS/Linux terminal; Python 3.x under `uv`; a numerical/statistical library
  pinned CVE-clean at authoring, used deliberately **after** each quantity has first been computed from
  its definition in plain Python; a plotting library for the interval and distribution figures;
  `pytest`; Neovim/VSCode.
- **Assumed knowledge**: arithmetic with proportions and percentages; reading a table of labeled cases;
  writing a loop in Python. Calculus is not required anywhere in this course.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-20 — **durable spine**: every technique in this course predates LLMs by decades. Chance-corrected
  agreement coefficients, binomial confidence intervals, the bootstrap, and paired significance tests are
  settled classical statistics. Nothing here has a vendor, a version, or a deprecation risk — which is
  precisely why this course is safe to place in a spine while framework material is not.
- 2026-07-20 — `[Needs Verification]` **at authoring**: the exact names, publication years, and canonical
  formulations of the named agreement coefficients (Cohen's kappa, Krippendorff's alpha, Scott's pi,
  Fleiss's kappa) and of the named significance tests (McNemar's test, the bootstrap percentile
  interval, Wilson and Clopper-Pearson intervals) — verify each against a primary statistical reference
  before authoring, and cite the reference read. This course must not ship a formula from memory.
- 2026-07-20 — `[Needs Verification]` **volatile, accuracy-note only**: the statistical library's API
  surface and default parameterizations (in particular which interval method a library's default returns
  — several default to the normal approximation, which is the one this course teaches learners to avoid
  at small n). Pin the version and re-verify the defaults at authoring.
- 2026-07-20 — **contested, teach as contested**: there is no consensus threshold for "acceptable" kappa,
  and the widely circulated verbal scales (poor/fair/moderate/substantial) are conventions from a single
  paper, not results. Teach the learner to report the coefficient with its interval and justify a
  threshold against the stakes of the decision, and explicitly teach that the verbal scales are
  conventions rather than findings.
- 2026-07-20 — no model IDs, prices, or benchmark numbers appear anywhere in this course's spine by
  design; there is nothing here to go stale.

## Concepts

<!-- co-NN · concept enumeration. Floor ≥ 10 (Annotated-concept, code-bearing). Every concept is here because an eval decision depends on it. -->

1. **co-01 · a-number-without-an-interval** — a point estimate reported alone invites a decision the data
   cannot support; the interval is the part that carries the information.
2. **co-02 · pass-rate-as-a-proportion** — an eval pass rate is a sample proportion estimating an unknown
   true rate, which is what makes all of the following apply.
3. **co-03 · sampling-error** — the same system re-measured on a different sample gives a different rate;
   that spread is quantifiable, not mysterious.
4. **co-04 · confidence-interval-on-a-rate** — an interval expresses the range of true rates consistent
   with what you observed.
5. **co-05 · small-n-interval-methods** — the normal approximation misbehaves at small n and near 0 or 1;
   Wilson and Clopper-Pearson style intervals are the corrective, and eval datasets are almost always
   small n.
6. **co-06 · how-many-cases-do-i-need** — required sample size follows from the effect you need to detect
   and the precision you need; this is a design question answered before collecting, not after.
7. **co-07 · sampling-strategy** — random, stratified, and convenience samples estimate different things;
   a convenience sample of the failures you happened to notice estimates nothing.
8. **co-08 · stratified-sampling-for-rare-modes** — rare failure modes need deliberate oversampling plus
   reweighting, or they are invisible at any feasible sample size.
9. **co-09 · raw-percent-agreement-overstates** — two raters agreeing 85% of the time on a task where one
   label appears 80% of the time have demonstrated almost nothing.
10. **co-10 · chance-corrected-agreement** — agreement coefficients subtract the agreement expected by
    chance, which is why they can be far lower than the raw percentage.
11. **co-11 · choosing-an-agreement-coefficient** — two raters and nominal labels, more than two raters,
    ordinal labels, and missing data each call for a different coefficient.
12. **co-12 · the-prevalence-problem** — chance-corrected coefficients themselves behave badly when one
    label dominates, so the coefficient is reported alongside the marginal distribution, never alone.
13. **co-13 · agreement-has-an-interval-too** — an agreement coefficient computed on sixty items is
    itself an estimate and gets a confidence interval.
14. **co-14 · judge-concordance** — measuring an automated judge against human labels is an
    inter-rater-agreement problem, and the same corrections apply.
15. **co-15 · concordance-is-per-question** — concordance is estimated separately for each criterion,
    because a judge's reliability is not a global property.
16. **co-16 · human-ceiling** — human labelers disagree with each other; the human-human agreement is the
    ceiling any judge can be expected to reach, and comparing a judge to perfection is a category error.
17. **co-17 · comparing-two-runs** — the question "is B better than A" is a hypothesis test, not a
    comparison of two printed numbers.
18. **co-18 · paired-comparison** — when both systems ran on the same cases, the paired test is far more
    sensitive than treating the runs as independent samples.
19. **co-19 · significance-vs-practical-importance** — a statistically detectable difference can be too
    small to act on, and a large difference on tiny n can be undetectable; both are routine.
20. **co-20 · bootstrap-resampling** — resampling the observed data approximates the sampling
    distribution of almost any statistic without a closed form, which is why it is the practical default
    for eval metrics.
21. **co-21 · multiple-comparisons** — testing twenty criteria at once manufactures apparent wins; the
    correction is arithmetic, and skipping it is how eval suites produce phantom improvements.
22. **co-22 · noise-floor-of-a-suite** — re-running an unchanged stochastic system produces a
    distribution, and its spread is the floor below which no CI regression bar can sit.
23. **co-23 · variance-from-stochastic-generation** — repeat runs of the same case are a distinct
    variance source from case-to-case sampling, and the two compose.
24. **co-24 · reporting-honestly** — the reportable unit is the estimate, its interval, the sample size,
    and the method — a number stripped of those cannot be checked by a reader.

## Tensions & trade-offs — when NOT to reach for this

- **Rigor vs sample size you actually have**: most of these techniques want more labeled cases than a
  team has budget to produce. The honest response is a wider interval and a more cautious claim, not a
  narrower method — but there is a real point where the sample is too small to support any decision and
  the correct action is to collect more, not to compute harder.
- **Chance correction vs interpretability**: a chance-corrected coefficient is the right statistic and is
  much harder to explain to a stakeholder than "they agreed 85% of the time". Report both, and expect to
  spend the explanation.
- **Bootstrap vs closed form**: the bootstrap works on almost any statistic and needs no distributional
  assumption, at the cost of compute and of a false sense of security on tiny samples — resampling forty
  cases does not manufacture information that forty cases do not contain.
- **When NOT to reach for this course**: if the eval decision is "does this parse against the schema",
  there is no uncertainty to quantify and no statistic to compute. Do not attach an interval to a
  deterministic result.
- **When NOT to reach for statistics at all**: an effect visible to the naked eye across every case does
  not need a test. Significance testing is for the ambiguous middle, and reaching for it on an obvious
  result is ceremony that delays the fix.
- **What this course deliberately does not cover**: regression modelling, causal inference, and
  product-experiment design. Those live in
  [`analytics-and-experimentation`](./analytics-and-experimentation.md), which shares some machinery but
  answers a different question.

## Lineage — why it beat the alternative

- The alternative that lost was reporting bare eval numbers and arguing about them, which persisted
  because it is fast and because the numbers look authoritative. It failed in the same specific ways
  every time: raw percent agreement was mistaken for agreement on skewed label distributions; pass-rate
  differences well inside run-to-run noise were shipped as improvements; and CI regression bars were set
  below the suite's own noise floor, producing random build failures that trained teams to ignore the
  gate. Each of those has been a solved problem in classical statistics for decades — chance-corrected
  agreement coefficients were developed precisely because raters agreeing by chance was inflating
  reliability claims in content analysis and medical diagnosis, and the bootstrap exists precisely
  because most interesting statistics have no closed-form sampling distribution. The reason this course
  exists as a separate body rather than as a chapter inside
  [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md) is that the deep-eval course's
  central claims — that a judge must be validated against humans, and that a regression bar must sit
  above a measured noise floor — are unteachable without this machinery, and burying it as an appendix
  is how it gets skipped. It is separated for the same reason
  [`analytics-and-experimentation`](./analytics-and-experimentation.md) is not a substitute: that course
  answers "did this product change move a business metric", which shares tools with, but is not, the
  question an eval asks.

## Worked examples

No fixed Beginner/Intermediate/Advanced bands (Annotated-concept); grouped by theme. Every quantity is
computed **twice** — once from its definition in plain Python so the learner sees what it is, then once
via the pinned statistical library so the learner knows what to call in practice, with the two verified
equal. Prose + WCAG-accessible Mermaid and plotted figures where a distribution or an interval is the
point. Colocated under `statistics-for-evaluation/learning/code/` (runnable) and `.../artifacts/`
(figures). Contiguous `ex-01..ex-46`. Every example cites the `co-NN` it exercises. All examples run on
synthetic or committed label data — no model calls, no keys.

### Theme A · Uncertainty on a rate (ex 01–12)

1. **ex-01 · two-runs-two-numbers** — the same unchanged system yields different pass rates on two
   samples — verify the spread is real and not a bug. (co-03, co-02)
2. **ex-02 · pass-rate-is-an-estimate** — annotate the pass rate as a sample proportion of an unknown
   true rate — verify the framing. (co-02)
3. **ex-03 · simulate-sampling-error** — draw repeated samples from a known true rate and plot the
   spread — verify the distribution tightens as n grows. (co-03)
4. **ex-04 · interval-from-definition** — compute a confidence interval on a rate from first principles —
   verify against the library. (co-04)
5. **ex-05 · normal-approximation-breaks** — compute an interval near a rate of 0.95 with small n — verify
   the approximation produces an interval extending above 1. (co-05)
6. **ex-06 · wilson-and-clopper-pearson** — compute better-behaved intervals on the same data — verify
   they stay in bounds. (co-05)
7. **ex-07 · interval-width-vs-n** — plot interval width against sample size — verify the shape and the
   diminishing return. (co-04, co-06)
8. **ex-08 · how-many-cases-for-this-effect** — compute the n needed to detect a stated effect at a stated
   precision — verify the number against a simulation. (co-06)
9. **ex-09 · forty-cases-cannot-see-it** — annotate a real effect invisible at n=40 and visible at n=400 —
   verify both. (co-06, co-19)
10. **ex-10 · overlapping-intervals-are-not-a-test** — two overlapping intervals that nonetheless differ
    significantly under a paired test — verify the common mistake. (co-04, co-18)
11. **ex-11 · interval-figure** — a plotted figure of pass rates with intervals for three prompt variants
    — verify each interval is labeled with n and method. (co-01, co-24)
12. **ex-12 · report-estimate-interval-n-method** — a reporting helper emitting all four fields — verify
    no bare number can escape it. (co-24, co-01)

### Theme B · Sampling (ex 13–20)

1. **ex-13 · random-sample** — draw a random sample of cases and estimate the rate — verify the estimate
   is unbiased across repeats. (co-07, co-02)
2. **ex-14 · convenience-sample-bias** — estimate from the failures someone happened to notice — verify
   the estimate is badly biased. (co-07)
3. **ex-15 · stratified-sample** — sample within failure-mode strata — verify per-stratum coverage.
   (co-08, co-07)
4. **ex-16 · reweight-a-stratified-estimate** — recover the population rate from an oversampled stratum —
   verify the reweighted estimate matches the truth. (co-08)
5. **ex-17 · rare-mode-invisible** — show a 1%-prevalence failure mode absent from a 50-case random sample
   — verify the miss and the stratified fix. (co-08)
6. **ex-18 · sampling-frame-mismatch** — sample from a log that excludes timeouts — verify the estimate
   answers a different question than intended. (co-07)
7. **ex-19 · sampling-diagram** — a Mermaid diagram of population → frame → sample → estimate with the
   failure point at each arrow — verify each stage. (co-07, co-08)
8. **ex-20 · sample-size-plan-for-an-eval-set** — produce a written sampling plan for a real eval set —
   verify it states target effect, precision, strata, and n. (co-06, co-08, co-24)

### Theme C · Agreement and judge concordance (ex 21–34)

1. **ex-21 · raw-percent-agreement** — compute raw agreement between two labelers — verify the
   arithmetic. (co-09)
2. **ex-22 · skewed-labels-inflate-agreement** — compute raw agreement where one label is 80% prevalent —
   verify how little it demonstrates. (co-09, co-12)
3. **ex-23 · agreement-by-chance** — compute the agreement two random labelers would reach on that
   distribution — verify it is close to the observed raw number. (co-10, co-09)
4. **ex-24 · chance-corrected-from-definition** — implement a two-rater chance-corrected coefficient from
   its definition — verify against the library. (co-10)
5. **ex-25 · the-coefficient-collapses** — show 85% raw agreement corresponding to a near-zero corrected
   coefficient — verify both numbers on the same data. (co-10, co-09)
6. **ex-26 · choose-the-coefficient** — a decision table mapping rater count, label type, and missing data
   to the appropriate coefficient — verify each branch against a worked case. (co-11)
7. **ex-27 · more-than-two-raters** — compute agreement across three labelers — verify the multi-rater
   coefficient differs from averaging pairwise. (co-11)
8. **ex-28 · ordinal-labels** — weight disagreements by distance on an ordinal scale — verify a
   one-step disagreement costs less than a three-step one. (co-11)
9. **ex-29 · prevalence-alongside-the-coefficient** — report the marginal label distribution beside every
   coefficient — verify the report is interpretable without the raw data. (co-12, co-24)
10. **ex-30 · interval-on-a-coefficient** — bootstrap an interval on an agreement coefficient computed
    over sixty items — verify the width. (co-13, co-20)
11. **ex-31 · judge-vs-human-is-agreement** — frame judge concordance as inter-rater agreement and compute
    it — verify the identical machinery applies. (co-14)
12. **ex-32 · concordance-per-criterion** — compute one judge's concordance separately on two criteria —
    verify the two values differ materially. (co-15)
13. **ex-33 · human-ceiling** — compute human-human agreement on the same items — verify the judge is
    compared against that ceiling rather than against perfect. (co-16)
14. **ex-34 · concordance-report** — a per-criterion concordance table with intervals, prevalence, n, and
    the human ceiling — verify every column is populated. (co-14, co-15, co-16, co-24)

### Theme D · Comparing runs and gating on them (ex 35–46)

1. **ex-35 · two-printed-numbers** — annotate why "72% vs 75%" is not yet a finding — verify the missing
   pieces. (co-17, co-01)
2. **ex-36 · unpaired-comparison** — test two runs treated as independent samples — verify the result and
   its low sensitivity. (co-17)
3. **ex-37 · paired-comparison** — test the same two runs paired by case — verify the paired test detects
   what the unpaired test missed. (co-18)
4. **ex-38 · paired-test-from-definition** — implement the paired test for binary outcomes from its
   definition — verify against the library. (co-18)
5. **ex-39 · significant-but-tiny** — a detectable difference too small to act on — verify the distinction
   from practical importance. (co-19)
6. **ex-40 · large-but-undetectable** — a large observed difference on n=20 that no test can support —
   verify the interval spans zero. (co-19, co-06)
7. **ex-41 · bootstrap-a-metric** — bootstrap an interval for a metric with no closed form — verify
   stability across resample counts. (co-20)
8. **ex-42 · bootstrap-does-not-create-data** — bootstrap n=15 and inspect the interval — verify the width
   honestly reflects the tiny sample. (co-20)
9. **ex-43 · twenty-criteria-one-phantom-win** — test twenty criteria on unchanged data — verify roughly
   one "significant" result appears by chance. (co-21)
10. **ex-44 · correct-for-multiple-comparisons** — apply a correction across the twenty tests — verify the
    phantom win disappears. (co-21)
11. **ex-45 · measure-a-suite-noise-floor** — re-run an unchanged stochastic suite and characterize the
    distribution, separating case-sampling variance from generation variance — verify both components.
    (co-22, co-23)
12. **ex-46 · capstone-statistically-defensible-eval-report** — a complete report for one real eval
    decision: a sampling plan with justified n, pass rates with small-n-appropriate intervals,
    per-criterion judge concordance chance-corrected and interval-bounded against the human ceiling, a
    paired comparison of candidate against baseline with a multiple-comparisons correction, and a
    regression bar derived from the measured noise floor — verify every number carries its interval, n,
    and method, and that the report's recommendation follows from the statistics rather than from the
    point estimates. (co-01–co-24)

## Capstone spec — intra-topic (concept → full runnable)

- **Goal**: produce a statistically defensible evaluation report for one real decision from
  [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md) — should this candidate change
  ship? — where every claim carries its uncertainty, every agreement number is chance-corrected and
  compared against the human ceiling, the run comparison is paired and corrected for multiple
  comparisons, and the CI regression bar is derived from a measured noise floor rather than chosen.
- **Concepts exercised**: [ ] a written sampling plan with justified n (co-06, co-07, co-08) [ ] pass
  rates with small-n-appropriate intervals (co-02, co-04, co-05) [ ] chance-corrected agreement with an
  interval and reported prevalence (co-09–co-13) [ ] per-criterion judge concordance against the human
  ceiling (co-14–co-16) [ ] a paired run comparison distinguishing significance from importance
  (co-17–co-19) [ ] bootstrap intervals for metrics without closed forms (co-20) [ ] a
  multiple-comparisons correction (co-21) [ ] a noise floor decomposed into sampling and generation
  variance (co-22, co-23) [ ] honest reporting of estimate, interval, n, and method throughout (co-24).
- **Ordered steps**:
  1. `statistics-for-evaluation/learning/capstone/sampling_plan.md` + `sample.py` — write the sampling
     plan (target effect, required precision, strata for rare failure modes, resulting n) and draw the
     sample with reweighting. Verify the plan's n is justified by a simulation and that the reweighted
     estimate recovers a known population rate on synthetic data.
  2. `agreement.py` — compute human-human agreement and per-criterion judge concordance, each
     chance-corrected, each with a bootstrap interval, each reported beside its label prevalence and the
     human ceiling. Verify every coefficient is computed twice — from definition and from the library —
     and that the two agree.
  3. `compare.py` — run the paired comparison of candidate against baseline across all criteria, apply a
     multiple-comparisons correction, and separate statistical detectability from practical importance.
     Verify the pipeline finds a planted real effect and rejects a planted phantom one.
  4. `noise_floor.py` + `report.md` — characterize the suite's noise floor with its sampling and
     generation components, derive the regression bar from it, and assemble the report. Verify the report
     contains no bare number: every figure carries estimate, interval, n, and method, and the shipping
     recommendation is traceable to the statistics.
- **Acceptance criteria**: the sampling plan states and justifies its n before any data is drawn; every
  reported rate carries an interval computed with a method appropriate to its sample size; every
  agreement figure is chance-corrected, interval-bounded, reported alongside label prevalence, and
  compared against the measured human ceiling rather than against perfect agreement; the run comparison
  is paired, corrected for multiple comparisons, and explicitly separates detectability from practical
  importance; the regression bar is derived from a measured noise floor with its two variance components
  identified; every statistic is computed both from its definition and via the pinned library with the
  results verified equal; and the report contains no number stripped of its interval, n, and method.
- **Done bar**: runnable end-to-end (offline, synthetic and committed label data, no model calls) +
  web-verified against a primary statistical reference.

## Read more

> Every reference below is `[Needs Verification]` at authoring: confirm the exact edition, year, and
> canonical formulation before citing, and cite the version actually read. This course must not ship a
> formula reproduced from memory.

- A standard reference on **inter-rater reliability and chance-corrected agreement coefficients** —
  covering the two-rater nominal case, the multi-rater case, weighted coefficients for ordinal labels,
  and the prevalence problem. Select and cite at authoring.
- A standard reference on **binomial confidence intervals**, covering why the normal approximation fails
  at small n and near the boundaries, and the Wilson and Clopper-Pearson alternatives taught here.
  Select and cite at authoring.
- A standard reference on **the bootstrap**, covering percentile intervals, resample-count guidance, and
  the explicit limits of resampling small samples. Select and cite at authoring.
- **Designing Machine Learning Systems** — Chip Huyen (2022). For the framing of evaluation uncertainty
  as a production concern; the statistical treatment itself comes from the references above.

## In which paths

- `immediately-effective/software-engineer-to-ai-engineer` — **owning path**: a hard prerequisite for
  [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md), placed immediately before it
  (D6).
- `interview-ready/software-engineer` — candidate placement in the AI & harness engineering deepening
  tail — pending manifest re-verification (D8 four-path rule).
- `immediately-effective/software-engineer` — candidate placement in the deepening band — pending
  manifest re-verification (D8 four-path rule).
- `fundamentally-strong/software-engineer` — candidate placement in Stage 12 · AI & harness engineering
  — pending manifest re-verification (D8 four-path rule).

---

← Back to [README.md — course library catalog](./README.md)
