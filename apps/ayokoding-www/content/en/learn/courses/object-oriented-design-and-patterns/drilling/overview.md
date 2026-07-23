---
title: "Overview"
date: 2026-07-17T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Object-Oriented Design & Patterns topic: five
fixed drills that force active recall instead of passive re-reading. Work through them in order --
short-answer recall first, then scenario judgment, then hands-on repetition, then a checklist to
confirm real automaticity, and finally why/why-not prompts that test whether you can explain the
reasoning, not just execute the syntax. Every answer is hidden in a `<details>` block; try each item
yourself before opening it. Together, the five drills below touch every one of this topic's 37
concepts and cite specific examples spanning all 84 worked examples in the Beginner, Intermediate, and
Advanced tiers, plus the capstone.

## Recall Q&A

Thirty-seven short-answer questions, one per concept (`co-01` through `co-37`). Answer from memory,
then check.

**Q1 (co-01 -- SRP).** What does it mean for a class to have "one reason to change," and why is
splitting by reason-to-change different from splitting by "one method per class"?

<details>
<summary>Answer</summary>

A class has one reason to change when every method on it serves a single, coherent concern -- a
change to that concern is the ONLY thing that ever forces an edit. Splitting by reason-to-change
groups related methods together (a `ReportCalculator` keeps every pricing method, even if there are
several); splitting by "one method per class" would fragment a coherent concern into needlessly many
tiny classes with no such organizing principle (Examples 1-2, 57).

</details>

**Q2 (co-02 -- OCP).** What is the concrete code smell that signals an OCP violation, and what's the
standard fix?

<details>
<summary>Answer</summary>

An `if`/`elif` (or `match`) chain that must be edited every time a new case is added is the smell --
each new case is a risky edit to code that already worked. The standard fix routes the variation
through polymorphism instead: a new subclass, a new registered strategy, or a new handler that plugs
into a stable seam without touching the dispatcher (Examples 3-4, 66).

</details>

**Q3 (co-03 -- LSP).** Give the general shape of an LSP violation, independent of any specific
example.

<details>
<summary>Answer</summary>

A subtype that "is-a" its base type syntactically (inheritance compiles) but not behaviorally --
typically by narrowing a precondition the base type promised to accept, widening a postcondition the
base type promised to satisfy, or raising where the base type promised it would not. Code written
against the base type breaks the moment it receives that particular subtype (Examples 5-6, 72).

</details>

**Q4 (co-04 -- ISP).** Why does a fat interface hurt implementers that never call most of its methods?

<details>
<summary>Answer</summary>

Every implementer of a fat interface is forced to support (or stub out) methods it has no real
implementation for, and a signature change to ANY method on that interface risks breaking every
implementer, even ones that never call the changed method. Splitting into role-specific interfaces
means each implementer only depends on, and is only affected by changes to, the methods it actually
uses (Examples 7-8, 73).

</details>

**Q5 (co-05 -- DIP).** What is inverted in "dependency inversion," and what does a high-level policy
depend on instead?

<details>
<summary>Answer</summary>

The USUAL direction -- high-level policy depending directly on low-level infrastructure -- is
inverted: the high-level policy defines an abstraction (a protocol/interface) it needs, and low-level
infrastructure implements that abstraction. The policy depends on the abstraction it owns, never on a
concrete infrastructure class (Examples 9-10, 56, 74).

</details>

**Q6 (co-06 -- Information Expert).** What single question does Information Expert reduce "which class
should this method live on?" to?

<details>
<summary>Answer</summary>

"Which class already has the fields this computation needs?" -- if `Order` holds the line items,
`Order` is the natural home for `order_total()`, because computing it anywhere else means first
extracting `Order`'s data and duplicating the summing logic outside the class that owns it
(Examples 13, 71).

</details>

**Q7 (co-07 -- Creator).** When should a class B's construction logic live on class A instead of at
every call site that needs a new B?

<details>
<summary>Answer</summary>

When A aggregates, contains, or closely uses B -- if `Order` owns its `OrderLine` objects, `Order`
is the natural place for an `add_line()` method that constructs a new `OrderLine`, keeping whatever
invariants a new line needs (defaults, validation, wiring to the parent) in one place instead of
duplicated at every caller (Examples 14, 71).

</details>

**Q8 (co-08 -- Controller).** What does routing UI events through a dedicated controller object buy
you that direct UI-to-domain calls don't?

<details>
<summary>Answer</summary>

A single, stable seam between the UI layer and domain logic -- swapping the UI (web to CLI) or the
domain implementation only requires rewiring the controller, since neither side calls the other
directly. Without a controller, UI code and domain code become directly coupled, so a change to either
risks breaking the other (Examples 15, 71).

</details>

**Q9 (co-09 -- Low Coupling).** Name two mechanisms that reduce coupling between two modules that don't
otherwise need to know about each other.

<details>
<summary>Answer</summary>

An event/callback (the publisher never names or imports the subscriber directly) and an injected
abstraction (a class depends on a protocol, not a concrete class, so the concrete implementation can
change independently). Composition over inheritance is the same idea applied to class relationships
specifically -- a has-a relationship couples less tightly than an is-a one (Examples 17, 26, 58, 71).

</details>

**Q10 (co-10 -- High Cohesion).** What makes a class low-cohesion, even if every one of its methods is
individually well-written?

<details>
<summary>Answer</summary>

Its methods barely touch each other's fields -- they happen to be grouped in the same class without
genuinely sharing state or purpose. A low-cohesion class is confusing to navigate (its methods don't
tell one coherent story) and resists reuse, because you can rarely take "half" of its behavior without
dragging the unrelated rest along (Examples 16, 27, 57, 71).

</details>

**Q11 (co-11 -- Polymorphism).** What does replacing an `isinstance`-based type-switch with polymorphic
dispatch actually change about adding a new type later?

<details>
<summary>Answer</summary>

Adding a new type becomes "add a new class implementing the shared method" instead of "find and edit
every type-switch that mentions the old types" -- the type-switch is an OCP violation waiting to
happen, since it's easy to miss a branch when a new type is added (Examples 45-46, 71).

</details>

**Q12 (co-12 -- Pure Fabrication).** Why is a `Repository` class "not a domain concept," and why invent
one anyway?

<details>
<summary>Answer</summary>

Nothing in the business domain of, say, a library or a shop is called a "repository" -- it is a class
invented purely to keep persistence logic out of domain classes that would otherwise need to know
about databases. A pure fabrication absorbs an infrastructure concern so the domain model stays about
the domain, at the cost of one class that doesn't map to anything a domain expert would recognize
(Examples 47, 71).

</details>

**Q13 (co-13 -- Indirection).** How does a mediator let two collaborators change independently of each
other?

<details>
<summary>Answer</summary>

Neither collaborator imports or references the other directly -- both only know the mediator. A
change to one collaborator's internals never has to ripple to the other, because the mediator is the
only thing that ever names both sides (Examples 48, 71).

</details>

**Q14 (co-14 -- Protected Variations).** What is the general recipe for confining the blast radius of a
volatile external dependency?

<details>
<summary>Answer</summary>

Identify the specific point most likely to change (an unstable vendor API, a volatile format), and
wrap it behind a stable interface owned by your own code. When the vendor API changes, only the
wrapper's implementation changes -- every client of the stable interface is unaffected (Examples 49,
71, 74).

</details>

**Q15 (co-15 -- Law of Demeter).** What is a "train wreck," and what is the "tell, don't ask"
alternative?

<details>
<summary>Answer</summary>

A train wreck is a chained call that reaches through an object to command a third object it happens
to hold a reference to (`a.get_b().get_c().do_x()`) -- it couples the caller to the entire chain of
internal structure between it and the final object. "Tell, don't ask" replaces this with a method on
the immediate collaborator that does the work internally, so the caller only ever makes one hop
(Examples 11-12).

</details>

**Q16 (co-16 -- Factory Method).** What does a factory method decouple a caller from?

<details>
<summary>Answer</summary>

The concrete class being constructed -- a caller asks the factory for "a `Shape` of this kind" and
depends only on the abstract return type, never importing or naming the concrete subclass. Adding a
new shape means editing the factory in one place, not every call site that used to construct shapes
directly (Examples 18-19, 53, 67, 80).

