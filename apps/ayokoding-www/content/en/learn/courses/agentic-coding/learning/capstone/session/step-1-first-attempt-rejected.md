---
title: "Capstone Session Step 1: First Attempt, Rejected"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 20
---

The agent's first generation, in full (`parse_duration.py` at this point):

```python
"""Capstone attempt 1: parse_duration -- convert an "1h30m"-style duration string to total seconds."""  # => co-05: restates the prompt's own framing
from __future__ import annotations  # => DD-39 hygiene

import re  # => co-05: stdlib-only per the prompt's constraint

_TOKEN = re.compile(r"(\d+)([hms])")  # => matches one <digits><unit> token, e.g. "30m"
_UNIT_SECONDS: dict[str, int] = {"h": 3600, "m": 600, "s": 1}  # => co-16: LOOKS right, IS wrong -- "m" should map to 60, not 600


def parse_duration(s: str) -> int:  # => co-05: matches the prompt's exact signature
    """Parse a duration string like "1h30m" or "45s" into total whole seconds."""
    if not s:  # => co-05: satisfies the empty-string acceptance bullet
        raise ValueError("duration string must not be empty")
    total = 0
    consumed = 0
    for match in _TOKEN.finditer(s):  # => co-07: walks every token the regex can find
        value = int(match.group(1))
        unit = match.group(2)
        total += value * _UNIT_SECONDS[unit]  # => co-16: silently wrong for every "m" token
        consumed += len(match.group(0))
    if consumed != len(s):  # => co-05: satisfies the garbage-suffix / no-valid-tokens bullets
        raise ValueError(f"invalid duration string: {s!r}")
    return total
```

**Run**: `python3 -m pytest test_parse_duration.py -q`

**Output** (genuine, captured transcript):

```text
F.F....                                                                  [100%]
=================================== FAILURES ===================================
____________________________ test_hours_and_minutes ____________________________

    def test_hours_and_minutes():
>       assert parse_duration("1h30m") == 5400
E       AssertionError: assert 21600 == 5400
E        +  where 21600 = parse_duration('1h30m')

test_parse_duration.py:6: AssertionError
_____________________________ test_all_three_units _____________________________

    def test_all_three_units():
>       assert parse_duration("1h1m1s") == 3661
E       AssertionError: assert 4201 == 3661
E        +  where 4201 = parse_duration('1h1m1s')

test_parse_duration.py:14: AssertionError
=========================== short test summary info ============================
FAILED test_parse_duration.py::test_hours_and_minutes - AssertionError: asser...
FAILED test_parse_duration.py::test_all_three_units - AssertionError: assert ...
2 failed, 5 passed in 0.01s
```

**Rejection reason (written before any further step)**: `_UNIT_SECONDS["m"]` is `600`, not `60` --
a plausible-looking typo (visually one digit away from `60`, and the code otherwise reads as
correct, type-annotated, and idiomatic) that the tripwire test caught immediately (co-16:
hallucination awareness -- the failure was caught by running the test, not by reading the code and
trusting it). Five of seven tests still passed, which is itself a trap: a partial pass is not a
green build, and this diff is rejected in full, not "mostly accepted."

**Verify**: the test run above is a genuine, captured failure -- two of the seven acceptance-bullet
tests fail with a concrete `AssertionError` showing the wrong numeric answer (`21600` instead of
`5400`), and the rejection reason above names the exact line and exact wrong value, not a vague
"doesn't work."

---

← Previous: [Session Overview](./overview.md) &middot; Next: [Step 2: Fix, Green](./step-2-fix-and-green.md) →
