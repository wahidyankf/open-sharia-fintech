"""Example 25: PATCH Partial."""

from fastapi import FastAPI  # => the web framework this whole tier builds on
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

app = FastAPI()  # => the ASGI application uvicorn will serve

# => one seeded record, module-level, to demonstrate a partial update against it
tasks: dict[int, dict[str, object]] = {1: {"title": "draft", "done": False}}


class TaskPatch(BaseModel):  # => every field optional, PATCH only touches what is sent
    """Every field optional -- PATCH only touches fields the client actually sent."""

    # => only "done" is modeled here -- a real TaskPatch would list every
    # => field ALLOWED to change, each defaulted to None the same way
    done: bool | None = None  # => None means "the client did not send this field"


@app.patch("/tasks/{task_id}")  # => PATCH means "partially update" (RFC 5789)
def update_task(task_id: int, patch: TaskPatch) -> dict[str, object]:
    """Only fields present in the patch (not None) overwrite the stored task."""
    # => compare directly with Example 24's PUT: PATCH's model makes every
    # => field OPTIONAL (contrast Item's required "name"), and this handler
    # => checks "is not None" before writing, instead of unconditionally replacing
    if patch.done is not None:  # => "title" is untouched -- it was never sent
        tasks[task_id]["done"] = patch.done  # => only THIS field ever changes
    return tasks[task_id]  # => "title" survives unchanged from before the PATCH
