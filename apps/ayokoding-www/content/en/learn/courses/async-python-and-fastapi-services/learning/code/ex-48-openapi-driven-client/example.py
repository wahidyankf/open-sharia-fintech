"""Example 48: An OpenAPI Driven Typed Client.

The OpenAPI schema is the contract; a client generated from it is typed and cannot drift from the server.
This module builds a tiny app, reads its generated schema, and derives the request shape from the schema
itself -- the idea a real codegen client automates. Run: python3 example.py. (co-20)
"""

from fastapi import FastAPI  # => the web framework (co-10)
from pydantic import BaseModel  # => Pydantic models (co-12)


def build_app() -> FastAPI:  # => a small service whose schema drives the client below
    app = FastAPI()  # => the ASGI app

    class Item(BaseModel):  # => a request/response model (co-12)
        name: str

    @app.get("/items/{item_id}")  # => one path operation
    def read_item(item_id: int) -> dict[str, int]:  # => a typed path param (co-11)
        return {"item_id": item_id}

    @app.post("/items")  # => another path operation
    def create_item(item: Item) -> Item:  # => a typed body (co-12)
        return item

    return app


def main() -> None:  # => derives the client's request shape FROM the schema (co-20)
    app = build_app()  # => build the service
    schema = app.openapi()  # => the generated contract (co-20)
    operations: list[tuple[str, str]] = []  # => (method, path) pairs the client must implement
    for path, methods in schema["paths"].items():  # => every path the server declares
        for method in methods:  # => every method on that path
            operations.append((method.upper(), path))  # => one operation the client can call
    print(operations)  # => Output: [('GET', '/items/{item_id}'), ('POST', '/items')]
    # => a real codegen client turns each operation into a typed method -- contract parity, for free (co-20)


if __name__ == "__main__":  # => run directly
    main()  # => prints the schema-derived operation list
