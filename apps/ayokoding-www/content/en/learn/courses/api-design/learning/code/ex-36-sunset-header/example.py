# pyright: strict
"""Example 36: The Sunset Header. (co-15)

RFC 8594's `Sunset` header names the DATE an endpoint will actually stop
working -- distinct from `Deprecation` (Example 35), which only says
"deprecated," with no promised retirement date attached.
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-15: status, headers (carrying the retirement date), and the still-working body
class Response:
    status: int  # => the HTTP status code -- a future sunset date does NOT change this yet
    headers: dict[str, str]  # => carries the Sunset notice
    body: dict[str, object]  # => the endpoint still returns real data, until the sunset date


def get_article_v1(article_id: int) -> Response:  # => GET /v1/articles/{id} -- a scheduled retirement
    return Response(  # => co-15: still succeeds, but names the exact retirement date
        status=200,  # => still succeeds -- Sunset alone does not reject a request
        headers={"Sunset": "Wed, 01 Jul 2026 00:00:00 GMT"},  # => co-15: RFC 8594's own date format
        body={"id": article_id, "title": "Hello"},  # => real data, right up until the sunset date
    )  # => end of the Response construction


def client_warning(response: Response) -> str | None:  # => co-15: a client that surfaces the notice
    sunset_date = response.headers.get("Sunset")  # => reads the header if present
    if sunset_date is None:  # => nothing to warn about
        return None  # => no Sunset header means no scheduled retirement
    return f"warning: this endpoint retires on {sunset_date}"  # => a human-facing warning string


response = get_article_v1(1)  # => call the endpoint with a scheduled sunset
print(f"status={response.status}, body={response.body}")  # => Output: 200, real data -- still works
warning = client_warning(response)  # => co-15: extracts the human-facing warning
# => warning is "warning: this endpoint retires on Wed, 01 Jul 2026 00:00:00 GMT" (type: str)
print(f"client sees: {warning}")  # => Output: warning naming the exact retirement date
