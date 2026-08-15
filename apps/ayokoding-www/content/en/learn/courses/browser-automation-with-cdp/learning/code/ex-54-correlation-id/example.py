"""Example 54: carry one correlation id through request and result."""

# => The id joins caller intent, protocol command, and the later audit record.
request = {"correlation_id": "run-42", "method": "Page.navigate"}
# => The service copies it to the result instead of inventing unrelated identifiers.
result = {"correlation_id": request["correlation_id"], "status": "ok"}
# => The assertion proves the trace remains joinable across the service boundary.
assert result["correlation_id"] == "run-42"
# => Output is a small, safe trace record.
print(result)
