# A typed registry is a local MCP-server-shaped provider.
from typing import Callable

# Each handler is deterministic and credential-free.
TOOLS: dict[str, Callable[[str], str]] = {
    "read": lambda x: x,
    "write": lambda x: f"saved:{x}",
    "search": lambda x: f"found:{x}",
}
# Every advertised tool is callable.
assert [TOOLS[name]("note") for name in TOOLS] == ["note", "saved:note", "found:note"]
# Print the discoverable names.
print(sorted(TOOLS))
