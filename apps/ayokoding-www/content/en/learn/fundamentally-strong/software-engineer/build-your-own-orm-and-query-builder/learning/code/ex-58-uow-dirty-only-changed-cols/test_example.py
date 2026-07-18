"""Example 58: pytest verification for Minimal Changed-Columns Diffing."""

from example import User, changed_columns


def test_only_the_mutated_field_appears_in_the_diff() -> None:
    snapshot = {"id": 1, "name": "Grace", "email": "g@example.com"}  # => load-time snapshot
    user = User(id=1, name="Grace", email="g@example.com")  # => starts identical
    user.name = "Gracie"  # => mutate ONLY name
    diff = changed_columns(user, snapshot)  # => compute the diff
    assert diff == {"name": "Gracie"}  # => email absent -- unchanged


def test_no_mutation_produces_an_empty_diff() -> None:
    snapshot = {"id": 1, "name": "A", "email": "a@x.com"}
    user = User(id=1, name="A", email="a@x.com")  # => nothing mutated
    assert changed_columns(user, snapshot) == {}  # => nothing to update


# => Run: pytest -- Output: 2 passed
