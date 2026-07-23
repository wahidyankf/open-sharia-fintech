"""Example 84: a deliberate str-for-int type mismatch -- pyright catches it, python3 still runs it."""


def repeat_label(label: int, times: int) -> str:
    # str(label) works fine even if label is ALREADY a str.
    return " ".join([str(label)] * times)


print(repeat_label("3", 2))  # => a str passed where int is annotated -- Output: 3 3
# => Run: pyright example.py -- flags reportArgumentType, 1 error
# => Run: python3 example.py -- still exits 0, runtime never checks annotations
