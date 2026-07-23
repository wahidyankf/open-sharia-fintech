"""Example 42: CRUD -- Missing Id Returns a 404 Envelope."""  # => module docstring for this example

# => combines the DB-backed UPDATE/DELETE from Example 40/41 with the shared
# => envelope pattern from Example 33/34 -- now BOTH sources of truth agree
from fastapi import FastAPI, Request  # => Request gives the handler access to the raw ASGI request
from fastapi.responses import JSONResponse  # => the response type this handler builds by hand
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

import repository  # => co-14: the module that owns EVERY database detail for this example

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.init_db()  # => fresh, seeded tasks.db for every run


class TaskNotFoundError(Exception):  # => the same envelope-shaped domain error as ex-33/ex-34
    def __init__(self, task_id: int) -> None:  # => constructor
        self.task_id = task_id  # => the id the caller asked for and did not get


@app.exception_handler(TaskNotFoundError)  # => co-11: ONE handler for BOTH routes below
async def task_not_found_handler(  # => co-11: registered handler's signature spans three lines
    request: Request,
    exc: TaskNotFoundError,  # => exc carries the id that was missing
) -> JSONResponse:  # => must return a Response FastAPI can send back to the client
    return JSONResponse(  # => builds the 404 envelope by hand, shared by PUT and DELETE below
        status_code=404,  # => co-03: identical status for every caller of this handler
        content={  # => the JSON body FastAPI serializes and sends back to the client
            "error": {  # => nests everything under ONE top-level key, matching ex-33/ex-34
                "code": "task_not_found",  # => a stable, machine-matchable code
                "message": f"task {exc.task_id} does not exist",  # => a human-readable summary
            }  # => closes the inner "error" object
        },  # => closes the "content" dict passed to JSONResponse
    )  # => closes the JSONResponse(...) call itself


class TaskUpdate(BaseModel):  # => the shape of a valid PUT /tasks/{id} body
    title: str  # => co-10: validated before the handler ever sees it


@app.put("/tasks/{task_id}")  # => co-02: PUT against a real, repository-backed store now
def update_task(task_id: int, task: TaskUpdate) -> dict[str, object]:  # => path param + validated body
    changed = repository.update_task(task_id, task.title)  # => co-14: delegates the UPDATE
    if not changed:  # => the ONLY branch this handler makes -- everything else lives in the repo
        raise TaskNotFoundError(task_id)  # => same envelope, now driven by rowcount==0
    return {"id": task_id, "title": task.title}  # => echoes the id + the value that was just written


@app.delete("/tasks/{task_id}", status_code=204)  # => co-03: 204 -- success, no body
def delete_task(task_id: int) -> None:  # => task_id arrives already parsed as an int
    removed = repository.delete_task(task_id)  # => co-14: delegates the DELETE
    if not removed:  # => the ONLY branch this handler makes -- everything else lives in the repo
        raise TaskNotFoundError(task_id)  # => the SAME error class as the PUT branch above
