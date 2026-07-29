# pyright: strict
"""Example 9: Versioning via the URI Path -- /v1/ vs /v2/. (co-03)

Routing the version into the URI path (/v1/tasks vs /v2/tasks) is the
strategy Google's AIP-185 names ("major version in the URI, e.g. v1 not
v1.0"). The version lives in the URL, so an HTTP cache or CDN naturally
treats each version as a distinct entry with no special config.
"""

from collections.abc import Callable  # => Callable: the type of the version-specific handlers
from dataclasses import dataclass  # => a small typed response record for each version


@dataclass  # => co-03: one version's own response shape -- v1 and v2 differ deliberately
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object]  # => the version-specific representation


def tasks_v1() -> Response:  # => /v1/tasks -- the original representation (title only)
    return Response(200, {"version": 1, "tasks": [{"id": 1, "title": "Legacy task"}]})  # => co-03: v1 shape


def tasks_v2() -> Response:  # => /v2/tasks -- the evolved representation (title + status added)
    return Response(200, {"version": 2, "tasks": [{"id": 1, "title": "Legacy task", "status": "open"}]})  # => co-03: v2 adds a field


ROUTES: dict[str, Callable[[], Response]] = {"/v1/tasks": tasks_v1, "/v2/tasks": tasks_v2}  # => co-03: version baked INTO the path


def route(path: str) -> Response:  # => a tiny path-based router
    handler = ROUTES.get(path)  # => looks up the handler for this exact versioned path
    if handler is None:  # => unknown path or unknown version -> 404
        return Response(404, {"error": f"no route for {path}"})  # => 404
    return handler()  # => invokes the version-specific handler


v1 = route("/v1/tasks")  # => resolves to the v1 handler
print(f"/v1/tasks -> status={v1.status}, body={v1.body}")  # => Output: version 1, title only

v2 = route("/v2/tasks")  # => resolves to the v2 handler
print(f"/v2/tasks -> status={v2.status}, body={v2.body}")  # => Output: version 2, title + status

missing = route("/v3/tasks")  # => a version that was never published -> 404
print(f"/v3/tasks -> status={missing.status}, body={missing.body}")  # => Output: 404

assert v1.body["version"] == 1 and v2.body["version"] == 2  # => co-03: each version resolves to its own handler
