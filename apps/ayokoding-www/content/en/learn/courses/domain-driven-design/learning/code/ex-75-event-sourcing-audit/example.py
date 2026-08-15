# => Keeps this domain step explicit and reviewable.
"""Example 75: event history can answer who changed what and when."""

# => Keeps scenario data close to the rule it exercises.
events = [
    # => Keeps this domain step explicit and reviewable.
    {"who": "ada", "what": "placed", "when": "2026-08-14T00:00:00Z"}
]  # => audit facts retain actor and time
audit = f"{events[0]['who']} {events[0]['what']} at {events[0]['when']}"  # => reconstruct from facts
# => Proves the stated business rule is observable.
assert audit.startswith("ada placed")
