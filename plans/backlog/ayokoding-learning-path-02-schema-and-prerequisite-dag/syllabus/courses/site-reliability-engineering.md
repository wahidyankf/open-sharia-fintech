# Site Reliability Engineering (Annotated-concept, Python)

**Course ID**: `site-reliability-engineering` · **Format**: Annotated-concept · **Language**: Python.

**Short summary**: SLOs, observability, incident response

**Scope note**: `*` concept-centric (Python where code appears) — operating software reliably at scale:
SLIs/SLOs/error budgets, the four golden signals, observability (metrics/logs/traces), alerting on symptoms
not causes, incident response & blameless postmortems, toil reduction, and capacity/load. The **journey
closer** — this final topic anchors the whole-journey `capstone-lead-at-altitude` (the Pass-4 concurrency
capstones now anchor at [`89-compilers-parsers-and-transpilers`](./compilers-parsers-and-transpilers.md),
the Pass-4 closer). Builds on the ops/observability threads
([`15-software-testing`](./software-testing.md),
[`50-containers-and-orchestration`](./containers-and-orchestration.md)).

## Why this exists · the big idea

- **The problem before the solution**: every service fails eventually, and chasing 100% uptime is both
  impossible and ruinously expensive. Without a principled target, teams either over-invest in reliability
  nobody needs or get blindsided by the outage that actually matters.
- **Keep-this-if-you-forget-everything**: reliability is a feature you _budget_, not a binary you promise —
  measure user-facing symptoms (SLIs), set an SLO, spend the error budget on velocity, alert on symptoms,
  and learn blamelessly.
- **Big ideas touched**: `consistency-latency-throughput` — the golden signals and error budget are where
  the distributed-systems trilemma becomes an operational dial; `determinism-vs-emergence` — a system at
  scale behaves in ways no one designed, so you observe and respond to emergent behaviour rather than
  predict it; `correctness-vs-pragmatism` — 100% is the wrong target, and the error budget makes "reliable
  enough" a disciplined, negotiated compromise.

## Prerequisites

- **Prior topics**: [topic 39 Backend at Scale](./backend-at-scale.md) (the services being operated),
  [topic 50 Containers & Orchestration](./containers-and-orchestration.md) (where they run), and
  [topic 44 System Design](./system-design.md) (load, capacity, failure modes).
- **Tools & environment**: **Python 3.x** for the runnable mechanisms; a local metrics stack
  (Prometheus-style scrape + a dashboard) runnable via containers (DD-20); Neovim/VSCode (DD-17).
- **Assumed knowledge**: running a backend service (topic 39); containers/orchestration basics (topic 50);
  reasoning about load + failure (topic 44).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified (exact match to Google SRE canon): SLIs/SLOs/error budgets (budget = 100% − SLO),
  the four golden signals (latency, traffic, errors, saturation), symptom-based alerting, blameless
  postmortems + incident command, and toil reduction / capacity planning are unchanged. (sre.google/sre-book)
- 2026-07-12 — verified: **Prometheus = Apache-2.0**, CNCF-graduated, de-facto metrics standard;
  **OpenTelemetry** is the current CNCF-graduated instrumentation standard for metrics/tracing. No drift.
  (github.com/prometheus/prometheus/blob/main/LICENSE)

### DD-35 primary-source citations (fetched-and-read)

Every definition, formula, and named tool below traces to a primary source fetched and read during
grounding. Unverifiable specifics are marked `[Needs Verification]` and never shipped as fact.

- **SLI/SLO/error budget** — an SLI is a ratio of good events to total; an SLO is a target for it; the
  **error budget = 100% − SLO**. Verified against the Google SRE book chs. 3–4 and _Implementing Service
  Level Objectives_ (Hidalgo, 2020). (sre.google/sre-book/service-level-objectives)
- **The four golden signals** — **latency, traffic, errors, saturation** — are from the SRE book ch. 6
  "Monitoring Distributed Systems". (sre.google/sre-book/monitoring-distributed-systems)
- **Symptom-based alerting** and **multi-window, multi-burn-rate SLO alerts** are from the SRE Workbook ch. 5
  "Alerting on SLOs". (sre.google/workbook/alerting-on-slos)
- **Toil** — manual, repetitive, automatable, tactical work with no enduring value; the SRE book recommends
  capping toil at **~50%** of an SRE's time (ch. 5). (sre.google/sre-book/eliminating-toil)
