# A fake server replaces a live MCP deployment in tests.
class FakeServer:
    # This method is a stable local contract.
    def call(self, name: str) -> str:
        # The fake exposes exactly one expected observation.
        return f"fake:{name}"


# A client test depends only on the contract.
def test_client() -> None:
    # Construct the fake with no credentials or network.
    server = FakeServer()
    # Assert the same result a real client expects.
    assert server.call("greet") == "fake:greet"


# Running the test directly keeps this artifact standalone.
test_client()
# Print the passing deterministic state.
print("passed")
