"""Example 48: recognize, but do not evade, a headless detection signal."""

# => The fixture exposes a signal so its ethical handling can be discussed locally.
environment = {"webdriver": True, "mode": "headless"}
# => Detection is an observation; this example deliberately performs no evasion.
detected = environment["webdriver"] is True
# => The assertion proves the signal can be surfaced in a transparent trace.
assert detected is True
# => Output states the observation without modifying browser-identifying behavior.
print("headless signal observed")
