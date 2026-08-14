# Correlation ids prevent shared-server cross-talk.
def call(agent_id: str) -> dict[str, str]:
    # Echo the caller id in the typed response.
    return {"agent_id": agent_id, "result": "ok"}


# Two callers use one local provider contract.
responses = [call("a"), call("b")]
# Each response preserves its own identity.
assert [item["agent_id"] for item in responses] == ["a", "b"]
# Print the separated responses.
print(responses)
