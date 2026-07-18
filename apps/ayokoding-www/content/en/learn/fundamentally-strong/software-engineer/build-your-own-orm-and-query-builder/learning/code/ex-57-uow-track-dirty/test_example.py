"""Example 57: pytest verification for Dirty Detection via Snapshot Comparison."""

from example import UnitOfWork, User


def test_untouched_object_is_not_dirty() -> None:
    uow = UnitOfWork()  # => a fresh unit of work
    user = User(id=1, name="Grace")  # => already-persisted object
    uow.track_clean(user)  # => snapshot taken
    assert uow.dirty_objects() == []  # => no mutation -- nothing dirty


def test_mutated_object_appears_in_dirty_objects() -> None:
    uow = UnitOfWork()
    user = User(id=2, name="Bob")
    uow.track_clean(user)
    user.name = "Bobby"  # => mutation AFTER tracking
    assert uow.dirty_objects() == [user]  # => detected as dirty


# => Run: pytest -- Output: 2 passed
