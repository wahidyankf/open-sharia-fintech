# pyright: strict
"""Example 4: 204 No Content for DELETE. (co-02)

A successful DELETE has nothing left to represent -- the resource is gone --
so RFC 9110 gives it 204 No Content: success, but an intentionally EMPTY
body, distinct from 200 OK's "success, and here is a representation."
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-02: status plus a body kept as a plain str for a trivial emptiness check
class Response:
    status: int  # => the HTTP status code
    body: str  # => kept as a plain str so an EMPTY body is trivially checkable ("" == empty)


STORE: dict[int, str] = {1: "Draft task", 2: "Another task"}  # => two seeded resources to delete from


def delete_task(task_id: int) -> Response:  # => DELETE /tasks/{id}
    if task_id not in STORE:  # => no such resource -- nothing to delete
        return Response(status=404, body="not found")  # => 404, the resource never existed
    del STORE[task_id]  # => co-02: the resource is now genuinely gone from the store
    return Response(status=204, body="")  # => co-02: 204 -- success, deliberately empty body


response = delete_task(1)  # => delete the one seeded task
print(f"status={response.status}, body={response.body!r}")  # => Output: status=204, body=''
assert response.status == 204  # => co-02: confirms the "no content" status
assert response.body == ""  # => confirms the body is genuinely empty, not e.g. "null"
assert 1 not in STORE  # => confirms the underlying resource really was removed
print(f"remaining in store: {STORE}")  # => Output: only task 2 remains
