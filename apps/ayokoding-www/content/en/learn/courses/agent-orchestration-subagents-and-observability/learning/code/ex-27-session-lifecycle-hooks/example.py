# A lifecycle trace models session hooks.
events: list[str] = []
# Start is recorded before work begins.
events.append("start")
# Stop is recorded after work completes.
events.append("stop")
# The ordered trace defines the session boundary.
assert events == ["start", "stop"]
# Print the lifecycle events.
print(events)
