"""Example 68: pytest verification for Per-Instance Lazy Caching via __set_name__."""

from example import LazyAttribute


def test_two_instances_cache_independently() -> None:
    log: list[str] = []  # => records which loader ran

    def loader() -> str:  # => a shared loader, run once PER instance
        log.append("ran")  # => counts this run
        return "value"

    class Holder:
        field = LazyAttribute(loader)  # => one descriptor, shared at the class level

    first = Holder()  # => instance one
    second = Holder()  # => instance two, a SEPARATE private cache slot
    _ = first.field  # => triggers instance one's own load
    _ = second.field  # => triggers instance two's own load, independently
    assert log == ["ran", "ran"]  # => two independent loads, not one shared cache hit


def test_repeated_access_on_the_same_instance_loads_once() -> None:
    log: list[str] = []

    def loader() -> str:
        log.append("ran")
        return "value"

    class Holder:
        field = LazyAttribute(loader)

    instance = Holder()
    _ = instance.field  # => first access -- loads
    _ = instance.field  # => second access -- must be a cache hit
    assert len(log) == 1  # => exactly one load for this ONE instance


# => Run: pytest -- Output: 2 passed
