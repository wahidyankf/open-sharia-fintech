"""Example 71: writes and reads optimise for different responsibilities."""


class Order:
    def __init__(self) -> None:
        self.status = "draft"

    def place(self) -> None:
        self.status = "placed"  # => writes protect the aggregate rule


read_model = {
    "o-1": {"status": "placed", "total": 25}
}  # => reads use a query-shaped projection

order = Order()
order.place()
assert read_model["o-1"]["total"] == 25 and order.status == "placed"
