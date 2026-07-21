# Object-Oriented Design and Patterns (By Example, Python)

**Course ID**: `object-oriented-design-and-patterns` · **Format**: By Example · **Language**: Python.

**Short summary**: SOLID, design patterns, refactoring toward them

**Scope note**: deep object-oriented **design** — SOLID, coupling/cohesion, and the essential Gang-of-Four
patterns — each taught as a code smell → refactor. The OO **mechanics** (classes, inheritance,
polymorphism) are prerequisites from
[`08-object-oriented-programming-essentials`](./object-oriented-programming-essentials.md); this topic
is about designing well with them. Domain modeling at scale continues in
[`43-domain-driven-design`](./domain-driven-design.md).

## Why this exists · the big idea

- **The problem before the solution**: OO mechanics let you build classes; they don't stop you building a
  rigid tangle where every change ripples outward. Design is what keeps a growing system **soft** —
  changeable without fear.
- **Keep-this-if-you-forget-everything**: depend on abstractions, not concretions, and put each
  responsibility where change is isolated — most patterns are just named tactics for that one move.
- **Big ideas touched**: `coupling-vs-cohesion` (the core lens), `abstraction-and-its-cost` (an interface
  buys pluggability and charges indirection), `taming-state` (encapsulation as a state-containment
  strategy).

## Prerequisites

- **Prior topics**: [topic 8 Object-Oriented Programming Essentials](./object-oriented-programming-essentials.md)
  (classes, inheritance, polymorphism, composition) and [topic 4 Just Enough Python](./just-enough-python.md).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x**; `pytest` to lock refactors behind tests.
- **Assumed knowledge**: writing Python classes; the difference between composition and inheritance;
  reading/writing a basic unit test (topic 15 helps but is not required).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the GoF catalogue of 23 patterns dates to 1994 and is unchanged canon; SOLID is
  distinct and later — Robert Martin distilled the five principles across the late-1990s/2000s and the
  **SOLID acronym** was coined ~2004 (Michael Feathers), so the two are not "unchanged since 1994" as one
  unit. GRASP (Craig Larman, _Applying UML and Patterns_, 1997) is a separate, still-current
  responsibility-assignment vocabulary. `typing.Protocol` (PEP 544, 3.8+) remains the current idiomatic
  structural-typing mechanism for strategy-style duck typing; `functools` (`wraps`, `partial`, decorator
  factories) remains the current stdlib decorator idiom — no deprecation or replacement.
  (docs.python.org / GoF canon / Larman 1997)
- 2026-07-12 — state-machine rung (co-35..co-37, ex-81..ex-84): the GoF **State** pattern (co-29) is the
  object-per-state form; **statecharts** are Harel's 1987 extension (nested/orthogonal states, guards,
  entry/exit actions) — the model **XState** implements — both stable canon.
