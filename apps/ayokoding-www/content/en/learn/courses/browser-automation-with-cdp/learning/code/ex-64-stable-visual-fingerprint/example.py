"""Example 64: derive a stable fingerprint from normalized fixture rendering data."""

import hashlib  # => hashlib produces a reproducible digest from controlled local bytes.

# => Normalized inputs pin viewport and rendered content before a visual comparison.
rendered = b"viewport=390x844;title=Fixture"
# => A digest gives visual tests a compact equality predicate.
fingerprint = hashlib.sha256(rendered).hexdigest()
# => The assertion verifies a fixed-width stable fingerprint was produced.
assert len(fingerprint) == 64
# => Output records the fingerprint, not a screenshot or browser session.
print(fingerprint)
