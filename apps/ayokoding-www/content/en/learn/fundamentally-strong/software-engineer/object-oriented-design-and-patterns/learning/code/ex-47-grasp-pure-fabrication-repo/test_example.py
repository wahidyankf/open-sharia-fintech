"""Example 47: pytest verification for the Repository Pure Fabrication."""

import inspect

from example import User, UserRepository


def test_user_class_defines_no_io_touching_methods() -> None:
    # => the domain class exposes only __init__/__post_init__ plus dataclass-generated
    # => dunder methods -- no save/load/find method exists on User itself
    method_names: set[str] = {name for name, _ in inspect.getmembers(User, predicate=inspect.isfunction)}
    assert "save" not in method_names  # => persistence lives on the repository, not here
    assert "find_by_id" not in method_names  # => persistence lives on the repository, not here


def test_repository_saves_and_retrieves_the_domain_object() -> None:
    repo: UserRepository = UserRepository()
    repo.save(User(user_id=1, email="ada@example.com"))
    found: User | None = repo.find_by_id(1)
    assert found == User(user_id=1, email="ada@example.com")


def test_repository_returns_none_for_an_unsaved_id() -> None:
    repo: UserRepository = UserRepository()
    assert repo.find_by_id(99) is None


# => Run: pytest -- Output: 3 passed
