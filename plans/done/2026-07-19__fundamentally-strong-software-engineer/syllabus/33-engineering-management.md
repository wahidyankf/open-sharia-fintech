# 33 · Engineering Management (Annotated-concept, ‡ no-code)

**prd row**: Pass 2 · Depth, Design & Craft · Annotated-concept · ‡ no-code · Learn 133 / Drill 233 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: `‡` leadership/no-code — leading engineers and engineering — the IC→manager transition, 1:1s
& feedback & growth, delivery/planning/estimation at team scale, technical strategy & prioritization, org
health & culture, and leading through influence. The
[topic 30 Software Engineering Practices](./30-software-engineering-practices.md) thread arrives here. Deliverables are **leadership/
decision artifacts**, not code. **Closes Pass 2** and anchors the `capstone-solid-core` inter-topic capstone
that re-engineers the Pass-1 app with everything Pass 2 taught (the whole-journey `capstone-lead-at-altitude`
now anchors at the journey's true close, [`94-site-reliability-engineering`](./94-site-reliability-engineering.md)).

## Why this exists · the big idea

- **The problem before the solution**: the best IC gets promoted and keeps solving every problem
  personally — and the team stalls behind the new bottleneck. Management is a different job, not
  senior-IC-plus: the scarce resource stops being your code and becomes other people's judgment.
- **Keep-this-if-you-forget-everything**: you now succeed _through_ others — your output is the team's
  decisions, growth, and trust, measured in outcomes you no longer type yourself.
- **Big ideas touched**: `correctness-vs-pragmatism` — leadership is disciplined compromise, every
  prioritization, estimate, and staffing call trading an ideal for what ships and holds;
  `mechanism-vs-policy` — a lead sets policy (what matters, who decides) and delegates the mechanism
  rather than owning every _how_.

## Prerequisites

- **Prior topics**: [topic 30 Software Engineering Practices](./30-software-engineering-practices.md) (the
  engineering practices a lead upholds and scales across a team), [topic 32 Software Product Engineering](./32-software-product-engineering.md)
  (strategy, prioritization, product partnership), and [topic 9 Project Management](./09-project-management.md)
  (planning, delivery, and the team process a manager stewards).
- **Tools & environment**: no toolchain — a text editor for the leadership artifacts (a growth plan, a
  strategy doc, a prioritization/decision record); Neovim/VSCode (DD-17). No paid account, no code (DD-20).
- **Assumed knowledge**: mature engineering practices (topic 30); business/product judgment (topic 32);
  project planning + delivery process (topic 09).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28); re-verified for Phase 36
> authoring per DD-35.

- 2026-07-12 — verified: IC→manager transition (e.g. Fournier's _The Manager's Path_), 1:1s, feedback,
  coaching, growth plans, competency ladders are current/evergreen. No-code topic, nothing
  version-pinned.
- 2026-07-18 — **correction**: the syllabus's original "DORA four keys" framing is now stale.
  Google Cloud's DORA program (`dora.dev/guides/dora-metrics-four-keys/`, page last updated
  2026-01-05, fetched and read 2026-07-18) has formalized a **five-metric model**, split into
  throughput (change lead time, deployment frequency, failed deployment recovery time — this
  replaces the older "time to restore service"/MTTR framing) and instability (change fail rate,
  plus a new fifth metric, deployment rework rate). The classic "four keys" (deployment frequency,
  lead time for changes, change-failure rate, time-to-restore) remain the widely recognized
  historical framing — Google's own DORA site now presents them as the origin of the current
  five-metric model, not the current model itself. co-11 and every worked scenario/artifact citing
  DORA below use this accurate, dated framing: teach the four-keys history (still how most
  engineering orgs talk about it day to day) while naming the current five-metric model
  explicitly, so nothing here misrepresents Google's current published guidance.
- 2026-07-18 — verified (Open Library API, publication-year check): Fournier's _The Manager's
  Path_ (2017), Larson's _An Elegant Puzzle_ (2019), DeMarco & Lister's _Peopleware_ (1987, 3rd ed.
  2013), and Scott's _Radical Candor_ (2017 original) all check out exactly as cited in this
  file's Read More section — no correction needed.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 8 (Leadership ‡ no-code topic). Each example below cites the co-NN it exercises. -->

