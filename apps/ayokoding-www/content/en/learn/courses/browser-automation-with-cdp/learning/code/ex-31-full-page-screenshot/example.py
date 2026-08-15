"""Example 31: model a full-page screenshot with explicit dimensions."""

# => Keep artifact metadata separate from bytes so size expectations are testable.
image = {"width": 1280, "height": 2400, "bytes": b"PNG"}
# => Full-page capture must be taller than the fixture viewport to prove scrolling coverage.
viewport_height = 800
# => The assertion checks dimensions without writing or retaining an image file.
assert image["height"] > viewport_height and image["bytes"] == b"PNG"
# => Output records the context needed for a later visual comparison.
print(f"{image['width']}x{image['height']}")
