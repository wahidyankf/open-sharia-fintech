"""Example 50: combine allowlisting, a pool result, and an artifact response."""

# => The capstone request starts at an explicit authorized fixture origin.
request = {"url": "https://fixture.test/checkout", "operation": "screenshot"}
# => The service response is plain data so callers cannot retain a browser target.
result = {"status": 200, "title": "Checkout", "screenshot": b"PNG"}
# => The end-to-end assertion covers authorization and the requested artifact contract.
assert (
    request["url"].startswith("https://fixture.test/")
    and result["screenshot"] == b"PNG"
)
# => Output is a deterministic local capstone result.
print(result["title"])
