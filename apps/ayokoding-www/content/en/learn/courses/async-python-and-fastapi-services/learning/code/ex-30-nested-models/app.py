"""Example 30: Nested Pydantic Models Serialize Together.

A model that contains a list of other models serializes the whole nested shape to JSON in one step.
Run: uvicorn app:app --port 8000, then: curl localhost:8000/order  (co-12, co-14)
"""

from fastapi import FastAPI  # => the web framework (co-10)
from pydantic import BaseModel  # => Pydantic models (co-12)

app = FastAPI()  # => the ASGI application uvicorn serves


class LineItem(BaseModel):  # => a NESTED model -- used inside another model
    sku: str  # => a product identifier
    quantity: int  # => a count


class Order(BaseModel):  # => a CONTAINING model -- it composes nested models (co-12)
    order_id: int  # => a top-level field
    items: list[LineItem]  # => a LIST of nested models -- serialized recursively (co-14)


@app.get("/order", response_model=Order)  # => returns the whole nested shape as one JSON document
def get_order() -> Order:  # => the handler returns a fully-constructed nested model
    return Order(  # => one constructor call builds the entire tree (co-12)
        order_id=1,  # => top-level scalar
        items=[LineItem(sku="A", quantity=2), LineItem(sku="B", quantity=1)],  # => nested list of models
    )  # => Pydantic serializes every level to JSON automatically (co-14)
