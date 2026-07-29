"""Example 69: CORS with Explicit Allowed Origins.

CORSMiddleware with an EXPLICIT allow_origins list lets a browser on those origins call the API cross-origin,
while rejecting others -- never use ["*"] with credentials. Run: uvicorn app:app --port 8000. (co-18)
"""

from fastapi import FastAPI  # => the web framework (co-18)
from fastapi.middleware.cors import CORSMiddleware  # => the CORS middleware (co-18)

app = FastAPI()  # => the ASGI application uvicorn serves
app.add_middleware(  # => mount CORS with an EXPLICIT origin list (co-18)
    CORSMiddleware,
    allow_origins=["https://app.example.com"],  # => ONLY this origin may call cross-origin (co-18)
    allow_methods=["GET", "POST"],  # => limit to the methods the frontend actually uses
    allow_headers=["Authorization", "Content-Type"],  # => limit to the headers the frontend sends
)


@app.get("/")  # => a route a browser on app.example.com can call cross-origin
def read_root() -> dict[str, str]:  # => minimal handler
    return {"msg": "cors-ok"}  # => a permitted origin's browser receives this (co-14)
