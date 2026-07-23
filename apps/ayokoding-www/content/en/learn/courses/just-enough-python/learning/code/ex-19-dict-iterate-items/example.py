"""Example 19: Dict Iterate Items."""

counts: dict[str, int] = {"a": 1, "b": 2}  # => counts is {"a": 1, "b": 2}
# .items() yields (key, value) pairs, in insertion order.
for key, value in counts.items():  # => unpacks each (key, value) pair per iteration
    print(f"{key}={value}")  # => Output: a=1 then b=2
