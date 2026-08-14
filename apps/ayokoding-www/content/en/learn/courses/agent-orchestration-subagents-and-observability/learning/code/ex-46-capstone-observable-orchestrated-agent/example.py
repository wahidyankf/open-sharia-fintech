# Workers return bounded summaries to the parent.
summaries = ("research:ok", "test:ok")
# The trace records parent and worker work.
trace = ("run", "research", "test")
# Metrics expose the local operational outcome.
metrics = {"cost": 2, "latency_ms": 5}
# A fixture eval verifies the complete local result.
passed = all(item.endswith("ok") for item in summaries)
# The composed system is observable and passes its check.
assert trace and metrics and passed
# Print the capstone result.
print({"passed": passed, "trace": trace})
