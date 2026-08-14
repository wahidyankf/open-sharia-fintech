# => Isolate the operation so its observable behavior can be checked.
def catalog(product_id: str) -> dict[str, str]:
    # This service owns product display data.
    # => Return the observable result of this modeled operation.
    return {"id": product_id, "name": "Book"}


# => Isolate the operation so its observable behavior can be checked.
def inventory(product_id: str) -> dict[str, bool]:
    # This service owns availability and exposes only that contract.
    # => Return the observable result of this modeled operation.
    return {"in_stock": product_id == "book"}


# => Isolate the operation so its observable behavior can be checked.
def gateway(product_id: str) -> dict[str, object]:
    # The gateway composes two calls behind one client-facing endpoint.
    # => Return the observable result of this modeled operation.
    return {"product": catalog(product_id), "inventory": inventory(product_id)}


# => Initialize or update deterministic state used by this demonstration.
result = gateway("book")
# One client call contains outputs from two independently owned services.
# => Check the promised observable behavior of the demonstration.
assert result["product"]["name"] == "Book" and result["inventory"]["in_stock"] is True
# => Emit the final observable state for a direct run.
print(result)
