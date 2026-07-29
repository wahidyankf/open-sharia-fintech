"""Example 65: Domain Exception Handlers Registered Centrally.

Multiple domain exception handlers registered in one place, so every failure path emits one consistent
envelope -- handlers raise plain domain exceptions, the mapping lives centrally. Run: uvicorn app:app --port 8000.
(co-17)
"""

from fastapi import FastAPI, Request  # => Request is passed to every handler (co-17)
from fastapi.responses import JSONResponse  # => the JSON response each handler returns (co-17)

app = FastAPI()  # => the ASGI application uvicorn serves


class NotFoundError(Exception):  # => a domain error -> 404
    pass


class ConflictError(Exception):  # => a domain error -> 409
    pass


def _envelope(code: str, status: int) -> JSONResponse:  # => one consistent shape for every error (co-17)
    return JSONResponse(status_code=status, content={"error": {"code": code}})  # => the uniform envelope


@app.exception_handler(NotFoundError)  # => map NotFoundError -> 404 (co-17)
async def handle_not_found(request: Request, exc: NotFoundError) -> JSONResponse:  # => central mapping
    _ = request, exc  # => available for logging, unused in the mapping
    return _envelope("not_found", 404)  # => 404


@app.exception_handler(ConflictError)  # => map ConflictError -> 409 (co-17)
async def handle_conflict(request: Request, exc: ConflictError) -> JSONResponse:  # => central mapping
    _ = request, exc  # => available for logging
    return _envelope("conflict", 409)  # => 409


@app.get("/items/{item_id}")  # => a route that raises a domain error
async def read_item(item_id: int) -> dict[str, str]:  # => handler stays free of HTTP status details
    if item_id == 0:  # => stand-in condition
        raise NotFoundError()  # => mapped centrally to 404 (co-17)
    if item_id == 1:  # => another stand-in condition
        raise ConflictError()  # => mapped centrally to 409 (co-17)
    return {"item_id": str(item_id)}  # => the success path (co-14)
