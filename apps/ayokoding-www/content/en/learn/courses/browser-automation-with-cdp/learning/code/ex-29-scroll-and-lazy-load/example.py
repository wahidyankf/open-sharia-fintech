"""Example 29: scrolling reveals a local lazy-loaded fixture item."""

# => The initial viewport deliberately lacks the item expected after scrolling.
visible = ["top"]
# => A modeled scroll updates the fixture's visible content deterministically.
visible.append("lazy-item")
# => Assert the content change, not merely that an input action was dispatched.
assert visible[-1] == "lazy-item"
# => Output records the newly observable lazy-loaded item.
print(visible)
