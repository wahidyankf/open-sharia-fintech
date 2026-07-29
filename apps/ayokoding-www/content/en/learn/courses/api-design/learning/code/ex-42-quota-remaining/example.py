# pyright: strict
"""Example 42: The Remaining Counter Decrements to Zero. (co-20)

Following Example 41's structured header, this example shows the FULL
lifecycle: `remaining` decrements per call until it reaches zero, at which
point the NEXT call is the one Example 40's `429` would reject.
"""

QUOTA = {"limit": 3, "remaining": 3}  # => co-20: a small quota, easy to exhaust in one script run
# => QUOTA is {'limit': 3, 'remaining': 3} (type: dict[str, int]) before any call runs


def call_api() -> dict[str, int]:  # => one call against the shared quota above
    QUOTA["remaining"] -= 1  # => co-20: every call decrements the remaining counter by exactly one
    return dict(QUOTA)  # => a snapshot of the quota state AFTER this call


for call_number in range(1, 4):  # => co-20: three calls, exactly draining the quota to zero
    state = call_api()  # => makes one call, observing the quota afterward
    print(f"call {call_number}: remaining={state['remaining']}")  # => Output: 2, 1, 0

print(f"quota exhausted: {QUOTA['remaining'] == 0}")  # => Output: True -- co-20: the NEXT call trips 429
