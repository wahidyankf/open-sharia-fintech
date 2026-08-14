"""Worked Example 40: express an architecture characteristic as a test."""


def test_domain_has_no_infrastructure_imports() -> None:
    imports = {"orders.domain": {"decimal", "typing"}}
    assert imports["orders.domain"].isdisjoint({"sqlalchemy", "fastapi"})


test_domain_has_no_infrastructure_imports()
print("fitness function passed")
