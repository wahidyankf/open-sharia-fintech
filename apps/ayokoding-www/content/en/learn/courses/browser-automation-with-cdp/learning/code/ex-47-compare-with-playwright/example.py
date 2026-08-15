"""Example 47: compare the result contract of raw CDP and a wrapper."""

# => Raw CDP exposes the method and its JSON-like result directly.
raw_result = {"method": "Runtime.evaluate", "value": "Fixture title"}
# => A wrapper changes ergonomics but should preserve the page-visible result.
wrapper_result = "Fixture title"
# => Compare the behavior contract instead of claiming their implementations are identical.
assert raw_result["value"] == wrapper_result
# => Output names the shared observable result.
print(wrapper_result)
