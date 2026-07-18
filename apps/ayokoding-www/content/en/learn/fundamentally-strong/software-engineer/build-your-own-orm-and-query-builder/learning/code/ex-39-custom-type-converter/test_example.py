"""Example 39: pytest verification for a Custom JSON Type Converter."""

from example import coerce_on_load, coerce_on_store


def test_dict_round_trips_through_json_conversion() -> None:
    original = {"a": 1, "b": [1, 2, 3]}  # => a dict with a nested list value
    stored = coerce_on_store("json", original)  # => dict -> JSON text
    reloaded = coerce_on_load("json", stored)  # => JSON text -> dict
    assert reloaded == original  # => nothing lost across the round trip


def test_stored_form_is_a_plain_string() -> None:
    stored = coerce_on_store("json", {"x": True})  # => encode a small dict
    assert isinstance(stored, str)  # => driver-native TEXT form, ready to bind as a parameter


# => Run: pytest -- Output: 2 passed