</details>

**Q17 (co-17 -- Abstract Factory).** How does an abstract factory prevent accidentally mixing objects
from two different families?

<details>
<summary>Answer</summary>

By making the WHOLE family swap at once -- a single `WidgetFactory` interface produces a matched
button, checkbox, and window that all belong to the same theme, so choosing the factory chooses the
entire consistent set. Without it, swapping "which family" means finding and swapping every individual
factory-method call site independently, risking a partial, inconsistent swap (Examples 28, 53, 67).

</details>

**Q18 (co-18 -- Builder).** What problem does a fluent builder solve that a constructor with many
optional parameters does not?

<details>
<summary>Answer</summary>

A "telescoping constructor" forces every caller to remember positional parameter order and to pass
placeholder values for parts it doesn't need. A builder makes each part self-documenting by name
(`.with_header(...)`) and lets optional parts be included or omitted in any order, readably, with
construction logic (validation, defaults) living in one place (Examples 29, 67).

</details>

**Q19 (co-19 -- Singleton).** What is the specific testability cost a singleton imposes, and what
usually replaces it?

<details>
<summary>Answer</summary>

Any test that mutates the singleton's state can leak that mutation into the next test unless
something explicitly resets it, and code depending on the singleton cannot easily be tested with a
different configuration -- the dependency doesn't show up in any constructor signature, so it's hidden.
Dependency injection (co-05) usually replaces it: pass the shared instance in explicitly, and a test
can substitute a fresh one with zero global state (Examples 30-31, 65, 67).

</details>

**Q20 (co-20 -- Adapter).** What does an adapter change about the client or the class being adapted?

<details>
<summary>Answer</summary>

Nothing -- neither the client nor the adapted class is modified. The adapter sits between them,
translating one interface into the interface the client already expects, which is essential when you
don't own one side (a third-party sensor, a legacy API) or don't want to touch code that already has
its own tests and callers (Examples 22, 50, 68).

</details>

**Q21 (co-21 -- Decorator).** Why does N independent add-ons modeled as subclasses risk 2^N classes,
and how does Decorator avoid that?

<details>
<summary>Answer</summary>

If every COMBINATION of add-ons needs its own subclass (milk, sugar, milk+sugar, ...), the subclass
count grows exponentially with the number of independent add-ons. Decorator turns "which combination"
into "which decorators did I wrap this in" -- N decorators can be composed in any combination without
a single new class per combination, and each decorator adds its behavior around whatever the wrapped
object's CURRENT behavior is (Examples 23, 51-52, 68, 79-80).

</details>

**Q22 (co-22 -- Facade).** What does a facade centralize, and what does it NOT do?

<details>
<summary>Answer</summary>

It centralizes the correct sequencing of calls across several subsystem classes (inventory, payment,
shipping) into one entry-point call, so most callers don't need to know or correctly order that
sequence themselves. It does NOT hide the subsystem's classes from callers who need finer control --
they can still reach the subsystem classes directly if the facade's default path doesn't fit
(Example 24, 68).

</details>

**Q23 (co-23 -- Composite).** What single interface lets a caller treat a leaf and a group uniformly?

<details>
<summary>Answer</summary>

A shared method both leaf and composite implement (e.g. `size()` on both `File` and `Directory`) --
the composite's implementation recurses into its children and calls the SAME method on each, so a
caller never special-cases "is this a leaf or a group?" at any level of the tree (Examples 34-35, 68,
76).

</details>

**Q24 (co-24 -- Proxy).** Name the three named uses of Proxy this topic covers, and what each defers or
guards.

<details>
<summary>Answer</summary>

Virtual proxy defers an expensive operation (loading a large resource) until it's actually accessed;
protection proxy checks permission before delegating a call to the real subject; a remote proxy (named
but not built here) stands in for an object that lives elsewhere. In every case, the client talks to
the proxy exactly as if it were the real subject (Examples 32-33, 68).

</details>

**Q25 (co-25 -- Strategy).** What is the single most common tactic for satisfying OCP, and why?

<details>
<summary>Answer</summary>

Strategy -- because an `if`/`elif` chain selecting behavior has to be edited every time a new option
appears, while a strategy family lets a new option be added as a new class that plugs into the
existing call site untouched. A registry-backed strategy (Example 77) goes further: even a third party
can add a strategy with zero edits to core code (Examples 3, 20, 45, 59, 69, 77, 80).

</details>

**Q26 (co-26 -- Observer).** What does a subject need to know about its subscribers, and what does
Observer do to the "who reacts to this event" question that Strategy does to "which algorithm runs"?

<details>
<summary>Answer</summary>

Nothing concrete -- the subject holds a list of subscriber references (or a protocol they satisfy) and
never imports a specific subscriber class. Both Observer and Strategy are the same OCP move: Strategy
lets you add a new algorithm without editing the call site; Observer lets you add a new subscriber
without editing the subject (Examples 21, 44, 55, 69, 75, 80).

</details>

**Q27 (co-27 -- Command).** What becomes possible once a request is turned into an object with
`execute()`/`undo()`, that a bare function call cannot support?

<details>
<summary>Answer</summary>

Queuing, logging, undoing, and grouping the request with other commands -- a bare function call
happens immediately and leaves nothing behind to inspect, replay, or reverse, while a Command object
persists as data that other code can act on later (Examples 36-37, 69, 76).

</details>

**Q28 (co-28 -- Template Method).** Where does the shared flow of a multi-step algorithm live in
Template Method, and what do subclasses supply?

<details>
<summary>Answer</summary>

The shared flow (e.g. open, process, close) lives exactly once, in the base class's template method;
subclasses override only the step-specific hooks that vary. Without this, every subclass needing a
variant of the same overall flow would have to re-implement (and keep in sync) the shared parts too
(Examples 25, 54, 69).

</details>

**Q29 (co-29 -- State).** How does modeling each state as its own object make illegal transitions
structurally impossible, rather than merely discouraged?

<details>
<summary>Answer</summary>

Each state object only exposes the methods that are legal FROM that state -- an illegal transition
isn't rejected by a conditional check, it simply has no method to call, or the method it does have
raises deliberately. A boolean-flag implementation, by contrast, allows any combination of flags to be
set, because nothing enumerates which combinations are legal (Examples 38-39, 60, 69).

</details>

**Q30 (co-30 -- Iterator).** What does an iterator hide from its caller, and what does a LAZY iterator
additionally avoid?

<details>
<summary>Answer</summary>

It hides the collection's internal representation -- a `for` loop over a custom tree walks it in order
without the caller ever seeing the tree's node layout. A lazy iterator additionally avoids doing work
(or making a network call) for elements the caller never actually reaches, fetching each page only
when asked for the next element (Examples 40-41, 69).

</details>

**Q31 (co-31 -- Chain of Responsibility).** How does a chain of handlers avoid the OCP violation of one
large `if`/`elif` handler?

<details>
<summary>Answer</summary>

Each case lives in its own handler object, addable to the chain without touching the handlers already
there -- a single large handler covering every case would need editing every time a new case appears.
Each handler decides independently whether to handle the request or pass it along (Examples 42-43,
69).

</details>

**Q32 (co-32 -- GoF Pattern Gallery).** What are the three GoF families, and what does each organize
around?

<details>
<summary>Answer</summary>

Creational (how objects get built: factory method, abstract factory, builder, singleton), structural
(how objects are composed: adapter, decorator, facade, composite, proxy), and behavioral (how objects
communicate and share responsibility: strategy, observer, command, template method, state, iterator,
chain of responsibility). Naming which family a problem belongs to narrows the search for the right
tactic quickly (Examples 67-69).

</details>

**Q33 (co-33 -- Refactor to Pattern).** What makes a pattern "earned" rather than speculative, per this
topic's framing?

<details>
<summary>Answer</summary>

