"""Example 1: pytest verification for Clause as Data, Not a String."""

from example import ColumnRef


def test_node_stores_name_without_rendering() -> None:
    # => construction alone must not produce any SQL text
    node = ColumnRef(name="email")  # => a fresh node, unrendered
    assert node.name == "email"  # => raw data is exactly what was passed in
    assert node.render() == "email"  # => rendering is a pure, separate step


def test_node_is_immutable_value() -> None:
    # => two nodes built from equal data compare equal (frozen dataclass value semantics)
    a = ColumnRef(name="id")  # => first node
    b = ColumnRef(name="id")  # => second, independently constructed node
    assert a == b  # => value equality, not identity -- both hold "id"


# => Run: pytest -- Output: 2 passed
