# pyright: strict
"""Example 7: 204 No Content for DELETE. (co-07)

A successful DELETE has nothing left to represent -- the resource is gone --
so RFC 9110 gives it `204 No Content`: success, but an intentionally EMPTY
body, distinct from `200 OK`'s "success, and here is a representation."
"""

from dataclasses import dataclass  # => a small typed response record for this example

STORE: dict[int, str] = {1: "Draft article"}  # => one seeded resource to delete
# => STORE is {1: 'Draft article'} (type: dict[int, str]) before the delete runs


@dataclass  # => co-07: status plus a body kept as a plain str for a trivial emptiness check
class Response:
    status: int  # => the HTTP status code
    body: str  # => kept as a plain str so an EMPTY body is trivially checkable ("" == empty)


def delete_article(article_id: int) -> Response:  # => DELETE /articles/{id}
    del STORE[article_id]  # => co-07: the resource is now genuinely gone from the store
    return Response(status=204, body="")  # => co-07: 204 -- success, deliberately empty body


response = delete_article(1)  # => delete the one seeded article
# => response is Response(status=204, body='') -- key 1 no longer in STORE
print(f"status={response.status}, body={response.body!r}")  # => Output: status=204, body=''
assert response.status == 204  # => co-07: confirms the "no content" status
assert response.body == ""  # => confirms the body is genuinely empty, not e.g. "null"
assert 1 not in STORE  # => confirms the underlying resource really was removed
