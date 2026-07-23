"""Example 9: pytest verification for Invert a Service to Depend on a Repository Protocol."""

from typing import get_type_hints

from example import InMemoryRepository, Repository, UserService


def test_constructor_is_typed_against_the_protocol() -> None:
    hints: dict[str, object] = get_type_hints(UserService.__init__)  # => reads the actual annotation UserService.__init__ declares
    assert hints["repository"] is Repository  # => the abstraction, not the concrete class


def test_service_still_works_with_an_injected_repository() -> None:
    service: UserService = UserService(InMemoryRepository())  # => injected at the boundary
    assert service.greet(1) == "Hi, Alice"
    assert service.greet(2) == "Hi, Bob"  # => any Repository-shaped object would work here


# => Run: pytest -- Output: 2 passed
