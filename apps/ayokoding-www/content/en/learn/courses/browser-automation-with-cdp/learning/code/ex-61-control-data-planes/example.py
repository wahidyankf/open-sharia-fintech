"""Example 61: separate service control metadata from page result data."""

# => Control data decides authorization and timeout without mixing it into page content.
control = {"allowed": True, "timeout_ms": 100}
# => Data contains only the caller-visible page observation.
data = {"title": "Fixture report"}
# => The assertion preserves two explicit boundaries in the service contract.
assert control["allowed"] is True and data == {"title": "Fixture report"}
# => Output shows only the safe data-plane value.
print(data)
