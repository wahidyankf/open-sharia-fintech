"""Example 25: Type Hints on a Function Signature."""


# Type hints document intent; CPython never checks them at call time (co-22).
def add(a: int, b: int) -> int:  # => a and b MUST be int; the return MUST be int
    return a + b  # => runs identically whether or not the hints are present


result = add(
    2, 3
)  # => hints are advisory here -- CPython never checks them at call time
print(result)  # => Output: 5
print(add.__annotations__)  # => introspects the hints themselves, as a dict

assert result == 5  # => confirms the function's actual behavior is unaffected by hints
assert add.__annotations__ == {
    "a": int,
    "b": int,
    "return": int,
}  # => confirms hints stored
print("ex-25 OK")  # => Output: ex-25 OK
