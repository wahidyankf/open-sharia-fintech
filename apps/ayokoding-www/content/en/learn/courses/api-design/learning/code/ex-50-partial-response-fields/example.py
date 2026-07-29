# pyright: strict
"""Example 50: ?fields= Selects a Subset of Returned Fields. (co-31)

`?fields=name,email` lets a caller ask for only the fields it needs --
fewer bytes on the wire, and no need to discard unused data the way a
full-record response would force the caller to.
"""

FULL_ARTICLE = {  # => co-31: the FULL resource, before any field selection is applied
    "id": 1,  # => always small, always included
    "title": "Hello, API Design",  # => the field a caller might actually want
    "body": "A very long article body..." * 20,  # => large -- exactly what field selection lets a caller skip
    "author": "Ada",  # => another optional field
}  # => end of FULL_ARTICLE


def get_article(fields: str | None) -> dict[str, object]:  # => GET /articles/1?fields=
    if fields is None:  # => co-31: no selection given -- return everything
        return dict(FULL_ARTICLE)  # => a full copy of the resource
    requested = fields.split(",")  # => co-31: parses the comma-separated field list
    return {key: FULL_ARTICLE[key] for key in requested if key in FULL_ARTICLE}  # => co-31: only those fields


full = get_article(fields=None)  # => request 1: no selection -- gets everything
print(f"full response has {len(full)} fields: {sorted(full.keys())}")  # => Output: all 4 fields

filtered = get_article(fields="id,title")  # => request 2: asks for ONLY id and title
# => filtered has 2 keys, not 4 -- the large "body" field never crosses the wire at all
print(f"filtered response: {filtered}")  # => Output: {'id': 1, 'title': 'Hello, API Design'} -- co-31
