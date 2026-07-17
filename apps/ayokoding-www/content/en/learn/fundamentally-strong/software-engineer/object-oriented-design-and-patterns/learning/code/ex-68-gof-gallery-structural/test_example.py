"""Example 68: pytest verification that each structural pattern wraps correctly."""

from example import (
    CelsiusAdapter,
    CheckoutFacade,
    DirectoryNode,
    FahrenheitSensor,
    FileNode,
    LazyImageProxy,
    greet,
)


def test_adapter_converts_fahrenheit_to_celsius() -> None:
    adapter = CelsiusAdapter(FahrenheitSensor())
    assert round(adapter.read_celsius(), 1) == 37.0  # => the client reads Celsius only


def test_decorator_wraps_the_function_without_editing_it() -> None:
    assert greet("Ada") == "[logged] hello, Ada"  # => logging added purely by wrapping


def test_facade_hides_subsystem_sequencing_behind_one_call() -> None:
    facade = CheckoutFacade()
    assert facade.checkout("Book", 12.5) is True  # => one call, inventory + payment both succeeded


def test_composite_computes_a_recursive_total_via_one_interface() -> None:
    tree = DirectoryNode([FileNode(10), DirectoryNode([FileNode(5), FileNode(3)])])
    assert tree.total_size() == 18  # => leaf and composite share total_size()


def test_proxy_defers_loading_until_first_access() -> None:
    proxy = LazyImageProxy("photo.png")
    assert proxy._real is None  # => not loaded yet
    proxy.display()  # => triggers the load
    assert proxy._real is not None  # => loaded exactly once, on first access


# => Run: pytest -q -- Output: 5 passed
