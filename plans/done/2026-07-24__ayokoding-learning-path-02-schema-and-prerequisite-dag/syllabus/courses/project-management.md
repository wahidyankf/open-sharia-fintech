# Project Management (Annotated-concept, — (concept, no code))

**Course ID**: `project-management` · **Format**: Annotated-concept · **Language**: — (concept, no code).

**Short summary**: Scoping, planning, estimating, tracking work

**Scope note**: the **Product & Delivery** track (`▲`) — delivery execution: methodologies, the triple
constraint, planning/estimation, execution mechanics, metrics, and risk/change management. Leadership
topic (`‡`): **no code** — prose, worked design/decision exercises, and diagrams. A **Pass-1** ▲ topic read
early so delivery discipline is available from the start; the Pass-2 boundary `capstone-solid-core` anchors
later at [`33-engineering-management`](./engineering-management.md), where people leadership also deepens.

## Why this exists · the big idea

- **The problem before the solution**: work that isn't planned, sequenced, and de-risked slips silently —
  the schedule is already late before anyone notices, because nobody made the constraints and dependencies visible.
- **Keep-this-if-you-forget-everything**: scope, schedule, and cost are one triangle — you can fix any two,
  and pretending you can fix all three is how projects fail. Make the trade-off explicit and chosen.
- **Big ideas touched**: `correctness-vs-pragmatism` (estimation and risk are decisions under uncertainty,
  not precision), `coupling-vs-cohesion` (task dependencies are coupling, and the critical path is the tightest chain).

## Prerequisites

- **Prior topics**: no code prerequisites. Pairs with
  [topic 32 Software Product Engineering](./software-product-engineering.md) (what to build → how to
  deliver it); assumes Pass-1/Pass-2 building experience so estimation and scope trade-offs are concrete.
- **Tools & environment**: a macOS/Linux terminal and a Markdown editor (Neovim per DD-17) for the plans
  and charts; no runtime — deliverables are planning artifacts and decision documents.
- **Assumed knowledge**: what a feature's worth of work feels like; reading a simple chart; the idea of a
  dependency between tasks.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the current official **Scrum Guide is the November 2020 revision** (Schwaber &
  Sutherland) — no newer official revision supersedes it in 2026; cite the 2020 guide specifically
  (13 pages, softened prescriptive language). Critical-path method, burndown/cycle-time/lead-time metrics,
  and story-point/velocity estimation remain standard unchanged PM vocabulary. (scrumguides.org)
