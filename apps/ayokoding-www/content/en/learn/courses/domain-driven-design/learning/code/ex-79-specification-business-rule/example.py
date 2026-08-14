"""Example 79: a composite discount policy reads as a business sentence."""


def eligible(loyal: bool, large_order: bool, delinquent: bool) -> bool:
    return (
        loyal and large_order and not delinquent
    )  # => AND and NOT compose the three named rules


assert eligible(True, True, False) and not eligible(True, True, True)
print("policy evaluated")  # => Output: policy evaluated
