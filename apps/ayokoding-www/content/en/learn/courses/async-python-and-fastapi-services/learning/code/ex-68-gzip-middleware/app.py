"""Example 68: Compressing Responses with GZip Middleware.

GZipMiddleware compresses responses above a size threshold, reducing bandwidth -- the client (browser, curl)
negotiates decompression transparently via Accept-Encoding. Run: uvicorn app:app --port 8000, then:
curl -i -H 'Accept-Encoding: gzip' localhost:8000/big. (co-18)
"""

from fastapi import FastAPI  # => the web framework (co-18)
from fastapi.middleware.gzip import GZipMiddleware  # => the gzip middleware (co-18)

app = FastAPI()  # => the ASGI application uvicorn serves
app.add_middleware(GZipMiddleware, minimum_size=64)  # => compress responses >= 64 bytes (co-18)


@app.get("/big")  # => a route returning a body large enough to trigger compression
def big() -> dict[str, str]:  # => minimal handler
    return {"data": "x" * 500}  # => a 500-char body -- well over the 64-byte threshold (co-14)
