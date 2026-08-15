"""Example 21: collect minimal metadata from a local network-event fixture."""

# => The fixture contains metadata only; no real request body or credential is captured.
requests = [{"method": "GET", "url": "https://fixture.test/report", "status": 200}]
# => Project only the fields needed for an observable request-log assertion.
log = [(request["method"], request["status"]) for request in requests]
# => A successful fixture request has one GET response with status 200.
assert log == [("GET", 200)]
# => Output is safe diagnostics rather than a raw network trace.
print(log)
