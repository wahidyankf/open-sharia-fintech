# The provider publishes a per-turn-filterable capability registry.
tools = {"greet": lambda name: f"hello, {name}"}
# Resources and prompts remain non-executable provider metadata.
resources = {"policy://greet": "Use the caller name."}
prompts = {"greet-user": "Greet {name}."}


# A client discovers only the requested allowed tool.
def complete(name: str) -> str:
    # Validation checks the server-owned registry first.
    if "greet" not in tools:
        return "error"
    # The tool returns a compact typed local observation.
    return tools["greet"](name)


# The end-to-end task uses only discovered provider data.
assert complete("Ada") == "hello, Ada" and resources and prompts
# Print the complete local task result.
print(complete("Ada"))
