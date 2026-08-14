"""Example 19: wait for an authorized fixture selector without a fixed sleep."""

# => Each snapshot models an event-driven DOM observation from a local fixture.
snapshots = [set(), {"#ready"}]
# => The selector is the explicit readiness condition for the next automation step.
ready = next(snapshot for snapshot in snapshots if "#ready" in snapshot)
# => The assertion proves readiness was observed rather than guessed after a delay.
assert "#ready" in ready
# => Output gives the caller the concrete condition that became true.
print("selector ready: #ready")
