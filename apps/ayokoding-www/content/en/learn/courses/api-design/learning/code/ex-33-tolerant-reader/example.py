# pyright: strict
"""Example 33: The Tolerant Reader -- a Client That Ignores Unknown Fields. (co-14, co-02)

Consumer-driven design (co-02) means a client reads defensively: it extracts
ONLY the fields it needs via `.get()`, so a server adding an unrelated field
never breaks it -- the client tolerates what it does not recognize.
"""

from dataclasses import dataclass  # => a small typed record for what THIS client actually needs


@dataclass  # => co-02: only the fields this ONE client cares about, nothing more
class ClientView:
    id: int  # => the only field this client reads
    title: str  # => the only OTHER field this client reads


def tolerant_read(response: dict[str, object]) -> ClientView:  # => co-14/co-02: reads defensively
    return ClientView(  # => builds the client's own narrow view of a possibly-larger response
        id=response.get("id", 0),  # type: ignore[arg-type]  # => co-02: .get(), never response["id"]
        title=response.get("title", ""),  # type: ignore[arg-type]  # => co-02: tolerates a missing key too
    )  # => end of the ClientView construction


v1_response: dict[str, object] = {"id": 1, "title": "Hello"}  # => the ORIGINAL server shape
v2_response: dict[str, object] = {"id": 1, "title": "Hello", "author": "Ada", "views": 42}
# => co-14: the server later added TWO new fields the client never asked about

view_from_v1 = tolerant_read(v1_response)  # => reads the original shape
print(f"from v1 response: {view_from_v1}")  # => Output: ClientView(id=1, title='Hello')

view_from_v2 = tolerant_read(v2_response)  # => co-02: reads the EXPANDED shape identically
# => view_from_v2 == view_from_v1 -- the two extra keys never even reach ClientView
print(f"from v2 response (unaffected): {view_from_v2}")  # => Output: identical -- new fields ignored
