"""Example 24: if/elif/else."""


def classify(n: int) -> str:  # => defines classify, takes an int, returns a str
    # Exactly one branch below runs per call -- elif/else are mutually exclusive.
    if n < 0:  # => checked first -- only one branch below ever runs
        return "negative"  # => returns immediately, skipping elif/else
    elif n == 0:  # => checked only if the first condition was False
        return "zero"  # => returns immediately, skipping else
    else:  # => catches everything else -- every positive n
        return "positive"  # => runs only when both prior conditions were False


for value in (-2, 0, 5):  # => exercises all three branches in one pass
    print(classify(value))  # => Output: negative, then zero, then positive
