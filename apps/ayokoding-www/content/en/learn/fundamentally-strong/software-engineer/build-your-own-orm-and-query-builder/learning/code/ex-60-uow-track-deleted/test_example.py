"""Example 60: pytest verification for UnitOfWork.register_deleted."""

from example import UnitOfWork, User


def test_registering_a_deleted_object_adds_it_to_deleted_objects() -> None:
    uow = UnitOfWork()  # => a fresh unit of work
    user = User(id=1, name="Grace")  # => already-persisted object
    uow.register_deleted(user)  # => tracked as deleted
    assert uow.deleted_objects == [user]  # => exactly one, and it is this object


def test_registering_two_deletions_tracks_both_in_order() -> None:
    uow = UnitOfWork()
    first = User(id=1, name="A")  # => registered first
    second = User(id=2, name="B")  # => registered second
    uow.register_deleted(first)
    uow.register_deleted(second)
    assert uow.deleted_objects == [first, second]  # => insertion order preserved


# => Run: pytest -- Output: 2 passed
