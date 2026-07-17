"""Example 73: Multi-Paradigm Request Handler."""

from dataclasses import dataclass, field  # => @dataclass generates Order's __init__; field() gives a fresh list


@dataclass  # => the OO domain model: an order with mutable, encapsulated state
class Order:  # => not frozen -- this domain model is intentionally mutable, unlike the pure core below
    order_id: str  # => the order's identifier
    items: list[str] = field(default_factory=list[str])  # => the ordered items
    status: str = "pending"  # => mutable OO state, changed ONLY through mark_shipped() below

    def mark_shipped(self) -> None:  # => the ONLY sanctioned way to change status
        self.status = "shipped"  # => the one mutation this whole example performs


def compute_summary(order: Order) -> str:  # => the FUNCTIONAL CORE: pure, no I/O, no mutation
    item_count = len(order.items)  # => reads only its argument
    return f"Order {order.order_id}: {item_count} item(s), status={order.status}"  # => a pure computation


class RequestRouter:  # => the EVENT-DRIVEN shell: framework-calls-you style routing
    def __init__(self) -> None:  # => constructor seeds the OO store and the request log
        self._orders: dict[str, Order] = {}  # => the OO domain store
        self.handled: list[str] = []  # => records every request this router actually processed

    def handle(self, event: str, order_id: str, items: list[str] | None = None) -> str:  # => one event in, one summary out
        self.handled.append(f"{event}:{order_id}")  # => event-driven: the router dispatches by event name
        if event == "create":  # => branch 1: construct a new mutable OO order
            self._orders[order_id] = Order(order_id, items or [])  # => the OO layer's own construction step
        elif event == "ship":  # => branch 2, only reached if "create" didn't match
            self._orders[order_id].mark_shipped()  # => an OO mutation, but ONLY reachable via the router
        summary = compute_summary(self._orders[order_id])  # => the functional core does the actual reporting
        return summary  # => the router's return value is entirely produced by the pure function above


router = RequestRouter()  # => construct the event-driven shell
create_result = router.handle("create", "ord-1", ["widget", "gadget"])  # => an incoming "event"
print(create_result)  # => the functional core's summary of the freshly created OO order
# => Output: Order ord-1: 2 item(s), status=pending

ship_result = router.handle("ship", "ord-1")  # => a second event, mutating the SAME OO object
print(ship_result)  # => status reflects the OO mutation, reported through the same pure function
# => Output: Order ord-1: 2 item(s), status=shipped
print(router.handled)  # => the event-driven shell recorded both requests, in order
# => Output: ['create:ord-1', 'ship:ord-1']
