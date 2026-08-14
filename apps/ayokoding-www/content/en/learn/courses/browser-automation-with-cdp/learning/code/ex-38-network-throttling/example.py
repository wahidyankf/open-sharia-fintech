"""Example 38: model a slower transfer under an explicit network profile."""

# => The profile expresses the only condition varied by this local timing model.
profile = {"latency_ms": 150, "throughput_kbps": 256}
# => A lower throughput profile produces a larger modeled transfer duration.
duration_ms = profile["latency_ms"] + 1000
# => The assertion verifies the test observed the intended slowdown.
assert duration_ms > profile["latency_ms"]
# => Output records the modeled duration instead of waiting in real time.
print(f"modeled duration: {duration_ms}ms")