- 2026-07-17 — verified: XState is current, actively maintained software (not deprecated or renamed) —
  current major version **XState v5** (latest patch `5.32.5` as of this sweep), with v4 relegated to
  legacy/archived docs. The terminology **states / events / guards / actions / actors** is confirmed
  current XState v5 vocabulary against `stately.ai/docs`: guards gate transitions, entry/exit actions
  fire on entering/leaving a state node, and actors are v5's organizing concept (created via
  `createActor`). The official repo explicitly cites Harel's statecharts and the SCXML spec as its
  theoretical foundation, confirming the "the model XState implements" framing. v4-era terms to avoid
  (`services`, `withConfig()`, `useInterpret()` — renamed `actors`, `provide()`, `useActorRef()` in v5)
  do not appear in this topic's prose. (stately.ai/docs / github.com/statelyai/xstate)

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · single-responsibility-principle** — a class has one reason to change; split mixed concerns.
- **co-02 · open-closed-principle** — open for extension, closed for modification; add behavior without editing.
- **co-03 · liskov-substitution-principle** — subtypes must be substitutable for their base without breaking callers.
- **co-04 · interface-segregation-principle** — many small role interfaces beat one fat interface.
- **co-05 · dependency-inversion-principle** — depend on abstractions; high-level policy owns the interface, not infra.
- **co-06 · grasp-information-expert** — assign a responsibility to the class holding the data it needs.
- **co-07 · grasp-creator** — the class that aggregates/contains B is the natural creator of B.
- **co-08 · grasp-controller** — route system events through a dedicated coordinating object, not the UI.
- **co-09 · grasp-low-coupling** — minimize dependencies between classes so change stays local.
- **co-10 · grasp-high-cohesion** — keep a class's responsibilities focused and mutually related.
- **co-11 · grasp-polymorphism** — replace type-switching with polymorphic dispatch on the varying type.
- **co-12 · grasp-pure-fabrication** — invent a non-domain class (e.g. Repository) to preserve cohesion/coupling.
- **co-13 · grasp-indirection** — insert a mediator to decouple two collaborators.
- **co-14 · grasp-protected-variations** — wrap an unstable point behind a stable interface.
- **co-15 · law-of-demeter** — talk only to immediate collaborators; avoid `a.getB().getC()` train wrecks.
- **co-16 · factory-method** — defer instantiation to a creation method so callers don't name concretes.
- **co-17 · abstract-factory** — a factory family that produces matched sets of related objects.
- **co-18 · builder** — assemble a complex object step-by-step, avoiding telescoping constructors.
- **co-19 · singleton-and-its-costs** — one shared instance — and the global-state/testability price it charges.
- **co-20 · adapter** — convert one interface into another a client expects.
- **co-21 · decorator** — wrap an object to add behavior without subclass explosion.
- **co-22 · facade** — a single simplified entry point over a complex subsystem.
- **co-23 · composite** — treat individual objects and compositions uniformly through one interface.
- **co-24 · proxy** — a stand-in controlling access (lazy, protection, remote) to a real subject.
- **co-25 · strategy** — encapsulate interchangeable algorithms behind a common interface.
- **co-26 · observer** — subjects notify subscribers of change without knowing them concretely.
- **co-27 · command** — reify a request as an object (execute/undo, queue, log).
- **co-28 · template-method** — a base defines the algorithm skeleton; subclasses fill named steps.
- **co-29 · state** — represent states as objects so transitions and legal moves are explicit.
- **co-30 · iterator** — expose sequential access without revealing the underlying representation.
- **co-31 · chain-of-responsibility** — pass a request along a handler chain until one handles it.
- **co-32 · gof-pattern-gallery** — recognizing the 23 patterns by intent across the three GoF families.
- **co-33 · refactor-to-pattern** — arrive at a pattern by relieving a smell under tests, not up front.
- **co-34 · anti-pattern-recognition** — name god objects, anemic domains, yo-yo inheritance, premature abstraction.
- **co-35 · finite-state-machine-modeling** — model a feature's lifecycle as an explicit FSM — a set of states, an alphabet of events, and a transition function — where a transition table (state × event → next state) makes every legal move explicit and every illegal one unrepresentable, going beyond the object-per-state form of co-29.
- **co-36 · statecharts-and-hierarchical-states** — Harel statecharts extend flat FSMs with nested/hierarchical states, orthogonal (parallel) regions, guards, and entry/exit actions (the model behind XState), taming the state explosion a flat FSM suffers as features grow.
- **co-37 · guards-and-entry-exit-actions** — a _guard_ is a boolean condition gating a transition; _entry/exit actions_ run side effects on entering/leaving a state, keeping effects at the state boundaries rather than scattered through the transition logic.

## Tensions & trade-offs — when NOT to reach for this

- **Pattern vs YAGNI**: a strategy or factory earns its indirection only when a second variant exists or is
  imminent; applied to a single case it is speculative generality — extra classes that hide straight-line
  logic behind ceremony.
- **Inheritance vs composition**: inheritance couples a subclass to its superclass's internals (the fragile
  base class); reach for it only for genuine substitutable is-a hierarchies, and prefer composition
  otherwise — the default, not the fallback.
- **When NOT to use it**: a small script, a one-off, or a stable spec with no real axis of change. SOLID
  and patterns are insurance against change; insurance you don't need is pure cost, and over-applied they
  make a codebase _harder_ to read, not easier.

## Lineage — why it beat the alternative

