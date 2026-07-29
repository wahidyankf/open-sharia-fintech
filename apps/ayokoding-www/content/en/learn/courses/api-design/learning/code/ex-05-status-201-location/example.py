# pyright: strict
"""Example 5: 201 Created + Location. (co-07)

A successful POST that creates a resource returns `201 Created` AND a
`Location` header pointing at the new resource -- the status code alone
never says WHERE the new thing lives; the header does.
"""

from dataclasses import dataclass, field  # => field: gives the dict param its own factory type


@dataclass  # => a small typed response record, reused by every status-code example
class Response:  # => co-07: the two facts a client needs -- status, and where the resource landed
    status: int  # => the HTTP status code
    headers: dict[str, str] = field(default_factory=dict[str, str])  # => response headers, typed
    # => default_factory avoids the classic "mutable default argument" bug


def create_article(title: str) -> Response:  # => POST /articles handler
    new_id = 42  # => a fixed id for this self-contained example (a real store would mint one)
    location = f"/articles/{new_id}"  # => co-07: the URI of the JUST-CREATED resource
    # => location is "/articles/42" (type: str)
    return Response(status=201, headers={"Location": location})  # => 201 + Location, co-07's pair


response = create_article("Hello, API Design")  # => run the handler once
# => response is Response(status=201, headers={'Location': '/articles/42'})
print(f"status={response.status}")  # => Output: status=201
print(f"Location={response.headers['Location']}")  # => Output: Location=/articles/42
assert response.status == 201  # => co-07: confirms the status half of the contract
assert response.headers["Location"] == "/articles/42"  # => confirms the Location half
