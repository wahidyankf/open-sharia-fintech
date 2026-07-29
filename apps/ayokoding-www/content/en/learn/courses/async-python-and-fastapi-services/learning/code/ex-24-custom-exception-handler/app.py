"""Example 24: Mapping a Domain Error with a Custom Handler.

A registered exception handler maps a whole CLASS of domain errors to a JSON response, so handlers raise a
plain domain exception and the framework decides the status + body. Run: uvicorn app:app --port 8000, then:
curl -i localhost:8000/items/999  (co-17)
"""

from fastapi import FastAPI, Request  # => Request is passed to every exception handler (co-17)
from fastapi.responses import JSONResponse  # => a raw JSON response the handler returns (co-17)

app = FastAPI()  # => the ASGI application uvicorn serves


class NotFoundError(Exception):  # => a DOMAIN error -- no HTTP concepts live here (co-17)
    def __init__(self, resource: str, ident: int) -> None:  # => carries the facts of the failure
        self.resource = resource  # => what kind of thing was missing
        self.ident = ident  # => which one


@app.exception_handler(NotFoundError)  # => register ONE handler for the whole exception class (co-17)
async def handle_not_found(request: Request, exc: NotFoundError) -> JSONResponse:  # => maps domain -> HTTP
    _ = request  # => the request is available (for logging/tracing) but unused in this mapping
    # => every NotFoundError now becomes a 404 with a consistent envelope, no per-handler status code (co-17)
    return JSONResponse(  # => the response the framework sends instead of a 500
        status_code=404,  # => the status this domain error maps to
        content={"error": {"code": "not_found", "resource": exc.resource, "id": exc.ident}},  # => a structured body (co-17)
    )


@app.get("/items/{item_id}")  # => a route that raises the DOMAIN error directly
async def read_item(item_id: int) -> dict[str, str]:  # => handler stays free of HTTP status code details
    if item_id != 1:  # => a stand-in for "this id is not in the store"
        raise NotFoundError("item", item_id)  # => a plain domain exception -- the handler decides nothing about HTTP
    return {"item_id": str(item_id)}  # => the found case, as JSON (co-14)
