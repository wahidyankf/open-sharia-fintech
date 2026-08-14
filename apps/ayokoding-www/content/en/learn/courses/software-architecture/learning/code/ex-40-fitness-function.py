# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 40: express an architecture characteristic as a test."""


# => This keeps the modeled rule explicit so its trade-off can be inspected.
def test_domain_has_no_infrastructure_imports() -> None:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    imports = {"orders.domain": {"decimal", "typing"}}
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    assert imports["orders.domain"].isdisjoint({"sqlalchemy", "fastapi"})


# => This keeps the modeled rule explicit so its trade-off can be inspected.
test_domain_has_no_infrastructure_imports()
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print("fitness function passed")
