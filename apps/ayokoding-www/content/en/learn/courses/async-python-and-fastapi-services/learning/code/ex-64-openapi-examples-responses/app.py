"""Example 64: OpenAPI Examples and Documented Responses.

Field(examples=...) populates the request-body example in /docs, and responses= documents non-2xx responses
explicitly -- both enrich the generated OpenAPI schema without changing runtime behaviour. Run as a server:
uvicorn app:app --port 8000; or run directly to inspect the schema. (co-20)
"""

from fastapi import FastAPI, HTTPException  # => HTTPException is one documented response (co-17)
from pydantic import BaseModel, Field  # => Field carries examples (co-12)

app = FastAPI()  # => the ASGI application uvicorn serves


class Item(BaseModel):  # => a body model with an example (co-20)
    name: str = Field(examples=["widget"])  # => the example appears in /docs (co-20)


@app.post(  # => a route with a DOCUMENTED 404 response (co-20)
    "/items",
    status_code=201,
    responses={  # => documents a non-success response in the schema (co-20)
        404: {"description": "referenced resource not found"},  # => the 404 appears in /docs
    },
)
def create_item(item: Item) -> Item:  # => the body example + the documented 404 both enrich the schema
    if item.name == "missing":  # => a stand-in condition that produces the documented 404 (co-17)
        raise HTTPException(status_code=404, detail="referenced resource not found")  # => matches the doc above
    return item  # => the success path (co-14)


if __name__ == "__main__":  # => run directly to inspect the documented responses
    schema = app.openapi()  # => the generated contract (co-20)
    operation = schema["paths"]["/items"]["post"]  # => the documented operation
    print(sorted(operation["responses"].keys()))  # => Output: ['201', '404'] -- both documented (co-20)
