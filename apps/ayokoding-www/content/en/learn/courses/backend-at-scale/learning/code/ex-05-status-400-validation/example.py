# pyright: strict
"""Example 5: 400 Bad Request -- a malformed payload. (co-02)

A syntactically malformed request body (wrong type, missing required field)
is rejected with 400 Bad Request -- the server never reaches business logic
because the payload could not be parsed into the expected shape.
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-02: status plus a small error body
class Response:
    status: int  # => the HTTP status code
    body: dict[str, str]  # => either an error message or the accepted payload


def parse_task_payload(raw: dict[str, object]) -> tuple[Response, str | None]:  # => returns (response, parsed title)
    # => co-02: validate BEFORE touching the store -- a malformed body is a 400, not a business error
    if "title" not in raw:  # => the required field is missing entirely
        return Response(400, {"error": "missing required field: title"}), None  # => 400, malformed
    title_value = raw["title"]  # => the value present at the title key
    if not isinstance(title_value, str):  # => the title is present but the WRONG TYPE (e.g. an int)
        return Response(400, {"error": "title must be a string"}), None  # => 400, malformed
    if title_value == "":  # => present and a string, but empty -- still malformed for this endpoint
        return Response(400, {"error": "title must not be empty"}), None  # => 400, malformed
    return Response(202, {"accepted": title_value}), title_value  # => accepted shape (202 just signals "ok" here)


missing = parse_task_payload({})  # => no title key at all
print(f"missing title:    status={missing[0].status}, body={missing[0].body}")  # => Output: 400

wrong_type = parse_task_payload({"title": 42})  # => title present but not a string
print(f"wrong type:       status={wrong_type[0].status}, body={wrong_type[0].body}")  # => Output: 400

empty = parse_task_payload({"title": ""})  # => title present, a string, but empty
print(f"empty title:      status={empty[0].status}, body={empty[0].body}")  # => Output: 400

ok = parse_task_payload({"title": "Valid task"})  # => a well-formed payload
print(f"well-formed:      status={ok[0].status}, body={ok[0].body}")  # => Output: 202, accepted

assert missing[0].status == 400 and wrong_type[0].status == 400 and empty[0].status == 400  # => co-02: all three are 400
