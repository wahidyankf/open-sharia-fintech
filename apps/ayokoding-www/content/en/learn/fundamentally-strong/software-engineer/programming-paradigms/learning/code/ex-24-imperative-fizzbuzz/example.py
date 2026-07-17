"""Example 24: Imperative FizzBuzz."""


def fizzbuzz_imperative(upper: int) -> list[str]:  # => classic imperative: an accumulator loop
    output: list[str] = []  # => mutable box we build up one iteration at a time
    for n in range(1, upper + 1):  # => explicit iteration, step by step
        if n % 15 == 0:  # => explicit selection, checked in a specific order (15 before 3 or 5 alone)
            output.append("FizzBuzz")  # => explicit mutate-in-place append
        elif n % 3 == 0:  # => next branch, only reached if the first didn't match
            output.append("Fizz")  # => same mutate-in-place append, different literal
        elif n % 5 == 0:  # => next branch, only reached if neither prior branch matched
            output.append("Buzz")  # => same mutate-in-place append, different literal
        else:  # => final branch: no rule applied, use the number itself
            output.append(str(n))  # => str() needed -- append() expects a str, not an int
    return output  # => the fully built accumulator
    # => every value was decided by re-running the same if/elif/elif/else chain, once per number


result = fizzbuzz_imperative(20)  # => classic 1..20 range
print(result)  # => 1,2,Fizz,4,Buzz,Fizz,7,8,Fizz,Buzz,11,Fizz,13,14,FizzBuzz,16,17,Fizz,19,Buzz
# => Output: ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz', '16', '17', 'Fizz', '19', 'Buzz']
