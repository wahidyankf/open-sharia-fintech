"""Example 19: pytest verification for Simple Factory: Centralize Parser Construction."""

import pytest  # => pytest.raises asserts a specific exception is raised

from example import Parser, ParserFactory


def test_known_extensions_build_the_right_parser() -> None:
    csv_parser: Parser = ParserFactory.create("csv")
    assert csv_parser.parse("a,b,c") == ["a", "b", "c"]
    json_parser: Parser = ParserFactory.create("json")
    assert json_parser.parse('["x", "y"]') == ["x", "y"]  # => a different parser entirely


def test_unknown_extension_raises_a_clean_value_error() -> None:
    # => the test PASSES only because ValueError fires with a specific, readable message
    with pytest.raises(ValueError, match="unknown extension"):
        ParserFactory.create("xml")  # => an extension the factory does not recognize


# => Run: pytest -- Output: 2 passed
