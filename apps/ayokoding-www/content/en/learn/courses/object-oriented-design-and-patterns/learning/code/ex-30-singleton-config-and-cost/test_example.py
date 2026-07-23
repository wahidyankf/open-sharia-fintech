"""Example 30: pytest verification for A Config Singleton, and Its Cost."""

from example import Config


def test_instance_always_returns_the_same_object() -> None:
    Config.reset()  # => start from a known-clean state -- the cost this test proves
    assert Config.instance() is Config.instance()  # => two calls, one shared object


def test_mutation_leaks_across_every_reference_without_reset() -> None:
    Config.reset()  # => without this line, a PRIOR test's leftover state leaks in here
    a: Config = Config.instance()
    a.debug = True  # => mutate through one reference
    b: Config = Config.instance()
    assert b.debug is True  # => visible through a totally different reference -- the pain
    Config.reset()  # => clean up so later tests are not poisoned by this test's mutation


# => Run: pytest -- Output: 2 passed
