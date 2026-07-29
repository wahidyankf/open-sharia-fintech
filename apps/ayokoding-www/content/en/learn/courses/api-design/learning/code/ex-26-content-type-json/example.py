# pyright: strict
"""Example 26: Content-Type: application/json. (co-21)

`Content-Type` tells the RECEIVER how to interpret the bytes in the body --
without it, a client cannot safely assume a response body is JSON at all.
This example sets the header on the server side, then a client parses the
body using exactly that header as its cue.
"""

import json  # => stdlib: (de)serializes the body itself
from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-21: status, headers, and the raw body TEXT before any parsing
class Response:
    status: int  # => the HTTP status code
    headers: dict[str, str]  # => carries the Content-Type declaration
    body: str  # => the raw bytes-as-text, before any parsing happens


def get_article() -> Response:  # => a handler that serializes its own body as JSON
    body = json.dumps({"id": 1, "title": "Hello"})  # => co-21: the body's actual encoding
    # => body is '{"id": 1, "title": "Hello"}' (type: str)
    return Response(status=200, headers={"Content-Type": "application/json"}, body=body)
    # => co-21: the header DECLARES what the body just above actually is


def client_parse(response: Response) -> object:  # => a client that trusts the declared Content-Type
    if response.headers.get("Content-Type") == "application/json":  # => co-21: reads the cue first
        return json.loads(response.body)  # => only parses as JSON because the header said so
    raise ValueError(f"unexpected Content-Type: {response.headers.get('Content-Type')}")  # => else fail


response = get_article()  # => run the handler
parsed = client_parse(response)  # => co-21: the client's parsing DECISION is driven by the header
# => parsed is {'id': 1, 'title': 'Hello'} (type: object, runtime type dict)
print(f"Content-Type={response.headers['Content-Type']}, parsed={parsed}")  # => Output: parsed dict
