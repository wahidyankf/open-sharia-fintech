# learning/code/ex-21-group-tests-in-class/test_example.py
"""Example 21: Group Tests in a Class."""


# ex-21: related tests grouped in a class -- pytest discovers Test* classes automatically (co-09)
class Adder:  # => the unit under test -- a tiny class, not itself a test class
    def add(self, a: int, b: int) -> int:  # => instance method under test
        return a + b  # => a plain, pure computation


class TestAdder:  # => MUST start with "Test" (capital T) for pytest to discover it (co-09)
    def setup_method(self) -> None:  # => pytest calls this before EACH test method in the class  # fmt: skip
        self.adder = Adder()  # => fresh Adder instance per test -- shared setup, isolated state  # fmt: skip

    def test_add_two_positive_numbers(self) -> None:  # => method name still needs the test_ prefix  # fmt: skip
        assert self.adder.add(2, 3) == 5  # => uses the instance setup_method just built

    def test_add_a_positive_and_a_negative(
        self,
    ) -> None:  # => a SECOND method in the same class
        assert self.adder.add(10, -4) == 6  # => a SECOND test, sharing setup_method's fresh instance  # fmt: skip

    def test_add_two_negative_numbers(
        self,
    ) -> None:  # => a THIRD method, same class, same setup
        assert self.adder.add(-3, -7) == -10  # => grouped alongside the other two -- one coherent unit  # fmt: skip
