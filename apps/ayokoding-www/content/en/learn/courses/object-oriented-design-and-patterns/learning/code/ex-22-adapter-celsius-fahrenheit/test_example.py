"""Example 22: pytest verification for Adapter: Fahrenheit Sensor to Celsius Interface."""

from example import CelsiusSensorAdapter, FahrenheitSensor, read_temperature


def test_adapter_converts_fahrenheit_to_celsius_correctly() -> None:
    legacy: FahrenheitSensor = FahrenheitSensor(98.6)
    adapted: CelsiusSensorAdapter = CelsiusSensorAdapter(legacy)
    assert round(adapted.get_celsius(), 1) == 37.0  # => the standard conversion, exact


def test_client_reads_celsius_through_the_adapter_only() -> None:
    adapted: CelsiusSensorAdapter = CelsiusSensorAdapter(FahrenheitSensor(32.0))
    result: float = read_temperature(adapted)  # => the client never calls get_fahrenheit()
    assert result == 0.0  # => freezing point, correctly translated


# => Run: pytest -- Output: 2 passed
