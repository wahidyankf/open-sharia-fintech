# Discovery supplies the client-owned usable surface.
tools = {"add": lambda left, right: left + right}


# Validation ensures the proposed tool exists.
def run(name: str, left: int, right: int) -> str:
    # Unknown names cannot be dispatched.
    if name not in tools:
        return "error"
    # A successful typed result completes the local goal.
    return "done" if tools[name](left, right) == 5 else "error"


# The deterministic agent task uses only discovery data.
assert run("add", 2, 3) == "done"
# Print the completed goal.
print(run("add", 2, 3))
