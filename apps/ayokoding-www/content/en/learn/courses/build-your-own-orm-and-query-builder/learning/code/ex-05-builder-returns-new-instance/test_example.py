"""Example 5: pytest verification for Builder Returns a New Instance."""

import dataclasses

import pytest

from example import Query


def test_original_query_unchanged_after_where() -> None:
    base = Query(table="orders")  # => a fresh, filter-free query
    base.where("status = 'open'")  # => call .where() but DISCARD the return value
    assert base.wheres == ()  # => base is untouched -- the discarded call had no effect


def test_where_returns_a_different_object() -> None:
    base = Query(table="orders")  # => original
    branched = base.where("status = 'open'")  # => keep the returned object this time
    assert branched is not base  # => a genuinely new object, not base mutated in place
    assert branched.wheres == ("status = 'open'",)  # => the new object carries the filter


def test_frozen_dataclass_rejects_direct_mutation() -> None:
    query = Query(table="orders")  # => a frozen instance
    with pytest.raises(dataclasses.FrozenInstanceError):  # => attribute assignment must fail
        query.table = "users"  # type: ignore[misc]  # => deliberately illegal -- proves frozen=True


# => Run: pytest -- Output: 3 passed
