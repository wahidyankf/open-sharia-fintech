"""Example 50: orchestration asks the domain to decide."""


class Order:
    def approve(self, credit: int) -> bool:
        return credit >= 10  # => business threshold stays in the model


def application_service(order: Order, credit: int) -> bool:
    return order.approve(credit)  # => no duplicate business predicate appears here


assert application_service(Order(), 10)
