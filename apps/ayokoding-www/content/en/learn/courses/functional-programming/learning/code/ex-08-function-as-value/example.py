"""Example 8: A Function Assigned to a Variable."""


def shout(text: str) -> str:  # => an ordinary function, defined once
    return text.upper() + "!"  # => uppercases and appends an exclamation mark


greeter = shout  # => assigns the FUNCTION OBJECT itself to a new name -- no call, no ()
# => greeter and shout now both refer to the SAME underlying function object

direct_result = shout("hello")  # => calling through the original name
aliased_result = greeter("hello")  # => calling through the alias -- identical behavior

print(direct_result)  # => Output: HELLO!
print(aliased_result)  # => Output: HELLO!
print(direct_result == aliased_result)  # => Output: True -- same function, same result
print(greeter is shout)  # => Output: True -- greeter is not a copy, it IS shout
