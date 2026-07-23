"""Example 20: Status 204 No Content."""

from fastapi import FastAPI, Response, status  # => Response lets a handler control the body directly

app = FastAPI()  # => the ASGI application uvicorn will serve


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)  # => override 200 default
def delete_task(task_id: int) -> Response:
    """204 means "succeeded, nothing more to say" -- the body MUST be empty."""
    # => task_id is accepted but never used below -- a real handler would look
    # => the row up and delete it; this example only demonstrates the STATUS line
    # => returning a bare Response (no body arg) keeps the body empty, unlike
    # => returning a dict, which FastAPI would otherwise try to serialize
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # => an empty Response object -- no JSON body is ever written to the wire
    # => RFC 9110 requires a 204 response to carry NO body at all, ever
