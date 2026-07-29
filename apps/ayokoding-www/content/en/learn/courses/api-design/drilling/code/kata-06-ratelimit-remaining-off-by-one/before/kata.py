# pyright: strict
"""Kata 6 (before): the RateLimit header reports remaining BEFORE this call's own cost is deducted."""

BUDGET = [3]


def call_and_report() -> str:
    # THE BUG: the header is built from BUDGET[0] BEFORE decrementing -- the
    # caller is told it has one MORE request left than it actually does, right
    # up until the call that reports remaining=0 and then gets rejected anyway.
    header = f"limit=3, remaining={BUDGET[0]}"
    BUDGET[0] -= 1
    return header


print(f"call 1: {call_and_report()}")  # BUG: claims remaining=3, but THIS call already used 1
print(f"call 2: {call_and_report()}")  # BUG: claims remaining=2, actually 1 left
print(f"call 3: {call_and_report()}")  # BUG: claims remaining=1, actually 0 left -- next call is rejected
