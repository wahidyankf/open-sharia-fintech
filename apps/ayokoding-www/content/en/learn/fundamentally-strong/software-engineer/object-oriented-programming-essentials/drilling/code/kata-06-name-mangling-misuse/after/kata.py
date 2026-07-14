"""Kata 6 (after): use the class's own sanctioned accessor instead of poking at __pin."""


class Wallet:
    def __init__(self, pin: str) -> None:
        self.__pin = pin

    def check_pin(self, guess: str) -> bool:
        return guess == self.__pin


w = Wallet("1234")
print(w.check_pin("1234"))
