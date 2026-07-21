# Platform Engineering and DevEx (Annotated-concept, — (concept, no code))

**Course ID**: `platform-engineering-and-devex` · **Format**: Annotated-concept · **Language**: — (concept, no code).

**Short summary**: Internal platforms, golden paths, DevEx

**Scope note**: paving the road for other engineers — internal developer platforms (Backstage-style portals
and IDPs), golden paths, self-service infrastructure, and measuring developer productivity (DORA, SPACE)
without weaponizing the numbers. `‡ no-code`: this is a concept/practice topic; its deliverables are golden-
path templates, a platform contract, and a measurement dashboard rather than an application. It builds on
the operational substrate — [`50-containers-and-orchestration`](./containers-and-orchestration.md),
[`51-cloud-and-iac`](./cloud-and-iac.md), and [`55-cicd-and-release-engineering`](./cicd-and-release-engineering.md)
— and treats those as the platform's raw material.

## Why this exists · the big idea

- **The problem before the solution**: as an org grows, every team reinvents CI, deploy, secrets, and infra
  glue slightly differently; cognitive load explodes and the same problems get solved badly N times. Platform
  engineering exists to factor that shared work out once, as a product, so stream-aligned teams can ship
  without becoming part-time infra experts.
- **Keep-this-if-you-forget-everything**: treat the platform as a product with internal customers — the win
  is a paved golden path that is genuinely easier than the DIY route, offered as self-service, not mandated.
  If the paved road is worse than going off-road, you have built a toll booth, not a platform.
- **Big ideas touched**: `mechanism-vs-policy` (the platform provides mechanism — self-service infra, golden
  paths — while leaving product teams to decide policy; a good platform is opinionated defaults, not a
  straitjacket), `coupling-vs-cohesion` (Team Topologies' platform/stream-aligned split is coupling-and-
  cohesion applied to the org chart — reduce inter-team coupling by giving teams a well-bounded platform
  interface).

## Prerequisites

- **Prior topics**: [topic 50 Containers & Orchestration](./containers-and-orchestration.md) (the runtime
  substrate a platform abstracts), [topic 51 Cloud & IaC](./cloud-and-iac.md) (the self-service infra a
  platform provisions), and [topic 55 CI/CD & Release Engineering](./cicd-and-release-engineering.md) (the
  delivery pipeline golden paths automate).
- **Tools & environment**: no application to build; a developer portal / IDP concept (Backstage-style catalog
  - scaffolder templates), an IaC + CI stack from the prior topics for the golden path to sit on, and a
    DORA/SPACE metrics source. Any scripting for scaffolders or dashboards that uses Python is fully
    type-annotated (DD-39). Neovim/VSCode (DD-17).
- **Assumed knowledge**: containers/orchestration basics (topic 50); IaC and cloud provisioning (topic 51);
  CI/CD pipelines and DORA metrics (topic 55); team/organizational structure trade-offs (topic 33).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the core frames — Team Topologies' platform-as-a-product and platform/stream-aligned
  team types, golden paths, self-service IDPs, and the DORA four keys plus the SPACE framework for developer
  productivity — are current, widely adopted, and correctly left tool-version-unpinned. Backstage is named as
  the representative open portal but the topic stays tool-agnostic about the specific IDP.
- 2026-07-12 — verified: the CNCF Platforms White Paper is the industry-consensus definition of an internal
  developer platform and is the right anchor for the "what is a platform" framing; no version pin needed.
  (tag-app-delivery.cncf.io/whitepapers/platforms)

### DD-35 primary-source citations (fetched-and-read)

Every framework, metric, and named project below traces to a primary source fetched and read during
grounding. Unverifiable specifics are marked `[Needs Verification]` and never shipped as fact.

- **Team Topologies** (Skelton & Pais, 2019) defines four team types — **stream-aligned, platform, enabling,
  complicated-subsystem** — and three interaction modes — **collaboration, X-as-a-service, facilitating**.
  (teamtopologies.com/key-concepts)