- **Blameless postmortems** + incident command are from the SRE book chs. 14–15; SRE was coined by
  **Ben Treynor** at Google (~2003). (sre.google/sre-book/postmortem-culture)
- **Prometheus** is **Apache-2.0**, CNCF-**graduated**, pull/scrape-based (counters, gauges, histograms);
  **OpenTelemetry** is CNCF-**graduated**, vendor-neutral instrumentation (metrics/traces/logs) via an SDK +
  collector. (prometheus.io, opentelemetry.io, cncf.io/projects)
- **Nines** — 99.9% ≈ 43.8 min/month of allowed downtime; 99.99% ≈ 4.38 min/month. (sre.google/sre-book/availability-table)
- **Implementation** — Python for the runnable mechanisms + a local Prometheus-style stack; `*` concept-centric
  (code where it clarifies).

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (annotated-concept). Each example below cites the co-NN it exercises. -->

- **co-01 · reliability-as-feature** — reliability is budgeted and negotiated, never promised as 100%.
- **co-02 · sli** — a service level indicator measures a user-facing quality (good events / total).
- **co-03 · slo** — a service level objective is the target value for an SLI.
- **co-04 · sla** — a service level agreement adds external consequences to an objective.
- **co-05 · error-budget** — the allowed unreliability: `budget = 100% − SLO`.
- **co-06 · budget-velocity-tradeoff** — the error budget is spent on shipping velocity, then defends reliability.
- **co-07 · nines** — availability "nines" map to concrete allowed downtime per month.
- **co-08 · golden-signal-latency** — request latency, one of the four golden signals.
- **co-09 · golden-signal-traffic** — demand/traffic, a golden signal.
- **co-10 · golden-signal-errors** — error rate, a golden signal.
- **co-11 · golden-signal-saturation** — resource saturation/utilization, a golden signal.
- **co-12 · metrics** — numeric time series (counters, gauges, histograms).
- **co-13 · logs** — structured, queryable event records.
- **co-14 · traces** — distributed traces of a request across services (spans).
- **co-15 · observability** — metrics, logs, and traces together let you ask new questions of a system.
- **co-16 · instrumentation** — adding measurement points to code.
- **co-17 · opentelemetry** — OTel's vendor-neutral SDK + collector for metrics/traces/logs.
- **co-18 · prometheus-scrape** — Prometheus pull-scrapes a `/metrics` endpoint.
- **co-19 · dashboard** — visualizing signals and SLO/budget state.
- **co-20 · symptom-based-alerting** — page on user-facing symptoms, not internal causes.
- **co-21 · slo-burn-alert** — a multi-window burn-rate alert on error-budget consumption.
- **co-22 · alert-fatigue** — page-storms desensitize on-call and hide real incidents.
- **co-23 · on-call** — the on-call rotation and the page-vs-ticket judgment.
- **co-24 · incident-severity** — classifying an incident by impact severity.
- **co-25 · incident-command** — the incident-command roles (commander, comms, ops).
- **co-26 · blameless-postmortem** — a systemic, blame-free write-up of an incident.
- **co-27 · action-items** — concrete, owned follow-ups from a postmortem.
- **co-28 · toil** — manual, repetitive, automatable operational work (cap ~50%).
- **co-29 · toil-automation** — eliminating toil with automation that is itself maintained.
- **co-30 · capacity-planning** — planning capacity against load and growth.

## Tensions & trade-offs — when NOT to reach for this

- **Reliability vs velocity**: every extra nine of uptime costs exponentially more and slows shipping. The
  error budget exists precisely so the trade is explicit and owned, not re-argued case by case.
- **Symptom vs cause alerting**: alert on causes and you drown in noise for failures users never felt;
  alert only on symptoms and a slow-burning root cause can hide. Symptom/SLO-burn alerts that page, plus
  diagnostic signals that don't, split the difference.
- **Coverage vs alert fatigue**: more alerts feel safer, but page-storms desensitize on-call and the real
  incident gets missed. Fewer, symptom-based, budget-burn alerts beat exhaustive cause alerts.
- **Automating toil vs its cost**: automation frees humans, but every automation is itself a system to
  maintain that can fail worse than the manual step. Automate the repetitive and reversible first.

## Lineage — why it beat the alternative

