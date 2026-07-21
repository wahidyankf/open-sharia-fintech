# Object-Oriented Programming Essentials (By Example, Python)

**Course ID**: `object-oriented-programming-essentials` · **Format**: By Example · **Language**: Python.

**Short summary**: Classes, inheritance, encapsulation, polymorphism

**Scope note**: the **usable slice** of OOP — enough to model a domain cleanly. SOLID, design patterns,
and deeper design go to [`21-object-oriented-design-and-patterns`](./object-oriented-design-and-patterns.md)
(split-and-interleave, DD-11).

## Why this exists · the big idea

- **The problem before the solution**: once data and the code that changes it drift apart, invariants
  break silently — anyone can put an object into an invalid state from anywhere.
- **Keep-this-if-you-forget-everything**: bundle state with the operations that guard it, and expose
  behavior, not fields — an object is a small guarantee about what stays true.
- **Big ideas touched**: `taming-state` (encapsulation contains mutable state behind an invariant),
  `coupling-vs-cohesion` (a well-shaped object is cohesive and narrowly coupled to the rest).

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./just-enough-python.md) (classes, functions,
  modules).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.10+** (required by `@dataclass(slots=True)`
  in ex-39) with `pytest` in a `venv`.
- **Assumed knowledge**: reading/writing basic Python including the one-line class preview from topic 04;
  no prior OOP background required.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: `@dataclass` options current — `frozen` (raises on field assignment), `slots`
  (since 3.10, drops per-instance `__dict__`), `eq` (generates `__eq__`); when `eq` and `frozen` are both
  True, `__hash__` is auto-generated. Overriding `__eq__` without `__hash__` sets `__hash__ = None`
  (unhashable). `abc.ABC`/`abstractmethod` mechanics stable. (docs.python.org dataclasses/datamodel)
