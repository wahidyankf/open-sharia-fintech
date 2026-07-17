"""Example 25: Declarative FizzBuzz."""

RULES: list[tuple[int, str]] = [  # => STATES the rules as data: (divisor, label) pairs, ordered by priority
    (15, "FizzBuzz"),  # => checked first -- the more specific rule
    (3, "Fizz"),  # => checked next
    (5, "Buzz"),  # => checked next
]  # => no imperative "if/elif" chain anywhere -- the priority order lives in the list itself


def label_for(n: int) -> str:  # => WHAT: "the first matching rule's label, or the number itself"
    return next((label for divisor, label in RULES if n % divisor == 0), str(n))  # => one expression
    # => next(..., default) reads as "the first rule that fits, falling back to str(n)"


def fizzbuzz_declarative(upper: int) -> list[str]:  # => mapped over the range, no accumulator variable
    return [label_for(n) for n in range(1, upper + 1)]  # => "the label for every n in the range"


# => the imperative example (24) computed this exact literal via its accumulator loop -- repeated
# => here so this example's Output block is self-contained and independently diffable against it, and
# => byte-identical to fizzbuzz_imperative(20)'s result in example 24
imperative_reference: list[str] = ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz", "16", "17", "Fizz", "19", "Buzz"]

declarative_result = fizzbuzz_declarative(20)  # => same 1..20 range as example 24
print(declarative_result)  # => must be byte-identical to the imperative version's output
# => Output: ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz', '16', '17', 'Fizz', '19', 'Buzz']
print(declarative_result == imperative_reference)  # => confirms both styles agree, value for value
# => Output: True
