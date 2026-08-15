# Each worker reports a local operational measurement.
runs = ((2, 10), (3, 15))
# Totals make coordination cost visible.
cost = sum(item[0] for item in runs)
# Latency is separately accumulated for this local model.
latency = sum(item[1] for item in runs)
# The compact report supports a design comparison.
assert (cost, latency) == (5, 25)
# Print the orchestration metrics.
print({"cost": cost, "latency": latency})
