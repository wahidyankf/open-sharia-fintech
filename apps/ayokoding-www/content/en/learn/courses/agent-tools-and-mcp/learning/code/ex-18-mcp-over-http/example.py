# A dictionary models a decoded HTTP JSON request.
Request = dict[str, str]


# The handler models the remote server endpoint.
def handle(request: Request) -> dict[str, str]:
    # Return JSON-shaped data without opening a listener.
    return {"status": "200", "result": request["method"]}


# The local request crosses the simulated transport boundary.
response = handle({"method": "tools/list"})
# The response proves remote invocation semantics.
assert response == {"status": "200", "result": "tools/list"}
# Print the transport result.
print(response)