- SRE emerged at Google (Ben Treynor, ~2003) as the answer to a structural conflict: developers want to
  ship, a separate ops team wants to freeze, and the split produces either fragile speed or safe
  stagnation. SRE dissolved the conflict by making reliability a measurable, budgeted engineering concern
  owned jointly — SLOs quantify "reliable enough," the error budget turns the dev-vs-ops fight into a
  shared number, and blameless postmortems (borrowed from aviation and medicine safety culture) replaced
  blame with systemic learning. It beat both the throw-it-over-the-wall model and the "just add more nines"
  instinct because it made the trade-off explicit rather than political. As the journey's closer it gathers
  the program's operational threads — [`15-software-testing`](./software-testing.md),
  [`50-containers-and-orchestration`](./containers-and-orchestration.md),
  [`39-backend-at-scale`](./backend-at-scale.md), [`44-system-design`](./system-design.md) — into the
  altitude question every senior engineer eventually owns: not "does it work?" but "how reliable does it
  need to be, and what will we trade for that?" — which is why it anchors `capstone-lead-at-altitude`.

## Worked examples

Colocated under `site-reliability-engineering/learning/code/`; Python + a local metrics stack (DD-20/DD-30).
Contiguous `ex-01..ex-52`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · instrument-latency** — measure per-request latency — verify a latency metric is recorded. (co-08, co-16)
- **ex-02 · instrument-traffic** — count requests per second — verify a traffic counter increments. (co-09, co-16)
- **ex-03 · instrument-errors** — count error responses — verify the error metric rises on a 5xx. (co-10, co-16)
- **ex-04 · instrument-saturation** — measure resource utilization — verify a saturation gauge reflects load. (co-11, co-16)
- **ex-05 · metrics-endpoint** — expose a `/metrics` endpoint — verify it serves the metrics. (co-12, co-18)
- **ex-06 · prometheus-scrape** — scrape the endpoint with Prometheus — verify metrics ingest. (co-18)
- **ex-07 · counter-metric** — a Prometheus counter — verify it only increases. (co-12)
- **ex-08 · gauge-metric** — a gauge — verify it rises and falls. (co-12)
- **ex-09 · histogram-latency** — a latency histogram — verify buckets populate and p99 is derivable. (co-08, co-12)
- **ex-10 · structured-log** — emit a structured (JSON) log line — verify the fields parse. (co-13)
- **ex-11 · log-correlation-id** — attach a request id to logs — verify logs correlate by id. (co-13)
- **ex-12 · trace-span** — create a single span — verify its start/end and duration. (co-14)
- **ex-13 · trace-propagation** — propagate trace context across a call — verify one trace spans both services. (co-14)
- **ex-14 · otel-sdk-setup** — configure the OpenTelemetry SDK — verify it emits telemetry. (co-17)
- **ex-15 · otel-collector** — export through an OTel collector — verify the collector receives it. (co-17)
- **ex-16 · three-pillars** — one request producing a metric, a log, and a trace — verify all three link up. (co-15)
- **ex-17 · nines-table** — compute allowed downtime for 99.9%/99.99% — verify 43.8 min vs 4.38 min per month. (co-07)
- **ex-18 · availability-calc** — compute availability from good/total requests — verify the ratio. (co-07, co-10)

### Intermediate

- **ex-19 · define-sli** — define an SLI as good events / total — verify the computed ratio. (co-02)
- **ex-20 · sli-availability** — an availability SLI — verify it drops when errors rise. (co-02, co-10)
- **ex-21 · sli-latency** — a latency SLI (fraction of requests under a threshold) — verify it reflects slow requests. (co-02, co-08)
- **ex-22 · define-slo** — set a 99.9% SLO — verify the target is encoded. (co-03)
- **ex-23 · error-budget-calc** — `budget = 100% − SLO` — verify a 99.9% SLO yields a 0.1% budget. (co-05)
- **ex-24 · budget-consumed** — track budget consumption over a window — verify it decrements with errors. (co-05)
- **ex-25 · budget-velocity** — freeze risky changes when the budget is exhausted — verify the gate trips. (co-06)
- **ex-26 · sla-vs-slo** — contrast an SLA (external consequence) with an SLO (internal target) — verify the distinction is documented. (co-04, co-03)
- **ex-27 · burn-rate** — compute the error-budget burn rate — verify a spike raises it. (co-21)
- **ex-28 · multiwindow-burn-alert** — a multi-window multi-burn-rate alert — verify a fast burn pages, a slow burn tickets. (co-21)
- **ex-29 · symptom-alert-rule** — an alert on a user-facing symptom — verify it fires on symptom, not on internals. (co-20)
- **ex-30 · cause-alert-antipattern** — show a CPU-only alert firing with no user impact — verify why it is noise. (co-20)
- **ex-31 · page-vs-ticket** — route urgent to a page, diagnostic to a ticket — verify the routing. (co-20, co-23)
- **ex-32 · alert-fatigue-prune** — remove a chronically noisy alert — verify page volume drops. (co-22)
- **ex-33 · slo-based-page** — an SLO-burn page fires on injected errors — verify it pages. (co-21, co-20)
- **ex-34 · quiet-under-normal** — normal load — verify no alert fires. (co-20)
- **ex-35 · alert-runbook-link** — an alert linking a runbook — verify the link resolves to steps. (co-23)
- **ex-36 · budget-policy** — an error-budget policy document — verify it states the freeze rule. (co-06, co-05)

