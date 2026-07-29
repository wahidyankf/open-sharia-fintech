# pyright: strict
"""Example 35: The Deprecation Header. (co-15)

RFC 9745's `Deprecation` header notifies a caller that an endpoint (or the
whole API version) is deprecated, optionally paired with a `Link` header
pointing at the replacement -- notification only, the endpoint still works.
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-15: status, headers (carrying the notice), and the still-working body
class Response:  # => co-15: deprecation is signaled via headers, never via a different status
    status: int  # => the HTTP status code -- deprecation does NOT change this
    headers: dict[str, str]  # => carries the Deprecation + Link notice
    body: dict[str, object]  # => the endpoint still returns real data


def get_article_v1(article_id: int) -> Response:  # => GET /v1/articles/{id} -- now deprecated
    return Response(  # => co-15: still succeeds, but carries a notice
        status=200,  # => the request STILL succeeds -- deprecation is a notice, not a rejection
        headers={  # => the two headers RFC 9745 defines for this purpose
            "Deprecation": "true",  # => co-15: signals this endpoint is deprecated
            "Link": '</v2/articles/1>; rel="successor-version"',  # => co-15: points at the replacement
        },  # => end of the headers dict
        body={"id": article_id, "title": "Hello"},  # => the deprecated endpoint's own real data
    )  # => end of the Response construction


response = get_article_v1(1)  # => call the deprecated endpoint
print(f"status={response.status}, body={response.body}")  # => Output: 200, real data -- still works
print(f"Deprecation={response.headers['Deprecation']}")  # => Output: Deprecation=true
print(f"Link={response.headers['Link']}")  # => Output: points at the v2 successor
# => a client can automate migration by parsing the Link header's rel="successor-version"
