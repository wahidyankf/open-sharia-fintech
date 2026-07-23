# learning/code/ex-12-input-validation-at-the-boundary/orders_app.py
"""Example 12: Input Validation at the Boundary."""  # => co-07: module docstring

from __future__ import (
    annotations,
)  # => co-07: DD-39 hygiene, unrelated to the validation itself

from flask import (
    Flask,
    jsonify,
    request,
)  # => co-01: request.get_json() below is the tainted boundary
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
)  # => co-07: schema + the exception boundary validation raises

app = Flask(__name__)  # => co-07: a single throwaway app, self-contained per-run
business_logic_calls: list[
    object
] = []  # => co-07: a spy list -- proves whether business logic ever ran


class OrderRequest(
    BaseModel
):  # => co-07: the schema every request body must satisfy BEFORE handling
    sku: str = Field(
        min_length=3, max_length=20
    )  # => co-07: type AND length constraint, checked together
    quantity: int = Field(
        gt=0, le=1000
    )  # => co-07: type AND range constraint -- rejects negative or huge orders


@app.route(
    "/orders", methods=["POST"]
)  # => co-01: the boundary -- untrusted JSON crosses in here
def create_order() -> tuple[
    dict[str, object], int
]:  # => co-07: returns (body, status) -- Flask accepts this tuple
    """Validate the request body against OrderRequest BEFORE any business logic runs."""  # => co-07: doc
    try:  # => co-07: validation happens FIRST, wrapping the untrusted payload
        order = OrderRequest.model_validate(
            request.get_json(force=True)
        )  # => co-01: tainted JSON, validated here
    except (
        ValidationError
    ) as exc:  # => co-07: pydantic's own structured exception for a schema mismatch
        return jsonify(
            {"errors": exc.errors()}
        ), 422  # => co-07: 422 Unprocessable Entity -- structured, not a crash
    business_logic_calls.append(
        order
    )  # => co-07: reached ONLY when validation passed -- proves ordering
    return jsonify(
        {"sku": order.sku, "quantity": order.quantity}
    ), 201  # => co-07: 201 Created -- happy path


if (
    __name__ == "__main__"
):  # => co-07: entry point -- Flask's own test client, no real socket needed
    client = (
        app.test_client()
    )  # => co-07: an in-process client -- issues real Flask request/response cycles

    print(
        "=== Well-formed request ==="
    )  # => co-07: sanity check -- valid input passes through cleanly
    good = client.post(
        "/orders", json={"sku": "WIDGET-1", "quantity": 5}
    )  # => co-07: satisfies both constraints
    print(
        f"status={good.status_code} body={good.get_json()}"
    )  # => co-07: 201, echoes the validated order

    print(
        "\n=== Malformed request: sku too short, quantity negative ==="
    )  # => co-01: attacker-shaped payload
    bad = client.post(
        "/orders", json={"sku": "AB", "quantity": -5}
    )  # => co-01: violates BOTH field constraints
    print(
        f"status={bad.status_code} body={bad.get_json()}"
    )  # => co-07: 422, structured field-level errors

    print(
        f"\nbusiness_logic_calls after both requests: {len(business_logic_calls)}"
    )  # => co-07: still just 1
    assert (
        len(business_logic_calls) == 1
    )  # => co-07: mechanically proves the malformed request NEVER reached it
