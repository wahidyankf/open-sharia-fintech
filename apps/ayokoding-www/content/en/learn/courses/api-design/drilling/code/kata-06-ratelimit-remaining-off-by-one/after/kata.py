# pyright: strict
"""Kata 6 (after): the header is built AFTER decrementing, reporting the TRUE remaining budget."""

BUDGET = [3]


def call_and_report() -> str:
    # THE FIX: decrement FIRST, then report -- the header always reflects
    # budget genuinely remaining AFTER this call has already been counted.
    BUDGET[0] -= 1
    return f"limit=3, remaining={BUDGET[0]}"


print(f"call 1: {call_and_report()}")
print(f"call 2: {call_and_report()}")
print(f"call 3: {call_and_report()}")
