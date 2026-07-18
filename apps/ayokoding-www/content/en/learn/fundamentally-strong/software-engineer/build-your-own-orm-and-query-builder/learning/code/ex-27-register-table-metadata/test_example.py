"""Example 27: pytest verification for Register Table Metadata."""

from example import Column, TableMeta, register_table, registry


def test_registered_table_returns_its_column_list() -> None:
    # => a fresh table registered under a different name than the module-level example
    meta = TableMeta(name="orders", columns=(Column(name="id"), Column(name="total")), primary_key="id")
    register_table(meta)  # => writes into the SAME shared registry dict
    assert [c.name for c in registry["orders"].columns] == ["id", "total"]  # => order preserved


def test_registering_same_name_twice_overwrites() -> None:
    first = TableMeta(name="tags", columns=(Column(name="id"),), primary_key="id")
    second = TableMeta(name="tags", columns=(Column(name="id"), Column(name="label")), primary_key="id")
    register_table(first)  # => first registration
    register_table(second)  # => re-registration under the same name
    assert registry["tags"] is second  # => the registry holds the LATEST registration, not the first


# => Run: pytest -- Output: 2 passed
