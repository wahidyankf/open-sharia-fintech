# Domain-Driven Design (By Example, Python)

**Course ID**: `domain-driven-design` · **Format**: By Example · **Language**: Python.

**Short summary**: Bounded contexts, ubiquitous language, modeling

**Scope note**: tactical + strategic DDD as runnable code — entities, value objects, aggregates,
repositories, domain events, bounded contexts, context maps, and anti-corruption layers. The catalogue
entry lives in [`42-software-architecture`](./software-architecture.md); this is the deep, hands-on
teaching of it. Domain events connect forward to
[`45-event-driven-architecture`](./event-driven-architecture.md).

## Why this exists · the big idea

- **The problem before the solution**: code that models database tables instead of the business drifts from
  how domain experts think — the translation tax shows up as bugs, miscommunication, and rules enforced in
  the wrong place.
- **Keep-this-if-you-forget-everything**: name the code after the domain and put each invariant inside a
  single consistency boundary (an aggregate) so the rule has exactly one home and cannot be violated from
  outside.
- **Big ideas touched**: `coupling-vs-cohesion` (bounded contexts draw the seams), `taming-state`
  (an aggregate root is a consistency boundary quarantining invariant-protected state),
  `correctness-vs-pragmatism` (DDD pays off on complex domains and is overkill on simple ones).

## Prerequisites

- **Prior topics**: [topic 21 Object-Oriented Design & Patterns](./object-oriented-design-and-patterns.md)
  (encapsulation, invariants), [topic 42 Software Architecture](./software-architecture.md) (bounded
  contexts, ports), and [topic 8 Object-Oriented Programming Essentials](./object-oriented-programming-essentials.md).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** with a pinned CVE-clean test runner;
  Neovim/VSCode (DD-17). No DB required for the core — persistence is behind a repository port.
- **Assumed knowledge**: classes/invariants (topic 08/21); the idea of a domain core separated from I/O
  (topic 42); writing a unit test.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: DDD terminology (entities, value objects, aggregates/aggregate roots,
  repositories, domain events, ubiquitous language, bounded contexts, context maps, anti-corruption layer)
  is unchanged canon from Evans (2003) + Vernon's _Implementing DDD_ (2013). Vernon's four aggregate-design
  rules of thumb (protect true invariants inside consistency boundaries; small aggregates; reference other
  aggregates by identity; update others via eventual consistency) remain the canonical reference.
  (archi-lab.io / learn.microsoft.com anti-corruption-layer)

> DD-35 primary-source pass (2026-07-12). Definitions traced to Evans' own 2015 Reference PDF, Vernon's
> "Effective Aggregate Design" essay, Evans & Fowler's "Specifications" paper, and Fowler's bliki (all
> fetched and read). Unverifiable specifics flagged `[Needs Verification]`. Keep exact when drafting.

- **Ubiquitous Language** — "shared, precise communication between developers and domain experts, grounded
  in the Domain Model," coined by Evans (2003). It is **per bounded context**, not global. Source:
  [Fowler, UbiquitousLanguage](https://martinfowler.com/bliki/UbiquitousLanguage.html) (2006).
- **Entity** (Evans, DDD Reference PDF) — "When an object is distinguished by its identity, rather than its
  attributes, make this primary to its definition." **Value Object** — "When you care only about the
  attributes and logic of an element … classify it as a value object" (immutable, side-effect-free
  functions, replaceable). Source: [DDD Reference (Evans, 2015)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf).
- **Aggregate + Root** (Evans) — "Cluster the entities and value objects into aggregates and define
  boundaries around each. Choose one entity to be the root." Vernon: "aggregate is synonymous with
  **transactional consistency boundary**." Source: [Vernon, Effective Aggregate Design Part I](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_1.pdf) (2011), reviewed by Evans.
