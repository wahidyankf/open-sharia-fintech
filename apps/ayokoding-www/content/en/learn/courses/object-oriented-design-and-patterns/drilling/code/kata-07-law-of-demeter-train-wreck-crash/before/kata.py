"""Kata 7 (before): Law of Demeter violation -- a train wreck crashes when an intermediate link is missing."""


class Address:
    def __init__(self, city: str) -> None:
        self.city = city


class Customer:
    def __init__(self, address: "Address | None") -> None:
        self.address = address  # optional -- some customers have no address on file yet


def shipping_label(customer: Customer) -> str:
    return customer.address.city.upper()  # type: ignore[union-attr]  # SMELL: reaches through TWO links, assumes address is never None


customer = Customer(address=None)
try:
    print(shipping_label(customer))
except AttributeError as error:
    print(f"crashed: {error}")
