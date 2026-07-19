# 63 · Analytics & Experimentation (By Example, Python †)

**prd row**: Pass 3 · Build for the Real World · By Example · Python † · Learn 163 / Drill 263 · Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: measuring what you ship without fooling yourself — event instrumentation, funnels and
cohorts, A/B testing, statistical significance and its traps, and reading a metric honestly. This is the
data-literacy pass every shipping engineer needs: the usable persistence layer is
[`10-sql-essentials`](./10-sql-essentials.md) and the discipline of a controlled comparison extends
[`15-software-testing`](./15-software-testing.md). Pulled earlier in the spiral because its prerequisites
are light. `†`: Python, fully type-annotated (DD-39, pyright-clean spirit), driving a query engine and a
small statistics stack.

## Why this exists · the big idea

- **The problem before the solution**: a shipped feature you cannot measure is a guess with a deploy
  button — teams argued from opinion and anecdote because they had no trustworthy way to tell whether a
  change helped, hurt, or did nothing.
- **Keep-this-if-you-forget-everything**: a number is only as honest as the way it was collected and
  compared — instrument deliberately, randomize the comparison, and assume every surprising result is a
  measurement artifact until it survives scrutiny.
- **Big ideas touched**: `correctness-vs-pragmatism` (a perfectly clean statistical result yields to a
  decision you can defend and ship — you choose a significance bar and a stopping rule, then live with the
  disciplined compromise), `determinism-vs-emergence` (product metrics are emergent signal from thousands
  of independent user choices, not a deterministic output — you measure the aggregate, and separate signal
  from noise rather than reading each event as truth).

## Prerequisites

- **Prior topics**: [topic 10 SQL Essentials](./10-sql-essentials.md) (aggregation, joins, and
  group-by over event tables) and [topic 15 Software Testing](./15-software-testing.md) (the mindset of a
  controlled comparison with a stated hypothesis).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** (fully type-annotated) with a pinned
  CVE-clean data/stats stack (a dataframe library plus a statistics/hypothesis-test module); a local SQL DB
  holding an events table; Neovim/VSCode with the Python LSP (DD-17).