- **Vernon's four aggregate rules (verbatim intent)** — (1) "Model True Invariants In Consistency
  Boundaries"; (2) "Design Small Aggregates" — "the root entity and a minimal number of attributes … the
  ones necessary, and no more"; (3) "Reference Other Aggregates By Identity" — "prefer references … only by
  their globally unique identity, not by holding a direct object reference"; (4) "Use Eventual Consistency
  Outside the Boundary" — quoting Evans (DDD p128): "Any rule that spans AGGREGATES will not be expected to
  be up-to-date at all times." One aggregate instance modified per transaction. Sources: [Vernon Part I](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_1.pdf) & [Part II](https://kalele.io/wp-content/uploads/2019/01/DDD_COMMUNITY_ESSAY_AGGREGATES_PART_2.pdf).
- **Repository** (Evans) — "For each type of aggregate that needs global access, create a service that can
  provide the illusion of an in-memory collection." Keyed to **aggregate types**; the "one per aggregate
  root" phrasing is the standard paraphrase, `[Needs Verification]` as a verbatim Evans quote. Source:
  DDD Reference PDF; cf. [Fowler PoEAA Repository](https://martinfowler.com/eaaCatalog/repository.html).
- **Factory** (Evans) — "Shift the responsibility for creating instances of complex objects and aggregates
  to a separate object." **Domain Service** (Evans) — "When a significant process or transformation … is not
  a natural responsibility of an entity or value object, add … a standalone interface declared as a
  service." Source: DDD Reference PDF.
- **Domain Event** — "Captures the memory of something interesting which affects the domain" and can
  "trigger a change to the state of the application." Used to decouple and propagate across aggregates/
  contexts under eventual consistency. Source: [Fowler, DomainEvent](https://martinfowler.com/eaaDev/DomainEvent.html) (2005); Vernon Part II worked example (`BacklogItemCommitted`).
- **Layered Architecture** (Evans) — "Isolate the expression of the domain model and the business logic,
  and eliminate any dependency on infrastructure, user interface, or even application logic." The four
  layers (UI / Application / Domain / Infrastructure) and the "Application layer has no business rules,
  only coordinates tasks" wording is widely reported but `[Needs Verification]` as a direct book quote —
  cite Evans Ch. 4 or Vernon rather than presenting it verbatim.
- **Anticorruption Layer** (Evans) — "As a downstream client, create an isolating layer to provide your
  system with functionality of the upstream system in terms of your own domain model." One of the
  context-map relationship patterns (with Shared Kernel, Customer/Supplier, Conformist, Open Host Service,
  Published Language, Separate Ways, Partnership). Source: DDD Reference PDF (Evans, 2015).
- **Subdomains** (Evans) — Core Domain (apply top talent, "easily distinguishable from the mass of
  supporting model"), Supporting, and Generic subdomains (factored out, lower priority). Source: DDD
  Reference PDF.
- **Specification pattern** (Evans & Fowler) — "separate the statement of how to match a candidate, from the
  candidate object"; `isSatisfiedBy(anObject): Boolean`; composites combine via **and/or/not**. Source:
  [Evans & Fowler, "Specifications"](https://martinfowler.com/apsupp/spec.pdf) (undated; ~2002 — `[Needs Verification]` on exact year).
- **Anemic Domain Model (anti-pattern)** — "objects … with hardly any behavior … little more than bags of
  getters and setters … contrary to the basic idea of object-oriented design." Source: [Fowler, AnemicDomainModel](https://martinfowler.com/bliki/AnemicDomainModel.html) (2003).
- **CQRS ≠ Event Sourcing (keep independent)** — CQRS = "use a different model to update information than the
  model you use to read" (Greg Young, via [Fowler, CQRS](https://martinfowler.com/bliki/CQRS.html), 2011).
  Event Sourcing = "Capture all changes to application state as a sequence of events" ([Fowler, EventSourcing](https://martinfowler.com/eaaDev/EventSourcing.html), 2005). Commonly combined but **independent** patterns —
  teach both as intros here; deep in [`45-event-driven-architecture`](./event-driven-architecture.md).
- **When NOT to use DDD** — DDD is "particularly suited to complex domains"; invest the tactical effort on
  the **core** domain, buy/library the generic subdomains. A direct "don't use DDD for CRUD" sentence from
  Evans/Vernon is `[Needs Verification]`; Greg Young states the cost/benefit tie to complexity + ROI
  directly. Source: [Fowler, DomainDrivenDesign](https://martinfowler.com/bliki/DomainDrivenDesign.html) (2020).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · ubiquitous-language** — one precise, shared language binds domain experts, conversation, and code; it lives inside a bounded context, not globally.
- **co-02 · domain-model** — model the business behaviour, not the database tables; replace primitive obsession with domain types.
- **co-03 · entity** — an object defined by identity and continuity over time, not by its attributes.
- **co-04 · value-object** — an immutable object defined only by its attributes, compared by value, freely replaceable.
- **co-05 · side-effect-free-behaviour** — value-object methods return new values instead of mutating, keeping them safe to share.
- **co-06 · aggregate** — a cluster of entities and value objects treated as one unit with a boundary.
- **co-07 · aggregate-root** — the single entity that is the only external entry point; outside code touches children only through it.
- **co-08 · consistency-boundary** — the aggregate is the transactional consistency boundary; its invariants hold at every commit.
- **co-09 · invariant** — a business rule that must always hold; each invariant has exactly one home, inside its aggregate.
- **co-10 · small-aggregates** — Vernon's rule: design the smallest aggregate that still protects a true invariant.
- **co-11 · reference-by-identity** — an aggregate references other aggregates by identity (an id), never by holding a direct object reference.
- **co-12 · one-aggregate-per-transaction** — modify a single aggregate instance per transaction.
- **co-13 · eventual-consistency** — rules that span aggregates are reconciled asynchronously, not inside one transaction.
- **co-14 · repository** — a collection-like abstraction over aggregate persistence; one repository per aggregate root.
- **co-15 · port-and-adapter-persistence** — the repository interface is a domain-facing port; the storage implementation is an adapter outside the domain.
- **co-16 · factory** — encapsulates the creation of a complex, valid entity or aggregate.
- **co-17 · domain-service** — a stateless domain operation that belongs to no single entity or value object.
- **co-18 · domain-event** — a first-class record of something meaningful that happened in the domain.
- **co-19 · event-decoupling** — events decouple the producer from consumers and propagate change across aggregates and contexts.
- **co-20 · application-service** — the thin orchestration layer that coordinates repositories, aggregates, and events but holds no business rules.
- **co-21 · layered-architecture** — UI / Application / Domain / Infrastructure layers with dependencies pointing inward; the domain depends on nothing outer.
- **co-22 · bounded-context** — an explicit boundary within which one model and its language apply; the same word can mean different things across contexts.
- **co-23 · context-map** — the map of relationships between bounded contexts (shared kernel, customer/supplier, conformist, open-host, published language, ACL, separate ways).
- **co-24 · anticorruption-layer** — an isolating translation layer that protects a downstream model from an upstream/foreign model.
- **co-25 · shared-kernel** — a deliberately shared subset of the model between two teams/contexts.
- **co-26 · customer-supplier-conformist** — upstream/downstream integration patterns; a conformist downstream adopts the upstream model wholesale.
- **co-27 · subdomains** — core vs supporting vs generic subdomains; invest modelling effort in the core, buy or library the generic.
- **co-28 · specification** — a business rule reified as a composable predicate object (`is_satisfied_by`) combinable via and/or/not.
- **co-29 · anemic-domain-model** — the anti-pattern of data-bag objects with getters/setters and no behaviour; logic leaks into services.
- **co-30 · cqrs** — separate the write model from the read model (intro here; deep in [`45-event-driven-architecture`](./event-driven-architecture.md)).
- **co-31 · event-sourcing** — persist state as an append-only log of events and rebuild state by replay (intro here; deep in [`45-event-driven-architecture`](./event-driven-architecture.md)).
- **co-32 · when-ddd-pays-off** — DDD's tactical/strategic investment repays on complex core domains and is overkill on CRUD/generic ones.

## Tensions & trade-offs — when NOT to reach for this

- **Ceremony vs simplicity**: value objects, aggregates, repositories, and ACLs are a lot of scaffolding; on
  a CRUD app with no real invariants they add indirection and buy nothing. DDD's own answer is to apply the
  tactical patterns only where the domain is genuinely complex.
- **Aggregate boundaries**: too-large aggregates kill concurrency (everything locks the root); too-small ones
  can't protect their invariant. Vernon's "small aggregates, reference others by identity, eventual
  consistency across them" is a hard-won balance, not a default to reach for blindly.
- **When NOT to use it**: a generic/technical subdomain (a mailer, a PDF exporter) needs no ubiquitous
  language or bounded context — buy or use a library. Spend the modeling effort on the _core_ domain that
  differentiates the business.

## Lineage — why it beat the alternative

- DDD (Evans 2003) reacted to two failures: anemic data-model code that scattered business rules across
  services, and the analysis-paralysis of trying to model an entire enterprise at once. Its move was to
  align code with the domain's language and to divide the model into bounded contexts so each stays
  internally consistent — the same "boundaries so things that change together stay together" idea as
  [`42-software-architecture`](./software-architecture.md), aimed at the domain. Vernon's _Implementing
  DDD_ (2013) added the tactical rules of thumb. The domain events modeled here become the backbone of
  [`45-event-driven-architecture`](./event-driven-architecture.md).

## Worked examples

Colocated under `domain-driven-design/learning/code/` as typed, pyright-clean Python; each runnable +
unit-tested (DD-20/DD-30). Contiguous `ex-01..ex-80`. Every example cites the `co-NN` concept(s) it
exercises; concepts are taught before the examples that use them.

### Beginner

- **ex-01 · ubiquitous-language-rename** — rename `t1`/`process()` into domain terms (`booking`/`confirm()`) — verify tests read as domain sentences. (co-01)
- **ex-02 · model-vs-table** — model an `Order` by behaviour, not as a row-shaped data class — verify a method enforces a rule a table could not. (co-02)
- **ex-03 · value-object-equality** — `Money(10,"USD") == Money(10,"USD")` but `!= Money(10,"EUR")` — verify equality by value. (co-04)
- **ex-04 · value-object-immutable** — a frozen dataclass `Money` rejects attribute assignment — verify `FrozenInstanceError`. (co-04)
- **ex-05 · value-object-behaviour** — `Money.add` returns a new `Money`, leaving operands unchanged — verify no mutation. (co-05)
- **ex-06 · entity-identity** — two `Customer` objects with the same id are equal despite different names — verify identity equality. (co-03)
- **ex-07 · entity-mutable-state** — a `Customer` changes email yet keeps its identity — verify id stable across change. (co-03)
- **ex-08 · entity-vs-value-choice** — decide `Address` is a value object, `Customer` an entity — verify the equality semantics of each. (co-03, co-04)
- **ex-09 · invariant-in-constructor** — `Money` rejects an unknown currency at construction — verify `ValueError` on invalid. (co-09)
- **ex-10 · invariant-guard-method** — `Account.withdraw` refuses to overdraw — verify the balance invariant holds. (co-09)
- **ex-11 · money-value-object** — a full `Money` VO with currency + arithmetic invariants — verify mixed-currency add raises. (co-04, co-09)
- **ex-12 · email-value-object** — an `Email` VO validating format at construction — verify malformed input rejected. (co-04)
- **ex-13 · quantity-value-object** — a `Quantity` VO rejecting negatives — verify `Quantity(-1)` raises. (co-04, co-09)
- **ex-14 · daterange-value-object** — a `DateRange` VO enforcing `start < end` — verify inverted range rejected. (co-04, co-09)
- **ex-15 · value-object-composition** — an `OrderLine` composed of `ProductId` + `Quantity` + `Money` VOs — verify line total computed from VOs. (co-04)
- **ex-16 · entity-lifecycle** — an `Order` transitions `draft → placed → shipped` — verify only legal transitions allowed. (co-03)
- **ex-17 · self-validating-entity** — an `Order` refuses `ship()` before `place()` — verify illegal transition raises. (co-09)
- **ex-18 · ubiquitous-language-test** — tests named `test_customer_cannot_exceed_credit_limit` — verify names mirror domain rules. (co-01)
- **ex-19 · no-primitive-obsession** — replace `str`/`float` params with `Email`/`Money` VOs — verify type errors caught at construction not deep in logic. (co-02, co-04)
- **ex-20 · factory-simple** — a `Customer.register` factory builds a valid entity — verify it returns a ready-to-use `Customer`. (co-16)
- **ex-21 · factory-aggregate** — an `Order.create` factory assembles a root plus initial lines — verify the aggregate is valid on return. (co-16, co-06)
- **ex-22 · domain-service-transfer** — a `MoneyTransfer` domain service moves funds across two `Account`s — verify both balances update atomically. (co-17)
- **ex-23 · domain-service-vs-method** — decide cross-account transfer is a service, not an `Account` method — verify neither account "owns" the operation. (co-17)
- **ex-24 · anemic-vs-rich** — contrast an anemic `Order` (getters/setters + service) with a behaviour-rich one — verify the rich model localizes the rule. (co-29)
- **ex-25 · anemic-antipattern-fix** — move a total-calculation rule out of a service into the `Order` root — verify the service now only orchestrates. (co-29)
- **ex-26 · specification-predicate** — a `PremiumCustomerSpec.is_satisfied_by(customer)` predicate — verify true/false on sample customers. (co-28)
- **ex-27 · specification-compose** — combine specs via `&`/`|`/`~` into a composite — verify the composite matches expected members. (co-28)
- **ex-28 · specification-select** — filter a list with a spec — verify only satisfying elements returned. (co-28)

### Intermediate

- **ex-29 · aggregate-boundary** — an `Order` aggregate clusters its `OrderLine` children — verify lines are reachable only via the order. (co-06)
- **ex-30 · aggregate-root-access** — add a line only through `Order.add_line`, not by mutating the list — verify direct list mutation is blocked. (co-07)
- **ex-31 · aggregate-invariant-across-children** — `Order` enforces `total <= credit_limit` across all lines — verify adding an over-limit line raises. (co-09, co-06)
- **ex-32 · consistency-boundary** — one commit persists a whole `Order` aggregate atomically — verify partial state never stored. (co-08)
- **ex-33 · small-aggregate** — split a bloated `Customer`-with-orders aggregate into `Customer` + `Order` — verify each protects its own invariant. (co-10)
- **ex-34 · reference-by-identity** — `Order` holds a `CustomerId`, not a `Customer` object — verify the order needs no customer instance to exist. (co-11)
- **ex-35 · one-aggregate-per-transaction** — a use case modifies only one aggregate and defers the other — verify the second update is queued, not inline. (co-12)
- **ex-36 · eventual-consistency-across-aggregates** — updating `Inventory` after `Order` placement happens via an event — verify inventory converges after handling. (co-13)
- **ex-37 · repository-port** — a `Repository` `Protocol` with `add`/`get`/`next_id` — verify the domain depends only on the protocol. (co-14, co-15)
- **ex-38 · repository-in-memory-adapter** — an in-memory dict-backed `OrderRepository` — verify round-trip add/get. (co-15)
- **ex-39 · repository-one-per-root** — separate `OrderRepository` and `CustomerRepository` — verify each keys on its own root. (co-14)
- **ex-40 · repository-collection-illusion** — `repo.add`/`repo[id]` feel like an in-memory collection — verify the collection semantics. (co-14)
- **ex-41 · repository-swap-adapter** — swap the in-memory adapter for a fake-SQL adapter behind the same port — verify the domain code is unchanged. (co-15)
- **ex-42 · aggregate-reconstitution** — the repository rebuilds a full `Order` aggregate from stored rows — verify reconstituted invariants hold. (co-16, co-14)
- **ex-43 · domain-event-define** — an `OrderPlaced` frozen event dataclass — verify it carries `order_id` + `occurred_at`. (co-18)
- **ex-44 · domain-event-raise** — `Order.place` records an `OrderPlaced` on the aggregate — verify the event appears in `order.pending_events`. (co-18)
- **ex-45 · domain-event-payload** — the event carries the right identities and amounts — verify payload matches the transition. (co-18)
- **ex-46 · domain-event-dispatch** — a handler subscribed to `OrderPlaced` runs on publish — verify the handler side effect fires. (co-19)
- **ex-47 · domain-event-decouple** — the `Order` root does not import or know its consumers — verify producer has no handler reference. (co-19)
- **ex-48 · domain-event-cross-aggregate** — an `OrderPlaced` handler decrements `Inventory` — verify the second aggregate updates through the event. (co-19, co-13)
- **ex-49 · application-service-orchestrate** — a `place_order` app service loads a repo, calls the root, saves, publishes events — verify end-to-end flow. (co-20)
- **ex-50 · application-vs-domain-service** — the app service holds no business rule; the rule lives in the aggregate — verify moving a rule into the service is a smell. (co-20, co-17)
- **ex-51 · layered-architecture** — package into `domain`/`application`/`infrastructure` with inward deps — verify an import-lint forbids domain→infra. (co-21)
- **ex-52 · domain-core-no-infra** — assert the `domain` package imports no db/http module — verify via an AST/import test. (co-21)
- **ex-53 · aggregate-root-invariant-guard** — external code cannot bypass the credit-limit invariant — verify tampering with a child raises or is impossible. (co-07, co-09)
- **ex-54 · aggregate-collection-encapsulation** — `Order.lines` returns a read-only view — verify callers cannot append to it. (co-07)
- **ex-55 · factory-vs-constructor** — a factory for a complex `Order`, a plain constructor for a `Money` VO — verify the split matches complexity. (co-16)
- **ex-56 · specification-in-repository** — pass a `Specification` to `repo.matching(spec)` — verify only matching aggregates returned. (co-28, co-14)

### Advanced

- **ex-57 · bounded-context-define** — a `sales` `Customer` and a `shipping` `Customer` are different models — verify each has only its context's fields. (co-22)
- **ex-58 · bounded-context-model-drift** — "Product" carries price in `sales`, weight in `shipping` — verify the two models don't share a class. (co-22)
- **ex-59 · context-map-relationships** — encode a context map as a typed structure (upstream/downstream pairs) — verify it lists the relationship kind per edge. (co-23)
- **ex-60 · anticorruption-layer** — an ACL translates a legacy `LegacyCustomerDTO` into the domain `Customer` — verify the domain never sees the DTO. (co-24)
- **ex-61 · acl-isolation** — neither context imports the other's model class — verify via an import test. (co-24)
- **ex-62 · acl-translation-map** — the ACL maps upstream field names to domain VOs — verify a field-by-field translation table. (co-24)
- **ex-63 · shared-kernel** — a `Money` VO shared by `billing` and `payroll` contexts — verify both import the one shared type. (co-25)
- **ex-64 · customer-supplier** — `orders` (upstream) publishes what `shipping` (downstream) needs — verify downstream consumes the agreed contract. (co-26)
- **ex-65 · conformist** — a downstream context adopts an upstream payment provider's model as-is — verify no translation layer exists (contrast ex-60). (co-26)
- **ex-66 · open-host-published-language** — expose a versioned published-language DTO at a context edge — verify external callers bind to the DTO, not the domain. (co-23)
- **ex-67 · subdomain-core** — identify `pricing` as the core domain of a retail system — verify it gets the richest model. (co-27)
- **ex-68 · subdomain-supporting-generic** — classify `notifications` as generic, `catalog` as supporting — verify the generic one is a thin wrapper. (co-27)
- **ex-69 · core-domain-focus** — invest tactical modelling in the core, library the generic — verify effort concentrated on the core aggregate. (co-27, co-32)
- **ex-70 · when-ddd-overkill** — a CRUD address-book where DDD adds only ceremony — verify a plain data class suffices. (co-32)
- **ex-71 · cqrs-read-write-split** — a write model (`Order` aggregate) separate from a read model (`OrderSummary`) — verify writes go through the aggregate, reads through the summary. (co-30)
- **ex-72 · cqrs-read-model** — a denormalized `OrderSummary` projection built for a query — verify it answers a query with no aggregate load. (co-30)
- **ex-73 · event-sourcing-append** — persist `Order` state as an append-only event list, not a row — verify no state overwrite occurs. (co-31)
- **ex-74 · event-sourcing-replay** — rebuild an `Order` by folding its event stream — verify replayed state matches the live aggregate. (co-31)
- **ex-75 · event-sourcing-audit** — the event log answers "who changed what, when" — verify the history is reconstructable from events. (co-31)
- **ex-76 · domain-to-integration-event** — a `domain` `OrderPlaced` maps to a cross-context integration event — verify the integration event drops internal fields. (co-19, co-22)
- **ex-77 · aggregate-across-contexts** — a `shipping` `Shipment` references a `sales` order by `OrderId` — verify no cross-context object reference. (co-11, co-22)
- **ex-78 · ubiquitous-language-per-context** — "account" means login in `identity`, ledger in `billing` — verify each context's tests use its own meaning. (co-01, co-22)
- **ex-79 · specification-business-rule** — a composite `EligibleForDiscount` spec (loyal AND large-order AND NOT delinquent) — verify it matches only qualifying customers. (co-28)
- **ex-80 · ddd-domain-model** — assemble orders + inventory: VOs, an `Order` aggregate root, a repository port + adapter, domain events, two bounded contexts, and an ACL — verify invariants hold through the root, the core imports no infra, events fire, and the ACL isolates contexts. (co-04, co-07, co-14, co-18, co-22, co-24)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: model one non-trivial domain (e.g. orders/inventory) with proper DDD tactical patterns —
  value objects, an aggregate root that enforces its invariants, a repository port with an in-memory
  adapter, domain events on key transitions — and split it into two bounded contexts connected by an
  anti-corruption layer, all unit-tested with the domain core free of infrastructure.
- **Concepts exercised**: [ ] value objects (co-04, co-05) [ ] an aggregate root + invariant (co-06,
  co-07, co-08, co-09) [ ] a repository port + in-memory adapter (co-14, co-15) [ ] domain events (co-18,
  co-19) [ ] two bounded contexts (co-22, co-23) [ ] an ACL translating between them (co-24) [ ] a domain
  core free of infrastructure (co-21).
- **Ordered steps**:
  1. `.../learning/capstone/code/domain/` — value objects + an entity with identity. Verify value equality
     and an invariant rejection via unit tests.
  2. Add an aggregate root enforcing an invariant across children + a repository port. Verify the invariant
     holds through the root and the port has an in-memory adapter.
  3. Emit domain events on key transitions. Verify the right event fires with the right payload on each
     transition.
  4. Split into two bounded contexts + an ACL translating one context's model to the other. Verify the ACL
     maps correctly and neither context leaks the other's model.
- **Acceptance criteria**: aggregate invariants cannot be violated through the root; the domain core imports
  no infrastructure; events fire correctly; the ACL isolates the two contexts; all unit tests green.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Domain-Driven Design: Tackling Complexity in the Heart of Software** — Eric Evans (2003). The original book that coined DDD and its vocabulary (bounded context, aggregate, ubiquitous language).
- **Implementing Domain-Driven Design** — Vaughn Vernon (2013). The standard practical/tactical companion showing how to apply Evans's strategic patterns in real codebases.
- **Domain-Driven Design Distilled** — Vaughn Vernon (2016). Concise, widely recommended on-ramp to strategic DDD concepts.

**Papers & articles**

- **Domain-Driven Design Reference** — Eric Evans (2015). Free, author-published summary of every pattern and definition from the original book, under Creative Commons. <https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf>
- **Bounded Context** — Martin Fowler (2014). The widely cited bliki explanation of DDD's central strategic-design concept. <https://martinfowler.com/bliki/BoundedContext.html>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Architecture, distributed & internals builds — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Architecture, distributed & internals builds — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 7 · Networking, architecture & distributed systems.

> _Content originated in the now-closed FS-SE plan (topic 43); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
