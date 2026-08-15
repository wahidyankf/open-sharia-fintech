"""Example 42: detect a visual change from deterministic fixture bytes."""

# => Fixture bytes stand in for two normalized screenshot artifacts.
baseline, candidate = b"PNG:blue", b"PNG:orange"
# => Equality is the smallest deterministic visual-regression predicate.
changed = baseline != candidate
# => The assertion proves the test detects a changed rendered artifact.
assert changed is True
# => Output reports the visual-regression result without retaining an image file.
print("visual regression detected")
