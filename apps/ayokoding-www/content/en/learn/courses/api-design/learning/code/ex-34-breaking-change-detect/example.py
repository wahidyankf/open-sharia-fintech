# pyright: strict
"""Example 34: A Consumer Contract Test Catches a Breaking Change. (co-14)

A consumer contract test asserts the fields a real client depends on are
still present. Removing a field the test asserts on makes the test fail
LOUDLY, at build time -- exactly the point where a breaking change should be
caught, not discovered by a client in production.
"""


def get_article_v1() -> dict[str, object]:  # => the ORIGINAL, contract-conforming response
    return {"id": 1, "title": "Hello", "legacy_field": "still here"}  # => the field the contract needs


def get_article_broken() -> dict[str, object]:  # => co-14: a hypothetical FUTURE, breaking change
    return {"id": 1, "title": "Hello"}  # => "legacy_field" was REMOVED -- a real consumer still needs it


def consumer_contract_test(response: dict[str, object]) -> None:  # => co-14: the test a CI pipeline runs
    assert "id" in response, "contract violation: 'id' missing"  # => still-required field 1
    assert "title" in response, "contract violation: 'title' missing"  # => still-required field 2
    assert "legacy_field" in response, "contract violation: 'legacy_field' missing"  # => the field at risk


consumer_contract_test(get_article_v1())  # => co-14: passes silently -- the contract still holds
print("v1 response: contract test passed")  # => Output: contract test passed

try:  # => co-14: run the SAME test against the hypothetical breaking change
    consumer_contract_test(get_article_broken())  # => this call is expected to fail
    print("broken response: contract test passed (UNEXPECTED)")  # => would only print if the bug went uncaught
except AssertionError as exc:  # => co-14: the breaking change is caught HERE, loudly
    # => exc's message is "contract violation: 'legacy_field' missing" -- names the exact failure
    print(f"broken response: contract test FAILED as expected: {exc}")  # => Output: caught, with a clear reason