- The GoF catalogue (1994) named patterns that kept recurring in C++/Smalltalk codebases; SOLID (Robert
  Martin, 2000s) distilled the principles underneath them. Both were a reaction to inheritance-heavy 1990s
  OO producing rigid, fragile hierarchies (the "you wanted a banana, you got a gorilla holding the whole
  jungle" problem). The lesson is not the 23 patterns as a checklist but the **pressure** that produced
  them: unmanaged coupling makes systems ossify. So the durable skill is reading coupling and cohesion and
  judging which tactic — or none — relieves it; that same judgment carries forward into
  [`43-domain-driven-design`](./domain-driven-design.md) and [`42-software-architecture`](./software-architecture.md).

## Worked examples

Colocated under `object-oriented-design-and-patterns/learning/code/`; each a runnable before→after refactor
with a locking `pytest` test (DD-20/DD-30) and static type hints (DD-39). Every example cites the `co-NN`
it exercises. Contiguous `ex-01..ex-84`.

### Beginner

- **ex-01 · srp-split-god-class** — split a class doing parsing + formatting + IO into three — verify each class has one reason to change. (co-01)
- **ex-02 · srp-extract-report-writer** — extract file-writing out of a report calculator — verify the calculator module imports no IO. (co-01)
- **ex-03 · ocp-strategy-for-discount** — replace an `if/elif` discount chain with strategy objects — verify a new discount is added without editing the dispatcher. (co-02, co-25)
- **ex-04 · ocp-plugin-registry** — add behavior via registered handlers not an edited switch — verify a new handler needs zero edits to existing code. (co-02)
- **ex-05 · lsp-rectangle-square** — show `Square(Rectangle)` breaking `set_width` — verify the test fails, then fix via separate types. (co-03)
- **ex-06 · lsp-bird-fly** — refactor an `Ostrich(Bird)` that cannot `fly()` — verify no `NotImplementedError` is reachable. (co-03)
- **ex-07 · isp-split-fat-interface** — split a `Worker` interface that forces robots to `eat()` — verify a robot implements only `Workable`. (co-04)
- **ex-08 · isp-role-interfaces** — break a `Printer-Scanner-Fax` interface into role protocols — verify a plain printer depends on one protocol. (co-04)
- **ex-09 · dip-inject-repository** — invert a service depending on a concrete `MySQLRepo` — verify the service takes a `Repository` protocol. (co-05)
- **ex-10 · dip-notifier-abstraction** — depend on a `Notifier` protocol not `EmailSender` — verify swapping to SMS needs no service edit. (co-05)
- **ex-11 · lod-avoid-train-wreck** — replace `a.get_b().get_c().do_x()` with a tell-don't-ask method — verify the caller uses one dot. (co-15)
- **ex-12 · lod-wallet-payment** — `customer.pay(amt)` not `customer.get_wallet().get_money()` — verify the caller never touches `Wallet`. (co-15)
- **ex-13 · grasp-information-expert-total** — put `order_total` on `Order`, which owns the line items — verify no external total loop exists. (co-06)
- **ex-14 · grasp-creator-order-line** — `Order` creates its own `OrderLine` (it aggregates them) — verify the creation method lives on `Order`. (co-07)
- **ex-15 · grasp-controller-session** — route UI events through a single `SessionController` — verify the UI never calls the domain directly. (co-08)
- **ex-16 · grasp-high-cohesion-split** — split a mixed-concern module into cohesive units — verify each unit's methods share its state. (co-10)
- **ex-17 · grasp-low-coupling-event** — decouple two modules via an event, not a direct call — verify neither imports the other. (co-09)
- **ex-18 · factory-method-shape** — a `ShapeFactory.create(kind)` returning `Shape` subtypes — verify the caller obtains a `Circle` without importing `Circle`. (co-16)
- **ex-19 · simple-factory-parser** — centralize parser construction by file extension — verify an unknown extension raises a clean error. (co-16)
- **ex-20 · strategy-sort-key** — a pluggable comparison strategy for sorting — verify a new sort key is added as a function. (co-25)
- **ex-21 · observer-newsletter** — subscribers notified on `publish()` — verify adding a subscriber needs no publisher edit. (co-26)
- **ex-22 · adapter-celsius-fahrenheit** — adapt a Fahrenheit sensor to a Celsius interface — verify the client reads Celsius. (co-20)
- **ex-23 · decorator-logging** — wrap a service call in a logging decorator — verify the call is logged without editing the service. (co-21)
- **ex-24 · facade-checkout** — a `CheckoutFacade` hiding inventory + payment + shipping — verify the caller makes one call. (co-22)
- **ex-25 · template-method-report** — a base report defines the skeleton, subclasses fill steps — verify the shared flow is not duplicated. (co-28)
- **ex-26 · composition-over-inheritance-badge** — model a `Badge` via has-a not is-a — verify no subclass explosion. (co-09)
- **ex-27 · value-object-money** — an immutable `Money` with value-based `__eq__` — verify two equal `Money` instances compare equal. (co-10)

### Intermediate

- **ex-28 · abstract-factory-ui-theme** — a `WidgetFactory` family (dark/light) — verify swapping the theme swaps the whole widget family. (co-17)
- **ex-29 · builder-http-request** — a fluent `RequestBuilder` assembling optional parts — verify a request is built without a telescoping constructor. (co-18)
- **ex-30 · singleton-config-and-cost** — a `Config` singleton plus a test showing the global-state seam — verify one instance and demonstrate the isolation pain. (co-19)
- **ex-31 · singleton-to-injection** — replace a singleton with an injected dependency — verify a test isolates it without global reset. (co-19, co-05)
- **ex-32 · proxy-lazy-load** — a virtual proxy defers an expensive image load — verify loading happens on first access only. (co-24)
- **ex-33 · proxy-access-control** — a protection proxy checks permission before delegating — verify an unauthorized call is blocked. (co-24)
- **ex-34 · composite-file-tree** — treat `File` and `Directory` uniformly for `size()` — verify a recursive total via one interface. (co-23)
- **ex-35 · composite-menu** — nested menu items rendered uniformly — verify leaf and group share `render()`. (co-23)
- **ex-36 · command-undo** — `Command` objects with `execute`/`undo` for an editor — verify `undo` reverses the last command. (co-27)
- **ex-37 · command-queue** — queue commands for deferred batch execution — verify execution order is preserved. (co-27)
- **ex-38 · state-vending-machine** — a state machine with state objects, not flags — verify an illegal transition is rejected. (co-29)
- **ex-39 · state-traffic-light** — cycle states via the state pattern — verify `next()` moves red→green→yellow. (co-29)
- **ex-40 · iterator-custom-tree** — implement `__iter__` for an in-order tree walk — verify a `for` loop yields sorted values. (co-30)
- **ex-41 · iterator-paged-api** — an iterator that lazily pages a remote API — verify pages are fetched on demand. (co-30)
- **ex-42 · chain-of-responsibility-support** — escalate a ticket through a handler chain — verify an unhandled ticket falls to the next handler. (co-31)
- **ex-43 · chain-validation** — a validation pipeline as a handler chain — verify the first failure stops the chain. (co-31)
- **ex-44 · observer-typed-events** — a typed event bus with unsubscribe — verify an unsubscribed handler is not called. (co-26)
- **ex-45 · strategy-with-protocol** — a strategy via `typing.Protocol` duck typing — verify a plain function satisfies the protocol. (co-25, co-11)
- **ex-46 · grasp-polymorphism-dispatch** — replace a type-switch with polymorphic dispatch — verify adding a type edits no switch. (co-11)
- **ex-47 · grasp-pure-fabrication-repo** — introduce a `Repository` (not a domain concept) for persistence — verify the domain stays IO-free. (co-12)
- **ex-48 · grasp-indirection-mediator** — a `Mediator` decouples two collaborators — verify neither references the other. (co-13)
- **ex-49 · grasp-protected-variations-interface** — stabilize an unstable vendor API behind an interface — verify a vendor swap needs no client edit. (co-14)
- **ex-50 · adapter-two-way** — a two-way adapter bridging a legacy and a new API — verify both directions work. (co-20)
- **ex-51 · decorator-stacking** — stack retry + cache + log decorators — verify the composition order is correct. (co-21)
- **ex-52 · decorator-vs-inheritance** — decorator avoids the subclass explosion of coffee add-ons — verify N add-ons need no 2^N classes. (co-21)
- **ex-53 · factory-method-vs-abstract-factory** — contrast the two on one example — verify each solves its own axis of change. (co-16, co-17)
- **ex-54 · template-method-vs-strategy** — the same problem both ways — verify strategy swaps behavior at runtime. (co-28, co-25)
- **ex-55 · observer-vs-pubsub** — direct observer vs a broker — verify the added decoupling of the broker version. (co-26)
- **ex-56 · dip-with-abc** — DIP using an `abc.ABC` abstract base — verify a concrete subtype must implement all abstract methods. (co-05)
- **ex-57 · srp-cohesion-metric** — measure cohesion before/after a split — verify the methods-share-fields ratio improves. (co-01, co-10)

### Advanced

- **ex-58 · refactor-inheritance-to-composition** — convert a 4-level hierarchy to strategy composition — verify behavior identical, depth reduced to 1. (co-33, co-09)
- **ex-59 · refactor-to-strategy** — extract an embedded `if`-chain to a strategy family under tests — verify green throughout. (co-33, co-25)
- **ex-60 · refactor-to-state** — replace boolean-flag soup with the state pattern — verify invalid state combos become impossible. (co-33, co-29)
- **ex-61 · refactor-god-object** — decompose a god object applying SRP + information-expert — verify responsibilities are distributed. (co-33, co-01, co-06)
- **ex-62 · anti-pattern-god-object** — recognize and diagnose a god object — verify the smell is named and a fix sketched. (co-34)
- **ex-63 · anti-pattern-anemic-domain** — spot an anemic model (data + a separate service) — verify behavior is moved onto the entity. (co-34, co-06)
- **ex-64 · anti-pattern-yo-yo** — diagnose yo-yo inheritance jumping up and down a hierarchy — verify it is flattened. (co-34)
- **ex-65 · anti-pattern-singleton-abuse** — show a singleton as hidden global coupling — verify the test pain is demonstrated. (co-34, co-19)
- **ex-66 · anti-pattern-premature-abstraction** — remove a speculative strategy with one implementation (YAGNI) — verify the code is simpler. (co-34, co-02)
- **ex-67 · gof-gallery-creational** — one runnable file touring factory-method / abstract-factory / builder / singleton — verify each constructs correctly. (co-32, co-16, co-17, co-18, co-19)
- **ex-68 · gof-gallery-structural** — tour adapter / decorator / facade / composite / proxy — verify each wraps correctly. (co-32, co-20, co-21, co-22, co-23, co-24)
- **ex-69 · gof-gallery-behavioral** — tour strategy / observer / command / template-method / state / iterator / chain — verify each dispatches correctly. (co-32, co-25, co-26, co-27, co-28, co-29, co-30, co-31)
- **ex-70 · solid-full-order-engine** — apply all five SOLID principles to an order engine — verify each principle's seam. (co-01, co-02, co-03, co-04, co-05)
- **ex-71 · grasp-full-assignment** — assign responsibilities across a domain via all nine GRASP patterns — verify each pattern is placed. (co-06, co-07, co-08, co-09, co-10, co-11, co-12, co-13, co-14)
- **ex-72 · lsp-contract-test** — write a contract test suite every subtype must pass — verify a violating subtype fails it. (co-03)
- **ex-73 · isp-protocol-decomposition** — decompose a fat service into fine protocols checked with `pyright` — verify `pyright` passes minimal implementations. (co-04)
- **ex-74 · dip-hexagonal-ports** — ports-and-adapters wiring domain to infra — verify the domain imports no infra module. (co-05, co-14)
- **ex-75 · observer-memory-leak** — fix an observer leak via `weakref` — verify unsubscribed observers are garbage-collected. (co-26)
- **ex-76 · command-macro-undo** — a composite macro command with grouped undo — verify the group undoes atomically. (co-27, co-23)
- **ex-77 · strategy-registry-plugin** — a registry-driven strategy plugin system — verify a third-party strategy loads without a core edit. (co-25, co-02)
- **ex-78 · pattern-vs-yagni-judgment** — decide pattern-or-not across three scenarios — verify each choice is justified in prose. (co-34, co-02)
- **ex-79 · decorator-python-native** — cross-cutting via `functools` decorators vs a GoF class decorator — verify both work and note the trade-off. (co-21)
- **ex-80 · clean-design-preview** — a mini order/pricing re-engineer (strategy + factory + observer + decorator under SOLID) — verify the system extends without editing closed classes. (co-02, co-25, co-16, co-26, co-21)

### State machines & statecharts

- **ex-81 · transition-table-order-lifecycle** — model an order lifecycle (created→paid→shipped→delivered / cancelled) as an explicit state × event transition table — verify every illegal event in a state is rejected by the table itself, not scattered `if`s. (co-35)
- **ex-82 · statechart-hierarchical-media-player** — a hierarchical statechart for a media player (a parent `Playing` state with nested `Normal`/`Shuffle` substates + an orthogonal volume region) — verify a nested-state event is handled and the parent's shared transition still applies. (co-36)
- **ex-83 · guards-and-entry-exit-actions** — add a guard (`ship` only if `paid`) plus entry/exit actions (log on enter, release-lock on exit) to the order FSM — verify the guard blocks the transition and each action fires exactly once per state crossing. (co-37)
- **ex-84 · fsm-vs-boolean-flags-contrast** — contrast the transition-table FSM against the boolean-flag version (tie to ex-60) — verify the FSM makes an illegal state combination unrepresentable that the flag soup allowed. (co-35, co-33)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: take a deliberately smelly small system (e.g. an order/pricing engine) and re-engineer it
  applying SOLID and a coherent set of patterns (strategy + factory + observer + decorator), keeping a
  test suite green through every refactor step — ending with a clean, extensible design.
- **Concepts exercised**: [ ] each SOLID principle applied to a real smell (co-01, co-02, co-03, co-04,
  co-05) [ ] GRASP responsibility assignment (co-06, co-09, co-10, co-12) [ ] composition over inheritance
  (co-09) [ ] strategy + factory + observer + decorator used cohesively (co-25, co-16, co-26, co-21)
  [ ] an anti-pattern removed (co-34) [ ] arrived at via refactor-to-pattern under tests (co-33), green
  through every step.
- **Ordered steps**:
  1. `.../learning/capstone/code/` — the smelly baseline + a `pytest` suite pinning current behavior.
     Verify the suite passes against the baseline.
  2. Refactor to SOLID (SRP/OCP first): extract responsibilities, invert a dependency. Verify tests stay
     green after each move.
  3. Introduce strategy (pluggable pricing) + factory (creation) + observer (events) + decorator
     (cross-cutting). Verify a new pricing rule/event can be added without editing existing classes (OCP).
  4. Document the before→after design with a Mermaid class diagram. Verify the diagram matches the code.
- **Acceptance criteria**: behavior is unchanged (suite green throughout); extending the system needs no
  edits to closed classes; each applied principle/pattern is justified in prose.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Design Patterns: Elements of Reusable Object-Oriented Software** — Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides (1994). The original "Gang of Four" catalog of 23 patterns that defined the vocabulary of object-oriented design.
- **Object-Oriented Software Construction** — Bertrand Meyer (1997, 2nd ed.). Foundational text on OO design principles; introduced Design by Contract and the Open/Closed Principle. <https://bertrandmeyer.com/wp-content/upLoads/OOSC2.pdf>
- **Refactoring: Improving the Design of Existing Code** — Martin Fowler (1999; 2nd ed. 2018). Canonical catalog of code smells and refactorings for evolving object-oriented designs safely.
- **Agile Software Development: Principles, Patterns, and Practices** — Robert C. Martin (2002). Introduced the SOLID principles alongside worked object-oriented design case studies.
- **Head First Design Patterns** — Eric Freeman, Elisabeth Robson, Bert Bates & Kathy Sierra (2004; 2nd ed. 2020, Freeman & Robson only). The most widely used accessible introduction to the GoF patterns.

**Papers & articles**

- **Design Principles and Design Patterns** — Robert C. Martin (2000). The original paper naming the design principles later branded as SOLID. <https://staff.cs.utu.fi/~jounsmed/doos_06/material/DesignPrinciplesAndPatterns.pdf>

## In which paths

- `interview-ready/software-engineer` — Phase 1 · Interview preparation (through senior).
- `immediately-effective/software-engineer` — Deepening band · CS fundamentals, DS&A & algorithms — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 2 · Data structures, algorithms & object-oriented design.

> _Content originated in the now-closed FS-SE plan (topic 21); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
