"""Example 26: two targets retain independent page state."""

# => Each target owns its title rather than sharing mutable page state.
tabs = {"target-a": "Orders", "target-b": "Reports"}
# => Read both targets through their own stable target identifiers.
titles = (tabs["target-a"], tabs["target-b"])
# => The distinct values prove work in one tab has not overwritten the other.
assert titles == ("Orders", "Reports")
# => Output is a deterministic observation of independent state.
print(titles)