Scope stays at the people-leadership altitude: topic 9 owns delivery **mechanics** (triple constraint,
methodology fit, WBS, critical-path, story-point/velocity estimation, sprint/backlog planning, burndown,
risk registers, retro mechanics); topic 32 owns product-strategy **mechanics** (JTBD discovery,
RICE/MoSCoW, MVP scoping, A/B design, north-star/AARRR funnels); topic 30 owns the craft/workflow layer
(git model, PR review, TDD, CI/CD, ADRs, incident hygiene). This topic assumes those are practiced and
teaches _who owns, decides, unblocks, and grows_.

- **co-01 · ic-to-manager-transition** — the job changes from personally solving problems to building a team that solves them; the new scarce resource is other people's judgment, not the manager's own output.
- **co-02 · one-on-ones** — a recurring, report-owned 1:1 is the primary channel for coaching, feedback, and trust-building, not a status-update meeting.
- **co-03 · feedback-sbi** — timely, specific, behavior-focused feedback (Situation-Behavior-Impact), both reinforcing and corrective, changes future behavior better than vague praise or criticism.
- **co-04 · coaching-vs-directing** — a coaching stance (asking questions that draw out the report's own judgment) grows capability, while directing (telling) only resolves the immediate problem.
- **co-05 · growth-plans** — a written growth plan turns vague potential into named strengths, gaps, and observable next-level behaviors a report can act on.
- **co-06 · competency-ladders** — a competency/career ladder defines the observable behaviors that distinguish each level, making promotion and feedback conversations concrete instead of political.
- **co-07 · performance-management-and-calibration** — regular, honest performance assessment, including calibration across reports and managers, catches drift early and makes promotion/PIP decisions defensible.
- **co-08 · delegation-and-context-setting** — a manager delegates the how while retaining the what and why, giving enough context that a report can make the same call the manager would.
- **co-09 · team-delivery-stewardship** — a manager stewards delivery at the team level — unblocking, sequencing, and managing WIP across people — distinct from the task-level estimation/planning mechanics a single project uses.
- **co-10 · prioritization-under-competing-demands** — deciding which of several competing team-level demands (new work, tech debt, incidents, staffing asks) gets done now is a leadership call that produces an explicit, defensible trade-off record.
- **co-11 · dora-metrics-as-outcome-lens** — DORA's software delivery metrics (originally four keys — deployment frequency, lead time for changes, change-failure rate, time-to-restore — now formalized by Google Cloud's DORA program as a five-metric throughput/instability model) give a manager an outcome lens on team health, used as a diagnostic, not a per-person scorecard.
- **co-12 · technical-strategy** — a manager sets a technical direction — what bets, in what order — that ties engineering work to business/product outcomes, distinct from any single project's delivery plan.
- **co-13 · roadmap-partnership-with-product** — an engineering lead partners with product on the roadmap, representing technical cost, risk, and dependency so trade-offs are made jointly rather than imposed by either side.
- **co-14 · communicating-tradeoffs** — a leader makes a trade-off and its cost legible to stakeholders, so the decision is understood and ownable instead of read as arbitrary.
- **co-15 · culture-and-psychological-safety** — a team's culture — its norms, what's rewarded, what's safe to say — determines whether problems surface early or hide until they're expensive.
- **co-16 · hiring-intuition** — evaluating candidates for the traits a role actually needs, with structured, evidence-based scoring over pedigree or gut feel, is a distinct, learnable leadership skill.
- **co-17 · influence-without-authority** — a lead moves peers and stakeholders who don't report to them through trust, credibility, and shared incentive, not positional power.
- **co-18 · org-design-and-team-topology** — Conway's Law makes team boundaries a technical decision: team communication structure shapes system structure, so org design is an engineering lever.
- **co-19 · learning-as-a-team-norm** — a manager makes continuous learning, not just delivery, an explicit recurring team habit, converting individual growth into an organizational capability.
- **co-20 · manager-vs-maker-tension** — staying hands-on keeps technical credibility, but coding on the critical path recreates the bottleneck the manager was promoted to remove.

## Tensions & trade-offs — when NOT to reach for this

- **Autonomy vs alignment**: over-direct and you get a team of hands, not minds; under-direct and effort
  scatters. Set the _what_ and _why_, delegate the _how_ — the lever is context, not control.