- **DORA metrics** — the **four keys** are deployment frequency, lead time for changes, change failure rate,
  and failed-deployment recovery time (formerly MTTR); DORA later added a **fifth key, reliability**
  (operational performance). So cite it as "four throughput/stability keys **plus reliability**", not just
  four. Empirical base: _Accelerate_ (Forsgren, Humble, Kim, 2018) + the annual State of DevOps reports.
  (dora.dev/guides/dora-metrics-four-keys)
- **SPACE framework** — Satisfaction & well-being, Performance, Activity, Communication & collaboration,
  Efficiency & flow — is the multidimensional productivity model (Forsgren et al., ACM Queue, 2021).
  (queue.acm.org/detail.cfm?id=3454124)
- **Backstage** is a **CNCF Incubating** project (donated by Spotify) — the representative open developer
  portal; the topic stays tool-agnostic about the specific IDP. (cncf.io/projects/backstage, backstage.io)
- **CNCF Platforms White Paper** (TAG App Delivery, 2023) is the industry-consensus definition of an internal
  developer platform. (tag-app-delivery.cncf.io/whitepapers/platforms)
- **Goodhart's law** ("when a measure becomes a target, it ceases to be a good measure") is the grounding for
  the metrics-anti-weaponization boundary — framing, not a version claim.

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (‡ leadership / annotated-concept). Each scenario below cites the co-NN it exercises. -->

