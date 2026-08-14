# => Keeps this domain step explicit and reviewable.
"""Example 62: keep field mapping explicit and testable."""


# => Names policy so callers do not recreate the rule.
def translate(record: dict[str, object]) -> dict[str, object]:
    # => Returns the domain result instead of leaking representation.
    return {
        # => Keeps this domain step explicit and reviewable.
        "id": record["client_id"],
        # => Keeps this domain step explicit and reviewable.
        "credit": int(record["credit_cents"]) // 100,
    }  # => translate names and units


# => Keeps scenario data close to the rule it exercises.
sales = translate({"client_id": "c-1", "credit_cents": 2500})
# => Proves the stated business rule is observable.
assert sales == {"id": "c-1", "credit": 25}
