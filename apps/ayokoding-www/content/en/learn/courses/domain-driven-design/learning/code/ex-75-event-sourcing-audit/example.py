"""Example 75: event history can answer who changed what and when."""

events = [
    {"who": "ada", "what": "placed", "when": "2026-08-14T00:00:00Z"}
]  # => audit facts retain actor and time
audit = f"{events[0]['who']} {events[0]['what']} at {events[0]['when']}"  # => reconstruct from facts
assert audit.startswith("ada placed")
