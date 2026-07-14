"""Example 32: A Custom Error Envelope."""

# => FastAPI's DEFAULT 422 body is {"detail": [...]} -- fine for debugging,
#    awkward for a client that expects one stable {"error": {code, message}} shape
from fastapi import FastAPI, Request  # => Request gives the handler access to the raw ASGI request
from fastapi.exceptions import RequestValidationError  # => the exception FastAPI raises internally
from fastapi.responses import JSONResponse  # => the response type this handler builds by hand
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

app = FastAPI()  # => the ASGI application uvicorn will serve


class TaskCreate(BaseModel):  # => the shape of a valid POST /tasks body
    title: str  # => required, no default


@app.exception_handler(RequestValidationError)  # => overrides FastAPI's DEFAULT 422 handler
async def validation_exception_handler(
    request: Request,  # => unused here, but FastAPI's handler signature always passes it
    exc: RequestValidationError,  # => exc carries every violation FastAPI found
) -> JSONResponse:  # => must return a Response FastAPI can send back to the client
    # => co-11: reshape the default {"detail": [...]} array into a bespoke,
    #    project-specific envelope -- {"error": {"code", "message"}}
    first_error = exc.errors()[0]  # => take the first offending field for a concise message
    field = ".".join(  # => joins the loc TUPLE into one dotted field path string
        str(part)
        for part in first_error["loc"]
        if part != "body"  # => drops the generic "body" segment
    )  # => e.g. "title" (drops the generic "body" location segment)
    return JSONResponse(  # => builds the bespoke envelope BY HAND -- no automatic reshaping exists
        status_code=422,  # => co-03: still 422 -- only the BODY shape changed, not the status
        content={  # => the JSON body FastAPI serializes and sends back to the client
            "error": {  # => nests everything under ONE top-level key, unlike the default array
                "code": "validation_error",  # => a stable, machine-matchable code
                "message": f"{field}: {first_error['msg']}",  # => a human-readable summary
            }  # => closes the inner "error" object
        },  # => closes the "content" dict passed to JSONResponse
    )  # => closes the JSONResponse(...) call itself


@app.post("/tasks", status_code=201)  # => co-08: a handler for creating a task
def create_task(task: TaskCreate) -> dict[str, str]:  # => "task" only exists if validation passed
    return {"title": task.title}  # => the happy path is untouched by the envelope override
