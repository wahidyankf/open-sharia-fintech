# pyright: strict
"""Example 51: JSON:API Sparse Fieldsets. (co-31, co-28)

JSON:API's `fields[type]=` parameter selects a sparse fieldset the SAME way
Example 50 does, but wraps the result in JSON:API's own
`data`/`type`/`id`/`attributes` envelope -- co-28's standardized hypermedia shape.
"""

FULL_ATTRIBUTES = {"title": "Hello, API Design", "body": "A long body...", "author": "Ada"}
# => co-31: the full attribute set, before sparse-fieldset selection


def jsonapi_response(resource_id: str, resource_type: str, fields: str | None) -> dict[str, object]:
    # => GET /articles/1?fields[articles]=title -- co-28: the JSON:API envelope shape
    attributes = FULL_ATTRIBUTES  # => defaults to every attribute
    if fields is not None:  # => co-31: a sparse fieldset was explicitly requested
        requested = fields.split(",")  # => parses the comma-separated attribute list
        attributes = {k: v for k, v in FULL_ATTRIBUTES.items() if k in requested}  # => co-31: only those
    return {  # => co-28: the standardized JSON:API top-level envelope
        "data": {"type": resource_type, "id": resource_id, "attributes": attributes}  # => co-28's own shape
    }  # => end of the envelope


full = jsonapi_response("1", "articles", fields=None)  # => request 1: no sparse fieldset
print(f"full: {full}")  # => Output: all three attributes, wrapped in the JSON:API envelope

sparse = jsonapi_response("1", "articles", fields="title")  # => request 2: only "title" requested
# => sparse["data"]["attributes"] has exactly 1 key -- the top-level envelope shape never changes
print(f"sparse: {sparse}")  # => Output: only title, still wrapped in the SAME envelope shape
