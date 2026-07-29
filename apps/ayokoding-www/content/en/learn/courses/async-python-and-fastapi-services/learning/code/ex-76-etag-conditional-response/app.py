"""Example 76: ETag and Conditional Responses.

The server stamps a response with an ETag (a content hash); a client that sends If-None-Match with a matching
ETag gets a 304 (empty body) instead of the full payload -- saving bandwidth on unchanged resources.
Run: uvicorn app:app --port 8000, then: curl -i -H 'If-None-Match: "v1"' localhost:8000/doc. (co-17, co-14)
"""

import hashlib  # => a stable content hash for the ETag (co-14)

from fastapi import FastAPI, Request, Response  # => Request reads If-None-Match (co-17)

app = FastAPI()  # => the ASGI application uvicorn serves

BODY = b'{"doc":"hello"}'  # => the (fixed) resource body for this example
ETAG = '"' + hashlib.md5(BODY).hexdigest() + '"'  # => a content-derived ETag (co-14)


@app.get("/doc")  # => a route supporting conditional responses
async def doc(request: Request) -> Response:  # => returns a Response so we can set headers/status directly
    if request.headers.get("if-none-match") == ETAG:  # => the client already has this exact version (co-17)
        return Response(status_code=304, headers={"ETag": ETAG})  # => 304 Not Modified -- no body sent (co-17)
    return Response(content=BODY, media_type="application/json", headers={"ETag": ETAG})  # => full payload + ETag (co-14)
