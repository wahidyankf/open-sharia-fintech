# A run metric record keeps cost and latency explicit.
metrics = {"cost": 3, "latency_ms": 20, "success": True}
# Each operational value is available for comparison.
assert metrics["success"] and metrics["cost"] == 3
# Print the compact run metrics.
print(metrics)
