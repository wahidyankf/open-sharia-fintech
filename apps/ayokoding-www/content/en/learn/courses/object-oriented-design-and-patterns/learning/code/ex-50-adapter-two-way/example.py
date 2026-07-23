"""Example 50: A Two-Way Adapter Bridging Legacy and New Temperature APIs."""


class LegacyThermometer:  # => the OLD interface -- reports Fahrenheit, cannot be changed
    def __init__(self, fahrenheit: float) -> None:  # => the constructor
        self.fahrenheit = fahrenheit  # => stores fahrenheit on this instance

    def get_fahrenheit(self) -> float:  # => defines the get_fahrenheit() method
        return self.fahrenheit  # => returns this value to the caller


class NewThermometer:  # => the NEW interface -- reports Celsius, cannot be changed either
    def __init__(self, celsius: float) -> None:  # => the constructor
        self.celsius = celsius  # => stores celsius on this instance

    def get_celsius(self) -> float:  # => defines the get_celsius() method
        return self.celsius  # => returns this value to the caller


class TemperatureAdapter:  # => bridges BOTH directions -- neither original class was touched
    def __init__(self, legacy: LegacyThermometer | None = None, new: NewThermometer | None = None) -> None:  # => accepts EITHER side, wraps whichever one is provided
        self._legacy = legacy  # => stores legacy on this instance
        self._new = new  # => stores new on this instance

    def get_celsius(self) -> float:  # => the NEW-style method, works even when wrapping LEGACY
        if self._new is not None:  # => already Celsius -- pass it straight through
            return self._new.get_celsius()  # => returns this value to the caller
        assert self._legacy is not None  # => one of the two must always be set
        return (self._legacy.get_fahrenheit() - 32) * 5 / 9  # => converts F -> C on the fly

    def get_fahrenheit(self) -> float:  # => the LEGACY-style method, works even when wrapping NEW
        if self._legacy is not None:  # => already Fahrenheit -- pass it straight through
            return self._legacy.get_fahrenheit()  # => returns this value to the caller
        assert self._new is not None  # => one of the two must always be set
        return self._new.get_celsius() * 9 / 5 + 32  # => converts C -> F on the fly


legacy_to_new: TemperatureAdapter = TemperatureAdapter(legacy=LegacyThermometer(98.6))  # => wraps a LEGACY sensor for NEW-style callers
print(round(legacy_to_new.get_celsius(), 1))  # => the NEW-style method works on legacy data
# => Output: 37.0

new_to_legacy: TemperatureAdapter = TemperatureAdapter(new=NewThermometer(20.0))  # => wraps a NEW sensor for LEGACY-style callers
print(round(new_to_legacy.get_fahrenheit(), 1))  # => the LEGACY-style method works on new data
# => Output: 68.0
# => One adapter class satisfies BOTH APIs -- neither LegacyThermometer nor NewThermometer needed editing
