"""Example 32: apply one reproducible mobile device profile."""

# => A device profile pins the conditions under which a responsive assertion is meaningful.
profile = {"width": 390, "height": 844, "mobile": True}
# => The fixture renderer chooses the compact layout from the explicit width.
layout = "compact" if profile["width"] < 600 else "wide"
# => Assert both device mode and the responsive layout contract.
assert profile["mobile"] is True and layout == "compact"
# => Output identifies the reproducible emulation result.
print(layout)