### Advanced

- **ex-37 · golden-signals-dashboard** — a dashboard of all four golden signals — verify each panel renders live data. (co-19)
- **ex-38 · dashboard-slo-panel** — an SLO/error-budget panel — verify it shows remaining budget. (co-19, co-05)
- **ex-39 · seeded-incident** — inject a seeded incident (error spike) — verify the signals move. (co-24)
- **ex-40 · incident-detection** — the alert detects the seeded incident — verify it fires promptly. (co-20, co-24)
- **ex-41 · incident-severity-classify** — assign a severity to the incident — verify the classification rubric. (co-24)
- **ex-42 · incident-command-roles** — name incident-command roles — verify commander/comms/ops are assigned. (co-25)
- **ex-43 · incident-timeline** — build the incident timeline — verify events are ordered with timestamps. (co-26)
- **ex-44 · blameless-postmortem** — write a blameless postmortem — verify it explains the system, not a person. (co-26)
- **ex-45 · postmortem-action-items** — extract owned action items — verify each has an owner. (co-27)
- **ex-46 · postmortem-no-blame** — review postmortem language — verify no individual is blamed. (co-26)
- **ex-47 · identify-toil** — flag a repetitive manual task as toil — verify it meets the toil criteria. (co-28)
- **ex-48 · toil-budget** — cap toil at a percentage of time — verify the cap is tracked. (co-28)
- **ex-49 · automate-toil** — script away an identified toil task — verify the manual step is eliminated. (co-29)
- **ex-50 · automation-failure-mode** — reason about the automation's own failure mode — verify a guard/rollback exists. (co-29)
- **ex-51 · capacity-load-test** — load-test to a capacity limit — verify saturation is observed at the ceiling. (co-30)
- **ex-52 · capstone-sre-loop** — the capstone: observe → alert → incident → postmortem on one service — verify the full loop runs end-to-end. (co-05, co-11, co-20, co-26)

## Capstone spec — intra-topic (subject → runnable mechanisms + reliability artifact)

- **Goal**: make a small service **observable and operable** — instrument the four golden signals, define an
  SLI/SLO with an error budget in code, wire a symptom-based alert and a dashboard, then run a seeded
  incident and produce a blameless postmortem with action items — the full SRE loop from measurement to
  learning.
- **Concepts exercised**: [ ] four-golden-signals instrumentation + a metrics endpoint (co-08, co-09, co-10,
  co-11, co-16, co-18) [ ] an SLI + SLO + error budget defined in code (co-02, co-03, co-05) [ ] a
  symptom-based (not cause-based) alert rule (co-20, co-21) [ ] a golden-signals dashboard (co-19) [ ] a
  seeded incident + a blameless postmortem with action items (co-24, co-26, co-27).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — instrument a small service with latency/traffic/errors/saturation +
     a metrics endpoint. Verify the endpoint exposes all four signals under load.
  2. Define an SLI + SLO + error budget in code and a symptom-based alert rule. Verify the alert fires when
     the SLO is violated (drive it with injected errors/latency) and stays quiet otherwise.
  3. Add a dashboard; run a seeded incident and write `postmortem.md` (blameless, with timeline + action
     items). Verify the dashboard reflects the incident and the postmortem is symptom-focused and blameless.
- **Acceptance criteria**: all four golden signals are instrumented; the SLO + error budget are defined in
  code; the alert is symptom-based and fires correctly; the dashboard reflects reality; the postmortem is
  blameless with concrete action items.
- **Done bar**: runnable end-to-end + reliability artifact + web-verified.

