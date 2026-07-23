"""Example 2: Referential Transparency by Substitution."""


def add(a: int, b: int) -> int:  # => a pure function -- referentially transparent
    return a + b  # => always returns the same value for the same a, b


def price_with_call() -> int:  # => uses the CALL add(2, 3) inside a larger expression
    return add(2, 3) * 10  # => add(2, 3) is evaluated, then multiplied by 10


def price_with_value() -> int:  # => the call REPLACED by its own return value, 5
    return 5 * 10  # => substituting add(2, 3) -> 5 changes nothing about the result


call_result = price_with_call()  # => call_result is 50
value_result = price_with_value()  # => value_result is 50 -- IDENTICAL to call_result
print(
    call_result == value_result
)  # => True: the call was safely replaceable by its value
# => Output: True