- **Delivery vs growth**: shipping this quarter competes with growing people who ship every quarter.
  Over-index on delivery and you spend the team down, stopping the learning that compounds into next
  year's velocity.
- **Metrics vs trust**: DORA keys and velocity focus a team, but any metric is gameable, and measuring
  people as throughput corrodes the trust that actually drives delivery. Metrics inform judgment; they
  don't replace it.
- **Manager vs maker**: staying hands-on keeps technical credibility, but coding on the critical path
  makes you the bottleneck you were promoted to remove — the hardest habit to unlearn.

## Lineage — why it beat the alternative

- Engineering management professionalized as teams outgrew the heroic-lead / player-coach model that
  doesn't scale past a handful of people. Command-and-control factory management (Taylorism) treated
  engineers as interchangeable throughput and failed on creative knowledge work; the pure servant-leader
  reaction under-set direction and drifted. Modern practice converged on a middle — set clear direction
  with high trust, measure outcomes not activity, grow people as the durable asset — evidenced by DORA's
  research base and codified in Fournier's _The Manager's Path_ and Larson's systems view. Conway's Law
  made org design a technical concern (team boundaries become system boundaries), which is why this closes
  Pass 2 on `coupling-vs-cohesion` at org scale, pairs with [`32-software-product-engineering`](./32-software-product-engineering.md)
  (what to build) and [`09-project-management`](./09-project-management.md) (deliver it), and matures into
  the org-level reliability trade-offs of [`94-site-reliability-engineering`](./94-site-reliability-engineering.md).

## Worked examples

Colocated under `engineering-management/learning/artifacts/` (no `code/` — leadership deliverables per the
`‡` shape, DD-27/DD-30). Contiguous `ex-01..ex-27`. Every example cites the `co-NN` it exercises; every
concept above is exercised by ≥1 scenario.

### Beginner

- **ex-01 · first-1-1-agenda** — draft a report-owned 1:1 agenda template that flips the traditional status-update format — verify the report's items lead the agenda and the manager's items sit last. (co-02)
- **ex-02 · sbi-feedback-positive** — write a positive-feedback note for a report's strong incident response using Situation-Behavior-Impact — verify it names the specific situation, the observed behavior, and its impact, not a general "great job." (co-03)
- **ex-03 · sbi-feedback-corrective** — write a corrective-feedback note for a missed deadline using SBI — verify it stays behavior-focused (not character-focused) and states the "instead" wanted going forward. (co-03)
- **ex-04 · coaching-question-vs-answer** — given a report's stuck design problem, write both a directive answer and three coaching questions — verify the coaching version supplies no solution, only questions that let the report reach one. (co-04)
- **ex-05 · growth-plan-artifact** — a growth plan for a hypothetical report naming strengths, gaps, and next-level behaviors — verify every gap maps to an observable behavior, not a vague trait. (co-05, co-06)
- **ex-06 · ladder-behavior-mapping** — map three of a report's recent actions onto specific rungs of a competency ladder — verify each mapping cites the ladder's stated behavior text, not a subjective impression. (co-06)
- **ex-07 · delegation-context-brief** — write a delegation brief handing a report a decision, stating the what and why but not the how — verify a reader unfamiliar with the manager's intent could still make the same call from the brief alone. (co-08)
- **ex-08 · ic-to-manager-mindset-memo** — a first-week memo from a newly promoted manager naming what they will stop doing personally and what replaces it — verify it names concrete IC habits given up, not just aspirations. (co-01)
- **ex-09 · manager-vs-maker-catch** — diagnose a week where the manager coded on the critical path and missed two 1:1s — verify the artifact names the bottleneck this created and one corrective habit change. (co-20, co-01)

### Intermediate

