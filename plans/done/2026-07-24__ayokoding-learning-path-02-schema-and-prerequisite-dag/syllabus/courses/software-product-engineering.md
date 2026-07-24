# Software Product Engineering (Annotated-concept, — (concept, no code))

**Course ID**: `software-product-engineering` · **Format**: Annotated-concept · **Language**: — (concept, no code).

**Short summary**: Turning engineering into shipped products

**Scope note**: the **Product & Delivery** track (`▲`) — product thinking for engineers: discovery,
prioritization, value delivery, and metrics, so engineers build the right thing, not just build the thing
right. Leadership/governance topic (`‡`): **no code** — prose, worked design/decision exercises, and
diagrams. Pairs with [`09-project-management`](./project-management.md), which handles delivery
execution.

## Why this exists · the big idea

- **The problem before the solution**: engineers optimize _building the thing right_ and can ship a
  flawless product nobody needs — the most expensive waste in software is a well-built wrong thing.
- **Keep-this-if-you-forget-everything**: start from the user's problem and the outcome, not the feature —
  output is motion, outcome is the point, and the two are easy to confuse.
- **Big ideas touched**: `correctness-vs-pragmatism` (MVP and experiments are deliberately incomplete-but-validated
  bets), `mechanism-vs-policy` (product decides _what_ to build; engineering is the mechanism that builds it).

## Prerequisites

- **Prior topics**: no code prerequisites. Assumes the reader has **built working software** across Pass 1
  (e.g. [topic 11 Backend](./backend-essentials.md), [topic 14 Frontend](./frontend-essentials.md),
  [topic 15 Testing](./software-testing.md)) so product trade-offs land against real building experience.
- **Tools & environment**: a macOS/Linux terminal and a Markdown editor (Neovim per DD-17) for the written
  artifacts; no runtime/toolchain — deliverables are decision documents, not programs.
- **Assumed knowledge**: what it takes to ship a small feature end to end; reading a simple metric/funnel.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28) and re-verified under the DD-35
> no-hallucination pass against primary/authoritative sources (author fetched and read each cited page).

