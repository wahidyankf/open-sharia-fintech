"""Example 33: A Domain Exception Handler."""  # => module docstring for this example

# => the exception class below knows NOTHING about HTTP -- no status code, no
# => JSON -- that translation happens in exactly one place, the handler below
from fastapi import FastAPI, Request  # => Request gives the handler access to the raw ASGI request
from fastapi.responses import JSONResponse  # => the response type this handler builds by hand

app = FastAPI()  # => the ASGI application uvicorn will serve


class TaskNotFoundError(Exception):  # => a DOMAIN error -- knows nothing about HTTP
    def __init__(self, task_id: int) -> None:  # => constructor
        self.task_id = task_id  # => the id the caller asked for and did not get


@app.exception_handler(TaskNotFoundError)  # => co-11: maps the domain error to an HTTP shape
async def task_not_found_handler(  # => co-11: registered handler's signature spans three lines
    request: Request,
    exc: TaskNotFoundError,  # => exc carries the id that was missing
) -> JSONResponse:  # => must return a Response FastAPI can send back to the client
    return JSONResponse(  # => builds the 404 envelope by hand, same shape as Example 32's 422
        status_code=404,  # => co-03: not-found status, decided HERE, not in the handler
        content={  # => the JSON body FastAPI serializes and sends back to the client
            "error": {  # => nests everything under ONE top-level key, matching Example 32's shape
                "code": "task_not_found",  # => a stable, machine-matchable code
                "message": f"task {exc.task_id} does not exist",  # => a human-readable summary
            }  # => closes the inner "error" object
        },  # => closes the "content" dict passed to JSONResponse
    )  # => closes the JSONResponse(...) call itself


_TASKS: dict[int, str] = {1: "Buy milk", 2: "Walk dog"}  # => a tiny in-memory store for this example


@app.get("/tasks/{task_id}")  # => co-12: a typed path parameter
def get_task(task_id: int) -> dict[str, str]:  # => task_id arrives already parsed as an int
    if task_id not in _TASKS:  # => the handler stays free of any HTTP-status knowledge
        raise TaskNotFoundError(task_id)  # => co-24: raise the DOMAIN error, let it be mapped
    return {"title": _TASKS[task_id]}  # => the found-case return value
