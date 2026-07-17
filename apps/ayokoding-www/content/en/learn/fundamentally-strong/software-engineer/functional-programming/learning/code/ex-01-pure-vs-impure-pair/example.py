"""Example 1: Pure vs. Impure -- Same Result Every Time."""

counter_total = 0  # => module-level global state -- the impure twin's playground


def add_pure(a: int, b: int) -> int:  # => pure: output depends ONLY on a and b
    return a + b  # => no write to anything outside this function -- no side effect


def add_impure(a: int, b: int) -> int:  # => same signature, very different behavior
    global counter_total  # => declares intent to MUTATE module-level state
    counter_total += a + b  # => side effect: writes state outside this function's scope
    # => the return value now depends on how many times this ran BEFORE, not just a, b
    return counter_total


first_pure = add_pure(2, 3)  # => first_pure is 5
second_pure = add_pure(2, 3)  # => second_pure is 5 -- SAME args, SAME result
print(
    first_pure == second_pure
)  # => True: repeat calls with identical args always agree
# => Output: True

first_impure = add_impure(
    2, 3
)  # => first_impure is 5 (counter_total was 0 before this)
second_impure = add_impure(
    2, 3
)  # => second_impure is 10 -- SAME args, DIFFERENT result!
print(first_impure == second_impure)  # => False: hidden global state changed the answer
# => Output: False
