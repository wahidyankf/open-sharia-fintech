"""Example 49: pytest verification for Multi-Paradigm Boundary."""

from example import InventoryService, functional_pipeline


def test_boundary_passes_only_immutable_data() -> None:
    cleaned = functional_pipeline((100, 50, 5, 200))  # => run the pure side
    assert isinstance(cleaned, tuple)  # => the boundary value itself is immutable

    service = InventoryService(accepted_prices=[])  # => fresh OO service
    service.record_batch(cleaned)  # => cross the boundary
    assert service.accepted_prices == [90, 45, 5, 180]  # => the OO side received the pipeline's output
    assert cleaned == (90, 45, 5, 180)  # => and the tuple itself is provably unchanged after crossing


def test_functional_side_never_mutates_its_own_input_tuple() -> None:
    raw = (10, 20)  # => a small immutable input
    functional_pipeline(raw)  # => call once, discard the result -- only checking for mutation
    assert raw == (10, 20)  # => tuples cannot be mutated in place at all, but this documents the contract


# => Run: pytest -- Output: 2 passed
