# pyright: strict
"""Example 3: 201 Created + Location. (co-02)

A successful POST that creates a resource returns 201 Created AND a Location
header pointing at the new resource -- the status alone never says WHERE the
new thing lives; the header does. Source: RFC 9110 Sec 15.3.2.
"""

from dataclasses import dataclass, field  # => field: gives the headers dict its own factory


@dataclass  # => co-02: the two facts a caller needs -- status, and where the resource landed
class Response:
    status: int  # => the HTTP status code
    headers: dict[str, str] = field(default_factory=dict[str, str])  # => response headers (Location lives here)
    body: dict[str, object] = field(default_factory=dict[str, object])  # => the created resource representation


STORE: dict[int, dict[str, object]] = {}  # => in-memory resource store, keyed by id
NEXT_ID = [1]  # => a mutable counter cell -- the next id a create will mint


def create_task(title: str) -> Response:  # => POST /tasks -- creates a new subordinate resource
    new_id = NEXT_ID[0]  # => mints a fresh id for this new resource
    resource: dict[str, object] = {"id": new_id, "title": title}  # => the created representation
    STORE[new_id] = resource  # => persists it so a follow-up GET could find it
    NEXT_ID[0] += 1  # => advances the counter for the next create
    location = f"/tasks/{new_id}"  # => co-02: the URI of the JUST-CREATED resource
    return Response(status=201, headers={"Location": location}, body=resource)  # => 201 + Location, co-02's pair


response = create_task("Deploy to staging")  # => run the handler once
print(f"status={response.status}")  # => Output: 201
print(f"Location={response.headers['Location']}")  # => Output: /tasks/1
assert response.status == 201  # => co-02: confirms the status half of the contract
assert response.headers["Location"] == "/tasks/1"  # => confirms the Location half
print(f"created: {response.body}")  # => Output: the created representation, echoed back