- **Assumed knowledge**: writing an aggregate SQL query over a table (topic 10); stating a hypothesis and
  a pass/fail bar (topic 15); reading typed Python (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the statistical core is stable and correctly left version-unpinned — A/B test
  mechanics (randomized assignment, power/sample-size, p-values, confidence intervals), the classic traps
  (peeking/optional-stopping, multiple comparisons, Simpson's paradox, novelty and primacy effects), and
  funnel/cohort analysis are settled practice, not tooling that goes stale. Keep the Python stats stack at
  "a recent stable" in shipped text.
- 2026-07-12 — verified (GAP for plan owner): no specific analytics vendor or dataframe/stats library
  version is claimed in the body — re-verify exact package versions and any hosted-tool names once the
  worked examples are drafted.

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary source the pre-authoring `web-researcher` sweep fetched and read.
> Unverifiable-at-source items are flagged `[Needs Verification]` and must not be stated as settled fact
> in shipped teaching text.

- **Overall Evaluation Criterion (OEC), randomization, sample size, ramp-up** — Kohavi, Longbotham,
  Sommerfield, Henne, _"Controlled experiments on the web: survey and practical guide"_, _Data Mining and
  Knowledge Discovery_ 18:140–181 (2009). OEC = the quantitative metric the experiment is meant to move,
  chosen so short-term gains that hurt long-term value are penalised. Sample-size rule of thumb
  n ≈ 16σ²/Δ² per variant for 80% power (21 for 90%) at α = 0.05. Randomization must be (1) persistent,
  (2) independent of treatment, (3) uniform; hash-and-partition on a user id is the standard mechanism
  (MD5 shown to distribute cleanly; other hashes had bias). Primacy and newness (novelty) effects and
  ramp-up (gradual exposure %) are named there. `[Verified]`
- **p-value meaning & misuse** — Wasserstein & Lazar, _"The ASA Statement on p-Values: Context, Process,
  and Purpose"_, _The American Statistician_ 70(2):129–133 (2016), PMC5187603. Six principles, incl.
  "P-values do not measure the probability that the studied hypothesis is true, or the probability that
  the data were produced by random chance alone" and "a p-value near 0.05 taken by itself offers only weak
  evidence against the null." `[Verified]`
- **Type I/II error, significance level, power, CI & sample-size formula** — NIST/SEMATECH _e-Handbook of
  Statistical Methods_ §1.3.5, §7.2.2.2 (itl.nist.gov/div898/handbook). Type I = α (significance level),
  Type II = β, power = 1 − β; sample-size formula for a proportion/mean difference given α, β, and effect
  size. `[Verified]`
- **CUPED (variance reduction)** — Deng, Xu, Kohavi, Walker, _"Improving the Sensitivity of Online
  Controlled Experiments by Utilizing Pre-Experiment Data"_, WSDM 2013. Adjusted metric
  Ŷ_cv = Ȳ − θX̄ + θE[X] with θ = Cov(Y,X)/Var(X); variance shrinks by a factor (1 − ρ²), giving ~50%
  variance reduction when the pre-period covariate correlates strongly. `[Verified]`
- **Sample Ratio Mismatch (SRM)** — Fabijan et al., _"Diagnosing Sample Ratio Mismatch in Online
  Controlled Experiments"_, KDD 2019. A chi-square test on the observed vs expected assignment split;
  ~6% of Microsoft experiments tripped it; described as a top guardrail — a failing SRM invalidates the
  experiment and the analysis must stop. `[Verified]`
- **Peeking / optional-stopping / always-valid inference** — Johari, Pekelis, Walsh, _"Always Valid
  Inference: Continuous Monitoring of A/B Tests"_, arXiv:1512.04922. Repeatedly testing a fixed-horizon
  p-value and stopping at first significance inflates the false-positive rate far above α; sequential
  (always-valid) p-values or a pre-committed fixed sample size fix it. `[Verified]`
- **Simpson's paradox** — Stanford Encyclopedia of Philosophy, "Simpson's Paradox"
  (plato.stanford.edu/entries/paradox-simpson). An association that holds in every subgroup can reverse in
  the aggregate; the correct conditioning depends on the causal structure. `[Verified]`
- **Funnel / cohort / retention / DAU-MAU / North Star** — Amplitude documentation
  (amplitude.com/docs) and Amplitude's _North Star Playbook_. North Star = one metric with 3–5 input
  metrics forming a metric tree; standard product-analytics definitions of funnel, cohort, retention,
  DAU/MAU. `[Needs Verification]` on exact current wording (vendor docs revise without version tags).
- **Guardrail metrics** — Kohavi, Tang, Xu, _Trustworthy Online Controlled Experiments_ (2020): metrics
  that must NOT regress (latency, crash rate, unsubscribes) even when the OEC improves. `[Verified]`
  (book is the standard reference; specific page wording `[Needs Verification]`).
- **Frequentist vs Bayesian A/B testing** — vendor engineering docs (LaunchDarkly, VWO). Directional
  guidance only; treat as `[Needs Verification]` and teach the statistics from the peer-reviewed sources
  above, not the vendor framing.
- **Feature flags as experiment delivery** — LaunchDarkly docs: a flag both gates rollout and assigns the
  experiment bucket, so ramp % and holdout are the same mechanism. `[Needs Verification]` on exact wording.
- **`[Needs Verification]` / currency risk** — Segment's `analytics-python` SDK is in **maintenance mode**;
  do NOT teach it as the current recommended instrumentation path. Worked examples instrument via a
  hand-rolled typed event writer to a local SQL table instead, so nothing depends on a stale vendor SDK.
- **`[Needs Verification]` (paywalled / 403 at fetch time)** — Amazon's specific email-OEC formula, the
  full Benjamini–Hochberg FDR original text, and several survivorship/p-hacking/HARKing papers could not be
  fetched to source; the curriculum teaches Benjamini–Hochberg from its standard textbook statement and
  flags the rest rather than citing them as read.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · event-instrumentation** — a tracking plan names events and properties deliberately before
  any code emits them, so the schema is a contract not an accident.
- **co-02 · idempotent-events** — a stable event id (client- or server-side) lets the pipeline dedupe
  retries, so one user action counts exactly once and never double-counts.
- **co-03 · conversion-funnel** — an ordered sequence of steps, counting distinct users who reach each,
  measures where a flow leaks and what fraction converts end to end.
- **co-04 · retention-cohort** — grouping users by an entry event (e.g. signup week) and measuring their
  return over N days exposes whether a product keeps people, not just acquires them.
- **co-05 · segmentation** — slicing any metric by a user or event property (platform, country, plan)
  turns a single number into a comparison that can reveal or hide effects.
- **co-06 · north-star-metric** — one metric expressing delivered value, decomposed into 3–5 input
  metrics forming a metric tree, aligns a team without collapsing to a single gameable number.
- **co-07 · guardrail-metrics** — metrics that must NOT regress (latency, crash rate, unsubscribes) even
  when the OEC improves; a guardrail breach blocks a ship the primary metric would approve.
- **co-08 · ratio-metrics-treachery** — a ratio of two random quantities (clicks/user) is not a simple
  mean; its variance needs the delta method, and averaging ratios ≠ ratio of averages.
- **co-09 · hypothesis-and-oec** — a testable hypothesis plus an Overall Evaluation Criterion chosen so
  short-term wins that hurt long-term value are penalised, stated before data is collected.
- **co-10 · randomized-assignment** — persistent, treatment-independent, uniform assignment via
  hash-and-partition on a user id is the only mechanism that makes the counterfactual real.
- **co-11 · statistical-power** — Type I error = α (false positive), Type II = β (false negative),
  power = 1 − β; an underpowered test cannot detect a true effect and produces confident noise.
- **co-12 · sample-size-and-mde** — the minimum detectable effect and the required sample size
  (n ≈ 16σ²/Δ² per arm for 80% power) are committed BEFORE the test, not discovered during it.
- **co-13 · p-value** — the probability of a result at least this extreme under the null; it is NOT the
  probability the hypothesis is true, and 0.05 alone is weak evidence (ASA statement).
- **co-14 · confidence-interval** — a range of effect sizes consistent with the data at a stated level;
  it carries the effect magnitude a bare p-value hides, and drives the ship decision.
- **co-15 · peeking-optional-stopping** — repeatedly checking a fixed-horizon test and stopping at first
  significance inflates the false-positive rate far above α; fix with a pre-committed N or always-valid
  sequential inference.
- **co-16 · multiple-comparisons** — testing many metrics or variants inflates the family-wise error
  rate; Bonferroni (control FWER) or Benjamini–Hochberg (control FDR) restores honesty.
- **co-17 · simpsons-paradox** — an association present in every subgroup can reverse in the aggregate;
  which conditioning is correct depends on the causal structure, not the arithmetic.
- **co-18 · srm-sample-ratio-mismatch** — a chi-square test on observed vs expected assignment split; a
  failing SRM means the randomization is broken and the whole experiment is invalid — stop, don't analyse.
- **co-19 · cuped-variance-reduction** — adjusting the metric with a pre-experiment covariate
  (Ŷ = Ȳ − θX̄ + θE[X]) cuts variance by (1 − ρ²), reaching significance with far fewer users.
- **co-20 · novelty-primacy-effects** — a new treatment can spike (novelty) or dip (primacy) transiently
  before settling; reading day-one numbers as the steady state is a classic misread.
- **co-21 · seasonality-and-ramp** — weekly/holiday cycles and gradual exposure ramps mean a test must
  run over full cycles and account for the ramp, or it measures the calendar not the change.
- **co-22 · survivorship-bias** — analysing only the users/sessions that "survived" to the end silently
  drops the ones the change drove away, flattering the result.
- **co-23 · correlation-vs-causation** — only a randomized comparison licenses a causal claim; an
  observed correlation can be a confounder, reverse causation, or coincidence.
- **co-24 · goodhart-metrics-theater** — once a metric becomes a target it stops measuring what mattered;
  optimising a proxy (clicks, session length) can harm the real goal while every dashboard turns green.
- **co-25 · frequentist-vs-bayesian** — the two inference frameworks answer different questions (long-run
  error control vs posterior probability of an effect); each has a coherent stopping and decision rule.
- **co-26 · feature-flags-as-delivery** — a feature flag both gates rollout and assigns the experiment
  bucket, so ramp %, holdout, and treatment assignment are one mechanism, not three.

## Tensions & trade-offs — when NOT to reach for this

- **When NOT to A/B test**: below a traffic threshold you cannot reach statistical power, and a test just
  delays a decision you should make on judgment plus qualitative signal. Underpowered tests produce
  confident-looking noise — worse than no test.
- **Goodhart's law / metrics theater**: the moment a metric becomes a target it stops measuring what you
  cared about. Optimizing a proxy (clicks, session length) can actively harm the real goal (user value,
  retention) while every dashboard turns green.
- **Peeking is not impatience, it's a bug**: repeatedly checking a running experiment and stopping at the
  first significant reading inflates the false-positive rate badly. Fixing a sample size (or using a proper
  sequential method) up front is not optional rigor — it is the difference between a result and an
  artifact.

## Lineage — why it beat the alternative

- Controlled experimentation descends from R. A. Fisher's agricultural randomized trials and the clinical
  RCT: the insight that a randomized control group is the only clean way to separate an intervention's
  effect from everything else changing at once. The web made this cheap and continuous — Google, Microsoft,
  and Amazon industrialized online controlled experiments in the 2000s, replacing argue-from-opinion product
  decisions with measured ones. The through-line: randomize the comparison so the counterfactual is real,
  and treat surprising numbers as artifacts until proven otherwise. The instrumentation and honest-metric
  discipline built here feeds the telemetry and usage signals of the tools you ship next, including
  [`77-building-production-cli-tools`](./77-building-production-cli-tools.md).

## Worked examples

Colocated under `analytics-and-experimentation/learning/code/`; each runnable + exercised from the CLI,
Python fully type-annotated (DD-20/DD-30/DD-34/DD-39). Contiguous `ex-01..ex-78`. Every example cites the
`co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · tracking-plan-doc** — write a typed `Event` dataclass + a tracking-plan table (event name,
  properties, types) for a 3-step signup flow — verify every emitted event validates against the plan. (co-01)
- **ex-02 · event-schema-typed** — model events as a typed union (`SignupStarted`, `PlanSelected`,
  `SignupCompleted`) — verify pyright rejects a mistyped property. (co-01)
- **ex-03 · emit-events-to-table** — insert typed events into a local SQL `events` table via a
  hand-rolled writer (no vendor SDK) — verify rows land with correct columns. (co-01)
- **ex-04 · idempotency-key-dedup** — attach a stable `event_id`; re-emit the same event twice — verify
  an upsert keyed on `event_id` leaves exactly one row. (co-02)
- **ex-05 · client-vs-server-event** — emit the same conversion from a simulated client retry and a
  server confirmation — verify dedup keeps the server-authoritative row. (co-02)
- **ex-06 · avoid-double-count** — count a purchase event with and without dedup — verify the naive count
  overstates and the keyed count matches the true user total. (co-02)
- **ex-07 · count-distinct-users** — `COUNT(DISTINCT user_id)` vs `COUNT(*)` on the events table — verify
  the two differ when users repeat an event, and explain which a funnel needs. (co-03)
- **ex-08 · conversion-funnel-sql** — build a 3-step funnel (visited → started → completed) counting
  distinct users per step — verify each step ⊆ the previous. (co-03)
- **ex-09 · funnel-step-dropoff** — compute step-to-step drop-off percentages — verify they sum with the
  survivors to 100% of the entry cohort. (co-03)
- **ex-10 · funnel-overall-conversion** — compute end-to-end conversion (completed ÷ visited) — verify it
  equals the product of the per-step retention rates. (co-03)
- **ex-11 · cohort-by-signup-week** — bucket users into weekly signup cohorts — verify each user lands in
  exactly one cohort by their first event. (co-04)
- **ex-12 · retention-curve** — compute the % of each cohort active on days 1/7/30 — verify the curve is
  monotic non-increasing within a cohort. (co-04)
- **ex-13 · n-day-retention** — implement classic vs range ("bounded") N-day retention — verify the two
  definitions give different numbers on the same data and state which you chose. (co-04)
- **ex-14 · segment-by-property** — split conversion by platform (ios/android/web) — verify the weighted
  segments recombine to the overall rate. (co-05)
- **ex-15 · segment-funnel** — run the funnel per country segment — verify a segment with low volume is
  flagged as too small to read. (co-05)
- **ex-16 · north-star-definition** — pick a north-star metric (weekly active creators) and write it as a
  typed function over the events table — verify it returns a single number for a period. (co-06)
- **ex-17 · north-star-input-tree** — decompose the north star into 3–5 input metrics — verify the inputs
  reconstruct the north star (or explain the gap). (co-06)
- **ex-18 · guardrail-metric-list** — declare guardrails (p95 latency, error rate) as typed metrics —
  verify each returns a value and a pass/fail against a stated threshold. (co-07)
- **ex-19 · ratio-metric-trap** — average per-user click-through then compare to total clicks ÷ total
  users — verify the two disagree and name why (ratio of averages ≠ average of ratios). (co-08)
- **ex-20 · sample-mean-and-variance** — compute mean, variance, and standard error of a sample — verify
  SE shrinks as √n on resampled subsets. (co-14)
- **ex-21 · mean-ci-normal** — build a 95% CI for a sample mean via the normal approximation — verify
  ~95% of CIs over repeated samples cover the true mean. (co-14)
- **ex-22 · proportion-ci** — build a Wald + Wilson CI for a conversion proportion — verify Wilson behaves
  near p=0/1 where Wald fails. (co-14)
- **ex-23 · effect-size-abs-rel** — compute absolute and relative lift between two arms — verify the
  relative lift equals abs ÷ control rate. (co-14)
- **ex-24 · minimum-detectable-diff** — given a baseline rate and N, back out the smallest lift you could
  detect — verify a larger N lowers the MDE. (co-12)
- **ex-25 · hypothesis-statement** — encode a null + alternative hypothesis and a one/two-sided choice as
  typed config — verify the analysis reads the direction from it. (co-09)
- **ex-26 · oec-definition** — define an OEC that penalises a short-term-win/long-term-harm metric — verify
  a scenario that games the proxy scores worse on the OEC. (co-09)

### Intermediate

- **ex-27 · randomized-assignment-hash** — assign users to control/treatment by `md5(user_id+salt) % 100`
  — verify the split is ~50/50 over many ids. (co-10)
- **ex-28 · deterministic-bucketing** — re-run assignment for the same user twice — verify identical
  bucket (persistence property). (co-10)
- **ex-29 · assignment-independence** — check assignment is independent of a pre-existing user property —
  verify no correlation between bucket and platform. (co-10)
- **ex-30 · type-i-and-ii-errors** — simulate many null experiments at α=0.05 — verify ~5% false-positive
  rate; simulate a true effect and measure the false-negative rate. (co-11)
- **ex-31 · power-definition** — compute power = 1 − β for a fixed effect and N — verify it rises with N
  and with a larger true effect. (co-11)
- **ex-32 · sample-size-formula** — implement n ≈ 16σ²/Δ² per arm for 80% power — verify it matches a
  power simulation within tolerance. (co-12)
- **ex-33 · mde-tradeoff** — plot required N vs MDE — verify halving the MDE roughly quadruples N. (co-12)
- **ex-34 · power-curve** — sweep power across effect sizes at fixed N — verify the S-shaped curve crosses
  0.8 at the MDE. (co-11, co-12)
- **ex-35 · two-proportion-z-test** — run a two-proportion z-test on an A/B conversion result — verify the
  z-statistic and p-value against a hand computation. (co-13)
- **ex-36 · welch-t-test** — compare two continuous-metric arms with Welch's t-test — verify it handles
  unequal variances where Student's t would not. (co-13)
- **ex-37 · p-value-compute** — compute a p-value from a test statistic and its null distribution — verify
  a null-data run is uniform on [0,1]. (co-13)
- **ex-38 · p-value-misinterpretation** — write assertions that a p-value is NOT P(H₀ true) and NOT
  1−P(effect) — verify a worked counterexample. (co-13)
- **ex-39 · ci-p-value-agreement** — check a 95% CI excludes 0 exactly when p<0.05 for the same test —
  verify agreement on many simulated results. (co-14)
- **ex-40 · bootstrap-ci** — bootstrap a CI for a difference in means — verify it tracks the analytic CI
  on normal data and adapts on skewed data. (co-14)
- **ex-41 · ship-no-ship-decision** — combine effect CI + significance bar + guardrails into a typed
  decision — verify a guardrail breach flips a significant win to no-ship. (co-09, co-07)
- **ex-42 · guardrail-check-in-analysis** — evaluate guardrails alongside the OEC — verify a latency
  regression is surfaced even when conversion improves. (co-07)
- **ex-43 · srm-chi-square** — run a chi-square SRM test on the observed split — verify a clean 50/50
  passes and a 52/48 on large N fails. (co-18)
- **ex-44 · srm-guardrail-abort** — gate the analysis on SRM — verify a failing SRM aborts before any
  effect is reported. (co-18)
- **ex-45 · cuped-adjustment** — apply CUPED with a pre-period covariate (θ = Cov/Var) — verify the
  adjusted means are unbiased vs the raw means. (co-19)
- **ex-46 · cuped-variance-reduction** — measure variance before/after CUPED — verify the reduction ≈
  (1−ρ²) for the covariate correlation ρ. (co-19)
- **ex-47 · delta-method-ratio-metric** — compute the variance of a ratio metric via the delta method —
  verify it matches a bootstrap and differs from the naive per-user variance. (co-08)
- **ex-48 · sequential-vs-fixed-preview** — compare a fixed-horizon test to a group-sequential design on
  the same stream — verify both control α when used as designed. (co-15)
- **ex-49 · bonferroni-correction** — apply Bonferroni across k metrics — verify the family-wise error
  rate drops to ~α and power drops with it. (co-16)
- **ex-50 · benjamini-hochberg-fdr** — apply the BH procedure to a batch of p-values — verify it rejects
  more than Bonferroni while controlling the false-discovery rate. (co-16)
- **ex-51 · multiple-metrics-family** — run one experiment scored on 10 metrics — verify the naive
  "any significant" rule inflates false positives and the correction fixes it. (co-16)
- **ex-52 · frequentist-vs-bayesian-intro** — analyse the same A/B result both ways — verify the
  frequentist p-value and the Bayesian P(treatment>control) answer different questions. (co-25)
- **ex-53 · bayesian-beta-posterior** — model two conversion arms with Beta posteriors — verify
  P(treatment>control) via Monte Carlo matches a grid computation. (co-25)
- **ex-54 · feature-flag-assignment** — assign the experiment bucket through a simulated feature flag —
  verify flag state and experiment arm are the same mapping. (co-26)

### Advanced

- **ex-55 · peeking-simulation** — simulate a no-effect experiment, test daily, stop at first p<0.05 —
  verify the false-positive rate blows past 5%. (co-15)
- **ex-56 · peeking-false-positive-rate** — sweep number-of-peeks vs realised α — verify the inflation
  grows with peek count. (co-15)
- **ex-57 · fixed-sample-fixes-peeking** — enforce a pre-committed N and test once — verify the
  false-positive rate returns to ~5%. (co-15)
- **ex-58 · always-valid-sequential** — implement an always-valid p-value (mixture SPRT / e-value) —
  verify continuous monitoring keeps type-I control. (co-15)
- **ex-59 · alpha-spending** — implement an O'Brien-Fleming-style spending function for k looks — verify
  cumulative α stays ≤ the target. (co-15)
- **ex-60 · simpsons-paradox-demo** — construct data where treatment wins in every segment but loses
  overall — verify both facts numerically. (co-17)
- **ex-61 · simpsons-segment-weighting** — show the reversal comes from unequal segment sizes/mix — verify
  reweighting to equal exposure restores the within-segment direction. (co-17)
- **ex-62 · novelty-effect-decay** — simulate a treatment that spikes then decays to baseline — verify a
  day-1 read overstates the steady-state effect. (co-20)
- **ex-63 · primacy-effect** — simulate a treatment that dips then recovers — verify an early stop would
  wrongly reject it. (co-20)
- **ex-64 · seasonality-weekly** — inject a weekday/weekend cycle — verify a sub-week test misreads the
  effect and a full-week test recovers it. (co-21)
- **ex-65 · ramp-up-exposure** — model a gradual exposure ramp — verify pooling ramp-period data biases
  the estimate and excluding it fixes it. (co-21)
- **ex-66 · survivorship-bias-demo** — analyse only end-of-funnel survivors — verify it flatters the
  result vs the full intent-to-treat cohort. (co-22)
- **ex-67 · correlation-not-causation** — generate a confounded observational correlation — verify a
  naive regression finds an effect that randomization removes. (co-23)
- **ex-68 · confounder-randomization** — add the confounder, then randomize assignment — verify the
  spurious effect disappears under randomization. (co-23)
- **ex-69 · goodhart-proxy-harm** — optimise a proxy metric (clicks) — verify the real goal (retention)
  degrades while the proxy climbs. (co-24)
- **ex-70 · metrics-theater-dashboard** — build a dashboard that turns green while the OEC falls — verify
  the guardrail/OEC pairing catches what the vanity metric hides. (co-24)
- **ex-71 · guardrail-catches-regression** — ship a "winning" variant that breaks a guardrail — verify the
  guardrail gate blocks it end to end. (co-07)
- **ex-72 · underpowered-test-noise** — run a test below its required N — verify the CI is too wide to
  decide and the "significant" reads are unstable across reruns. (co-12)
- **ex-73 · when-not-to-ab-test** — given a low-traffic feature, compute that power is unreachable — verify
  the tool recommends a judgment call over an underpowered test. (co-12)
- **ex-74 · bayesian-decision-rule** — set a Bayesian decision threshold (expected loss) — verify it and a
  frequentist rule can disagree and document the stopping rule for each. (co-25)
- **ex-75 · feature-flag-ramp-experiment** — ramp a flag 1%→50% while holding an experiment arm — verify
  the ramp % and the assignment stay consistent. (co-26)
- **ex-76 · holdout-group** — keep a long-run holdout via the flag — verify the holdout measures cumulative
  treatment effect the per-experiment reads miss. (co-26)
- **ex-77 · end-to-end-honest-experiment** — instrument → assign → pre-commit N → analyse with CI + SRM +
  guardrails — verify a known-null dataset does not read significant. (co-09, co-10, co-18)
- **ex-78 · decision-memo-reconcile** — generate a decision memo whose numbers are pulled from the analysis
  output — verify every figure in the memo matches the computed result. (co-09, co-07)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: run one honest experiment end to end — instrument the events, build the funnel/cohort view,
  design an A/B test with a pre-committed sample size, analyze it with a confidence interval and a stated
  significance bar, and write a decision memo that names the guardrail metrics and the traps you controlled
  for — all in fully type-annotated Python.
- **Concepts exercised**: [ ] event instrumentation + tracking plan (co-01, co-02) [ ] funnel + retention
  cohort (co-03, co-04) [ ] north-star + guardrail metrics (co-06, co-07) [ ] randomized assignment +
  pre-committed sample size (co-10, co-12) [ ] confidence interval + significance decision (co-13, co-14,
  co-09) [ ] a named-trap check — peeking / multiple comparisons / Simpson's / SRM (co-15, co-16, co-17,
  co-18).
- **Ordered steps**:
  1. `.../learning/capstone/code/instrument/` — emit typed events into the DB and build a funnel + cohort
     query. Verify the funnel counts reconcile with the raw event rows (no double-counting).
  2. `.../learning/capstone/code/design/` — state the hypothesis, north-star + guardrail metrics, and
     compute the required sample size for a chosen minimum detectable effect. Verify the power calculation
     runs and outputs a concrete N.
  3. `.../learning/capstone/code/analyze/` — randomize assignment on a provided dataset, compute the effect
     size + confidence interval + p-value. Verify a known-null dataset does not read as significant.
  4. `.../learning/capstone/decision-memo.md` — the ship/no-ship call, the guardrail readings, and the
     specific trap you controlled (peeking, multiple comparisons, or Simpson's). Verify the memo's numbers
     match the analysis output.
- **Acceptance criteria**: instrumentation reconciles with raw events; the sample size is committed before
  analysis; the significance decision follows from a CI + stated bar; a named trap is explicitly checked;
  all Python is type-annotated and runs from the CLI.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing** — Ron Kohavi, Diane
  Tang, Ya Xu (2020). Written by experimentation leaders at Google, LinkedIn, and Microsoft; the standard
  modern reference for running trustworthy A/B tests at scale.
- **Lean Analytics: Use Data to Build a Better Startup Faster** — Alistair Croll, Benjamin Yoskovitz
  (2013). Widely read reference connecting product analytics to actionable business metrics.

**Papers & articles**

- **Seven Pitfalls to Avoid when Running Controlled Experiments on the Web** — Thomas Crook, Brian Frasca,
  Ron Kohavi, Roger Longbotham (2009), KDD. Highly cited paper on common statistical and practical mistakes
  in online experimentation. <https://dl.acm.org/doi/10.1145/1557019.1557139>

---

← Previous: [62 · IT Governance, Risk & Compliance](./62-it-governance-grc.md) · Next: [64 · Just Enough Go](./64-just-enough-go.md) →
