# Product Patterns for Probabilistic Systems (Annotated-concept, no code)

**Course ID**: `product-patterns-for-probabilistic-systems` · **Format**: Annotated-concept ·
**Language**: — (concept, no code). **NEW** — no course in the library owns this material today.

**Scope note**: designing the **product** around a component that is sometimes wrong — the interaction
patterns, expectation-setting, and release discipline that make a non-deterministic feature usable and
recoverable. Covers **surfacing uncertainty** without either hiding it or drowning the user in it,
**confidence and provenance** as interface elements, **human-in-the-loop** designs where review is the
product rather than a fallback, **graceful degradation** when the model is unavailable, slow, or
plainly wrong, **error recovery and undo** sized to the action's blast radius, and **ship / hold /
rollback criteria** for features whose quality is a distribution rather than a boolean. Written in the
Annotated-concept **no-code register**: worked scenarios, interface walkthroughs, and WCAG-accessible
Mermaid diagrams, no code blocks. Pairs with
[`evaluating-ai-output-essentials`](./evaluating-ai-output-essentials.md) and
[`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md), which supply the measurements
this course turns into product decisions.

> **Scope guard — product patterns vs the human-in-the-loop guardrail.**
> [`agent-permissions-and-sandboxing`](./agent-permissions-and-sandboxing.md) owns human-in-the-loop as a
> **safety control**: deny/ask/allow enforced by the harness so an agent cannot take a dangerous action.
> This course owns human-in-the-loop as a **product design**: what the reviewer sees, how much cognitive
> load the review imposes, whether the interface earns calibrated trust, and what happens when the
> reviewer disengages. The safety course answers "can this action proceed"; this course answers "is a
> human meaningfully in a position to judge". Both are needed and neither substitutes for the other.

## Why this exists · the big idea

- **The problem before the solution**: every pattern in a product designer's vocabulary assumes the
  system either succeeds or fails, and says so. A probabilistic feature breaks that assumption — it
  succeeds partially, fails silently, fails confidently, and fails differently for the same input twice.
  Teams ship these features inside interfaces designed for deterministic software, and users learn
  either to distrust everything the feature produces or, far worse, to trust all of it uniformly. Both
  outcomes are design failures, not model failures.
- **Keep-this-if-you-forget-everything**: design for the wrong answer, because it is coming — make it
  visible, make it cheap to catch, and make it cheap to undo.
- **Big ideas touched**: `determinism-vs-emergence` (the interface is where a stochastic component meets
  a human who expects determinism), `correctness-vs-pragmatism` (the product goal is a recoverable
  workflow, not a correct one), `abstraction-and-its-cost` (every confidence indicator is a lossy
  summary of a distribution, and users read it as a promise).

## Prerequisites

- **Prior topics**: [`creating-ai-powered-apps`](./creating-ai-powered-apps.md) (what the model can and
  cannot be asked for), [`evaluating-ai-output-essentials`](./evaluating-ai-output-essentials.md) (you
  cannot set a ship criterion without a measurement),
  [`software-product-engineering`](./software-product-engineering.md) (product framing, scoping, release
  practice), [`frontend-essentials`](./frontend-essentials.md) (interface vocabulary and accessibility
  baseline).
- **Tools & environment**: no runtime and no code. A diagramming surface for the Mermaid flows, a
  whiteboard or document for the interface walkthroughs, and access to one real probabilistic feature —
  the learner's own or a public one — to critique. Written artefacts are the deliverable throughout.
- **Assumed knowledge**: what an LLM feature does and roughly how it fails; the ability to read an eval
  report and interpret a pass rate with an interval; basic interface and accessibility vocabulary.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-20 — **durable spine**: designing for partial correctness, calibrating user trust to actual
  reliability, provenance as an interface element, degradation paths, undo sized to blast radius, and
  release criteria expressed as distributions rather than booleans are design principles. They are
  independent of model, vendor, and framework, and they predate LLMs in aviation automation, medical
  decision support, spam filtering, and autocomplete.
- 2026-07-20 — `[Needs Verification]` **volatile, accuracy-note only**: every named product used as an
  illustration — which assistant surfaces confidence how, which tool shows citations, which one offers a
  diff-before-apply — will have changed by the time the course is read. Use current products only as
  dated screenshots or dated descriptions in an accuracy-note sidebar, and keep every spine claim
  expressed as a pattern rather than as "product X does this".
- 2026-07-20 — `[Needs Verification]` **at authoring**: the automation-trust literature this course draws
  on (automation bias, complacency, trust calibration, the vigilance decrement) is established
  human-factors research, but the specific studies and their findings must be verified against primary
  sources before citation. Teach the phenomena — which are robust — and cite only what is read.
- 2026-07-20 — **contested, teach as contested**: whether to display a numeric confidence score to end
  users is genuinely disputed. Numeric scores are precise and routinely misread as probabilities of
  correctness when they are not; qualitative bands are read more accurately but discard information.
  Present the trade-off and the conditions favouring each, and do not resolve it.
- 2026-07-20 — no model IDs, prices, or SDK shapes appear in this course's spine by design.

## Concepts

<!-- co-NN · concept enumeration. Floor ≥ 8 (Annotated-concept, no-code register). Each scenario below cites the co-NN it exercises. -->

1. **co-01 · the-deterministic-interface-assumption** — standard product patterns encode a
   success-or-error model that a probabilistic feature violates, which is why they mislead when reused
   unchanged.
2. **co-02 · failure-modes-users-experience** — confidently wrong, subtly wrong, refused, truncated,
   slow, and inconsistent-across-identical-requests are distinct user experiences requiring distinct
   designs.
3. **co-03 · setting-expectations-before-first-use** — what the feature is told to be on first contact
   determines how its errors are interpreted for the rest of the relationship.
4. **co-04 · trust-calibration** — the goal is user trust proportional to actual reliability; both
   over-trust and blanket distrust are failures, and both are caused by the interface.
5. **co-05 · automation-bias-and-complacency** — users under-scrutinize output from a system that is
   usually right, and the better the system gets, the worse the scrutiny becomes.
6. **co-06 · surfacing-uncertainty** — communicating that an output may be wrong, at the moment and place
   the user could act on it.
7. **co-07 · confidence-representation-tradeoffs** — numeric scores, qualitative bands, hedged language,
   and visual treatments each trade precision against being read correctly.
8. **co-08 · confidence-is-not-correctness** — a model's expressed or computed confidence is not a
   probability of being right, and presenting it as one manufactures unearned trust.
9. **co-09 · provenance-and-citation** — showing where an answer came from lets a user verify it
   themselves, which is often more useful than any confidence signal.
10. **co-10 · verifiability-by-design** — structuring output so checking it is cheaper than producing it
    is the single strongest lever on a probabilistic feature's usability.
11. **co-11 · human-in-the-loop-as-product** — designs where human review is the intended workflow rather
    than an admission of failure, and how to make review fast enough to survive contact with volume.
12. **co-12 · review-cost-and-the-vigilance-decrement** — a reviewer's accuracy decays with volume and
    with the system's reliability; a review step that ignores this is theatre.
13. **co-13 · consequence-scaled-friction** — the amount of confirmation, preview, and delay a design
    imposes should scale with the action's reversibility and blast radius, not be uniform.
14. **co-14 · preview-and-diff-before-apply** — showing exactly what will change before it changes
    converts an irreversible action into a reviewable one.
15. **co-15 · undo-and-recovery** — cheap, obvious, complete reversal is worth more than a marginal
    accuracy improvement, and is usually cheaper to build.
16. **co-16 · graceful-degradation** — defining what the product does when the model is unavailable,
    rate-limited, too slow, or returns something unusable — including doing nothing visibly rather than
    failing invisibly.
17. **co-17 · latency-as-a-design-material** — streaming, progressive disclosure, optimistic states, and
    honest waiting all change what a slow probabilistic response feels like.
18. **co-18 · fallback-hierarchies** — a designed ladder from best-effort model output to a cheaper
    model, to a deterministic heuristic, to an honest unavailable state.
19. **co-19 · silent-failure-is-the-worst-failure** — a wrong answer presented identically to a right one
    is more damaging than a visible error, and most probabilistic features default to it.
20. **co-20 · scoping-to-what-the-model-can-do** — the highest-leverage product decision is usually
    narrowing the feature until its failure rate is tolerable, not improving the model.
21. **co-21 · ship-criteria-for-a-distribution** — a launch decision on a probabilistic feature is a
    threshold on a measured distribution with an interval, plus a named worst case that is acceptable.
22. **co-22 · staged-rollout-and-guardrail-metrics** — exposure is ramped while pre-agreed guardrail
    metrics are watched, because eval sets do not contain the traffic that will break it.
23. **co-23 · rollback-criteria-agreed-in-advance** — the conditions for turning the feature off are
    written down before launch, because they cannot be negotiated honestly during an incident.
24. **co-24 · feedback-capture-as-a-product-surface** — the correction affordance is both a user
    recovery path and the pipeline that feeds the next error-analysis pass.

## Tensions & trade-offs — when NOT to reach for this

- **Surfacing uncertainty vs usability**: caveats on every output train users to ignore caveats, and an
  interface that hedges constantly is exhausting and reads as a product that does not believe in itself.
  Uncertainty signals must be selective enough to carry information — which means deciding, deliberately,
  which outputs get them.
- **Human review vs the value proposition**: a feature whose output must be fully checked has saved the
  user nothing except typing. If review costs as much as doing the work, the honest conclusion is that
  the feature should be narrowed (co-20) or not shipped — not that the review step should be quietly
  weakened.
- **Friction vs flow**: consequence-scaled friction is correct in principle and painful in practice —
  every confirmation is a chance for the user to disengage, and uniform friction trains people to click
  through it. Reserve real friction for genuinely irreversible actions, and pay for the rest with undo.
- **Confidence display vs misreading**: showing a confidence number invites users to treat it as a
  probability of correctness, which it is not (co-08). Showing nothing invites uniform trust. There is no
  free option here, only a choice made deliberately and validated with real users.
- **When NOT to reach for this course**: if the feature's output is fully verified downstream by a
  deterministic check before any human sees it — a generated query that is validated and executed, a
  classification confirmed against a schema — the user is not exposed to the distribution and these
  patterns add ceremony. This material is for output that reaches a human unverified.
- **When NOT to ship the feature at all**: if no scoping narrows the failure rate to something the
  workflow can absorb, and no undo makes the failures cheap, the correct product decision is not to
  ship. Recognising that case is part of this course, not an admission that it failed.

## Lineage — why it beat the alternative

- The pattern that lost was treating a probabilistic feature as an ordinary one and letting the model's
  output flow into an interface built for deterministic results — a text box that returns an answer, a
  button that performs an action, an error state for the rare failure. It lost because the failure it
  designed for is not the failure that occurs: the dominant failure of a probabilistic system is not an
  error message, it is a plausible wrong answer rendered identically to a right one (co-19), and no
  amount of model improvement removes it. The disciplines that replaced it were not invented for LLMs.
  Aviation automation established decades ago that operators under-scrutinize systems that are usually
  right, and that the effect intensifies as reliability improves — which is why automation bias is a
  design constraint rather than a training problem. Spam filtering established that a
  false-positive-tolerant workflow with a cheap recovery path beats a more accurate classifier with no
  recovery path. Autocomplete established that a suggestion the user can ignore at zero cost can be
  wrong most of the time and still be valuable, because the interaction is designed around rejection.
  Each of those is the same move: accept the distribution, design the recovery, and scope the feature
  until its failure rate fits the workflow. This course collects those moves for a component whose error
  rate is higher and whose errors are more fluent than anything the earlier examples faced, and it
  depends on [`evaluating-ai-output-essentials`](./evaluating-ai-output-essentials.md) and
  [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md) for the measurements that turn
  "it seems good" into a defensible ship criterion.

## Worked examples

No fixed difficulty bands (Annotated-concept, no-code register); grouped by theme. Each entry is a
**worked scenario**: a concrete product situation, the design move, and the check that verifies the move
worked. Deliverables are written artefacts — interface walkthroughs, annotated wireframe descriptions,
decision tables, written criteria, and WCAG-accessible Mermaid diagrams. **No code blocks appear in this
course.** Colocated under `product-patterns-for-probabilistic-systems/learning/artifacts/`. Contiguous
`ex-01..ex-44`. Every scenario cites the `co-NN` it exercises.

### Theme A · The wrong answer is coming (ex 01–11)

1. **ex-01 · the-deterministic-interface-fails** — walk a probabilistic feature through an interface
   designed for success-or-error — verify the confidently-wrong case has no state to land in. (co-01)
2. **ex-02 · catalogue-the-user-visible-failures** — enumerate the six failure modes for one real feature
   with a user-observable description of each — verify each is distinguishable from the others. (co-02)
3. **ex-03 · silent-failure-walkthrough** — trace a plausible wrong answer through the current interface
   to the user's decision — verify nothing in the path would have caught it. (co-19, co-02)
4. **ex-04 · first-run-expectation-setting** — draft first-contact copy that frames the feature's
   reliability honestly — verify it survives the user's first wrong answer. (co-03)
5. **ex-05 · overpromise-postmortem** — critique marketing copy that promises determinism — verify the
   specific trust damage its first failure causes. (co-03, co-04)
6. **ex-06 · trust-calibration-diagram** — a Mermaid diagram mapping actual reliability against user
   trust, with the over-trust and distrust quadrants named — verify both failure quadrants. (co-04)
7. **ex-07 · automation-bias-in-a-review-flow** — walk a reviewer through fifty mostly-correct items —
   verify the point at which scrutiny predictably collapses. (co-05, co-12)
8. **ex-08 · reliability-makes-scrutiny-worse** — annotate why improving the model degrades review
   quality — verify the counterintuitive direction. (co-05)
9. **ex-09 · blanket-distrust-case** — a feature users stopped using after two bad answers — verify the
   interface never gave them a way to tell good from bad. (co-04, co-06)
10. **ex-10 · narrow-the-feature-instead** — redesign an unreliable broad feature into a narrow reliable
    one — verify the failure rate the workflow now absorbs. (co-20)
11. **ex-11 · decide-not-to-ship** — a feature with no viable scoping and no cheap undo — verify the
    written rationale for not shipping. (co-20, co-15)

### Theme B · Uncertainty, confidence, and provenance (ex 12–22)

1. **ex-12 · where-uncertainty-belongs** — place the uncertainty signal at the decision point rather than
   in a footer — verify the user encounters it while it is actionable. (co-06)
2. **ex-13 · four-confidence-representations** — the same output shown with a numeric score, a
   qualitative band, hedged language, and a visual treatment — verify what each communicates and misses.
   (co-07)
3. **ex-14 · confidence-is-not-correctness** — a walkthrough where a high-confidence output is wrong —
   verify why presenting confidence as probability-of-correct was the design error. (co-08)
4. **ex-15 · numeric-vs-band-user-reading** — a comparison of how users interpret "0.82" against "likely"
   — verify the contested trade-off is presented without being resolved. (co-07, co-08)
5. **ex-16 · caveat-fatigue** — an interface that hedges every output — verify users stop reading the
   hedges. (co-06)
6. **ex-17 · selective-uncertainty-policy** — a written rule for which outputs carry a signal and which do
   not — verify the rule is applicable without case-by-case judgment. (co-06, co-07)
7. **ex-18 · citation-as-the-better-signal** — replace a confidence score with a source citation — verify
   the user can now check the claim rather than estimate it. (co-09)
8. **ex-19 · provenance-that-does-not-help** — a citation the user cannot practically follow — verify why
   it produces the appearance of verifiability without the substance. (co-09, co-10)
9. **ex-20 · design-for-cheap-verification** — restructure an output so checking it costs far less than
   producing it — verify the cost asymmetry. (co-10)
10. **ex-21 · verifiability-diagram** — a Mermaid diagram of output structures ranked by verification
    cost — verify each rung. (co-10, co-09)
11. **ex-22 · accessible-uncertainty** — express an uncertainty signal without relying on colour alone,
    meeting WCAG AA — verify screen-reader and colour-blind readings both carry the signal. (co-06,
    co-07)

### Theme C · Humans in the loop, friction, and recovery (ex 23–33)

1. **ex-23 · review-as-the-product** — a workflow where the model drafts and the human decides, designed
   as the intended path — verify the review is faster than doing the work. (co-11)
2. **ex-24 · review-that-costs-more-than-doing** — a review step that destroys the value proposition —
   verify the measurement and the redesign. (co-11, co-12)
3. **ex-25 · vigilance-decrement-mitigation** — batch sizes, sampling, and forced-attention designs that
   slow reviewer decay — verify each mitigation's cost. (co-12, co-05)
4. **ex-26 · review-theatre** — an approval gate nobody meaningfully reads — verify it provides no safety
   and delays the workflow. (co-12, co-11)
5. **ex-27 · consequence-scaled-friction-table** — a decision table mapping reversibility and blast radius
   to the required confirmation — verify every action in one real product lands in a cell. (co-13)
6. **ex-28 · uniform-friction-fails** — an interface confirming everything — verify users click through
   the confirmations that mattered. (co-13)
7. **ex-29 · preview-and-diff** — show the exact change before applying it — verify the user catches a
   wrong edit they would otherwise have accepted. (co-14)
8. **ex-30 · undo-beats-accuracy** — compare investment in a marginal accuracy gain against investment in
   complete undo — verify which produces the better workflow. (co-15)
9. **ex-31 · partial-undo-is-a-trap** — an undo that reverses some effects — verify the user's incorrect
   mental model and its consequence. (co-15)
10. **ex-32 · correction-affordance** — an in-context way for the user to fix a wrong output — verify it
    recovers the user and produces a labeled failure case. (co-24, co-15)
11. **ex-33 · feedback-into-error-analysis** — route captured corrections into the next error-analysis
    pass — verify the loop closes into
    [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md). (co-24)

### Theme D · Degradation, latency, and the launch decision (ex 34–44)

1. **ex-34 · model-unavailable-state** — design the state for a model that cannot be reached — verify the
   product remains honest and usable. (co-16)
2. **ex-35 · fallback-hierarchy** — a written ladder from best model, to cheaper model, to deterministic
   heuristic, to honest unavailable — verify each rung's quality and cost. (co-18, co-16)
3. **ex-36 · degradation-diagram** — a Mermaid diagram of the fallback ladder with its trigger conditions
   — verify every trigger is observable. (co-18, co-16)
4. **ex-37 · fail-visibly-not-silently** — convert a silent degraded response into a visible degraded
   state — verify the user can tell which rung they are on. (co-19, co-16)
5. **ex-38 · latency-as-material** — streaming, progressive disclosure, and honest waiting compared on the
   same slow response — verify the perceived-quality difference. (co-17)
6. **ex-39 · optimistic-state-that-lies** — an optimistic UI that implies a completed action — verify the
   damage when the action fails. (co-17, co-19)
7. **ex-40 · ship-criteria-from-a-distribution** — write launch criteria as a threshold on a measured pass
   rate with its interval plus a named acceptable worst case — verify each criterion is checkable against
   an eval report. (co-21)
8. **ex-41 · the-worst-case-nobody-named** — a launch whose criteria covered the average and not the tail
   — verify the failure the criteria permitted. (co-21)
9. **ex-42 · staged-rollout-with-guardrails** — an exposure ramp with pre-agreed guardrail metrics —
   verify each metric would actually halt the ramp. (co-22)
10. **ex-43 · rollback-criteria-written-first** — rollback conditions agreed before launch — verify they
    are unambiguous enough to act on during an incident without renegotiation. (co-23)
11. **ex-44 · capstone-probabilistic-feature-design-dossier** — the complete design dossier for one real
    probabilistic feature: a user-visible failure catalogue, an expectation-setting and trust-calibration
    plan, a selective uncertainty and provenance policy meeting WCAG AA, a human-review design costed
    against the vigilance decrement, a consequence-scaled friction table with preview and complete undo, a
    fallback hierarchy with observable triggers, and written ship, guardrail, and rollback criteria
    expressed against a measured distribution — verify a reviewer can trace every design decision to a
    named failure mode and every launch criterion to an eval measurement. (co-01–co-24)

## Capstone spec — intra-topic (concept → full written dossier)

- **Goal**: produce the complete product-design dossier for one real probabilistic feature — the
  learner's own or a public one being redesigned — that a team could take to a launch review. The
  deliverable is written and diagrammatic throughout; no code is produced or required.
- **Concepts exercised**: [ ] a user-visible failure catalogue including the silent-failure path
  (co-02, co-19) [ ] expectation setting and a trust-calibration plan (co-03, co-04, co-05) [ ] a
  selective uncertainty and provenance policy, accessible without colour (co-06–co-09) [ ] verifiability
  designed into the output shape (co-10) [ ] a human-review design costed against reviewer decay (co-11,
  co-12) [ ] a consequence-scaled friction table with preview and complete undo (co-13–co-15) [ ] a
  fallback hierarchy with observable triggers (co-16–co-18) [ ] scoping decisions taken against the
  measured failure rate (co-20) [ ] ship, guardrail, and rollback criteria against a distribution
  (co-21–co-23) [ ] a correction affordance feeding error analysis (co-24).
- **Ordered steps**:
  1. `.../capstone/failure-catalogue.md` — enumerate the feature's user-visible failure modes with a
     concrete example of each and trace the confidently-wrong path end to end. Verify every mode is
     distinguishable by a user and that the silent-failure path is explicitly walked to the user's
     decision point.
  2. `.../capstone/interface-design.md` — the expectation-setting copy, the selective uncertainty and
     provenance policy, and the output restructuring that makes verification cheap, each annotated with
     the failure mode it addresses and each meeting WCAG AA without relying on colour alone. Verify every
     design element traces to a catalogued mode and that no element is uncertainty theatre.
  3. `.../capstone/review-and-recovery.md` — the human-review design with its measured or estimated review
     cost, the consequence-scaled friction table covering every action the feature can take, the
     preview/diff design, the complete-undo design, and the correction affordance. Verify review is
     cheaper than doing the work, that friction is not uniform, and that undo is complete rather than
     partial.
  4. `.../capstone/degradation.md` + `.../capstone/launch-criteria.md` — the fallback hierarchy with
     observable trigger conditions and its Mermaid diagram, then the ship, staged-rollout guardrail, and
     rollback criteria written against a measured distribution with a named acceptable worst case. Verify
     each launch criterion is checkable against a real eval report from
     [`evaluating-ai-output-essentials`](./evaluating-ai-output-essentials.md) or
     [`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md), and that the rollback
     criteria are unambiguous enough to act on without renegotiation.