- **ex-10 · prioritization-decision-record** — a prioritization/trade-off decision record for a team facing competing demands (a new feature, mounting tech debt, and on-call load) — verify it states the options, the trade-off, the decision, and the communication plan. (co-10, co-14)
- **ex-11 · dora-diagnostic-memo** — read a team's four DORA numbers and write a diagnostic memo on where to invest next — verify the recommendation ties to the specific weak metric, not a generic "go faster." (co-11)
- **ex-12 · wip-unblock-triage** — triage a week's blocker list into what the manager personally unblocks, delegates, or escalates — verify every item has a named owner and a stated reason for that owner. (co-09)
- **ex-13 · performance-calibration-note** — a calibration note comparing two reports' impact against the same ladder rung — verify it cites ladder-level evidence for each, not a relative popularity judgment. (co-07, co-06)
- **ex-14 · difficult-feedback-conversation-script** — script a corrective conversation for a pattern of missed deadlines, not a single incident — verify it opens with the pattern (not the latest miss) and ends with one named next step. (co-03, co-07)
- **ex-15 · roadmap-tradeoff-memo** — a memo representing engineering cost and risk in a product roadmap negotiation — verify it states the specific trade-off product is being asked to accept, not just a technical objection. (co-13, co-14)
- **ex-16 · psychological-safety-incident** — diagnose a retro where nobody raised the real blocker until after the deadline slipped — verify the artifact names the safety failure and one concrete norm change to fix it. (co-15)
- **ex-17 · hiring-debrief-structured** — a structured hiring debrief scoring a candidate against role-specific signals — verify every score cites observed evidence from the interview loop, not a gut "I liked them." (co-16)
- **ex-18 · influence-without-authority-plan** — a plan to win a peer team's buy-in on a shared platform change with no reporting line into them — verify the plan names the shared incentive it appeals to, not an appeal to authority. (co-17)
- **ex-19 · team-culture-norm-change** — propose one culture-norm change (e.g. blameless postmortems) plus the mechanism that makes it stick — verify the mechanism outlasts the announcement (a recurring ritual, not a one-time email). (co-15)

### Advanced

- **ex-20 · technical-strategy-doc** — a one-page technical strategy tying team goals to product outcomes with explicit trade-offs — verify every technical bet traces to a stated product outcome and its trade-off is explicit. (co-12, co-14)
- **ex-21 · conways-law-reorg-memo** — propose a team-topology change and predict the resulting system-boundary shift — verify the memo names Conway's Law explicitly and states the predicted new boundary. (co-18)
- **ex-22 · dora-goodhart-guardrail** — design a way to use DORA metrics for team-level diagnosis without turning them into an individual scorecard — verify the design names the specific gaming risk it guards against. (co-11)
- **ex-23 · autonomy-vs-alignment-calibration** — for two reports (one needing more direction, one needing more autonomy), calibrate delegation differently and justify each — verify each calibration cites a specific readiness signal, not a uniform policy applied to both. (co-08, co-04)
- **ex-24 · delivery-vs-growth-tradeoff-memo** — decide whether a stretch assignment under deadline pressure goes to the fastest engineer or the growing one — verify the memo states explicitly what is traded: near-term speed vs future team capability. (co-01, co-05)
- **ex-25 · learning-norm-institutionalization** — design a recurring team ritual (e.g. a rotating tech talk or post-incident learning review) meant to survive the founding manager leaving — verify the design names the mechanism that keeps it running without its original owner. (co-19)
- **ex-26 · succession-and-delegation-plan** — a plan delegating a manager's own responsibilities to grow a future lead on the team — verify the plan names which decisions transfer first and the observable signal that triggers transferring the next one. (co-08, co-01)
- **ex-27 · full-leadership-decision-set** — assemble the growth plan, the prioritization decision record, and the technical strategy into one internally coherent leadership decision set for a hypothetical team — verify every artifact references the same team context and no trade-off in one contradicts another. (co-01, co-05, co-06, co-10, co-12, co-13, co-14)

## Capstone spec — intra-topic (leadership → decision artifact, no code)

- **Goal**: produce a **leadership decision set** a new engineering lead would actually use — a growth plan
  for a report, a team prioritization/trade-off decision record, and a one-page technical strategy linking
  team goals to product outcomes — demonstrating leadership through structured judgment and clear
  communication. **No code.**
- **Concepts exercised**: [ ] a growth plan (strengths/gaps/next-level behaviours + a feedback frame)
  (co-03, co-05, co-06) [ ] a prioritization/trade-off decision record (co-10, co-14) [ ] a one-page
  technical strategy tying team → product outcomes (co-12, co-13) [ ] explicit, communicated trade-offs
  (co-14) [ ] leading through influence (co-17).
