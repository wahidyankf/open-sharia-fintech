---
title: "Capstone: The Prompt"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 10
---

_Capstone step 1 of 3 -- exercises co-05 (prompting for code) and co-13/co-14 (verification
discipline, test-driven agent workflows)._

## The feature

A `parse_duration(s: str) -> int` function that converts a compact human duration string (e.g.
`"1h30m"`) into a total whole-second count -- the kind of small, well-scoped utility a real project
actually needs (log-retention windows, rate-limit windows, cache TTLs) and that is genuinely
delegable to an agent because it is cheap to specify and cheap to verify.

## The prompt, as actually given to the agent

> **Goal**: implement `parse_duration(s: str) -> int` in `parse_duration.py`, converting a duration
> string composed of `<digits>h`, `<digits>m`, `<digits>s` tokens (in that order, each optional, each
> appearing at most once) into a total whole-second count.
>
> **Constraints**:
>
> - Python 3.13, standard library only, fully type-annotated.
> - Raise `ValueError` for an empty string, a string with no valid tokens, or any unmatched trailing
>   content (e.g. a stray character, a duplicated unit, or out-of-order units).
> - No external dependencies; the function must be a pure function (no I/O, no global mutable state).
>
> **Example**: `parse_duration("1h30m") == 5400` (1 hour + 30 minutes = 3600 + 1800 = 5400 seconds).
>
> **Acceptance criteria** (every bullet below is a test in the attached `test_parse_duration.py`,
> the tripwire for this session -- do not claim the feature is done until every one of these passes):
>
> - `parse_duration("1h30m") == 5400`
> - `parse_duration("45s") == 45`
> - `parse_duration("1h1m1s") == 3661`
> - `parse_duration("0h") == 0`
> - `parse_duration("")` raises `ValueError`
> - `parse_duration("1h30mx")` raises `ValueError` (trailing garbage)
> - `parse_duration("hello")` raises `ValueError` (no valid tokens)

## The failing test (the tripwire), attached to the prompt

`test_parse_duration.py` (colocated at `learning/capstone/code/test_parse_duration.py`, the final
resting copy -- shown here as it existed at this step, before `parse_duration.py` existed at all):

```python
from parse_duration import parse_duration
import pytest


def test_hours_and_minutes():
    assert parse_duration("1h30m") == 5400


def test_seconds_only():
    assert parse_duration("45s") == 45


def test_all_three_units():
    assert parse_duration("1h1m1s") == 3661


def test_zero_valued_token():
    assert parse_duration("0h") == 0


def test_empty_string_rejected():
    with pytest.raises(ValueError):
        parse_duration("")


def test_garbage_suffix_rejected():
    with pytest.raises(ValueError):
        parse_duration("1h30mx")


def test_no_tokens_rejected():
    with pytest.raises(ValueError):
        parse_duration("hello")
```

**Run**: `python3 -m pytest test_parse_duration.py -q` (before any implementation file exists)

**Output** (genuine, captured transcript):

```text
ERRORS ====================================
___________________ ERROR collecting test_parse_duration.py ____________________
ImportError while importing test module '.../test_parse_duration.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
test_parse_duration.py:1: in <module>
    from parse_duration import parse_duration
E   ModuleNotFoundError: No module named 'parse_duration'
=========================== short test summary info ============================
ERROR test_parse_duration.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.05s
```

**Verify**: the test suite fails (a genuine `ModuleNotFoundError`, not a fabricated one -- there is
no implementation yet), and the prompt above states a concrete, checkable acceptance bar (seven
bullets, each one a literal assertion in the attached test file) before any code was generated.

---

Next: [Session](./session/overview.md) →
