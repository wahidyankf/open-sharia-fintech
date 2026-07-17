"""Example 23: Match-Case Dispatch."""


def handle_command(tag: str) -> str:  # => dispatches on a plain string tag (Python 3.10+, PEP 634)
    match tag:  # => structural pattern matching -- declares the shape of every case up front
        case "start":  # => case #1: an exact literal match
            return "engine started"  # => matched branch returns immediately, no further case checked
        case "stop":  # => case #2: another exact literal match
            return "engine stopped"  # => same shape as the branch above, different literal and result
        case "status" | "ping":  # => case #3: an OR-pattern -- either literal fires this branch
            return "engine idle"  # => one return value covers both "status" and "ping" tags
        case _:  # => the wildcard: catches anything not matched above
            return f"unknown command: {tag}"  # => never reached for the three known tags above


for tag in ("start", "stop", "ping", "explode"):  # => exercise every branch, including the wildcard
    print(handle_command(tag))  # => confirms each case fires for its own tag
# => Output: engine started
# => Output: engine stopped
# => Output: engine idle
# => Output: unknown command: explode
