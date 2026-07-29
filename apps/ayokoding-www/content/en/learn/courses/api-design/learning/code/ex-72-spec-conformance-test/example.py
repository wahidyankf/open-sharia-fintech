# pyright: strict
"""Example 72: Asserting Live Responses Conform to the Spec. (co-12, co-01)

An OpenAPI spec (co-01: "the API IS the contract with its consumers") is
only as trustworthy as the tests that enforce it -- a conformance test
calls the LIVE handler and asserts the response matches the declared
schema's types, not merely that the required keys exist (Example 71).
"""

from typing import Any  # => the spec is arbitrary nested JSON

RESPONSE_SCHEMA: dict[str, Any] = {  # => co-12: field name -> the Python type it must actually be
    "id": int,  # => co-12: the spec says "integer" -- Python's int
    "title": str,  # => co-12: the spec says "string" -- Python's str
}  # => end of RESPONSE_SCHEMA


def get_article_handler(article_id: int) -> dict[str, object]:  # => the LIVE handler under test
    return {"id": article_id, "title": "Hello, API Design"}  # => a conforming response


def get_article_handler_broken(article_id: int) -> dict[str, object]:  # => co-12: a hypothetical regression
    return {"id": str(article_id), "title": "Hello, API Design"}  # => co-12: "id" is now a STRING, not int


def assert_conforms(response: dict[str, object], schema: dict[str, Any]) -> None:  # => co-12: the actual test
    for field_name, expected_type in schema.items():  # => co-01: checks EVERY promised field, one by one
        assert field_name in response, f"missing field: {field_name!r}"  # => co-12: presence check
        actual_value = response[field_name]  # => the live value returned
        assert isinstance(actual_value, expected_type), (  # => co-12: TYPE check, not just presence
            f"{field_name!r} should be {expected_type.__name__}, got {type(actual_value).__name__}"
        )  # => end of the type-mismatch message


assert_conforms(get_article_handler(1), RESPONSE_SCHEMA)  # => co-01: the contract holds -- passes silently
print("conforming handler: contract test passed")  # => Output: contract test passed

try:  # => co-12: run the SAME test against the type-regressed handler
    assert_conforms(get_article_handler_broken(1), RESPONSE_SCHEMA)  # => expected to fail on "id"'s type
    print("broken handler: contract test passed (UNEXPECTED)")  # => would only print if the bug went uncaught
except AssertionError as exc:  # => co-12: the type regression is caught HERE, loudly
    # => exc's message names the exact field and the exact type mismatch found
    print(f"broken handler: contract test FAILED as expected: {exc}")  # => Output: caught, with a clear reason
