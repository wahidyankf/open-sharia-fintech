"""Example 19: Name Mangling with a Double-Underscore Attribute."""


class SecureBox:  # => begins the SecureBox class body
    def __init__(
        self, pin: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.__pin: str = pin  # => double leading underscore triggers NAME MANGLING

    def check_pin(
        self, guess: str
    ) -> bool:  # => the sanctioned way to compare against __pin
        return guess == self.__pin  # => inside the class, __pin still reads normally


box: SecureBox = SecureBox("1234")  # => constructs box
print(box.check_pin("1234"))  # => internal access works exactly as written
# => Output: True
print(box._SecureBox__pin)  # type: ignore  # => the MANGLED name Python actually stores it under (static checkers cannot resolve this literal spelling)
# => Output: 1234
# => `self.__pin` inside a class is rewritten by Python itself to `self._ClassName__pin` at parse time
