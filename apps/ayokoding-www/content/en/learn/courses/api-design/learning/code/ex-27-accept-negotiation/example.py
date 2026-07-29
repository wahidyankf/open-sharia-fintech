# pyright: strict
"""Example 27: Accept Chooses JSON vs. CSV. (co-21)

`Accept` lets a client ASK for a specific representation of the same
underlying resource. This example serves the identical article data as
either JSON or CSV depending purely on what the request's `Accept` header
requests.
"""

import json  # => stdlib: serializes the JSON representation
from dataclasses import dataclass  # => a small typed response record for this example

ARTICLE = {"id": 1, "title": "Hello, API Design"}  # => the one underlying resource, two representations


@dataclass  # => co-21: status, headers, and the negotiated body
class Response:  # => co-21: the body's shape depends entirely on what was negotiated
    status: int  # => the HTTP status code
    headers: dict[str, str]  # => carries the negotiated Content-Type
    body: str  # => the body, shaped by whichever representation was chosen


def get_article(accept_header: str) -> Response:  # => co-21: content negotiation happens HERE
    if accept_header == "text/csv":  # => the client explicitly asked for CSV
        csv_body = f"id,title\n{ARTICLE['id']},{ARTICLE['title']}"  # => the SAME data, CSV-shaped
        return Response(200, {"Content-Type": "text/csv"}, csv_body)  # => the CSV representation
    return Response(200, {"Content-Type": "application/json"}, json.dumps(ARTICLE))  # => JSON fallback
    # => default: JSON, the fallback co-21 assumes when Accept is absent or */*


json_response = get_article("application/json")  # => request 1: explicitly asks for JSON
json_line = f"JSON: Content-Type={json_response.headers['Content-Type']}, body={json_response.body}"
print(json_line)  # => Output: application/json, JSON body

csv_response = get_article("text/csv")  # => request 2: asks for CSV instead -- SAME resource
csv_line = f"CSV: Content-Type={csv_response.headers['Content-Type']}, body={csv_response.body!r}"
print(csv_line)  # => Output: two different bodies, one JSON one CSV, same underlying ARTICLE dict
# => both responses carry status 200 -- only the representation, never the outcome, was negotiated
