# Startup discovery makes the client schema-driven.
from dataclasses import dataclass


# A tool descriptor is all the client needs to build its registry.
@dataclass(frozen=True)
class Tool:
    # Names are server-owned and may grow independently.
    name: str


# The provider added status without editing any client code.
server_tools = (Tool("greet"), Tool("status"))


# Startup turns current server metadata into a usable registry.
def startup_registry(tools: tuple[Tool, ...]) -> dict[str, Tool]:
    # Map names to descriptors after discovery completes.
    return {tool.name: tool for tool in tools}


# The client has no hard-coded list to maintain.
registry = startup_registry(server_tools)
# The assertion proves the newly advertised capability is visible.
assert "status" in registry
# Print the dynamically discovered registry keys.
print(sorted(registry))
