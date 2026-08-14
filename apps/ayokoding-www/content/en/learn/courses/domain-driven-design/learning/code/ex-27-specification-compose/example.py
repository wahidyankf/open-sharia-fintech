"""Example 27: predicates compose into a policy."""


def premium(spend: int) -> bool:
    return spend >= 100  # => first business predicate


def active(days: int) -> bool:
    return days <= 30  # => second business predicate


def eligible(spend: int, days: int) -> bool:
    return premium(spend) and active(days)  # => logical AND


assert eligible(100, 1) and not eligible(100, 31)
print("composed")  # => Output: composed
