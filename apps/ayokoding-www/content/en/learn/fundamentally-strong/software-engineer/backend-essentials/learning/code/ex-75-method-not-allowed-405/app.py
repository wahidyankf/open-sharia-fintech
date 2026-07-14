"""Example 75: Method Not Allowed -- an unsupported method returns 405 with an Allow header."""
# => co-03: FastAPI/Starlette handle THIS status code entirely automatically -- there is no
# => `raise HTTPException(405)` anywhere in this file; the 405 comes purely from route registration

from fastapi import FastAPI  # => co-16: no other import needed -- routing alone drives this example

app = FastAPI()  # => a fresh app -- this example needs no database, only route registration


@app.get("/tasks")  # => co-02: ONLY GET is registered for this exact path -- no PUT/POST/DELETE at all
def list_tasks() -> list[str]:
    return ["write the report"]  # => a fixed, single-item list -- this example never mutates state


@app.post("/reports")  # => a DIFFERENT path, registered with ONLY POST -- proves Allow is per-PATH
def create_report() -> dict[str, str]:
    return {"created": "true"}  # => reachable only via POST -- GET /reports itself would 405 too


# => co-03: RFC 9110 SS15.5.6 requires a 405 response to carry an Allow header listing the method(s)
# => that path genuinely supports -- Starlette (FastAPI's ASGI toolkit) generates this automatically.
# => VERIFIED NUANCE: when a single path has multiple decorators (e.g. both @app.get("/x") and
# => @app.post("/x")), Starlette's 405 Allow header reflects only the FIRST-matched route object,
# => not the union of every decorator for that path -- which is exactly why this example keeps
# => /tasks and /reports as two separate, single-method paths instead.
