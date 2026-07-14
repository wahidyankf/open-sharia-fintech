"""Kata 6 (before): reaching for a double-underscore attribute by its unmangled name."""


class Wallet:
    def __init__(self, pin: str) -> None:
        self.__pin = pin


w = Wallet("1234")
print(w.__pin)  # type: ignore
