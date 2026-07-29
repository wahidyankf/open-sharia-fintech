# pyright: strict
"""Example 73: Evolving v1 -> v2 With a Deprecation Window. (co-13, co-15)

A real migration serves BOTH versions simultaneously for a window: v1
carries Examples 35-36's `Deprecation`/`Sunset` headers while still
working, and v2 (Example 29's URI-path strategy) serves the new shape --
callers migrate on their own schedule, within the stated window.
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-15: status, headers (carrying the migration notice on v1 only), and the body
class Response:  # => co-13/co-15: the SAME shape serves both v1 and v2 responses
    status: int  # => the HTTP status code -- identical for v1 and v2 while both are served
    headers: dict[str, str]  # => empty for v2, carries Deprecation+Sunset for v1
    body: dict[str, object]  # => v1's older shape vs v2's newer shape


def get_article_v1(article_id: int) -> Response:  # => co-13: the OLD path, still served during the window
    return Response(  # => co-15: still works, but flagged for retirement
        status=200,  # => v1 still succeeds -- this IS the deprecation window, not an outage
        headers={  # => co-15: BOTH migration-notice headers, together
            "Deprecation": "true",  # => Example 35: signals deprecation
            "Sunset": "Wed, 01 Jul 2026 00:00:00 GMT",  # => Example 36: names the exact retirement date
        },  # => end of the headers dict
        body={"id": article_id, "title": "Hello"},  # => co-13: the OLDER response shape
    )  # => end of the v1 Response construction


def get_article_v2(article_id: int) -> Response:  # => co-13: the NEW path, the migration TARGET
    return Response(  # => co-13: no deprecation headers -- this is the CURRENT, supported version
        status=200,  # => v2 also succeeds
        headers={},  # => co-13: nothing to warn about -- v2 has no retirement scheduled
        body={"id": article_id, "title": "Hello", "author": "Ada"},  # => co-13: the NEWER, additive shape
    )  # => end of the v2 Response construction


v1_response = get_article_v1(1)  # => a caller still on the OLD path, during the window
print(f"v1: status={v1_response.status}, deprecated={'Deprecation' in v1_response.headers}")  # => Output: True

v2_response = get_article_v2(1)  # => a caller ALREADY migrated to the NEW path
print(f"v2: status={v2_response.status}, deprecated={'Deprecation' in v2_response.headers}")  # => Output: False

both_serve_now = v1_response.status == 200 and v2_response.status == 200  # => co-13: the window's own promise
# => both_serve_now is True -- neither caller is forced to migrate on someone else's schedule
print(f"both versions serve during the window: {both_serve_now}")  # => Output: True
