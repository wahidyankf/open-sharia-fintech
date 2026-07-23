---
title: "Overview"
date: 2026-07-17T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Take one non-trivial small problem -- a **sequential transaction processor** -- and implement it in
four paradigms (imperative, OO, functional, reactive) producing byte-identical output on the same
input, verified by one shared test. Then write a decision record arguing which paradigm best fits the
problem, grounded in the actual code, not general paradigm preference. This capstone is a
consolidation, not a new mechanism: every paradigm shape it combines was already taught, individually,
across the Beginner, Intermediate, and Advanced tiers of this topic (most directly, Examples 29-32's
and 59's earlier "same problem, four ways" pattern).

**The problem**: given a starting balance and an ordered list of transaction amounts (positive =
deposit, negative = withdrawal), apply each transaction in order. A transaction that would drive the
balance negative is **rejected** (skipped; balance unchanged for that step) rather than applied. Return
the final balance and the list of rejected transaction indices.

## Concepts exercised

- [x] imperative/procedural solution (co-01, co-02)
- [x] OO solution (co-05, co-06)
- [x] functional solution (co-09, co-11)
- [x] declarative or reactive solution (co-08, co-17)
- [x] a reasoned paradigm-selection decision grounded in trade-offs (co-23, co-24, co-25)

All colocated code lives under `learning/capstone/code/`: four paradigm implementations in
`paradigms/`, the full `pytest` suite (including the shared cross-paradigm test) in `tests/`, and the
decision record at `paradigms/../decision.md`. Every listing below is the complete file, verbatim --
nothing on this page is truncated or paraphrased.

## Step 1: define the problem and a shared test

_exercises co-23_

Before writing any implementation, `tests/test_shared.py` fixes the problem's shape: one shared input
(`AMOUNTS = [50, -200, 30, -1000, 20]`, `STARTING_BALANCE = 100`) and one expected result
(`EXPECTED_BALANCE = 200`, `EXPECTED_REJECTED = [1, 3]`) that every one of the four implementations
below is checked against. `test_a_stub_implementation_would_fail_this_shared_test()` proves the test is
meaningful -- a deliberately wrong stub that accepts every transaction is shown to disagree with the
expected result, confirming the shared test actually discriminates a correct implementation from an
incorrect one, not just a smoke test that always passes.

**`learning/capstone/code/tests/test_shared.py`** (complete file)

```python
"""Shared test: all four paradigm implementations must agree on the identical result.

This is the capstone's step-1 requirement -- one test asserting the expected output, checked
against every implementation. AMOUNTS/STARTING_BALANCE/EXPECTED are the single source of truth
every paradigm-specific test file (test_imperative.py, test_oo.py, test_functional.py,
test_reactive.py) also checks its own implementation against.
"""

from paradigms.functional import process_transactions_functional
from paradigms.imperative import process_transactions_imperative
from paradigms.oo import TransactionProcessor
from paradigms.reactive import process_transactions_reactive

AMOUNTS = [50, -200, 30, -1000, 20]  # => the ONE shared problem input, used by all four paradigms
STARTING_BALANCE = 100
EXPECTED_BALANCE = 200
EXPECTED_REJECTED = [1, 3]  # => -200 (index 1) and -1000 (index 3) both would have gone negative


def test_all_four_paradigms_agree_on_the_expected_result() -> None:
    imperative_result = process_transactions_imperative(list(AMOUNTS), starting_balance=STARTING_BALANCE)
    oo_result = TransactionProcessor(starting_balance=STARTING_BALANCE).process_all(list(AMOUNTS))
    functional_balance, functional_rejected = process_transactions_functional(tuple(AMOUNTS), starting_balance=STARTING_BALANCE)
    reactive_result = process_transactions_reactive(list(AMOUNTS), starting_balance=STARTING_BALANCE)

    expected = (EXPECTED_BALANCE, EXPECTED_REJECTED)  # => the ONE expected shape every paradigm must match
    assert imperative_result == expected
    assert oo_result == expected
    assert (functional_balance, list(functional_rejected)) == expected
    assert reactive_result == expected


def test_a_stub_implementation_would_fail_this_shared_test() -> None:
    # => proves the shared test is meaningful (not vacuously true): a deliberately wrong stub,
    # => shaped like the real functions but always accepting every transaction, fails the check
    def stub_always_accepts(amounts: list[int], starting_balance: int) -> tuple[int, list[int]]:
        return starting_balance + sum(amounts), []  # => never rejects anything -- the wrong behavior

    stub_result = stub_always_accepts(list(AMOUNTS), starting_balance=STARTING_BALANCE)
    assert stub_result != (EXPECTED_BALANCE, EXPECTED_REJECTED)  # => the stub is provably NOT a valid solution


def test_all_four_paradigms_agree_on_a_second_independent_sample() -> None:
    amounts = [10, -5, -50, 100, -200]  # => a different transaction sequence
    starting_balance = 20
    # => trace: 20+10=30(ok), 30-5=25(ok), 25-50=-25 rejected(stays 25), 25+100=125(ok), 125-200=-75 rejected(stays 125)
    expected = (125, [2, 4])

    imperative_result = process_transactions_imperative(list(amounts), starting_balance=starting_balance)
    oo_result = TransactionProcessor(starting_balance=starting_balance).process_all(list(amounts))
    functional_balance, functional_rejected = process_transactions_functional(tuple(amounts), starting_balance=starting_balance)
    reactive_result = process_transactions_reactive(list(amounts), starting_balance=starting_balance)

    assert imperative_result == expected
    assert oo_result == expected
    assert (functional_balance, list(functional_rejected)) == expected
    assert reactive_result == expected
```

## Step 2: the imperative and OO implementations

_exercises co-01, co-02, co-05, co-06_

`paradigms/imperative.py` is the direct shape: a mutable `balance` and a mutable `rejected` list,
updated in place by an explicit `for` loop. `paradigms/oo.py`'s `TransactionProcessor` bundles the
identical logic as encapsulated instance state -- `_balance` and `_rejected` are private, and
`apply()`/`process_all()` are the only sanctioned ways to touch them.

**`learning/capstone/code/paradigms/imperative.py`** (complete file)

```python
"""Capstone -- Imperative: Sequential Transaction Processor (co-01, co-02)."""


def process_transactions_imperative(amounts: list[int], starting_balance: int) -> tuple[int, list[int]]:
    # => explicit loop, mutable balance, mutable rejected list -- the direct imperative shape
    balance = starting_balance  # => mutable running balance, updated in place as we go
    rejected: list[int] = []  # => mutable accumulator of rejected transaction indices
    for index, amount in enumerate(amounts):  # => step through transactions one at a time, in order
        if balance + amount < 0:  # => would this transaction drive the balance negative?
            rejected.append(index)  # => reject: record the index, balance stays UNCHANGED this step
        else:
            balance += amount  # => accept: mutate the running balance in place
    return balance, rejected  # => the final mutated state, handed back as a plain tuple


if __name__ == "__main__":
    amounts = [50, -200, 30, -1000, 20]  # => shared capstone input across all four paradigms
    final_balance, rejected = process_transactions_imperative(amounts, starting_balance=100)
    print(final_balance, rejected)  # => 100+50=150(ok), -200 rejected, +30=180(ok), -1000 rejected, +20=200(ok)
    # => Output: 200 [1, 3]
```

**Run**

```shell
python3 -m paradigms.imperative
```

**Output**

```text
200 [1, 3]
```

**`learning/capstone/code/paradigms/oo.py`** (complete file)

```python
"""Capstone -- OO: Sequential Transaction Processor (co-05, co-06)."""


class TransactionProcessor:  # => bundles balance + rejection tracking as encapsulated instance state
    def __init__(self, starting_balance: int) -> None:
        self._balance = starting_balance  # => private state, only this class's own methods touch it
        self._rejected: list[int] = []  # => private state: which transaction indices were rejected

    def apply(self, index: int, amount: int) -> None:  # => the ONE sanctioned way to process a transaction
        if self._balance + amount < 0:  # => the same rejection rule as the imperative version
            self._rejected.append(index)  # => reject: record it, balance untouched
        else:
            self._balance += amount  # => accept: mutate this instance's own balance

    def process_all(self, amounts: list[int]) -> tuple[int, list[int]]:  # => drive apply() over every transaction
        for index, amount in enumerate(amounts):  # => same ordering guarantee as the imperative version
            self.apply(index, amount)
        return self._balance, list(self._rejected)  # => a defensive copy of the rejected list


if __name__ == "__main__":
    amounts = [50, -200, 30, -1000, 20]  # => identical shared input to the imperative version
    processor = TransactionProcessor(starting_balance=100)
    final_balance, rejected = processor.process_all(amounts)
    print(final_balance, rejected)  # => must match the imperative version exactly
    # => Output: 200 [1, 3]
```

**Run**

```shell
python3 -m paradigms.oo
```

**Output**

```text
200 [1, 3]
```

**`learning/capstone/code/tests/test_imperative.py`** (complete file)

```python
"""Tests for the imperative Sequential Transaction Processor."""

from paradigms.imperative import process_transactions_imperative


def test_matches_the_shared_expected_result() -> None:
    balance, rejected = process_transactions_imperative([50, -200, 30, -1000, 20], starting_balance=100)
    assert (balance, rejected) == (200, [1, 3])  # => the one expected result every paradigm must match


def test_a_transaction_that_exactly_zeroes_the_balance_is_accepted() -> None:
    balance, rejected = process_transactions_imperative([-100], starting_balance=100)
    assert (balance, rejected) == (0, [])  # => landing exactly at zero is NOT rejected, only negative is


def test_an_empty_transaction_list_returns_the_starting_balance_unchanged() -> None:
    assert process_transactions_imperative([], starting_balance=42) == (42, [])
```

**`learning/capstone/code/tests/test_oo.py`** (complete file)

```python
"""Tests for the OO Sequential Transaction Processor."""

from paradigms.oo import TransactionProcessor


def test_matches_the_shared_expected_result() -> None:
    processor = TransactionProcessor(starting_balance=100)
    balance, rejected = processor.process_all([50, -200, 30, -1000, 20])
    assert (balance, rejected) == (200, [1, 3])


def test_two_processors_have_independent_state() -> None:
    a = TransactionProcessor(starting_balance=10)
    b = TransactionProcessor(starting_balance=10)
    a.apply(0, -5)  # => mutate only a's state
    assert a.process_all([]) == (5, [])  # => a reflects its own mutation
    assert b.process_all([]) == (10, [])  # => b is untouched by a's mutation


def test_process_all_returns_a_defensive_copy_of_rejected() -> None:
    processor = TransactionProcessor(starting_balance=0)
    _, rejected = processor.process_all([-1])  # => rejected immediately
    rejected.append(999)  # => mutate the RETURNED list
    _, rejected_again = processor.process_all([])  # => query the processor's own state again
    assert rejected_again == [0]  # => the processor's internal list was never touched by the caller's mutation
```

**Verify**

```shell
python3 -m pytest tests/test_imperative.py tests/test_oo.py -q
```

**Output**

```text
6 passed
```

## Step 3: the functional and reactive implementations

_exercises co-08, co-09, co-11, co-17_

`paradigms/functional.py` folds a plain `(balance, rejected)` tuple through `functools.reduce()` --
each step returns a brand-new accumulator, never mutating the previous one. `paradigms/reactive.py`'s
`ReactiveAccount` pushes a rejection notification to every subscriber automatically, the instant a
transaction is rejected -- `rejected` is filled entirely through that push, never by a direct append
inside the driving loop. The subscription itself is declarative: `account.on_reject(...)` says only
_what_ should happen on a rejection, never _how_ or _when_ to check for one -- the caller writes no
polling loop, which is exactly what `test_rejection_subscriber_is_pushed_automatically_not_polled`'s
name calls out by contrast.

**`learning/capstone/code/paradigms/functional.py`** (complete file)

```python
"""Capstone -- Functional: Sequential Transaction Processor (co-09, co-11)."""

from functools import reduce


def process_transactions_functional(amounts: tuple[int, ...], starting_balance: int) -> tuple[int, tuple[int, ...]]:
    # => a PURE fold: the accumulator is a plain (balance, rejected) tuple, REPLACED every step, never mutated
    def step(acc: tuple[int, tuple[int, ...]], indexed: tuple[int, int]) -> tuple[int, tuple[int, ...]]:
        balance, rejected = acc  # => unpack the immutable accumulator carried in from the previous step
        index, amount = indexed
        if balance + amount < 0:  # => the SAME rejection rule as the other three paradigms
            return balance, rejected + (index,)  # => a BRAND NEW tuple -- the old `rejected` is untouched
        return balance + amount, rejected  # => a BRAND NEW accumulator -- nothing mutated in place

    return reduce(step, enumerate(amounts), (starting_balance, ()))  # => fold over (index, amount) pairs


if __name__ == "__main__":
    amounts: tuple[int, ...] = (50, -200, 30, -1000, 20)  # => identical shared input, as an immutable tuple
    final_balance, rejected = process_transactions_functional(amounts, starting_balance=100)
    print(final_balance, list(rejected))  # => must match the other two paradigms exactly
    # => Output: 200 [1, 3]
```

**Run**

```shell
python3 -m paradigms.functional
```

**Output**

```text
200 [1, 3]
```

**`learning/capstone/code/paradigms/reactive.py`** (complete file)

```python
"""Capstone -- Reactive: Sequential Transaction Processor (co-08, co-17)."""

from collections.abc import Callable


class ReactiveAccount:  # => a reactive source: rejections PUSH to subscribers automatically, no polling
    def __init__(self, starting_balance: int) -> None:
        self._balance = starting_balance  # => the account's current balance
        self._on_reject: list[Callable[[int], None]] = []  # => subscribers notified on every rejection

    def on_reject(self, fn: Callable[[int], None]) -> None:  # => register a rejection subscriber
        self._on_reject.append(fn)  # => append -- does NOT replay past rejections to a late subscriber

    def apply(self, index: int, amount: int) -> None:  # => process one transaction, reactively
        if self._balance + amount < 0:  # => the SAME rejection rule as the other three paradigms
            for fn in self._on_reject:  # => PUSH: every subscriber is notified automatically, right here
                fn(index)
        else:
            self._balance += amount  # => accept: update the balance

    def balance(self) -> int:  # => the only sanctioned way to read the current balance
        return self._balance


def process_transactions_reactive(amounts: list[int], starting_balance: int) -> tuple[int, list[int]]:
    account = ReactiveAccount(starting_balance)  # => construct the reactive source
    rejected: list[int] = []  # => a subscriber's own recorder -- filled ENTIRELY via the push callback below
    account.on_reject(lambda index: rejected.append(index))  # => subscribe BEFORE processing any transaction
    for index, amount in enumerate(amounts):  # => drive the reactive account through every transaction in order
        account.apply(index, amount)
    return account.balance(), rejected  # => `rejected` was never appended to directly -- only via the push


if __name__ == "__main__":
    amounts = [50, -200, 30, -1000, 20]  # => identical shared input to the other three paradigms
    final_balance, rejected = process_transactions_reactive(amounts, starting_balance=100)
    print(final_balance, rejected)  # => must match the other three paradigms exactly
    # => Output: 200 [1, 3]
```

**Run**

```shell
python3 -m paradigms.reactive
```

**Output**

```text
200 [1, 3]
```

**`learning/capstone/code/tests/test_functional.py`** (complete file)

```python
"""Tests for the functional Sequential Transaction Processor."""

from paradigms.functional import process_transactions_functional


def test_matches_the_shared_expected_result() -> None:
    balance, rejected = process_transactions_functional((50, -200, 30, -1000, 20), starting_balance=100)
    assert (balance, list(rejected)) == (200, [1, 3])


def test_pure_fold_never_mutates_its_input_tuple() -> None:
    amounts = (10, -5, 3)  # => fresh immutable input
    process_transactions_functional(amounts, starting_balance=0)  # => call once, discard the result
    assert amounts == (10, -5, 3)  # => provably unchanged -- tuples can't be mutated in place anyway,
    # => but this documents the deliberate no-mutation contract the fold was written to satisfy


def test_calling_twice_with_the_same_arguments_returns_the_same_result() -> None:
    first = process_transactions_functional((5, -10), starting_balance=0)  # => call #1
    second = process_transactions_functional((5, -10), starting_balance=0)  # => call #2, identical arguments
    assert first == second  # => referential transparency: no hidden state anywhere
```

**`learning/capstone/code/tests/test_reactive.py`** (complete file)

```python
"""Tests for the reactive Sequential Transaction Processor."""

from paradigms.reactive import ReactiveAccount, process_transactions_reactive


def test_matches_the_shared_expected_result() -> None:
    balance, rejected = process_transactions_reactive([50, -200, 30, -1000, 20], starting_balance=100)
    assert (balance, rejected) == (200, [1, 3])


def test_rejection_subscriber_is_pushed_automatically_not_polled() -> None:
    account = ReactiveAccount(starting_balance=0)
    seen: list[int] = []  # => local recorder, filled only via the push callback
    account.on_reject(lambda index: seen.append(index))
    account.apply(0, -5)  # => would go negative -- must push a rejection notification immediately
    assert seen == [0]  # => the subscriber saw it without ever polling the account


def test_multiple_subscribers_are_all_notified_of_the_same_rejection() -> None:
    account = ReactiveAccount(starting_balance=0)
    seen_a: list[int] = []
    seen_b: list[int] = []
    account.on_reject(lambda index: seen_a.append(index))
    account.on_reject(lambda index: seen_b.append(index))
    account.apply(3, -1)  # => one rejection event
    assert seen_a == [3]
    assert seen_b == [3]  # => both subscribers received the same push, independently
```

**Verify**

```shell
python3 -m pytest tests/test_functional.py tests/test_reactive.py tests/test_shared.py -q
```

**Output**

```text
9 passed
```

## Step 4: the decision record

_exercises co-23, co-24, co-25_

`decision.md` argues the paradigm best-fit for this problem, citing the concrete readability,
testability, and change-cost trade-offs measured against the four implementations above -- reproduced
here in full.

**`learning/capstone/code/decision.md`** (complete file)

```markdown
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
```

## Done bar

Runnable end to end: `python3 -m paradigms.imperative`, `python3 -m paradigms.oo`,
`python3 -m paradigms.functional`, and `python3 -m paradigms.reactive` each independently print
`200 [1, 3]`; `python3 -m pytest` from `learning/capstone/code/` runs all four paradigm-specific test
files plus `tests/test_shared.py`, 15 passed, 0 failed.
