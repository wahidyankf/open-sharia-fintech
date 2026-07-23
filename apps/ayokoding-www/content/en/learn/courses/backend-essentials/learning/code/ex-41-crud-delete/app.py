"""Example 41: CRUD -- Delete."""

# => the "D" in CRUD -- one DELETE endpoint, backed by repository.delete_task(),
#    which reports back whether a row actually existed to remove
from fastapi import FastAPI, HTTPException  # => HTTPException raises FastAPI's default error shape

import repository  # => co-14: the module that owns EVERY database detail for this example

app = FastAPI()  # => the ASGI application uvicorn will serve
repository.init_db()  # => fresh, seeded tasks.db for every run


@app.delete("/tasks/{task_id}", status_code=204)  # => co-03: 204 -- success, no body
def delete_task(task_id: int) -> None:  # => task_id arrives already parsed as an int
    removed = repository.delete_task(task_id)  # => co-14: delegates the DELETE
    if not removed:  # => the ONLY branch this handler makes -- everything else lives in the repo
        raise HTTPException(status_code=404)  # => distinguishes "gone" from "never existed"
