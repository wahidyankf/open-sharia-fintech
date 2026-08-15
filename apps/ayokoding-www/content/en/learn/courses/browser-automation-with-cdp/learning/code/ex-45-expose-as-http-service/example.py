"""Example 45: model a narrow HTTP-shaped browser-control service operation."""

# => The request accepts only the fixture origin and one explicit navigate operation.
request = {"operation": "navigate", "url": "https://fixture.test/report"}
# => The service returns data, not a browser handle that leaks resource ownership.
response = {"status": 200, "title": "Fixture report"}
# => Assert authorization-shaped input and the caller-visible service result.
assert request["url"].startswith("https://fixture.test/") and response["status"] == 200
# => Output is the stable API result a client can consume.
print(response)
