# => Keeps this domain step explicit and reviewable.
"""Example 50: orchestration asks the domain to decide."""


# => Gives domain rules a single, named home.
class Order:
    # => Names policy so callers do not recreate the rule.
    def approve(self, credit: int) -> bool:
        return credit >= 10  # => business threshold stays in the model


# => Names policy so callers do not recreate the rule.
def application_service(order: Order, credit: int) -> bool:
    return order.approve(credit)  # => no duplicate business predicate appears here


# => Proves the stated business rule is observable.
assert application_service(Order(), 10)
