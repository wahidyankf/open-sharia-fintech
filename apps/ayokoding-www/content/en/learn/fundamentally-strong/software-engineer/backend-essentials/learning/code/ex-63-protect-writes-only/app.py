"""Example 63: Protect Writes Only -- GET is open, POST/PUT/DELETE require a token."""
# => co-02, co-18: a very common real-world policy -- ANYONE can read the catalog, but only an
# => authenticated caller can change it. The HTTP method itself decides which rule applies below.

from fastapi import Depends, FastAPI, HTTPException, Request  # => co-02: method-sensitive protection
from fastapi.responses import JSONResponse  # => co-11: builds the exception handler's structured body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer  # => co-18: parses "Bearer <token>"

app = FastAPI()  # => a fresh app -- this example needs no database, only an in-memory dict below

VALID_TOKEN = "s3cr3t-token-abc123"  # => hardcoded stand-in for a real signed/opaque token
security = HTTPBearer(auto_error=False)  # => auto_error=False: WE own the 401 body's shape below
ITEMS: dict[int, str] = {1: "milk", 2: "bread"}  # => in-memory store -- fine for this pedagogical example
# => (two seed rows so list_items() below has something visibly non-empty to return before any write)
NEXT_ID = 3  # => module-level counter for the next inserted id (co-05 caveat: not multi-worker safe --
# => Example 80 revisits this exact tension with a REAL, two-process-shared SQLite file instead)


@app.exception_handler(HTTPException)  # => co-11: one consistent {"error": {...}} envelope, unwrapped
async def structured_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    body = (
        exc.detail
        if isinstance(exc.detail, dict)  # => the raise below always supplies a dict already
        else {"error": {"code": "error", "message": str(exc.detail)}}  # => fallback for a plain string
    )
    return JSONResponse(status_code=exc.status_code, content=body)  # => co-11: same shape, every error


def require_token(  # => co-18: this dependency is opted into ONLY by write routes below --
    # => note the return type is None, not str -- this variant doesn't need the resolved identity,
    # => only the yes/no decision of whether the request is allowed to proceed at all
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> None:
    if credentials is None or credentials.credentials != VALID_TOKEN:  # => co-18: either failure mode
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "unauthorized", "message": "missing or invalid token"}},
        )
    # => co-18: no `return` needed -- reaching the end of this function IS the "allowed" outcome;
    # => FastAPI just runs the dependency for its side effect (raise-or-don't) and discards None


@app.get("/items")  # => co-02: GET has NO Depends(require_token) at all -- reads are open to everyone
# => co-02: read methods (GET, HEAD) are conventionally safe/idempotent -- open access here mirrors that
def list_items() -> dict[int, str]:
    return ITEMS  # => co-02: no auth check anywhere on this path -- curl with zero headers succeeds


@app.post("/items", dependencies=[Depends(require_token)])  # => co-02, co-18: WRITE guarded --
# => `dependencies=[...]` runs require_token for its SIDE EFFECT ONLY, without injecting a
# => parameter into create_item's own signature below -- the route itself never sees the token value
def create_item(name: str) -> dict[str, int | str]:
    global NEXT_ID  # => mutates the module-level counter -- co-05: this is process-local state,
    # => exactly the kind of in-memory mutation that breaks the moment a second worker exists
    item_id = NEXT_ID
    ITEMS[item_id] = name  # => the actual write this token protects
    NEXT_ID += 1  # => co-05: NOT atomic across concurrent requests in a real multi-threaded deployment
    return {"id": item_id, "name": name}  # => co-02: 200 by default here, unlike ex-19's explicit 201


@app.delete("/items/{item_id}", dependencies=[Depends(require_token)])  # => co-02, co-18: WRITE guarded --
# => same dependencies=[...] pattern as the POST route above -- consistent policy, one line each
# => co-02: DELETE, POST, and (in a real app) PUT/PATCH all share this exact same guard style
def delete_item(item_id: int) -> dict[str, bool]:
    ITEMS.pop(item_id, None)  # => the actual write this token protects -- second-arg None means
    # => "don't raise KeyError if item_id doesn't exist," making delete naturally idempotent (co-02)
    return {"deleted": True}  # => co-02: reports success even if the id was already gone -- by design
