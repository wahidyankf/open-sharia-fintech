"""Example 51: Middleware -- CORS."""

# => co-16: unlike ex-48/49/50, this middleware ships WITH FastAPI -- configured
#    once here, not hand-written, and still applies to every route below
from fastapi import FastAPI  # => the web framework whose built-in CORS middleware this example uses
from fastapi.middleware.cors import CORSMiddleware  # => co-16: ships with FastAPI, no hand-rolling needed

app = FastAPI()  # => the ASGI application uvicorn will serve

app.add_middleware(  # => co-16: FastAPI's OWN built-in middleware, not hand-rolled
    CORSMiddleware,  # => the middleware class being registered
    allow_origins=["https://example.com"],  # => co-04: only THIS origin gets the header back
    allow_methods=["GET"],  # => only GET is permitted cross-origin for this app
)  # => closes the add_middleware(...) call


@app.get("/tasks")  # => co-08: a handler that knows NOTHING about CORS
def list_tasks() -> list[dict[str, str]]:  # => a plain handler, unaware any middleware even exists
    return [{"title": "Buy milk"}]  # => CORSMiddleware decides the header, not this function
