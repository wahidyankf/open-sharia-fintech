"""Example 6: pytest verification for Refactor an Ostrich That Cannot Fly."""

from example import Bird, FlyingBird, Ostrich, Sparrow, make_flock_fly


def test_ostrich_has_no_fly_method_at_all() -> None:
    # => the mechanical guarantee that replaces "raise NotImplementedError"
    assert not hasattr(Ostrich, "fly")  # => fly() genuinely does not exist here
    assert not issubclass(Ostrich, FlyingBird)  # => Ostrich never claims flying capability
    assert issubclass(Ostrich, Bird)  # => Ostrich still shares the base bird attributes


def test_flock_of_flying_birds_never_raises() -> None:
    flock: list[FlyingBird] = [Sparrow("Jay"), Sparrow("Wren")]
    results: list[str] = make_flock_fly(flock)  # => no NotImplementedError is reachable through this type signature
    assert results == ["Jay flies", "Wren flies"]


# => Run: pytest -- Output: 2 passed
