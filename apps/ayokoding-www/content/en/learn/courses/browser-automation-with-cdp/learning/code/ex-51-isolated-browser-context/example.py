"""Example 51: isolate fixture storage between browser contexts."""

# => Each context owns an independent cookie store for deterministic tests.
contexts = {"first": {"cookie": "a"}, "second": {"cookie": "b"}}
# => Mutate only the first context to demonstrate that isolation holds.
contexts["first"]["cookie"] = "changed"
# => The second context remains untouched by the first context's state transition.
assert contexts["second"]["cookie"] == "b"
# => Output confirms independent context ownership.
print("contexts isolated")