<!-- Inter-topic capstone spec block: this file (the journey's final topic) anchors the whole-journey capstone -->

## Capstone spec — inter-topic: capstone-lead-at-altitude (whole-journey)

> **Weight**: `capstone-lead-at-altitude/_index.md` = **1045** (section root, after the journey's final
> topic 94). Kind: **whole-journey synthesis → leadership/decision artifact + a shipped system**. The
> capstone of the entire program — it looks back across all 94 topics.

- **Goal**: act as the **technical lead of the whole journey** — take one of the earlier runnable systems (the
  `capstone-concurrency-and-systems` service from [`89-compilers-parsers-and-transpilers`](./compilers-parsers-and-transpilers.md)
  or the `capstone-real-world-delivery` app) and **operate it at altitude**: define its SLOs and reliability
  posture (topic 94), author a technical strategy + prioritization record that a team could execute (topics
  32/33), and produce a whole-journey **retrospective** that names, per pass, what the relearn-and-drill habit
  changed — closing the program by turning the individual learning loop into an organizational one.
- **Concepts integrated**: [ ] SLIs/SLOs/error budgets + a golden-signals dashboard on a real service (94)
  [ ] a one-page technical strategy tying team → product outcomes (32/33) [ ] a prioritization/trade-off
  decision record for the service's roadmap (33) [ ] a growth-plan + leading-through-influence frame (33)
  [ ] a whole-journey retrospective mapping each pass (P0–P5) to a concrete capability gained.
- **Ordered steps**:
  1. `capstone-lead-at-altitude/code/` — take an earlier capstone service, define its SLI/SLO/error budget,
     and stand up a golden-signals dashboard + a symptom-based alert (94). Verify the SLO alert fires on an
     injected violation and the dashboard reflects load.
  2. `strategy.md` + `prioritization.md` — a one-page technical strategy linking the service's reliability
     work to product outcomes, and a prioritization record for its roadmap under an error-budget constraint
     (32/33). Verify every bet traces to an outcome and each priority states its trade-off.
  3. `retrospective.md` — a whole-journey retrospective: for each pass (P0 Editor Foundations → P5 Internals &
     Lead at Altitude) name one capability the relearn-and-drill habit produced, and the organizational
     practice that would sustain it. Verify every pass is covered and each entry is concrete, not generic.
- **Acceptance criteria**: the chosen service is genuinely operable (SLO + alert + dashboard work); the
  strategy and prioritization artifacts are executable and trade-off-explicit; the retrospective covers all
  six passes with concrete, evidence-backed capabilities; the set reads as a lead's altitude view of the
  whole journey.
- **Done bar**: the service is runnable + observable, the leadership artifacts are internally coherent, the
  whole-journey retrospective is complete + web-verified.

## Read more

**Books**

- **Site Reliability Engineering: How Google Runs Production Systems** — Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (eds.) (2016). The book that defined SRE as a discipline; free online from Google. <https://sre.google/sre-book/table-of-contents/>
- **The Site Reliability Workbook** — Betsy Beyer, Niall Richard Murphy, David K. Rensin, Kent Kawahara, Stephen Thorne (eds.) (2018). The hands-on companion applying SRE principles (SLOs, error budgets, incident response) in practice; free online. <https://sre.google/workbook/table-of-contents/>
- **Seeking SRE** — David N. Blank-Edelman (ed.) (2018). Widely cited collection of essays showing how SRE principles are adapted across diverse organizations.
- **Implementing Service Level Objectives** — Alex Hidalgo (2020). The definitive practical guide to SLIs, SLOs, and error budgets, the core measurement toolkit of SRE.

## In which paths

- `interview-ready/software-engineer` — Go deeper · Ops, platform, quality & product — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Scale, cloud & platform ops — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 10 · Scale, cloud & platform ops.

> _Content originated in the now-closed FS-SE plan (topic 94); it now lives here in
> full — this course block is self-contained._

## In which paths — `capstone-lead-at-altitude` (DD-20)

This whole-journey capstone needs `software-product-engineering` and `engineering-management` — both
later than this course within the final "quality/product/leadership" section of every manifest — so it
closes that section, right after `project-management`, as the very last item before each manifest's
optional interview tail:

- `interview-ready/software-engineer` — Go deeper · Ops, platform, quality & product, right after `project-management` (the final item in the manifest).
- `immediately-effective/software-engineer` — Deepening band · Quality, product, delivery & leadership, right after `project-management` (right before the optional interview tail).
- `fundamentally-strong/software-engineer` — Stage 14 · Quality, product, delivery & leadership, right after `project-management` (right before the optional interview tail).

See [DD-20](../../tech-docs.md#design-decisions) for the full reconciliation ruling.

---

← Back to the [course library catalog](./README.md)