- 2026-07-14 — re-confirmed for Phase 9 authoring, no changes since 2026-07-12 sweep: `frozen=True`
  field assignment still raises `dataclasses.FrozenInstanceError`; `slots=True` still "Added in
  version 3.10" and still drops per-instance `__dict__`; `eq=True` (default) still auto-generates
  `__eq__` (Python 3.13 changed the generated method to compare fields individually rather than as
  tuples — behavior-equivalent, not breaking); hash table unchanged (`eq`+`frozen` both True → auto
  `__hash__`; `eq=True`/`frozen=False` default → `__hash__ = None`); `order=True` still adds
  `__lt__`/`__le__`/`__gt__`/`__ge__`; `field(default_factory=...)` still the documented
  mutable-default mechanism. Plain-class `__eq__` without `__hash__` still sets `__hash__ = None`
  ([datamodel](https://docs.python.org/3/reference/datamodel.html#object.__hash__)). `abc.ABC` +
  `@abstractmethod` instantiation still raises `TypeError`
  ([abc](https://docs.python.org/3/library/abc.html)). `typing.Protocol` structural typing unchanged
  since 3.8 ([typing](https://docs.python.org/3/library/typing.html#typing.Protocol)).
  `object.__init_subclass__` (added 3.6) still fires on subclass creation. (re-fetched 2026-07-14,
  docs.python.org dataclasses/datamodel/abc/typing)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary source fetched and read in the retroactive grounding sweep
> (2026-07-12, `web-researcher`). Sources: `docs.python.org` (dataclasses/datamodel/abc/typing), ACM DL,
> a directly-fetched copy of the Liskov & Wing paper PDF, and publisher records. All checkable claims
> verified; no factual corrections (one editorial precision fix: Python-version floor).

- **dataclass + hashing (Accuracy notes, co-06, ex-36/39/40/53)** —
  [dataclasses](https://docs.python.org/3/library/dataclasses.html): `slots` "Added in version 3.10",
  `frozen=True` assignment → `FrozenInstanceError`, hash table (`eq&frozen`→generated; `eq` alone→`None`);
  [datamodel `__repr__`/`__hash__`](https://docs.python.org/3/reference/datamodel.html#object.__hash__)
  — all verbatim. Prerequisites tightened to **Python 3.10+** (ex-39 requires `slots=True`).
- **Identity/equality, name mangling, ABCs, protocols (co-03/05/11/12/16, ex-19/59-64/78)** —
  [`is` vs `==`](https://docs.python.org/3/reference/expressions.html#is), private name mangling
  `__spam`→`_Class__spam` ([expressions](https://docs.python.org/3/reference/expressions.html#atom-identifiers)),
  [`abc`](https://docs.python.org/3/library/abc.html) (can't instantiate abstract class → `TypeError`;
  `.register()` virtual subclass), [`typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)
  structural typing, `__init_subclass__` auto-registration — all confirmed.
- **Read more** — GoF _Design Patterns_ (Gamma/Helm/Johnson/Vlissides, 1994, Addison-Wesley); Booch
  _OOAD with Applications_ 3rd ed. 2007 ([ACM](https://dl.acm.org/doi/book/10.5555/1407387), UML "Three
  Amigos"); Bloch _Effective Java_ 3rd ed. 2018; Liskov & Wing "A Behavioral Notion of Subtyping" **ACM
  TOPLAS 16(6), Nov 1994, 1811–1841** (PDF fetched + read at
  [cs.cmu.edu/~wing](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf), ACM
  [10.1145/197320.197383](https://dl.acm.org/doi/10.1145/197320.197383)); Kay "The Early History of
  Smalltalk" **ACM SIGPLAN Notices 28(3), Mar 1993** ([10.1145/155360.155364](https://dl.acm.org/doi/10.1145/155360.155364))
  — all author/venue/year confirmed. Note: the _term_ "Liskov Substitution Principle" was coined by
  Robert C. Martin (SOLID); the 1994 paper is its formal behavioral-subtyping basis (universally cited as
  the LSP paper).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By Example). Each example below cites the co-NN it exercises. -->

- **co-01 · class-and-instance** — A class is a template; instances are objects carrying their own state,
  built by `__init__` where `self` is the receiver the method acts on.
- **co-02 · encapsulation** — Bundle state with the methods that guard it and expose behavior rather than
  raw fields, so the object is a small guarantee about what stays true.
- **co-03 · identity-vs-equality** — `is` compares object identity (same address); `==` compares value via
  `__eq__`, and the two answers can differ for distinct objects holding equal data.
- **co-04 · repr-and-str** — `__repr__` gives an unambiguous developer-facing string (ideally
  round-trippable); `__str__` gives a readable end-user string; `repr` is the fallback when `str` is absent.
- **co-05 · eq-and-hash** — `__eq__` defines value equality and `__hash__` must stay consistent with it;
  defining `__eq__` alone sets `__hash__ = None`, making instances unhashable.
- **co-06 · dataclass-value-object** — `@dataclass` auto-generates `__init__`/`__repr__`/`__eq__`; `frozen`
  gives immutability + hashability, `slots` drops `__dict__`, `order` adds comparison, `field(default_factory=…)`
  gives per-instance mutable defaults.
- **co-07 · properties** — `@property` exposes a computed or guarded attribute through attribute syntax; a
  matching setter enforces invariants on assignment without changing the caller's `obj.attr = x` idiom.
- **co-08 · inheritance** — A subclass reuses and extends a base class; `super().__init__(...)` chains
  construction and `isinstance` reflects the resulting type hierarchy.
- **co-09 · method-overriding** — A subclass replaces a base method's behavior, optionally calling
  `super().method()` to augment rather than fully replace it.
- **co-10 · polymorphism** — A single call-site invokes a shared method name and each object dispatches to
  its own implementation, so new types plug in without editing the call-site.
- **co-11 · abstraction-abc** — `abc.ABC` + `@abstractmethod` declare an interface contract that cannot be
  instantiated and forces subclasses to implement the required methods.
- **co-12 · duck-typing** — Compatibility is decided by the methods an object actually has, not by a declared
  base type; `typing.Protocol` captures that structural contract for static checking.
- **co-13 · composition-over-inheritance** — Model "has-a" by holding collaborator objects (injected via the
  constructor) instead of "is-a" subclassing, keeping coupling narrow and behavior swappable.
- **co-14 · class-vs-instance-attributes** — Class attributes are shared across all instances; instance
  attributes are per-object, and a mutable class-level default is a classic shared-state bug.
- **co-15 · classmethod-and-staticmethod** — `@classmethod` receives `cls` (alternative constructors,
  subclass-aware factories); `@staticmethod` is a namespaced function needing neither instance nor class.
- **co-16 · encapsulation-conventions** — Python has no true private: `_name` signals "internal" by
  convention and `__name` triggers name-mangling to `_Class__name`; exposing copies protects internal collections.
- **co-17 · invariant-enforcement** — Validate in `__init__`, `__post_init__`, and setters on every path so
  an object can never enter an invalid state from anywhere.

## Worked examples

Colocated under `object-oriented-programming-essentials/learning/code/`; every example is runnable + `pytest`
(DD-20) and uses static type hints throughout (DD-39). Each cites the `co-NN` it exercises. Contiguous
`ex-01..ex-80`.

### Beginner

- **ex-01 · define-minimal-class** — define `class Dog: pass` and instantiate `d: Dog = Dog()` — verify
  `type(d) is Dog`. (co-01)
- **ex-02 · init-with-fields** — write `__init__(self, name: str) -> None` setting `self.name` — verify
  `Dog("Rex").name == "Rex"`. (co-01)
- **ex-03 · instance-method** — add `def bark(self) -> str: return "woof"` — verify `d.bark() == "woof"`.
  (co-01)
- **ex-04 · method-reads-state** — add `greet(self) -> str` returning an f-string over `self.name` — verify
  the returned string contains the instance's name. (co-01)
- **ex-05 · multiple-instances-independent** — create two `Dog`s with different names — verify each retains
  its own `name` with no cross-talk. (co-01)
- **ex-06 · method-mutates-state** — add `rename(self, new: str) -> None` — verify `name` reflects the new
  value after the call. (co-01)
- **ex-07 · default-init-argument** — `__init__(self, name: str, legs: int = 4) -> None` — verify the default
  applies when `legs` is omitted. (co-01)
- **ex-08 · repr-for-debugging** — add `__repr__(self) -> str` returning `Dog(name=…)` — verify `repr(d)`
  matches the expected string. (co-04)
- **ex-09 · str-vs-repr** — add distinct `__str__` and `__repr__` — verify `str(d)` and `repr(d)` return
  different strings. (co-04)
- **ex-10 · identity-with-is** — bind `a: Dog = Dog("Rex"); b: Dog = a` — verify `a is b` is `True`. (co-03)
- **ex-11 · default-equality-is-identity** — compare two separate `Dog("Rex")` without `__eq__` — verify `==`
  is `False` (falls back to identity). (co-03)
- **ex-12 · define-eq** — add `__eq__(self, other: object) -> bool` comparing `name` — verify two same-name
  dogs compare equal. (co-03, co-05)
- **ex-13 · class-attribute-shared** — add class attr `species: str = "canine"` — verify both instances read
  the same shared value. (co-14)
- **ex-14 · instance-shadows-class-attr** — assign `d.species = "wolf"` on one instance — verify only that
  instance changes and the other keeps the class value. (co-14)
- **ex-15 · encapsulate-balance** — a `BankAccount` holding `self._balance: float` with `deposit`/`balance`
  methods — verify `deposit` raises the reported balance. (co-02)
- **ex-16 · reject-negative-deposit** — make `deposit` raise `ValueError` on a negative amount — verify
  `pytest.raises(ValueError)` fires. (co-02, co-17)
- **ex-17 · withdraw-guard-overdraft** — make `withdraw` raise when amount exceeds balance — verify an
  overdrawing call is rejected and balance is unchanged. (co-02, co-17)
- **ex-18 · protected-attr-convention** — name the field `_balance` (single underscore) — verify it signals
  "internal" yet remains technically accessible. (co-16)
- **ex-19 · name-mangled-attr** — use `self.__pin: str` and access it via `obj._Class__pin` — verify direct
  `obj.__pin` raises `AttributeError`. (co-16)
- **ex-20 · dataclass-basic** — `@dataclass class Point: x: int; y: int` — verify the auto `__init__` builds
  `Point(1, 2)`. (co-06)
- **ex-21 · dataclass-auto-repr** — reuse the same `Point` — verify it prints `Point(x=1, y=2)` with no
  hand-written `__repr__`. (co-06, co-04)
- **ex-22 · dataclass-auto-eq** — verify `Point(1, 2) == Point(1, 2)` is `True` by value alone. (co-06, co-05)
- **ex-23 · dataclass-default-field** — add `label: str = ""` — verify omitting it uses the default. (co-06)
- **ex-24 · dataclass-default-factory** — declare `tags: list[str] = field(default_factory=list)` — verify
  each instance receives its own independent list. (co-06)
- **ex-25 · post-init-validation** — a `Temperature` dataclass whose `__post_init__` rejects values below
  absolute zero — verify invalid construction raises. (co-06, co-17)
- **ex-26 · duck-typed-area-preview** — two unrelated classes each with `area(self) -> float`; a function
  calls `.area()` — verify both are accepted (duck-typing preview). (co-12)
- **ex-27 · objects-in-collection** — place instances in a `list[Dog]` and iterate — verify iteration yields
  each object in order. (co-01)
- **ex-28 · self-is-explicit** — show `Dog.bark(d)` equals `d.bark()` — verify both return the same value,
  demystifying `self`. (co-01)

### Intermediate

- **ex-29 · property-read-only** — a `@property def area(self) -> float` on `Rectangle` — verify `r.area` is
  read as an attribute (no parentheses). (co-07)
- **ex-30 · property-setter-validation** — a `@width.setter` rejecting non-positive values — verify assigning
  `r.width = -1` raises `ValueError`. (co-07, co-17)
- **ex-31 · property-backed-by-private** — store `_width`, expose it via a property — verify external code
  uses `.width`, never `._width`. (co-07, co-16)
- **ex-32 · computed-property-derived** — a `@property def perimeter(self) -> float` derived from sides —
  verify it updates after `width` changes. (co-07)
- **ex-33 · eq-value-object** — a `Money` with `__eq__` on `(amount, currency)` — verify equal amount+currency
  compare equal. (co-05)
- **ex-34 · hash-consistent-with-eq** — add `__hash__` over the same fields — verify equal `Money` share a
  hash and deduplicate inside a `set[Money]`. (co-05)
- **ex-35 · eq-without-hash-unhashable** — define `__eq__` but omit `__hash__` — verify the instance is
  unhashable (`TypeError` when added to a set). (co-05)
- **ex-36 · frozen-dataclass-immutable** — `@dataclass(frozen=True)` — verify assigning a field raises
  `FrozenInstanceError`. (co-06)
- **ex-37 · frozen-dataclass-hashable** — reuse the frozen dataclass — verify it works as a `dict` key and
  `set` member. (co-06, co-05)
- **ex-38 · dataclass-eq-false** — `@dataclass(eq=False)` — verify equality falls back to identity. (co-06,
  co-03)
- **ex-39 · dataclass-slots** — `@dataclass(slots=True)` — verify assigning an undeclared attribute raises
  `AttributeError` and the instance has no `__dict__`. (co-06)
- **ex-40 · dataclass-order** — `@dataclass(order=True)` — verify instances sort by their field tuple. (co-06)
- **ex-41 · inherit-fields-methods** — `Animal` base with `Cat(Animal)` — verify `Cat` inherits the base
  `__init__` fields. (co-08)
- **ex-42 · super-init-chain** — `Cat.__init__` calls `super().__init__(...)` then adds a field — verify both
  base and subclass fields are set. (co-08)
- **ex-43 · override-method** — `Cat.speak()` overrides `Animal.speak()` — verify the subclass version runs
  on a `Cat`. (co-09)
- **ex-44 · super-call-in-override** — an override that calls `super().speak()` then augments it — verify the
  combined result. (co-08, co-09)
- **ex-45 · polymorphic-list-dispatch** — a `list[Animal]` of mixed subclasses looped calling `.speak()` —
  verify each element dispatches to its own override. (co-10)
- **ex-46 · isinstance-check** — verify `isinstance(cat, Animal)` is `True` across the hierarchy. (co-08)
- **ex-47 · classmethod-alt-constructor** — `@classmethod from_string(cls, s: str) -> "Date"` — verify it
  builds an instance from parsed text. (co-15)
- **ex-48 · staticmethod-namespaced** — `@staticmethod is_leap(year: int) -> bool` — verify it is callable
  without an instance. (co-15)
- **ex-49 · classmethod-uses-cls** — a `@classmethod` instantiating `cls()` — verify a subclass factory
  returns the subclass type. (co-15, co-08)
- **ex-50 · class-attr-instance-counter** — increment a class attr in `__init__` — verify the counter equals
  the number of instances created. (co-14)
- **ex-51 · mutable-class-attr-pitfall** — reproduce a shared mutable class-level `list` bug, then fix it in
  `__init__` — verify the fix isolates per-instance state. (co-14, co-17)
- **ex-52 · invariant-in-init-and-setter** — enforce the same rule in both `__init__` and the setter — verify
  neither path admits an invalid state. (co-17, co-07)
- **ex-53 · repr-round-trip** — write a `__repr__` that reconstructs the object — verify `eval(repr(obj)) ==
obj`. (co-04, co-05)
- **ex-54 · encapsulated-collection** — expose a read-only copy/tuple of an internal `list` — verify caller
  mutation of the returned view leaves internals untouched. (co-02, co-16)
- **ex-55 · duck-typed-function** — `total_area(shapes: Iterable[HasArea]) -> float` calling `.area()` —
  verify a mix of unrelated types sums correctly. (co-12, co-10)
- **ex-56 · protocol-structural-type** — define `class HasArea(Protocol)` and type-hint against it — verify a
  class satisfies it without inheriting (static + runtime). (co-12)
- **ex-57 · equality-across-subclass** — decide `__eq__` between base and subclass instances — verify the
  chosen (type-strict) contract holds. (co-05, co-08)
- **ex-58 · dataclass-inheritance** — a dataclass subclassing another dataclass and adding a field — verify
  the combined `__init__` field order. (co-06, co-08)

### Advanced

- **ex-59 · define-abc-interface** — `class Shape(abc.ABC)` with `@abstractmethod area` — verify `Shape()`
  cannot be instantiated (`TypeError`). (co-11)
- **ex-60 · abc-subclass-must-implement** — a subclass omitting `area` — verify it also cannot be
  instantiated. (co-11)
- **ex-61 · abc-concrete-implementations** — `Circle`/`Square` implementing `area` — verify both instantiate
  and compute correctly. (co-11, co-09)
- **ex-62 · abc-polymorphic-callsite** — `def describe(s: Shape) -> str` calling `.area()` — verify one
  call-site handles every implementation. (co-11, co-10)
- **ex-63 · abstract-with-shared-helper** — an ABC providing a concrete helper reused by subclasses — verify
  a subclass inherits the shared logic while implementing the abstract method. (co-11, co-08)
- **ex-64 · register-virtual-subclass** — `Shape.register(ThirdParty)` — verify `isinstance` is `True`
  without inheritance. (co-11, co-12)
- **ex-65 · naive-inheritance-smell** — start with `Stack(list)` — verify it wrongly leaks `insert`/`append`,
  violating the intended interface (LSP leak). (co-08)
- **ex-66 · refactor-to-composition** — reimplement `Stack` holding `self._items: list[T]` — verify only
  `push`/`pop`/`peek` are public and the original tests stay green. (co-13)
- **ex-67 · composition-delegates** — a `Service` holding a `Logger` collaborator delegates logging — verify
  swapping the collaborator changes observed behavior. (co-13)
- **ex-68 · dependency-injection-constructor** — inject a collaborator via `__init__` instead of constructing
  it inside — verify a fake substitutes cleanly in a test. (co-13, co-12)
- **ex-69 · strategy-via-composition** — hold a pluggable `pricing: PricingStrategy` — verify swapping the
  strategy changes the computed price with no subclassing. (co-13, co-10)
- **ex-70 · favor-interface-over-concrete** — type the injected field as the ABC/Protocol, not a concrete
  class — verify any conforming implementation is accepted. (co-13, co-11)
- **ex-71 · encapsulated-state-machine** — an `Order` enforcing legal status transitions in its methods —
  verify an illegal transition raises. (co-02, co-17)
- **ex-72 · immutable-value-object-full** — a frozen `Money` whose arithmetic returns new instances — verify
  operands are left unchanged. (co-06, co-02)
- **ex-73 · value-objects-set-dedup** — place value objects in a `set` — verify duplicates collapse via
  consistent `__eq__` + `__hash__`. (co-05, co-06)
- **ex-74 · polymorphism-without-inheritance** — duck-typed `render()` across unrelated renderers — verify a
  single pipeline handles all of them. (co-12, co-10)
- **ex-75 · template-method-pattern** — a base defining an algorithm that calls abstract hooks — verify the
  overall flow is fixed while subclass hooks vary the steps. (co-11, co-09)
- **ex-76 · refactor-god-class** — split a two-responsibility class into two composed collaborators — verify
  each has one responsibility and all tests pass. (co-13, co-02)
- **ex-77 · invariant-survives-refactor** — after the composition refactor, re-run the invariant tests —
  verify the original invariant still cannot be violated. (co-17, co-13)
- **ex-78 · subclass-registry** — a base auto-registering subclasses via `__init_subclass__` — verify each
  subclass appears in the registry on definition. (co-15, co-08)
- **ex-79 · full-domain-model** — assemble an entity + value object + ABC interface + one composition into a
  single package — verify `pytest` is green end-to-end. (co-02, co-06, co-11, co-13)
- **ex-80 · property-based-invariant-test** — a `pytest` that constructs many randomized inputs asserting the
  invariant — verify no generated input reaches an invalid state. (co-17, co-07)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: model a small domain (e.g. a library or a payments ledger) as a clean object model —
  encapsulated invariants, a polymorphic operation, a `@dataclass` value object, and one composition
  refactor — as a runnable, tested package.
- **Concepts exercised**: [ ] encapsulated invariant enforced in `__init__`/setters [ ] polymorphism via
  a shared method across subclasses/duck types [ ] `@dataclass` value object with `__eq__`/`__hash__`
  [ ] composition over inheritance [ ] an `abc.ABC` interface.
- **Ordered steps**:
  1. `.../learning/capstone/code/domain/` — a value object (`@dataclass(frozen=True)`) + an entity with
     an invariant. Verify `pytest` rejects invalid construction.
  2. Add an `abc.ABC` interface with ≥2 implementations exercised polymorphically. Verify a single
     call-site handles all implementations.
  3. Refactor one naive inheritance chain into composition. Verify behavior unchanged (tests still green).
- **Acceptance criteria**: `pytest` green; invariants cannot be violated; the polymorphic call-site is
  implementation-agnostic; value object equality/hash behave correctly.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Design Patterns: Elements of Reusable Object-Oriented Software** — Gamma, Helm, Johnson, Vlissides (1994, "Gang of Four"). Canonical catalog of 23 OO patterns and the shared vocabulary still used industry-wide.
- **Object-Oriented Analysis and Design with Applications** — Grady Booch (3rd ed., 2007). Foundational OO analysis/design methodology from a UML co-creator.
- **Effective Java** — Joshua Bloch (3rd ed., 2018). Java-specific but its item-based OO-design tradeoffs (composition vs inheritance, immutability, interfaces) are widely cited.

**Papers & articles**

- **"A Behavioral Notion of Subtyping"** — Liskov, Wing (1994, ACM TOPLAS). The formal paper defining the Liskov Substitution Principle. <https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf>
- **"The Early History of Smalltalk"** — Alan Kay (1993, ACM SIGPLAN Notices). Kay's own account of the origin of "object-oriented." <https://dl.acm.org/doi/10.1145/155360.155364>

## In which paths

- `interview-ready/software-engineer` — Phase 1 · Interview preparation (through senior).
- `immediately-effective/software-engineer` — Deepening band · CS fundamentals, DS&A & algorithms — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 2 · Data structures, algorithms & object-oriented design.

> _Content originated in the now-closed FS-SE plan (topic 8); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
