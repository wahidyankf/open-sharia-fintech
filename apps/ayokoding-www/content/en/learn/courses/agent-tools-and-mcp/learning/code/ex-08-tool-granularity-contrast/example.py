# Tool names show whether the surface is shaped to tasks.
from dataclasses import dataclass


# Each tool carries only the selection metadata needed here.
@dataclass(frozen=True)
class Tool:
    # The name reveals the authority granted.
    name: str


# A focused selector maps a read intent to a read operation.
def select(task: str, tools: list[Tool]) -> Tool:
    # Read intent should not select a write-capable catch-all.
    return next(tool for tool in tools if "read" in tool.name)


# The coarse tool hides two different authorities.
coarse = Tool("manage_note")
# Focused tools expose the intended operation plainly.
focused = [Tool("read_note"), Tool("write_note")]
# The deterministic fake demonstrates the clearer selection.
assert select("read note", focused).name == "read_note"
# The output compares the available surface shapes.
print(coarse.name, [tool.name for tool in focused])
