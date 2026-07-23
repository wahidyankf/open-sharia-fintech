"""Example 47: Custom Module Import."""

# Python resolves sibling-directory imports via the current working directory.
from greeting import shout  # => imports the sibling file greeting.py's shout() function

print(shout("Ada"))  # => Output: HELLO, ADA!
