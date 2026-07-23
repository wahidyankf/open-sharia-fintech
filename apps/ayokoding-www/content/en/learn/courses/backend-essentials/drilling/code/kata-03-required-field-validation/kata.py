def validate_required(body: dict[str, object], required: list[str]) -> dict[str, object] | None:  # => co-10/co-11: reject bad shapes with a 422 BEFORE handler logic runs
    missing = [field for field in required if field not in body]  # => every required field not present
    if not missing:  # => nothing missing -- the body is shaped correctly, no error to return
        return None
    return {  # => co-11: a consistent JSON error envelope, never a bare stack trace
        "status": 422,  # => co-03: 422 Unprocessable Content, defined natively in RFC 9110 Section 15.5.21
        "error": {
            "code": "validation_error",
            "message": "missing required field(s)",
            "detail": missing,  # => names EXACTLY which fields were missing, for the caller to fix
        },
    }


good_body: dict[str, object] = {"title": "Ship report", "owner": "alice"}
bad_body: dict[str, object] = {"title": "Ship report"}  # => "owner" is missing
required_fields = ["title", "owner"]

good_result = validate_required(good_body, required_fields)  # => nothing missing
bad_result = validate_required(bad_body, required_fields)  # => "owner" missing
print(good_result)  # => Output: None
print(bad_result)  # => Output: {'status': 422, 'error': {'code': 'validation_error', 'message': 'missing required field(s)', 'detail': ['owner']}}

assert good_result is None  # => a fully-shaped body produces no error envelope at all
assert bad_result is not None
assert bad_result["status"] == 422
error = bad_result["error"]
assert isinstance(error, dict) and error["detail"] == ["owner"]  # => names the exact missing field
print("kata-03 OK")
