"""Example 18: lifecycle events are observed in a meaningful readiness order."""

# => A local fixture models the event stream without opening a browser or contacting a website.
events = [
    "Page.frameStartedLoading",
    "Page.domContentEventFired",
    "Page.loadEventFired",
]
# => DOM content is ready before the whole document's load event in this fixture sequence.
dom_ready = events.index("Page.domContentEventFired")
# => Full load follows DOM readiness, so a caller can choose the weakest sufficient wait.
fully_loaded = events.index("Page.loadEventFired")
# => The assertion makes sequence, rather than a guessed sleep, the tested contract.
assert dom_ready < fully_loaded
# => Output is deterministic evidence of the observed lifecycle order.
print(" -> ".join(events))