- **Ordered steps**:
  1. `.../learning/capstone/artifacts/growth-plan.md` — a growth plan for a hypothetical report with a
     concrete feedback frame. Verify it names strengths, gaps, and observable next-level behaviours.
  2. `prioritization.md` — a decision record for competing team demands. Verify it states the options, the
     trade-offs, the decision, and the communication plan.
  3. `strategy.md` — a one-page technical strategy linking team goals to product outcomes. Verify every
     technical bet traces to a product outcome and its trade-off is explicit.
- **Acceptance criteria**: the growth plan is actionable and specific; the prioritization record makes
  trade-offs explicit and communicable; the strategy ties team work to product outcomes; the set reads as
  usable leadership judgment. No code.
- **Done bar**: complete leadership artifact set + internally coherent + web-verified.

<!-- Inter-topic capstone spec block: this file (last topic of Pass 2) anchors the Pass-2 boundary capstone -->

## Capstone spec — inter-topic: capstone-solid-core (Pass-2 boundary)

- **Weight**: `capstone-solid-core/_index.md` = **435** (section root, after Pass 2 / topic 33). Kind:
  **pass-boundary**, integrating Pass 2 topics 19–33 (design + paradigms + concurrency + algorithms +
  advanced SQL + practices + product/delivery discipline).
- **Goal**: take the **`capstone-first-working-software`** app from Pass 1 and **re-engineer it to a
  professional core**: apply SOLID + patterns (21), choose paradigms deliberately with a functional core
  (22/23), make a hot path concurrent and correct (24), improve an algorithm/complexity (25), tune the
  data layer with `EXPLAIN`-driven indexing (26), wrap it in an engineering workflow — clean git history,
  CI gate, ADRs (30) — and frame the work with product/delivery discipline (32/33). CS-foundations
  reasoning (19) justifies the performance choices.
- **Concepts integrated**: [ ] SOLID + patterns refactor (21) [ ] deliberate paradigm choice + functional
  core (22/23) [ ] safe concurrency on a hot path (24) [ ] an algorithm/complexity improvement (25/19)
  [ ] `EXPLAIN`-driven SQL tuning (26) [ ] CI gate + clean history + ADR (30) [ ] a product brief + delivery
  plan framing the work (32/33).
- **Ordered steps**:
  1. `capstone-solid-core/code/` — import the Pass-1 app under a green test suite; write an ADR stating the
     re-engineering goals (30/32/33). Verify the suite passes against the imported baseline.
  2. Refactor the core to SOLID + patterns with a functional core / imperative shell split (21/22/23).
     Verify behavior is unchanged (suite green) and a new variation can be added without editing closed
     classes (OCP).
  3. Make one hot path concurrent (24) and improve one algorithm/query: apply an index guided by
     `EXPLAIN ANALYZE` (26/25). Verify correctness is preserved and a before/after measurement shows the
     improvement.
  4. Wrap it in the workflow: clean conventional-commit history + a CI pipeline gate (lint→test→build) +
     ADRs; attach the product brief + delivery plan (30/32/33). Verify CI gates the change green and fails
     on a bad commit.
- **Acceptance criteria**: a reader on a clean machine builds and tests the re-engineered app, confirms the
  SOLID/functional-core refactor preserved behavior, sees the measured concurrency/SQL/algorithm
  improvements, and finds the CI gate, clean history, ADRs, and product/delivery artifacts in place — end
  to end, no hidden setup.
- **Done bar**: runnable end-to-end (clean-machine reproduction) + produces the decision artifacts +
  web-verified.

## Read more

**Books**

- **The Manager's Path** — Camille Fournier (2017). The standard reference guide for engineers moving into technical leadership and management roles.
- **An Elegant Puzzle: Systems of Engineering Management** — Will Larson (2019). Widely cited systems-thinking guide to engineering organization design and management.
- **Peopleware: Productive Projects and Teams** — Tom DeMarco & Timothy Lister (1987; 3rd ed. 2013). Classic text on the human and organizational factors that determine software team productivity.
- **Radical Candor: Be a Kick-Ass Boss Without Losing Your Humanity** — Kim Scott (2017; revised ed. 2019). Standard reference framework for direct, caring feedback and effective one-on-ones.

---

← Previous: [32 · Software Product Engineering](./32-software-product-engineering.md) · Next: [34 · NoSQL Databases](./34-nosql-databases.md) →
