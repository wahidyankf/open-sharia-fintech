"""Example 67: pytest verification that each creational pattern constructs correctly."""

import pytest

from example import AppConfig, Circle, DarkWidgetFactory, RequestBuilder, shape_factory


def test_factory_method_constructs_the_correct_concrete_type() -> None:
    shape = shape_factory("circle", 2.0)  # => caller never named Circle directly
    assert isinstance(shape, Circle)  # => yet the correct concrete type was constructed
    with pytest.raises(ValueError):
        shape_factory("hexagon", 1.0)  # => an unknown kind is rejected cleanly


def test_abstract_factory_produces_a_matched_family() -> None:
    factory = DarkWidgetFactory()
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    assert button.theme == checkbox.theme == "dark"  # => both members of the family share one theme


def test_builder_assembles_a_request_without_a_telescoping_constructor() -> None:
    request = RequestBuilder("https://api.example.com").with_header("Accept", "json").with_body("{}").build()
    assert request.url == "https://api.example.com"  # => the required part
    assert request.headers == {"Accept": "json"}  # => an optional part, included
    assert request.body == "{}"  # => another optional part, included


def test_singleton_returns_the_same_instance_every_time() -> None:
    assert AppConfig() is AppConfig()  # => two calls, one object


# => Run: pytest -q -- Output: 4 passed
