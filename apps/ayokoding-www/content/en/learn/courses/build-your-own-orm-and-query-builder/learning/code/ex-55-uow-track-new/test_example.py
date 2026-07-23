"""Example 55: pytest verification for UnitOfWork.register_new."""

from example import UnitOfWork, User


def test_registering_a_new_object_adds_it_to_new_objects() -> None:
    uow = UnitOfWork()  # => a fresh unit of work
    user = User(id=None, name="Grace")  # => not yet persisted
    uow.register_new(user)  # => tracked as new
    assert uow.new_objects == [user]  # => exactly one, and it is this object


def test_registering_two_objects_tracks_both_in_order() -> None:
    uow = UnitOfWork()
    first = User(id=None, name="A")  # => registered first
    second = User(id=None, name="B")  # => registered second
    uow.register_new(first)
    uow.register_new(second)
    assert uow.new_objects == [first, second]  # => insertion order preserved


# => Run: pytest -- Output: 2 passed
