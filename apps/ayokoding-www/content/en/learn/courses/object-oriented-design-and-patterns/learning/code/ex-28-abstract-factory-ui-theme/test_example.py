"""Example 28: pytest verification for An Abstract Factory for UI Widget Families."""

from example import DarkThemeFactory, LightThemeFactory, build_toolbar


def test_dark_factory_produces_only_dark_family_products() -> None:
    button, checkbox = build_toolbar(DarkThemeFactory())
    assert button == "dark-button"  # => both products share the dark family
    assert checkbox == "dark-checkbox"  # => never mixed with the light family


def test_swapping_the_factory_swaps_the_whole_family() -> None:
    button, checkbox = build_toolbar(LightThemeFactory())
    assert (button, checkbox) == (
        "light-button",
        "light-checkbox",
    )  # => one swapped argument, whole family changed


# => Run: pytest -- Output: 2 passed
