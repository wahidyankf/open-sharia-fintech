"""Kata 7 (after): the SAME invariant enforced by a property setter too."""


class Temperature:
    def __init__(self, celsius: float) -> None:
        self.celsius = (
            celsius  # routes through the property setter below, even in __init__
        )

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value


t = Temperature(20.0)
try:
    t.celsius = -300.0
except ValueError as exc:
    print(exc)
