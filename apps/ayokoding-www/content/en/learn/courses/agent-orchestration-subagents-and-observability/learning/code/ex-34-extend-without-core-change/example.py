# The core loop stays a stable small function.
def core() -> str:
    return "result"


# An extension wraps the core's returned value.
def extension() -> str:
    return f"{core()}:extra"


# The original core contract remains unchanged.
assert core() == "result" and extension() == "result:extra"
# Print the extension result.
print(extension())
