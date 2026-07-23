---
title: "Overview"
date: 2026-07-17T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Programming Paradigms topic: five fixed drills
that force active recall instead of passive re-reading. Work through them in order -- short-answer
recall first, then scenario judgment, then hands-on repetition, then a checklist to confirm real
automaticity, and finally why/why-not prompts that test whether you can explain the reasoning, not
just execute the syntax. Every answer is hidden in a `<details>` block; try each item yourself before
opening it. Together, the five drills below touch every one of this topic's 25 concepts and cite
specific examples spanning all 80 worked examples in the Beginner, Intermediate, and Advanced tiers,
plus the capstone.

## Recall Q&A

Twenty-five short-answer questions, one per concept. Answer from memory before opening each answer.

**Q1 (co-01 -- Imperative Programming).** What makes code "imperative," and what specific cost does
that buy?

<details>
<summary>Answer</summary>

Imperative code is an explicit sequence of statements that change state step by step -- a loop that
mutates a counter, an assignment that overwrites a variable. It maps directly onto how a CPU actually
executes instructions, which makes it predictable to trace one line at a time -- but nothing stops a
later statement from silently depending on state set several lines earlier (Example 1's mutating
word-count loop; Example 33's turnstile modeled as a mutable state variable).

</details>

**Q2 (co-02 -- Procedural Abstraction).** What changes, and what stays exactly the same, when an inline
imperative block is refactored into named procedures?

<details>
<summary>Answer</summary>

The underlying execution model stays 100% imperative -- `tokenize()` and `tally()` are still just as
mutating internally. What changes is that the logic now has a name, a boundary, and an independent
test surface, so `main()` shrinks to a readable sequence of calls (Example 2's `tokenize()`/`tally()`
refactor; Example 27's procedural `area_via_tag()`).

</details>

**Q3 (co-03 -- Structured Programming).** Why do sequence, selection, and iteration replace
`goto`-style jumps specifically, rather than just being "cleaner syntax"?

<details>
<summary>Answer</summary>

A `goto`-shaped jump (in Python, usually a boolean flag standing in for a jump target) can transfer
control from anywhere to anywhere, so understanding one line can require understanding the whole
program. Sequence, selection, and iteration each have exactly one entry and one exit, so a reader can
understand a block by reading its own lines, never hunting for where control jumped in from (Example 3
replaces a boolean goto flag with `if`/`elif`/`else`; Example 26 flattens a nested-`if` pyramid into
guard clauses).

</details>

**Q4 (co-04 -- Mutable State and Assignment).** What's the concrete difference between rebinding a name
and mutating an object through an alias, and why does conflating them cause bugs?

<details>
<summary>Answer</summary>

Rebinding (`x = 20`) points a name at a new object; mutating through an alias (`alias.append(4)`)
changes the SAME object every name pointing at it can see. An aliased mutable object can be changed by
code that has no visible connection to the code reading it later -- two names, one box (Example 4
demonstrates both directly; Example 53 dispatches transitions off a plain `enum.Enum`).

</details>

**Q5 (co-05 -- Object-Oriented Paradigm).** What does bundling state and behavior into an object buy
that a bare data structure plus a separate function does not?

<details>
<summary>Answer</summary>

Every method on a class has guaranteed access to that instance's own data without it being passed in
separately, and two instances of the same class never share state by accident. That isolation is what
makes encapsulation (co-06) possible in the first place (Example 6's `WordCounter` class; Example 30's
OO leg of the four-paradigm comparison).

</details>

**Q6 (co-06 -- Encapsulation as State Containment).** Why does forcing every mutation through a small
set of methods matter more than just "hiding" a field?

<details>
<summary>Answer</summary>

When every mutation is forced through `deposit()`/`withdraw()`, those methods become the ONLY place an
invariant (balance never negative) can be broken -- which means they're also the only place it needs
to be checked, tested, and trusted. Direct field access scatters that responsibility across every
caller instead (Example 7's `BankBalance` guards its invariant, and a rejected withdrawal is shown to
leave it intact).

</details>

**Q7 (co-07 -- Message-Passing vs Method Call).** Why can two unrelated classes with no shared base
class both respond correctly to the same message?

<details>
<summary>Answer</summary>

Structural typing (a `Protocol`) means the caller only needs to know the message SHAPE, never the
concrete class receiving it -- each receiver decides for itself how to respond. This is what makes
polymorphic dispatch work: the same call site produces different behavior depending purely on which
object receives the message at runtime (Example 8 sends `speak()` to an unrelated `Duck` and `Dog`).

</details>

**Q8 (co-08 -- Declarative vs Imperative).** What does the reader gain, and what do they have to trust
blindly, when code is declarative instead of imperative?

<details>
<summary>Answer</summary>

Declarative code hands the "how" to the language or engine, so the reader only verifies the "what" --
there's no accumulator variable or loop index to trace. The cost is that the "how" becomes opaque; you
trust the engine (a comprehension, a rules table, a SQL planner) to do it correctly (Example 9's
comprehension vs. loop; Example 54's declarative validation rules table).

</details>

**Q9 (co-09 -- Functional Paradigm Overview).** Why is a function that never mutates anything the
caller can observe "trivially safe" in a way an equivalent mutating loop is not?

<details>
<summary>Answer</summary>

A function that only reads its arguments and returns a new value is safe to call twice, safe to call
from multiple threads, and easy to test in isolation -- no setup beyond the arguments is ever needed
(Example 11's `Counter`/`reduce` word count with no visible mutation; Example 64's state rebuilt by
folding an event log).

</details>

**Q10 (co-10 -- Expressions vs Statements).** Why does "threading values through expressions" read
differently than "threading values through assigned variables," even when both compute the same
result?

<details>
<summary>Answer</summary>

An expression composes -- it can be passed as an argument, embedded in a larger expression, or
returned directly -- while a statement can only be executed for its effect. Chaining expressions is a
large part of what makes declarative code read as one flowing computation rather than a sequence of
steps (Example 12 contrasts a conditional expression against an `if`/assign block; Example 44's lazy
pipeline is built entirely from composed expressions).

</details>

**Q11 (co-11 -- Pure vs Impure).** What does "referentially transparent" mean concretely, and what
specifically breaks it?

<details>
<summary>Answer</summary>

A pure function called twice with the same argument always produces the same result and touches
nothing else -- it can be reasoned about, cached, and reused without knowing its calling context. Any
hidden effect (appending to a log, mutating an argument) breaks that guarantee even if the return value
looks identical (Example 13 contrasts `normalize()` against `normalize_and_log()`; Example 67 refactors
a mutation-heavy routine into a pure fold).

</details>

**Q12 (co-12 -- First-Class and Higher-Order Functions).** What becomes possible once functions are
ordinary values that can be passed as arguments?

<details>
<summary>Answer</summary>

Behavior itself becomes a parameter -- the same `apply_all(fn, items)` helper can double every item,
square every item, or apply an arbitrary lambda, all without `apply_all`'s own code changing at all.
This is the seed that grows into decorators, callbacks, and strategy objects (Example 14 passes
`double`, `square`, and a lambda into the same helper).

</details>

**Q13 (co-13 -- Logic Programming).** What's the fundamental mental-model shift from "write the
algorithm that finds the answer" to logic programming?

<details>
<summary>Answer</summary>

In a logic program you state relationships (facts and rules) and ask questions; the engine's search
finds answers you never explicitly computed -- "who is Alice's grandchild" was never stored anywhere,
yet the query resolves it (Example 19 infers a grandparent relationship via composed facts; Example 60
builds a mini backtracking engine resolving a transitive-closure query).

</details>

**Q14 (co-14 -- Unification and Backtracking).** What does "backtrack" mean mechanically, and why does
skipping it corrupt a search?

<details>
<summary>Answer</summary>

Backtracking means: try a candidate binding, recurse deeper, and if that path fails, UNDO the choice
before trying the next candidate. Skip the undo and a rejected choice leaks into sibling branches that
never should have seen it, producing a wrong or oversized result (Example 37's N-Queens
`is_safe()`/`backtrack()` pair; Kata 6 reproduces exactly this bug by omitting the pop).

</details>

**Q15 (co-15 -- Constraint Programming).** Why does one generic `CSPSolver` work unchanged across map
coloring, Sudoku, and scheduling?

<details>
<summary>Answer</summary>

Separating "what must be true" (the declared constraints) from "how to search for it" (the solver)
means the same solver reuses across entirely different puzzles -- only the variables, domains, and
constraints change (Example 61's generic `CSPSolver` reused for map coloring and a Latin-square
puzzle; Example 71 schedules tasks under precedence constraints).

</details>

**Q16 (co-16 -- Event-Driven Paradigm).** What's the control-flow inversion that defines event-driven
code, and what do you give up in exchange?

<details>
<summary>Answer</summary>

In you-call-library code, your code decides exactly when things happen; in event-driven code, the
framework decides when your handler runs, based on events it observes. You give up control of the
timeline in exchange for not writing the loop that watches for events yourself (Example 45 contrasts
both control-flow shapes directly; Example 55's typed publish/subscribe bus).

</details>

**Q17 (co-17 -- Reactive Programming).** What entire bug class does automatic reactive propagation
eliminate?

<details>
<summary>Answer</summary>

"I changed A but forgot to also update the thing that depends on A" -- reactive propagation makes the
dependency wiring itself responsible for keeping derived values current, automatically, every time
(Example 17's `ObservableValue` pushes to subscribers on `set()`; Example 42 contrasts a
manually-maintained derived value that goes stale against the same thing done reactively).

</details>

**Q18 (co-18 -- Dataflow Programming).** What can a scheduler do with a computation expressed as a
dependency graph that it cannot do with a fixed, hand-written sequence of steps?

<details>
<summary>Answer</summary>

It can find independent nodes and run them in parallel, skip recomputing nodes whose inputs never
changed (memoization), and reorder execution freely as long as every edge is respected -- none of
which a fixed sequence gives you for free (Example 43 executes a DAG in topological order; Example 57
memoizes dataflow nodes, skipping recompute on an unchanged subtree).

</details>

**Q19 (co-19 -- Relational/Set-Based Thinking).** Why does a declared relational query stay fast
regardless of dataset size, while a hand-written nested loop's performance is locked in?

<details>
<summary>Answer</summary>

Relational operations (select, project, join) compose freely and are optimizable by a query planner
precisely because they're declared as set operations rather than a specific loop order -- the same
declared query can run efficiently at any scale, while a hand-written loop's performance is fixed by
the loop structure you wrote (Example 15's SQL top-3-words query; Example 47 contrasts a SQL `JOIN`
against an equivalent nested loop).

</details>

**Q20 (co-20 -- Multi-Paradigm Languages).** Why does a language blending several paradigms make BOTH
good judgment and paradigm soup equally easy to write?

<details>
<summary>Answer</summary>

Python doesn't force a single paradigm -- a genuine strength -- but that also means the discipline of
choosing ONE paradigm per boundary (co-25) has to come from the developer, not the language (Example 20
mixes a class, a comprehension, and a generator in one script; Example 78's comparison matrix across
every paradigm solution built in this topic).

</details>

**Q21 (co-21 -- Paradigm as Constraint Buys Property).** What's the topic's central abstraction for
understanding every paradigm at once?

<details>
<summary>Answer</summary>

Each paradigm trades a constraint for a guarantee -- purity buys reasoning, immutability buys safe
sharing, encapsulation buys change isolation, declarative style buys optimizability. Naming the
specific constraint and the specific property it buys turns "which paradigm should I use" into an
engineering question, not a taste question (Example 21 shares a frozen `tuple`/`frozenset` and confirms
neither function can mutate it).

</details>

**Q22 (co-22 -- State as the Fault Line).** Why is "where does mutable state live, and who's allowed to
touch it" described as the fault line every other concept in this topic runs along?

<details>
<summary>Answer</summary>

OO's encapsulated instance state, functional programming's insistence on no shared mutable state,
reactive programming's automatic propagation instead of manual mutation -- every one of those
distinctions is ultimately a different answer to that same question (Example 22 contrasts a
mutable-global running total against an immutable fold; Example 74 reproduces a real data race from
shared mutable state under two threads and shows the immutable-design twin has none).

</details>

**Q23 (co-23 -- Matching Paradigm to Problem).** What does "fluency in matching" mean, as opposed to
"loyalty to one paradigm"?

<details>
<summary>Answer</summary>

Recognizing the shape a problem already has -- search-and-satisfy fits constraint programming, a UI
that must stay synchronized fits reactive, a batch transformation with no shared state fits functional
-- and reaching for the paradigm built for that shape, rather than forcing every problem into one
default lens (Example 66's decision table; Example 80's final choose-and-defend grounded in this
topic's own code).

</details>

**Q24 (co-24 -- Paradigm Cost and Tradeoff).** Why is naming a paradigm's benefit without naming its
cost "marketing, not engineering"?

<details>
<summary>Answer</summary>

Every paradigm's benefit is paid for with a specific cost -- readability, testability, or change-cost.
A comprehension is fewer lines but hides the "how"; a constraint solver reuses across problems but
costs more to write the first time. Every contrast example in this topic is really asking "which cost
am I willing to pay here" (Example 58 measures lines-of-code trade-offs directly; Example 79 measures a
concrete performance cost of immutability).

</details>

**Q25 (co-25 -- Mixing Paradigms at Boundaries).** What's the actual difference between legitimate
multi-paradigm code and "paradigm soup"?

<details>
<summary>Answer</summary>

Discipline at the boundary: know which side of a function call is "the functional part" and which is
"the OO part," and never let a paradigm's guarantee (like "this value can't be mutated") get silently
violated by code that only LOOKS like it respects that guarantee (Example 49 crosses a
functional-to-OO boundary passing only immutable data; Example 50 reproduces the paradigm-soup failure
mode directly -- a mutable object aliased and silently corrupted through a "functional-looking" chain).

</details>

## Applied problems

Ten scenarios. Each describes a task without naming the paradigm -- decide which concept applies, then
check.

**AP1.** A `for` loop's exit condition depends on a boolean flag that a nested `if`, three levels deep,
sets on one specific iteration -- and a teammate just spent twenty minutes tracing where that flag gets
set before they could trust the loop's exit behavior.

<details>
<summary>Answer</summary>

This is a structured-programming violation (co-03) -- the flag is a `goto`-style jump target standing
in for a proper exit. Replace it with the specific construct that actually needs to fire: an early
`return`, a `break` at the point of decision, or a `continue` scoped to just that iteration, so a
reader never has to hunt for where control "jumped in from" (Example 26; Kata 2).

</details>

**AP2.** Two functions compute the identical checkout total from the identical inputs, but one of them
also silently appends a line to a shared `audit_log` list every time it's called -- and a caller who
calls it twice to redisplay a total on screen doubles the log.

<details>
<summary>Answer</summary>

This is a pure-vs-impure boundary problem (co-11) -- the "total" computation and the "log an audit
entry" side effect are two different responsibilities wearing one function's name. Split them: a pure
`compute_total()` safe to call any number of times, and an explicit, separately-called `log_audit()`
(Example 13; Kata 1's mutable-default variant of the same "hidden side effect" family).

</details>

**AP3.** A UI panel shows "3 items in cart," but after removing an item the panel still says "3" until
the page is manually refreshed -- the underlying `items` list is correct; only the displayed number is
wrong.

<details>
<summary>Answer</summary>

This is a reactive-programming gap (co-17) -- `total` (or the displayed count) is stored as a plain
field kept "in sync" by hand at every call site that touches `items`, and one call site was missed.
Making the count a computed property (or a subscriber pushed to on every `items` change) makes it
structurally impossible to forget (Example 42; Kata 4).

</details>

**AP4.** A puzzle-solving routine explores placements one at a time, and when a placement turns out to
be invalid several moves later, the routine's next attempt inexplicably starts from a board state that
still has the invalid piece sitting on it.

<details>
<summary>Answer</summary>

This is a backtracking violation (co-14) -- a failed branch must undo (pop, unset) its choice before
trying the alternative. Without the undo, state from a REJECTED branch leaks into the next branch tried
(Example 37's N-Queens; Kata 6 reproduces this exact bug with a missing `chosen.pop()`).

</details>

**AP5.** A dispatcher processes a queue of pending events, and events fired as a SIDE EFFECT of
processing an earlier event in the same batch (a signup that should trigger a welcome email) never get
processed at all -- yet the queue variable clearly has them appended.

<details>
<summary>Answer</summary>

This is an event-driven-paradigm violation (co-16) -- the dispatch loop iterates a frozen snapshot of
the queue taken at loop start, rather than draining the live queue. Replace the snapshot iteration with
a `while queue:` drain so events appended mid-dispatch are also seen (Example 40; Kata 7).

</details>

**AP6.** A node in a computation graph caches its result the first time it's computed, and a change to
one of its declared inputs later in the program has zero effect on what that node returns when asked
again.

<details>
<summary>Answer</summary>

This is a dataflow-programming violation (co-18) -- a memoized node must be invalidated (or its
staleness detected) whenever a dependency it's declared to depend on actually changes; caching once and
never checking again silently breaks the "recompute on change" contract dataflow depends on (Example
57's correctly-memoized nodes; Kata 8 reproduces the stale-cache bug directly).

</details>

**AP7.** Four threads each increment what's supposed to be a running total 200,000 times, and the final
total is consistently and reproducibly lower than the arithmetic would predict, even though every
individual increment "looks correct" in isolation.

<details>
<summary>Answer</summary>

This is state-as-the-fault-line (co-22) -- a shared mutable cell's read-modify-write is not atomic, so
two threads can interleave and lose an update. The fix is not a bigger lock budget; it's removing the
shared mutable target entirely: give each thread its own private slot and combine with a pure fold only
after every thread finishes (Example 74; Kata 9).

</details>

**AP8.** A code review flags a `map()`-based pipeline as "not actually functional" even though every
individual function in the chain returns a value and looks side-effect-free at a glance.

<details>
<summary>Answer</summary>

This is paradigm soup (co-25) -- somewhere in the chain a closure captures and mutates state that
outlives a single call (a module-level list, a mutable default argument), so calling the SAME pipeline
twice with the SAME input produces different results. A genuinely pure pipeline depends only on its own
arguments, nothing else (Example 50; Kata 10).

</details>

**AP9.** A scheduling problem (which task runs on which day, respecting "task B must follow task A" and
"only one task per resource per day") is currently solved with three hand-nested loops and a growing
pile of special-case `if`s for every new rule that gets added.

<details>
<summary>Answer</summary>

This calls for constraint programming (co-15) -- declare the precedence and single-resource-per-day
rules as constraints and hand them to a generic solver, instead of hand-encoding the search as nested
loops. A new rule becomes "add a constraint," not "add another special-case `if` to an already-deep
loop nest" (Example 61's generic `CSPSolver`; Example 71's task scheduling).

</details>

**AP10.** A fifteen-line one-off script that reads a CSV and prints a total gets rewritten by a
well-meaning teammate into a `Strategy`-pattern hierarchy with an abstract base class, a factory, and
three concrete implementations -- for a computation that will only ever be run once.

<details>
<summary>Answer</summary>

This is paradigm cost ignored (co-24), and specifically the "choose the paradigm whose grain fits the
problem" skill (co-23) applied backwards -- the script's actual shape (read, sum, print, done) needs no
paradigm machinery at all. Naming a pattern's benefit without weighing its cost against a problem this
small is exactly the mistake co-24 warns about (Example 28's explicit "paradigm choice is noise" case).

</details>

## Code katas

Ten hands-on repetition drills. Each is a before/after `.py` file colocated under `drilling/code/`.
Every "before" script is a real, runnable Python program that misapplies the concept being drilled --
run it yourself, diagnose the bug from the observed behavior, fix it from memory, then compare your fix
against the "after" script and the model solution before checking your work against the
actually-executed output shown.

### Kata 1 -- mutable state: a default argument is silently shared across every instance

_relates to co-04, Example 4_

**Task.** `WordCounter()` with no arguments should start with a fresh, empty `words` list every time
it's constructed. The version below is broken: two DIFFERENT instances end up sharing the SAME list.

**Before** (`drilling/code/kata-01-mutable-default-aliasing/before/kata.py`)

```python
"""Kata 1 (before): mutable-state aliasing bug -- a mutable default argument is shared across calls."""


class WordCounter:
    def __init__(self, words: list[str] = []) -> None:  # SMELL: mutable default shared across every instance
        self.words = words

    def add(self, word: str) -> None:
        self.words.append(word)


first = WordCounter()
first.add("alpha")
second = WordCounter()  # meant to start EMPTY -- but shares the same default list object as `first`
second.add("beta")
print(first.words)
print(second.words)
```

**Observed (buggy) output** (captured by actually running the script above):

```text
['alpha', 'beta']
['alpha', 'beta']
```

**After** (`drilling/code/kata-01-mutable-default-aliasing/after/kata.py`)

```python
"""Kata 1 (after): mutable-state aliasing bug fixed -- each instance gets its own fresh list."""


class WordCounter:
    def __init__(self, words: list[str] | None = None) -> None:
        self.words: list[str] = words if words is not None else []  # fresh list per instance, never shared

    def add(self, word: str) -> None:
        self.words.append(word)


first = WordCounter()
first.add("alpha")
second = WordCounter()
second.add("beta")
print(first.words)
print(second.words)
```

<details>
<summary>Model solution</summary>

**Root cause**: Python evaluates a default argument expression exactly ONCE, at function-definition
time -- not once per call. `[]` is created a single time and every call that omits `words` receives
that SAME list object. The fix uses `None` as a sentinel and constructs a genuinely fresh `[]` inside
the body, on every call.

**Run**: `python3 kata.py`

**Output**:

```text
['alpha']
['beta']
```

</details>

### Kata 2 -- structured programming: a goto-style flag leaks past its intended scope

_relates to co-03, Example 26_

**Task.** `process_orders()` should skip only orders that are themselves refunded, and process every
other order normally. The version below is broken: a flag meant to skip ONE refunded order never gets
reset, so it silently skips every order that comes after it too.

**Before** (`drilling/code/kata-02-goto-flag-leak/before/kata.py`)

```python
"""Kata 2 (before): structured-programming violation -- a goto-style flag leaks past its intended scope."""


def process_orders(orders: list[dict[str, object]]) -> list[str]:
    processed: list[str] = []
    skip = False  # SMELL: this flag is meant to skip ONE refunded order, but nothing ever resets it
    for order in orders:
        if order["refunded"]:
            skip = True  # goto-style: "jump past" this one order
        if skip:
            continue  # BUG: skip is never turned back off, so every order AFTER the first refund is also skipped
        processed.append(str(order["id"]))
    return processed


orders: list[dict[str, object]] = [
    {"id": "A", "refunded": False},
    {"id": "B", "refunded": True},
    {"id": "C", "refunded": False},  # should still be processed -- it was never refunded
]
print(process_orders(orders))
```

**Observed (buggy) output** (captured by actually running the script above):

```text
['A']
```

**After** (`drilling/code/kata-02-goto-flag-leak/after/kata.py`)

```python
"""Kata 2 (after): structured-programming fix -- a per-iteration `continue` replaces the leaking flag."""


def process_orders(orders: list[dict[str, object]]) -> list[str]:
    processed: list[str] = []
    for order in orders:
        if order["refunded"]:  # decision scoped to THIS iteration only -- nothing leaks to the next one
            continue
        processed.append(str(order["id"]))
    return processed


orders: list[dict[str, object]] = [
    {"id": "A", "refunded": False},
    {"id": "B", "refunded": True},
    {"id": "C", "refunded": False},
]
print(process_orders(orders))
```

<details>
<summary>Model solution</summary>

**Root cause**: `skip` is a variable that outlives the single iteration it was meant to govern -- a
`goto`-style stand-in for "jump past this one order" that structured programming's single-entry/single-
exit constructs make unnecessary. A `continue` scoped to the current iteration expresses the SAME
intent without any state that can leak into later iterations.

**Run**: `python3 kata.py`

**Output**:

```text
['A', 'C']
```

</details>

### Kata 3 -- encapsulation: direct field mutation bypasses the invariant

_relates to co-06, Example 7_

**Task.** A `BankBalance` should never go negative -- `withdraw()` already guards that invariant. The
version below is broken: the balance is a public field, so code outside the class can change it without
ever calling `withdraw()`, bypassing the guard entirely.

**Before** (`drilling/code/kata-03-encapsulation-bypass/before/kata.py`)

```python
"""Kata 3 (before): encapsulation violation -- direct field mutation bypasses the never-negative invariant."""


class BankBalance:
    def __init__(self, amount: int) -> None:
        self.balance = amount  # SMELL: public field -- nothing stops direct mutation

    def withdraw(self, amount: int) -> bool:
        if self.balance - amount < 0:
            return False
        self.balance -= amount
        return True


account = BankBalance(50)
account.balance = account.balance - 100  # BUG: bypasses withdraw()'s guard entirely
print(account.balance)
```

**Observed (buggy) output** (captured by actually running the script above):

```text
-50
```

**After** (`drilling/code/kata-03-encapsulation-bypass/after/kata.py`)

```python
"""Kata 3 (after): encapsulation fix -- state hidden behind methods, the invariant can't be bypassed."""


class BankBalance:
    def __init__(self, amount: int) -> None:
        self._balance = amount  # underscore-prefixed -- convention signals "route through methods only"

    def withdraw(self, amount: int) -> bool:
        if self._balance - amount < 0:
            return False
        self._balance -= amount
        return True

    def read(self) -> int:
        return self._balance


account = BankBalance(50)
succeeded = account.withdraw(100)  # the ONLY way to change balance -- and it correctly refuses
print(succeeded)
print(account.read())
```

<details>
<summary>Model solution</summary>

**Root cause**: a public field is an open door -- ANY code with a reference to the object can mutate it
without going through the method that enforces the invariant. Renaming the field `_balance` and
exposing only `withdraw()`/`read()` makes the invariant-checking method the ONLY path that can ever
change the value.

**Run**: `python3 kata.py`

**Output**:

```text
False
50
```

</details>

### Kata 4 -- reactive programming: a manually maintained derived value goes stale

_relates to co-17, Example 42_

**Task.** `cart.total` should always equal the sum of `cart.items`. The version below is broken:
`total` is a plain field updated by hand inside `add_item()`, and the symmetric update was forgotten
inside `remove_item()`.

**Before** (`drilling/code/kata-04-reactive-stale-derived/before/kata.py`)

```python
"""Kata 4 (before): reactive-programming violation -- a manually maintained derived value goes stale."""


class Cart:
    def __init__(self) -> None:
        self.items: list[int] = []
        self.total = 0  # SMELL: a derived value stored as a plain field, kept "in sync" by hand

    def add_item(self, price: int) -> None:
        self.items.append(price)
        self.total = sum(self.items)  # easy to forget this line at ANY future call site

    def remove_item(self, price: int) -> None:
        self.items.remove(price)  # BUG: forgot to also update self.total here


cart = Cart()
cart.add_item(10)
cart.add_item(20)
cart.remove_item(10)
print(cart.items)
print(cart.total)  # stale -- still reflects the removed item
```

**Observed (buggy) output** (captured by actually running the script above):

```text
[20]
30
```

**After** (`drilling/code/kata-04-reactive-stale-derived/after/kata.py`)

```python
"""Kata 4 (after): reactive fix -- total is a computed property, impossible to forget updating."""


class Cart:
    def __init__(self) -> None:
        self.items: list[int] = []

    @property
    def total(self) -> int:
        return sum(self.items)  # ALWAYS current -- there is no separate field that could go stale

    def add_item(self, price: int) -> None:
        self.items.append(price)

    def remove_item(self, price: int) -> None:
        self.items.remove(price)


cart = Cart()
cart.add_item(10)
cart.add_item(20)
cart.remove_item(10)
print(cart.items)
print(cart.total)
```

<details>
<summary>Model solution</summary>

**Root cause**: `total` was a plain field, so keeping it in sync depended on every mutating method
remembering to also update it -- a manual contract with no enforcement. Making `total` a `@property`
that recomputes from `items` every time it's read removes the separate field entirely; there is nothing
left that could ever go stale.

**Run**: `python3 kata.py`

**Output**:

```text
[20]
20
```

</details>

### Kata 5 -- purity: a function that looks pure secretly mutates its input

_relates to co-11, Example 13_

**Task.** `sorted_scores()` should return a new, sorted list without changing the caller's original
list. The version below is broken: it sorts the list IN PLACE, so the caller's `original` is silently
changed too.

**Before** (`drilling/code/kata-05-impure-mutates-input/before/kata.py`)

```python
"""Kata 5 (before): purity violation -- a function that LOOKS pure secretly mutates its input."""


def sorted_scores(scores: list[int]) -> list[int]:
    scores.sort()  # BUG: list.sort() mutates IN PLACE -- the caller's list is silently changed too
    return scores


original = [3, 1, 2]
result = sorted_scores(original)
print(result)
print(original)  # SMELL: caller never asked for `original` to change, but it did
```

**Observed (buggy) output** (captured by actually running the script above):

```text
[1, 2, 3]
[1, 2, 3]
```

**After** (`drilling/code/kata-05-impure-mutates-input/after/kata.py`)

```python
"""Kata 5 (after): purity fix -- `sorted()` returns a NEW list, the caller's input is untouched."""


def sorted_scores(scores: list[int]) -> list[int]:
    return sorted(scores)  # pure -- builds and returns a new list, never touches the argument


original = [3, 1, 2]
result = sorted_scores(original)
print(result)
print(original)  # unchanged -- proves the function is referentially transparent
```

<details>
<summary>Model solution</summary>

**Root cause**: `list.sort()` mutates its receiver in place and returns `None` -- calling it on the
argument the caller passed in changes THEIR list, not a copy. `sorted()` builds and returns a brand-new
list, leaving the argument completely untouched, which is what makes the function safe to call without
worrying about the caller's data.

**Run**: `python3 kata.py`

**Output**:

```text
[1, 2, 3]
[3, 1, 2]
```

</details>

### Kata 6 -- backtracking: a failed branch never undoes its choice

_relates to co-14, Example 37_

**Task.** `find_subset([5, 3, 2], 2)` should return `[2]` -- the only subset of the given numbers that
sums to 2. The version below is broken: it forgets to undo (pop) a rejected number before trying the
"exclude this number" branch, so the rejected number stays in the result.

**Before** (`drilling/code/kata-06-backtracking-forgets-undo/before/kata.py`)

```python
"""Kata 6 (before): backtracking violation -- a failed branch never undoes its choice before retrying."""


def find_subset(numbers: list[int], target: int) -> list[int] | None:
    chosen: list[int] = []

    def backtrack(index: int, remaining: int) -> bool:
        if remaining == 0:
            return True
        if index >= len(numbers) or remaining < 0:
            return False
        chosen.append(numbers[index])  # try INCLUDING this number
        if backtrack(index + 1, remaining - numbers[index]):
            return True
        # BUG: no chosen.pop() here -- the rejected number stays in `chosen` when we try EXCLUDING it
        return backtrack(index + 1, remaining)

    if backtrack(0, target):
        return chosen
    return None


result = find_subset([5, 3, 2], 2)
print(result)  # correct answer is [2] -- watch what the missing undo actually returns
```

**Observed (buggy) output** (captured by actually running the script above):

```text
[5, 3, 2]
```

**After** (`drilling/code/kata-06-backtracking-forgets-undo/after/kata.py`)

```python
"""Kata 6 (after): backtracking fix -- a failed branch undoes (pops) its choice before trying the alternative."""


def find_subset(numbers: list[int], target: int) -> list[int] | None:
    chosen: list[int] = []

    def backtrack(index: int, remaining: int) -> bool:
        if remaining == 0:
            return True
        if index >= len(numbers) or remaining < 0:
            return False
        chosen.append(numbers[index])
        if backtrack(index + 1, remaining - numbers[index]):
            return True
        chosen.pop()  # undo the rejected choice BEFORE trying the "exclude this number" branch
        return backtrack(index + 1, remaining)

    if backtrack(0, target):
        return chosen
    return None


result = find_subset([5, 3, 2], 2)
print(result)
```

<details>
<summary>Model solution</summary>

**Root cause**: `chosen.append()` mutates a SHARED list across the entire recursive search tree. When
an inclusion branch fails, the number appended for that branch is still sitting in `chosen` when the
sibling "exclude" branch runs -- `chosen.pop()` is what removes it, restoring `chosen` to exactly the
state it had before the rejected choice was tried.

**Run**: `python3 kata.py`

**Output**:

```text
[2]
```

</details>

### Kata 7 -- event-driven: a snapshot iteration drops events fired during processing

_relates to co-16, Example 40_

**Task.** `run_dispatcher(["signup", "login"])` should also process a `"welcome_email"` event fired as
a side effect of handling `"signup"`. The version below is broken: it iterates a frozen snapshot of the
queue taken at loop start, so anything appended mid-loop is never seen.

**Before** (`drilling/code/kata-07-event-snapshot-drops-events/before/kata.py`)

```python
"""Kata 7 (before): event-driven violation -- a snapshot iteration drops events fired during processing."""


def run_dispatcher(initial_events: list[str]) -> list[str]:
    queue = list(initial_events)
    processed: list[str] = []
    for event in list(queue):  # SMELL: `list(queue)` takes a frozen snapshot at loop start
        processed.append(event)
        if event == "signup":
            queue.append("welcome_email")  # BUG: appended to `queue`, but the loop iterates the SNAPSHOT, not `queue`
    return processed


print(run_dispatcher(["signup", "login"]))
```

**Observed (buggy) output** (captured by actually running the script above):

```text
['signup', 'login']
```

**After** (`drilling/code/kata-07-event-snapshot-drops-events/after/kata.py`)

```python
"""Kata 7 (after): event-driven fix -- draining the live queue processes events added during dispatch too."""


def run_dispatcher(initial_events: list[str]) -> list[str]:
    queue = list(initial_events)
    processed: list[str] = []
    while queue:  # keeps going as long as ANY event -- including ones added mid-dispatch -- remains
        event = queue.pop(0)
        processed.append(event)
        if event == "signup":
            queue.append("welcome_email")
    return processed


print(run_dispatcher(["signup", "login"]))
```

<details>
<summary>Model solution</summary>

**Root cause**: `list(queue)` copies the queue's CURRENT contents once, at loop start -- the `for` loop
then walks that frozen copy, completely disconnected from any later appends to `queue` itself.
Replacing the snapshot iteration with `while queue: event = queue.pop(0)` drains the LIVE queue, so an
event appended mid-dispatch is picked up on a later trip through the loop.

**Run**: `python3 kata.py`

**Output**:

```text
['signup', 'login', 'welcome_email']
```

</details>

### Kata 8 -- dataflow: a memoized node is never invalidated when its input changes

_relates to co-18, Example 57_

**Task.** `Doubler.total_doubled()` should reflect the CURRENT contents of `source`, including changes
made after the first call. The version below is broken: it caches its result once and never checks
whether `source` has changed since.

**Before** (`drilling/code/kata-08-dataflow-stale-memo/before/kata.py`)

```python
"""Kata 8 (before): dataflow violation -- a memoized node is never invalidated when its input changes."""


class Doubler:
    def __init__(self, source: list[int]) -> None:
        self.source = source
        self._cache: int | None = None  # SMELL: cached once, nothing ever clears it

    def total_doubled(self) -> int:
        if self._cache is None:
            self._cache = sum(n * 2 for n in self.source)
        return self._cache  # BUG: returns the STALE cached value even after `source` has changed


doubler = Doubler([1, 2, 3])
print(doubler.total_doubled())  # correct: 12
doubler.source.append(10)  # dependency changed
print(doubler.total_doubled())  # should be 32, but the stale cache still says 12
```

**Observed (buggy) output** (captured by actually running the script above):

```text
12
12
```

**After** (`drilling/code/kata-08-dataflow-stale-memo/after/kata.py`)

```python
"""Kata 8 (after): dataflow fix -- the node recomputes whenever its source has actually changed."""


class Doubler:
    def __init__(self, source: list[int]) -> None:
        self.source = source
        self._cache: int | None = None
        self._cached_length = -1  # tracks the source length the cache was computed FOR

    def total_doubled(self) -> int:
        if self._cache is None or self._cached_length != len(self.source):  # dependency changed -> stale
            self._cache = sum(n * 2 for n in self.source)
            self._cached_length = len(self.source)
        return self._cache


doubler = Doubler([1, 2, 3])
print(doubler.total_doubled())
doubler.source.append(10)
print(doubler.total_doubled())
```

<details>
<summary>Model solution</summary>

**Root cause**: `_cache is None` is the ONLY staleness check, and once the cache is populated it's
`None` never again -- there is no mechanism that notices `source` changed. Tracking a cheap signal of
the dependency's state (here, its length) and recomputing whenever that signal disagrees with what the
cache was built for is a minimal, real dataflow "dirty check."

**Run**: `python3 kata.py`

**Output**:

```text
12
32
```

</details>

### Kata 9 -- state fault line: two threads share one mutable counter and lose an update

_relates to co-22, Example 74_

**Task.** Two threads should each record one page view, for a total of 2. The version below is broken:
both threads read the SAME stale value before either writes, so one increment is silently lost -- and
this reproduces the SAME way every single run, via the deterministic `threading.Event` handshake
Example 74 uses.

**Before** (`drilling/code/kata-09-shared-mutable-race/before/kata.py`)

```python
"""Kata 9 (before): state-fault-line violation -- two threads share one mutable counter and lose an update."""

import threading


class PageViewCounter:
    def __init__(self) -> None:
        self.views = 0  # SMELL: one shared mutable box, read-then-written by two threads


def record_view(counter: PageViewCounter, read_done: threading.Event, may_write: threading.Event) -> None:
    current = counter.views  # STEP 1: read the shared value
    read_done.set()  # signal "I have read" -- forces a specific, deterministic interleaving
    may_write.wait()  # STEP 2: wait until it's safe to write (forces the race window open)
    counter.views = current + 1  # BUG: STEP 3 writes back based on the STALE value read in step 1


counter = PageViewCounter()
event_a_read = threading.Event()
event_b_read = threading.Event()
thread_a = threading.Thread(target=record_view, args=(counter, event_a_read, event_b_read))
thread_b = threading.Thread(target=record_view, args=(counter, event_b_read, event_a_read))
# Each thread waits on the OTHER thread's "read done" signal before it's allowed to write -- this
# deterministically forces BOTH threads to read 0 before EITHER of them writes 1, every single run.
thread_a.start()
thread_b.start()
thread_a.join()
thread_b.join()

print(counter.views)  # two views were recorded, but only ONE survived -- a lost update
```

**Observed (buggy) output** (captured by actually running the script above, five times in a row --
deterministic, not a coin flip):

```text
1
```

**After** (`drilling/code/kata-09-shared-mutable-race/after/kata.py`)

```python
"""Kata 9 (after): state-fault-line fix -- each thread owns a private slot; combine with a pure fold at the end."""

import threading

results: list[int] = [0, 0]  # each thread writes to its OWN index -- never the same memory location


def record_view(index: int) -> None:
    results[index] = 1  # a single write to a private slot -- nothing else can read or write it mid-flight


thread_a = threading.Thread(target=record_view, args=(0,))
thread_b = threading.Thread(target=record_view, args=(1,))
thread_a.start()
thread_b.start()
thread_a.join()
thread_b.join()

total_views = sum(results)  # combine ONLY after both threads finished -- no concurrent write to `total_views`
print(total_views)  # both views correctly counted, every single run
```

<details>
<summary>Model solution</summary>

**Root cause**: `counter.views` is one shared mutable cell; a read-then-write is not atomic, and the
`threading.Event` handshake deterministically forces BOTH threads to read the stale value `0` before
EITHER writes `1` -- so the second write simply overwrites the first with the same value, and one
increment vanishes. The fix removes the shared mutable target entirely: each thread owns a disjoint
slot in `results`, and the two counts are combined with a pure `sum()` only after both threads have
finished -- there is no memory location either thread could ever race on.

**Run**: `python3 kata.py`

**Output**:

```text
2
```

</details>

### Kata 10 -- paradigm soup: a `map`-based pipeline secretly mutates shared state

_relates to co-25, Example 50_

**Task.** Calling `build_report(rows)` twice with the identical `rows` should produce identical
results -- that's what "functional-looking" code implies. The version below is broken: `enrich()`
looks like a pure `map()` callback, but it secretly depends on and mutates module-level state, so the
second call disagrees with the first.

**Before** (`drilling/code/kata-10-paradigm-soup-hidden-state/before/kata.py`)

```python
"""Kata 10 (before): paradigm-soup violation -- a `map`-based pipeline secretly mutates shared MODULE state."""

from typing import cast

_seen_ids: list[int] = []  # SMELL: module-level mutable state captured by a "functional-looking" map


def enrich(row: dict[str, object]) -> dict[str, object]:
    _seen_ids.append(cast(int, row["id"]))  # BUG: side effect hidden inside what looks like a pure transform
    return {"id": row["id"], "seen_count": len(_seen_ids)}


def build_report(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return list(map(enrich, rows))


rows: list[dict[str, object]] = [{"id": 1}, {"id": 2}]
report_a = build_report(rows)
report_b = build_report(rows)  # same input, called again
print([r["seen_count"] for r in report_a])
print([r["seen_count"] for r in report_b])  # BUG: NOT equal to report_a -- proves it's not referentially transparent
```

**Observed (buggy) output** (captured by actually running the script above):

```text
[1, 2]
[3, 4]
```

**After** (`drilling/code/kata-10-paradigm-soup-hidden-state/after/kata.py`)

```python
"""Kata 10 (after): paradigm-soup fix -- the transform depends ONLY on its own arguments, no shared state."""


def enrich(row: dict[str, object], index: int) -> dict[str, object]:
    return {"id": row["id"], "seen_count": index + 1}  # depends only on its OWN inputs -- no closure, no shared list


def build_report(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [enrich(row, i) for i, row in enumerate(rows)]  # pure -- same input always produces same output


rows: list[dict[str, object]] = [{"id": 1}, {"id": 2}]
report_a = build_report(rows)
report_b = build_report(rows)
print([r["seen_count"] for r in report_a])
print([r["seen_count"] for r in report_b])  # now IDENTICAL -- referentially transparent
```

<details>
<summary>Model solution</summary>

**Root cause**: `enrich()` reads its "how many seen so far" number from module-level `_seen_ids`,
mutated as a side effect of every call, EVER -- across BOTH invocations of `build_report()`. It looks
functional (it's passed to `map()`, it returns a value) but it is not pure, because its result depends
on something other than its own argument. Passing the index explicitly (`enumerate`) makes the same
information available WITHOUT any shared, mutated state.

**Run**: `python3 kata.py`

**Output**:

```text
[1, 2]
[1, 2]
```

</details>

## Self-check checklist

Work through this list without looking anything up. Every item should be something you can do from
memory, not something you'd need to search for.

**Imperative, procedural, structured, mutable state**

- [ ] I can identify code as imperative by its explicit, mutating, step-by-step statements, and name
      the specific tracing cost that buys (co-01).
- [ ] I can refactor an inline imperative block into named procedures without changing the underlying
      execution model at all (co-02).
- [ ] I can replace a `goto`-style boolean flag or a nested-`if` pyramid with plain sequence,
      selection, and iteration (co-03).
- [ ] I can distinguish rebinding a name from mutating an object through an alias, and explain why
      conflating them causes bugs (co-04).

**OO and declarative/functional**

- [ ] I can bundle state and the behavior that acts on it into a class, and explain what isolation
      that buys over a bare data structure plus a separate function (co-05).
- [ ] I can force every mutation of an object's state through a small set of methods so an invariant
      has exactly one place it can be checked (co-06).
- [ ] I can send the same message shape to two unrelated classes via structural typing and get correct
      polymorphic dispatch (co-07).
- [ ] I can state a computation declaratively (a comprehension, a rules table, a query) and name what
      the reader trusts blindly in exchange (co-08).
- [ ] I can write a pure, immutable computation using `Counter`/`reduce` instead of a mutating loop
      (co-09).
- [ ] I can thread a value through composed expressions instead of a sequence of assigned-variable
      statements (co-10).
- [ ] I can name the specific hidden effect that turns a pure-looking function into an impure one
      (co-11).
- [ ] I can pass a function as an ordinary value into a higher-order helper, making behavior itself a
      parameter (co-12).

**Logic, constraint, event, reactive, dataflow**

- [ ] I can state facts and rules and let an engine's search resolve a query I never explicitly
      computed (co-13).
- [ ] I can explain what "backtrack" means mechanically and correctly undo a rejected choice before
      trying the alternative (co-14).
- [ ] I can separate "what must be true" (constraints) from "how to search for it" (a generic solver)
      and reuse one solver across different puzzles (co-15).
- [ ] I can register a handler and explain the you-call-library vs framework-calls-you control-flow
      inversion (co-16).
- [ ] I can make a derived value recompute automatically on a source change instead of manually
      maintaining it (co-17).
- [ ] I can express a computation as a dependency graph and explain what a scheduler gains over a
      fixed, hand-written sequence (co-18).

**Relational and multi-paradigm**

- [ ] I can state a query as a declared set operation (select/project/join) instead of a hand-written
      nested loop (co-19).
- [ ] I can name the specific discipline a multi-paradigm language like Python demands from the
      developer, since the language itself won't enforce it (co-20).

**Paradigm as a design decision**

- [ ] I can name the specific constraint a paradigm gives up and the specific property it buys in
      exchange (co-21).
- [ ] I can identify where mutable shared state lives in a design and explain why that's the fault
      line separating most paradigm distinctions (co-22).
- [ ] I can recognize a problem's shape and match it to the paradigm built for that shape, rather than
      forcing every problem into one default lens (co-23).
- [ ] I can name a paradigm's concrete cost (readability, testability, change-cost), not just its
      benefit (co-24).
- [ ] I can keep one paradigm per boundary and explain the specific difference between legitimate
      multi-paradigm code and paradigm soup (co-25).

## Elaborative interrogation & self-explanation

Eight why/why-not prompts. Answer in your own words before checking -- the goal is explaining the
reasoning, not reciting a definition.

**W1.** Why is co-22 (state as the fault line) described as running under every OTHER concept in this
topic, rather than being just one paradigm distinction among many?

<details>
<summary>Answer</summary>

OO's encapsulated instance state, functional programming's insistence on no shared mutable state, and
reactive programming's automatic propagation are all, at bottom, different answers to "where does
mutable state live, and who's allowed to touch it." Once you can name a design's answer to that one
question, you can predict most of its other paradigm-level properties without inspecting anything else.

</details>

**W2.** Why does this topic insist a paradigm be chosen by matching the problem's shape (co-23), rather
than by which paradigm the team happens to be most comfortable with?

<details>
<summary>Answer</summary>

Comfort is about the DEVELOPER; shape-matching is about the PROBLEM. Forcing a search-and-satisfy
problem into hand-written imperative loops doesn't just cost more code -- it actively hides structure
the problem already has (a constraint solver would find the feasible space directly). The durable skill
is recognizing that shape, independent of which paradigm feels most familiar.

</details>

**W3.** Why does Kata 6's missing `chosen.pop()` corrupt the RESULT and not just waste some extra
recursive calls?

<details>
<summary>Answer</summary>

`chosen` is one shared, mutable list referenced by the entire recursive call tree, not a fresh copy per
branch. When an inclusion branch fails and the code falls through to the exclusion branch, the
already-appended number is still physically present in `chosen` -- so the final returned list reflects
a combination of "excluded" and "included" choices that never should have coexisted, not merely a
slower search.

</details>

**W4.** Why does Kata 9's `threading.Event` handshake make a race condition reproduce identically on
every run, when races are usually described as "non-deterministic"?

<details>
<summary>Answer</summary>

A real race's timing is non-deterministic because the OS scheduler decides when each thread runs. The
`Event` handshake replaces "hope the scheduler interleaves badly" with an explicit protocol: each
thread signals "I have read" and then WAITS for the other thread's signal before writing. That forces
the exact interleaving that causes the bug, every single time, which is what makes it teachable and
testable rather than a flaky coin flip.

</details>

**W5.** Why is co-08's "declarative vs imperative" framed as a trade (something gained, something
trusted blindly), rather than declarative simply being the "better" style?

<details>
<summary>Answer</summary>

Declarative code hands the "how" to an engine, so the reader only verifies the "what" -- a real
readability and correctness win. But that same "how" becomes opaque: a slow SQL query or an
unexpectedly expensive comprehension is harder to diagnose precisely because the mechanics are hidden
from the code that expresses the intent. Neither style dominates; each is a different bet on what the
reader needs to see.

</details>

**W6.** Why does co-25 (mixing paradigms at boundaries) explicitly distinguish "legitimate
multi-paradigm code" from "paradigm soup," instead of treating any paradigm-mixing as automatically
suspect?

<details>
<summary>Answer</summary>

A multi-paradigm language like Python is often at its best mixing paradigms deliberately -- a
functional pipeline handing immutable data to an OO service is fine. What makes it soup is a guarantee
being silently violated: a "functional-looking" chain that secretly threads a mutable object through
every step collects the COSTS of both paradigms (indirection, hidden effects) while delivering the
BENEFITS of neither.

</details>

**W7.** Why does Kata 4's fix (a `@property`) count as "reactive" when it contains no subscriber list,
no `on_change()` callback, and no push notification at all?

<details>
<summary>Answer</summary>

Reactive programming's actual goal is eliminating "I changed A but forgot to update the thing that
depends on A." A push/subscribe mechanism is ONE way to guarantee that; a computed property that
recomputes from source data on every read is a simpler way to guarantee the exact same thing for a
value with no independent state of its own. The mechanism differs; the guarantee -- no possible
staleness -- is identical.

</details>

**W8.** Why does co-21 (paradigm as constraint buys property) matter more as a way of THINKING about
paradigms than as a fact about any one paradigm?

<details>
<summary>Answer</summary>

Once "purity buys reasoning," "immutability buys safe sharing," and "encapsulation buys change
isolation" are all instances of the SAME pattern (give up a capability, receive a guarantee), a new,
unfamiliar paradigm can be evaluated the same way: what does it force you to give up, and what does it
promise in return? That question turns "which paradigm should I use" from a taste question into an
engineering one, for paradigms this topic never even names.

</details>

---

← Previous: [Capstone](../learning/capstone/overview.md)
