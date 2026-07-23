"""Example 22: Adapter: Fahrenheit Sensor to Celsius Interface."""


class FahrenheitSensor:  # => the LEGACY interface -- reports only in Fahrenheit
    def __init__(self, reading_f: float) -> None:  # => the constructor
        self.reading_f = reading_f  # => stores the raw Fahrenheit reading

    def get_fahrenheit(self) -> float:  # => the ONLY method this legacy sensor offers
        return self.reading_f  # => returns the value exactly as read


class CelsiusSensorAdapter:  # => the ADAPTER -- wraps Fahrenheit, exposes Celsius
    def __init__(self, sensor: FahrenheitSensor) -> None:  # => the constructor
        self._sensor = sensor  # => holds the incompatible legacy object internally
        # => neither FahrenheitSensor nor the client below was ever modified

    def get_celsius(self) -> float:  # => the interface the CLIENT actually wants
        fahrenheit: float = self._sensor.get_fahrenheit()  # => delegates to the legacy call
        return (fahrenheit - 32) * 5 / 9  # => the conversion formula, isolated here


def read_temperature(sensor: CelsiusSensorAdapter) -> float:  # => the CLIENT, expects Celsius
    return sensor.get_celsius()  # => never calls get_fahrenheit() at all


legacy: FahrenheitSensor = FahrenheitSensor(98.6)  # => an incompatible legacy sensor
adapted: CelsiusSensorAdapter = CelsiusSensorAdapter(legacy)  # => wraps the legacy object to match what the client expects

print(round(read_temperature(adapted), 1))  # => the client reads Celsius, transparently
# => Output: 37.0
# => `CelsiusSensorAdapter` translates one interface into another -- neither side was rewritten
