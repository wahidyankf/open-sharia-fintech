"""Example 56: Forbidding Extra Fields with Model Config.

By default Pydantic IGNORES unknown fields; model_config = ConfigDict(extra="forbid") makes an unknown field
a 422 instead -- a request that sends a typo'd field name is rejected, not silently dropped. Run as a server:
uvicorn app:app --port 8000; or run directly to inspect. (co-12, co-13)
"""

from fastapi import FastAPI  # => the web framework (co-10)
from pydantic import BaseModel, ConfigDict  # => ConfigDict tunes model behaviour (co-12)

app = FastAPI()  # => the ASGI application uvicorn serves


class StrictItem(BaseModel):  # => a model that REJECTS unknown fields (co-13)
    model_config = ConfigDict(extra="forbid")  # => an unknown field becomes a 422 (co-12)
    name: str  # => the only accepted field


@app.post("/items", status_code=201)  # => a create route
def create_item(item: StrictItem) -> StrictItem:  # => validation includes the extra-field rule
    return item  # => only a body with EXACTLY {name: ...} reaches here


if __name__ == "__main__":  # => run directly to demonstrate the rule in-process
    ok = StrictItem(name="widget")  # => accepted -- exactly the declared field
    print(ok.model_dump())  # => Output: {'name': 'widget'}
    import pydantic  # => to catch the ValidationError below

    try:
        StrictItem(name="widget", extra="oops")  # => an UNKNOWN field -- forbidden by the config (co-13)
        raised = False
    except pydantic.ValidationError:
        raised = True
    print(raised)  # => Output: True -- the extra field was rejected
