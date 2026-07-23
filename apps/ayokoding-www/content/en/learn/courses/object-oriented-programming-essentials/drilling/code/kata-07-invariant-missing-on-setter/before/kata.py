"""Kata 7 (before): invariant checked in __init__ but NOT on later mutation."""


class Temperature:
    def __init__(self, celsius: float) -> None:
        if celsius < -273.15:
            raise ValueError("below absolute zero")
        self.celsius = celsius


t = Temperature(20.0)
t.celsius = -300.0  # bypasses the constructor's guard entirely
print(t.celsius)