Arriving at it by relieving a real, currently-felt smell, under a test suite pinned BEFORE the
refactor and kept green through every step -- not choosing the pattern up front and building toward it
in anticipation of a variant that doesn't exist yet. The pinning tests are what make each refactor step
verifiably safe (Examples 58-61, 84; the capstone's Step 1-2).

</details>

**Q34 (co-34 -- Anti-Pattern Recognition).** Name the five anti-patterns this topic names explicitly,
in one phrase each.

<details>
<summary>Answer</summary>

God object (one class doing everything), anemic domain model (data classes with all behavior pulled
into a separate service), yo-yo inheritance (understanding a class requires jumping up and down a deep
hierarchy), singleton abuse (hidden global coupling), and premature abstraction (a pattern applied for
a variant that doesn't exist yet) (Examples 62-66, 78).

</details>

**Q35 (co-35 -- Finite-State-Machine Modeling).** What makes an illegal (state, event) pair
"unrepresentable" rather than merely "unreached" in a transition-table FSM?

<details>
<summary>Answer</summary>

The table simply has no entry for it -- there is no code path, however convoluted, that could ever
produce that transition, because the lookup itself fails. "Unreached" (as in a boolean-flag model)
means the bad combination hasn't happened YET in this particular run, but nothing in the type prevents
it from happening in some other run (Examples 81, 84).

</details>

**Q36 (co-36 -- Statecharts and Hierarchical States).** Why does a flat FSM modeling two independent
concerns suffer a combinatorial explosion, and how do hierarchical/orthogonal states avoid it?

<details>
<summary>Answer</summary>

A flat FSM needs a distinct state for every COMBINATION of the two concerns (three playback modes
times four volume levels needs twelve states), growing multiplicatively as more concerns are added.
Hierarchical states let one parent state hold nested substates for one concern, sharing a single
parent-level transition across all of them; an orthogonal region lets a second concern (volume) vary
completely independently, with no combinatorial states at all (Example 82).

</details>

**Q37 (co-37 -- Guards and Entry/Exit Actions).** What problem do guards solve that a bare transition
table cannot express, and what problem do entry/exit actions solve?

<details>
<summary>Answer</summary>

A transition table alone can only say "this event moves to that state" -- it cannot express "only IF
some additional condition holds" (a guard adds that condition on top of the table lookup). Entry/exit
actions anchor side effects (logging, releasing a lock) to the state BOUNDARY itself, guaranteeing they
fire exactly once per crossing, regardless of which event triggered the crossing or how many places in
the code could trigger it (Example 83).

</details>

## Applied problems

Twelve scenarios. Each describes a task without naming the construct -- decide which principle or
pattern solves it, then check.

**AP1.** A team keeps re-editing the same `checkout()` method every time a new discount type ships,
and each edit risks breaking the discount types that already worked and were already tested.

<details>
<summary>Answer</summary>

This is an OCP violation (co-02) -- route the variation through a Strategy (co-25): give each discount
type its own class implementing a shared `apply()` method, and have `checkout()` accept whichever
strategy it's handed. Adding a new discount becomes "add a new class," never "edit `checkout()` again"
(Examples 3, 59, 70).

</details>

**AP2.** A `CheckoutService`'s unit tests each need to stand up a real database connection just to test
pricing math that has nothing to do with persistence.

<details>
<summary>Answer</summary>

This is a DIP violation (co-05) -- `CheckoutService` should depend on a `Repository` PROTOCOL, not a
concrete database class, injected at construction. Tests substitute a fake, in-memory implementation of
the protocol, and the pricing logic can be tested with zero real database involved (Examples 9, 74;
the capstone's Step 2).

</details>

**AP3.** Two independent booleans on an `Order` (`is_paid`, `is_shipped`) can currently be set in any
combination, including "shipped but not paid," which should never be possible.

<details>
<summary>Answer</summary>

Model the lifecycle as an explicit finite-state machine (co-35) with a transition table -- a single
`state: str` field replaces the two independent booleans, and the only reachable states are the ones
that appear as a VALUE somewhere in the table. "Shipped but not paid" becomes structurally
unrepresentable, not merely unlikely (Examples 60, 81, 84).

</details>

**AP4.** A media player needs three playback modes AND four volume levels, and modeling every
combination as its own flat state would require twelve states, most of which differ only in volume.

<details>
<summary>Answer</summary>

This calls for hierarchical/orthogonal states (co-36) -- model playback mode as one region (three
states) and volume as a completely separate, orthogonal region (four states, independent of playback
mode), instead of multiplying them into twelve combined states (Example 82).

</details>

**AP5.** A `Robot` class is forced to implement an `eat()` method (inherited from a fat `Worker`
interface it otherwise needs) that makes no sense for a robot, and the stub silently returns the wrong
thing when a caller happens to call it.

<details>
<summary>Answer</summary>

This is an ISP violation (co-04) -- split `Worker` into role-specific protocols (`Workable`,
`Eatable`), so `Robot` implements only `Workable` and structurally cannot be passed anywhere an
`Eatable` is required, catching the mismatch at the type level instead of at a silently-wrong runtime
call (Examples 7-8, 73).

</details>

**AP6.** A `Square(Rectangle)` subclass passes every unit test written specifically for `Square`, but a
generic function written against `Rectangle` produces the wrong result the moment it's handed a
`Square`.

<details>
<summary>Answer</summary>

This is an LSP violation (co-03) -- `Square` overriding `set_width` to also change `height` breaks the
`Rectangle` contract that width and height vary independently. The fix is usually to stop `Square` from
subclassing `Rectangle` at all, giving each its own contract, rather than forcing an incompatible is-a
relationship (Example 5).

</details>

**AP7.** Three unrelated responsibilities (email validation, database persistence, welcome
notification) currently live in one `UserManager` class, and a bug in the notification logic risks
breaking validation because they share internal mutable state.

<details>
<summary>Answer</summary>

This is a god object (co-34), fixable with SRP (co-01) -- split into `EmailValidator`,
`UserRepository`, and `WelcomeNotifier`, each with its own single reason to change and no shared
mutable state connecting concerns that have nothing to do with each other (Examples 1-2, 61-62).

</details>

**AP8.** A codebase has a `PaymentStrategy` interface with exactly one implementation, and no second
implementation is planned on any roadmap, yet every payment call site goes through the strategy
indirection anyway.

<details>
<summary>Answer</summary>

This is premature abstraction (co-34) -- a pattern applied for a variant that doesn't exist yet is
pure ceremony. Unless a second `PaymentStrategy` implementation is real or imminent, collapse the
indirection back into a plain function or class; reintroduce Strategy only when a genuine second
variant shows up (Examples 66, 78).

</details>

**AP9.** A `Notifier`'s `send()` method needs to log every call, retry on failure, and cache
recent results -- and a future requirement might need any subset of these three behaviors, in any
combination, on different notifiers.

<details>
<summary>Answer</summary>

This is a Decorator (co-21) situation -- three independent add-ons, each its own decorator class
wrapping any `Notifier`, composable in any combination without a subclass per combination. Modeling
all eight combinations as subclasses would risk 2^3 = 8 subclasses; three decorators cover every
combination by stacking (Examples 51-52).

</details>

**AP10.** A `ship` transition should only be allowed to fire if the order is already paid, but the
transition table alone has no way to express that condition.

<details>
<summary>Answer</summary>

Add a guard (co-37) -- a boolean condition checked IN ADDITION to the table lookup succeeding. The
table says the transition EXISTS; the guard says whether it's ALLOWED to fire right now, given
additional state the table alone cannot see (Example 83).

</details>

**AP11.** A `Library` class currently constructs its own `LoanRepository` and its own concrete email
notifier internally, making it impossible to test `Library`'s checkout logic without a real
database and a real email service.

<details>
<summary>Answer</summary>

Multiple GRASP seams apply at once: Pure Fabrication (co-12) for the repository (persistence isn't a
domain concept), Indirection (co-13)/Low Coupling (co-09) for the notifier (inject a callback or
protocol instead of a concrete class), and DIP (co-05) generally -- `Library` should receive both as
constructor parameters, never construct them itself (Example 71).

</details>

**AP12.** A vendor's third-party pricing API changes its response shape twice a year, and each change
currently means editing pricing logic scattered across a dozen call sites that all call the vendor
directly.

<details>
<summary>Answer</summary>

This is a Protected Variations (co-14) problem -- wrap the volatile vendor API behind a stable
interface owned by your own code (e.g. a `PricingPort`), so a vendor shape change only requires editing
the one adapter that implements that port. Every one of the dozen call sites is unaffected (Examples
49, 74).

</details>

## Code katas

Twelve hands-on repetition drills. Each is a before/after `.py` file colocated under `drilling/code/`.
Every "before" script is a real, runnable Python program that misapplies the concept being drilled --
run it yourself, diagnose the bug from the observed behavior, fix it from memory, then compare your fix
against the "after" script and the model solution before checking your work against the
actually-executed output shown.

### Kata 1 -- SRP: a "just checking the total" call quietly sends an email

_relates to co-01, Examples 1-2_

**Task.** `ReportGenerator.total()` should be a pure calculation, safe to call as many times as needed
(e.g. to redisplay a number on screen). The version below is broken: `total()` has a hidden
notification side effect, so calling it twice for display purposes sends two emails.

**Before** (`drilling/code/kata-01-srp-notification-side-effect/before/kata.py`)

```python
"""Kata 1 (before): SRP violation -- pricing and notification mixed in one class."""


class ReportGenerator:
    def __init__(self) -> None:
        self.email_log: list[str] = []

    def total(self, amounts: list[float]) -> float:
        result = sum(amounts)
        self.email_log.append(f"emailed total {result}")  # SMELL: a "total" getter has a notification side effect
        return result


report = ReportGenerator()
print(report.total([10.0, 20.0]))
print(report.total([10.0, 20.0]))  # called again, e.g. to redisplay -- but this ALSO re-sends an email
print(report.email_log)
```

**Observed (buggy) output** (captured by actually running the script above):

```text
30.0
30.0
['emailed total 30.0', 'emailed total 30.0']
```

**After** (`drilling/code/kata-01-srp-notification-side-effect/after/kata.py`)

```python
"""Kata 1 (after): SRP -- pricing and notification separated into two classes."""


class ReportCalculator:
    def total(self, amounts: list[float]) -> float:
        return sum(amounts)  # a PURE calculation -- no side effect, safe to call any number of times


class ReportMailer:
    def __init__(self) -> None:
        self.email_log: list[str] = []

    def send(self, total: float) -> None:
        self.email_log.append(f"emailed total {total}")


calculator = ReportCalculator()
mailer = ReportMailer()
total = calculator.total([10.0, 20.0])
print(total)
print(calculator.total([10.0, 20.0]))  # calling total() again is now SAFE -- no side effect
mailer.send(total)  # sending is now an EXPLICIT, separate action
print(mailer.email_log)
```

<details>
<summary>Model solution</summary>

**Root cause**: a single class mixed a pure calculation with a notification side effect, so any call
to the "read-only-looking" `total()` method silently mutated shared state. Splitting into
`ReportCalculator` (pure) and `ReportMailer` (explicit `send()`) makes the calculation callable any
number of times, and sending an email a deliberate, separate action.

**Run**: `python3 kata.py`

**Output**:

```text
30.0
30.0
['emailed total 30.0']
```

</details>

### Kata 2 -- OCP: two unrelated `if`s let two discounts silently stack

_relates to co-02, co-25, Example 3_

**Task.** A customer who is both premium and placing their first order should get exactly ONE 10%
discount. The version below is broken: two independent `if` checks (not `elif`, not a single decision
point) both fire, stacking the discount twice.

**Before** (`drilling/code/kata-02-ocp-stacking-discount-bug/before/kata.py`)

```python
"""Kata 2 (before): OCP violation -- unrelated `if` checks (not elif) let two discounts silently stack."""


def checkout_total(subtotal: float, is_premium: bool, is_first_order: bool) -> float:
    total = subtotal
    if is_premium:  # discount #1
        total = total * 0.90
    if is_first_order:  # discount #2 -- added LATER, as a separate `if`, not connected to the first
        total = total * 0.90
    return total


print(checkout_total(100.0, is_premium=True, is_first_order=True))  # customer meant to get ONE 10% discount
```

**Observed (buggy) output** (captured by actually running the script above):

```text
81.0
```

**After** (`drilling/code/kata-02-ocp-stacking-discount-bug/after/kata.py`)

```python
"""Kata 2 (after): OCP -- Strategy makes exactly one discount rule apply, with no chance of silent stacking."""

from typing import Protocol


class DiscountStrategy(Protocol):
    def apply(self, subtotal: float) -> float: ...


class NoDiscount:
    def apply(self, subtotal: float) -> float:
        return subtotal


class PremiumDiscount:
    def apply(self, subtotal: float) -> float:
        return subtotal * 0.90


class FirstOrderDiscount:
    def apply(self, subtotal: float) -> float:
        return subtotal * 0.90


def choose_discount(is_premium: bool, is_first_order: bool) -> DiscountStrategy:
    if is_premium:  # ONE explicit choice -- premium takes precedence, first-order never also fires
        return PremiumDiscount()
    if is_first_order:
        return FirstOrderDiscount()
    return NoDiscount()


def checkout_total(subtotal: float, is_premium: bool, is_first_order: bool) -> float:
    strategy = choose_discount(is_premium, is_first_order)  # exactly ONE strategy selected, never two
    return strategy.apply(subtotal)


print(checkout_total(100.0, is_premium=True, is_first_order=True))  # exactly one 10% discount now
```

<details>
<summary>Model solution</summary>

**Root cause**: two sequential, unrelated `if` statements each independently mutate the same running
total -- when both conditions are true, both fire, stacking the discount. Funneling the decision through
ONE selection function (`choose_discount`) that returns exactly one Strategy object makes "which
discount applies" a single decision, structurally preventing two discounts from ever both firing.

**Run**: `python3 kata.py`

**Output**:

```text
90.0
```

</details>

### Kata 3 -- LSP: `Square(Rectangle)` breaks a generic caller

_relates to co-03, Example 5_

**Task.** A function written against `Rectangle` resizes width only and expects height to stay
unchanged. The version below is broken: `Square` overrides `set_width` to also change `height`,
silently breaking that caller the moment it's handed a `Square`.

**Before** (`drilling/code/kata-03-lsp-square-breaks-rectangle/before/kata.py`)

```python
"""Kata 3 (before): LSP violation -- Square overrides set_width in a way that breaks callers of Rectangle."""


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def set_width(self, width: float) -> None:
        self.width = width

    def area(self) -> float:
        return self.width * self.height


class Square(Rectangle):
    def set_width(self, width: float) -> None:
        self.width = width
        self.height = width  # SMELL: also changes height -- breaks the Rectangle contract silently


def double_width_only(shape: Rectangle) -> float:
    original_height = shape.height
    shape.set_width(shape.width * 2)
    return shape.height - original_height  # a caller of Rectangle.set_width expects height UNCHANGED


square = Square(4, 4)
print(double_width_only(square))  # expected 0 (height unchanged) -- LSP violation breaks this
```

**Observed (buggy) output** (captured by actually running the script above):

```text
4
```

**After** (`drilling/code/kata-03-lsp-square-breaks-rectangle/after/kata.py`)

```python
"""Kata 3 (after): LSP -- Square no longer subclasses Rectangle; each honors its own, distinct contract."""


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def set_width(self, width: float) -> None:
        self.width = width

    def area(self) -> float:
        return self.width * self.height


class Square:  # => no longer a Rectangle subclass -- avoids inheriting a contract it cannot honor
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side * self.side


def double_width_only(shape: Rectangle) -> float:  # => genuinely only accepts Rectangle-shaped things now
    original_height = shape.height
    shape.set_width(shape.width * 2)
    return shape.height - original_height


rectangle = Rectangle(4, 4)
print(double_width_only(rectangle))  # 0 -- Rectangle actually honors ITS OWN contract
```

<details>
<summary>Model solution</summary>

**Root cause**: `Square` is-a `Rectangle` syntactically, but width and height are not independent for a
square -- the moment `set_width` also changes `height` to preserve "squareness," it breaks the
contract `Rectangle.set_width` promised. Removing the inheritance relationship (rather than forcing
`Square` to fake independence it structurally cannot have) fixes it -- `Square` becomes its own type
with its own contract.

**Run**: `python3 kata.py`

**Output**:

```text
0
```

</details>

### Kata 4 -- ISP: a stubbed method returns the wrong thing, silently

_relates to co-04, Examples 7-8_

**Task.** A fat `MultiTool` interface forces `SimpleScrewdriver` to implement `saw()`, even though it
has no saw. The version below is broken: the stub returns "screwed" instead of failing loudly, so a
caller relying on `saw()` gets silently wrong behavior.

**Before** (`drilling/code/kata-04-isp-fat-interface-stub-bug/before/kata.py`)

```python
"""Kata 4 (before): ISP violation -- a fat interface forces an unrelated stub, causing a silent wrong-behavior bug."""

from abc import ABC, abstractmethod


class MultiTool(ABC):  # SMELL: bundles unrelated capabilities into one fat interface
    @abstractmethod
    def screw(self) -> str: ...

    @abstractmethod
    def saw(self) -> str: ...


class SimpleScrewdriver(MultiTool):
    def screw(self) -> str:
        return "screwed"

    def saw(self) -> str:
        return "screwed"  # BUG: stubbed to satisfy the ABC, but callers relying on saw() get the WRONG behavior


def use_saw(tool: MultiTool) -> str:
    return tool.saw()


print(use_saw(SimpleScrewdriver()))  # expected some sawing behavior -- gets "screwed" instead, silently wrong
```

**Observed (buggy) output** (captured by actually running the script above):

```text
screwed
```

**After** (`drilling/code/kata-04-isp-fat-interface-stub-bug/after/kata.py`)

```python
"""Kata 4 (after): ISP -- two narrow protocols; SimpleScrewdriver only implements the one it genuinely supports."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Screwable(Protocol):
    def screw(self) -> str: ...


@runtime_checkable
class Sawable(Protocol):
    def saw(self) -> str: ...


class SimpleScrewdriver:  # => implements ONLY Screwable -- no stubbed, wrong-behavior saw()
    def screw(self) -> str:
        return "screwed"


print(isinstance(SimpleScrewdriver(), Sawable))  # False -- the type system itself catches the mismatch now
```

<details>
<summary>Model solution</summary>

**Root cause**: the fat `MultiTool` interface forced `SimpleScrewdriver` to implement `saw()` even
though it has no meaningful implementation, so it stubbed one out that silently returned the wrong
result. Splitting into narrow `Screwable`/`Sawable` protocols means `SimpleScrewdriver` never claims to
support `saw()` at all -- `isinstance(..., Sawable)` correctly reports `False`, catching the mismatch
structurally instead of at a surprising runtime call.

**Run**: `python3 kata.py`

**Output**:

```text
False
```

</details>

### Kata 5 -- DIP: a hard-coded dependency cannot be tested

_relates to co-05, Examples 9-10_

**Task.** `ReportService` needs to be testable without a real database. The version below is broken:
it hard-codes a concrete `MySQLRepository` inside its own constructor, so there is no way to substitute
a fake from outside -- and in this sandbox, that concrete repository genuinely cannot connect.

**Before** (`drilling/code/kata-05-dip-hardcoded-repository/before/kata.py`)

```python
"""Kata 5 (before): DIP violation -- ReportService hard-codes a concrete repository, so it cannot be tested with a fake."""


class MySQLRepository:
    def fetch_total(self) -> float:
        raise ConnectionError("no real database available in this environment")  # simulates an unavailable real DB


class ReportService:
    def __init__(self) -> None:
        self.repository = MySQLRepository()  # SMELL: hard-coded concrete dependency, constructed INSIDE __init__

    def total(self) -> float:
        return self.repository.fetch_total()


service = ReportService()
try:
    print(service.total())  # there is no way to substitute a fake repository from outside
except ConnectionError as error:
    print(f"crashed: {error}")
```

**Observed (buggy) output** (captured by actually running the script above):

```text
crashed: no real database available in this environment
```

**After** (`drilling/code/kata-05-dip-hardcoded-repository/after/kata.py`)

```python
"""Kata 5 (after): DIP -- ReportService depends on an injected Repository protocol, testable with a fake."""

from typing import Protocol


class Repository(Protocol):
    def fetch_total(self) -> float: ...


class FakeRepository:  # => a lightweight, INJECTABLE stand-in -- no real database needed
    def fetch_total(self) -> float:
        return 42.0


class ReportService:
    def __init__(self, repository: Repository) -> None:  # => injected, not constructed internally
        self.repository = repository

    def total(self) -> float:
        return self.repository.fetch_total()


service = ReportService(FakeRepository())  # => the fake substitutes cleanly, no database required
print(service.total())
```

<details>
<summary>Model solution</summary>

**Root cause**: `ReportService` constructs its own concrete dependency, so no caller (including a test)
can ever hand it something else. Accepting a `Repository` PROTOCOL as a constructor parameter inverts
the dependency: `ReportService` depends on an abstraction it owns, and any implementation (real or
fake) that satisfies that protocol can be injected.

**Run**: `python3 kata.py`

**Output**:

```text
42.0
```

</details>

### Kata 6 -- Information Expert: a snapshot goes stale

_relates to co-06, Example 13_

**Task.** A running total should always reflect an order's CURRENT items. The version below is broken:
`OrderPrinter` captures a snapshot of `order.items` at construction time, so items added afterward
never show up in its total.

**Before** (`drilling/code/kata-06-information-expert-stale-snapshot/before/kata.py`)

```python
"""Kata 6 (before): GRASP Information Expert violation -- OrderPrinter computes the total instead of Order, and goes stale."""


class Order:
    def __init__(self) -> None:
        self.items: list[float] = []

    def add_item(self, price: float) -> None:
        self.items.append(price)


class OrderPrinter:  # SMELL: computes a total from a SNAPSHOT, not from Order itself (which actually owns the data)
    def __init__(self, order: Order) -> None:
        self.snapshot = list(order.items)  # captured once, at construction time

    def total(self) -> float:
        return sum(self.snapshot)


order = Order()
order.add_item(10.0)
printer = OrderPrinter(order)
order.add_item(20.0)  # added AFTER the printer was built
print(printer.total())  # expected 30.0 -- but the printer's stale snapshot never saw the second item
```

**Observed (buggy) output** (captured by actually running the script above):

```text
10.0
```

**After** (`drilling/code/kata-06-information-expert-stale-snapshot/after/kata.py`)

```python
"""Kata 6 (after): GRASP Information Expert -- Order computes its own total, always reading its CURRENT items."""


class Order:  # => co-06: Order owns items, so Order is the natural information expert for the total
    def __init__(self) -> None:
        self.items: list[float] = []

    def add_item(self, price: float) -> None:
        self.items.append(price)

    def total(self) -> float:
        return sum(self.items)  # => always reads CURRENT state, never a stale snapshot


order = Order()
order.add_item(10.0)
order.add_item(20.0)
print(order.total())
```

<details>
<summary>Model solution</summary>

**Root cause**: `OrderPrinter` copied `Order`'s data instead of asking `Order` to compute the total
itself, so the copy went stale the moment `Order` changed. Information Expert's fix is mechanical: the
class that already holds the data (`Order`) is the natural home for the computation that reads it, so
`total()` always reflects current state by construction.

**Run**: `python3 kata.py`

**Output**:

```text
30.0
```

</details>

### Kata 7 -- Law of Demeter: a train wreck crashes on a missing link

_relates to co-15, Example 11_

**Task.** `shipping_label` needs to work even for a customer with no address on file. The version
below is broken: it reaches through two links (`customer.address.city`), assuming `address` is never
`None`.

**Before** (`drilling/code/kata-07-law-of-demeter-train-wreck-crash/before/kata.py`)

```python
"""Kata 7 (before): Law of Demeter violation -- a train wreck crashes when an intermediate link is missing."""


class Address:
    def __init__(self, city: str) -> None:
        self.city = city


class Customer:
    def __init__(self, address: "Address | None") -> None:
        self.address = address  # optional -- some customers have no address on file yet


def shipping_label(customer: Customer) -> str:
    return customer.address.city.upper()  # type: ignore[union-attr]  # SMELL: reaches through TWO links, assumes address is never None


customer = Customer(address=None)
try:
    print(shipping_label(customer))
except AttributeError as error:
    print(f"crashed: {error}")
```

**Observed (buggy) output** (captured by actually running the script above):

```text
crashed: 'NoneType' object has no attribute 'city'
```

**After** (`drilling/code/kata-07-law-of-demeter-train-wreck-crash/after/kata.py`)

```python
"""Kata 7 (after): Tell, Don't Ask -- Customer owns the null-check, callers never reach through it."""


class Address:
    def __init__(self, city: str) -> None:
        self.city = city


class Customer:
    def __init__(self, address: "Address | None") -> None:
        self.address = address

    def shipping_city(self) -> str:  # => co-15: the customer TELLS its own city, callers never ASK through address
        if self.address is None:
            return "unknown"
        return self.address.city.upper()


def shipping_label(customer: Customer) -> str:
    return customer.shipping_city()  # => ONE hop, delegated -- no train wreck, no crash


customer = Customer(address=None)
print(shipping_label(customer))
```

<details>
<summary>Model solution</summary>

**Root cause**: the caller reached through `Customer` into `Address`'s internals, coupling itself to
the assumption that `address` is always present. Moving the null-check INTO `Customer` (which is the
class that actually knows whether its own `address` might be missing) means every caller makes exactly
one hop, and the missing-address case is handled once, in the class that owns the data.

**Run**: `python3 kata.py`

**Output**:

```text
unknown
```

</details>

### Kata 8 -- composition over inheritance: a leaked `sort()` breaks chronological order

_relates to co-09, Example 58_

**Task.** `EventLog` should record events in chronological order, always. The version below is broken:
subclassing `list` leaks EVERY list method, including `sort()`, which a caller can call to silently
reorder events.

**Before** (`drilling/code/kata-08-inheritance-leaks-list-interface/before/kata.py`)

```python
"""Kata 8 (before): naive inheritance leaks list's full interface, letting sort() silently reorder events."""


class EventLog(list):  # SMELL: is-a list -- inherits EVERY list method, including sort()
    def record(self, event: str) -> None:
        self.append(event)


log = EventLog()
log.record("login")
log.record("purchase")
log.record("logout")
log.sort()  # BUG: nothing stops a caller from calling a leaked list method that breaks chronological order
print(log)
```

**Observed (buggy) output** (captured by actually running the script above):

```text
['login', 'logout', 'purchase']
```

**After** (`drilling/code/kata-08-inheritance-leaks-list-interface/after/kata.py`)

```python
"""Kata 8 (after): composition over inheritance -- EventLog HOLDS a list, sort() is simply not part of its interface."""

from __future__ import annotations

from typing import Iterator


class EventLog:  # => has-a list -- never subclasses list, so no leaked method can ever be called
    def __init__(self) -> None:
        self._events: list[str] = []

    def record(self, event: str) -> None:
        self._events.append(event)

    def __iter__(self) -> Iterator[str]:
        return iter(self._events)

    def __repr__(self) -> str:
        return repr(self._events)


log = EventLog()
log.record("login")
log.record("purchase")
log.record("logout")
print(log)  # chronological order is now structurally guaranteed -- sort() does not exist on this class
```

<details>
<summary>Model solution</summary>

**Root cause**: `EventLog(list)` inherits list's ENTIRE interface, including methods that were never
meant to be part of an event log's API. Composition (`EventLog` HOLDS a `_events: list[str]` instead of
BEING one) exposes only `record()` and iteration -- `sort()` simply does not exist on the class, so
there is no leaked method left to call by accident.

**Run**: `python3 kata.py`

**Output**:

```text
['login', 'purchase', 'logout']
```

</details>

### Kata 9 -- god object: a "just validating" call has a hidden write side effect

_relates to co-34, co-01, Examples 61-62_

**Task.** Checking whether an email is valid should never, by itself, persist anything. The version
below is broken: `is_valid_email` stages a save through shared mutable state, so a LATER, unrelated
`save()` call persists an email that was never actually valid.

**Before** (`drilling/code/kata-09-god-object-hidden-coupling/before/kata.py`)

```python
"""Kata 9 (before): god object -- one class mixes validation, persistence, AND notification, so a validation-only call also writes."""


class UserManager:  # SMELL: one class handles validation, persistence, AND notification
    def __init__(self) -> None:
        self.database: list[str] = []
        self.notifications: list[str] = []
        self._pending: str | None = None  # shared mutable state -- the root of the coupling below

    def is_valid_email(self, email: str) -> bool:
        self._pending = email  # SMELL: a "just validate" call has a SIDE EFFECT of staging a save
        return "@" in email

    def save(self) -> None:
        if self._pending is not None:
            self.database.append(self._pending)
            self.notifications.append(f"welcome {self._pending}")


manager = UserManager()
manager.is_valid_email("not-an-email")  # caller only wanted to CHECK validity...
manager.save()  # ...but a later, unrelated save() call now persists the INVALID email anyway
print(manager.database)
```

**Observed (buggy) output** (captured by actually running the script above):

```text
['not-an-email']
```

**After** (`drilling/code/kata-09-god-object-hidden-coupling/after/kata.py`)

```python
"""Kata 9 (after): the god object split into three cohesive classes -- validation has no side effect anymore."""


class EmailValidator:  # => SRP: validation, and only validation -- no shared mutable state with anything else
    def is_valid(self, email: str) -> bool:
        return "@" in email


class UserRepository:  # => SRP: persistence, and only persistence
    def __init__(self) -> None:
        self.database: list[str] = []

    def save(self, email: str) -> None:
        self.database.append(email)


class WelcomeNotifier:  # => SRP: notification, and only notification
    def __init__(self) -> None:
        self.notifications: list[str] = []

    def notify(self, email: str) -> None:
        self.notifications.append(f"welcome {email}")


validator = EmailValidator()
repository = UserRepository()
notifier = WelcomeNotifier()

email = "not-an-email"
if validator.is_valid(email):  # a PURE check -- no side effect, safe to call as many times as needed
    repository.save(email)
    notifier.notify(email)

print(repository.database)  # never persisted -- the invalid email correctly never reached save()
```

<details>
<summary>Model solution</summary>

**Root cause**: three unrelated responsibilities shared one piece of mutable state
(`self._pending`), so an innocuous-looking validation call had a hidden coupling to a LATER,
unrelated save. Splitting into three cohesive classes with no shared state removes the coupling
entirely -- `validator.is_valid()` is now a pure function with zero side effects.

**Run**: `python3 kata.py`

**Output**:

```text
[]
```

</details>

### Kata 10 -- boolean flags to FSM: complete-without-assign slips through

_relates to co-35, Example 81_

**Task.** A task should never be completed before it's assigned. The version below is broken:
`Task.complete()` sets `is_completed = True` without checking `is_assigned` first.

**Before** (`drilling/code/kata-10-boolean-flags-to-fsm/before/kata.py`)

```python
"""Kata 10 (before): boolean-flag soup lets a task be marked complete without ever being assigned."""


class Task:
    def __init__(self) -> None:
        self.is_assigned = False
        self.is_completed = False

    def complete(self) -> None:
        self.is_completed = True  # BUG: nothing checks is_assigned first


task = Task()
task.complete()  # marked complete WITHOUT ever being assigned to anyone
print(task.is_assigned, task.is_completed)
```

**Observed (buggy) output** (captured by actually running the script above):

```text
False True
```

**After** (`drilling/code/kata-10-boolean-flags-to-fsm/after/kata.py`)

```python
"""Kata 10 (after): a transition-table FSM makes "complete without assign" structurally illegal."""


class IllegalTransition(Exception):
    pass


TASK_TRANSITIONS: dict[tuple[str, str], str] = {
    ("open", "assign"): "assigned",
    ("assigned", "complete"): "completed",
}


class Task:
    def __init__(self) -> None:
        self.state = "open"

    def send(self, event: str) -> None:
        key = (self.state, event)
        if key not in TASK_TRANSITIONS:
            raise IllegalTransition(f"event {event!r} is illegal in state {self.state!r}")
        self.state = TASK_TRANSITIONS[key]


task = Task()
try:
    task.send("complete")  # attempting the SAME illegal move as the before-script
except IllegalTransition as error:
    print(error)
```

<details>
<summary>Model solution</summary>

**Root cause**: two independent booleans allow any of the four combinations, including
"completed but not assigned," because nothing enumerates which combinations are legal. A transition
table with only two entries (`open -> assigned` via `assign`, `assigned -> completed` via `complete`)
has no entry for `("open", "complete")`, so the illegal move is rejected by a lookup failure rather
than a forgotten `if`.

**Run**: `python3 kata.py`

**Output**:

```text
event 'complete' is illegal in state 'open'
```

</details>

### Kata 11 -- Decorator: a hardcoded subclass total drifts from the base price

_relates to co-21, Examples 51-52_

**Task.** `CoffeeWithMilkAndSugar`'s price should always reflect the CURRENT base `Coffee` price. The
version below is broken: each subclass hardcodes an absolute total, so a later change to `Coffee`'s
own price leaves every subclass's hardcoded total stale.

**Before** (`drilling/code/kata-11-subclass-explosion-price-drift/before/kata.py`)

```python
"""Kata 11 (before): subclass explosion -- CoffeeWithMilkAndSugar hardcodes a price that drifts from Coffee's own price."""


class Coffee:
    def cost(self) -> float:
        return 2.00


class CoffeeWithMilk(Coffee):
    def cost(self) -> float:
        return 2.50  # hardcoded: base 2.00 + 0.50, duplicated by hand


class CoffeeWithMilkAndSugar(CoffeeWithMilk):
    def cost(self) -> float:
        return 2.75  # hardcoded AGAIN -- if Coffee.cost() ever changes, this number silently goes stale


Coffee.cost = lambda self: 3.00  # type: ignore[method-assign]  # simulates a LATER price bump to the base Coffee
print(CoffeeWithMilkAndSugar().cost())  # expected 3.75 (3.00 + 0.50 + 0.25) -- still shows the STALE 2.75
```

**Observed (buggy) output** (captured by actually running the script above):

```text
2.75
```

**After** (`drilling/code/kata-11-subclass-explosion-price-drift/after/kata.py`)

```python
"""Kata 11 (after): Decorator wraps the CURRENT Coffee price, so a base price change is picked up automatically."""

from typing import Protocol


class CoffeeLike(Protocol):
    def cost(self) -> float: ...


class Coffee:
    def cost(self) -> float:
        return 3.00  # the "later" price, current from the start this time


class MilkDecorator:  # => co-21: wraps ANY CoffeeLike, adds its own delta on top of whatever cost() returns NOW
    def __init__(self, wrapped: CoffeeLike) -> None:
        self._wrapped = wrapped

    def cost(self) -> float:
        return self._wrapped.cost() + 0.50


class SugarDecorator:
    def __init__(self, wrapped: CoffeeLike) -> None:
        self._wrapped = wrapped

    def cost(self) -> float:
        return self._wrapped.cost() + 0.25


coffee_with_milk_and_sugar = SugarDecorator(MilkDecorator(Coffee()))
print(coffee_with_milk_and_sugar.cost())  # always reflects Coffee's CURRENT price, no stale hardcoded total
```

<details>
<summary>Model solution</summary>

**Root cause**: each subclass hardcodes an ABSOLUTE total instead of composing on top of whatever the
base class's `cost()` returns right now, so the hardcoded numbers silently drift the moment the base
price changes. A decorator calls `self._wrapped.cost()` -- the CURRENT value -- and adds its own delta,
so a base price change propagates automatically through every decorator stacked on top.

**Run**: `python3 kata.py`

**Output**:

```text
3.75
```

</details>

### Kata 12 -- guards: a transition fires despite a false real-world precondition

_relates to co-37, Example 83_

**Task.** A door should never report "unlocked" while its battery is dead. The version below is
broken: `unlock()` unconditionally flips `state`, with no guard checking `battery_level` first.

**Before** (`drilling/code/kata-12-guard-blocks-physical-impossibility/before/kata.py`)

```python
"""Kata 12 (before): a state transition without a guard can fire even when a real precondition is false."""


class DoorLock:
    def __init__(self) -> None:
        self.state = "locked"
        self.battery_level = 0  # dead battery -- physically CANNOT actuate the lock

    def unlock(self) -> None:
        self.state = "unlocked"  # BUG: no guard checks battery_level before flipping state


lock = DoorLock()
lock.unlock()
print(lock.state)  # claims "unlocked" even though the battery is dead and nothing physically moved
```

**Observed (buggy) output** (captured by actually running the script above):

```text
unlocked
```

**After** (`drilling/code/kata-12-guard-blocks-physical-impossibility/after/kata.py`)

```python
"""Kata 12 (after): a guard blocks the transition when the real precondition (battery_level > 0) is not met."""


class GuardBlocked(Exception):
    pass


class DoorLock:
    def __init__(self) -> None:
        self.state = "locked"
        self.battery_level = 0

    def unlock(self) -> None:
        if self.battery_level <= 0:  # => the GUARD -- checked in addition to any transition-table entry
            raise GuardBlocked("cannot unlock: battery is dead")
        self.state = "unlocked"


lock = DoorLock()
try:
    lock.unlock()
except GuardBlocked as error:
    print(error)
print(lock.state)  # correctly still "locked" -- the guard prevented the state from lying about reality
```

<details>
<summary>Model solution</summary>

**Root cause**: the state transition itself carried no notion of a precondition beyond "this event is
recognized" -- it happily fired regardless of whether unlocking was physically possible. A guard checks
an ADDITIONAL condition (`battery_level > 0`) before the state is allowed to change, so the reported
state never lies about what actually happened in the real world.

**Run**: `python3 kata.py`

**Output**:

```text
cannot unlock: battery is dead
locked
```

</details>

## Self-check checklist

Work through this list without looking anything up. Every item should be something you can do from
memory, not something you'd need to search for.

**SOLID**

- [ ] I can name the concrete code smell that signals an SRP violation (a class with multiple,
      unrelated reasons to change) and split it by reason-to-change, not by method count (co-01).
- [ ] I can replace an `if`/`elif` chain selecting behavior with a Strategy class family, satisfying
      OCP (co-02).
- [ ] I can spot an LSP violation by asking "does code written against the base type still work
      correctly when handed this subtype?" (co-03).
- [ ] I can split a fat interface into role-specific protocols so no implementer is forced to stub an
      unrelated method (co-04).
- [ ] I can invert a hard-coded concrete dependency into an injected protocol parameter (co-05).

**GRASP + Law of Demeter**

- [ ] I can answer "which class should this method live on?" by asking which class already holds the
      data it needs (Information Expert, co-06).
- [ ] I can place a "create a B" method on the class that aggregates B, rather than scattering
      construction at every call site (Creator, co-07).
- [ ] I can route a UI/system event through a dedicated controller instead of letting the UI call
      domain objects directly (Controller, co-08).
- [ ] I can reduce coupling between two modules via an event, callback, or injected abstraction instead
      of a direct import-and-call (Low Coupling, co-09).
- [ ] I can identify a low-cohesion class by checking whether its methods genuinely share the class's
      own fields (High Cohesion, co-10).
- [ ] I can replace an `isinstance`-based type-switch with polymorphic dispatch (Polymorphism, co-11).
- [ ] I can invent a non-domain "pure fabrication" class (like a Repository) to keep a domain class
      IO-free (Pure Fabrication, co-12).
- [ ] I can insert a mediator so two collaborators never reference each other directly (Indirection,
      co-13).
- [ ] I can wrap a volatile external dependency behind a stable interface I own (Protected Variations,
      co-14).
- [ ] I can rewrite a train-wreck call (`a.get_b().get_c().do_x()`) as a tell-don't-ask method on the
      immediate collaborator (Law of Demeter, co-15).

**GoF Creational**

- [ ] I can build a factory method that returns an abstract type, so callers never name a concrete
      class directly (co-16).
- [ ] I can build an abstract factory that produces a matched family of related objects, swappable as
      one unit (co-17).
- [ ] I can build a fluent builder that replaces a telescoping constructor (co-18).
- [ ] I can name the specific testability cost of a Singleton and replace it with an injected dependency
      (co-19).

**GoF Structural**

- [ ] I can write an adapter that translates one interface into another without modifying either side
      (co-20).
- [ ] I can stack multiple decorators to compose independent add-ons without a subclass per combination
      (co-21).
- [ ] I can build a facade that centralizes a multi-step subsystem call sequence into one entry point
      (co-22).
- [ ] I can implement a composite where a leaf and a group share one method, so a caller never
      special-cases which one it has (co-23).
- [ ] I can distinguish a virtual proxy (defers work) from a protection proxy (guards access) (co-24).

**GoF Behavioral**

- [ ] I can encapsulate an algorithm family behind a shared interface so it can be swapped at a call
      site (Strategy, co-25).
- [ ] I can let a subject notify subscribers it knows nothing concrete about (Observer, co-26).
- [ ] I can turn a request into an object with `execute()`/`undo()` (Command, co-27).
- [ ] I can define a fixed algorithm skeleton once, with subclasses supplying only the varying steps
      (Template Method, co-28).
- [ ] I can model each lifecycle state as its own object, so illegal transitions have no method to call
      (State, co-29).
- [ ] I can implement `__iter__` to hide a collection's internal representation, including lazily
      (Iterator, co-30).
- [ ] I can chain independent handlers so each decides whether to handle a request or pass it along
      (Chain of Responsibility, co-31).

**Meta-skills**

- [ ] I can name which of the three GoF families (creational, structural, behavioral) a given pattern
      belongs to (co-32).
- [ ] I can describe the refactor-to-pattern discipline: pin behavior with tests FIRST, then refactor,
      keeping tests green every step (co-33).
- [ ] I can name and diagnose all five anti-patterns this topic covers by their one-phrase description
      (co-34).
- [ ] I can model a lifecycle as an explicit state x event -> state transition table instead of
      independent booleans (co-35).
- [ ] I can explain why hierarchical/orthogonal states avoid the combinatorial explosion a flat FSM
      suffers when modeling two independent concerns (co-36).
- [ ] I can add a guard and entry/exit actions to a transition table, and explain what each solves that
      the bare table cannot (co-37).

## Elaborative interrogation & self-explanation

Ten why/why-not prompts. Answer in your own words before checking -- the goal is explaining the
reasoning, not reciting a definition.

**W1.** Why is SRP (co-01) described as "the entry point into every other principle," rather than just
one principle among five?

<details>
<summary>Answer</summary>

Every other principle assumes a class already does roughly one thing. LSP is easier to satisfy when a
subtype has one clear contract to honor; DIP is easier to apply when the abstraction being extracted
covers one coherent responsibility; Strategy and Decorator both wrap or swap ONE behavior cleanly only
when that behavior isn't already tangled with two or three others inside the same class. A class that
already violates SRP resists every other principle simultaneously.

</details>

**W2.** Why does this topic insist a pattern be "earned" (co-33) by a real, currently-felt smell, rather
than applied up front by someone who correctly predicts a future need?

<details>
<summary>Answer</summary>

Because the cost of a pattern (extra indirection, extra classes to navigate) is paid immediately and
certainly, while the benefit (flexibility for a future variant) is speculative and may never arrive.
Even a CORRECT prediction pays the indirection cost for however long the second variant doesn't yet
exist. Refactoring under a pinning test suite, once the smell is real, defers that cost until it's
actually justified -- and the tests prove the refactor didn't change behavior along the way.

</details>

**W3.** Why is a boolean-flag model of lifecycle state (the anti-pattern co-29's State pattern and
co-35's FSM both fix) worse than it looks at first glance?

<details>
<summary>Answer</summary>

It's not just that illegal combinations are POSSIBLE -- it's that nothing in the code enumerates which
combinations are legal in the first place. A reviewer has to reconstruct the legal state space by
reading every method that touches any of the flags; there is no single place that says "these are the
only valid combinations." A transition table or a state-object hierarchy makes that enumeration
explicit and inspectable.

</details>

**W4.** Why does Decorator (co-21) specifically solve the 2^N subclass explosion, when Strategy (co-25)
does not?

<details>
<summary>Answer</summary>

Strategy swaps ONE algorithm at a time -- it has no notion of "combining" multiple strategies. Decorator
is explicitly designed to COMPOSE: each decorator wraps whatever is inside it and adds its own behavior
on top, so stacking three decorators applies all three, in any combination, without needing a distinct
class per combination. The N independent add-ons stay independent because each is its own decorator,
not baked into a subclass alongside the others.

</details>

**W5.** Why does the capstone's Step 1 (pin the smelly baseline with tests BEFORE touching any code)
matter more than it might seem?

<details>
<summary>Answer</summary>

Without a pinning suite, "the refactor didn't change behavior" is an unverified claim -- you're trusting
that you read the smelly code correctly and reproduced its exact behavior in the new design. A pinning
suite written against the ORIGINAL code, still passing against the REFACTORED code, is direct evidence
(not an assertion) that behavior was preserved through every step.

</details>

**W6.** Why is DIP (co-05) framed as "policy depends on abstraction, infrastructure implements it" --
why does the DIRECTION of the dependency arrow matter, not just whether an interface exists somewhere?

<details>
<summary>Answer</summary>

If a `Repository` PROTOCOL were defined in the infrastructure layer and the domain imported it from
there, the domain would still depend (transitively) on the infrastructure package existing at all --
swapping infrastructure would still risk breaking the import. Defining the protocol IN the domain
layer, with infrastructure importing IT, means infrastructure can change or be replaced entirely without
the domain layer's source ever needing to change, not even an import statement.

</details>

**W7.** Why does GRASP's Pure Fabrication (co-12) exist as its own named pattern, instead of just being
"apply SRP to persistence code"?

<details>
<summary>Answer</summary>

SRP tells you to split responsibilities; it doesn't tell you WHERE the split-off responsibility should
live if no domain concept naturally owns it. Pure Fabrication names the specific move of inventing a
class with no domain meaning (a `Repository`, a `Mediator`) purely to hold a responsibility that would
otherwise pollute a domain class -- it's the answer to "SRP says split this out, but split it out to
WHERE?"

</details>

**W8.** Why does this topic teach both the object-per-state State pattern (co-29) and a separate,
explicit transition-table FSM (co-35), rather than treating them as the same thing?

<details>
<summary>Answer</summary>

State (co-29) makes illegal moves impossible by NOT giving the wrong methods to the current state
object, but the full picture of "what states exist and what moves between them" is scattered across
however many state classes there are -- you'd have to read every class to reconstruct the whole
machine. A transition table (co-35) is a SINGLE data structure listing every legal (state, event) pair
in one place, inspectable and enumerable without reading any class body at all -- useful when you need
the whole machine visible at once, e.g. to generate a diagram or audit every legal path.

</details>

**W9.** Why does Protected Variations (co-14) say to wrap the UNSTABLE thing specifically, rather than
wrapping everything behind an interface defensively?

<details>
<summary>Answer</summary>

Every interface has a cost (an extra layer of indirection to read through), so wrapping something that
never changes buys nothing and adds navigation overhead for no reason -- that's premature abstraction
(co-34) by another name. Protected Variations targets the specific point most LIKELY to change (a
vendor API with a history of breaking changes) and accepts direct coupling everywhere else, where the
volatility doesn't exist.

</details>

**W10.** Why does this topic distinguish "unrepresentable" (co-35's FSM) from "unreached" (co-29's
boolean flags, before the fix) as a meaningfully different guarantee, rather than treating "the bug
hasn't happened yet" as good enough?

<details>
<summary>Answer</summary>

"Unreached" is a fact about the runs that have happened SO FAR -- it says nothing about whether some
future caller, some new code path, or a bug elsewhere could still produce the illegal combination.
"Unrepresentable" is a fact about the TYPE itself -- there is no code path, however contrived, that
could ever construct the illegal state, because the representation (a single state string, checked
against a table) has no slot for it. The second guarantee holds regardless of what future code does;
the first one only holds until something changes.

</details>

---

← Previous: [Capstone](../learning/capstone/overview.md) →
