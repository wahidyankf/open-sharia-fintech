"""Example 67: verify a wrapper preserves the needed CDP result contract."""

# => The low-level command exposes a concrete serializable response shape.
cdp = {"id": 3, "result": {"value": "Fixture title"}}
# => The wrapper publishes the same user-visible value through a simpler API.
wrapper = {"title": "Fixture title"}
# => Compare the guarantee callers need instead of comparing implementation details.
assert cdp["result"]["value"] == wrapper["title"]
# => Output names the preserved contract value.
print(wrapper["title"])
