# Decision Record: Sequential Transaction Processor

## The problem

Given a starting balance and an ordered list of transaction amounts (positive = deposit,
negative = withdrawal), apply each transaction in order. A transaction that would drive the
balance negative is **rejected** (skipped; balance unchanged for that step) rather than applied.
Return the final balance and the list of rejected transaction indices.

Four implementations of this identical problem live in `paradigms/`:

- `paradigms/imperative.py` — `process_transactions_imperative()`
- `paradigms/oo.py` — `TransactionProcessor`
- `paradigms/functional.py` — `process_transactions_functional()`
- `paradigms/reactive.py` — `ReactiveAccount` / `process_transactions_reactive()`

All four pass the identical shared test in `tests/test_shared.py` against the shared input
`AMOUNTS = [50, -200, 30, -1000, 20]`, `STARTING_BALANCE = 100`, expecting
`(final_balance=200, rejected=[1, 3])`.

## Trade-offs, measured against the actual code above

**Readability**

- `process_transactions_imperative()` is the most immediately readable to anyone who has ever
  written a `for` loop — one mutable `balance`, one mutable `rejected` list, one `if`/`else`. No
  new vocabulary required.
- `TransactionProcessor` spreads the same logic across `__init__`, `apply()`, and `process_all()`
  — three places instead of one function, but each piece is individually smaller and named.
- `process_transactions_functional()` requires understanding `reduce()` and tuple-rebuilding
  (`rejected + (index,)`) before its logic is legible — the steepest reading cost of the four.
- `process_transactions_reactive()` requires understanding the push/subscribe pattern before
  `rejected` being filled via `account.on_reject(lambda index: rejected.append(index))` makes
  sense — not obvious on first read, though familiar to anyone who has used Example 17's
  `ObservableValue` or Example 55's `EventBus` earlier in this topic.

**Testability**

- All four are equally testable in isolation — `tests/test_imperative.py`,
  `tests/test_oo.py`, `tests/test_functional.py`, and `tests/test_reactive.py` each hit their own
  implementation with zero I/O and zero mocking, because none of the four implementations does
  any I/O in the first place. Testability here is not a differentiator between paradigms; it is a
  property of the problem (pure computation over in-memory data) that every paradigm preserves.
- `test_oo.py`'s `test_two_processors_have_independent_state` and
  `test_process_all_returns_a_defensive_copy_of_rejected` exist ONLY because `TransactionProcessor`
  has instance state to worry about — the other three paradigms need no equivalent test, because
  they have no comparable state-isolation risk to verify.

**Change-cost**

- Adding a second rejection reason (say, "reject any single transaction over 10000") is a
  one-line `if` change in `imperative.py` and `oo.py`'s `apply()`, a one-line change to the
  `step()` closure's condition in `functional.py`, and a one-line change to `apply()`'s condition
  in `reactive.py` — genuinely equal cost across all four for THIS specific problem, because the
  rejection rule is a single boolean check, not a growing rule table (contrast Example 54's
  `RULES` list, where declarative genuinely wins on change-cost).
- Adding a SECOND kind of subscriber (say, "notify when balance crosses a low-balance threshold,
  independent of rejection") is near-zero cost in `reactive.py` — add another `_on_threshold`
  list and another `on_threshold()` registration method, following the exact shape already
  established by `_on_reject`/`on_reject()`. The other three paradigms would each need a new
  parameter threaded through their whole call chain (imperative: a new local variable and
  `if`; OO: a new instance list and check inside `apply()`; functional: a wider accumulator
  tuple and a second condition in `step()`) — none of which is free, but none is as
  structurally cheap as reactive's "just add another subscriber list."

**Paradigm boundaries**

- Each of the four files stays paradigm-pure internally: `imperative.py`'s loop never touches an
  object's private state, `oo.py`'s private `_balance`/`_rejected` never leak into a fold,
  `functional.py`'s fold never registers a callback, and `reactive.py`'s `_on_reject` subscriber list
  never appears as a loop-local mutable accumulator the way `imperative.py`'s `rejected` does.
- The one place all four genuinely meet is `tests/test_shared.py`, and it crosses that boundary only
  through each implementation's plain, immutable-value return interface — `(balance, rejected)` tuples
  in, `(balance, rejected)` tuples out — never by reaching into `TransactionProcessor`'s private state
  or `ReactiveAccount`'s `_on_reject` list directly. That is co-25 in miniature: pick one paradigm per
  boundary (here, per file), and let paradigms meet only through a value-shaped seam, not by freely
  mixing mutable OO state into a nominally functional fold the way Example 50's
  `paradigm-soup-antipattern` deliberately does wrong.

## The choice

**Imperative** is the right default for this specific problem as it stands today: a single,
sequential, stateful computation with one rejection rule and no need for external observers.
`process_transactions_imperative()` is the shortest, most immediately legible implementation of
the four, and per co-24's cost/benefit framing, none of the other three paradigms' extra
machinery (encapsulation boundaries, pure-fold vocabulary, or a push/subscribe wiring layer) buys
anything this problem, as stated, actually needs.

**Reactive is the paradigm to reach for the moment this problem grows an observer requirement** —
e.g., a UI panel that must show rejected transactions live, or a second subsystem (fraud
detection) that needs to react to every rejection independently of the caller that triggered it.
`ReactiveAccount`'s `on_reject()` is already built for exactly that extension, at essentially zero
added complexity to the paradigms that don't need it. This is co-23's matching-paradigm-to-problem
skill in miniature: the "right" paradigm is a property of the problem's actual shape, including
which direction it is likely to grow, not a permanent ranking of paradigms against each other.
