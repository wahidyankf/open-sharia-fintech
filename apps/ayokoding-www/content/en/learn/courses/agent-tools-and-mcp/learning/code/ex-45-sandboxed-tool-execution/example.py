# A workspace label models an isolated execution boundary.
def run(workspace: str) -> dict[str, str]:
    # The tool returns its assigned boundary for auditing.
    return {"workspace": workspace, "result": "ok"}


# The local operation stays inside its named sandbox.
result = run("sandbox-a")
# The assertion verifies the boundary travels with the result.
assert result["workspace"] == "sandbox-a"
# Print the sandbox-scoped outcome.
print(result)
