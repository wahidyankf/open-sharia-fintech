"""Example 13: String Methods."""

raw: str = "  a b c  "
# repr() makes the leading/trailing spaces visible as explicit quote characters --
# a plain print() here would produce the same spaces, just invisible on the page.
print(repr(raw.upper()))  # => .upper() keeps whitespace -- Output: '  A B C  '
print(repr(raw.strip()))  # => .strip() trims leading/trailing space -- Output: 'a b c'
print(raw.strip().split())  # => .split() splits on any whitespace run
# => Output: ['a', 'b', 'c']
