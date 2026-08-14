# => Keeps this domain step explicit and reviewable.
"""Example 79: a composite discount policy reads as a business sentence."""


# => Names policy so callers do not recreate the rule.
def eligible(loyal: bool, large_order: bool, delinquent: bool) -> bool:
    # => Returns the domain result instead of leaking representation.
    return (
        # => Keeps this domain step explicit and reviewable.
        loyal and large_order and not delinquent
    )  # => AND and NOT compose the three named rules


# => Proves the stated business rule is observable.
assert eligible(True, True, False) and not eligible(True, True, True)
print("policy evaluated")  # => Output: policy evaluated
