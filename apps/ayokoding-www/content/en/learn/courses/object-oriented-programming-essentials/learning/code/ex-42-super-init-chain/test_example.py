"""Example 42: pytest verification for Chaining Construction with super().__init__()."""

from example import Cat


def test_super_init_sets_base_and_subclass_fields() -> None:
    c: Cat = Cat("Whiskers", indoor=True)
    assert c.name == "Whiskers"  # => set by Animal.__init__ via super()
    assert c.indoor is True  # => set by Cat.__init__ itself, after the super() call


# => Run: pytest -- Output: 1 passed
