# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 29: distinguish a module's public API from internals."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
PUBLIC_ORDERS_API = {"place_order", "get_order"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
requested_name = "_repository"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert requested_name not in PUBLIC_ORDERS_API
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print("internal dependency rejected")
