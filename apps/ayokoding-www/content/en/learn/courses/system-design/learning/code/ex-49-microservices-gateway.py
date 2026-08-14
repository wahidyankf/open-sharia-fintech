def catalog(product_id: str) -> dict[str, str]:
    # This service owns product display data.
    return {"id": product_id, "name": "Book"}


def inventory(product_id: str) -> dict[str, bool]:
    # This service owns availability and exposes only that contract.
    return {"in_stock": product_id == "book"}


def gateway(product_id: str) -> dict[str, object]:
    # The gateway composes two calls behind one client-facing endpoint.
    return {"product": catalog(product_id), "inventory": inventory(product_id)}


result = gateway("book")
# One client call contains outputs from two independently owned services.
assert result["product"]["name"] == "Book" and result["inventory"]["in_stock"] is True
print(result)
