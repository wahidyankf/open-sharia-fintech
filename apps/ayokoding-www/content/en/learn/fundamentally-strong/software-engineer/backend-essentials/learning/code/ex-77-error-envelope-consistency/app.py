"""Example 77: Error Envelope Consistency -- every error path shares one shape."""
# => co-11: five DIFFERENT failure kinds (400, 401, 404, 422, 500) below, all rendered through
# => the SAME `envelope()` helper -- a client parses exactly one shape, regardless of WHICH failed

from fastapi import Depends, FastAPI, Header, HTTPException, Request  # => co-23: Depends wires 401 in
from fastapi.exceptions import RequestValidationError  # => co-10: FastAPI's own validation failure type
from fastapi.responses import JSONResponse  # => co-11: builds every exception handler's body below
from pydantic import BaseModel  # => co-10: validates the POST body, feeding the 422 path
# => co-11: five handlers below, one shared helper -- this file is the single reference for
# => "what does an error look like in this app," regardless of which route or dependency raised it


def envelope(code: str, message: str) -> dict[str, dict[str, str]]:  # => co-11: the ONE shape every
    # => error path in this app returns -- a machine-readable `code` plus a human-readable `message`
    return {"error": {"code": code, "message": message}}


app = FastAPI()  # => a fresh app -- this example needs only enough state to trigger each error kind
# => (fully self-contained: nothing here is imported from any other example directory)


@app.exception_handler(HTTPException)  # => co-11: catches every raise HTTPException(...) in this app --
# => this handler alone is what turns FastAPI's default {"detail": ...} nesting into {"error": {...}}
async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict):  # => a route already built a structured envelope itself
        return JSONResponse(status_code=exc.status_code, content=exc.detail)  # => used as-is, unwrapped
    return JSONResponse(  # => a route raised HTTPException(status_code=X, detail="plain string")
        status_code=exc.status_code, content=envelope("error", str(exc.detail))
    )  # => co-11: normalized into the SAME envelope shape either way


@app.exception_handler(RequestValidationError)  # => co-10, co-11: FastAPI's own 422 gets the SAME shape --
# => without THIS handler, a validation failure would ship FastAPI's default {"detail": [...]} array instead
async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    first = exc.errors()[0]  # => co-11: names the OFFENDING field, same spirit as an earlier example's
    # => detail array -- only the FIRST error is surfaced, keeping the envelope's message a single string
    field = ".".join(str(loc) for loc in first["loc"])  # => co-11: e.g. "body.title" for a missing field
    return JSONResponse(  # => co-11: SAME shape as the HTTPException handler above, code differs
        status_code=422, content=envelope("validation_error", f"{field}: {first['msg']}")
    )


@app.exception_handler(Exception)  # => co-11: the LAST resort -- catches anything else, sanitized --
# => registration ORDER matters here: FastAPI checks the more specific handlers above FIRST
async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(  # => co-11: the SAME two-key {"error": {code, message}} shape as every
        # => OTHER handler in this file -- a client never needs to special-case a 500 differently
        status_code=500,
        content=envelope("internal_error", "an unexpected error occurred"),
    )  # => co-11: NEVER leaks exc's message or a stack trace to the client -- deliberately generic


TASKS = {1: "write the report"}  # => a tiny in-memory store, just enough to trigger each error kind --
# => id 1 exists (drives the 200 path), any other id drives the 404 path further down
VALID_TOKEN = "s3cr3t-token-abc123"  # => hardcoded stand-in for a real signed/opaque token


class CreateTask(BaseModel):  # => co-10: the POST body's expected shape --
    # => this is the model VALIDATED before create_task's own body even runs, per co-10
    title: str  # => co-10: required -- omitting it triggers the 422 path


def require_token(  # => co-04, co-18: 401 trigger -- reused via Depends() on the write route below
    authorization: str | None = Header(default=None),  # => co-04: MUST be Header(), not a bare
    # => default -- FastAPI treats an unannotated `str | None = None` as a QUERY param instead
) -> None:
    if authorization != f"Bearer {VALID_TOKEN}":  # => co-18: either missing entirely or genuinely wrong
        raise HTTPException(status_code=401, detail=envelope("unauthorized", "missing or invalid token"))


@app.get("/tasks/{task_id}")  # => co-03, co-11: the 404 trigger -- path params validate their
# => TYPE automatically (a non-integer id is a 422), but existence is business logic, checked below
def get_task(task_id: int) -> dict[str, str]:
    if task_id not in TASKS:  # => co-03: any id besides the single seeded one below triggers this
        raise HTTPException(status_code=404, detail=envelope("not_found", "no such task"))
    return {"title": TASKS[task_id]}  # => co-11: the ONLY success-path response in this whole file


@app.get("/tasks")  # => co-03, co-11: the 400 trigger -- a semantically bad input Pydantic can't catch
def list_tasks(bad: bool = False) -> dict[str, str]:
    if bad:  # => a deliberate business-rule violation, not a type/shape error -- co-10 validation
        # => would happily accept `bad=true` as a well-formed bool; THIS check is business logic, not typing
        raise HTTPException(status_code=400, detail=envelope("bad_request", "the bad=true flag is rejected"))
    return {"count": str(len(TASKS))}  # => co-11: the ordinary, unguarded success path


@app.post("/tasks", dependencies=[Depends(require_token)])  # => co-10, co-11: the 422 trigger, if
# => `title` is omitted from the body -- and separately, the 401 trigger if no valid token is sent
def create_task(body: CreateTask) -> dict[str, str]:
    return {"title": body.title}  # => co-11: unreachable without BOTH a valid token and a valid body


@app.get("/boom")  # => co-11: the 500 trigger -- an unhandled exception, sanitized by the handler above
def boom() -> dict[str, str]:
    raise RuntimeError("a genuinely unexpected internal failure")  # => never reaches the client verbatim --
    # => the generic Exception handler above catches THIS and every other undeclared exception type
