# pyright: strict
"""Example 71: Implementing Handlers From the Spec. (co-12)

Following Example 70's contract-first spec, the handler is now WRITTEN TO
MATCH the schema that already existed -- the spec drove the implementation,
and this example verifies the resulting response actually satisfies every
field the spec required.
"""

REQUIRED_FIELDS = ["id", "title"]  # => co-12: taken directly from Example 70's already-agreed contract
# => REQUIRED_FIELDS is ['id', 'title'] (type: list[str]) -- lifted verbatim from the spec


def get_article_handler(article_id: int) -> dict[str, object]:  # => co-12: WRITTEN AFTER the spec existed
    return {"id": article_id, "title": "Hello, API Design"}  # => co-12: deliberately matches REQUIRED_FIELDS


def response_matches_schema(response: dict[str, object], required: list[str]) -> bool:  # => co-12: validates
    return all(field in response for field in required)  # => co-12: every required field must be present


response = get_article_handler(1)  # => co-12: calls the handler that was written to satisfy the spec
print(f"response: {response}")  # => Output: {'id': 1, 'title': 'Hello, API Design'}

conforms = response_matches_schema(response, REQUIRED_FIELDS)  # => co-12: checks it against the CONTRACT
# => conforms is True (type: bool) -- the implementation was designed AFTER the contract, not before
print(f"conforms to spec: {conforms}")  # => Output: True -- co-12: the handler satisfies what was designed first
