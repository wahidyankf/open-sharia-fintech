from typing import TypedDict


class ErrorBody(TypedDict):  # => co-11: one FIXED shape every error path returns, never a bare string
    code: str
    message: str
    detail: object | None


class ErrorEnvelope(TypedDict):  # => the full response body wrapping ErrorBody
    status: int
    error: ErrorBody


def error_envelope(status: int, code: str, message: str, detail: object | None = None) -> ErrorEnvelope:
    # => co-11: a single constructor every failure path calls -- guarantees UNIFORM shape (co-24: ex-77's idea)
    return {"status": status, "error": {"code": code, "message": message, "detail": detail}}


not_found = error_envelope(404, "not_found", "task 42 does not exist")  # => co-03: a missing resource
unauthorized = error_envelope(401, "unauthorized", "missing or invalid bearer token")  # => co-18's failure
server_fault = error_envelope(500, "internal_error", "unexpected failure")  # => co-11: NEVER a stack trace

print(not_found)  # => Output: {'status': 404, 'error': {'code': 'not_found', 'message': 'task 42 does not exist', 'detail': None}}
print(unauthorized)  # => Output: {'status': 401, 'error': {'code': 'unauthorized', 'message': 'missing or invalid bearer token', 'detail': None}}
print(server_fault)  # => Output: {'status': 500, 'error': {'code': 'internal_error', 'message': 'unexpected failure', 'detail': None}}

# => every envelope this function produces shares the EXACT same top-level keys, regardless of status
assert set(not_found.keys()) == set(unauthorized.keys()) == set(server_fault.keys()) == {"status", "error"}
assert not_found["status"] == 404
assert unauthorized["error"]["code"] == "unauthorized"
print("kata-08 OK")
