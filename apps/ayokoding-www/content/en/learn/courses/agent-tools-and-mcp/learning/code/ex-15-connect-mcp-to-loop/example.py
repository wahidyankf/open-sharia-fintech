# The loop dispatches a discovered tool without owning its implementation.
from collections.abc import Callable


# A server exposes a local handler registry.
server: dict[str, Callable[[str], str]] = {"greet": lambda name: f"hello, {name}"}


# Discovery returns the server-owned capability names.
def discover() -> tuple[str, ...]:
    # The loop receives names rather than hard-coded handlers.
    return tuple(server)


# Dispatch validates the requested tool against discovery.
def run_loop(tool: str, name: str) -> str:
    # Reject a call that is not currently advertised.
    if tool not in discover():
        raise ValueError("tool unavailable")
    # Invoke the provider only after the boundary check.
    return server[tool](name)


# The fake loop reaches the local MCP-shaped server.
assert run_loop("greet", "Ada") == "hello, Ada"
# Print the observation appended to loop state.
print(run_loop("greet", "Ada"))
