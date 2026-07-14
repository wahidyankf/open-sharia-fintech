"""Example 34: A Consistent 404 Envelope Across Methods."""  # => module docstring for this example

# => the same domain error, the same handler, and the same shared helper
# => serve BOTH a GET route and a DELETE route below -- consistency by construction
from fastapi import FastAPI, Request  # => Request gives the handler access to the raw ASGI request
from fastapi.responses import JSONResponse  # => the response type this handler builds by hand

app = FastAPI()  # => the ASGI application uvicorn will serve


class TaskNotFoundError(Exception):  # => the same domain error shape as Example 33
    def __init__(self, task_id: int) -> None:  # => constructor
        self.task_id = task_id  # => the id the caller asked for and did not get


@app.exception_handler(TaskNotFoundError)  # => co-11: ONE handler, reused by every route below
async def task_not_found_handler(  # => co-11: registered handler's signature spans three lines
    request: Request,
    exc: TaskNotFoundError,  # => exc carries the id that was missing
) -> JSONResponse:  # => must return a Response FastAPI can send back to the client
    return JSONResponse(  # => builds the 404 envelope by hand, once, for every caller
        status_code=404,  # => co-03: identical status for every caller of this handler
        content={  # => the JSON body FastAPI serializes and sends back to the client
            "error": {  # => nests everything under ONE top-level key, matching Example 33's shape
                "code": "task_not_found",  # => a stable, machine-matchable code
                "message": f"task {exc.task_id} does not exist",  # => a human-readable summary
            }  # => closes the inner "error" object
        },  # => closes the "content" dict passed to JSONResponse
    )  # => closes the JSONResponse(...) call itself


_TASKS: dict[int, str] = {1: "Buy milk"}  # => a tiny in-memory store for this example


def _require_task(task_id: int) -> str:  # => a small shared helper both routes call
    if task_id not in _TASKS:  # => the SAME check, regardless of which route called it
        raise TaskNotFoundError(task_id)  # => the SAME error, regardless of HTTP method
    return _TASKS[task_id]  # => the found-case return value


@app.get("/tasks/{task_id}")  # => co-12: GET reads
def get_task(task_id: int) -> dict[str, str]:  # => task_id arrives already parsed as an int
    return {"title": _require_task(task_id)}  # => delegates the existence check to the shared helper


@app.delete("/tasks/{task_id}", status_code=204)  # => co-02: DELETE removes
def delete_task(task_id: int) -> None:  # => 204 means "no body" -- there is nothing to return
    _require_task(task_id)  # => raises the SAME error for a missing id as GET does
    del _TASKS[task_id]  # => only reached once the id is confirmed to exist