- **Acceptance criteria**: every design decision in the dossier traces to a named user-visible failure
  mode; the confidently-wrong path is explicitly addressed rather than assumed away; uncertainty signals
  are selective, accessible without colour, and never present confidence as probability-of-correct; the
  human-review design is costed and is cheaper than doing the work unaided, with the vigilance decrement
  explicitly mitigated; friction scales with reversibility and blast radius rather than being uniform;
  undo is complete; the fallback ladder's triggers are observable and the degraded state is visible to
  the user rather than silent; and the ship, guardrail, and rollback criteria are each expressed as a
  threshold on a measured distribution with an interval plus a named acceptable worst case, checkable
  against a real eval report and written down before launch.
- **Done bar**: a complete, reviewable written dossier a launch review could act on + web-verified.

## Read more

> The human-factors references below are `[Needs Verification]` at authoring: confirm the specific
> studies and their findings against primary sources before citing, and cite only what is read.

- **Designing Machine Learning Systems** — Chip Huyen (2022). For the production framing of ML features
  as products with measured failure rates rather than as models with accuracies.
- A primary reference on **automation bias, complacency, and trust calibration** in human-automation
  interaction — the research grounding co-04, co-05, and co-12. Select and cite at authoring.
- A primary reference on **the vigilance decrement** in monitoring tasks — the research grounding the
  claim that reviewer accuracy decays with volume and with system reliability. Select and cite at
  authoring.

## In which paths

- `immediately-effective/ai-engineer` — **owning path**: placed after the light eval
  gate, so ship criteria can be written against a real measurement rather than a hope.
- `interview-ready/software-engineer` — candidate placement in the AI & harness engineering deepening
  tail — pending manifest re-verification (D8 four-path rule).
- `immediately-effective/software-engineer` — candidate placement in the deepening band — pending
  manifest re-verification (D8 four-path rule).
- `fundamentally-strong/software-engineer` — candidate placement in Stage 12 · AI & harness engineering
  — pending manifest re-verification (D8 four-path rule).

---

← Back to [README.md — course library catalog](./README.md)
