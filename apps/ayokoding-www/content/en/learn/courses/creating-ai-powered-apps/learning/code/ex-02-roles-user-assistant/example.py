roles = ["user", "assistant", "user"]  # => fixture conversation order
assert all(a != b for a, b in zip(roles, roles[1:]))  # => roles alternate
print("PASS: roles-user-assistant")  # => offline acceptance result
