# Optional fields permit additive schema evolution.
from typing import Optional


# Both old and new callers use the same handler.
def greet(name: str, punctuation: Optional[str] = None) -> str:
    # The default preserves the v1 behavior.
    return f"hello, {name}{punctuation or ''}"


# The original schema still works unchanged.
assert greet("Ada") == "hello, Ada"
# The extended schema adds behavior without a break.
assert greet("Ada", "!") == "hello, Ada!"
# Print the compatible new result.
print(greet("Ada", "!"))
