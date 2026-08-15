# This local record is a text-only extension-surface diagram.
surface = ("tools", "MCP", "hooks", "skills")
# Each mechanism must remain visible in architecture review.
assert set(surface) == {"tools", "MCP", "hooks", "skills"}
# Print the extension surface.
print(" → ".join(surface))
