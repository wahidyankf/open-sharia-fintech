"""Example 20: Sort Tuples by a Field."""

# key=lambda picks WHICH field drives the comparison -- the tuples themselves
# are never modified, only the order of the returned list changes (co-15).
people: list[tuple[int, str]] = [(3, "carol"), (1, "alice"), (2, "bob")]
by_name = sorted(people, key=lambda pair: pair[1])  # => sorts by the string field
print(by_name)  # => Output: [(1, 'alice'), (2, 'bob'), (3, 'carol')]

assert by_name == [(1, "alice"), (2, "bob"), (3, "carol")]  # => confirms name order
assert [pair[0] for pair in by_name] == [1, 2, 3]  # => IDs happen to align too here
print("ex-20 OK")  # => Output: ex-20 OK
