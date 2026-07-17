"""Kata 7 (after): Tell, Don't Ask -- Customer owns the null-check, callers never reach through it."""


class Address:
    def __init__(self, city: str) -> None:
        self.city = city


class Customer:
    def __init__(self, address: "Address | None") -> None:
        self.address = address

    def shipping_city(self) -> str:  # => co-15: the customer TELLS its own city, callers never ASK through address
        if self.address is None:
            return "unknown"
        return self.address.city.upper()


def shipping_label(customer: Customer) -> str:
    return customer.shipping_city()  # => ONE hop, delegated -- no train wreck, no crash


customer = Customer(address=None)
print(shipping_label(customer))
