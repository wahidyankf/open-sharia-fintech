# Client discovery decouples the agent from server internals.
from dataclasses import dataclass


# Tool metadata crosses the client-server boundary.
@dataclass(frozen=True)
class Tool:
    # The name is sufficient for this discovery slice.
    name: str


# The server exposes a discoverable local list.
class Server:
    # This tuple models a tools/list response.
    tools = (Tool("greet"),)

    # Return the advertised schema data.
    def list_tools(self) -> tuple[Tool, ...]:
        return self.tools


# The client asks instead of maintaining a separate list.
discovered = Server().list_tools()
# The assertion proves discovery delivered server-owned metadata.
assert [tool.name for tool in discovered] == ["greet"]
# Print the client-visible names.
print([tool.name for tool in discovered])
