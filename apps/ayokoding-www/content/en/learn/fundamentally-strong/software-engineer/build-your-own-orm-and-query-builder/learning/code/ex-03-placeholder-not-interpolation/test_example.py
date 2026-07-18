"""Example 3: pytest verification for Bind a Value as a Placeholder."""

from example import Param


def test_render_emits_placeholder_text_only() -> None:
    param = Param(value=42)  # => an ordinary integer literal
    sql_fragment, bound = param.render()  # => splits into text + params
    assert sql_fragment == "?"  # => text is always exactly "?", regardless of value
    assert bound == [42]  # => value travels only in the params list


def test_hostile_string_never_becomes_sql_text() -> None:
    hostile = "x'); DROP TABLE users;--"  # => a classic injection payload
    param = Param(value=hostile)  # => wrapped as a param, not concatenated
    sql_fragment, bound = param.render()  # => splits into text + params
    assert hostile not in sql_fragment  # => the payload never touches the SQL string
    assert bound == [hostile]  # => the payload is confined to the params list


# => Run: pytest -- Output: 2 passed
