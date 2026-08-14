# => Keeps this domain step explicit and reviewable.
"""Example 27: predicates compose into a policy."""


# => Names policy so callers do not recreate the rule.
def premium(spend: int) -> bool:
    return spend >= 100  # => first business predicate


# => Names policy so callers do not recreate the rule.
def active(days: int) -> bool:
    return days <= 30  # => second business predicate


# => Names policy so callers do not recreate the rule.
def eligible(spend: int, days: int) -> bool:
    return premium(spend) and active(days)  # => logical AND


# => Proves the stated business rule is observable.
assert eligible(100, 1) and not eligible(100, 31)
print("composed")  # => Output: composed
