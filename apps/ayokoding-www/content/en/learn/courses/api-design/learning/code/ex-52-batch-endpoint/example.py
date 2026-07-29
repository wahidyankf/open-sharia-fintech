# pyright: strict
"""Example 52: POST /batch -- N Sub-Operations, One Request. (co-32)

A batch endpoint applies N distinct sub-operations in one HTTP round trip,
dispatching each to its own handler and returning an array of INDIVIDUAL
sub-results -- one sub-operation failing does not fail the others.
"""

from typing import Any, Callable  # => a handler is just a function, typed for clarity

STORE: dict[int, str] = {1: "Existing article"}  # => the resource store the batch operates against


def handle_get(article_id: int) -> dict[str, Any]:  # => one possible sub-operation
    if article_id not in STORE:  # => this specific sub-op can fail on its own
        return {"status": 404, "body": {"error": "not found"}}  # => 404, but only for THIS sub-op
    return {"status": 200, "body": {"id": article_id, "title": STORE[article_id]}}  # => 200, found


HANDLERS: dict[str, Callable[[int], dict[str, Any]]] = {"get": handle_get}  # => co-32: op name -> handler


def run_batch(operations: list[dict[str, Any]]) -> list[dict[str, Any]]:  # => POST /batch
    results: list[dict[str, Any]] = []  # => co-32: one sub-result per sub-operation, in order
    for op in operations:  # => co-32: dispatches EACH sub-operation independently
        handler = HANDLERS[op["method"]]  # => co-32: looks up the right handler for this sub-op
        results.append(handler(op["article_id"]))  # => co-32: a failure here does not stop the loop
    return results  # => the full array of individual sub-results


batch_request = [  # => co-32: three sub-operations, one of which targets a missing resource
    {"method": "get", "article_id": 1},  # => sub-op 1: found
    {"method": "get", "article_id": 999},  # => sub-op 2: NOT found -- fails independently
    {"method": "get", "article_id": 1},  # => sub-op 3: found, unaffected by sub-op 2's failure
]
results = run_batch(batch_request)  # => co-32: runs all three in one call
# => results has 3 entries: status 200, 404, 200 -- one failure did not abort the batch
for i, result in enumerate(results, start=1):  # => print each sub-result on its own line
    print(f"sub-op {i}: {result}")  # => Output: 200, 404, 200 -- each independent
