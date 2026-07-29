# pyright: strict
"""Example 10: The Stateless Constraint. (co-03)

Fielding's stateless constraint says every request carries ALL the context
the server needs -- no session remembered between calls. This example proves
it by handling two requests with TWO INDEPENDENT handler instances (no
shared session dict) and showing both still succeed identically.
"""

from dataclasses import dataclass  # => a small typed record for one self-contained request


@dataclass  # => co-03: everything the server needs travels WITH the request
class Request:
    token: str  # => auth, carried on every call -- never assumed remembered from a prior one
    path: str  # => the resource path this one request targets


def handle(request: Request) -> str:  # => a FRESH call each time -- no session state read
    if request.token != "valid-token":  # => co-03: the check reads ONLY this request's own field
        return "401 Unauthorized"  # => rejected -- purely from this request's own token
    return f"200 OK: served {request.path} using only this request's own token"  # => co-03: self-sufficient


# Two "server instances" -- simulated by literally not sharing any object between the calls.
request_a = Request(token="valid-token", path="/articles/1")  # => request 1, its OWN full context
result_a = handle(request_a)  # => handled with zero memory of any earlier call
# => result_a is "200 OK: served /articles/1 using only this request's own token"
print(f"instance A: {result_a}")  # => Output: 200 OK

request_b = Request(token="valid-token", path="/articles/2")  # => request 2, ALSO its own context
result_b = handle(request_b)  # => a completely independent call -- same outcome either way
print(f"instance B: {result_b}")  # => Output: 200 OK -- co-03: neither call depended on the other
