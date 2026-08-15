"""Example 24: return a deterministic local response for an authorized request."""

# => The mock is a fixture contract, not a substitute for an untrusted remote service.
request_url = "https://fixture.test/api/greeting"
# => The canned result is scoped to the one endpoint the example owns.
response = {"url": request_url, "status": 200, "body": {"message": "hello"}}
# => The assertion verifies both routing and the UI-relevant response value.
assert response["url"] == request_url and response["body"]["message"] == "hello"
# => Output exposes the stable mock payload for a test assertion.
print(response["body"])
