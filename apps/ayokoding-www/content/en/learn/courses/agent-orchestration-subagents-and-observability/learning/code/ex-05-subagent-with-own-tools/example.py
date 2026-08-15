# This specialist receives only task-relevant tools.
tools = ("search",)
# A write capability is intentionally absent.
assert "search" in tools and "write" not in tools
# The narrow registry is the authority boundary.
print(tools)
