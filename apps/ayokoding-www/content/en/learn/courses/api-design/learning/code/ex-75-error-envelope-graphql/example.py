# pyright: strict
"""Example 75: GraphQL Partial Errors vs REST problem+json. (co-30, co-08)

REST signals failure via the STATUS CODE (Example 6's `problem+json`, a
non-2xx status); GraphQL signals failure via an `errors` ARRAY alongside a
`data` object that may be PARTIALLY populated -- the HTTP status stays 200
even when part of the query failed.
"""

from typing import Any  # => both error shapes are arbitrary nested JSON


def rest_error_response(article_id: int) -> tuple[int, dict[str, Any]]:  # => co-08: REST's own error shape
    status = 404  # => co-08: the FAILURE is communicated via the status code itself
    body = {  # => RFC 9457's application/problem+json envelope (Example 6)
        "type": "https://example.com/probs/not-found",  # => a URI identifying this problem TYPE
        "title": "Article Not Found",  # => a short, human-readable summary
        "status": status,  # => co-08: the SAME status, echoed inside the body too
        "detail": f"No article with id {article_id}",  # => specific to THIS occurrence
    }  # => end of the problem+json body
    return status, body  # => co-08: status and body travel together, as one failure signal


def graphql_response_with_partial_error() -> dict[str, Any]:  # => co-30: GraphQL's own error shape
    return {  # => co-30: status stays 200 -- the FAILURE lives entirely inside this body
        "data": {"article": {"id": "1", "title": "Hello"}, "comments": None},  # => co-30: PARTIAL success
        "errors": [  # => co-30: a list -- MULTIPLE fields can fail independently in one response
            {"message": "Comments service unavailable", "path": ["comments"]}  # => co-30: WHICH field failed
        ],  # => end of errors
    }  # => end of the GraphQL response


rest_status, rest_body = rest_error_response(999)  # => co-08: a REST call for a missing article
print(f"REST: status={rest_status}, body={rest_body}")  # => Output: 404, full problem+json body

graphql_body = graphql_response_with_partial_error()  # => co-30: a GraphQL call where ONE field failed
# => the transport-level status for this call is 200 -- the failure lives entirely in "errors"
print(f"GraphQL: status=200 (always), body={graphql_body}")  # => Output: 200, article present, comments failed

article_succeeded = graphql_body["data"]["article"] is not None  # => co-30: this field's data IS present
comments_failed = graphql_body["data"]["comments"] is None  # => co-30: this field's data is NOT present
print(f"GraphQL partial success: article ok={article_succeeded}, comments failed={comments_failed}")
# => Output: True, True -- co-30: one field's failure did not fail the WHOLE response
