"""Example 50: pytest verification for the Two-Way Temperature Adapter."""

from example import LegacyThermometer, NewThermometer, TemperatureAdapter


def test_legacy_wrapped_adapter_reports_celsius_via_the_new_interface() -> None:
    adapter: TemperatureAdapter = TemperatureAdapter(legacy=LegacyThermometer(98.6))
    assert round(adapter.get_celsius(), 1) == 37.0  # => 98.6F converted to C


def test_new_wrapped_adapter_reports_fahrenheit_via_the_legacy_interface() -> None:
    adapter: TemperatureAdapter = TemperatureAdapter(new=NewThermometer(20.0))
    assert round(adapter.get_fahrenheit(), 1) == 68.0  # => 20C converted to F


# => Run: pytest -- Output: 2 passed
