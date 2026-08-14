"""Worked Example 29: distinguish a module's public API from internals."""

PUBLIC_ORDERS_API = {"place_order", "get_order"}
requested_name = "_repository"
assert requested_name not in PUBLIC_ORDERS_API
print("internal dependency rejected")
