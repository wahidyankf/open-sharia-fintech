"""Example 40: register instrumentation before a fixture page script runs."""

# => Registration happens before the page script to make ordering explicit.
events = ["instrumentation-registered", "page-script-ran"]
# => The first event represents addScriptToEvaluateOnNewDocument-like setup.
instrumentation_index = events.index("instrumentation-registered")
# => The assertion proves instrumentation precedes page-owned script execution.
assert instrumentation_index < events.index("page-script-ran")
# => Output records the safe local execution order.
print(" -> ".join(events))