- 2026-07-14 — re-confirmed (Phase 10 pre-authoring currency check, `web-researcher`): all four
  load-bearing claim groups still current — (1) Scrum Guide's revision history at
  [scrumguides.org/revisions.html](https://scrumguides.org/revisions.html) still lists November 2020 as
  the latest entry, no newer official revision exists; (2) Agile Manifesto site
  ([agilemanifesto.org](https://agilemanifesto.org/)) unchanged — 17 signatories, four values, links to
  the twelve principles; (3) CPM/PERT 1950s lineage (DuPont/Remington Rand CPM, US Navy Special Projects
  Office PERT) independently corroborated via [PMI](https://www.pmi.org/learning/library/origins-cpm-personal-history-3762)
  and cross-checked against Wikipedia's Critical path method article, no correction needed; (4) all three
  "Read more" book citations (Brooks, DeMarco & Lister 3rd ed. 2013, McConnell 2006) independently
  re-corroborated, including a spot-check resolving an unrelated ACM-catalog "2016" artifact in favor of
  Peopleware's confirmed 2013 3rd-edition date. No syllabus corrections required.

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary/authoritative source fetched and read in the retroactive
> grounding sweep (2026-07-12, `web-researcher`). All 9 checkable claims verified; no corrections.

- **Scrum Guide (co-scrum, Lineage)** — current official guide is the **November 18, 2020** revision
  (Schwaber & Sutherland), per [scrumguides.org](https://scrumguides.org/) +
  [revisions](https://scrumguides.org/revisions.html); no 2021–2026 official revision exists ("Scrum Guide
  Expanded" v2026.1 is an unofficial community derivative, not superseding). The file never mis-cites
  legacy "ceremonies"/"three roles"/"Development Team" vocabulary to the Guide (the one "ceremonies" use
  is generic PM prose).
- **Agile Manifesto (Lineage, Read more)** — [agilemanifesto.org](https://agilemanifesto.org/): title
  exact, **17 signatories** (Kent Beck + 16, [authors](https://agilemanifesto.org/authors.html)), Snowbird
  Utah Feb 11–13 2001, four values + [twelve principles](https://agilemanifesto.org/principles.html) — all
  confirmed.
- **CPM / PERT lineage** — CPM 1956–59 (Kelley/Walker, DuPont + Remington Rand); PERT 1958 (US Navy Special
  Projects Office / Polaris), per [PMI history](https://www.pmi.org/learning/library/origins-cpm-personal-history-3762)
  - [Mosaic Projects](https://mosaicprojects.com.au/PMKI-ZSY-030.php). File's "(1950s, US Navy / DuPont)"
    shorthand accurate. Kanban = lean-manufacturing flow (Toyota/Ohno), uncontested.
- **Read more books** — _The Mythical Man-Month_, Brooks, Anniversary ed. 1995 (orig. 1975), Brooks's Law
  ([ACM](https://dl.acm.org/doi/book/10.5555/207583)); _Peopleware_, DeMarco & Lister, 3rd ed. 2013 (orig.
  1987); _Software Estimation: Demystifying the Black Art_, McConnell, 2006
  ([Microsoft Press](https://www.microsoftpressstore.com/store/software-estimation-demystifying-the-black-art-9780735690851)) —
  author/edition/year all confirmed.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 8 (Annotated-concept ‡). Each example below cites the co-NN it exercises. -->

- **co-01 · triple-constraint** — Scope, schedule, and cost form one triangle: you can fix any two, and
  pretending to fix all three is how projects fail — the trade-off must be made explicit and chosen.
- **co-02 · delivery-methodologies** — Waterfall, agile (Scrum, Kanban), and hybrid each fit a different
  context; the methodology follows the shape of the work, not fashion.
- **co-03 · work-breakdown-structure** — Decompose deliverables into a WBS of work packages small enough to
  be independently estimated and assigned.
- **co-04 · dependency-graph-and-critical-path** — Task dependencies form a directed graph; the critical
  path is the longest cumulative-duration chain and it, not any single task, bounds the schedule.
- **co-05 · estimation-points-velocity** — Story points plus velocity estimate work under uncertainty and
  forecast completion; raw hour-estimates fake a precision that does not exist.
- **co-06 · planning-poker-pitfalls** — Relative estimation is distorted by anchoring and authority bias;
  facilitation rules (blind reveal, discuss outliers) counter each named bias.
- **co-07 · sprint-and-backlog-planning** — An ordered backlog plus per-sprint commitment must respect team
  capacity and task dependencies, so no sprint over-commits or violates ordering.
- **co-08 · execution-mechanics** — Standups, WIP limits, and issue/blocker tracking keep in-flight work
  visible day to day so problems surface early rather than at the deadline.
- **co-09 · metrics** — Burndown/burnup, cycle time, lead time, and throughput each inform a specific
  decision; a metric that names no decision is decoration.
- **co-10 · risk-management** — A living risk register identifies risks, rates them by likelihood×impact,
  assigns an owner, and pairs each with a concrete mitigation.
- **co-11 · change-management** — Scope change runs through a controlled decision (accept/defer/trade) against
  the triple constraint, so the triangle stays honest instead of silently overloaded.
- **co-12 · retrospectives** — Structured reflection on delivered work turns raw observations into owned,
  tracked improvement actions — continuous improvement, not blame.
- **co-13 · stakeholder-communication** — Tailoring cadence, audience, and format keeps expectations and
  decisions aligned; each update should drive a decision, not merely report status.
- **co-14 · goodhart-metric-abuse** — A measure used as a target stops measuring: velocity-as-productivity
  invites point inflation and destroys the signal it was meant to provide.
- **co-15 · process-weight-fit** — Coordination cost scales with communication paths (`n(n-1)/2`), so
  ceremony must be right-sized to team size — process that exceeds the coordination it saves is waste.

## Tensions & trade-offs — when NOT to reach for this

- **Methodology fit**: Scrum's cadence suits evolving product work with an engaged customer; Kanban suits
  continuous-flow and ops; waterfall genuinely fits fixed-scope, high-cost-of-change domains (regulated,
  hardware). Cargo-culting Scrum onto the wrong context adds ceremony without the benefit it was built for.
- **Estimation honesty**: points and velocity beat hour-estimates because they embrace uncertainty instead of
  faking precision — but velocity becomes a lie the instant it's used as a productivity target (Goodhart
  again). Estimates inform a commitment; they don't remove the need for slack.
- **Process weight**: standups, planning, and retros cost real hours; on a two-person project they can exceed
  the coordination they save. Match process to the number of communication paths — which grow with the square
  of team size, not linearly.

## Lineage — why it beat the alternative

- Project management formalized in mid-20th-century large engineering — critical-path method and PERT (1950s,
  US Navy / DuPont) — where sequencing dependencies on enormous projects was the binding constraint. Agile
  (2001 Manifesto) was a reaction against heavyweight plan-everything-upfront PM failing on software's high
  rate of change: it moved the constraint from _following the plan_ to _responding to change_, and Kanban
  imported lean-manufacturing flow. The invariant across all of it is one move — make work, constraints, and
  risk _visible_, so trade-offs are chosen rather than stumbled into. That visibility discipline is exactly
  what [`33-engineering-management`](./engineering-management.md) scales up to people and organizations.

## Worked examples

Worked scenarios / decision artifacts under `project-management/learning/artifacts/` (prose + diagrams; no
`code/` runtime — DD-27 leadership kind). Each is a decision document or chart a team could act on, and each
cites the `co-NN` it exercises. Contiguous `ex-01..ex-25`.

### Beginner

- **ex-01 · triple-constraint-tradeoff** — given a fixed deadline plus a fixed-scope request, write the
  trade-off memo choosing which constraint gives — verify the artifact names which two are fixed and what the
  third absorbs. (co-01)
- **ex-02 · pick-methodology** — map three contexts (regulated hardware, evolving product, ops queue) to
  waterfall/Scrum/Kanban with a one-line rationale each — verify every mapping cites the context property that
  drives it. (co-02)
- **ex-03 · wbs-decompose** — decompose a sample feature into a two-level WBS of work packages — verify every
  leaf is independently estimable and assignable. (co-03)
- **ex-04 · dependency-graph** — draw a Mermaid dependency graph over the WBS tasks — verify every edge
  encodes a real "must finish before" relation. (co-04)
- **ex-05 · identify-critical-path** — mark the critical path on that graph — verify it is the longest
  cumulative-duration chain and has zero slack. (co-04)
- **ex-06 · story-point-estimate** — assign story points to a small backlog against a reference story —
  verify estimates are relative to the reference, not hour-based. (co-05)
- **ex-07 · velocity-forecast** — from three sprints of past velocity, forecast a backlog's completion —
  verify the forecast uses average velocity, not a single sprint's number. (co-05)
- **ex-08 · metric-decision-map** — for burndown, cycle time, and lead time, name the decision each informs —
  verify every metric row states a concrete decision, not just a definition. (co-09)

### Intermediate

- **ex-09 · sprint-backlog-plan** — split an estimated backlog into two sprints respecting capacity and
  dependencies — verify no sprint exceeds velocity and no task precedes its dependency. (co-07)
- **ex-10 · planning-poker-debias** — write facilitation rules that counter anchoring and authority bias —
  verify each rule maps to a named bias it neutralizes. (co-06)
- **ex-11 · burndown-diagnosis** — interpret a burndown that flatlines mid-sprint — verify the artifact names
  a plausible cause plus one corrective action. (co-09)
- **ex-12 · burnup-vs-burndown** — choose burnup when scope is changing and justify it — verify the rationale
  ties scope-change visibility to burnup's separate scope line. (co-09, co-11)
- **ex-13 · cycle-time-bottleneck** — read an aging/cumulative-flow diagram to locate a WIP bottleneck —
  verify the artifact identifies the stage with growing WIP. (co-09, co-08)
- **ex-14 · risk-register** — build a risk register (likelihood, impact, mitigation, owner) for five risks —
  verify each top risk has a concrete, assigned mitigation. (co-10)
- **ex-15 · risk-prioritization** — rank the risks by likelihood×impact and pick the top three to act on —
  verify the ranking is consistent with the computed scores. (co-10)
- **ex-16 · change-request-decision** — given a mid-sprint scope-add, write the accept/defer/trade decision
  against the triple constraint — verify it states what is dropped or extended to absorb the change. (co-11,
  co-01)
- **ex-17 · standup-redesign** — redesign a status-theater standup into a blocker-focused one — verify the new
  format surfaces blockers and WIP rather than status recitation. (co-08)
- **ex-18 · stakeholder-comm-plan** — build a stakeholder communication matrix (audience, cadence, format,
  decision) — verify each audience row names the decision the update drives. (co-13)

### Advanced

- **ex-19 · velocity-goodhart-memo** — write a memo on why making velocity a productivity target backfires,
  with an alternative — verify it explains point inflation and proposes an outcome metric. (co-14, co-05)
- **ex-20 · process-weight-right-size** — for a two-person vs an eight-person team, right-size ceremonies from
  communication-path count — verify the recommendation cites `n(n-1)/2` paths. (co-15)
- **ex-21 · methodology-antipattern** — diagnose cargo-culted Scrum installed on fixed-scope regulated work —
  verify the artifact names the mismatch and proposes a better fit. (co-02, co-15)
- **ex-22 · crashing-vs-fast-tracking** — for a late critical path, compare crashing (spend cost) vs
  fast-tracking (spend risk) — verify each option is tied to the constraint it spends. (co-04, co-01)
- **ex-23 · retrospective-to-action** — turn a retro's raw notes into tracked, owned improvement actions —
  verify each action has an owner and a measurable done-signal. (co-12)
- **ex-24 · risk-register-over-time** — plan how the risk register evolves across sprints — verify the
  artifact shows risks retired as mitigations land and new risks added as they emerge. (co-10, co-12)
- **ex-25 · full-delivery-plan** — assemble WBS + critical path, velocity estimate, sprint plan, risk
  register, and metrics plan into one internally consistent delivery plan — verify the critical path drives
  the schedule, estimates align with sprints, and every metric names its decision. (co-01, co-03, co-04,
  co-05, co-07, co-09, co-10)

## Capstone spec — intra-topic (leadership ‡ → design/decision artifact)

- **Goal**: produce a compact **delivery plan** for a small project: a work-breakdown structure with a
  dependency graph and critical path, a velocity-based estimate, a sprint/backlog plan, a risk register,
  and a metrics plan (burndown + cycle time) — a decision artifact a team could execute against.
- **Concepts exercised**: [ ] WBS + dependency graph + critical path [ ] velocity/story-point estimation
  [ ] a sprint/backlog plan [ ] a risk register with mitigations [ ] a metrics plan (burndown/cycle time).
- **Ordered steps**:
  1. `project-management/learning/capstone/plan.md` — the WBS + a Mermaid dependency graph; mark the
     critical path. Verify the critical path is the longest dependency chain in the graph.
  2. Add a velocity-based estimate + a sprint/backlog breakdown. Verify the estimate uses points/velocity
     (not raw hours) and the sprint plan respects dependencies.
  3. Add a risk register (likelihood/impact/mitigation) + a metrics plan. Verify each top risk has a
     concrete mitigation and each metric names what decision it informs.
- **Acceptance criteria**: the plan is internally consistent (critical path drives the schedule; estimates
  and sprints align; risks have mitigations) and executable without hand-waving.
- **Done bar**: produces the stated artifact (delivery plan) + web-verified.

## Read more

**Books**

- **The Mythical Man-Month** — Frederick P. Brooks Jr. (Anniversary ed., 1995; orig. 1975). Seminal essays on software project management; origin of Brooks's Law.
- **Peopleware: Productive Projects and Teams** — DeMarco, Lister (3rd ed., 2013; orig. 1987). Classic argument that software success is a human/organizational problem first.
- **Software Estimation: Demystifying the Black Art** — Steve McConnell (2006). Standard practical reference for estimation techniques.

**Papers & articles**

- **Manifesto for Agile Software Development** — Kent Beck + 16 co-signatories (2001). Founding document of agile: four values, twelve principles. <https://agilemanifesto.org/>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Ops, platform, quality & product — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Quality, product, delivery & leadership — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 14 · Quality, product, delivery & leadership.

> _Content originated in the now-closed FS-SE plan (topic 9); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
