"""Example 54: Hand-Written Accept Header Negotiation."""  # => module docstring for this example

from fastapi import Depends, FastAPI, Header, HTTPException  # => Header() reads a request header

app = FastAPI()  # => the ASGI application uvicorn will serve
# => co-21: FastAPI does NOT enforce `Accept` negotiation on its own. Its built-in
# => strict_content_type_checking only validates the REQUEST's Content-Type; nothing
# => in the framework inspects `Accept` -- the dependency below is entirely hand-written


def require_json_accept(accept: str = Header(default="*/*")) -> None:  # => co-21: a FastAPI dependency
    # => co-21: a DEPENDENCY that runs BEFORE the handler -- accepts "application/json"
    # => (or any wildcard that matches it) and rejects everything else with a 406
    if "application/json" not in accept and "*/*" not in accept:  # => the entire negotiation rule
        raise HTTPException(status_code=406, detail="only application/json is supported")  # => co-21: 406


@app.get("/tasks", dependencies=[Depends(require_json_accept)])  # => runs on EVERY call to this route
def list_tasks() -> list[dict[str, str]]:  # => a plain handler, reached only after the dependency passes
    return [{"title": "Buy milk"}]  # => only reached once require_json_accept() did not raise
