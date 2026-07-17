"""Example 32: pytest verification for A Virtual Proxy Defers an Expensive Load."""

from example import ImageProxy, RealImage


def test_constructing_the_proxy_loads_nothing() -> None:
    before: int = RealImage.load_count
    ImageProxy("unit-test.png")  # => constructing the proxy itself must stay cheap
    assert RealImage.load_count == before  # => no RealImage was constructed yet


def test_first_render_call_loads_exactly_once() -> None:
    before: int = RealImage.load_count
    proxy: ImageProxy = ImageProxy("unit-test-2.png")
    proxy.render()  # => triggers the one and only load
    proxy.render()  # => must NOT trigger a second load
    proxy.render()  # => must NOT trigger a third load
    assert RealImage.load_count == before + 1  # => loaded exactly once across 3 calls


# => Run: pytest -- Output: 2 passed
