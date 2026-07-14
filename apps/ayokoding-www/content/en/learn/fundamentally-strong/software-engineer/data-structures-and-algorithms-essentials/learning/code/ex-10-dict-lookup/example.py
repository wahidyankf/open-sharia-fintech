"""Example 10: Dict Lookup with .get."""

# dict gives average-O(1) keyed lookup via hashing -- no scan required (co-08).
ages: dict[str, int] = {"alice": 30, "bob": 25}  # => a hash map literal

present = ages.get("alice")  # => hashes "alice" straight to its bucket -- O(1) average
absent = ages.get("carol")  # => key not found -- .get() returns None instead of raising
default = ages.get("carol", 0)  # => a second argument supplies a fallback value
print(present)  # => Output: 30
print(absent)  # => Output: None
print(default)  # => Output: 0

assert present == 30  # => confirms the present key resolves to its stored value
assert absent is None  # => confirms .get() with no default returns None, not KeyError
assert default == 0  # => confirms the explicit default is used when the key is missing
print("ex-10 OK")  # => Output: ex-10 OK
