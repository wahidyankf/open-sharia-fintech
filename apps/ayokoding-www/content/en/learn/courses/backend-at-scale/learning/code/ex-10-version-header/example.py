# pyright: strict
"""Example 10: Versioning via a Request Header. (co-03)

Selecting the version from a request header (e.g. Stripe's `Stripe-Version`)
keeps the URL identical across versions but asks the client to opt into one.
The trade-off: a cache keyed only on the URL now needs extra configuration to
avoid conflating two versions under the same cached URL.
"""

from dataclasses import dataclass  # => a small typed response record for each version


@dataclass  # => co-03: one version's own response shape
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object]  # => the version-specific representation


@dataclass  # => co-03: a request carries a path AND a version-selecting header
class Request:
    path: str  # => the (version-free) resource path
    headers: dict[str, str]  # => the version is selected HERE, not in the URL


def tasks_v1() -> Response:  # => the original representation
    return Response(200, {"version": 1, "tasks": [{"id": 1, "title": "Legacy task"}]})  # => v1 shape


def tasks_v2() -> Response:  # => the evolved representation (a field added)
    return Response(200, {"version": 2, "tasks": [{"id": 1, "title": "Legacy task", "status": "open"}]})  # => v2 adds status


VERSION_HEADER = "X-API-Version"  # => the header name this API selects the version with


def route(request: Request) -> Response:  # => a header-based router -- the URL is the SAME for both versions
    version = request.headers.get(VERSION_HEADER, "1")  # => defaults to v1 when the header is absent
    if version == "1":  # => co-03: the client opted into v1 (or sent nothing)
        return tasks_v1()  # => v1 handler
    if version == "2":  # => co-03: the client opted into v2
        return tasks_v2()  # => v2 handler
    return Response(404, {"error": f"unknown version {version}"})  # => an unrecognized version


default_req = Request(path="/tasks", headers={})  # => no version header -> defaults to v1
print(f"no header (default v1): version={route(default_req).body['version']}")  # => Output: 1

v1_req = Request(path="/tasks", headers={VERSION_HEADER: "1"})  # => explicitly v1
print(f"header=1:               version={route(v1_req).body['version']}")  # => Output: 1

v2_req = Request(path="/tasks", headers={VERSION_HEADER: "2"})  # => explicitly v2 -- SAME path as v1
print(f"header=2:               version={route(v2_req).body['version']}")  # => Output: 2

# Same URL, two versions: a cache keyed only on /tasks would conflate them -- the header-versioning trade-off.
assert route(v1_req).body["version"] == 1 and route(v2_req).body["version"] == 2  # => co-03
print("same path '/tasks' served versions 1 and 2 by header")  # => Output: header routing confirmed
