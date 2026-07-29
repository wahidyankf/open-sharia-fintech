# pyright: strict
"""Example 78: Pact -- consumer-driven contract testing. (co-35)

In consumer-driven contract testing, the CONSUMER writes a test describing
the request it sends and the response it expects; this test GENERATES a
contract. The PROVIDER is then verified against that contract. This example
models a consumer contract and verifies the provider honours it. Source:
pact.io -- "code-first consumer-driven contract testing."
"""

from dataclasses import dataclass  # => a small typed record for the contract


@dataclass  # => co-35: the consumer's declared expectation of one interaction
class Interaction:
    description: str  # => a human label for this interaction
    request: dict[str, object]  # => what the consumer sends (method + path)
    expected_response_status: int  # => the status the consumer depends on
    expected_body_fields: list[str]  # => the response fields the consumer reads


# The CONSUMER declares: "when I GET /users/1, I expect 200 with {id, name}."
CONSUMER_CONTRACT: list[Interaction] = [  # => co-35: the generated contract
    Interaction(
        description="get a user by id",
        request={"method": "GET", "path": "/users/1"},
        expected_response_status=200,
        expected_body_fields=["id", "name"],
    ),
]


def provider_handle(method: str, path: str) -> tuple[int, dict[str, object]]:  # => the PROVIDER's real handler
    if method == "GET" and path == "/users/1":  # => the route the consumer calls
        return 200, {"id": 1, "name": "ada", "email": "ada@example.com"}  # => the real response (carries an EXTRA field)
    return 404, {"error": "not found"}  # => unknown route


def verify_provider(contract: list[Interaction]) -> list[tuple[str, bool]]:  # => co-35: provider verification
    results: list[tuple[str, bool]] = []  # => per-interaction pass/fail
    for interaction in contract:  # => replay each consumer interaction against the provider
        method = str(interaction.request["method"])  # => the consumer's method
        path = str(interaction.request["path"])  # => the consumer's path
        status, body = provider_handle(method, path)  # => the provider's real response
        status_ok = status == interaction.expected_response_status  # => status matches the contract
        fields_ok = all(field in body for field in interaction.expected_body_fields)  # => required fields present
        results.append((interaction.description, status_ok and fields_ok))  # => pass/fail for this interaction
    return results  # => the verification report


report = verify_provider(CONSUMER_CONTRACT)  # => co-35: verify the provider against the consumer contract
for desc, passed in report:  # => print each interaction's result
    print(f"interaction '{desc}': {'PASS' if passed else 'FAIL'}")  # => Output: PASS

assert all(passed for _desc, passed in report)  # => co-35: the provider honours the consumer contract
