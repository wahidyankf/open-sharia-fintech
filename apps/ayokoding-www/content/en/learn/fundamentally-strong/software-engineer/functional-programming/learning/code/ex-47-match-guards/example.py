"""Example 47: case Clauses With if Guards."""


def classify(n: int) -> str:  # => match/case WITH guards -- a pattern PLUS a condition
    match n:  # => opens the match/case block over n
        case int(value) if value < 0:  # => guard: only matches negative ints
            return "negative"  # => the negative branch's result
        case 0:  # => an exact-value pattern, no guard needed
            return "zero"  # => the zero branch's result
        case int(value) if value % 2 == 0:  # => guard: only matches even positive ints
            return "positive even"  # => the positive-even branch's result
        case _:  # => catches everything else -- positive odd ints
            return "positive odd"  # => the positive-odd branch's result


# => guards let one case pattern cover many related conditions
print(classify(-5))  # => Output: negative
print(classify(0))  # => Output: zero
print(classify(4))  # => Output: positive even
print(classify(7))  # => Output: positive odd
