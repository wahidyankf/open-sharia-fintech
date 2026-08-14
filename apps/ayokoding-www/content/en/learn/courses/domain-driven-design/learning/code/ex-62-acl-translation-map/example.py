"""Example 62: keep field mapping explicit and testable."""


def translate(record: dict[str, object]) -> dict[str, object]:
    return {
        "id": record["client_id"],
        "credit": int(record["credit_cents"]) // 100,
    }  # => translate names and units


sales = translate({"client_id": "c-1", "credit_cents": 2500})
assert sales == {"id": "c-1", "credit": 25}