- 2026-07-12 — verified attribution + framing (each traced to a primary source):
  - **JTBD** — Christensen, Cook & Hall, "Marketing Malpractice," _HBR_ Dec 2005, and Christensen et al.,
    "Know Your Customers' Jobs to Be Done," _HBR_ Sept 2016. The unit of analysis is the _circumstance_,
    not the demographic. Ulwick's **Outcome-Driven Innovation** is a distinct, earlier (~1990s) quantitative
    variant — teach the two as related-but-separate, do not conflate.
  - **RICE** — Sean McBride, Intercom blog, Jan 2018; formula `(Reach × Impact × Confidence) ÷ Effort`.
  - **MoSCoW** — Dai Clegg (Oracle UK, ~1994), donated to the DSDM Consortium; "Won't" means "won't _this
    time_" (out of scope for this timebox), not permanent rejection.
  - **Kano model** — Noriaki Kano et al., "Attractive Quality and Must-Be Quality," 1984; teach the three
    practically load-bearing categories — must-be/one-dimensional(performance)/attractive. Resolved
    2026-07-18 (see re-verification entry below): secondary academic literature attributes a fourth
    category, "indifferent," to the 1984 original alongside these three; "reverse quality" is documented
    in later literature and is not confirmed as part of the original four — present must-be/performance/
    attractive as this topic's teaching core, and indifferent/reverse as recognized-but-secondary categories.
  - **AARRR "Pirate Metrics"** — Dave McClure, "Startup Metrics for Pirates," 2007 (predates 500 Startups;
    do not credit the firm).
  - **North-star metric** — coined/popularized by Sean Ellis; systematized as the North Star Framework by
    Amplitude (John Cutler). Distinct from **OMTM ("One Metric That Matters,"** Croll & Yoskovitz, _Lean
    Analytics_ 2013) — do not use interchangeably.
  - **MVP / Build-Measure-Learn / validated learning** — Eric Ries, _The Lean Startup_ (2011) and
    theleanstartup.com/principles: MVP is "the fastest way to get through the Build-Measure-Learn loop with
    the minimum effort" to test a hypothesis — explicitly **not** the smallest shippable product.
  - **Continuous discovery / opportunity-solution tree** — Teresa Torres, _Continuous Discovery Habits_
    (2021), producttalk.org. **The Mom Test** — Rob Fitzpatrick (2013): ask about past behavior/specifics,
    never pitch the idea.
  - **Guardrail metric** — standard term, formalized in Kohavi, Tang & Xu, _Trustworthy Online Controlled
    Experiments_ (Cambridge, 2020): a must-not-regress metric distinct from the primary OEC.
  - **Feature-toggle taxonomy** (release / experiment / ops / permission) — authored by **Pete Hodgson**,
    published _on_ martinfowler.com (2016). Credit Hodgson, not Fowler himself.
  - **Four big risks** (value / usability / feasibility / viability) — Marty Cagan, SVPG / _Inspired_.
    **Dual-track discovery+delivery** — Jeff Patton / Cagan. Resolved 2026-07-18 (see re-verification entry
    below): confirmed via a primary source that Cagan's current writing avoids the term and frames a
    discovery/delivery team split as an anti-pattern; teach this as a principle (one continuous
    cross-functional team, not two), not as a dated historical claim about a dropped term.
  - **HEART** (Happiness/Engagement/Adoption/Retention/Task-success) — Rodden, Hutchinson & Fu, Google, ACM
    CHI 2010.
  - **Goodhart's Law** — concept: Charles Goodhart (1975); the popular phrasing "when a measure becomes a
    target it ceases to be a good measure" is **Marilyn Strathern's** 1997 reformulation — attribute the law
    to Goodhart and the wording to Strathern.
  - **Vanity vs actionable metrics** — Eric Ries (2009 guest post, expanded in _The Lean Startup_).
  - **PR-FAQ / "working backwards"** — Amazon internal practice (mid-2000s); documented in Bryar & Carr,
    _Working Backwards_ (2021). **Shape Up** (appetite / shaping / betting / circuit-breaker) — Ryan Singer,
    Basecamp (2019), basecamp.com/shapeup.
  - **WSJF** — Reinertsen's CD3: `WSJF = Cost of Delay ÷ Duration` (_Principles of Product Development Flow_,
    2009). Resolved 2026-07-18 (see re-verification entry below): SAFe's proxy sub-formula (Business/user
    Value + Time Criticality + Risk Reduction/Opportunity Enablement, divided by Job Size) is confirmed via
    SAFe's own public page; cite Reinertsen's core ratio as this topic's primary formula, flag SAFe's named-
    factor variant as a related-but-distinct proprietary elaboration.
  - **Impact–effort matrix** — a generic/folk 2×2 with no verifiable single originator; present it as a
    common tool, do **not** attribute it to a named person or company.
- 2026-07-18 — `web-researcher` follow-up pass resolving the three `[Needs Verification]` items above
  (Phase 35 V step); all three fetched live and read directly (not from cache or a secondary quote):
  - **Kano model categories**: `en.wikipedia.org/wiki/Kano_model`'s "Satisfaction drivers terminology"
    comparison table (citing Bartikowski & Llosa, 2003, "Identifying Satisfiers, Dissatisfiers, Criticals
    and Neutrals in Customer Satisfaction," Euromed working paper) attributes **four** driver types
    directly to "Kano (1984)": Must-be, Attractive, One-dimensional, and Indifferent — "Reverse Quality" is
    documented on the same page but not attributed to the 1984 row in that comparison table. Resolution:
    treat must-be/one-dimensional/attractive as the practically load-bearing three this topic teaches;
    treat "indifferent" as also traceable to the 1984 original per this secondary academic source, and
    "reverse" as a related-but-separately-documented category, not confirmed part of the original four.
  - **Dual-track discovery+delivery**: fetched Marty Cagan's own article "Discovery – Delivery"
    (svpg.com/discovery-delivery/, Oct 30, 2020, part of his "common confusions" series, still live as of
    2026-07-18) directly. The article never uses the phrase "dual-track" and explicitly calls a
    discovery-team/delivery-team split a "very damaging anti-pattern," insisting on one continuous,
    cross-functional team doing both. This is a primary source consistent with (though not a verbatim
    quote of) the secondary reports that Cagan moved away from the "dual-track" phrasing. Resolution:
    teach the underlying principle (one team, continuous discovery+delivery) as intended; do not assert a
    dated "he dropped the term on date X" historical claim, which remains unconfirmed as a discrete event.
  - **WSJF / SAFe proxy formula**: fetched `framework.scaledagile.com/wsjf/` (canonical redirect target of
    `scaledagileframework.com/wsjf/`) directly on 2026-07-18. The publicly visible portion (no login
    required) confirms SAFe estimates WSJF as relative Cost of Delay ÷ relative job duration, with Cost of
    Delay composed of relative user/business value, time criticality, and risk reduction/opportunity
    enablement — matching the commonly-cited proxy sub-formula's factor list; the full worked-arithmetic
    breakdown remains gated behind SAFe's login as of this date (the page literally reads "Log in to
    continue reading" past the definition). Resolution: cite Reinertsen's core CD3 ratio (Cost of Delay ÷
    Duration, _Principles of Product Development Flow_, 2009) as this topic's primary, non-proprietary
    formula; name SAFe's factor list (value, time criticality, risk reduction/opportunity enablement, job
    size) as a related-but-distinct proprietary elaboration, confirmed public but not fully reproduced here
    (its complete worked formula is gated).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 8 (Leadership ‡ no-code topic). Each scenario below cites the co-NN it exercises. -->

