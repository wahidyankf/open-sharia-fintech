"""Example 39: record minimal HAR-like metadata for a fixture page load."""

# => Keep only request timing and status, never an unbounded response body.
entries = [{"url": "https://fixture.test/", "status": 200, "duration_ms": 12}]
# => A HAR-like trace is useful when each entry has an observable response status.
statuses = [entry["status"] for entry in entries]
# => The fixture load contains one successful, bounded trace entry.
assert statuses == [200]
# => Output is compact diagnostic evidence for a later failure report.
print(entries)
