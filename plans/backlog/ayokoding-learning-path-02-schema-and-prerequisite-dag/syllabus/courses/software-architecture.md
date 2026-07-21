# Software Architecture (Annotated-concept, Python)

**Course ID**: `software-architecture` · **Format**: Annotated-concept · **Language**: Python.

**Short summary**: Architectural styles, tradeoffs, structuring

**Scope note**: architectural styles and the trade-off thinking behind them — layered, hexagonal
(ports-and-adapters), functional core/imperative shell, monolith vs microservices — plus quality
attributes, boundaries/modularity, C4 documentation, and evolutionary architecture. Event-driven has its
own topic ([`45-event-driven-architecture`](./event-driven-architecture.md)); tactical DDD is
catalogued here and taught deeply in [`43-domain-driven-design`](./domain-driven-design.md). `*`:
Python where code appears, else annotated C4 diagrams.

## Why this exists · the big idea

- **The problem before the solution**: past a certain size, a system's cost is dominated not by any one
  module but by how the modules depend on each other — the wrong boundaries make every change ripple.
- **Keep-this-if-you-forget-everything**: architecture is the deliberate placement of boundaries so that
  things that change together live together and things that don't are decoupled — you are buying
  changeability, and every boundary costs indirection.
- **Big ideas touched**: `coupling-vs-cohesion` (the fundamental lever), `layering-and-leaks`
  (layered/hexagonal styles are about honest boundaries that don't leak), `abstraction-and-its-cost`
  (each boundary buys isolation and charges indirection).

## Prerequisites

- **Prior topics**: [topic 21 Object-Oriented Design & Patterns](./object-oriented-design-and-patterns.md)
  (coupling/cohesion, DIP), [topic 23 Functional Programming](./functional-programming.md) (functional
  core/imperative shell), and a built app from Pass 1/3 (e.g.
  [topic 39 Backend at Scale](./backend-at-scale.md)) to reason about.
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** for the ports-and-adapters code; a
  Markdown/Mermaid editor for C4 diagrams and ADRs (Neovim per DD-17).
- **Assumed knowledge**: dependency inversion and interfaces (topic 21); the idea of separating a domain
  core from I/O (topic 23); reading a system diagram.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the C4 model (Context/Container/Component/Code, Simon Brown), hexagonal /
  ports-and-adapters (Cockburn 2005), strangler-fig (Fowler), and fitness functions (_Building Evolutionary
  Architectures_, 2017) are stable unchanged canonical terminology — no revision. (c4model.com)
- 2026-07-12 — verified (evolving-discourse flag): microservices-vs-monolith is a genuinely evolving debate,
  not a settled fact (e.g. Amazon Prime Video's 2023 move away from microservices). The file's trade-off
  framing is fine; content drafted here should reflect the current "boring / modular-monolith-first"
  counter-narrative, not an unqualified "microservices are the scale answer." (industry sources)

> DD-35 primary-source pass (2026-07-12). Every citation traces to a source the author fetched and
> read; unverifiable specifics flagged `[Needs Verification]`, never guessed. Keep exact when drafting.

- **Definition (two distinct authors)** — Ralph Johnson (via Fowler): "Architecture is about the important
  stuff. Whatever that is." Grady Booch: "the significant design decisions that shape a system, where
  significant is measured by cost of change." These are **two separate primaries**, not one Fowler quote.
  Sources: [Fowler, "Who Needs an Architect?"](https://martinfowler.com/ieeeSoftware/whoNeedsArchitect.pdf) (IEEE Software, 2003); Booch, "On Architecture" (2006).
- **Layered architecture** — presentation/business/persistence/database; "layers of isolation" (a change in
  one layer doesn't ripple); the **sinkhole anti-pattern** = requests passing through layers with little
  logic (80/20 diagnostic). Source: [Mark Richards, _Software Architecture Patterns_](https://www.oreilly.com/content/software-architecture-patterns/) (O'Reilly, 2015).
- **Hexagonal (Ports & Adapters)** — "allow an application to equally be driven by users, programs,
  automated test or batch scripts, and to be developed and tested in isolation from its eventual run-time
  devices and databases"; rule: "code pertaining to the inside part should not leak into the outside part."
  Source: [Cockburn, Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) (2005, v0.9).
- **Clean / Onion Architecture** — Martin's Dependency Rule: "Source code dependencies can only point
  inwards" (Entities → Use Cases → Interface Adapters → Frameworks). Palermo's Onion (2008, predates Clean):
  "all code can depend on layers more central, but code cannot depend on layers further out." Sources:
  [Martin, The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) (2012); [Palermo, Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/) (2008).
- **Coupling metric** — Stable Dependencies Principle "Depend in the direction of stability"; instability
  `I = Ce / (Ca + Ce)` (0 = maximally stable, 1 = maximally unstable). Source: R.C. Martin (SDP / _Clean
  Architecture_). Constantine & Yourdon's original coupling/cohesion (_Structured Design_, 1979) is
  `[Needs Verification]` (not directly fetched).
- **Dependency Inversion Principle** — "High-level modules should not depend on low-level modules. Both
  should depend on abstractions. Abstractions should not depend on details. Details should depend on
  abstractions." Source: R.C. Martin, DIP (_C++ Report_ 1996 / _Agile PPP_ 2002).
- **Quality attributes / ATAM** — quality attributes are "the properties of a system that stakeholders use
  to judge its quality"; ATAM is the SEI's structured method "for understanding the tradeoffs inherent in
  the architectures." Sources: Bass, Clements & Kazman, _Software Architecture in Practice_ (SEI);
  [SEI ATAM](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/). The exact
  attribute chapter-list and the ASR term's sole origin are `[Needs Verification]`.
- **First Law** — "Everything in software architecture is a trade-off"; corollary "if you think you've found
  something that isn't a trade-off, you just haven't identified the trade-off yet." Source: Richards & Ford,
  _Fundamentals of Software Architecture_ (O'Reilly, 2020).
- **Conway's Law (quote precisely)** — Conway's own words: **"Any organization that designs a system … will
  produce a design whose structure is a copy of the organization's communication structure."** Quote this,
  not the looser "organizations design systems that mirror their communication structure" paraphrase.
  Source: [Conway, "How Do Committees Invent?"](https://www.melconway.com/Home/Conways_Law.html) (_Datamation_, 1968).
- **C4 model** — four levels **Context / Container / Component / Code**, notation- and tool-independent.
  Source: [c4model.com](https://c4model.com/) (Simon Brown).
- **4+1 views** — Logical, Process, Development, Physical, + Scenarios (the "+1" validates the other four).
  Source: Kruchten, "Architectural Blueprints — The '4+1' View Model" (_IEEE Software_, 1995).
- **ADR** — sections Title / Status / Context / Decision / Consequences; ~1–2 pages; consequences include
  "all outcomes, not just the positive ones." Source: [Nygard, Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) (2011).
- **Evolutionary architecture** — "an architectural fitness function provides an objective integrity
  assessment of some architectural characteristic(s)." Source: Ford, Parsons & Kua, _Building Evolutionary
  Architectures_ (O'Reilly, 2017); [Fowler foreword](https://martinfowler.com/articles/evo-arch-forward.html).
- **CAP / PACELC** — CAP proven by Gilbert & Lynch (2002); Brewer's 2012 retrospective: the "2 of 3" framing
  is misleading — partition tolerance must be handled, and the real trade-off **during a partition is C vs
  A**. PACELC (Abadi 2012) adds: else (no partition) latency vs consistency. Sources: Gilbert & Lynch,
  "Brewer's Conjecture…" (_SIGACT News_, 2002); Brewer, "CAP Twelve Years Later" (_IEEE Computer_, 2012).
- **Twelve-Factor App** — I Codebase, II Dependencies, III Config, IV Backing services, V Build/release/run,
  VI Processes, VII Port binding, VIII Concurrency, IX Disposability, X Dev/prod parity, XI Logs, XII Admin
  processes. Source: [12factor.net](https://12factor.net/) (Adam Wiggins, Heroku).
- **Big Ball of Mud / No Silver Bullet** — BBoM = "a haphazardly structured, sprawling, sloppy, duct-tape and
  bailing wire" system ([Foote & Yoder, 1997/1999](https://www.laputan.org/mud/)). Brooks: the hard part is
  the **essential** complexity (the conceptual construct), not the **accidental**; "there is inherently no
  silver bullet" ([Brooks, "No Silver Bullet"](https://worrydream.com/refs/Brooks_1986_-_No_Silver_Bullet.pdf), 1986).
- **"Distributed monolith"** — a widely-used community term (independently-deployed services that must ship/
  fail together); no single primary coiner — present as community-coined, `[Needs Verification]` on attribution.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Annotated-concept topic). Each example below cites the co-NN it exercises. -->

- **co-01 · architecture-definition** — architecture is the significant/hard-to-change decisions ("the important stuff"; "significant = cost of change").
- **co-02 · coupling-cohesion** — the fundamental lever: keep things that change together together (cohesion) and decouple things that don't; afferent/efferent coupling.
- **co-03 · dependency-direction-dip** — pointing dependencies at abstractions, not details; the Dependency Inversion Principle applied at architecture scale.
- **co-04 · stable-dependencies** — depending in the direction of stability; the instability metric `I = Ce/(Ca+Ce)` and stable-abstractions.
- **co-05 · architectural-styles** — the catalogue of styles (layered, hexagonal, event-driven, pipe-and-filter, microkernel) as reusable structures.
- **co-06 · layered-architecture** — presentation/business/persistence/database layers with layers-of-isolation.
- **co-07 · layered-sinkhole** — the sinkhole anti-pattern: requests passing through layers with little logic.
- **co-08 · hexagonal-ports-adapters** — isolating the application core from external actors behind ports and adapters (Cockburn).
- **co-09 · functional-core-imperative-shell** — a pure, I/O-free domain core wrapped by an imperative shell that does the effects.
- **co-10 · clean-onion-architecture** — the dependency rule: source dependencies point only inward, toward the domain.
- **co-11 · quality-attributes** — the "-ilities" (modifiability, scalability, availability, performance, security) and architecturally-significant requirements.
- **co-12 · tradeoff-first-law** — "everything in software architecture is a trade-off"; every boundary buys isolation and charges indirection.
- **co-13 · atam** — the Architecture Tradeoff Analysis Method for reasoning about competing quality attributes and risks.
- **co-14 · monolith-vs-microservices** — the trade-offs of independent deploy/scale vs distributed failure, and the distributed-monolith anti-pattern.
- **co-15 · modular-monolith** — enforcing module boundaries inside one deployable, the modular-monolith-first counter-narrative.
- **co-16 · bounded-context-boundary** — a DDD bounded context as an architectural boundary with its own model.
- **co-17 · conways-law** — a system's structure tends to copy the organization's communication structure.
- **co-18 · c4-model** — the Context / Container / Component / Code diagram hierarchy for communicating architecture.
- **co-19 · 4plus1-views** — the logical / process / development / physical views plus scenarios that validate them.
- **co-20 · adr** — Architecture Decision Records (title / status / context / decision / consequences) capturing why a decision was made.
- **co-21 · evolutionary-architecture-fitness-functions** — automated, objective checks that guard an architectural characteristic over time.
- **co-22 · strangler-fig** — incrementally replacing a legacy system behind a facade rather than a big-bang rewrite.
- **co-23 · cap-pacelc** — CAP's consistency-vs-availability choice during a partition, and PACELC's else-latency-vs-consistency.
- **co-24 · twelve-factor** — the twelve-factor principles (config, backing services, disposability, logs, dev/prod parity) for cloud-native apps.
- **co-25 · big-ball-of-mud** — the haphazardly-structured anti-pattern and the boundary-drawing remedy.
- **co-26 · essential-vs-accidental-complexity** — Brooks's distinction: the irreducible conceptual complexity vs the incidental, tooling-imposed kind.
- **co-27 · cross-cutting-concerns** — config, logging, error handling, and transactions that span boundaries and need deliberate placement.

## Tensions & trade-offs — when NOT to reach for this

- **Microservices vs monolith**: microservices buy independent deploy/scale and charge network failure,
  distributed debugging, and operational overhead. The 2020s counter-narrative (modular-monolith-first;
  Amazon Prime Video's 2023 re-consolidation) is that most teams pay the distributed tax without needing it.
  Start modular-monolith; split only at a proven scaling or team-boundary seam.
- **Hexagonal everywhere**: ports-and-adapters buys testability and swappable infra and charges indirection.
  Wrapping a trivial CRUD app in ports is ceremony — apply it where the core is genuinely worth protecting.
- **When NOT to invest**: for a small, short-lived, or well-understood system, heavy architecture is
  speculative generality (YAGNI). Architecture earns its cost at scale, longevity, and team size.

## Lineage — why it beat the alternative

- Architecture patterns are reactions to the pain of large-system _change_. Layered architecture answered
  spaghetti; hexagonal (Cockburn 2005) answered business logic entangled with frameworks and the DB;
  microservices (2010s) answered monolith deploy-coupling at org scale; evolutionary architecture / fitness
  functions (2017) answered big-upfront-design failing against change. Each generation traded one rigidity
  for a new cost, and the pendulum is mid-swing back toward modular monoliths — so read the _current_
  pressure rather than cargo-culting the last era's answer. The tactical detail lives in
  [`43-domain-driven-design`](./domain-driven-design.md); the runtime-decoupled style in
  [`45-event-driven-architecture`](./event-driven-architecture.md).

## Worked examples

Colocated under `software-architecture/learning/`; each example is either a runnable, type-annotated
`pyright`-clean Python snippet (ports-and-adapters, fitness functions) or an annotated artifact (a C4
Mermaid diagram, an ADR, a quality-attribute table) per the `*` designation (DD-20/DD-30/DD-34/DD-39).
Contiguous `ex-01..ex-52`. Every example cites the `co-NN` it exercises; every concept above is
exercised by ≥ 1 example.

### Beginner

- **ex-01 · coupling-count** — measure a module's afferent/efferent coupling in Python — verify the counts match its imports. (co-02)
- **ex-02 · instability-metric** — compute `I = Ce/(Ca+Ce)` for two modules — verify the more-depended-on module is more stable. (co-04)
- **ex-03 · cohesion-smell** — a low-cohesion class vs a refactored high-cohesion pair — verify the split raises cohesion. (co-02)
- **ex-04 · dip-invert-dependency** — invert a concrete dependency behind an interface — verify the high-level module no longer imports the low-level one. (co-03)
- **ex-05 · architecture-definition-note** — an annotated artifact contrasting the Johnson and Booch definitions — verify both are attributed correctly. (co-01)
- **ex-06 · styles-catalogue-diagram** — a diagram cataloguing four architectural styles — verify each style's shape is distinct. (co-05)
- **ex-07 · layered-diagram** — a C4 diagram of a four-layer architecture — verify the layer stack and allowed dependencies. (co-06)
- **ex-08 · layered-isolation** — change the persistence layer without touching presentation — verify presentation code is unedited. (co-06)
- **ex-09 · sinkhole-antipattern** — a pass-through layer plus the 80/20 diagnostic note — verify the layer adds no logic. (co-07)
- **ex-10 · hexagonal-port-define** — define a port interface (Python `Protocol`) — verify the core depends only on the port. (co-08)
- **ex-11 · hexagonal-adapter** — an adapter implementing the port — verify it satisfies the port's contract. (co-08)
- **ex-12 · hexagonal-diagram** — a C4 diagram of the hexagon (core + ports + adapters) — verify the core sits inside the ports. (co-08)
- **ex-13 · functional-core-pure** — a pure domain function with no I/O — verify it is deterministic and side-effect-free. (co-09)
- **ex-14 · imperative-shell** — the shell doing I/O around the pure core — verify all effects live in the shell. (co-09)
- **ex-15 · quality-attribute-table** — an artifact listing the system's -ilities — verify each attribute has a concrete measure. (co-11)
- **ex-16 · asr-identify** — identify the architecturally-significant requirements from a set — verify the non-significant ones are excluded. (co-11)
- **ex-17 · conways-law-note** — map an org chart onto a system structure — verify the mirrored boundaries. (co-17)
- **ex-18 · c4-context-diagram** — a C4 Level-1 Context diagram — verify external actors and system boundary. (co-18)

### Intermediate

- **ex-19 · c4-container-diagram** — a C4 Level-2 Container diagram — verify each deployable unit and its tech. (co-18)
- **ex-20 · c4-component-diagram** — a C4 Level-3 Component diagram — verify components within one container. (co-18)
- **ex-21 · 4plus1-views** — the five 4+1 views for one system — verify each view answers its own question. (co-19)
- **ex-22 · adr-template** — an ADR with title/status/context/decision/consequences — verify all five sections are present. (co-20)
- **ex-23 · adr-tradeoff-sync-async** — an ADR analysing sync vs async integration — verify the consequences name both upsides and downsides. (co-20, co-12)
- **ex-24 · tradeoff-first-law-note** — apply "everything is a trade-off" to one decision — verify the hidden trade-off is named. (co-12)
- **ex-25 · atam-scenario** — an ATAM-style quality-attribute scenario with a sensitivity point — verify the risk is identified. (co-13)
- **ex-26 · monolith-diagram** — a C4 diagram of a monolith — verify one deployable, internal modules. (co-14)
- **ex-27 · microservices-diagram** — the same system as microservices — verify service boundaries and network hops. (co-14)
- **ex-28 · distributed-monolith-smell** — a microservices split that must ship together — verify the anti-pattern (shared release). (co-14)
- **ex-29 · modular-monolith** — a modular monolith with enforced package boundaries — verify modules communicate only through public interfaces. (co-15)
- **ex-30 · module-boundary-enforce** — a check that a module doesn't import another's internals — verify the check fails on a violation. (co-15, co-02)
- **ex-31 · bounded-context-map** — a context map with two bounded contexts — verify the relationship (e.g. anticorruption layer) between them. (co-16)
- **ex-32 · clean-architecture-layers** — an entities/use-cases/adapters/frameworks diagram — verify the concentric layering. (co-10)
- **ex-33 · dependency-rule-check** — verify inner layers import no outer layer in Python — verify a violation is caught. (co-10, co-03)
- **ex-34 · cross-cutting-logging** — a logging concern applied across boundaries via a decorator/middleware — verify it wraps handlers uniformly. (co-27)
- **ex-35 · cross-cutting-transaction** — a transaction spanning a boundary — verify commit/rollback is atomic across the seam. (co-27)
- **ex-36 · config-as-concern** — externalized config (12-factor III) — verify config comes from the environment, not code. (co-27, co-24)
- **ex-37 · twelve-factor-audit** — audit an app against the twelve factors — verify each factor is pass/fail with evidence. (co-24)
- **ex-38 · cap-tradeoff-note** — a CAP C-vs-A choice under partition for a design — verify the chosen behaviour during a partition. (co-23)

### Advanced

- **ex-39 · pacelc-note** — a PACELC else-latency-vs-consistency framing — verify the no-partition trade-off is stated. (co-23)
- **ex-40 · fitness-function-code** — an automated fitness function checking a dependency rule (Python test) — verify it fails on a rule violation. (co-21)
- **ex-41 · fitness-function-cycle-check** — a fitness function detecting a package import cycle — verify it flags an introduced cycle. (co-21, co-02)
- **ex-42 · strangler-fig-plan** — a strangler-fig migration plan with before/after diagrams — verify the incremental cutover steps. (co-22)
- **ex-43 · strangler-fig-facade** — a facade routing old vs new during migration (Python) — verify traffic shifts without a big-bang switch. (co-22)
- **ex-44 · big-ball-of-mud-diagnose** — diagnose a tangled system and recommend a boundary — verify the mud symptoms and the remedy. (co-25)
- **ex-45 · essential-vs-accidental** — classify a design's complexity as essential or accidental (Brooks) — verify each is labelled with a reason. (co-26)
- **ex-46 · ports-adapters-swap** — swap a SQL adapter for an in-memory one with no core change (runnable Python) — verify the core code is unedited and both pass. (co-08, co-09)
- **ex-47 · hexagonal-test-in-isolation** — test the core with a fake adapter — verify the test needs no real infrastructure. (co-08)
- **ex-48 · stable-abstractions** — a stable module is abstract, an unstable one concrete — verify the stable-abstractions alignment. (co-04)
- **ex-49 · style-selection-tradeoff** — pick a style for a scenario with justification — verify the choice names its trade-off. (co-05, co-12)
- **ex-50 · quality-attribute-tradeoff** — show improving one -ility costs another (e.g. security vs performance) — verify the tension is measured. (co-11, co-12)
- **ex-51 · architecture-review-adr-set** — a set of ADRs documenting a system's key decisions — verify each decision is traceable. (co-20)
- **ex-52 · rearchitect-capstone** — re-architect a tangled service to ports-and-adapters with a functional core, plus C4 diagrams and an ADR — verify the core is infrastructure-free and adapters are interchangeable. (co-08, co-09, co-03, co-20)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: take a small tangled service and re-architect it to ports-and-adapters with a functional core:
  isolate the domain from infrastructure behind ports, provide two interchangeable adapters (e.g. SQL vs
  in-memory), document the before/after with C4 diagrams, and record an ADR for the key trade-off — a
  runnable proof that the core is infrastructure-free.
- **Concepts exercised**: [ ] ports-and-adapters boundary (co-08) [ ] functional core / imperative shell
  (co-09) [ ] DIP — core depends on abstractions (co-03) [ ] two interchangeable adapters (co-08) [ ] C4
  before/after diagrams (co-18) [ ] an ADR (co-20).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — the tangled baseline + a characterization test. Verify the test pins
     current behavior.
  2. Extract ports (interfaces) and move the domain into an infrastructure-free core. Verify the core
     imports no I/O module and the test stays green.
  3. Provide two adapters (SQL + in-memory) behind the same port. Verify swapping the adapter changes no
     core code and both pass the test.
  4. `architecture.md` — before/after C4 (context + container + component) Mermaid + an ADR for the key
     decision. Verify the diagrams match the code and the ADR states context/decision/consequences.
- **Acceptance criteria**: the domain core is provably free of infrastructure imports; adapters are
  interchangeable without core edits; C4 diagrams and the ADR match the implementation.
- **Done bar**: runnable end-to-end (adapter swap) + produces the C4/ADR artifacts + web-verified.

## Read more

**Books**

- **Software Architecture in Practice** — Len Bass, Paul Clements, Rick Kazman (4th ed., 2021). The foundational SEI textbook defining quality attributes and architecture as an engineering discipline.
- **Documenting Software Architectures: Views and Beyond** — Paul Clements et al. (2nd ed., 2010). The standard reference for the multi-view approach to architecture documentation.
- **Fundamentals of Software Architecture** — Mark Richards, Neal Ford (2020). Widely adopted modern survey of architectural styles and architectural thinking.
- **Clean Architecture** — Robert C. Martin (2017). Influential synthesis of dependency-inversion-centric architecture principles.

**Papers & articles**

- **Architectural Blueprints — The "4+1" View Model of Software Architecture** — Philippe Kruchten (1995), IEEE Software. Introduced the multi-view approach to describing architecture that underlies most modern architecture documentation practice. <https://dl.acm.org/doi/10.1109/52.469759>
- **Documenting Architecture Decisions** — Michael Nygard (2011). The blog post that originated the Architecture Decision Record (ADR) format now standard across the industry. <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Architecture, distributed & internals builds — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Architecture, distributed & internals builds — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 7 · Networking, architecture & distributed systems.

> _Content originated in the now-closed FS-SE plan (topic 42); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
