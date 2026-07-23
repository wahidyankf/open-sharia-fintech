"""Example 6: Balanced Parentheses via Stack."""


# Returns True if every '(' in text has a matching ')' (co-04).
def is_balanced(text: str) -> bool:  # => a plain function, no class needed
    stack: list[str] = []  # => tracks open parens waiting for a close
    for char in text:  # => scans the string left to right, once, O(n)
        if char == "(":  # => an opener -- remember it for later
            stack.append(char)  # => push: remember this open paren
        elif char == ")":  # => a closer -- must match SOME earlier opener
            if not stack:  # => a close with nothing open means unbalanced
                return False  # => bail out early -- no matching '(' exists
            stack.pop()  # => pop: this close matches the most recent open
    return not stack  # => balanced only if every open was eventually closed


balanced = is_balanced("(())")  # => "(())": open,open,close,close -- stack empties
unbalanced = is_balanced("(()")  # => "(()": one open never gets a matching close
print(balanced)  # => Output: True
print(unbalanced)  # => Output: False

assert is_balanced("(())") is True  # => confirms nested, fully-closed parens balance
assert is_balanced("(()") is False  # => confirms a dangling open paren is detected
assert is_balanced("") is True  # => confirms the empty string is trivially balanced
print("ex-06 OK")  # => Output: ex-06 OK
