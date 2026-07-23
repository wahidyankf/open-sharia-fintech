"""Example 67: pytest verification for Lazy-Loading Descriptor Deferral."""

from example import LazyAttribute


def test_loader_does_not_run_before_first_access() -> None:
    calls: list[int] = []  # => records every time the loader actually runs, explicitly typed

    def loader() -> str:  # => a named loader -- makes the counted side effect explicit and typed
        calls.append(1)  # => counts THIS run
        return "value"  # => the value LazyAttribute eventually returns

    class Holder:  # => a minimal class to attach the descriptor to
        field = LazyAttribute(loader)  # => a fresh, unaccessed descriptor

    Holder()  # => construction alone must NOT trigger the loader
    assert calls == []  # => confirmed -- nothing ran yet


def test_first_access_runs_the_loader_exactly_once() -> None:
    calls: list[int] = []  # => a second, independent counter for this test

    def loader() -> str:  # => a second named loader, same shape as above
        calls.append(1)  # => counts THIS run
        return "value"  # => the value LazyAttribute eventually returns

    class Holder:
        field = LazyAttribute(loader)  # => a fresh, unaccessed descriptor for THIS test

    instance = Holder()
    _ = instance.field  # => first access -- triggers the loader
    _ = instance.field  # => second access -- must NOT trigger it again
    assert len(calls) == 1  # => exactly one run, despite two accesses


# => Run: pytest -- Output: 2 passed
