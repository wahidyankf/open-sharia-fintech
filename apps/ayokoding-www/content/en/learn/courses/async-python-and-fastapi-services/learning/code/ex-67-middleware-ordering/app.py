"""Example 67: Middleware Ordering Matters.

Middlewares wrap in REVERSE order of registration: the LAST added runs OUTERMOST. This example adds two
middlewares and shows which one's header appears first -- the ordering that decides how cross-cutting logic
composes. Run: uvicorn app:app --port 8000, then: curl -i localhost:8000/. (co-18)
"""

from fastapi import FastAPI  # => the web framework (co-18)

app = FastAPI()  # => the ASGI application uvicorn serves


@app.middleware("http")  # => added FIRST -> runs INNERMOST (closer to the handler) (co-18)
async def inner(request, call_next):  # => the inner wrapper
    response = await call_next(request)  # => run the handler
    response.headers["X-Inner"] = "1"  # => added close to the handler
    return response


@app.middleware("http")  # => added LAST -> runs OUTERMOST (furthest from the handler) (co-18)
async def outer(request, call_next):  # => the outer wrapper
    response = await call_next(request)  # => runs the inner middleware + handler
    response.headers["X-Outer"] = "1"  # => added furthest out
    return response


@app.get("/")  # => a route wrapped by both middlewares
def read_root() -> dict[str, str]:  # => minimal handler
    return {"msg": "ok"}  # => the response carries BOTH X-Inner and X-Outer headers (co-18)
