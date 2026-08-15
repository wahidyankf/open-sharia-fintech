"""Example 62: validate a narrow browser-operation input schema."""

# => The fixture input names one supported operation and an authorized URL.
request = {
    "operation": "navigate",
    "url": "https://fixture.test/report",
    "timeout_ms": 100,
}
# => Validation checks operation, origin, and a positive bounded timeout.
valid = (
    request["operation"] == "navigate"
    and request["url"].startswith("https://fixture.test/")
    and request["timeout_ms"] > 0
)
# => The assertion proves invalid shapes would be rejected before target allocation.
assert valid is True
# => Output confirms the request passed the local schema boundary.
print("schema valid")
