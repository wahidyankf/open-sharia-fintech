# Providers contribute their own advertised tools.
servers = {"notes": ("search",), "status": ("health",)}
# A manifest is a read-only summary of discovery.
manifest = {server: list(tools) for server, tools in servers.items()}
# Every provider capability appears in the review artifact.
assert manifest == {"notes": ["search"], "status": ["health"]}
# Print the capability manifest.
print(manifest)
