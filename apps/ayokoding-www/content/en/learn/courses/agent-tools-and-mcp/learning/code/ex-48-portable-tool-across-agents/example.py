# One provider contract serves different loop implementations.
def tool(name: str) -> str:
    # The local handler is independent of the caller.
    return f"hello, {name}"


# The first loop invokes the portable contract.
first = tool("Ada")
# The second loop invokes the same portable contract.
second = tool("Ada")
# Both loops receive the identical provider result.
assert first == second == "hello, Ada"
# Print the portable result.
print(first)
