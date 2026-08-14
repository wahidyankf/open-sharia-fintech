# An inspector reports all advertised MCP capability categories.
from dataclasses import dataclass


# The server descriptor keeps categories explicit.
@dataclass(frozen=True)
class Server:
    # Tools are executable capabilities.
    tools: tuple[str, ...]
    # Resources are readable context.
    resources: tuple[str, ...]
    # Prompts are parameterized instruction templates.
    prompts: tuple[str, ...]


# This local server provides one of every category.
server = Server(("greet",), ("policy://greet",), ("greet-user",))
# Inspection reads metadata without invoking authority.
report = {
    "tools": server.tools,
    "resources": server.resources,
    "prompts": server.prompts,
}
# The assertion verifies the complete capability surface.
assert all(report.values())
# Print the deployment-review report.
print(report)
