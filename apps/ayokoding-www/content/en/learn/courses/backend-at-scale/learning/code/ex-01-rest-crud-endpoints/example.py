# pyright: strict
"""Example 1: REST CRUD Endpoints -- one resource, four verbs. (co-01)

GET/POST/PUT/DELETE each take their OWN path to the SAME /tasks resource.
This example routes every verb to its own handler over one in-memory store
and verifies each verb produces the effect its RFC 9110 semantics promise.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-01: the shape every handler below returns -- status + body
class Response:
    status: int  # => the HTTP status code this verb produced
    body: dict[str, object] = field(default_factory=dict[str, object])  # => resource or error payload


STORE: dict[int, str] = {1: "Write tests", 2: "Ship feature"}  # => co-01: the in-memory /tasks store
NEXT_ID = [3]  # => a mutable counter cell -- the next id a POST will mint


def handle_get() -> Response:  # => GET /tasks -- READ, safe + idempotent (co-01)
    return Response(status=200, body={"tasks": {i: t for i, t in STORE.items()}})  # => returns the whole collection


def handle_post(title: str) -> Response:  # => POST /tasks -- CREATE, neither safe nor idempotent (co-01)
    new_id = NEXT_ID[0]  # => mints a brand-new id on every call
    STORE[new_id] = title  # => adds a NEW member to the collection
    NEXT_ID[0] += 1  # => advances the counter for the next create
    return Response(status=201, body={"id": new_id, "title": title})  # => 201 Created


def handle_put(task_id: int, title: str) -> Response:  # => PUT /tasks/{id} -- REPLACE, idempotent (co-01)
    if task_id not in STORE:  # => no such resource -> 404, PUT to a missing id cannot invent it here
        return Response(status=404, body={"error": "not found"})  # => 404
    STORE[task_id] = title  # => OVERWRITES the resource with the given representation
    return Response(status=200, body={"id": task_id, "title": title})  # => 200, replaced


def handle_delete(task_id: int) -> Response:  # => DELETE /tasks/{id} -- REMOVE, idempotent (co-01)
    if task_id not in STORE:  # => already gone -> 404
        return Response(status=404, body={"error": "not found"})  # => 404
    del STORE[task_id]  # => removes the member from the collection
    return Response(status=204, body={})  # => 204 No Content


get = handle_get()  # => GET: reads the collection, no side effect
print(f"GET    -> status={get.status}, tasks={get.body['tasks']}")  # => Output: 200, both seeded tasks

created = handle_post("Review PR")  # => POST: creates a new task
print(f"POST   -> status={created.status}, created={created.body}")  # => Output: 201, id=3

replaced = handle_put(1, "Write MORE tests")  # => PUT: replaces task 1's title
print(f"PUT    -> status={replaced.status}, replaced={replaced.body}")  # => Output: 200, new title

deleted = handle_delete(2)  # => DELETE: removes task 2
print(f"DELETE -> status={deleted.status}, body={deleted.body}")  # => Output: 204, empty body

print(f"final store: {STORE}")  # => Output: task 1 replaced, task 2 gone, task 3 added