- **co-01 · platform-as-product** — treat the platform as a product with internal customers, not a mandate.
- **co-02 · internal-customer** — the product/stream-aligned teams are the platform's customers.
- **co-03 · team-topologies** — the platform vs stream-aligned (plus enabling, complicated-subsystem) split.
- **co-04 · interaction-modes** — collaboration, X-as-a-service, and facilitating modes between teams.
- **co-05 · cognitive-load** — the platform's purpose is to lower stream-aligned teams' cognitive load.
- **co-06 · golden-path** — a paved, opinionated-default route that is genuinely easier than DIY.
- **co-07 · golden-path-escapable** — the paved road stays optional and escapable, never a cage.
- **co-08 · idp** — an internal developer platform/portal is the self-service surface.
- **co-09 · software-catalog** — a catalog of services with clear ownership (Backstage-style).
- **co-10 · scaffolder-template** — templates that generate new services pre-wired with CI/deploy.
- **co-11 · self-service** — capabilities are self-serve and ticket-free.
- **co-12 · guard-rails** — safe defaults and constraints bound what self-service can do.
- **co-13 · platform-contract** — a documented interface/SLA for each platform capability.
- **co-14 · mechanism-vs-policy** — the platform supplies mechanism; teams decide policy.
- **co-15 · dora-metrics** — the DORA four keys plus reliability, measuring delivery performance.
- **co-16 · space-framework** — SPACE's five dimensions of developer productivity.
- **co-17 · leading-vs-lagging** — distinguishing leading signals from lagging outcomes.
- **co-18 · metrics-anti-weaponization** — measure the system, never rank individuals (Goodhart's law).
- **co-19 · devex** — developer experience is the outcome the platform optimizes for.
- **co-20 · platform-maturity** — build the platform only when org-wide friction is measurable (not fashion).

## Tensions & trade-offs — when NOT to reach for this

- **Platform before pain**: a dedicated platform team and an IDP are overhead that a small org cannot amortize.
  Build the platform when repeated, org-wide friction is measurable — not because "platform engineering" is
  fashionable. Prematurely, it is a team maintaining abstractions nobody needed yet.
- **Golden path vs golden cage**: an opinionated path is only a gift if it is genuinely easier and remains
  escapable. Mandate it, or make it worse than the DIY route, and teams route around it — you have added
  coupling and cognitive load instead of removing them. The paved road must win on merit.
- **Metrics as weapons (hard boundary)**: DORA/SPACE measure the delivery _system_. The moment they become
  individual performance rankings or targets, Goodhart's law takes over — people optimize the number, not the
  outcome, and the signal dies. When NOT to use them: never as a stack-ranking or a stick.

## Lineage — why it beat the alternative

- Platform engineering is the current synthesis of two prior swings. First, siloed Dev-throws-to-Ops created
  the friction DevOps set out to remove; but "you build it, you run it" pushed so much operational surface
  onto every product team that cognitive load became the new bottleneck. Platform engineering answers that by
  re-centralizing the _undifferentiated_ heavy lifting — as a self-service product, not a gatekeeping ops
  silo — so teams keep autonomy without each rebuilding the same infra. Team Topologies gave the
  organizational vocabulary (platform vs stream-aligned teams), Accelerate/DORA gave the measurement base,
  and the CNCF codified the definition. What it hands forward: the reliability and operational rigor of the
  paved road feed directly into [`94-site-reliability-engineering`](./site-reliability-engineering.md),
  where SLOs and error budgets govern the services the platform helps ship.

## Worked examples

Colocated under `platform-engineering-and-devex/learning/`; the deliverables are platform artifacts —
golden-path templates, a platform contract, and a metrics dashboard — not an application (DD-20/DD-30). Any
scaffolder/dashboard scripting in Python is fully type-annotated (DD-39). `‡ no-code` topic: the `ex-NN`
below are **decision scenarios** (a situation → the right platform-leadership call), contiguous `ex-01..ex-26`.
Every scenario cites the `co-NN` it exercises. Concepts come before scenarios.

### Foundational scenarios

- **ex-01 · platform-before-pain** — a 15-person startup wants a dedicated platform team — decide: not yet; wait for measurable, repeated org-wide friction. (co-20)
- **ex-02 · cognitive-load-audit** — a stream-aligned team is drowning in bespoke infra glue — factor the shared, undifferentiated work into the platform. (co-05, co-01)
- **ex-03 · platform-as-product-framing** — the platform is built with no user research — reframe it as a product and treat teams as customers. (co-01, co-02)
- **ex-04 · team-topologies-split** — an org reorganizes around fast flow — apply the platform vs stream-aligned team split. (co-03)
- **ex-05 · interaction-mode-collaboration** — a brand-new capability needs co-design with a pilot team — use the collaboration mode temporarily. (co-04)
- **ex-06 · interaction-mode-xaas** — a capability has matured and stabilized — shift it to X-as-a-service. (co-04)
- **ex-07 · platform-team-charter** — the platform team lacks a clear mission — charter it as a product team with an internal customer. (co-01, co-03)
- **ex-08 · platform-vs-ops-silo** — the platform is drifting into gatekeeping ops — keep it self-service, not a toll booth. (co-01, co-06)

### Golden paths & self-service scenarios

- **ex-09 · golden-path-ci-wiring** — new services keep skipping CI and containerization — provide a golden path that pre-wires CI/container/deploy. (co-06, co-10)
- **ex-10 · scaffolder-adoption** — service creation is inconsistent across teams — offer scaffolder templates from the catalog. (co-10)
- **ex-11 · golden-cage-mandate** — leadership wants to mandate the golden path — refuse the mandate; keep it opt-in and escapable. (co-07, co-06)
- **ex-12 · paved-road-worse-than-diy** — teams route around the golden path — diagnose that it must win on merit, and fix it. (co-06)
- **ex-13 · escape-hatch-design** — a power-user team needs an off-path option — design an explicit, documented escape hatch. (co-07, co-12)
- **ex-14 · self-service-db-request** — developers file tickets for every database — build a guard-railed, ticket-free self-service capability. (co-11, co-12)
- **ex-15 · guard-rail-unsafe-request** — a dev requests an oversized/insecure resource — the guard-rails block it while allowing safe defaults. (co-12)
- **ex-16 · platform-contract-define** — a capability has no documented interface — write its platform contract (inputs, defaults, SLA, escape hatch). (co-13)
- **ex-17 · mechanism-not-policy** — the platform starts dictating teams' tech choices — pull back to mechanism, leave policy to teams. (co-14)
- **ex-18 · idp-portal-decision** — buy vs build a developer portal — choose a tool-agnostic IDP with a catalog + scaffolder. (co-08, co-09)
- **ex-19 · catalog-ownership** — services have unclear owners during an incident — establish a software catalog with ownership. (co-09)
- **ex-20 · internal-customer-feedback** — adoption is low and unexplained — gather internal-customer feedback and iterate the product. (co-02, co-01)

### Metrics & DevEx scenarios

- **ex-21 · dora-baseline** — there are no delivery metrics at all — establish the DORA four keys plus reliability. (co-15)
- **ex-22 · space-beyond-dora** — DORA misses satisfaction and collaboration — add SPACE dimensions for a fuller picture. (co-16)
- **ex-23 · leading-signal-choice** — only lagging outcomes are tracked — add leading signals that predict them. (co-17)
- **ex-24 · metrics-as-stack-rank** — an exec wants to rank engineers by DORA numbers — refuse; measure the system, not individuals. (co-18)
- **ex-25 · goodhart-target** — deploy frequency has become a personal target and is being gamed — restore it as a system signal, measure the outcome. (co-18)
- **ex-26 · devex-friction-survey** — leadership asks "is developer experience good?" — run a DevEx survey plus signals rather than guessing. (co-19)

## Capstone spec — intra-topic (subject → paved golden path)

- **Goal**: design and stand up a minimal internal developer platform slice — one golden-path scaffolder that
  takes a new service from nothing to a deployed, monitored state using the topics-50/51/55 substrate; one
  self-service capability with guard-rails and an escape hatch; and a DORA/SPACE dashboard plus the policy
  that keeps it a system-measurement, not an individual scorecard.
- **Concepts exercised**: [ ] a golden-path scaffolder template (co-06, co-10) [ ] self-service infra with
  guard-rails + escape hatch (co-11, co-12, co-07) [ ] a software-catalog/portal entry (co-08, co-09) [ ] a
  DORA/SPACE dashboard (co-15, co-16, co-17) [ ] a metrics anti-weaponization policy (co-18) [ ]
  platform-as-a-product framing (internal customer + contract) (co-01, co-02, co-13).
- **Ordered steps**:
  1. `.../learning/capstone/golden-path/` — a scaffolder template producing a new service pre-wired with CI +
     container + deploy (topics 50/51/55). Verify a generated service builds and deploys with no hand-editing.
  2. `.../learning/capstone/self-service/` — one capability (e.g. database provisioning) as a guard-railed,
     self-serve building block with a documented escape hatch. Verify a developer provisions it without a
     ticket and the guard-rails block an unsafe request.
  3. `.../learning/capstone/devex-metrics/` — a DORA/SPACE dashboard from delivery signals + a written policy
     on how it may and may not be used. Verify the dashboard reflects real signals and the policy forbids
     individual ranking.
- **Acceptance criteria**: the golden path is genuinely easier than DIY and escapable; the self-service
  capability is guard-railed and ticket-free; the metrics measure the system with an explicit
  anti-weaponization policy; every piece is framed as a product for an internal customer.
- **Done bar**: the golden path produces a deployed service end-to-end + the platform contract and metrics
  policy are documented + web-verified.

## Read more

**Books**

- **Team Topologies** — Matthew Skelton, Manuel Pais (2019). The field-defining model for organizing teams
  (including platform teams) for fast flow; foundational to platform-engineering practice.
- **Platform Engineering: A Guide for Technical, Product, and People Leaders** — Camille Fournier, Ian
  Nowland (2024). The current canonical practitioner book on building internal platforms as products.
- **Accelerate** — Nicole Forsgren, Jez Humble, Gene Kim (2018). The empirical research base (DORA metrics)
  behind modern platform-engineering and developer-experience investment decisions.

**Papers & articles**

- **CNCF Platforms White Paper** — CNCF TAG App Delivery Platforms Working Group (2023). The
  industry-consensus definition and framing of internal developer platforms; free official paper.
  <https://tag-app-delivery.cncf.io/whitepapers/platforms/>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Ops, platform, quality & product — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Scale, cloud & platform ops — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 10 · Scale, cloud & platform ops.

> _Content originated in the now-closed FS-SE plan (topic 93); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
