# This registry is a local MCP-server-shaped capability provider.
from dataclasses import dataclass


# A tool descriptor is what the server advertises.
@dataclass(frozen=True)
class Tool:
    # The capability name is stable for clients.
    name: str


# The server owns its advertised capability list.
class Server:
    # Start with a single local tool.
    tools = (Tool("greet"),)

    # Discovery returns metadata, never executes a tool.
    def list_tools(self) -> tuple[Tool, ...]:
        return self.tools


# The local server starts with no socket or credentials.
server = Server()
# The assertion verifies startup advertisement.
assert server.list_tools()[0].name == "greet"
# Print the visible capability.
print(server.list_tools())
