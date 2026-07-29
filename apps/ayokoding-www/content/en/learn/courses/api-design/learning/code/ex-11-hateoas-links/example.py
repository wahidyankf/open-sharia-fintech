# pyright: strict
"""Example 11: HATEOAS -- Following Links Instead of Hardcoding URLs. (co-03, co-28)

The fourth uniform-interface sub-constraint (HATEOAS) says a response
carries links to its own next legal actions. A client that reads `_links`
instead of hardcoding `/orders/{id}/cancel` can follow the API wherever it
actually points -- co-28 names this specific mechanism.
"""

from dataclasses import dataclass, field  # => field: gives the links dict its own factory type


@dataclass  # => co-03/co-28: state PLUS the actions available from that state
class OrderResponse:  # => co-28: one resource, carrying its own hypermedia controls
    id: int  # => the order's own id
    status: str  # => the order's CURRENT state -- what actions are legal depends on this
    links: dict[str, str] = field(default_factory=dict[str, str])  # => the hypermedia controls


def get_order(order_id: int) -> OrderResponse:  # => GET /orders/{id}
    return OrderResponse(  # => a "pending" order can still be cancelled -- the link says so
        id=order_id,  # => echoes the requested id back
        status="pending",  # => co-28: this specific status is what makes "cancel" a legal action
        links={  # => co-28: the ONLY actions this order legally supports right now
            "self": f"/orders/{order_id}",  # => co-28: where THIS resource lives
            "cancel": f"/orders/{order_id}/cancel",  # => co-28: the one action legal from "pending"
        },  # => end of the links dict
    )  # => end of the OrderResponse construction


def cancel_via_link(order: OrderResponse) -> str:  # => a client that NEVER hardcodes the URL
    cancel_url = order.links["cancel"]  # => co-03: reads the action from the response itself
    # => cancel_url is "/orders/101/cancel" -- read from the response, never typed by the client
    return f"POST {cancel_url}"  # => the client followed the link, not a string it guessed


order = get_order(101)  # => fetch the order once
# => order.links is {'self': '/orders/101', 'cancel': '/orders/101/cancel'}
print(f"order: id={order.id}, status={order.status}, links={order.links}")  # => Output: both links shown

action = cancel_via_link(order)  # => the client discovers the cancel action FROM the response
print(f"client action: {action}")  # => Output: POST /orders/101/cancel -- discovered, not guessed
