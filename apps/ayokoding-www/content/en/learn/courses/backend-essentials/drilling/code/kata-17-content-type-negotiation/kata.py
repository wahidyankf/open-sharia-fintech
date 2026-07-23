def accepts_json_body(content_type: str | None) -> tuple[bool, int]:  # => returns (should_parse, status)
    # => co-21: mirrors FastAPI's strict_content_type=True default (since 0.132.0) -- reject non-JSON bodies
    if content_type is None:  # => no Content-Type header sent at all
        return False, 422  # => co-21: still 422 -- FastAPI parses this as "body didn't match the model"
    media_type = content_type.split(";")[0].strip().lower()  # => strip a "; charset=utf-8" suffix if present
    if media_type == "application/json":  # => co-21: the only media type this endpoint accepts as JSON
        return True, 200
    return False, 422  # => co-21: NOT a 415 -- FastAPI's default has no dedicated 415 for this case


json_ct = "application/json"  # => the well-formed, expected case
json_ct_with_charset = "application/json; charset=utf-8"  # => co-21: a charset suffix must not break matching
plain_text_ct = "text/plain"  # => co-21: JSON body sent with the wrong declared Content-Type
missing_ct = None  # => co-21: no Content-Type header at all

for label, ct in [
    ("json", json_ct),
    ("json+charset", json_ct_with_charset),
    ("plain-text", plain_text_ct),
    ("missing", missing_ct),
]:
    accepted, status = accepts_json_body(ct)
    print(label, accepted, status)
    # => Output rows: json True 200 / json+charset True 200 / plain-text False 422 / missing False 422

assert accepts_json_body(json_ct) == (True, 200)
assert accepts_json_body(json_ct_with_charset) == (True, 200)  # => co-21: charset suffix tolerated
assert accepts_json_body(plain_text_ct) == (False, 422)  # => co-21: rejected -- a framework default, not hand-written
assert accepts_json_body(missing_ct) == (False, 422)
print("kata-17 OK")