- **co-01 · outcome-vs-output** — output is what a team ships; outcome is the change in user behaviour it causes; a team can maximize output while producing zero outcome, and the two are easy to confuse.
- **co-02 · problem-before-solution** — a well-formed problem statement names the user, the circumstance, and the desired outcome, and deliberately withholds the solution so the space of answers stays open.
- **co-03 · jobs-to-be-done** — customers "hire" a product to make progress against a job that arises in a circumstance; the unit of analysis is the job/circumstance, not the demographic (Christensen), distinct from Ulwick's Outcome-Driven Innovation.
- **co-04 · customer-discovery-interviewing** — the Mom Test: ask about the person's real past behaviour and specifics, never pitch or ask them to predict what they'd do, because people lie to be kind about your idea.
- **co-05 · continuous-discovery-opportunity-solution-tree** — discovery is a habit, not a phase; an opportunity-solution tree maps a desired outcome → opportunities → solutions → assumption tests so features trace back to a validated need.
- **co-06 · riskiest-assumption-and-four-big-risks** — every bet carries value, usability, feasibility, and business-viability risk (Cagan); the discipline is to test the _riskiest_ assumption most cheaply before committing, not to research everything or nothing.
- **co-07 · rice-prioritization** — RICE scores an item as `(Reach × Impact × Confidence) ÷ Effort`, making the estimate and its uncertainty explicit and comparable across a backlog.
- **co-08 · moscow-prioritization** — MoSCoW buckets requirements into Must / Should / Could / Won't-this-time, where "Won't" is scoped to the current timebox, not permanently rejected.
- **co-09 · impact-effort-matrix** — a generic 2×2 of impact vs effort surfaces quick wins (high-impact/low-effort) from time-sinks; a fast folk tool with no single named inventor.
- **co-10 · kano-model** — features relate to satisfaction non-linearly: must-be (absence dissatisfies, presence is neutral), performance (linear), and attractive/delighter (presence delights, absence is neutral).
- **co-11 · cost-of-delay-and-wsjf** — sequencing by economic urgency: `WSJF = Cost of Delay ÷ Duration` (Reinertsen's CD3) ranks short high-urgency jobs ahead of long low-urgency ones.
- **co-12 · mvp-as-hypothesis-test** — an MVP is the fastest path through Build-Measure-Learn for a chosen hypothesis, not the smallest shippable product; "minimum" qualifies the _learning bet_, which may be a non-shippable artifact (concierge, landing page).
- **co-13 · build-measure-learn-pivot-or-persevere** — the core loop turns a hypothesis into a measurement and a decision to pivot (change direction) or persevere (double down), with validated learning as the unit of progress.
- **co-14 · iterative-incremental-delivery** — value ships in thin end-to-end slices that each stand alone and return signal, rather than one big-bang release, so learning and risk are spread across the timeline.
- **co-15 · ab-experimentation-hypothesis-and-guardrail** — a trustworthy online experiment names a hypothesis, a single primary metric (the OEC), and guardrail metrics that must not regress (Kohavi et al.).
- **co-16 · feature-flag-toggle-taxonomy** — release, experiment, ops, and permission toggles have different lifespans and owners (Hodgson); conflating them creates flag debt and accidental long-lived branches in production.
- **co-17 · north-star-and-input-metrics** — a north-star is one durable metric that captures delivered value, decomposed into a few input metrics teams can actually move; distinct from a stage-specific OMTM.
- **co-18 · aarrr-funnel** — the customer lifecycle as Acquisition → Activation → Retention → Referral → Revenue (McClure), a shared vocabulary for where a product leaks users.
- **co-19 · heart-framework** — Google's Happiness / Engagement / Adoption / Retention / Task-success mapped through Goals → Signals → Metrics, so a chosen metric traces to a stated product goal.
- **co-20 · activation-and-retention** — activation (the user's first genuine value moment) and retention (repeat value over time) are the funnel's hardest, highest-leverage stages, and each needs an explicit, testable definition.
- **co-21 · vanity-vs-actionable-metrics** — an actionable metric ties a specific change to a resulting effect against a hypothesis; a vanity metric (raw totals) looks good but drives no decision (Ries).
- **co-22 · goodhart-metric-gaming** — "when a measure becomes a target, it ceases to be a good measure" (Strathern's phrasing of Goodhart's law): optimizing a proxy degrades it, so metrics need guardrails and judgment.
- **co-23 · writing-specs-and-pr-faq** — a good spec states the customer problem and expected outcome before the build; Amazon's "working backwards" PR-FAQ writes the press release and FAQ _first_ to force clarity on value.
- **co-24 · dual-track-discovery-and-delivery** — discovery and delivery run as parallel continuous tracks, not a waterfall handoff, so the team validates what to build while building what is already validated.
- **co-25 · shaping-and-appetite** — Shape Up fixes an _appetite_ (time budget) and shapes a problem to fit it, bets at a betting table, and uses a circuit-breaker so unfinished work stops rather than silently overrunning (Singer).
- **co-26 · engineer-product-design-collaboration** — engineers are not order-takers: their feasibility knowledge surfaces cheaper alternatives and hidden constraints early, and the strongest products come from the trio deciding together.

## Tensions & trade-offs — when NOT to reach for this

- **Discovery vs delivery**: too much research and you analysis-paralyze; too little and you build
  confidently in the wrong direction. The bet is always under uncertainty — validate the _riskiest_
  assumption most cheaply, then commit, rather than researching everything or nothing.
- **MVP vs credibility**: a "minimum" product too thin damages trust and mis-measures demand (users reject
  the execution, not the idea); too fat and you've spent the learning budget before the first signal.
  "Minimum" describes the _hypothesis_ under test, not the smallest possible code.
- **Metrics vs judgment**: a north-star focuses a team, but any single metric is gameable — engagement is
  not value, and a locally optimized funnel can degrade the whole. Quantitative signal informs product
  judgment; it does not replace it.

## Lineage — why it beat the alternative

- Product engineering rose as a reaction to two failures: waterfall's build-the-full-spec-then-discover-it's-wrong
  (1970s–90s), and feature-factory Agile that shipped output velocity while ignoring outcomes. Lean Startup
  (Ries, 2011) reframed the unit of progress as _validated learning_; Jobs-to-be-Done (Christensen) reframed
  features as hired for a job; continuous discovery (Torres) wove research into delivery instead of front-loading
  it. The durable idea beneath the framework churn is singular: _reduce the cost of being wrong_. That is why
  this topic pairs with [`09-project-management`](./project-management.md) (deliver the validated thing) and
  matures into the strategic altitude of [`33-engineering-management`](./engineering-management.md) /
  [`33-engineering-management`](./engineering-management.md).

## Worked examples

No-code design/decision scenarios under `software-product-engineering/learning/artifacts/` (prose +
diagrams; no `code/` runtime — DD-27 leadership kind). Contiguous `ex-01..ex-30`. Every scenario cites the
`co-NN` it exercises; every concept above is exercised by ≥1 scenario.

### Beginner

- **ex-01 · outcome-vs-output-rewrite** — rewrite three feature-request tickets ("add an export button") as outcome statements — verify each names a user behaviour change, not a feature. (co-01)
- **ex-02 · problem-statement-from-request** — turn a vague request into a problem statement — verify it names user + circumstance + desired outcome and withholds the solution. (co-02)
- **ex-03 · jtbd-job-story** — write a job story ("when \_\_\_, I want to \_\_\_, so I can \_\_\_") for a sample product — verify it names the circumstance, the motivation, and the expected progress. (co-03)
- **ex-04 · mom-test-interview-script** — draft six discovery questions for a feature idea — verify every question asks about past behaviour/specifics and none pitches the idea. (co-04)
- **ex-05 · mom-test-red-flag-audit** — mark which of eight given interview questions violate the Mom Test — verify each flagged question asks for an opinion, a hypothetical, or a future prediction. (co-04)
- **ex-06 · rice-score-single-feature** — compute RICE for one feature from stated Reach/Impact/Confidence/Effort — verify the arithmetic equals `(R × I × C) ÷ E` and each factor's unit is named. (co-07)
- **ex-07 · moscow-bucketing** — sort a ten-item backlog into Must/Should/Could/Won't-this-time — verify each "Won't" item is scoped to this release, not rejected outright. (co-08)
- **ex-08 · impact-effort-quadrant** — place eight initiatives on the impact–effort 2×2 and name the quick wins — verify quick wins sit in the high-impact/low-effort quadrant. (co-09)
- **ex-09 · aarrr-funnel-map** — map a sample product's events onto the five AARRR stages — verify each stage has ≥1 concrete event in the correct order. (co-18)
- **ex-10 · vanity-metric-audit** — flag which of six metrics are vanity — verify each flagged metric lacks a cause→effect tie to a decision. (co-21)

### Intermediate

- **ex-11 · rice-backlog-ranking** — RICE-rank a six-item backlog and defend the order — verify each score is justified and the ordering follows the computed scores. (co-07)
- **ex-12 · rice-vs-moscow-reconciliation** — a feature is "Must" in MoSCoW but low in RICE; write the reconciliation — verify it names why a business necessity overrides the score. (co-07, co-08)
- **ex-13 · kano-classification** — classify six features as must-be / performance / attractive — verify each cites its presence-vs-satisfaction shape. (co-10)
- **ex-14 · wsjf-sequencing** — sequence four jobs by `WSJF = Cost of Delay ÷ Duration` — verify the ordering matches the computed ratios. (co-11)
- **ex-15 · riskiest-assumption-triage** — for a feature, list the four big risks and pick the one to test first — verify it names value/usability/feasibility/viability and the cheapest test of the chosen risk. (co-06)
- **ex-16 · mvp-scope-cut-with-engineering-input** — cut a twelve-feature idea to an MVP for one hypothesis while an engineer proposes a cheaper 80%-value alternative — verify the MVP tests the riskiest assumption (not the smallest build) and the feasibility-driven alternative is named. (co-12, co-06, co-26)
- **ex-17 · build-measure-learn-pivot-or-persevere** — given an MVP's result, write the pivot-or-persevere decision — verify it states the hypothesis, the measurement, and which of pivot/persevere follows and why. (co-13)
- **ex-18 · release-slicing-increments** — slice a feature into three thin end-to-end increments — verify each slice ships value alone and returns a distinct signal. (co-14)
- **ex-19 · opportunity-solution-tree** — draw an OST: outcome → three opportunities → solutions → assumption tests — verify each solution traces up to an opportunity and the outcome. (co-05)
- **ex-20 · ab-experiment-design** — design an A/B test with a hypothesis, primary metric, and guardrail — verify it names exactly one hypothesis, one primary (OEC) metric, and ≥1 guardrail. (co-15)
- **ex-21 · guardrail-metric-selection** — pick guardrails for a checkout-speed experiment — verify each guardrail is a must-not-regress metric distinct from the primary. (co-15)
- **ex-22 · feature-flag-toggle-classification** — classify five flags as release / experiment / ops / permission — verify each classification cites the toggle category's expected lifespan. (co-16)

### Advanced

- **ex-23 · north-star-and-inputs** — choose a north-star for a sample product plus three input metrics, and explain why it differs from a stage-specific OMTM — verify the NSM measures delivered value and each input is a lever the team controls. (co-17, co-20)
- **ex-24 · heart-goals-signals-metrics** — fill a HEART Goals→Signals→Metrics row for one product goal — verify goal, signal, and metric are all present and mutually consistent. (co-19)
- **ex-25 · activation-metric-definition** — define an "activation" event and its measure for a sample app — verify it names the first genuine value moment and is testable. (co-20)
- **ex-26 · goodhart-guardrail-memo** — a team is gaming an engagement metric; propose a redesign — verify it names the gaming path and a concrete countermeasure. (co-22)
- **ex-27 · discovery-vs-delivery-balance** — a team is over-researching; write the "commit now" call inside a dual-track cadence — verify it names the riskiest-assumption-validated stop rule. (co-24, co-06)
- **ex-28 · pr-faq-working-backwards** — write a one-page PR-FAQ for a small feature before building — verify the press release states the customer problem and the FAQ answers the top risks. (co-23)
- **ex-29 · shape-up-pitch** — write a Shape Up pitch: appetite, problem, solution outline, rabbit-holes, no-gos — verify the appetite is a fixed budget and a circuit-breaker is named. (co-25)
- **ex-30 · full-product-brief-consistency** — assemble a problem statement, MVP scope, RICE-ranked backlog, metrics, and an experiment into one brief and check internal consistency — verify scope serves the problem, metrics measure the outcome, and the experiment tests the hypothesis. (co-01, co-07, co-12, co-15, co-17)

## Capstone spec — intra-topic (leadership ‡ → design/decision artifact)

- **Goal**: produce a compact **product brief** for a small feature: a validated problem statement (JTBD),
  an MVP scope with explicit non-goals, a RICE-prioritized backlog, a north-star + supporting metrics, and
  an A/B experiment design — a decision artifact an engineer could hand to a team and act on.
- **Concepts exercised**: [ ] problem vs solution framing via JTBD (co-02, co-03) [ ] MVP scope + explicit
  non-goals (co-12) [ ] RICE prioritization with a defended ordering (co-07) [ ] north-star + AARRR funnel
  metrics (co-17, co-18) [ ] an A/B experiment with hypothesis, primary metric, and guardrail (co-15).
- **Ordered steps**:
  1. `software-product-engineering/learning/capstone/brief.md` — problem statement + JTBD + evidence.
     Verify it states the user problem, not a pre-chosen solution.
  2. Add MVP scope + explicit non-goals + a RICE-ranked backlog. Verify each RICE score is justified and the
     ordering is defended.
  3. Add the metrics section (north-star + AARRR funnel) and an A/B experiment design. Verify the
     experiment names a hypothesis, a primary metric, and a guardrail metric.
- **Acceptance criteria**: the brief is internally consistent (scope serves the stated problem; metrics
  measure the outcome; the experiment tests the hypothesis) and defensible without hand-waving.
- **Done bar**: produces the stated artifact (product brief) + web-verified.

## Read more

**Books**

- **Inspired: How to Create Tech Products Customers Love** — Marty Cagan (2008; 2nd ed. 2017). The standard reference on product management and product engineering practice at technology companies.
- **Continuous Discovery Habits** — Teresa Torres (2021). Canonical modern guide to product discovery techniques for cross-functional product teams.
- **The Lean Startup** — Eric Ries (2011). Foundational text on build-measure-learn and validated learning for product development.
- **The Mom Test** — Rob Fitzpatrick (2013). Standard practical reference on running customer discovery conversations that surface truth instead of false validation.
- **Shape Up: Stop Running in Circles and Ship Work that Matters** — Ryan Singer (2019). Free, widely adopted framework for shaping and scoping product work in fixed cycles. <https://basecamp.com/shapeup>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Ops, platform, quality & product — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Quality, product, delivery & leadership — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 14 · Quality, product, delivery & leadership.

> _Content originated in the now-closed FS-SE plan (topic 32); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
