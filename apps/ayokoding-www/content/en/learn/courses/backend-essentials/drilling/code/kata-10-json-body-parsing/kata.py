import json
from typing import cast


def parse_json_body(raw_body: str) -> tuple[dict[str, object] | None, str | None]:
    # => co-09/co-13: (de)serialize the raw request body into a typed Python object for the handler
    try:
        parsed = json.loads(raw_body)  # => co-09: JSON text -> Python value (json.loads returns Any)
    except json.JSONDecodeError as exc:  # => co-13: malformed body -- must NOT crash the handler
        return None, f"invalid JSON: {exc.msg}"  # => a caller-facing reason, not a raw traceback (co-11)
    if not isinstance(parsed, dict):  # => co-13: the handler expects an OBJECT body, not a bare list/number
        return None, "request body must be a JSON object"
    return cast(dict[str, object], parsed), None  # => JSON objects always have str keys -- safe to narrow


good_raw = '{"title": "Ship report", "done": false}'  # => a well-formed JSON object body
malformed_raw = '{"title": "Ship report",}'  # => a trailing comma -- invalid JSON syntax
wrong_shape_raw = "[1, 2, 3]"  # => valid JSON, but not an OBJECT -- still not usable as a request body

good_parsed, good_error = parse_json_body(good_raw)
malformed_parsed, malformed_error = parse_json_body(malformed_raw)
wrong_shape_parsed, wrong_shape_error = parse_json_body(wrong_shape_raw)

print(good_parsed, good_error)  # => Output: {'title': 'Ship report', 'done': False} None
print(malformed_parsed, malformed_error is not None)  # => Output: None True
print(wrong_shape_parsed, wrong_shape_error)  # => Output: None request body must be a JSON object

assert good_parsed == {"title": "Ship report", "done": False} and good_error is None
assert malformed_parsed is None and malformed_error is not None  # => rejected, not silently truncated
assert wrong_shape_parsed is None and wrong_shape_error == "request body must be a JSON object"
print("kata-10 OK")
